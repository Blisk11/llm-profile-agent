# src/llm_wrapper.py
from __future__ import annotations
import time
import threading
import hashlib
from typing import Dict, Tuple
from mistralai.models import SDKError
from src.profile_loader import client, PROFILE_CONTEXT, BANNED_KEYWORDS

# Simple in-memory answer cache: key=(mode, prompt_hash) -> (answer, timestamp)
_CACHE: Dict[Tuple[str, str], Tuple[str, float]] = {}
_CACHE_TTL_SECONDS = 900  # 15 minutes
_CACHE_MAX_ITEMS = 200

# Throttling (rudimentary): minimum seconds between calls
_MIN_INTERVAL = 0.6  # adjust as needed
_last_call_ts = 0.0
_lock = threading.Lock()

FRIENDLY_OVERLOAD_MESSAGE = (
    "Mistral API temporarily overloaded (rate/capacity). "
    "Please retry in a few seconds."
)

def _cache_key(mode: str, prompt: str) -> Tuple[str, str]:
    h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    return (mode, h)

def _get_cached(mode: str, prompt: str) -> str | None:
    now = time.time()
    k = _cache_key(mode, prompt)
    entry = _CACHE.get(k)
    if not entry:
        return None
    answer, ts = entry
    if now - ts > _CACHE_TTL_SECONDS:
        _CACHE.pop(k, None)
        return None
    return answer

def _set_cached(mode: str, prompt: str, answer: str) -> None:
    if len(_CACHE) >= _CACHE_MAX_ITEMS:
        # drop oldest (simple O(n) approach)
        oldest_key = min(_CACHE.items(), key=lambda kv: kv[1][1])[0]
        _CACHE.pop(oldest_key, None)
    _CACHE[_cache_key(mode, prompt)] = (answer, time.time())

def enforce_profile(user_input: str) -> str:
    """Check if user input tries to override identity."""
    lower_input = user_input.lower()
    if any(word in lower_input for word in BANNED_KEYWORDS):
        return "Cannot comply. Instruction violates the enforced user profile."
    return user_input

def _throttle():
    global _last_call_ts
    with _lock:
        now = time.time()
        wait = _MIN_INTERVAL - (now - _last_call_ts)
        if wait > 0:
            time.sleep(wait)
        _last_call_ts = time.time()

def query_model(prompt: str, mode: str = "short") -> str:
    """Query Mistral API with profile enforcement, retries, caching & graceful degradation."""
    safe_prompt = enforce_profile(prompt)

    mode_instructions = {
        "short": "\n\nAnswer concisely (2-3 sentences).",
        "long": "\n\nProvide a detailed, structured answer with examples where relevant."
    }
    if mode not in mode_instructions:
        raise ValueError("Invalid mode. Choose 'short' or 'long'.")

    full_user_prompt = safe_prompt + mode_instructions[mode]

    # Serve from cache if present
    cached = _get_cached(mode, full_user_prompt)
    if cached:
        return cached

    # Throttle upstream calls
    _throttle()

    max_retries = 5
    base_backoff = 1.5  # seconds

    for attempt in range(max_retries):
        try:
            response = client.chat.complete(
                model="mistral-medium-latest",
                messages=[
                    {"role": "system", "content": PROFILE_CONTEXT},
                    {"role": "user", "content": full_user_prompt},
                ],
                temperature=0.0
            )
            answer = response.choices[0].message.content.strip()
            _set_cached(mode, full_user_prompt, answer)
            return answer
        except SDKError as e:
            msg = str(e)
            is_429 = "429" in msg or "capacity" in msg.lower()
            if is_429 and attempt < max_retries - 1:
                sleep_for = base_backoff * (2 ** attempt)
                time.sleep(sleep_for)
                continue
            if is_429:
                # Final failure → friendly fallback (still cache short-lived to avoid hammering)
                _set_cached(mode, full_user_prompt, FRIENDLY_OVERLOAD_MESSAGE)
                return FRIENDLY_OVERLOAD_MESSAGE
            # Non-rate error: surface concise message
            return f"Upstream API error: {msg}"

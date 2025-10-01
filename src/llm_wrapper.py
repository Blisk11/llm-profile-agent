# src/llm_wrapper.py
from src.profile_loader import client, PROFILE_CONTEXT, BANNED_KEYWORDS
import time
from mistralai.models import SDKError

def enforce_profile(user_input: str) -> str:
    """Check if user input tries to override identity"""
    lower_input = user_input.lower()
    if any(word in lower_input for word in BANNED_KEYWORDS):
        return "Cannot comply. Instruction violates the enforced user profile."
    return user_input

def query_model(prompt: str, mode: str = "short") -> str:
    """Query Mistral API with profile enforcement"""
    safe_prompt = enforce_profile(prompt)
    
    # Add mode instruction
    mode_instructions = {
        "short": "\n\nPlease answer concisely in 2-3 sentences.",
        "long": "\n\nPlease provide a detailed and thorough answer, with examples if applicable."
    }
    if mode not in mode_instructions:
        raise ValueError("Invalid mode. Choose 'short' or 'long'.")
    
    safe_prompt += mode_instructions[mode]

    # Implement exponential backoff for retries
    max_retries = 5
    backoff = 2  # seconds

    for attempt in range(max_retries):
        try:
            response = client.chat.complete(
                model="mistral-medium",
                messages=[
                    {"role": "system", "content": PROFILE_CONTEXT},
                    {"role": "user", "content": safe_prompt},
                ],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except SDKError as e:
            if "Status 429" in str(e) and attempt < max_retries - 1:
                wait_time = backoff * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            raise RuntimeError("API overloaded. Please try again later.") from e

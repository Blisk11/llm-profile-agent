# src/agent.py
from langdetect import detect
from src.profile_loader import PROFILE_DATA
from src.llm_wrapper import query_model

def _build_style_prefix(lang: str) -> str:
    style = PROFILE_DATA.get("response_style", {}).get(lang)
    if not style:
        style = PROFILE_DATA.get("response_style", {}).get("en", [])
    if isinstance(style, list):
        style_text = " ".join(style)
    else:
        style_text = str(style)
    return f"Follow these style rules: {style_text}\n"

def ask_agent(question: str, mode: str = "short") -> str:
    """
    Ask Julien Vaughan's AI agent a question.
    """
    try:
        lang = detect(question)
    except Exception:
        lang = "en"

    style_prefix = _build_style_prefix(lang)
    # Append style instructions to user question (model system context already loaded in wrapper)
    prompt = f"{style_prefix}{question}"
    return query_model(prompt, mode=mode)

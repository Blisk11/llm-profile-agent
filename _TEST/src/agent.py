# src/agent.py
from langdetect import detect
from src.profile_loader import PROFILE_DATA
from src.llm_wrapper import query_model

def ask_agent(question: str, mode: str = "short") -> str:
    """
    Ask Julien Vaughan's AI agent a question.
    - Uses centralized profile from PROFILE_DATA.
    - Supports 'short' or 'long' response modes.
    - Automatically adapts response style based on detected language.
    """
    # Detect language
    try:
        lang = detect(question)
    except Exception:
        lang = "en"  # default to English if detection fails

    # Get response style from profile
    response_style = PROFILE_DATA.get("response_style", {}).get(lang, PROFILE_DATA.get("response_style", {}).get("en", ""))

    # Construct a system prompt using profile info
    system_prompt = (
        f"You are {PROFILE_DATA.get('name', 'Julien Vaughan')}, a {PROFILE_DATA.get('role', '')} based in {PROFILE_DATA.get('location', '')}.\n"
        f"Skills: {', '.join(PROFILE_DATA.get('skills', []))}.\n"
        f"Experience: {PROFILE_DATA.get('experience', '')}.\n"
        f"{response_style}"
    )

    # Query the model
    return query_model(question, mode=mode)

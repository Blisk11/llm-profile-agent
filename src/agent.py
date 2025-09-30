import json
from pathlib import Path
from src.llm_wrapper import query_model
from langdetect import detect
from profile_loader import load_profile, load_api_key

# Local set up 
# PROFILE_PATH = Path(__file__).parent.parent / "data" / "profile.json"
#def load_profile():
#    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
#        return json.load(f)

PROFILE_DATA = load_profile()
MISTRAL_API_KEY = load_api_key("MISTRAL_API_KEY")

def ask_agent(question: str, mode: str = "short") -> str:
    profile = load_profile()

    # Detect language
    try:
        lang = detect(question)
    except:
        lang = "en"  # Default to English if detection fails

    # Fetch the appropriate response style from profile.json
    response_style = profile["response_style"].get(lang, profile["response_style"]["en"])

    # Construct the system prompt
    system_prompt = (
        f"You are {profile['name']}, a {profile['role']} based in {profile['location']}.\n"
        f"Skills: {', '.join(profile['skills'])}.\n"
        f"Experience: {profile['experience']}.\n"
        f"{response_style}"
    )

    return query_model(question, system=system_prompt, mode=mode)

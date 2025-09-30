import os
import json
import streamlit as st
from dotenv import load_dotenv

# Load local .env if it exists (development)
load_dotenv()

def load_profile():
    """
    Load profile.json locally or from Streamlit secrets in production.
    """
    # First, try Streamlit secrets
    if "profile" in st.secrets:
        return dict(st.secrets["profile"])

    # Fallback to local profile.json
    profile_path = os.path.join("data", "profile.json")
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            return json.load(f)

    raise RuntimeError("Profile data not found. Either put it in data/profile.json locally or add it to Streamlit secrets.")

def load_api_key(key_name: str) -> str:
    """
    Load API key from env var locally or Streamlit secrets in prod.
    """
    # Try Streamlit secrets first
    if key_name in st.secrets:
        return st.secrets[key_name]

    # Then fallback to environment variables
    value = os.getenv(key_name)
    if value:
        return value

    raise RuntimeError(f"API key {key_name} not found in environment variables or Streamlit secrets.")

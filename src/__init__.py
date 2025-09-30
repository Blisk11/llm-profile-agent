# src/__init__.py

"""
llm-profile-agent package
Contains:
- agent.py       : main agent logic
- llm_wrapper.py : Mistral API interface and profile enforcement
- utils.py       : helper functions
- profile_loader.py : singleton loader for profile & API client
"""

# Optional: you can expose key functions at the package level
from .agent import ask_agent
from .llm_wrapper import query_model
from .profile_loader import PROFILE_DATA, PROFILE_CONTEXT, client

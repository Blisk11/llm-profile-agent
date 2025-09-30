import os
from pathlib import Path

# Root paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Environment variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("Missing MISTRAL_API_KEY. Export it before running.")

# Default model
DEFAULT_MODEL = "mistral-medium"

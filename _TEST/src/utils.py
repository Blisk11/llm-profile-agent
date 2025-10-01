import json
from pathlib import Path

def load_json(path: Path) -> dict:
    """Load JSON file into a Python dict."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: dict) -> None:
    """Save Python dict into a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

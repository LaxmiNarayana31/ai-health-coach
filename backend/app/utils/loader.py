from pathlib import Path
import os
import sys
import logging

BASE_DIR = Path(__file__).resolve().parent


def load_system_prompt() -> str:
    return (BASE_DIR.parent / "prompts" / "disha_system.txt").read_text(encoding="utf-8")

def check_env_vars():
    required_vars = ["GOOGLE_API_KEY", "DATABASE_URL"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        logging.error(f"Missing required environment variables: {', '.join(missing)}")
        # We can either exit or just warn. Exiting is safer for 'robustness'.
        sys.exit(1)

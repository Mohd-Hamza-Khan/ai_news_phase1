"""Load and validate application configuration."""

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "").strip()
# Default to the official OpenRouter API base URL if not provided
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "").strip() or "http://localhost:20128/v1"


def validate_openrouter_config() -> None:
    """Raise a clear error when required OpenRouter settings are missing."""
    missing = []
    if not OPENROUTER_API_KEY:
        missing.append("OPENROUTER_API_KEY")
    if not OPENROUTER_MODEL:
        missing.append("OPENROUTER_MODEL")
    if not OPENROUTER_BASE_URL:
        missing.append("OPENROUTER_BASE_URL")

    if missing:
        raise RuntimeError(
            "Missing configuration in .env: " + ", ".join(missing)
        )

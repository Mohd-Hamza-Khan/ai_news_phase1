"""Minimal OpenRouter chat-completions client."""

import requests

from scripts.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_BASE_URL,
    validate_openrouter_config,
)


def generate_response(prompt: str) -> str:
    """Send a prompt to the configured OpenRouter model and return its text."""
    if not prompt or not prompt.strip():
        raise ValueError("prompt must not be empty")

    validate_openrouter_config()

    base = OPENROUTER_BASE_URL.rstrip("/")
    url = f"{base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an accurate AI technology researcher and "
                    "technical writer. Do not invent facts or sources."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    # Attempt to decode JSON; if the body is empty or not JSON, raise an informative error.
    try:
        data = response.json()
    except Exception as exc:  # includes JSONDecodeError
        raise RuntimeError(
            f"OpenRouter response is not valid JSON: {exc}"  # noqa: E501
        ) from exc

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            "OpenRouter returned an unexpected response structure"
        ) from exc

    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("OpenRouter returned an empty response")

    return content.strip()

from typing import Optional

import httpx

from app.core.config import get_settings


def generate_summary(prompt: str, max_tokens: int = 512) -> Optional[str]:
    """
    Tiny LLM client.

    - If LLM is disabled in settings, returns None.
    - If HTTP call fails, returns None (we then use fallback templates).

    This is written to be compatible with a simple Ollama-style endpoint:
      POST {base_url}/api/generate
      body: {"model": "...", "prompt": "...", "stream": false}
      response: {"response": "...", ...}
    """
    settings = get_settings()

    if not settings.llm_enabled:
        return None

    try:
        with httpx.Client(timeout=20.0) as client:
            url = settings.llm_base_url.rstrip("/") + "/api/generate"
            payload = {
                "model": settings.llm_model_name,
                "prompt": prompt,
                "stream": False,
            }
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Ollama returns text in "response"
            text = data.get("response")
            if not text:
                return None
            return text.strip()
    except Exception as e:
        # In a real project you'd log this properly
        print(f"[LLM] Error calling LLM backend: {e}")
        return None

"""
Ollama interface for AI-OS Brain.
Handles chat models and embedding models.
"""

import requests

from brain.config.settings import (
    CHAT_MODEL,
    DEFAULT_CHAT_MAX_TOKENS,
    DEFAULT_CHAT_TIMEOUT_SECONDS,
    EMBED_MODEL,
    OLLAMA_CONTEXT_WINDOW,
    OLLAMA_URL,
)


class OllamaClient:
    def __init__(
        self,
        base_url: str = OLLAMA_URL,
        default_model: str = CHAT_MODEL,
):
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model

    def health(self) -> bool:
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        response = requests.get(
            f"{self.base_url}/api/tags",
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return [model["name"] for model in data.get("models", [])]

    def embed(self, text: str, model: str = EMBED_MODEL) -> list[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": model,
                "prompt": text,
            },
            timeout=60,
        )
        response.raise_for_status()

        return response.json()["embedding"]

    def chat(
        self,
        prompt: str,
        model: str | None = None,
        *,
        think: bool = False,
        max_tokens: int = DEFAULT_CHAT_MAX_TOKENS,
        timeout: int = DEFAULT_CHAT_TIMEOUT_SECONDS,
        temperature: float | None = None,
        seed: int | None = None,
    ) -> str:
        options = {
            "num_predict": max_tokens,
            "num_ctx": OLLAMA_CONTEXT_WINDOW,
        }

        if temperature is not None:
            options["temperature"] = temperature

        if seed is not None:
            options["seed"] = seed

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model or self.default_model,
                "prompt": prompt,
                "stream": False,
                "think": think,
                "options": options,
            },
            timeout=timeout,
        )

        response.raise_for_status()

        return response.json()["response"]

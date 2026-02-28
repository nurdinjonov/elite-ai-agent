"""
AI Router — Multi-provider AI so'rovlarni yo'naltirish tizimi.
Qo'llab-quvvatlanadigan provayderlar: OpenRouter, Groq.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional

try:
    import httpx  # type: ignore

    _HTTPX_AVAILABLE = True
except ImportError:
    _HTTPX_AVAILABLE = False

try:
    from openai import OpenAI  # type: ignore

    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False

_CONFIG_PATH = Path(__file__).parent.parent / "config" / "models.json"

_DEFAULT_CONFIG: dict = {
    "providers": {
        "openrouter": {
            "base_url": "https://openrouter.ai/api/v1",
            "models": {
                "fast": "meta-llama/llama-3.1-8b-instruct:free",
                "code": "deepseek/deepseek-coder-v2",
                "pro": "anthropic/claude-3.5-sonnet",
            },
        },
        "groq": {
            "base_url": "https://api.groq.com/openai/v1",
            "models": {
                "fast": "llama-3.1-8b-instant",
                "code": "llama-3.1-70b-versatile",
                "pro": "llama-3.1-70b-versatile",
            },
        },
    },
    "default_provider": "openrouter",
    "fallback_order": ["openrouter", "groq"],
}


def _load_config() -> dict:
    """Model konfiguratsiyasini yuklash."""
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return _DEFAULT_CONFIG


class AIRouter:
    """Multi-AI Orchestration — so'rovlarni eng mos modelga yo'naltirish."""

    def __init__(self) -> None:
        self._config = _load_config()
        self._api_keys: dict[str, Optional[str]] = {
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY"),
        }

    def _get_client(self, provider: str) -> Any:
        """Berilgan provayder uchun OpenAI-compatible client yaratish."""
        if not _OPENAI_AVAILABLE:
            raise ImportError("openai kutubxonasi o'rnatilmagan: pip install openai")

        provider_config = self._config["providers"].get(provider, {})
        base_url = provider_config.get("base_url", "")
        api_key = self._api_keys.get(provider, "")

        if not api_key:
            raise ValueError(f"{provider.upper()}_API_KEY o'rnatilmagan")

        return OpenAI(api_key=api_key, base_url=base_url)

    def _select_model(self, provider: str, mode: str, model_override: Optional[str] = None) -> str:
        """Rejim va provayderga qarab modelni tanlash."""
        if model_override:
            return model_override
        provider_config = self._config["providers"].get(provider, {})
        models = provider_config.get("models", {})
        mode_key = mode.lower()
        return models.get(mode_key, models.get("pro", ""))

    def route_request(
        self,
        messages: list[dict],
        mode: str = "pro",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """So'rovni mos provayderga yo'naltirish.

        Args:
            messages: OpenAI-format xabarlar ro'yxati
            mode: "fast" | "code" | "pro"
            model: Model override (ixtiyoriy)
            temperature: Temperatura parametri
            max_tokens: Maksimal tokenlar soni

        Returns:
            AI javobi matni
        """
        fallback_order: list[str] = self._config.get("fallback_order", ["openrouter", "groq"])
        last_error: Optional[Exception] = None

        for provider in fallback_order:
            api_key = self._api_keys.get(provider)
            if not api_key:
                continue

            try:
                client = self._get_client(provider)
                selected_model = self._select_model(provider, mode, model)

                if not selected_model:
                    continue

                response = client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content or ""

            except Exception as exc:
                last_error = exc
                continue

        # Hech qanday provayder ishlamasa
        if last_error:
            raise RuntimeError(
                f"Hech qanday AI provayderi javob bermadi. "
                f"API kalitlarini tekshiring. Oxirgi xato: {last_error}"
            )
        raise RuntimeError(
            "API kalitlari topilmadi. OPENROUTER_API_KEY yoki GROQ_API_KEY ni o'rnating."
        )

    def get_available_providers(self) -> list[str]:
        """API kaliti mavjud provayderlar ro'yxati."""
        return [p for p, key in self._api_keys.items() if key]

    def is_available(self) -> bool:
        """Kamida bitta provayder mavjudligini tekshirish."""
        return bool(self.get_available_providers())

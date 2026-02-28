"""Multi-AI Provider Router for JARVIS-X.

Routes prompts to the optimal AI provider based on mode and availability.
Supports OpenRouter, Groq, and OpenAI with automatic fallback.
"""

from __future__ import annotations

import json
from typing import Optional

from openai import OpenAI

from config.settings import get_settings
from core.modes import Mode


class AIRouter:
    """Routes AI requests to the optimal provider based on mode and availability."""

    def __init__(self) -> None:
        """Load API keys from settings and model configuration from models.json."""
        settings = get_settings()
        self._api_keys: dict[str, str] = {
            "openrouter": settings.openrouter_api_key,
            "groq": settings.groq_api_key,
            "openai": settings.openai_api_key,
        }
        config_path = settings.models_config_path
        with open(config_path, "r", encoding="utf-8") as f:
            self._models_config: dict = json.load(f)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(
        self,
        prompt: str,
        mode: Mode,
        preferred_provider: Optional[str] = None,
        system_prompt: str = "",
    ) -> dict:
        """Route a prompt to the best available provider.

        Args:
            prompt: The user prompt to send.
            mode: Current JARVIS-X mode (FAST, CODE, PRO).
            preferred_provider: If set, try this provider first.
            system_prompt: Optional system-level instruction.

        Returns:
            dict with keys: response, provider, model.

        Raises:
            Exception: When all providers fail.
        """
        providers_order = self._get_provider_order(mode, preferred_provider)
        last_error: Exception = Exception("No providers configured.")
        for provider in providers_order:
            model = self._get_model(provider, mode)
            try:
                response = self._call_provider(provider, prompt, model, system_prompt)
                return {"response": response, "provider": provider, "model": model}
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue
        raise Exception(f"Barcha provayderlar ishlamadi. Oxirgi xato: {last_error}") from last_error

    def list_providers(self) -> dict[str, dict]:
        """Return available providers and their availability status.

        Returns:
            dict mapping provider name to status info.
        """
        result: dict[str, dict] = {}
        providers = self._models_config.get("providers", {})
        for name, cfg in providers.items():
            key = self._api_keys.get(name, "")
            result[name] = {
                "available": bool(key),
                "base_url": cfg.get("base_url", ""),
                "has_key": bool(key),
            }
        return result

    def list_models(self) -> dict[str, dict]:
        """Return all configured models grouped by provider.

        Returns:
            dict mapping provider name to its model configuration.
        """
        providers = self._models_config.get("providers", {})
        return {name: cfg.get("models", {}) for name, cfg in providers.items()}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_provider_order(self, mode: Mode, preferred_provider: Optional[str]) -> list[str]:
        """Build the ordered list of providers to try for a given mode.

        Args:
            mode: The active JARVIS-X mode.
            preferred_provider: Optional override for the first provider to try.

        Returns:
            Ordered list of provider names.
        """
        priority: list[str] = list(
            self._models_config.get("default_provider_priority", {}).get(mode.value, [])
        )
        if preferred_provider and preferred_provider in self._models_config.get("providers", {}):
            # Move preferred provider to front without duplicating
            priority = [preferred_provider] + [p for p in priority if p != preferred_provider]
        return priority

    def _get_model(self, provider: str, mode: Mode) -> str:
        """Get the model name for a provider/mode combination.

        Args:
            provider: Provider name.
            mode: Active mode.

        Returns:
            Model name string.
        """
        providers = self._models_config.get("providers", {})
        return providers.get(provider, {}).get("models", {}).get(mode.value, "")

    def _call_provider(
        self,
        provider: str,
        prompt: str,
        model: str,
        system_prompt: str,
    ) -> str:
        """Call a specific provider and return the response text.

        Args:
            provider: Provider name (openrouter, groq, openai).
            prompt: User message.
            model: Model identifier to use.
            system_prompt: System-level instruction.

        Returns:
            Response text from the model.

        Raises:
            ValueError: If the provider API key is missing.
            Exception: On API call failure.
        """
        api_key = self._api_keys.get(provider, "")
        if not api_key:
            raise ValueError(f"API kaliti topilmadi: {provider}")

        base_url = (
            self._models_config.get("providers", {})
            .get(provider, {})
            .get("base_url", "")
        )
        client = OpenAI(base_url=base_url, api_key=api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content or ""

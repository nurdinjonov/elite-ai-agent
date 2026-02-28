"""JARVIS-X AI Router — Ko'p provayderli aqlli routing tizimi."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class AIRouter:
    """OpenRouter, Groq va OpenAI provayderlarini boshqaruvchi router.

    Har bir so'rov uchun rejimga mos optimal provayderni tanlaydi va
    xato bo'lsa avtomatik ravishda keyingi provayderga o'tadi (fallback).
    """

    DEFAULT_FALLBACK_MODEL = "gpt-4o-mini"

    def __init__(self) -> None:
        """Sozlamalardan API kalitlarni yuklaydi, models.json ni o'qiydi."""
        self._api_keys: dict[str, str] = {
            "openrouter": os.environ.get("OPENROUTER_API_KEY", ""),
            "groq": os.environ.get("GROQ_API_KEY", ""),
            "openai": os.environ.get("OPENAI_API_KEY", ""),
        }

        # settings.py mavjud bo'lsa undan ham o'qish
        try:
            from config.settings import settings  # type: ignore[import-not-found]

            if hasattr(settings, "openrouter_api_key") and settings.openrouter_api_key:
                self._api_keys["openrouter"] = settings.openrouter_api_key
            if hasattr(settings, "groq_api_key") and settings.groq_api_key:
                self._api_keys["groq"] = settings.groq_api_key
            if hasattr(settings, "openai_api_key") and settings.openai_api_key:
                self._api_keys["openai"] = settings.openai_api_key
        except Exception:
            pass

        self._models_config = self._load_models_config()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(
        self,
        prompt: str,
        mode: str = "pro",
        preferred_provider: str | None = None,
        system_prompt: str = "",
    ) -> str:
        """Asosiy routing metodi — so'rovni eng mos provayderga yo'naltiradi.

        Args:
            prompt: Foydalanuvchi so'rovi.
            mode: Rejim nomi ("fast", "code", "pro").
            preferred_provider: Majburiy provider (None bo'lsa avtomatik).
            system_prompt: System prompt matni.

        Returns:
            AI javob matni.

        Raises:
            Exception: Barcha provayderlar ishlamagan holda.
        """
        providers_order = self._get_provider_order(mode, preferred_provider)
        last_error: Exception | None = None

        for provider in providers_order:
            model = self._get_model(provider, mode)
            try:
                return self._call_provider(provider, prompt, model, system_prompt)
            except Exception as exc:
                last_error = exc
                continue

        raise Exception(
            f"Barcha provayderlar ishlamadi. Oxirgi xato: {last_error}"
        )

    def get_active_provider_and_model(
        self, mode: str, preferred_provider: str | None = None
    ) -> tuple[str, str]:
        """Joriy so'rov uchun ishlatiladigan provider va model nomini qaytaradi.

        Args:
            mode: Rejim nomi ("fast", "code", "pro").
            preferred_provider: Foydalanuvchi tanlagan provider (ixtiyoriy).

        Returns:
            (provider_nomi, model_nomi) tuple.
        """
        provider = self._get_provider_order(mode, preferred_provider)[0]
        model = self._get_model(provider, mode)
        return provider, model


        """Mavjud provayderlar va ularning holatini qaytaradi.

        Returns:
            Provider nomi → {available: bool, has_key: bool} lug'ati.
        """
        result: dict[str, dict[str, Any]] = {}
        for provider, key in self._api_keys.items():
            result[provider] = {
                "available": bool(key),
                "has_key": bool(key),
            }
        return result

    def list_models(self) -> dict[str, Any]:
        """Barcha mavjud modellarni provider bo'yicha qaytaradi.

        Returns:
            Provider → models lug'ati (models.json tuzilmasi).
        """
        providers: dict[str, Any] = self._models_config.get("providers", {})
        result: dict[str, Any] = {}
        for provider, cfg in providers.items():
            result[provider] = cfg.get("models", {})
        return result

    # ------------------------------------------------------------------
    # Provider callers
    # ------------------------------------------------------------------

    def _call_provider(
        self,
        provider: str,
        prompt: str,
        model: str,
        system_prompt: str,
    ) -> str:
        """Berilgan provayderga so'rov yuboradi.

        Args:
            provider: Provider nomi.
            prompt: Foydalanuvchi so'rovi.
            model: Model nomi.
            system_prompt: System prompt.

        Returns:
            AI javob matni.
        """
        if provider == "openrouter":
            return self._call_openrouter(prompt, model, system_prompt)
        elif provider == "groq":
            return self._call_groq(prompt, model, system_prompt)
        elif provider == "openai":
            return self._call_openai(prompt, model, system_prompt)
        raise ValueError(f"Noto'g'ri provider: {provider}")

    def _call_openrouter(self, prompt: str, model: str, system_prompt: str) -> str:
        """OpenRouter API orqali so'rov yuboradi.

        Args:
            prompt: Foydalanuvchi so'rovi.
            model: Model nomi.
            system_prompt: System prompt.

        Returns:
            AI javob matni.
        """
        from openai import OpenAI

        api_key = self._api_keys["openrouter"]
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY o'rnatilmagan")

        base_url = (
            self._models_config.get("providers", {})
            .get("openrouter", {})
            .get("base_url", "https://openrouter.ai/api/v1")
        )
        client = OpenAI(base_url=base_url, api_key=api_key)
        messages = self._build_messages(prompt, system_prompt)
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content or ""

    def _call_groq(self, prompt: str, model: str, system_prompt: str) -> str:
        """Groq API orqali so'rov yuboradi.

        Args:
            prompt: Foydalanuvchi so'rovi.
            model: Model nomi.
            system_prompt: System prompt.

        Returns:
            AI javob matni.
        """
        from openai import OpenAI

        api_key = self._api_keys["groq"]
        if not api_key:
            raise ValueError("GROQ_API_KEY o'rnatilmagan")

        base_url = (
            self._models_config.get("providers", {})
            .get("groq", {})
            .get("base_url", "https://api.groq.com/openai/v1")
        )
        client = OpenAI(base_url=base_url, api_key=api_key)
        messages = self._build_messages(prompt, system_prompt)
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content or ""

    def _call_openai(self, prompt: str, model: str, system_prompt: str) -> str:
        """OpenAI API orqali so'rov yuboradi.

        Args:
            prompt: Foydalanuvchi so'rovi.
            model: Model nomi.
            system_prompt: System prompt.

        Returns:
            AI javob matni.
        """
        from openai import OpenAI

        api_key = self._api_keys["openai"]
        if not api_key:
            raise ValueError("OPENAI_API_KEY o'rnatilmagan")

        base_url = (
            self._models_config.get("providers", {})
            .get("openai", {})
            .get("base_url", "https://api.openai.com/v1")
        )
        client = OpenAI(base_url=base_url, api_key=api_key)
        messages = self._build_messages(prompt, system_prompt)
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content or ""

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_provider_order(
        self, mode: str, preferred_provider: str | None
    ) -> list[str]:
        """Rejim va afzallikka qarab provayderlar tartibini qaytaradi.

        Args:
            mode: Rejim nomi.
            preferred_provider: Foydalanuvchi tanlagan provider (ixtiyoriy).

        Returns:
            Provayderlar ro'yxati (birinchisi ustuvor).
        """
        default_order: list[str] = (
            self._models_config.get("default_provider_priority", {}).get(mode, [])
            or ["openai", "openrouter", "groq"]
        )

        if preferred_provider:
            # Tanlangan provider birinchi, qolganlari saqlanadi
            rest = [p for p in default_order if p != preferred_provider]
            return [preferred_provider] + rest

        return default_order

    def _get_model(self, provider: str, mode: str) -> str:
        """Berilgan provider va rejim uchun model nomini qaytaradi.

        Args:
            provider: Provider nomi.
            mode: Rejim nomi.

        Returns:
            Model nomi.
        """
        return (
            self._models_config.get("providers", {})
            .get(provider, {})
            .get("models", {})
            .get(mode, self.DEFAULT_FALLBACK_MODEL)
        )

    @staticmethod
    def _build_messages(
        prompt: str, system_prompt: str
    ) -> list[dict[str, str]]:
        """Chat completions uchun xabarlar ro'yxatini tuzadi.

        Args:
            prompt: Foydalanuvchi xabari.
            system_prompt: System prompt.

        Returns:
            OpenAI messages format ro'yxati.
        """
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages

    def _load_models_config(self) -> dict[str, Any]:
        """config/models.json faylini o'qiydi.

        Returns:
            Konfiguratsiya lug'ati (xato bo'lsa bo'sh lug'at).
        """
        # Bir necha mumkin bo'lgan yo'llarni tekshirish
        candidates = [
            Path("config/models.json"),
            Path(__file__).parent.parent / "config" / "models.json",
        ]
        for path in candidates:
            if path.exists():
                try:
                    with open(path, encoding="utf-8") as fh:
                        return json.load(fh)  # type: ignore[no-any-return]
                except Exception:
                    pass
        return {}

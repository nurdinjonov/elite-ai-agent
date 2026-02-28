"""JARVIS-X Settings — Pydantic asosidagi konfiguratsiya tizimi."""

from __future__ import annotations

import os


def _make_dataclass_settings() -> object:
    """Pydantic mavjud bo'lmagan holda dataclass asosidagi settings yaratadi."""
    from dataclasses import dataclass

    @dataclass
    class _Settings:
        """Konfiguratsiya dataclass (pydantic mavjud bo'lmagan holatda)."""

        # --- OpenAI ---
        openai_api_key: str = ""

        # --- Multi-AI Router ---
        openrouter_api_key: str = ""
        groq_api_key: str = ""

        # --- JARVIS-X ---
        jarvis_default_mode: str = "pro"
        jarvis_voice_enabled: bool = False

        # --- Models Config ---
        models_config_path: str = "config/models.json"

    return _Settings(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        openrouter_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        groq_api_key=os.environ.get("GROQ_API_KEY", ""),
        jarvis_default_mode=os.environ.get("JARVIS_DEFAULT_MODE", "pro"),
        jarvis_voice_enabled=os.environ.get("JARVIS_VOICE_ENABLED", "false").lower() == "true",
        models_config_path=os.environ.get("MODELS_CONFIG_PATH", "config/models.json"),
    )


try:
    from pydantic_settings import BaseSettings  # type: ignore[import-not-found]
    from pydantic import Field

    _PYDANTIC_SETTINGS = True
except ImportError:
    _PYDANTIC_SETTINGS = False
    try:
        from pydantic import BaseSettings, Field  # type: ignore[no-redef,import-not-found]

        _PYDANTIC_SETTINGS = True
    except ImportError:
        _PYDANTIC_SETTINGS = False


if _PYDANTIC_SETTINGS:

    class Settings(BaseSettings):  # type: ignore[no-redef]
        """JARVIS-X barcha sozlamalari."""

        # --- OpenAI ---
        openai_api_key: str = Field(default="", description="OpenAI API kaliti")

        # --- Multi-AI Router ---
        openrouter_api_key: str = Field(
            default="", description="OpenRouter API kaliti"
        )
        groq_api_key: str = Field(default="", description="Groq API kaliti")

        # --- JARVIS-X ---
        jarvis_default_mode: str = Field(
            default="pro", description="Standart rejim: fast, code, pro"
        )
        jarvis_voice_enabled: bool = Field(
            default=False, description="Ovoz tizimini yoqish"
        )

        # --- Models Config ---
        models_config_path: str = Field(
            default="config/models.json",
            description="Model konfiguratsiya fayli yo'li",
        )

        model_config = {"env_file": ".env", "extra": "ignore"}

    settings = Settings()

else:
    settings = _make_dataclass_settings()  # type: ignore[assignment]

__all__ = ["settings", "Settings"]

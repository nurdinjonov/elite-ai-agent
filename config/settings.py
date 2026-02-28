"""JARVIS-X application settings.

Uses pydantic-settings (v2) to load configuration from environment
variables and a .env file.  All existing fields are preserved and new
JARVIS-X-specific fields have been appended.
"""

from __future__ import annotations

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application-wide settings for JARVIS-X."""

    # ------------------------------------------------------------------
    # Core AI keys (original fields)
    # ------------------------------------------------------------------
    openai_api_key: str = Field(default="", description="OpenAI API kaliti")

    # ------------------------------------------------------------------
    # Multi-AI Router
    # ------------------------------------------------------------------
    openrouter_api_key: str = Field(default="", description="OpenRouter API kaliti")
    groq_api_key: str = Field(default="", description="Groq API kaliti")

    # ------------------------------------------------------------------
    # JARVIS-X
    # ------------------------------------------------------------------
    jarvis_default_mode: str = Field(
        default="pro",
        description="Standart rejim: fast, code, pro",
    )
    jarvis_voice_enabled: bool = Field(
        default=False,
        description="Ovoz tizimini yoqish",
    )
    models_config_path: str = Field(
        default="config/models.json",
        description="Model konfiguratsiya fayli",
    )

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return the cached Settings singleton.

    Returns:
        Application settings loaded from environment / .env file.
    """
    global _settings  # noqa: PLW0603
    if _settings is None:
        _settings = Settings()
    return _settings

"""Mode management for JARVIS-X.

Defines the three operating modes (FAST, CODE, PRO) and the ModeManager
that provides mode-specific configuration such as system prompts,
preferred providers, and model recommendations.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional


class Mode(str, Enum):
    """JARVIS-X operating modes."""

    FAST = "fast"
    CODE = "code"
    PRO = "pro"


# ---------------------------------------------------------------------------
# System prompts per mode
# ---------------------------------------------------------------------------
_SYSTEM_PROMPTS: dict[Mode, str] = {
    Mode.FAST: (
        "You are JARVIS-X in FAST mode. "
        "Be ultra-concise — no extra text, 2-3 sentences max. "
        "Answer directly without preamble or filler."
    ),
    Mode.CODE: (
        "You are JARVIS-X in CODE mode. "
        "Always lead with working, runnable code. "
        "Follow best practices, use type hints, and include brief inline comments. "
        "Minimize prose — let the code speak."
    ),
    Mode.PRO: (
        "You are JARVIS-X in PRO mode. "
        "Provide deep explanations, thoughtful architecture design, "
        "and step-by-step reasoning. Use all available tools when helpful. "
        "Be thorough and professional."
    ),
}

# ---------------------------------------------------------------------------
# Preferred providers per mode
# ---------------------------------------------------------------------------
_PREFERRED_PROVIDERS: dict[Mode, str] = {
    Mode.FAST: "groq",
    Mode.CODE: "openrouter",
    Mode.PRO: "openai",
}

# ---------------------------------------------------------------------------
# Recommended model names per mode (human-readable label)
# ---------------------------------------------------------------------------
_RECOMMENDED_MODELS: dict[Mode, str] = {
    Mode.FAST: "llama-3.1-8b-instant",
    Mode.CODE: "deepseek/deepseek-coder-v2",
    Mode.PRO: "gpt-4o",
}


class ModeManager:
    """Manages the active JARVIS-X operating mode and related configuration."""

    def __init__(self) -> None:
        """Initialise with PRO as the default mode."""
        self._mode: Mode = Mode.PRO

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def current_mode(self) -> Mode:
        """Return the currently active mode."""
        return self._mode

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_mode(self, mode: Mode) -> None:
        """Change the active mode.

        Args:
            mode: The new mode to activate.
        """
        self._mode = mode

    def get_system_prompt(self, mode: Optional[Mode] = None) -> str:
        """Return the system prompt for the given (or current) mode.

        Args:
            mode: Mode override.  Uses current mode when *None*.

        Returns:
            System prompt string for the mode.
        """
        return _SYSTEM_PROMPTS[mode or self._mode]

    def get_preferred_provider(self, mode: Optional[Mode] = None) -> str:
        """Return the preferred AI provider for the given (or current) mode.

        Args:
            mode: Mode override.  Uses current mode when *None*.

        Returns:
            Provider name string (e.g. "groq", "openrouter", "openai").
        """
        return _PREFERRED_PROVIDERS[mode or self._mode]

    def get_model_for_mode(self, mode: Optional[Mode] = None) -> str:
        """Return the recommended model identifier for the given (or current) mode.

        Args:
            mode: Mode override.  Uses current mode when *None*.

        Returns:
            Model name string.
        """
        return _RECOMMENDED_MODELS[mode or self._mode]

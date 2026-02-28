"""JARVIS-X main orchestrator.

Wires together all JARVIS-X sub-systems: language detection, mode
management, AI routing, and voice I/O.
"""

from __future__ import annotations

from typing import Optional

from core.ai_router import AIRouter
from core.language import LanguageDetector
from core.modes import Mode, ModeManager
from core.voice import VoiceEngine


class JarvisX:
    """Central orchestrator for JARVIS-X.

    Coordinates language detection, mode selection, AI routing, and
    optional voice input/output to produce a unified response dict for
    every user interaction.
    """

    def __init__(self) -> None:
        """Initialise all JARVIS-X sub-components."""
        self.mode_manager = ModeManager()
        self.language_detector = LanguageDetector()
        self.ai_router = AIRouter()
        self.voice_engine = VoiceEngine()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(
        self,
        user_input: str,
        preferred_provider: Optional[str] = None,
    ) -> dict:
        """Process a text input and return a structured response.

        Steps:
            1. Detect the language of *user_input*.
            2. Retrieve the current mode and its system prompt.
            3. Append the language-response instruction to the system prompt.
            4. Route to the AI provider (PRO mode may use the LangGraph agent
               when tool integration is available; FAST/CODE go direct).
            5. Return a result dict.

        Args:
            user_input: Raw text from the user.
            preferred_provider: Optional provider name override.

        Returns:
            dict with keys: response, provider, model, mode, language.
        """
        # 1. Language detection
        language = self.language_detector.detect(user_input)
        lang_instruction = self.language_detector.get_response_instruction(language)

        # 2. Mode
        mode: Mode = self.mode_manager.current_mode

        # 3. Build system prompt
        system_prompt = self.mode_manager.get_system_prompt(mode)
        system_prompt = f"{system_prompt}\n{lang_instruction}"

        # 4 & 5. Route to AI provider
        result = self.ai_router.route(
            prompt=user_input,
            mode=mode,
            preferred_provider=preferred_provider,
            system_prompt=system_prompt,
        )

        return {
            "response": result["response"],
            "provider": result["provider"],
            "model": result["model"],
            "mode": mode.value,
            "language": language,
        }

    def process_voice(self) -> Optional[dict]:
        """Listen for voice input and return a spoken + structured response.

        Returns:
            Response dict (same shape as :py:meth:`process`) or *None* when
            the voice engine is unavailable or no speech was captured.
        """
        if not self.voice_engine.is_available():
            print("[JARVIS-X] Ovoz tizimi mavjud emas. Matn rejimidan foydalaning.")
            return None

        user_input = self.voice_engine.listen()
        if not user_input:
            return None

        result = self.process(user_input)
        self.voice_engine.speak(result["response"])
        return result

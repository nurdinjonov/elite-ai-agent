"""Language detection for JARVIS-X.

Detects whether the user is writing in Uzbek or English and returns
the appropriate response-language instruction for the AI model.
"""

from __future__ import annotations


# Uzbek language markers used for heuristic detection
_UZBEK_MARKERS: list[str] = [
    "o'z", "qil", "uchun", "bo'l", "kerak", "nima", "qanday",
    "salom", "rahmat", "menga", "berish", "olish", "yozish",
    "ochish", "ishla", "tushun", "dastur", "loyiha", "vazifa",
    "men", "bilan", "hamma",
]

_UZBEK_THRESHOLD = 2  # minimum marker count to classify as Uzbek


class LanguageDetector:
    """Simple heuristic-based language detector for Uzbek and English."""

    def detect(self, text: str) -> str:
        """Detect the language of *text*.

        Uses a lightweight marker-based approach: if two or more Uzbek
        keywords are found in the lower-cased input the language is
        classified as Uzbek; otherwise English is assumed.

        Args:
            text: Raw user input string.

        Returns:
            Language code: ``"uz"`` for Uzbek, ``"en"`` for English.
        """
        lower = text.lower()
        count = sum(1 for marker in _UZBEK_MARKERS if marker in lower)
        return "uz" if count >= _UZBEK_THRESHOLD else "en"

    def get_response_instruction(self, lang: str) -> str:
        """Return a system-level instruction for the detected language.

        Args:
            lang: Language code returned by :py:meth:`detect`.

        Returns:
            Instruction string to append to the system prompt.
        """
        if lang == "uz":
            return "Respond entirely in Uzbek language."
        return "Respond in English."

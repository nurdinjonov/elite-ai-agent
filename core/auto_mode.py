"""
JARVIS Auto Mode Switcher.
Foydalanuvchi kiritishiga qarab rejimni avtomatik tanlash.
"""
from __future__ import annotations


class AutoModeSwitcher:
    """Kiritishga qarab rejimni avtomatik aniqlash."""

    # Kalit so'zlar bo'yicha rejim aniqlash
    _CODE_KEYWORDS = [
        "kod", "code", "python", "javascript", "function", "class", "debug",
        "error", "bug", "script", "program", "api", "json", "html", "css",
        "git", "terminal", "bash", "pip", "install", "import", "def",
        "yoz", "yozib ber", "kod yoz", "dastur", "funksiya",
    ]

    _STUDY_KEYWORDS = [
        "o'qi", "study", "dars", "fan", "matematika", "fizika", "kimyo",
        "homework", "vazifa", "uy vazifa", "imtihon", "test", "quiz",
        "tushuntir", "explain", "formula", "masala", "misol",
    ]

    _PRO_KEYWORDS = [
        "tahlil", "analysis", "batafsil", "detailed", "chuqur",
        "strategiya", "strategy", "reja tuz", "plan", "loyiha",
        "project", "research", "tadqiqot",
    ]

    def detect_mode(self, text: str) -> str:
        """
        Kiritishga qarab rejimni aniqlash.

        Returns:
            "code" | "study" | "pro" | "fast"

        Default: "fast"
        """
        text_lower = text.lower()

        # Code mode
        for kw in self._CODE_KEYWORDS:
            if kw in text_lower:
                return "code"

        # Study mode
        for kw in self._STUDY_KEYWORDS:
            if kw in text_lower:
                return "study"

        # Pro mode
        for kw in self._PRO_KEYWORDS:
            if kw in text_lower:
                return "pro"

        # Default
        return "fast"

    def should_switch(self, current_mode: str, detected_mode: str) -> bool:
        """Rejim almashtirilishi kerakmi?"""
        return current_mode != detected_mode

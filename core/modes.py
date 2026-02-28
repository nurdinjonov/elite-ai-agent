"""JARVIS-X Mode Manager — 3 ta rejim tizimi (Fast, Code, Pro)."""

from enum import Enum


class Mode(str, Enum):
    """JARVIS-X ishlash rejimlari."""

    FAST = "fast"
    CODE = "code"
    PRO = "pro"


_SYSTEM_PROMPTS: dict[str, str] = {
    Mode.FAST: (
        "You are JARVIS-X in FAST mode.\n"
        "Rules:\n"
        "- Ultra-concise answers only\n"
        "- No extra explanations\n"
        "- Answer ONLY what was asked\n"
        "- Maximum 2-3 sentences\n"
        "- If user speaks Uzbek, respond in Uzbek\n"
        "- If user speaks English, respond in English\n"
    ),
    Mode.CODE: (
        "You are JARVIS-X in CODE mode — a world-class programming assistant.\n"
        "Rules:\n"
        "- Return code FIRST, explanation AFTER (only if needed)\n"
        "- Use best practices and modern patterns\n"
        "- Include type hints and docstrings\n"
        "- No unnecessary text\n"
        "- Support: Python, JavaScript, TypeScript, Go, Rust, Java, C++\n"
        "- Always provide complete, runnable code\n"
        "- If user speaks Uzbek, respond in Uzbek with English code\n"
    ),
    Mode.PRO: (
        "You are JARVIS-X in PRO mode — a senior AI architect and research assistant.\n"
        "Capabilities:\n"
        "- Deep, detailed explanations\n"
        "- Architecture design and system design\n"
        "- Step-by-step guidance\n"
        "- Research and analysis\n"
        "- Use tools: web search, code execution, file management\n"
        "- Real-time information via web search\n"
        "- If user speaks Uzbek, respond in Uzbek\n"
        "- If user speaks English, respond in English\n"
        "- Be thorough but structured\n"
    ),
}

_PREFERRED_PROVIDERS: dict[str, str] = {
    Mode.FAST: "groq",
    Mode.CODE: "openrouter",
    Mode.PRO: "openai",
}


class ModeManager:
    """JARVIS-X rejimlarini boshqaruvchi klass."""

    def __init__(self) -> None:
        """Standart rejim: PRO."""
        self._mode: Mode = Mode.PRO

    @property
    def current_mode(self) -> Mode:
        """Joriy rejimni qaytaradi."""
        return self._mode

    def set_mode(self, mode: Mode) -> None:
        """Rejimni o'zgartiradi.

        Args:
            mode: Yangi rejim (Mode enum qiymati).
        """
        self._mode = mode

    def get_system_prompt(self, mode: Mode | None = None) -> str:
        """Berilgan (yoki joriy) rejim uchun system prompt qaytaradi.

        Args:
            mode: Rejim. None bo'lsa joriy rejim ishlatiladi.

        Returns:
            System prompt matni.
        """
        target = mode if mode is not None else self._mode
        return _SYSTEM_PROMPTS.get(target, _SYSTEM_PROMPTS[Mode.PRO])

    def get_preferred_provider(self, mode: Mode | None = None) -> str:
        """Berilgan (yoki joriy) rejim uchun optimal provider qaytaradi.

        Args:
            mode: Rejim. None bo'lsa joriy rejim ishlatiladi.

        Returns:
            Provider nomi (masalan "groq", "openrouter", "openai").
        """
        target = mode if mode is not None else self._mode
        return _PREFERRED_PROVIDERS.get(target, "openai")

    def get_model_for_mode(self, mode: Mode | None = None) -> str:
        """Berilgan (yoki joriy) rejim uchun optimal model nomini qaytaradi.

        Bu metod models.json konfigurasiyasiga asoslanadi. AIRouter sinfi
        to'liq konfiguratsiyani yuklaydi; bu yerda faqat mode nomi qaytariladi.

        Args:
            mode: Rejim. None bo'lsa joriy rejim ishlatiladi.

        Returns:
            Mode nomi string sifatida (masalan "fast", "code", "pro").
        """
        target = mode if mode is not None else self._mode
        return target.value

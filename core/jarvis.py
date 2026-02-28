"""JARVIS-X — Asosiy Orchestrator. Barcha core modullarni birlashtiradi."""

from __future__ import annotations

from core.ai_router import AIRouter
from core.language import LanguageDetector
from core.modes import Mode, ModeManager
from core.voice import VoiceEngine


class JarvisX:
    """JARVIS-X asosiy orchestrator klassi.

    Barcha core modullarni (AI Router, Mode Manager, Language Detector,
    Voice Engine) boshqaradi va foydalanuvchi so'rovlarini qayta ishlaydi.
    """

    def __init__(self) -> None:
        """Core modullarni va ixtiyoriy agent komponentlarini ishga tushiradi."""
        self.mode_manager = ModeManager()
        self.ai_router = AIRouter()
        self.lang_detector = LanguageDetector()
        self.voice = VoiceEngine()

        # Ixtiyoriy: mavjud memory / knowledge / agent komponentlari
        self._short_memory = None
        self._long_memory = None
        self._knowledge_base = None
        self._agent_graph = None

        self._load_optional_components()

    # ------------------------------------------------------------------
    # Optional component loader
    # ------------------------------------------------------------------

    def _load_optional_components(self) -> None:
        """Mavjud memory, knowledge va agent modullarini yuklaydi.

        Agar modullar mavjud bo'lmasa xatosiz davom etadi.
        """
        try:
            from memory.short_term import ShortTermMemory  # type: ignore[import-not-found]

            self._short_memory = ShortTermMemory()
        except (ImportError, ModuleNotFoundError):
            pass

        try:
            from memory.long_term import LongTermMemory  # type: ignore[import-not-found]

            self._long_memory = LongTermMemory()
        except (ImportError, ModuleNotFoundError):
            pass

        try:
            from knowledge.base import KnowledgeBase  # type: ignore[import-not-found]

            self._knowledge_base = KnowledgeBase()
        except (ImportError, ModuleNotFoundError):
            pass

        try:
            from agent import build_agent_graph  # type: ignore[import-not-found]

            self._agent_graph = build_agent_graph()
        except (ImportError, ModuleNotFoundError):
            pass

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, user_input: str) -> str:
        """Foydalanuvchi so'rovini qayta ishlaydi va javob qaytaradi.

        Jarayon:
        1. Tilni aniqlash
        2. Joriy rejimni olish
        3. System prompt tuzish (rejim + til ko'rsatmasi)
        4. PRO rejimda → agent graph ishlatish (agar mavjud)
        5. FAST/CODE rejimda → to'g'ridan-to'g'ri AI Router
        6. Qisqa muddatli xotiraga saqlash
        7. Javobni qaytarish

        Args:
            user_input: Foydalanuvchi so'rovi (matn).

        Returns:
            AI javob matni.
        """
        if not user_input or not user_input.strip():
            return "Iltimos, so'rovingizni kiriting."

        lang = self.lang_detector.detect(user_input)
        mode = self.mode_manager.current_mode
        sys_prompt = self.mode_manager.get_system_prompt()
        sys_prompt += self.lang_detector.get_response_instruction(lang)

        response = ""

        if mode == Mode.PRO and self._agent_graph is not None:
            try:
                result = self._agent_graph.invoke(
                    {"messages": [{"role": "user", "content": user_input}]}
                )
                # LangGraph odatda {"messages": [...]} qaytaradi
                if isinstance(result, dict) and "messages" in result:
                    last_msg = result["messages"][-1]
                    response = (
                        last_msg.content
                        if hasattr(last_msg, "content")
                        else str(last_msg)
                    )
                else:
                    response = str(result)
            except Exception:
                # Fallback to direct AI Router
                response = ""

        if not response:
            try:
                preferred = self.mode_manager.get_preferred_provider()
                response = self.ai_router.route(
                    prompt=user_input,
                    mode=mode.value,
                    preferred_provider=preferred,
                    system_prompt=sys_prompt,
                )
            except Exception as exc:
                response = f"Xato: {exc}"

        # Qisqa muddatli xotiraga saqlash
        if self._short_memory is not None:
            try:
                self._short_memory.add(user=user_input, assistant=response)
            except Exception:
                pass

        return response

    def process_voice(self) -> str | None:
        """Ovozli so'rovni qayta ishlaydi.

        Jarayon:
        1. Mikrofondan ovoz olish (STT)
        2. Matnni qayta ishlash
        3. Javobni ovozga o'girish (TTS)
        4. Javobni qaytarish

        Returns:
            AI javob matni yoki None (ovoz aniqlanmasa).
        """
        text = self.voice.listen()
        if text is None:
            return None

        response = self.process(text)
        self.voice.speak(response)
        return response

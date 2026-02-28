"""
JARVIS-X — Asosiy Orchestrator.
Barcha modullarni birlashtiradi va foydalanuvchi so'rovlarini qayta ishlaydi.
"""

from __future__ import annotations

from typing import Optional

from .ai_router import AIRouter
from .modes import ModeManager
from .language import LanguageDetector
from .memory import MemoryManager
from .tools import ToolRegistry
from .rag import RAGEngine

_MODE_COMMANDS = {
    "/fast": "fast",
    "/code": "code",
    "/pro": "pro",
}

_PROVIDER_CMD = "/provider"
_PROVIDERS_CMD = "/providers"
_MODEL_CMD = "/model"
_MODELS_CMD = "/models"
_AUTO_CMD = "/auto"
_STATUS_CMD = "/status"

_SYSTEM_BASE = (
    "You are JARVIS-X, an autonomous AI agent. "
    "You can help with coding, research, planning, and general questions. "
    "You have access to tools, memory, and documents."
)


class Jarvis:
    """JARVIS-X — Asosiy AI Agent Orchestrator."""

    def __init__(
        self,
        default_mode: str = "pro",
        voice_enabled: bool = False,
        rag_dir: Optional[str] = None,
    ) -> None:
        self.router = AIRouter()
        self.mode_manager = ModeManager(default_mode=default_mode)
        self.language = LanguageDetector()
        self.memory = MemoryManager()
        self.tools = ToolRegistry()
        self.rag = RAGEngine()
        self._register_builtin_tools()

        # RAG hujjatlarini yuklash
        if rag_dir:
            try:
                self.rag.ingest_directory(rag_dir)
            except Exception:
                pass

    def _register_builtin_tools(self) -> None:
        """O'rnatilgan vositalarni ro'yxatga olish."""
        try:
            from tools.web_search import WebSearchTool

            ws = WebSearchTool()
            self.tools.register("web_search", ws.search, "Internet qidiruvchi")
        except Exception:
            pass

        try:
            from tools.file_manager import FileManagerTool

            fm = FileManagerTool()
            self.tools.register("read_file", fm.read_file, "Faylni o'qish")
            self.tools.register("write_file", fm.write_file, "Faylga yozish")
            self.tools.register("list_dir", fm.list_directory, "Katalogni ko'rish")
        except Exception:
            pass

        try:
            from tools.code_executor import CodeExecutorTool

            ce = CodeExecutorTool()
            self.tools.register("run_code", ce.execute, "Python kodni bajarish")
        except Exception:
            pass

        try:
            from tools.terminal import TerminalTool

            term = TerminalTool()
            self.tools.register("terminal", term.execute, "Terminal buyrug'ini bajarish")
        except Exception:
            pass

    def process(self, user_input: str) -> str:
        """Foydalanuvchi kiritishini qayta ishlash va javob qaytarish.

        ReAct tsikli: Reason → Act → Observe → Respond

        Args:
            user_input: Foydalanuvchi matni

        Returns:
            JARVIS javobi
        """
        if not user_input.strip():
            return ""

        # Rejim almashtirish buyruqlarini tekshirish
        parts = user_input.strip().split()
        cmd = parts[0].lower() if parts else ""
        if cmd in _MODE_COMMANDS:
            mode_name = _MODE_COMMANDS[cmd]
            self.mode_manager.set_mode(mode_name)
            mode_info = self.mode_manager.get_mode()
            return f"✅ Rejim o'zgartirildi: **{mode_info['name']}**"

        # /provider yoki /providers — provayder holati yoki tanlash
        if cmd in (_PROVIDER_CMD, _PROVIDERS_CMD):
            if len(parts) >= 2:
                provider_name = parts[1].lower()
                try:
                    self.router.set_provider(provider_name)
                    return f"✅ Provayder tanlandi: **{provider_name}**\nAutomatik rejimga qaytish uchun /auto ishlating."
                except ValueError as exc:
                    return f"❌ {exc}"
            else:
                return self.router.list_providers_status()

        # /model yoki /models — model holati yoki tanlash
        if cmd in (_MODEL_CMD, _MODELS_CMD):
            if len(parts) >= 2:
                model_name = " ".join(parts[1:])
                self.router.set_model(model_name)
                return f"✅ Model tanlandi: **{model_name}**\nAutomatik rejimga qaytish uchun /auto ishlating."
            else:
                return self.router.list_all_models()

        # /auto — avtomatik rejimga qaytish
        if cmd == _AUTO_CMD:
            self.router.reset_auto()
            return "✅ Avtomatik rejimga qaytildi. Provider va model avtomatik tanlanadi."

        # /status — hozirgi holat
        if cmd == _STATUS_CMD:
            status = self.get_status()
            forced_provider = self.router.get_current_provider()
            forced_model = self.router.get_current_model()
            provider_str = forced_provider if forced_provider else "avtomatik (fallback)"
            model_str = forced_model if forced_model else "avtomatik (rejimga qarab)"
            available = ", ".join(status["providers"]) if status["providers"] else "yo'q"
            ai_icon = "✅" if status["ai_available"] else "❌"
            return (
                "**Hozirgi holat:**\n"
                f"  • Rejim: **{status['mode'].upper()}**\n"
                f"  • Provayder: **{provider_str}**\n"
                f"  • Model: **{model_str}**\n"
                f"  • Mavjud provayderlar: {available}\n"
                f"  • AI tayyor: {ai_icon}"
            )

        # Tilni aniqlash
        detected_lang = self.language.detect(user_input)

        # Xotiraga qo'shish
        self.memory.add_to_short_term("user", user_input)

        # RAG qidiruvini amalga oshirish
        rag_context = ""
        try:
            rag_results = self.rag.query(user_input, k=3)
            if rag_results:
                rag_context = "\n\nMavjud hujjatlardan kontekst:\n" + "\n---\n".join(
                    f"[{r['source']}]: {r['content']}" for r in rag_results
                )
        except Exception:
            pass

        # Uzoq muddatli xotiradan qidirish
        memory_context = ""
        try:
            memory_results = self.memory.search_long_term(user_input, k=3)
            if memory_results:
                memory_context = "\n\nOldingi suhbatlardan:\n" + "\n".join(
                    r["content"] for r in memory_results
                )
        except Exception:
            pass

        # Tizim promptini yaratish
        system_prompt = self.mode_manager.get_system_prompt()
        lang_instruction = self.language.get_language_instruction()
        if lang_instruction:
            system_prompt = f"{system_prompt}\n\n{lang_instruction}"
        if rag_context:
            system_prompt += rag_context
        if memory_context:
            system_prompt += memory_context

        # Xabarlar ro'yxatini tayyorlash
        messages: list[dict] = [{"role": "system", "content": system_prompt}]
        messages.extend(self.memory.get_conversation_history())

        # AI ga so'rov yuborish
        mode = self.mode_manager.get_current_mode_name()
        try:
            response = self.router.route_request(
                messages=messages,
                mode=mode,
            )
        except Exception as exc:
            response = f"❌ AI provayderi bilan bog'lanishda xato: {exc}"

        # Javobni xotiraga saqlash
        self.memory.add_to_short_term("assistant", response)

        # Uzoq muddatli xotiraga saqlash (muhim suhbatlar)
        try:
            combined = f"Savol: {user_input}\nJavob: {response}"
            self.memory.add_to_long_term(combined, {"mode": mode, "lang": detected_lang})
        except Exception:
            pass

        return response

    def get_status(self) -> dict:
        """Joriy holat ma'lumotlari."""
        return {
            "mode": self.mode_manager.get_current_mode_name(),
            "language": self.language.get_response_language(),
            "ai_available": self.router.is_available(),
            "providers": self.router.get_available_providers(),
            "memory": self.memory.get_stats(),
            "rag": self.rag.get_stats(),
            "tools": self.tools.get_tool_names(),
        }

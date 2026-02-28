"""JARVIS-X — Asosiy entry point. Rich UI bilan interaktiv terminal interfeysi."""

from __future__ import annotations

import sys
from typing import Any

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from core.jarvis import JarvisX
from core.modes import Mode

# ── Rang xaritalari ──────────────────────────────────────────────────────────
MODE_COLORS: dict[str, str] = {
    Mode.FAST: "cyan",
    Mode.CODE: "green",
    Mode.PRO: "magenta",
}

JARVIS_BANNER = r"""
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗    ██╗  ██╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ╚██╗██╔╝
     ██║███████║██████╔╝██║   ██║██║███████╗     ╚███╔╝ 
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║     ██╔██╗ 
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║    ██╔╝ ██╗
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝    ╚═╝  ╚═╝
         Advanced AI Agent  |  v2.0  |  Multi-Provider
"""

HELP_TEXT = """
[bold cyan]Mavjud buyruqlar:[/bold cyan]

  [cyan]/mode fast[/cyan]          → Tez rejim (qisqa javoblar, Groq)
  [cyan]/mode code[/cyan]          → Kod rejimi (dasturlash, OpenRouter)
  [cyan]/mode pro[/cyan]           → Pro rejim (chuqur tahlil, OpenAI)

  [green]/voice[/green]              → Ovoz rejimini yoqish/o'chirish
  [green]/models[/green]             → Mavjud modellar ro'yxati
  [green]/providers[/green]          → Provayderlar holati
  [green]/provider <name>[/green]    → Ma'lum provayderni tanlash (openai/groq/openrouter)

  [yellow]/ingest <path>[/yellow]     → Hujjat yuklash
  [yellow]/remember <text>[/yellow]   → Xotiraga saqlash
  [yellow]/recall <query>[/yellow]    → Xotiradan qidirish

  [red]/clear[/red]               → Suhbatni tozalash
  [red]/help[/red]                → Ushbu yordam
  [red]/exit[/red]                → Chiqish
"""


class JarvisUI:
    """JARVIS-X terminal foydalanuvchi interfeysi."""

    def __init__(self) -> None:
        """Konsolni va JARVIS-X ni ishga tushiradi."""
        self.console = Console() if RICH_AVAILABLE else None
        self.jarvis = JarvisX()
        self._voice_enabled = False
        self._preferred_provider: str | None = None

    # ------------------------------------------------------------------
    # Print helpers
    # ------------------------------------------------------------------

    def _print(self, text: str, **kwargs: Any) -> None:
        if self.console:
            self.console.print(text, **kwargs)
        else:
            # Rich markup ni oddiy matndan tozalash (minimal)
            import re

            plain = re.sub(r"\[/?[^\]]+\]", "", text)
            print(plain)

    def _panel(self, content: str, title: str = "", style: str = "white") -> None:
        if self.console:
            self.console.print(Panel(content, title=title, border_style=style))
        else:
            print(f"\n{'='*60}")
            if title:
                print(f"  {title}")
            print(content)
            print("=" * 60)

    # ------------------------------------------------------------------
    # Banner & startup
    # ------------------------------------------------------------------

    def _show_banner(self) -> None:
        if self.console:
            self.console.print(Text(JARVIS_BANNER, style="bold magenta"))
            self.console.print(
                "[bold white]O'zbek va Ingliz tillarini qo'llab-quvvatlaydi. "
                "/help — buyruqlar ro'yxati.[/bold white]\n"
            )
        else:
            print(JARVIS_BANNER)
            print("O'zbek va Ingliz tillarini qo'llab-quvvatlaydi. /help — buyruqlar.\n")

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    def _handle_command(self, cmd: str) -> bool:
        """Maxsus buyruqni qayta ishlaydi.

        Args:
            cmd: Foydalanuvchi kiritgan buyruq (/ bilan boshlanadi).

        Returns:
            True — davom etish, False — chiqish.
        """
        parts = cmd.strip().split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command == "/exit":
            self._print("[bold red]JARVIS-X o'chirilmoqda... Xayr![/bold red]")
            return False

        elif command == "/help":
            self._print(HELP_TEXT)

        elif command == "/clear":
            if self.console:
                self.console.clear()
            else:
                print("\n" * 5)
            self._show_banner()

        elif command == "/mode":
            self._set_mode(arg)

        elif command == "/voice":
            self._toggle_voice()

        elif command == "/models":
            self._show_models()

        elif command == "/providers":
            self._show_providers()

        elif command == "/provider":
            self._set_provider(arg)

        elif command == "/ingest":
            self._ingest(arg)

        elif command == "/remember":
            self._remember(arg)

        elif command == "/recall":
            self._recall(arg)

        else:
            self._print(f"[red]Noma'lum buyruq: {command}. /help ga qarang.[/red]")

        return True

    def _set_mode(self, arg: str) -> None:
        mode_map = {"fast": Mode.FAST, "code": Mode.CODE, "pro": Mode.PRO}
        mode = mode_map.get(arg.lower())
        if mode:
            self.jarvis.mode_manager.set_mode(mode)
            color = MODE_COLORS[mode]
            self._print(f"[{color}]✓ Rejim o'zgartirildi: [bold]{mode.value.upper()}[/bold][/{color}]")
        else:
            self._print("[red]Noto'g'ri rejim. fast | code | pro dan birini tanlang.[/red]")

    def _toggle_voice(self) -> None:
        if not self.jarvis.voice.is_available():
            self._print(
                "[yellow]Ovoz kutubxonalari o'rnatilmagan.\n"
                "O'rnatish: pip install SpeechRecognition pyttsx3[/yellow]"
            )
            return
        self._voice_enabled = not self._voice_enabled
        state = "yoqildi ✓" if self._voice_enabled else "o'chirildi ✗"
        self._print(f"[green]Ovoz rejimi {state}[/green]")

    def _show_models(self) -> None:
        models = self.jarvis.ai_router.list_models()
        lines = []
        for provider, modes in models.items():
            lines.append(f"\n[bold]{provider.upper()}[/bold]")
            for m, name in modes.items():
                lines.append(f"  {m:8} → {name}")
        self._panel("\n".join(lines), title="🤖 Mavjud Modellar", style="cyan")

    def _show_providers(self) -> None:
        providers = self.jarvis.ai_router.list_providers()
        lines = []
        for name, info in providers.items():
            status = "[green]✓ Faol[/green]" if info["has_key"] else "[red]✗ API kalit yo'q[/red]"
            active = " ← [yellow]tanlangan[/yellow]" if name == self._preferred_provider else ""
            lines.append(f"  {name:12} {status}{active}")
        self._panel("\n".join(lines), title="🔌 Provayderlar Holati", style="green")

    def _set_provider(self, arg: str) -> None:
        valid = {"openai", "groq", "openrouter"}
        if arg.lower() in valid:
            self._preferred_provider = arg.lower()
            self._print(f"[green]✓ Provider tanlandi: [bold]{arg}[/bold][/green]")
        else:
            self._print("[red]Noto'g'ri provider. openai | groq | openrouter[/red]")

    def _ingest(self, path: str) -> None:
        if not path:
            self._print("[red]Fayl yo'lini kiriting: /ingest <path>[/red]")
            return
        kb = self.jarvis._knowledge_base
        if kb is None:
            self._print("[yellow]KnowledgeBase mavjud emas.[/yellow]")
            return
        try:
            kb.ingest(path)
            self._print(f"[green]✓ Hujjat yuklandi: {path}[/green]")
        except Exception as exc:
            self._print(f"[red]Xato: {exc}[/red]")

    def _remember(self, text: str) -> None:
        if not text:
            self._print("[red]Matnni kiriting: /remember <text>[/red]")
            return
        mem = self.jarvis._long_memory
        if mem is None:
            self._print("[yellow]LongTermMemory mavjud emas.[/yellow]")
            return
        try:
            mem.save(text)
            self._print("[green]✓ Xotiraga saqlandi.[/green]")
        except Exception as exc:
            self._print(f"[red]Xato: {exc}[/red]")

    def _recall(self, query: str) -> None:
        if not query:
            self._print("[red]So'rovni kiriting: /recall <query>[/red]")
            return
        mem = self.jarvis._long_memory
        if mem is None:
            self._print("[yellow]LongTermMemory mavjud emas.[/yellow]")
            return
        try:
            results = mem.search(query)
            self._panel(str(results), title="🔍 Xotira natijalari", style="yellow")
        except Exception as exc:
            self._print(f"[red]Xato: {exc}[/red]")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def _get_prompt_text(self) -> str:
        mode = self.jarvis.mode_manager.current_mode
        color = MODE_COLORS[mode]
        if RICH_AVAILABLE:
            return f"[{color}][{mode.value.upper()}][/{color}] You: "
        return f"[{mode.value.upper()}] You: "

    def run(self) -> None:
        """Asosiy interaktiv tsiklni ishga tushiradi."""
        self._show_banner()

        while True:
            try:
                # Ovoz rejimi yoqilgan bo'lsa mikrofondan o'qish
                if self._voice_enabled:
                    self._print("[cyan]🎙️  Gapiring yoki matn kiriting:[/cyan]")

                if RICH_AVAILABLE:
                    user_input = Prompt.ask(self._get_prompt_text())
                else:
                    user_input = input(self._get_prompt_text())

                if not user_input.strip():
                    continue

                # Maxsus buyruqlarni tekshirish
                if user_input.strip().startswith("/"):
                    if not self._handle_command(user_input.strip()):
                        break
                    continue

                # Ovoz rejimida ham matn so'rovi ishlanadi
                mode = self.jarvis.mode_manager.current_mode
                color = MODE_COLORS[mode]

                try:
                    response = self.jarvis.process(user_input)
                    provider, model = self.jarvis.ai_router.get_active_provider_and_model(
                        mode.value, self._preferred_provider
                    )
                    title = f"🤖 JARVIS-X [{mode.value.upper()}] via {provider}/{model}"
                    self._panel(response, title=title, style=color)

                    if self._voice_enabled:
                        self.jarvis.voice.speak(response)

                except Exception as exc:
                    self._print(f"[red]Xato yuz berdi: {exc}[/red]")

            except KeyboardInterrupt:
                self._print("\n[bold red]To'xtatildi. /exit — chiqish uchun.[/bold red]")
            except EOFError:
                break


def main() -> None:
    """JARVIS-X ni ishga tushiradi."""
    ui = JarvisUI()
    ui.run()


if __name__ == "__main__":
    main()

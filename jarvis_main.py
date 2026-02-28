"""JARVIS-X — Rich terminal entry point.

Provides an interactive REPL with special slash commands, coloured
output, and provider/model/mode status display.
"""

from __future__ import annotations

import sys
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich import print as rprint
    _rich_available = True
except ImportError:  # pragma: no cover
    _rich_available = False

from config.settings import get_settings
from core.jarvis import JarvisX
from core.modes import Mode, ModeManager

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_BANNER = r"""
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗      ██╗  ██╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝      ╚██╗██╔╝
     ██║███████║██████╔╝██║   ██║██║███████╗       ╚███╔╝ 
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║       ██╔██╗ 
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║      ██╔╝ ██╗
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝      ╚═╝  ╚═╝
               Multi-AI Agent — v2.0 (JARVIS-X)
"""

_MODE_COLORS: dict[str, str] = {
    "fast": "cyan",
    "code": "green",
    "pro": "magenta",
}

_HELP_TEXT = """
[bold]JARVIS-X Buyruqlari:[/bold]

  [cyan]/mode fast|code|pro[/cyan]   — Rejimni o'zgartirish
  [cyan]/voice[/cyan]                — Ovoz rejimi toggle
  [cyan]/models[/cyan]               — Barcha modellar ro'yxati
  [cyan]/providers[/cyan]            — Provider holati
  [cyan]/provider <name>[/cyan]      — Provider tanlash (openrouter/groq/openai)
  [cyan]/ingest <path>[/cyan]        — Hujjat yuklash (knowledge base)
  [cyan]/remember <text>[/cyan]      — Xotiraga saqlash
  [cyan]/recall <query>[/cyan]       — Xotiradan qidirish
  [cyan]/clear[/cyan]                — Ekranni tozalash
  [cyan]/help[/cyan]                 — Yordam ko'rsatish
  [cyan]/exit[/cyan]                 — Dasturdan chiqish
"""


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _make_console() -> "Optional[Console]":
    """Return a Rich Console or None when Rich is unavailable."""
    if _rich_available:
        from rich.console import Console  # noqa: PLC0415
        return Console()
    return None


def _print(console: Optional["Console"], message: str, style: str = "") -> None:
    """Print using Rich when available, otherwise plain print.

    Args:
        console: Rich Console instance or None.
        message: Message to display.
        style: Rich style string (ignored when Rich is unavailable).
    """
    if console is not None:
        console.print(message, style=style)
    else:
        # Strip basic Rich markup for plain output
        import re
        plain = re.sub(r"\[/?[^\]]+\]", "", message)
        print(plain)


def _print_banner(console: Optional["Console"]) -> None:
    """Display the JARVIS-X ASCII art banner."""
    if console is not None:
        from rich.panel import Panel  # noqa: PLC0415
        console.print(Panel(_BANNER, style="bold blue", expand=False))
    else:
        print(_BANNER)


def _mode_color(mode: str) -> str:
    """Return the Rich color name for a mode.

    Args:
        mode: Mode string value.

    Returns:
        Color name string.
    """
    return _MODE_COLORS.get(mode, "white")


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def _handle_mode(args: str, jarvis: JarvisX, console: Optional["Console"]) -> None:
    """Handle /mode command.

    Args:
        args: Remaining argument string after '/mode'.
        jarvis: Active JarvisX instance.
        console: Rich Console for output.
    """
    mode_str = args.strip().lower()
    try:
        new_mode = Mode(mode_str)
        jarvis.mode_manager.set_mode(new_mode)
        color = _mode_color(mode_str)
        _print(console, f"[{color}]✓ Rejim o'zgartirildi: {mode_str.upper()}[/{color}]")
    except ValueError:
        _print(console, "[red]Noto'g'ri rejim. fast, code yoki pro tanlang.[/red]")


def _handle_providers(jarvis: JarvisX, console: Optional["Console"]) -> None:
    """Handle /providers command."""
    providers = jarvis.ai_router.list_providers()
    _print(console, "\n[bold]Provider holati:[/bold]")
    for name, info in providers.items():
        status = "[green]✓ Mavjud[/green]" if info["available"] else "[red]✗ Kalit yo'q[/red]"
        _print(console, f"  {name:12s} {status}  ({info['base_url']})")
    _print(console, "")


def _handle_models(jarvis: JarvisX, console: Optional["Console"]) -> None:
    """Handle /models command."""
    models = jarvis.ai_router.list_models()
    _print(console, "\n[bold]Mavjud modellar:[/bold]")
    for provider, modes in models.items():
        _print(console, f"\n  [bold]{provider}[/bold]")
        for mode_name, model in modes.items():
            color = _mode_color(mode_name)
            _print(console, f"    [{color}]{mode_name:6s}[/{color}] → {model}")
    _print(console, "")


def _handle_voice_toggle(jarvis: JarvisX, console: Optional["Console"]) -> None:
    """Handle /voice command."""
    if jarvis.voice_engine.is_available():
        _print(console, "[yellow]Ovoz rejimi mavjud. /voice buyrug'ini ishlatish uchun ovozli kirish boshlaning.[/yellow]")
        result = jarvis.process_voice()
        if result:
            _display_response(result, console)
    else:
        _print(console, "[red]Ovoz tizimi mavjud emas. SpeechRecognition va pyttsx3/gTTS o'rnating.[/red]")


def _display_response(result: dict, console: Optional["Console"]) -> None:
    """Display an AI response with metadata.

    Args:
        result: Response dict from JarvisX.process().
        console: Rich Console for output.
    """
    mode = result.get("mode", "pro")
    provider = result.get("provider", "?")
    model = result.get("model", "?")
    response = result.get("response", "")
    language = result.get("language", "en")
    color = _mode_color(mode)

    meta = f"[dim]{provider} / {model} / {mode.upper()} / {language.upper()}[/dim]"
    _print(console, f"\n[{color}]JARVIS-X:[/{color}] {response}")
    _print(console, meta)
    _print(console, "")


# ---------------------------------------------------------------------------
# Main REPL
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the JARVIS-X interactive terminal session."""
    console = _make_console()
    _print_banner(console)

    try:
        jarvis = JarvisX()
    except Exception as exc:  # noqa: BLE001
        _print(console, f"[red]JARVIS-X ishga tushirishda xato: {exc}[/red]")
        sys.exit(1)

    settings = get_settings()

    # Apply default mode from settings
    try:
        default_mode = Mode(settings.jarvis_default_mode)
        jarvis.mode_manager.set_mode(default_mode)
    except ValueError:
        pass  # Keep PRO as default

    current_provider: Optional[str] = None

    _print(console, "[bold green]JARVIS-X tayyor! /help — yordam.[/bold green]\n")

    while True:
        mode = jarvis.mode_manager.current_mode
        color = _mode_color(mode.value)
        prompt_label = f"[{color}][{mode.value.upper()}][/{color}] > "

        try:
            if console is not None:
                from rich.prompt import Prompt  # noqa: PLC0415
                user_input = Prompt.ask(prompt_label)
            else:
                user_input = input(f"[{mode.value.upper()}] > ")
        except (KeyboardInterrupt, EOFError):
            _print(console, "\n[yellow]Chiqilmoqda...[/yellow]")
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        # ------------------------------------------------------------------
        # Slash commands
        # ------------------------------------------------------------------
        if user_input.startswith("/"):
            parts = user_input[1:].split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if cmd == "exit":
                _print(console, "[yellow]Xayr! Keyingi safargacha.[/yellow]")
                break

            elif cmd == "help":
                if console is not None:
                    console.print(_HELP_TEXT)
                else:
                    print(_HELP_TEXT)

            elif cmd == "clear":
                if console is not None:
                    console.clear()
                else:
                    print("\033[2J\033[H", end="")
                _print_banner(console)

            elif cmd == "mode":
                _handle_mode(args, jarvis, console)

            elif cmd == "providers":
                _handle_providers(jarvis, console)

            elif cmd == "models":
                _handle_models(jarvis, console)

            elif cmd == "provider":
                current_provider = args.strip().lower() or None
                if current_provider:
                    _print(console, f"[cyan]Provider tanlandi: {current_provider}[/cyan]")
                else:
                    _print(console, "[yellow]Provider tanlovi bekor qilindi (avtomatik).[/yellow]")

            elif cmd == "voice":
                _handle_voice_toggle(jarvis, console)

            elif cmd == "ingest":
                path = args.strip()
                _print(console, f"[yellow]Hujjat yuklanmoqda: {path} — bu funksiya knowledge/ moduli orqali amalga oshiriladi.[/yellow]")

            elif cmd == "remember":
                text = args.strip()
                _print(console, f"[yellow]Xotiraga saqlash: '{text}' — bu funksiya memory/ moduli orqali amalga oshiriladi.[/yellow]")

            elif cmd == "recall":
                query = args.strip()
                _print(console, f"[yellow]Xotiradan qidirish: '{query}' — bu funksiya memory/ moduli orqali amalga oshiriladi.[/yellow]")

            else:
                _print(console, f"[red]Noma'lum buyruq: /{cmd}. /help ni ko'ring.[/red]")

            continue

        # ------------------------------------------------------------------
        # Regular AI query
        # ------------------------------------------------------------------
        try:
            result = jarvis.process(user_input, preferred_provider=current_provider)
            _display_response(result, console)
        except Exception as exc:  # noqa: BLE001
            _print(console, f"[red]Xato: {exc}[/red]")


if __name__ == "__main__":
    main()

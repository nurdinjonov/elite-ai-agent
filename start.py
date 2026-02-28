"""
JARVIS-X — Asosiy ishga tushirish nuqtasi.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Toshkent vaqt zonasi (UTC+5)
_TASHKENT_TZ = timezone(timedelta(hours=5))

_BANNER = r"""
     ___  ___  ________  ________  ___      ___ ___  ________     ___    ___
    |\  \|\  \|\   __  \|\   __  \|\  \    /  /|\  \|\   ____\   |\  \  /  /|
    \ \  \\\  \ \  \|\  \ \  \|\  \ \  \  /  / | \  \ \  \___|   \ \  \/  / /
     \ \   __  \ \   __  \ \   _  _\ \  \/  / / \ \  \ \_____  \  \ \    / /
      \ \  \ \  \ \  \ \  \ \  \\  \\ \    / /   \ \  \|____|\  \  /     \/
       \ \__\ \__\ \__\ \__\ \__\\ _\\ \__/ /     \ \__\____\_\  \/  /\   \
        \|__|\|__|\|__|\|__|\|__|\|__|\|__|/       \|__|\_________/__/ /\ __\
                                                        \|_______||__|/ \|__|

                    JARVIS-X — Avtonom AI Agent v1.0.0
            Smart Life Assistant + AI + Memory + Tools + RAG
"""

_COMMANDS_HELP = """
  [bold cyan]Tabiiy tilda:[/bold cyan]
    bugungi darslar    — jadval ko'rsatish
    uy vazifalari      — homework ro'yxati
    bugungi reja       — kunlik reja
    statistika         — statistika
    kognitiv yuk       — kognitiv yuk tahlili
    haftalik tahlil    — haftalik aks ettirish
    focus boshlash     — Pomodoro sessiyasi
    focus to'xtat      — Pomodoro to'xtatish
    yordam             — yordam

  [bold cyan]Slash buyruqlar:[/bold cyan]
    /fast /code /pro   — rejim o'zgartirish
    /status            — tizim holati
    /today             — bugungi to'liq sharh
    /cognitive         — kognitiv yuk
    /reflect           — haftalik tahlil
    /exit              — chiqish
"""


def _clear_screen() -> None:
    """Terminalni tozalash (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def _tashkent_now() -> str:
    """Hozirgi Toshkent vaqtini ``YYYY-MM-DD HH:MM:SS`` formatida qaytarish."""
    return datetime.now(_TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S")


def _render_header(console: object, mode: str, ai_ready: bool) -> None:
    """Persistent header-ni render qilish.

    Args:
        console: Rich Console obyekti.
        mode: Joriy rejim nomi.
        ai_ready: AI tayyor holati.
    """
    from rich.console import Console as _Console

    c: _Console = console  # type: ignore[assignment]
    ai_icon = "🟢 Tayyor" if ai_ready else "🔴 Tayyor emas"
    sep = "═" * 42
    c.print(f"[bold cyan]{sep}[/bold cyan]")
    c.print(f"[bold cyan]{'JARVIS • AI AGENT':^42}[/bold cyan]")
    c.print(f"[bold cyan]{sep}[/bold cyan]")
    c.print(f"  [dim]📍 Toshkent: {_tashkent_now()}[/dim]")
    c.print(f"  [dim]🧭 Rejim: {mode.upper()} | {ai_icon}[/dim]")
    c.print(f"[bold cyan]{sep}[/bold cyan]")


def _log_interaction(log_file: Path, user_input: str, response: str, mode: str) -> None:
    """Suhbatni log faylga saqlash."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(_TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [MODE: {mode}]\n")
        f.write(f"🧑 Siz: {user_input}\n")
        f.write(f"🤖 JARVIS: {response}\n")
        f.write("-" * 40 + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="JARVIS-X — Avtonom AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["fast", "code", "pro"],
        default="pro",
        help="AI rejimi (default: pro)",
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        default=False,
        help="Ovoz rejimini yoqish",
    )
    parser.add_argument(
        "--life-only",
        action="store_true",
        default=False,
        help="Faqat Life Assistant rejimida ishga tushirish",
    )
    parser.add_argument(
        "--rag-dir",
        default=None,
        help="RAG uchun hujjatlar katalogi",
    )
    return parser.parse_args()


def run_life_assistant() -> None:
    """jarvis_life.py ni ishga tushirish."""
    import subprocess

    life_script = Path(__file__).parent / "jarvis_life.py"
    if not life_script.exists():
        print(f"Xato: jarvis_life.py topilmadi: {life_script}")
        sys.exit(1)
    subprocess.run([sys.executable, str(life_script)])


def run_jarvis(args: argparse.Namespace) -> None:
    """To'liq JARVIS-X agentini ishga tushirish."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.markdown import Markdown
    except ImportError:
        print("Rich kutubxonasi topilmadi. O'rnating: pip install rich")
        sys.exit(1)

    console = Console()

    # Jarvis ni ishga tushirish
    try:
        from core.jarvis import Jarvis

        jarvis = Jarvis(
            default_mode=args.mode,
            voice_enabled=args.voice,
            rag_dir=args.rag_dir,
        )
    except Exception as exc:
        console.print(f"[red]JARVIS ishga tushirishda xato: {exc}[/red]")
        sys.exit(1)

    # Intent parser va smart features
    try:
        from core.intent_parser import IntentParser
        from core.smart_features import SmartFeatures

        parser_obj = IntentParser()
        smart = SmartFeatures()
    except Exception:
        parser_obj = None  # type: ignore[assignment]
        smart = None  # type: ignore[assignment]

    log_file = Path(__file__).parent / "data" / "chat_history.log"

    # Ovoz rejimi
    voice_engine = None
    if args.voice:
        try:
            from core.voice import VoiceEngine

            voice_engine = VoiceEngine(enabled=True)
        except Exception:
            pass

    # Startup ekrani
    _clear_screen()
    console.print(f"[bold cyan]{_BANNER}[/bold cyan]")

    status = jarvis.get_status()
    ai_status = "[green]✅ Tayyor[/green]" if status["ai_available"] else "[yellow]⚠️ API kalit yo'q[/yellow]"
    providers = ", ".join(status["providers"]) if status["providers"] else "yo'q"
    tools_str = ", ".join(status["tools"]) or "yo'q"

    console.print(
        Panel(
            f"[bold]Rejim:[/bold] {status['mode'].upper()}\n"
            f"[bold]AI:[/bold] {ai_status}\n"
            f"[bold]Provayderlar:[/bold] {providers}\n"
            f"[bold]Xotira:[/bold] {status['memory']['storage_backend']}\n"
            f"[bold]Vositalar:[/bold] {tools_str}",
            title="🤖 JARVIS-X Holati",
            border_style="cyan",
        )
    )
    console.print(_COMMANDS_HELP)

    last_query: str | None = None
    last_response: str | None = None

    # Asosiy tsikl
    while True:
        _clear_screen()
        current_status = jarvis.get_status()
        _render_header(console, current_status["mode"], current_status["ai_available"])

        # Oxirgi savol-javobni ko'rsatish
        if last_query and last_response:
            console.print(f"\n[bold cyan]🧑 Siz:[/bold cyan] {last_query}\n")
            console.print("[bold green]🤖 JARVIS:[/bold green]")
            try:
                console.print(Markdown(last_response))
            except Exception:
                console.print(last_response)
            console.print()

        try:
            if voice_engine and getattr(voice_engine, "stt_available", False):
                console.print("[dim]Gapirishingiz mumkin yoki yozing...[/dim]")
            user_input = console.input("[bold cyan]🧑 Siz:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Xayr! Yaxshi kun tilaymiz! 👋[/yellow]")
            break

        if not user_input:
            continue

        # Exit tekshirish
        if user_input.lower() in ("/exit", "/quit", "/q", "chiqish", "xayr", "exit"):
            console.print("[yellow]Xayr! Yaxshi kun tilaymiz! 👋[/yellow]")
            break

        # Intent tahlili
        intent_info: dict = {}
        if parser_obj is not None:
            try:
                intent_info = parser_obj.parse(user_input)
            except Exception:
                intent_info = {}

        # Smart features: add_task uchun duplicate va conflict tekshiruvi
        if smart is not None and intent_info.get("intent") == "add_task":
            params = intent_info.get("params", {})
            new_time = params.get("time", "")
            new_title = params.get("title", "")
            try:
                from life import HomeworkManager
                hw = HomeworkManager()
                existing_tasks = [
                    {
                        "title": t.title,
                        "start_time": getattr(t, "start_time", ""),
                        "end_time": getattr(t, "end_time", ""),
                    }
                    for t in hw.get_all_pending()
                    if not isinstance(t, dict)
                ]
            except Exception:
                existing_tasks = []

            if new_title and smart.check_duplicate({"title": new_title}, existing_tasks):
                console.print(
                    f"[yellow]⚠️  Bu nomli vazifa allaqachon mavjud: '{new_title}'[/yellow]"
                )

            if new_time:
                schedule_list = [
                    {
                        "start_time": t.get("start_time", ""),
                        "end_time": t.get("end_time", ""),
                        "title": t.get("title", ""),
                    }
                    for t in existing_tasks
                ]
                conflicts = smart.check_conflict(new_time, schedule_list)
                if conflicts:
                    conflict_titles = ", ".join(c.get("title", "?") for c in conflicts)
                    suggested = smart.suggest_reschedule(new_time, schedule_list)
                    console.print(
                        f"[yellow]⚠️  Vaqt to'qnashuvi ({new_time}): {conflict_titles}. "
                        f"Tavsiya: {suggested}[/yellow]"
                    )

        # Javob olish
        with console.status("[dim]Fikrlayapman...[/dim]"):
            response = jarvis.process(user_input)

        # Terminal beep (eslatma uchun)
        print("\a", end="", flush=True)

        # Suhbat logini saqlash
        current_mode = jarvis.get_status().get("mode", "unknown")
        _log_interaction(log_file, user_input, response, current_mode)

        # Keyingi render uchun saqlash
        last_query = user_input
        last_response = response

        # Ovozli javob
        if voice_engine and getattr(voice_engine, "is_available", False):
            try:
                voice_engine.speak(response)
            except Exception:
                pass


def main() -> None:
    args = parse_args()

    if args.life_only:
        run_life_assistant()
    else:
        run_jarvis(args)


if __name__ == "__main__":
    main()

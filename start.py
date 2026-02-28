"""
JARVIS-X — Asosiy ishga tushirish nuqtasi.
"""

from __future__ import annotations

import argparse
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

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
    from pathlib import Path

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
    console.print(f"[bold cyan]{_BANNER}[/bold cyan]")

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

    console.print(
        "\n[dim]Buyruqlar: /fast, /code, /pro — rejim almashtirish | /exit — chiqish[/dim]\n"
    )

    # Ovoz rejimi
    voice_engine = None
    if args.voice:
        try:
            from core.voice import VoiceEngine

            voice_engine = VoiceEngine(enabled=True)
            if voice_engine.is_available:
                console.print("[green]🎙 Ovoz rejimi yoqildi[/green]")
            else:
                console.print("[yellow]⚠️ Ovoz tizimi ishga tushmadi[/yellow]")
        except Exception:
            pass

    # Asosiy tsikl
    while True:
        try:
            if voice_engine and voice_engine.stt_available:
                console.print("[dim]Gapirishingiz mumkin yoki yozing...[/dim]")

            user_input = console.input("[bold cyan]🧑 Siz:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Xayr! Yaxshi kun tilaymiz! 👋[/yellow]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/exit", "/quit", "/q"):
            console.print("[yellow]Xayr! Yaxshi kun tilaymiz! 👋[/yellow]")
            break

        # Javob olish
        with console.status("[dim]Fikrlayapman...[/dim]"):
            response = jarvis.process(user_input)

        console.print(f"\n[bold green]🤖 JARVIS:[/bold green]")
        try:
            console.print(Markdown(response))
        except Exception:
            console.print(response)
        console.print()

        # Ovozli javob
        if voice_engine and voice_engine.is_available:
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

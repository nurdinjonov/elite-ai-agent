"""Interactive terminal UI for EliteAgent."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from elite_agent.agent.graph import build_agent_graph
from elite_agent.config.settings import settings
from elite_agent.knowledge.ingest import KnowledgeBase
from elite_agent.memory.long_term import LongTermMemory
from elite_agent.memory.short_term import ShortTermMemory

console = Console()


def print_banner() -> None:
    """Display a welcome banner in the terminal."""
    banner = Text()
    banner.append("╔══════════════════════════════════════╗\n", style="bold cyan")
    banner.append("║         🤖  EliteAgent  🤖            ║\n", style="bold cyan")
    banner.append("║  ReAct + LangGraph + RAG + ChromaDB  ║\n", style="cyan")
    banner.append("╚══════════════════════════════════════╝\n", style="bold cyan")
    console.print(banner)
    console.print(
        Panel(
            "[bold green]Buyruqlar:[/bold green]\n"
            "  [yellow]/ingest <yo'l>[/yellow]   — Hujjatni bilim bazasiga yuklash\n"
            "  [yellow]/remember <matn>[/yellow] — Matnni uzoq muddatli xotiraga saqlash\n"
            "  [yellow]/recall <so'rov>[/yellow] — Uzoq muddatli xotiradan qidirish\n"
            "  [yellow]/clear[/yellow]           — Suhbat tarixini tozalash\n"
            "  [yellow]/exit[/yellow]            — Dasturdan chiqish",
            title="[bold]Qo'llanma[/bold]",
            border_style="dim",
        )
    )


def run() -> None:
    """Start the interactive EliteAgent session."""
    print_banner()

    stm = ShortTermMemory()
    ltm = LongTermMemory()
    kb = KnowledgeBase()

    console.print("[dim]Agent grafini qurilmoqda…[/dim]")
    agent_graph = build_agent_graph()
    console.print(f"[bold green]✅ {settings.agent_name} tayyor![/bold green]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold blue]Siz[/bold blue]").strip()
        except KeyboardInterrupt:
            console.print("\n[yellow]Dastur to'xtatildi.[/yellow]")
            break

        if not user_input:
            continue

        # ----------------------------------------------------------------
        # Special commands
        # ----------------------------------------------------------------
        if user_input.startswith("/exit"):
            console.print("[yellow]Xayr! 👋[/yellow]")
            break

        if user_input.startswith("/clear"):
            stm.clear()
            console.print("[green]Suhbat tarixi tozalandi.[/green]")
            continue

        if user_input.startswith("/ingest "):
            path = user_input[len("/ingest "):].strip()
            try:
                with console.status(f"[cyan]'{path}' yuklanmoqda…[/cyan]"):
                    p = Path(path)
                    if p.exists() and p.is_dir():
                        results = kb.ingest_directory(path)
                        total = sum(v for v in results.values() if v > 0)
                        console.print(
                            f"[green]✅ {len(results)} fayl, jami {total} bo'lak indekslandi.[/green]"
                        )
                    else:
                        count = kb.ingest_file(path)
                        console.print(f"[green]✅ '{path}' — {count} bo'lak indekslandi.[/green]")
            except Exception as exc:  # noqa: BLE001
                console.print(f"[red]Xato: {exc}[/red]")
            continue

        if user_input.startswith("/remember "):
            content = user_input[len("/remember "):].strip()
            try:
                mem_id = ltm.store_memory(content)
                console.print(f"[green]✅ Xotiraga saqlandi (ID: {mem_id[:8]}…)[/green]")
            except Exception as exc:  # noqa: BLE001
                console.print(f"[red]Xato: {exc}[/red]")
            continue

        if user_input.startswith("/recall "):
            query = user_input[len("/recall "):].strip()
            try:
                result = ltm.recall_as_text(query)
                console.print(
                    Panel(
                        result or "Hech narsa topilmadi.",
                        title="[bold]Uzoq muddatli xotira[/bold]",
                        border_style="magenta",
                    )
                )
            except Exception as exc:  # noqa: BLE001
                console.print(f"[red]Xato: {exc}[/red]")
            continue

        # ----------------------------------------------------------------
        # Normal chat message
        # ----------------------------------------------------------------
        stm.add_user_message(user_input)

        try:
            with console.status("[cyan]Fikrlanmoqda…[/cyan]"):
                result = agent_graph.invoke(
                    {
                        "messages": stm.get_messages(),
                        "long_term_context": "",
                        "knowledge_context": "",
                    },
                    config={"recursion_limit": settings.agent_max_iterations * 2},
                )

            ai_messages = result.get("messages", [])
            last_ai = None
            for msg in reversed(ai_messages):
                if hasattr(msg, "type") and msg.type == "ai":
                    last_ai = msg
                    break

            if last_ai is not None:
                answer = (
                    last_ai.content
                    if isinstance(last_ai.content, str)
                    else str(last_ai.content)
                )
                stm.add_ai_message(answer)
                console.print(
                    Panel(
                        answer,
                        title=f"[bold green]{settings.agent_name}[/bold green]",
                        border_style="green",
                    )
                )
            else:
                console.print("[yellow]Agent javob bermadi.[/yellow]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Jarayon to'xtatildi.[/yellow]")
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]Agent xatosi: {exc}[/red]")


if __name__ == "__main__":
    run()

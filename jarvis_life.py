"""
JARVIS Life Assistant — Kundalik hayot boshqaruvchisi.
Real vaqtda dars monitoring, homework tracking, kundalik rejalashtirish.
"""

import json
import sys
import time
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown
except ImportError:
    print("Rich kutubxonasi topilmadi. O'rnating: pip install rich")
    sys.exit(1)

from life import SmartScheduler, HomeworkManager, DailyPlanner, ReminderEngine

console = Console()

_BANNER = """
     _   _   ____    _____  __     __ ___   ____         _      _   _____  _____
    | | / \ |  _ \  |_   _| \ \   / /|_ _| / ___|       | |    | | |  ___|| ____|
 _  | |/ _ \| |_) |   | |    \ \ / /  | |  \___ \       | |    | | | |_   |  _|
| |_| / ___ \  _ <    | |     \ V /   | |   ___) |      | |___ | | |  _|  | |___
 \___/_/   \_\_| \_\  |_|      \_/   |___| |____/       |_____||_| |_|    |_____|

                    Smart Life Assistant — Hayot yordamchisi
"""


def print_banner() -> None:
    """JARVIS Life Assistant banner."""
    console.print(f"[bold cyan]{_BANNER}[/bold cyan]")
    console.print(
        "[dim]Kundalik dars jadvali, uy vazifalari va rejalashtirish tizimi[/dim]\n"
    )


def show_schedule(scheduler: SmartScheduler, day: str | None = None) -> None:
    """Jadvalini chiroyli jadval ko'rinishida ko'rsatish."""
    classes = scheduler.get_schedule(day)
    title = f"📅 {day.capitalize() if day else 'Bugungi'} Dars Jadvali"
    if not classes:
        console.print(Panel("[yellow]Dars topilmadi.[/yellow]", title=title))
        return
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Boshlanish", style="cyan", no_wrap=True)
    table.add_column("Tugash", style="cyan", no_wrap=True)
    table.add_column("Fan", style="bold")
    table.add_column("Xona")
    table.add_column("O'qituvchi")
    table.add_column("ID", style="dim", no_wrap=True)
    for c in classes:
        table.add_row(c.start_time, c.end_time, c.name, c.location, c.teacher, c.id[:8])
    console.print(table)


def show_weekly_schedule(scheduler: SmartScheduler) -> None:
    """Haftalik jadval."""
    weekly = scheduler.get_weekly_schedule()
    table = Table(title="📆 Haftalik Dars Jadvali", show_header=True, header_style="bold magenta")
    table.add_column("Kun", style="bold")
    table.add_column("Darslar")
    day_names_uz = {
        "monday": "Dushanba",
        "tuesday": "Seshanba",
        "wednesday": "Chorshanba",
        "thursday": "Payshanba",
        "friday": "Juma",
        "saturday": "Shanba",
        "sunday": "Yakshanba",
    }
    for day, classes in weekly.items():
        if classes:
            class_str = "\n".join(
                f"{c.start_time}-{c.end_time}: {c.name}" for c in classes
            )
        else:
            class_str = "[dim]Dars yo'q[/dim]"
        table.add_row(day_names_uz.get(day, day), class_str)
    console.print(table)


def show_homework(homework_mgr: HomeworkManager) -> None:
    """Bajarilmagan uy vazifalari."""
    pending = homework_mgr.get_pending_homework()
    if not pending:
        console.print(Panel("[green]✅ Barcha uy vazifalari bajarilgan![/green]", title="📝 Uy Vazifalari"))
        return
    table = Table(title="📝 Bajarilmagan Uy Vazifalari", show_header=True, header_style="bold yellow")
    table.add_column("Fan", style="bold")
    table.add_column("Vazifa")
    table.add_column("Muddat", style="cyan")
    table.add_column("Ustuvorlik", style="magenta")
    table.add_column("ID", style="dim", no_wrap=True)
    for hw in pending:
        table.add_row(hw.subject, hw.description, hw.deadline or "-", hw.priority.value, hw.id[:8])
    console.print(table)


def show_tasks(homework_mgr: HomeworkManager) -> None:
    """Barcha vazifalar."""
    all_pending = homework_mgr.get_all_pending()
    if not all_pending:
        console.print(Panel("[green]✅ Barcha vazifalar bajarilgan![/green]", title="✅ Vazifalar"))
        return
    table = Table(title="📋 Barcha Bajarilmagan Vazifalar", show_header=True, header_style="bold blue")
    table.add_column("Turi", style="cyan")
    table.add_column("Sarlavha/Fan", style="bold")
    table.add_column("Tavsif")
    table.add_column("Ustuvorlik", style="magenta")
    table.add_column("ID", style="dim", no_wrap=True)
    for entry in all_pending:
        item = entry["item"]
        if entry["type"] == "homework":
            title_col = item.subject
            desc_col = item.description
        else:
            title_col = item.title
            desc_col = item.description
        table.add_row(entry["type"], title_col, desc_col, item.priority.value, item.id[:8])
    console.print(table)


def show_stats(homework_mgr: HomeworkManager) -> None:
    """Statistika."""
    stats = homework_mgr.get_stats()
    lines = [
        f"📚 Jami uy vazifalari: {stats['total_homework']}",
        f"✅ Bajarilgan: {stats['completed_homework']}",
        f"⏳ Qolgan: {stats['pending_homework']}",
        f"⚠️  Muddati o'tgan: {stats['overdue_homework']}",
        "",
        f"📋 Jami vazifalar: {stats['total_tasks']}",
        f"✅ Bajarilgan: {stats['completed_tasks']}",
        "",
        f"📈 Bajarilish darajasi: {stats['completion_rate']}%",
    ]
    console.print(Panel("\n".join(lines), title="📊 Statistika"))


def show_help() -> None:
    """Yordam matnini ko'rsatish."""
    help_text = """
## JARVIS Life Assistant — Buyruqlar

### Jadval
- `/schedule` — bugungi jadval
- `/week` — haftalik jadval
- `/add_class <fan> <kun> <boshlanish> <tugash> [xona]` — dars qo'shish
- `/remove_class <id>` — dars o'chirish

### Uy Vazifalari
- `/homework` — bajarilmagan uy vazifalari
- `/add_hw <fan> <tavsif> [muddat]` — uy vazifasi qo'shish
- `/done_hw <id>` — uy vazifasini bajarilgan qilish

### Vazifalar
- `/tasks` — barcha vazifalar
- `/add_task <sarlavha> [tavsif] [muddat]` — vazifa qo'shish
- `/done_task <id>` — vazifani bajarilgan qilish

### Reja va Eslatmalar
- `/plan` — bugungi reja
- `/reminders` — eslatmalar
- `/stats` — statistika
- `/summary` — kun oxiri xulosasi

### Boshqa
- `/load_sample` — namuna jadval yuklash
- `/help` — yordam
- `/exit` — chiqish
"""
    console.print(Markdown(help_text))


def load_sample_schedule(scheduler: SmartScheduler) -> None:
    """config/schedule_config.json dan namuna jadval yuklash."""
    try:
        with open("config/schedule_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        sample = config.get("sample_schedule", [])
        for item in sample:
            scheduler.add_class(
                name=item["name"],
                day=item["day"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                location=item.get("location", ""),
                teacher=item.get("teacher", ""),
            )
        console.print(f"[green]✅ {len(sample)} ta namuna dars yuklandi.[/green]")
    except FileNotFoundError:
        console.print("[red]config/schedule_config.json topilmadi.[/red]")
    except Exception as exc:
        console.print(f"[red]Xato: {exc}[/red]")


def main() -> None:
    """Asosiy tsikl."""
    print_banner()

    scheduler = SmartScheduler()
    homework_mgr = HomeworkManager()
    planner = DailyPlanner()
    reminder_engine = ReminderEngine()

    # Ertalabki xulosa
    console.print(Panel(planner.get_morning_briefing(), title="🌅 Ertalabki Xulosa"))

    # Eslatmalarni tekshirish
    reminders = reminder_engine.check_all()
    if reminders:
        console.print(
            Panel(reminder_engine.format_notifications(reminders), title="🔔 Eslatmalar")
        )

    console.print("\n[dim]Yordam uchun /help yozing.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]🧑 Siz:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Xayr! Yaxshi kun tilaymiz! 👋[/yellow]")
            break

        if not user_input:
            continue

        parts = user_input.split()
        cmd = parts[0].lower()

        if cmd == "/exit":
            console.print("[yellow]Xayr! Yaxshi kun tilaymiz! 👋[/yellow]")
            break

        elif cmd == "/help":
            show_help()

        elif cmd == "/schedule":
            day_arg = parts[1] if len(parts) > 1 else None
            show_schedule(scheduler, day_arg)

        elif cmd == "/week":
            show_weekly_schedule(scheduler)

        elif cmd == "/add_class":
            # /add_class <fan> <kun> <boshlanish> <tugash> [xona] [oqituvchi]
            if len(parts) < 5:
                console.print("[red]Foydalanish: /add_class <fan> <kun> <boshlanish> <tugash> [xona][/red]")
            else:
                name, day, start, end_ = parts[1], parts[2], parts[3], parts[4]
                location = parts[5] if len(parts) > 5 else ""
                teacher = parts[6] if len(parts) > 6 else ""
                try:
                    cls = scheduler.add_class(name, day, start, end_, location, teacher)
                    console.print(f"[green]✅ Dars qo'shildi: {cls.name} ({cls.id[:8]})[/green]")
                except Exception as e:
                    console.print(f"[red]Xato: {e}[/red]")

        elif cmd == "/remove_class":
            if len(parts) < 2:
                console.print("[red]Foydalanish: /remove_class <id>[/red]")
            else:
                found = scheduler.find_class_by_prefix(parts[1])
                if found:
                    result = scheduler.remove_class(found.id)
                    if result:
                        console.print(f"[green]✅ Dars o'chirildi.[/green]")
                    else:
                        console.print("[red]Dars topilmadi.[/red]")
                else:
                    console.print("[red]Dars topilmadi.[/red]")

        elif cmd == "/homework":
            show_homework(homework_mgr)

        elif cmd == "/add_hw":
            # /add_hw <fan> <tavsif> [muddat] [ustuvorlik]
            if len(parts) < 3:
                console.print("[red]Foydalanish: /add_hw <fan> <tavsif> [muddat] [ustuvorlik][/red]")
            else:
                subject = parts[1]
                description = parts[2]
                deadline = parts[3] if len(parts) > 3 else ""
                priority = parts[4] if len(parts) > 4 else "medium"
                try:
                    hw = homework_mgr.add_homework(subject, description, deadline, priority)
                    console.print(f"[green]✅ Uy vazifasi qo'shildi: {hw.subject} ({hw.id[:8]})[/green]")
                except Exception as e:
                    console.print(f"[red]Xato: {e}[/red]")

        elif cmd == "/done_hw":
            if len(parts) < 2:
                console.print("[red]Foydalanish: /done_hw <id>[/red]")
            else:
                found = homework_mgr.find_homework_by_prefix(parts[1])
                if found:
                    result = homework_mgr.complete_homework(found.id)
                    console.print("[green]✅ Bajarilgan deb belgilandi![/green]" if result else "[red]Topilmadi.[/red]")
                else:
                    console.print("[red]Vazifa topilmadi.[/red]")

        elif cmd == "/tasks":
            show_tasks(homework_mgr)

        elif cmd == "/add_task":
            # /add_task <sarlavha> [tavsif] [muddat] [ustuvorlik] [kategoriya]
            if len(parts) < 2:
                console.print("[red]Foydalanish: /add_task <sarlavha> [tavsif] [muddat][/red]")
            else:
                title = parts[1]
                description = parts[2] if len(parts) > 2 else ""
                deadline = parts[3] if len(parts) > 3 else ""
                priority = parts[4] if len(parts) > 4 else "medium"
                category = parts[5] if len(parts) > 5 else "general"
                try:
                    task = homework_mgr.add_task(title, description, deadline, priority, category)
                    console.print(f"[green]✅ Vazifa qo'shildi: {task.title} ({task.id[:8]})[/green]")
                except Exception as e:
                    console.print(f"[red]Xato: {e}[/red]")

        elif cmd == "/done_task":
            if len(parts) < 2:
                console.print("[red]Foydalanish: /done_task <id>[/red]")
            else:
                found = homework_mgr.find_task_by_prefix(parts[1])
                if found:
                    result = homework_mgr.complete_task(found.id)
                    console.print("[green]✅ Bajarilgan deb belgilandi![/green]" if result else "[red]Topilmadi.[/red]")
                else:
                    console.print("[red]Vazifa topilmadi.[/red]")

        elif cmd == "/plan":
            plan = planner.generate_daily_plan()
            lines = [f"📅 Sana: {plan.date}", f"⏰ Uyg'onish: {plan.wake_up_time}", ""]
            if plan.classes:
                lines.append(f"🏫 Darslar ({len(plan.classes)} ta):")
                for c in plan.classes:
                    lines.append(f"  {c.get('start_time', '')}-{c.get('end_time', '')} — {c.get('name', '')}")
            if plan.study_blocks:
                lines.append(f"\n📖 O'qish vaqtlari ({len(plan.study_blocks)} ta):")
                for sb in plan.study_blocks:
                    lines.append(f"  {sb['start']}-{sb['end']}: {sb.get('suggestion', '')}")
            if plan.tasks:
                lines.append(f"\n📝 Bugungi vazifalar ({len(plan.tasks)} ta):")
                for t in plan.tasks:
                    lines.append(f"  - {t.get('subject', t.get('title', ''))}")
            console.print(Panel("\n".join(lines), title="📋 Bugungi Reja"))

        elif cmd == "/reminders":
            reminders = reminder_engine.check_all()
            text = reminder_engine.format_notifications(reminders)
            console.print(Panel(text, title="🔔 Eslatmalar"))

        elif cmd == "/stats":
            show_stats(homework_mgr)

        elif cmd == "/summary":
            summary = planner.get_end_of_day_summary()
            console.print(Panel(summary, title="📊 Kun Oxiri Xulosasi"))

        elif cmd == "/load_sample":
            load_sample_schedule(scheduler)

        else:
            console.print(
                f"[yellow]Noma'lum buyruq: {cmd}. Yordam uchun /help yozing.[/yellow]"
            )


if __name__ == "__main__":
    main()

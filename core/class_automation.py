"""
JARVIS Class Automation.
Dars boshlanishidan oldin eslatma, dars tugagandan keyin homework so'rash.
"""
from __future__ import annotations

from datetime import datetime

_POST_CLASS_WINDOW_MINUTES = 5  # Window after class ends to prompt for homework


class ClassAutomation:
    """Dars avtomatlashtirish tizimi."""

    def __init__(self) -> None:
        self._reminded_classes: set[str] = set()  # Bugun eslatilgan darslar
        self._ended_classes: set[str] = set()  # Bugun tugagan darslar

    def check_pre_class_reminder(
        self, events: list, minutes_before: int = 15
    ) -> list[str]:
        """
        Dars boshlanishidan ``minutes_before`` daqiqa oldin eslatma.

        Returns:
            list of reminder messages
        """
        now = datetime.now()
        current_minutes = now.hour * 60 + now.minute
        reminders: list[str] = []

        for event in events:
            if event.id in self._reminded_classes:
                continue
            try:
                eh, em = map(int, event.time.split(":"))
                event_minutes = eh * 60 + em
                diff = event_minutes - current_minutes
                if 0 < diff <= minutes_before:
                    self._reminded_classes.add(event.id)
                    reminders.append(
                        f"🔔 {diff} daqiqadan keyin: {event.title} ({event.time})"
                    )
            except (ValueError, AttributeError):
                continue
        return reminders

    def check_post_class_homework(self, events: list) -> list[str]:
        """
        Dars tugagandan keyin: 'Uyga vazifa bormi?' deb so'rash.

        Returns:
            list of homework prompts
        """
        now = datetime.now()
        current_minutes = now.hour * 60 + now.minute
        prompts: list[str] = []

        for event in events:
            if event.id in self._ended_classes:
                continue
            if not event.end_time:
                continue
            try:
                eh, em = map(int, event.end_time.split(":"))
                end_minutes = eh * 60 + em
                # Dars tugagan bo'lsa (0-_POST_CLASS_WINDOW_MINUTES daqiqa ichida)
                diff = current_minutes - end_minutes
                if 0 <= diff <= _POST_CLASS_WINDOW_MINUTES:
                    self._ended_classes.add(event.id)
                    prompts.append(
                        f"📚 {event.title} darsi tugadi. Uyga vazifa bormi?"
                    )
            except (ValueError, AttributeError):
                continue
        return prompts

    def reset_daily(self) -> None:
        """Kunlik holatni tozalash (yangi kun boshida)."""
        self._reminded_classes.clear()
        self._ended_classes.clear()

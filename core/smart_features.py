"""
SmartFeatures — Aqlli funksiyalar: duplicate detection, conflict detection,
auto reschedule va missed task tekshiruvi.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any


def _parse_time(time_str: str) -> datetime | None:
    """HH:MM formatdagi vaqtni datetime ga o'girish."""
    try:
        return datetime.strptime(time_str, "%H:%M")
    except (ValueError, TypeError):
        return None


class SmartFeatures:
    """Aqlli funksiyalar: duplicate detection, conflict detection, auto reschedule."""

    # ------------------------------------------------------------------
    # Duplicate detection
    # ------------------------------------------------------------------

    def check_duplicate(
        self,
        new_task: dict[str, Any],
        existing_tasks: list[dict[str, Any]],
    ) -> bool:
        """Bir xil vazifa ikki marta qo'shilmasligi uchun tekshirish.

        Args:
            new_task: ``{"title": str, ...}`` ko'rinishidagi yangi vazifa.
            existing_tasks: Mavjud vazifalar ro'yxati.

        Returns:
            ``True`` — agar duplikat topilsa, ``False`` — topilmasa.
        """
        new_title = (new_task.get("title") or "").lower().strip()
        if not new_title:
            return False

        for task in existing_tasks:
            existing_title = (task.get("title") or "").lower().strip()
            # To'liq mos yoki birining ichida boshqasi
            if existing_title and (
                new_title == existing_title
                or new_title in existing_title
                or existing_title in new_title
            ):
                return True
        return False

    # ------------------------------------------------------------------
    # Conflict detection
    # ------------------------------------------------------------------

    def check_conflict(
        self,
        new_time: str,
        existing_schedule: list[dict[str, Any]],
        duration_minutes: int = 60,
    ) -> list[dict[str, Any]]:
        """Vaqt to'qnashuvini aniqlash.

        Args:
            new_time: ``"HH:MM"`` formatdagi yangi vazifa vaqti.
            existing_schedule: Har bir yozuv ``{"start_time": str, "end_time": str, "title": str}``
                shaklida bo'lishi kerak.
            duration_minutes: Yangi vazifa davomiyligi (daqiqada), default 60.

        Returns:
            To'qnashadigan yozuvlar ro'yxati.
        """
        new_start = _parse_time(new_time)
        if new_start is None:
            return []

        new_end = new_start + timedelta(minutes=duration_minutes)
        conflicts: list[dict[str, Any]] = []

        for entry in existing_schedule:
            entry_start = _parse_time(entry.get("start_time", ""))
            entry_end = _parse_time(entry.get("end_time", ""))

            if entry_start is None:
                continue

            # end_time yo'q bo'lsa 1 soat deb hisoblaymiz
            if entry_end is None:
                entry_end = entry_start + timedelta(hours=1)

            # Oraliqlar kesishadimi?
            if new_start < entry_end and new_end > entry_start:
                conflicts.append(entry)

        return conflicts

    # ------------------------------------------------------------------
    # Auto reschedule suggestion
    # ------------------------------------------------------------------

    def suggest_reschedule(
        self,
        conflict_time: str,
        schedule: list[dict[str, Any]],
        duration_minutes: int = 60,
        search_window_hours: int = 4,
    ) -> str:
        """To'qnashuv bo'lsa yangi vaqt taklif qilish.

        Args:
            conflict_time: To'qnashuv bo'lgan ``"HH:MM"`` vaqt.
            schedule: Mavjud jadval (``check_conflict`` ga berilgan formatda).
            duration_minutes: Vazifa davomiyligi (daqiqada).
            search_window_hours: Qidirish oynasi (soat).

        Returns:
            Tavsiya etilgan vaqt ``"HH:MM"`` formatida, yoki "topilmadi" xabari.
        """
        base_time = _parse_time(conflict_time)
        if base_time is None:
            return "Vaqt formati noto'g'ri (HH:MM kerak)"

        candidate = base_time + timedelta(minutes=duration_minutes)
        end_window = base_time + timedelta(hours=search_window_hours)

        while candidate < end_window:
            candidate_str = candidate.strftime("%H:%M")
            if not self.check_conflict(candidate_str, schedule, duration_minutes):
                return candidate_str
            candidate += timedelta(minutes=15)

        return "Mos vaqt topilmadi (jadval to'liq)"

    # ------------------------------------------------------------------
    # Missed tasks
    # ------------------------------------------------------------------

    def check_missed_tasks(
        self,
        tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Kecha bajarilmagan vazifalarni topish.

        Args:
            tasks: Har bir yozuv ``{"deadline": str, "completed": bool, "title": str}``
                shaklida bo'lishi kerak.  ``deadline`` — ``"YYYY-MM-DD"`` yoki ``"YYYY-MM-DD HH:MM"``.

        Returns:
            Bajarilmagan va muddati o'tgan vazifalar ro'yxati.
        """
        today = datetime.now().date()
        missed: list[dict[str, Any]] = []

        for task in tasks:
            if task.get("completed"):
                continue

            deadline_raw = task.get("deadline") or ""
            if not deadline_raw:
                continue

            # deadline ni parse qilish
            deadline_date = None
            for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    deadline_date = datetime.strptime(deadline_raw, fmt).date()
                    break
                except ValueError:
                    continue

            if deadline_date is not None and deadline_date < today:
                missed.append(task)

        return missed

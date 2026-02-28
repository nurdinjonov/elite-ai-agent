"""
IntentParser — Foydalanuvchi kiritishini tabiiy tilda tahlil qilish.
O'zbek va ingliz tillarida slash buyruqlar ham qo'llab-quvvatlanadi.
"""

from __future__ import annotations

import re
from typing import Any

# Kun nomlari: o'zbek va ingliz
_DAY_MAP: dict[str, str] = {
    "dushanba": "monday",
    "monday": "monday",
    "seshanba": "tuesday",
    "tuesday": "tuesday",
    "chorshanba": "wednesday",
    "wednesday": "wednesday",
    "payshanba": "thursday",
    "thursday": "thursday",
    "juma": "friday",
    "friday": "friday",
    "shanba": "saturday",
    "saturday": "saturday",
    "yakshanba": "sunday",
    "sunday": "sunday",
    "bugun": "today",
    "today": "today",
    "ertaga": "tomorrow",
    "tomorrow": "tomorrow",
}

# Intent kalit so'zlari (past tartib — aniqroq pattern'lar avval)
_INTENT_PATTERNS: list[tuple[str, list[str]]] = [
    ("exit",           ["chiqish", "exit", "quit", "xayr", "bye"]),
    ("show_help",      ["yordam", "help", "nima qila olasan", "buyruqlar"]),
    ("show_status",    ["statusni ko'rsat", "holat", "status", "/status"]),
    # show_reflect avval — "haftalik tahlil" show_week dan oldin kelishi kerak
    ("show_reflect",   ["haftalik tahlil", "haftalik aks", "reflect", "/reflect"]),
    ("show_week",      ["haftalik jadval", "hafta jadvali", "hafta", "/week"]),
    ("show_schedule",  ["bugungi darslar", "jadval", "schedule", "darslar", "/schedule"]),
    ("add_class",      ["dars qo'sh", "yangi dars", "/add_class"]),
    ("show_homework",  ["uy vazifalari", "vazifalar", "homework", "/homework"]),
    ("add_homework",   ["vazifa qo'sh", "yangi vazifa", "/add_hw"]),
    ("done_homework",  ["vazifa bajarildi", "bajarildi", "tugadi", "/done_hw"]),
    ("show_tasks",     ["vazifalarim", "tasks", "/tasks"]),
    ("add_task",       ["uchrashuv qo'sh", "reja qo'sh", "uchrashuv", "qo'sh", "/add_task"]),
    ("done_task",      ["done_task", "/done_task"]),
    ("show_plan",      ["bugungi reja", "plan", "/plan"]),
    ("show_today",     ["bugun nima bor", "bugungi sharh", "bugun", "/today"]),
    ("show_stats",     ["statistika", "stats", "/stats"]),
    ("show_reminders", ["eslatmalar", "reminders", "/reminders"]),
    ("start_focus",    ["focus boshlash", "pomodoro", "diqqat", "focus start", "/focus"]),
    ("stop_focus",     ["focus to'xtat", "focus stop", "stop focus"]),
    ("change_mode",    ["rejimni o'zgartir", "fast rejim", "code rejim", "pro rejim", "/fast", "/code", "/pro"]),
    ("show_cognitive", ["kognitiv yuk", "cognitive", "/cognitive"]),
]

# Vaqt pattern'i: HH:MM
_TIME_RE = re.compile(r"\b(\d{1,2}:\d{2})\b")


class IntentParser:
    """Foydalanuvchi kiritishini tabiiy tilda tahlil qilish."""

    def parse(self, text: str) -> dict[str, Any]:
        """Matnni tahlil qilib intent va parametrlarini qaytarish.

        Args:
            text: Foydalanuvchi kiritgan matn.

        Returns:
            ``{"intent": str, "params": dict}`` ko'rinishidagi lug'at.
            Agar intent aniqlanmasa ``"chat"`` qaytariladi.
        """
        lower = text.lower().strip()

        # Avval slash buyruqlarni tekshirish (backward compatibility)
        slash_intent = self._check_slash(lower)
        if slash_intent:
            return {"intent": slash_intent, "params": self._extract_params(text, slash_intent)}

        # Tabiiy til intent'larini tekshirish
        for intent, keywords in _INTENT_PATTERNS:
            for kw in keywords:
                if kw in lower:
                    return {"intent": intent, "params": self._extract_params(text, intent)}

        # Intent topilmadi — AI ga yuborish
        return {"intent": "chat", "params": {}}

    # ------------------------------------------------------------------
    # Ichki yordamchi metodlar
    # ------------------------------------------------------------------

    def _check_slash(self, lower: str) -> str | None:
        """Slash buyruqlarni intent'ga moslashtirish."""
        slash_map: dict[str, str] = {
            "/exit": "exit",
            "/quit": "exit",
            "/help": "show_help",
            "/status": "show_status",
            "/week": "show_week",
            "/schedule": "show_schedule",
            "/add_class": "add_class",
            "/homework": "show_homework",
            "/add_hw": "add_homework",
            "/done_hw": "done_homework",
            "/tasks": "show_tasks",
            "/add_task": "add_task",
            "/done_task": "done_task",
            "/plan": "show_plan",
            "/today": "show_today",
            "/stats": "show_stats",
            "/reminders": "show_reminders",
            "/focus": "start_focus",
            "/cognitive": "show_cognitive",
            "/reflect": "show_reflect",
            "/fast": "change_mode",
            "/code": "change_mode",
            "/pro": "change_mode",
        }
        first_token = lower.split()[0] if lower.split() else ""
        return slash_map.get(first_token)

    def _extract_params(self, text: str, intent: str) -> dict[str, Any]:
        """Parametrlarni (kun, vaqt, sarlavha) ajratib olish."""
        params: dict[str, Any] = {}
        lower = text.lower()

        # Kun
        for uz_en, canonical in _DAY_MAP.items():
            if uz_en in lower:
                params["day"] = canonical
                break

        # Vaqt
        time_match = _TIME_RE.search(text)
        if time_match:
            params["time"] = time_match.group(1)

        # Rejim (change_mode uchun)
        if intent == "change_mode":
            for m in ("fast", "code", "pro"):
                if m in lower:
                    params["mode"] = m
                    break

        # Focus daqiqasi
        if intent == "start_focus":
            min_match = re.search(r"\b(\d+)\s*(?:daqiqa|min(?:utes?)?)\b", lower)
            if min_match:
                params["minutes"] = int(min_match.group(1))
            # "/focus stop" ni stop_focus ga yo'naltirish
            if "stop" in lower or "to'xtat" in lower:
                params["stop"] = True

        # Sarlavha — vaqt va kun so'zlarini olib tashlash
        if intent in ("add_task", "add_class", "add_homework"):
            title = text
            # Kun nomlarini o'chirish
            for uz_en in _DAY_MAP:
                title = re.sub(rf"\b{re.escape(uz_en)}\b", "", title, flags=re.IGNORECASE)
            # Vaqtni o'chirish
            title = _TIME_RE.sub("", title)
            # Slash buyruqlarni o'chirish
            title = re.sub(r"^/\w+\s*", "", title).strip()
            # Kalit so'zlarni o'chirish
            for kw in ["dars qo'sh", "yangi dars", "qo'sh", "add", "vazifa", "uchrashuv", "reja"]:
                title = re.sub(rf"\b{re.escape(kw)}\b", "", title, flags=re.IGNORECASE)
            title = title.strip(" ,.")
            if title:
                params["title"] = title

        return params

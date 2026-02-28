"""
TelegramNotifier — Telegram orqali bildirishnomalar yuborish.
Bot token va chat ID .env faylidan o'qiladi.
"""

from __future__ import annotations

import os
from typing import Any


class TelegramNotifier:
    """Telegram orqali bildirishnomalar."""

    def __init__(self) -> None:
        self.bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled: bool = bool(self.bot_token and self.chat_id)

    # ------------------------------------------------------------------
    # Asosiy yuborish metodlari
    # ------------------------------------------------------------------

    async def send_message(self, text: str) -> bool:
        """Telegram ga oddiy xabar yuborish.

        Args:
            text: Yuborilajak matn.

        Returns:
            ``True`` — muvaffaqiyatli, ``False`` — xato yoki o'chirilgan.
        """
        if not self.enabled:
            return False

        try:
            import aiohttp

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload: dict[str, Any] = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    return resp.status == 200
        except Exception:
            return False

    async def send_reminder(self, task_title: str, time: str) -> bool:
        """Vazifa eslatmasini yuborish.

        Args:
            task_title: Vazifa sarlavhasi.
            time: Eslatma vaqti (``"HH:MM"`` formatida).

        Returns:
            ``True`` — muvaffaqiyatli, ``False`` — xato yoki o'chirilgan.
        """
        text = f"🔔 Eslatma [{time}]\n<b>{task_title}</b>"
        return await self.send_message(text)

    async def send_daily_summary(self, summary: str) -> bool:
        """Kunlik xulosa yuborish.

        Args:
            summary: Kunlik xulosa matni.

        Returns:
            ``True`` — muvaffaqiyatli, ``False`` — xato yoki o'chirilgan.
        """
        text = f"📊 Kunlik Xulosa\n\n{summary}"
        return await self.send_message(text)

import os
from pathlib import Path

from langchain_core.tools import tool


@tool
def read_file_tool(file_path: str) -> str:
    """Faylni o'qish. Fayllarni ko'rish, tahlil qilish uchun ishlatiladi."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Fayl topilmadi: {file_path}"
        if path.stat().st_size > 1_000_000:
            return "Xato: Fayl hajmi 1MB dan katta."
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Fayl o'qish xatosi: {e}"


@tool
def write_file_tool(file_path: str, content: str) -> str:
    """Faylga yozish. Yangi fayl yaratish yoki mavjudini yangilash uchun."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Muvaffaqiyatli yozildi: {file_path}"
    except Exception as e:
        return f"Fayl yozish xatosi: {e}"


@tool
def list_directory_tool(directory_path: str = ".") -> str:
    """Katalog tarkibini ko'rsatish."""
    try:
        path = Path(directory_path)
        if not path.exists():
            return f"Katalog topilmadi: {directory_path}"
        items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        lines = []
        for item in items:
            icon = "\U0001f4c2" if item.is_dir() else "\U0001f4c4"
            lines.append(f"{icon} {item.name}")
        return "\n".join(lines) if lines else "Katalog bo'sh."
    except Exception as e:
        return f"Katalog ko'rish xatosi: {e}"
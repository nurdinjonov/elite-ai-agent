"""File management tools: read, write and list directory contents."""

import os
from pathlib import Path

from langchain_core.tools import tool

_MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB


@tool
def read_file_tool(file_path: str) -> str:
    """Read the contents of a file.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        The file's text content, or an error message if reading fails.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Xato: Fayl topilmadi — '{file_path}'"
        if not path.is_file():
            return f"Xato: '{file_path}' fayl emas."
        size = path.stat().st_size
        if size > _MAX_FILE_SIZE:
            return f"Xato: Fayl hajmi {size} bayt — 1 MB chegarasidan katta."
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        return f"Fayl o'qish xatosi: {exc}"


@tool
def write_file_tool(file_path: str, content: str) -> str:
    """Write content to a file, creating parent directories as needed.

    Args:
        file_path: Absolute or relative path to the target file.
        content: Text content to write.

    Returns:
        A success or error message.
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"✅ '{file_path}' fayliga muvaffaqiyatli yozildi ({len(content)} belgi)."
    except Exception as exc:  # noqa: BLE001
        return f"Fayl yozish xatosi: {exc}"


@tool
def list_directory_tool(directory_path: str = ".") -> str:
    """List the contents of a directory.

    Args:
        directory_path: Path to the directory (defaults to current directory).

    Returns:
        A formatted directory listing with 📂/📄 icons, or an error message.
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return f"Xato: Katalog topilmadi — '{directory_path}'"
        if not path.is_dir():
            return f"Xato: '{directory_path}' katalog emas."

        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        if not entries:
            return f"'{directory_path}' katalogi bo'sh."

        lines: list[str] = [f"📁 {directory_path}/"]
        for entry in entries:
            icon = "📄" if entry.is_file() else "📂"
            size = ""
            if entry.is_file():
                size = f"  ({entry.stat().st_size} bayt)"
            lines.append(f"  {icon} {entry.name}{size}")
        return "\n".join(lines)
    except Exception as exc:  # noqa: BLE001
        return f"Katalog ro'yxati xatosi: {exc}"

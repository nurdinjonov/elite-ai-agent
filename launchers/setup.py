"""JARVIS-X auto setup script.

Installs all required Python dependencies and creates a .env file from
.env.example when one does not already exist.  Run this once after
cloning the repository.

Usage::

    python launchers/setup.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys


def _run(cmd: list[str]) -> None:
    """Run a subprocess command and exit on failure.

    Args:
        cmd: Command and arguments list.
    """
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"[ERROR] Buyruq muvaffaqiyatsiz tugadi: {' '.join(cmd)}")
        sys.exit(result.returncode)


def _project_root() -> str:
    """Return the absolute path to the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def install_dependencies(root: str) -> None:
    """Install Python packages from requirements.txt.

    Args:
        root: Project root directory path.
    """
    req_file = os.path.join(root, "requirements.txt")
    if not os.path.isfile(req_file):
        print("[WARN] requirements.txt topilmadi — o'tkazib yuborildi.")
        return

    print("\n📦 Paketlar o'rnatilmoqda...")
    _run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    _run([sys.executable, "-m", "pip", "install", "-r", req_file])
    print("✓ Barcha paketlar o'rnatildi.")


def create_env_file(root: str) -> None:
    """Copy .env.example to .env if .env does not already exist.

    Args:
        root: Project root directory path.
    """
    env_path = os.path.join(root, ".env")
    example_path = os.path.join(root, ".env.example")

    if os.path.isfile(env_path):
        print("\n✓ .env fayli allaqachon mavjud — o'tkazib yuborildi.")
        return

    if not os.path.isfile(example_path):
        print("\n[WARN] .env.example topilmadi — .env yaratilmadi.")
        return

    shutil.copy(example_path, env_path)
    print(f"\n✓ .env fayli yaratildi: {env_path}")
    print("  ⚠  API kalitlarni .env fayliga qo'shing!")


def main() -> None:
    """Run the full setup sequence."""
    root = _project_root()
    print(f"\n🚀 JARVIS-X Setup — {root}\n")

    create_env_file(root)
    install_dependencies(root)

    print("\n✅ Setup muvaffaqiyatli tugadi!")
    print("   Boshlash uchun: python jarvis_main.py\n")


if __name__ == "__main__":
    main()

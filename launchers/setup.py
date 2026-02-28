"""JARVIS-X Auto Setup Script — Birinchi marta ishga tushirishda avtomatik sozlash."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).parent.parent
VENV_DIR = PROJECT_DIR / "venv"
REQUIREMENTS = PROJECT_DIR / "requirements.txt"
ENV_EXAMPLE = PROJECT_DIR / ".env.example"
ENV_FILE = PROJECT_DIR / ".env"
DATA_DIRS = [
    PROJECT_DIR / "data",
    PROJECT_DIR / "data" / "memory",
    PROJECT_DIR / "data" / "knowledge",
    PROJECT_DIR / "data" / "uploads",
]


def _run(cmd: list[str], **kwargs: object) -> int:
    """Buyruqni ishga tushiradi va chiqish kodini qaytaradi."""
    result = subprocess.run(cmd, **kwargs)  # type: ignore[call-overload]
    return result.returncode


def step_venv() -> None:
    """Virtual environment yaratadi (yo'q bo'lsa)."""
    if VENV_DIR.exists():
        print(f"✓ Virtual environment mavjud: {VENV_DIR}")
        return
    print("⏳ Virtual environment yaratilmoqda...")
    code = _run([sys.executable, "-m", "venv", str(VENV_DIR)])
    if code != 0:
        print("✗ Virtual environment yaratishda xato.")
        sys.exit(1)
    print(f"✓ Virtual environment yaratildi: {VENV_DIR}")


def step_dependencies() -> None:
    """Kutubxonalarni o'rnatadi."""
    if not REQUIREMENTS.exists():
        print(f"✗ requirements.txt topilmadi: {REQUIREMENTS}")
        sys.exit(1)

    venv_pip = (
        VENV_DIR / "bin" / "pip"
        if sys.platform != "win32"
        else VENV_DIR / "Scripts" / "pip.exe"
    )
    pip_cmd = str(venv_pip) if venv_pip.exists() else "pip"

    print("⏳ Kutubxonalar o'rnatilmoqda...")
    code = _run([pip_cmd, "install", "-r", str(REQUIREMENTS)])
    if code != 0:
        print("✗ Kutubxonalar o'rnatishda xato.")
        sys.exit(1)
    print("✓ Kutubxonalar o'rnatildi.")


def step_env() -> None:
    """.env fayl mavjudligini tekshiradi, yo'q bo'lsa .env.example dan nusxa oladi."""
    if ENV_FILE.exists():
        print(f"✓ .env fayli mavjud: {ENV_FILE}")
        return
    if not ENV_EXAMPLE.exists():
        print(f"⚠ .env.example topilmadi: {ENV_EXAMPLE}")
        return
    shutil.copy(ENV_EXAMPLE, ENV_FILE)
    print(f"✓ .env yaratildi (.env.example dan nusxa): {ENV_FILE}")
    print("  ⚠ API kalitlarini .env faylida to'ldiring!")


def step_data_dirs() -> None:
    """data/ kataloglarini yaratadi."""
    for d in DATA_DIRS:
        d.mkdir(parents=True, exist_ok=True)
    print("✓ data/ kataloglari yaratildi.")


def step_launcher_permissions() -> None:
    """jarvis.sh ga ijro huquqi beradi (Unix/macOS)."""
    if sys.platform == "win32":
        return
    jarvis_sh = PROJECT_DIR / "launchers" / "jarvis.sh"
    if jarvis_sh.exists():
        jarvis_sh.chmod(jarvis_sh.stat().st_mode | 0o111)
        print("✓ launchers/jarvis.sh — ijro huquqi berildi.")


def main() -> None:
    """Barcha setup qadamlarini ketma-ket bajaradi."""
    print("\n" + "=" * 60)
    print("  JARVIS-X Auto Setup")
    print("=" * 60 + "\n")

    step_venv()
    step_dependencies()
    step_env()
    step_data_dirs()
    step_launcher_permissions()

    print("\n" + "=" * 60)
    print("  ✅ O'rnatish muvaffaqiyatli yakunlandi!")
    print("  Ishga tushirish: python jarvis_main.py")
    print("  yoki:           ./launchers/jarvis.sh")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

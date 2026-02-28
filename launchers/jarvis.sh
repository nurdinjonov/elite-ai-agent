#!/bin/bash
# JARVIS-X Linux Launcher
# Foydalanish: ./jarvis.sh yoki source jarvis.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/venv"

# Virtual environment tekshirish va yaratish
if [ ! -d "$VENV_DIR" ]; then
    echo "⏳ Virtual environment yaratilmoqda..."
    python3 -m venv "$VENV_DIR" || { echo "✗ Virtual environment yaratishda xato."; exit 1; }
    source "$VENV_DIR/bin/activate"
    pip install -r "$PROJECT_DIR/requirements.txt" || { echo "✗ Kutubxonalar o'rnatishda xato."; exit 1; }
    echo "✓ O'rnatish muvaffaqiyatli yakunlandi."
else
    source "$VENV_DIR/bin/activate"
fi

# JARVIS-X ni ishga tushirish
cd "$PROJECT_DIR"
python jarvis_main.py "$@"

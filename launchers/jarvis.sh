#!/usr/bin/env bash
# JARVIS-X Linux/macOS launcher
# Usage: ./launchers/jarvis.sh [options]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    # shellcheck source=/dev/null
    source venv/bin/activate
fi

# Load .env if present
if [ -f ".env" ]; then
    set -o allexport
    # shellcheck source=/dev/null
    source .env
    set +o allexport
fi

exec python jarvis_main.py "$@"

@echo off
REM JARVIS-X Windows Launcher

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
set VENV_DIR=%PROJECT_DIR%\venv

if not exist "%VENV_DIR%" (
    echo ⏳ Virtual environment yaratilmoqda...
    python -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
    pip install -r "%PROJECT_DIR%\requirements.txt"
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

cd /d "%PROJECT_DIR%"
python jarvis_main.py %*

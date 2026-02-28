@echo off
REM JARVIS-X Windows launcher
REM Usage: launchers\jarvis.bat

cd /d "%~dp0\.."

REM Activate virtual environment if it exists
IF EXIST ".venv\Scripts\activate.bat" (
    CALL .venv\Scripts\activate.bat
) ELSE IF EXIST "venv\Scripts\activate.bat" (
    CALL venv\Scripts\activate.bat
)

python jarvis_main.py %*

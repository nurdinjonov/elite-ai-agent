@echo off
REM JARVIS-X Windows ishga tushiruvchi
cd /d "%~dp0"

SET VENV_DIR=runtime\venv

IF NOT EXIST "%VENV_DIR%" (
    echo Virtual muhit yaratilmoqda...
    python -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
    echo Bog'liqliklar o'rnatilmoqda...
    pip install -r requirements.txt
) ELSE (
    call "%VENV_DIR%\Scripts\activate.bat"
)

python start.py %*

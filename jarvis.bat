@echo off
REM JARVIS-X Windows ishga tushiruvchi
cd /d "%~dp0"

SET VENV_DIR=runtime\venv

REM Python mavjudligini tekshirish
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [91mXato: python topilmadi.[0m
    echo    Python 3.10+ o'rnating: https://www.python.org/downloads/
    exit /b 1
)

IF NOT EXIST "%VENV_DIR%\Scripts\python.exe" (
    echo [93mVirtual muhit topilmadi. Avval sozlashni ishga tushiring:[0m
    echo    python setup.py
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"

python start.py %*

@echo off
:: Check Claude Code installation status

title Claude Code Installation Status

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.6+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Change to script directory first
cd /d "%~dp0"

:: Run the Python installer with status flag
echo Checking Claude Code installation status...
echo.
python claude_code_installer.py --status

echo.
pause 
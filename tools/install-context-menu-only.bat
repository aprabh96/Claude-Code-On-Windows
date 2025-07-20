@echo off
:: Install only the context menu integration
:: For users who already have Claude Code installed

title Claude Code Context Menu Installer

:: Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This installer requires Administrator privileges.
    echo Right-click on this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

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

:: Run the Python installer with context-only flag
echo Installing Claude Code context menu integration...
echo.
python claude_code_installer.py --context-only

echo.
pause 
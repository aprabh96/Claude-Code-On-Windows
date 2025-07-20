@echo off
:: Test Claude Code installation and context menu integration

title Claude Code Installation Test

echo ===============================================
echo    Testing Claude Code Installation
echo ===============================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo ✓ Python is available
echo.

:: Change to script directory first
cd /d "%~dp0"

:: Run installation status check
echo Running installation status check...
echo.
python claude_code_installer.py --status

echo.
echo ===============================================
echo             Test Complete!
echo ===============================================
echo.
echo If everything shows "✓ Installed", your setup is working!
echo.
echo To test the context menu:
echo 1. Open Windows Explorer
echo 2. Right-click in any folder
echo 3. Look for "Open in Claude Code" option
echo.
pause 
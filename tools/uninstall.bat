@echo off
:: Uninstall Claude Code context menu integration

title Claude Code Uninstaller

:: Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This uninstaller requires Administrator privileges.
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
    echo You can also manually remove the context menu by deleting these registry keys:
    echo HKEY_CLASSES_ROOT\Directory\Background\shell\OpenInClaude
    echo HKEY_CLASSES_ROOT\Directory\shell\OpenInClaude
    echo.
    pause
    exit /b 1
)

:: Change to script directory first
cd /d "%~dp0"

:: Run the Python installer with uninstall flag
echo Uninstalling Claude Code context menu integration...
echo.
python claude_code_installer.py --uninstall

echo.
pause 
@echo off
:: Quick Context Menu Installer
:: For users who already have WSL, Ubuntu, and Claude Code installed
:: Just adds the "Open in Claude Code" context menu

title Quick Claude Code Context Menu Installer

echo ===============================================
echo    Quick Claude Code Context Menu Setup
echo ===============================================
echo.

:: Check if running as admin
echo Checking administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Administrator privileges required!
    echo.
    echo To fix this:
    echo 1. Close this window
    echo 2. Right-click on "quick-context-menu.bat"  
    echo 3. Select "Run as administrator"
    echo 4. Try again
    echo.
    echo Press any key to close this window...
    pause
    exit /b 1
)

echo OK: Administrator privileges confirmed
echo.

:: Change to script directory
cd /d "%~dp0"

echo This installer assumes you already have:
echo * WSL installed and working
echo * Ubuntu distribution in WSL  
echo * Claude Code installed in Ubuntu
echo.
echo If you don't have these, use run.bat instead for full installation.
echo.
set /p confirm="Continue with context menu installation? (y/n): "

if /i not "%confirm%"=="y" (
    echo Installation cancelled.
    pause
    exit /b 0
)

echo.
echo ====================================================
echo         Installing Context Menu Only
echo ====================================================
echo.

:: Run Python installer with context-only flag
echo Running context menu installer...
python claude_code_installer.py --context-only

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Context menu installed!
    echo.
    echo You can now:
    echo * Right-click any folder in Windows Explorer
    echo * Select "Open in Claude Code"
    echo * Claude Code will launch in that directory!
    echo.
) else (
    echo.
    echo ERROR: Context menu installation failed!
    echo Try using run.bat for full installation instead.
    echo.
)

echo Press any key to exit...
pause 
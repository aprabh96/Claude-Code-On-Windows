@echo off
echo ================================================================
echo  Claude Code Context Menu - Reinstall with Fixed Version
echo ================================================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click on this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo Running as Administrator - proceeding with reinstall...
echo.

:: Uninstall existing context menu first
echo Step 1: Removing old context menu integration...
python claude_code_installer.py --uninstall-context 2>nul
echo.

:: Install new context menu with fixed batch file
echo Step 2: Installing fixed context menu integration...
python claude_code_installer.py --context-only

echo.
echo ================================================================
echo Installation complete!
echo.
echo You should now be able to:
echo 1. Right-click in any folder
echo 2. Select "Open in Claude Code"
echo 3. See Claude Code launch in a new terminal window
echo.
echo If you encounter issues, check the log files:
echo - C:\Scripts\claude_launcher.log
echo - C:\Scripts\claude_launcher_error.log
echo ================================================================
pause 
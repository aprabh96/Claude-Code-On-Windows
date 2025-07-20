@echo off
:: Claude Code - One-Click Launcher
:: This script automatically checks for Python and runs the Claude Code installer

title Claude Code - Setup and Run

echo ===============================================
echo          Claude Code - One-Click Setup
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
    echo 2. Right-click on "run.bat"  
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
echo Switching to script directory...
cd /d "%~dp0"
echo Current directory: %CD%
echo.

:: Check if Python is available and working
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo OK: Python is available
    python --version
    echo.
    goto :run_claude
)

:: Python not found - offer to install it
echo.
echo WARNING: Python is not installed or not in PATH
echo.
echo Python is required to run Claude Code installer.
echo This installer can automatically download and install Python for you.
echo.
echo Options:
echo 1. Auto-download and install Python (recommended)
echo 2. Manual installation instructions  
echo 3. Exit
echo.
set /p choice="Choose an option (1-3): "

if "%choice%"=="1" goto :auto_install_python
if "%choice%"=="2" goto :manual_python  
if "%choice%"=="3" goto :exit

echo.
echo ERROR: Invalid choice "%choice%"
echo Please enter 1, 2, or 3
echo.
pause
goto :exit

:auto_install_python
echo.
echo ====================================================
echo           Auto-Installing Python 3.11.7
echo ====================================================
echo.
echo This will:
echo * Download Python 3.11.7 (about 25MB)
echo * Install it with PATH configured automatically
echo * Take about 2-3 minutes total
echo.
echo Starting download...

:: Download Python installer
echo Downloading from python.org...
powershell -Command "try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python_installer.exe' -UseBasicParsing; Write-Host 'Download completed successfully' } catch { Write-Host 'Download failed:' $_.Exception.Message; exit 1 }"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Download failed! This could be due to:
    echo * No internet connection
    echo * Firewall blocking the download
    echo * Temporary server issues
    echo.
    echo Please try manual installation instead.
    echo.
    pause
    goto :manual_python
)

if not exist "python_installer.exe" (
    echo ERROR: Python installer file not found after download
    echo Please try manual installation instead
    echo.
    pause
    goto :manual_python
)

echo OK: Python installer downloaded successfully
echo.
echo Installing Python (this will take 2-3 minutes)...
echo Please wait - the installer is running silently...

:: Install Python silently with PATH
echo Starting installation...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python installation failed (exit code: %errorlevel%)
    echo This could be due to:
    echo * Insufficient permissions
    echo * Antivirus blocking installation
    echo * Corrupted download
    echo.
    echo Please try manual installation instead.
    echo.
    pause
    goto :manual_python
)

:: Clean up installer
echo Cleaning up installer file...
del python_installer.exe >nul 2>&1

echo.
echo SUCCESS: Python installed successfully!
echo.
echo IMPORTANT: You need to restart this script for Python to be available.
echo.
echo Steps:
echo 1. Close this window
echo 2. Right-click "run.bat" again
echo 3. Select "Run as administrator"  
echo 4. Python should now be detected automatically
echo.
echo Press any key to close this window...
pause
exit /b 0

:manual_python
echo.
echo Manual Python Installation:
echo.
echo 1. Go to: https://python.org/downloads/
echo 2. Download Python 3.8 or newer for Windows
echo 3. During installation, CHECK "Add Python to PATH"
echo 4. After installation, run this script again
echo.
pause
exit /b 0

:run_claude
echo ====================================================
echo           Launching Claude Code Installer
echo ====================================================
echo.
echo Starting the Python installer with GUI interface...
echo.

:: Check if the Python script exists
if not exist "%~dp0claude_code_installer.py" (
    echo ERROR: claude_code_installer.py not found!
    echo.
    echo Make sure you're running this from the correct directory.
    echo Current directory: %CD%
    echo Expected file location: %~dp0claude_code_installer.py
    echo.
    echo Press any key to exit...
    pause
    exit /b 1
)

:: Run the Python installer with GUI
echo Executing GUI...
echo If a new window doesn't appear, there may be an issue with your Python's Tkinter library.
start "Claude Code GUI" /wait python "%~dp0claude_code_installer.py"

:: Check if Python script ran successfully
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python script exited with error code: %errorlevel%
    echo.
    echo This could indicate:
    echo * Python installation issues
    echo * Missing Python libraries (tkinter)
    echo * Script execution problems
    echo.
    echo Try running this command manually to see detailed errors:
    echo python "%~dp0claude_code_installer.py"
    echo.
    echo Press any key to exit...
    pause
    exit /b 1
)

echo.
echo SUCCESS: Claude Code setup completed successfully!
echo.
echo You can now:
echo * Right-click any folder in Windows Explorer
echo * Select "Open in Claude Code"  
echo * Claude Code will launch in that directory!
echo.
echo Press any key to exit...
pause
goto :exit

:exit
echo.
echo Exiting Claude Code installer...
echo.
pause
exit /b 0

echo.
echo =========================================
echo SCRIPT FINISHED - PRESS ANY KEY TO EXIT
echo =========================================
pause 
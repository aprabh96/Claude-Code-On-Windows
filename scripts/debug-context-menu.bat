@echo off
:: Debug Context Menu Launcher
:: This will help us figure out why "Open in Claude Code" doesn't work

title Debug Claude Code Context Menu

echo ===============================================
echo       Debug Claude Code Context Menu
echo ===============================================
echo.

echo Step 1: Check what launcher scripts exist in C:\Scripts
echo.
if exist "C:\Scripts" (
    echo ✓ C:\Scripts folder exists
    echo Contents:
    dir "C:\Scripts" /b
    echo.
) else (
    echo ❌ C:\Scripts folder does not exist!
    echo The context menu won't work without this folder.
    pause
    exit /b 1
)

echo Step 2: Check registry entries (what the context menu points to)
echo.
echo Background context menu points to:
reg query "HKEY_CLASSES_ROOT\Directory\Background\shell\OpenInClaude\command" /ve 2>nul
if %errorlevel% neq 0 echo ❌ Background context menu not found

echo.
echo Folder context menu points to:
reg query "HKEY_CLASSES_ROOT\Directory\shell\OpenInClaude\command" /ve 2>nul
if %errorlevel% neq 0 echo ❌ Folder context menu not found

echo.
echo Step 3: Test the launcher script manually
echo.
echo Current directory: %CD%
echo Testing launcher with current directory...
echo.

if exist "C:\Scripts\open_in_claude.py" (
    echo ✓ Found Python launcher: C:\Scripts\open_in_claude.py
    echo.
    echo Running: python "C:\Scripts\open_in_claude.py" "%CD%"
    echo.
    echo ========== LAUNCHER OUTPUT ==========
    python "C:\Scripts\open_in_claude.py" "%CD%"
    echo ========== END LAUNCHER OUTPUT ==========
    echo.
    if %errorlevel% equ 0 (
        echo ✅ Launcher executed successfully (exit code 0)
    ) else (
        echo ❌ Launcher failed with exit code: %errorlevel%
    )
) else if exist "C:\Scripts\open_in_claude.cmd" (
    echo ✓ Found CMD launcher: C:\Scripts\open_in_claude.cmd
    echo.
    echo Running: "C:\Scripts\open_in_claude.cmd" "%CD%"
    echo.
    echo ========== LAUNCHER OUTPUT ==========
    call "C:\Scripts\open_in_claude.cmd" "%CD%"
    echo ========== END LAUNCHER OUTPUT ==========
    echo.
    if %errorlevel% equ 0 (
        echo ✅ Launcher executed successfully (exit code 0)
    ) else (
        echo ❌ Launcher failed with exit code: %errorlevel%
    )
) else (
    echo ❌ No launcher script found!
    echo Expected: C:\Scripts\open_in_claude.py or C:\Scripts\open_in_claude.cmd
)

echo.
echo Step 4: Check if WSL and Claude Code work
echo.
echo Testing WSL access:
wsl --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ WSL is accessible
) else (
    echo ❌ WSL is not accessible
)

echo.
echo Testing Ubuntu access:
wsl -d Ubuntu echo "Ubuntu is working" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Ubuntu is accessible
) else (
    echo ❌ Ubuntu is not accessible
)

echo.
echo Testing Claude Code in interactive mode:
wsl -d Ubuntu bash -ic "which claude" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Claude Code is accessible in interactive mode
) else (
    echo ❌ Claude Code is not accessible in interactive mode
)

echo.
echo ===============================================
echo                Debug Complete
echo ===============================================
echo.
echo If you see any ❌ errors above, those need to be fixed.
echo If everything shows ✓ but Claude Code still doesn't open,
echo the issue is likely in the launcher script command.
echo.
pause 
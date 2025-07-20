@echo off
:: Fix Context Menu - Remove old files and install correctly

title Fix Claude Code Context Menu

echo ===============================================
echo    Fix Claude Code Context Menu
echo ===============================================
echo.

:: Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Need Administrator privileges
    echo Right-click this file and "Run as administrator"
    pause
    exit /b 1
)

echo Step 1: Remove old launcher file
echo.
if exist "C:\Scripts\open_in_claude.cmd" (
    echo Found old launcher file: C:\Scripts\open_in_claude.cmd
    echo Removing it...
    del "C:\Scripts\open_in_claude.cmd"
    if %errorlevel% equ 0 (
        echo ✓ Old file removed successfully
    ) else (
        echo ❌ Failed to remove old file
    )
) else (
    echo ✓ No old file to remove
)

echo.
echo Step 2: Install new context menu
echo.
cd /d "%~dp0"
echo Running: python claude_code_installer.py --context-only
python claude_code_installer.py --context-only

echo.
echo Step 3: Test the new launcher
echo.
if exist "C:\Scripts\open_in_claude.py" (
    echo ✓ New Python launcher exists
    echo Testing with current directory...
    echo.
    echo ========== TEST OUTPUT ==========
    python "C:\Scripts\open_in_claude.py" "%CD%"
    echo ========== END TEST ==========
    echo.
    if %errorlevel% equ 0 (
        echo ✅ Test successful!
    ) else (
        echo ❌ Test failed with error code: %errorlevel%
    )
) else (
    echo ❌ New Python launcher not found!
)

echo.
echo Step 4: Verify context menu in registry
echo.
reg query "HKEY_CLASSES_ROOT\Directory\Background\shell\OpenInClaude\command" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Context menu installed in registry
) else (
    echo ❌ Context menu not found in registry
)

echo.
echo ===============================================
echo                  Summary
echo ===============================================
echo.
echo If you see ✓ for all steps above:
echo 1. Right-click in any folder in Windows Explorer
echo 2. You should see "Open in Claude Code"
echo 3. Click it to test!
echo.
echo If you see any ❌ errors, we need to debug further.
echo.
pause 
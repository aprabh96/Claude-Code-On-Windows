@echo off
:: Test script to verify the Claude Code context menu launcher works
:: This simulates what happens when you right-click and select "Open in Claude Code"

title Test Claude Code Context Menu

echo ===============================================
echo      Testing Claude Code Context Menu
echo ===============================================
echo.

:: Check if launcher script exists
if not exist "C:\Scripts\open_in_claude.py" (
    echo ERROR: Launcher script not found at C:\Scripts\open_in_claude.py
    echo.
    echo Make sure you've run the installer first.
    echo.
    pause
    exit /b 1
)

echo ✓ Launcher script found
echo.

:: Test with current directory
echo Testing with current directory: %CD%
echo.
echo This will simulate right-clicking in this folder and selecting "Open in Claude Code"
echo.
set /p confirm="Press Enter to test, or Ctrl+C to cancel..."

echo.
echo ====================================================
echo           LAUNCHING CLAUDE CODE TEST
echo ====================================================
echo.

:: Run the launcher script with current directory (same as context menu)
echo Executing: python "C:\Scripts\open_in_claude.py" "%CD%"
python "C:\Scripts\open_in_claude.py" "%CD%"

echo.
echo ====================================================
echo                  TEST RESULTS
echo ====================================================
echo.

if %errorlevel% equ 0 (
    echo ✅ SUCCESS: Launcher executed without errors
    echo.
    echo What should have happened:
    echo 1. A new command window should have opened
    echo 2. Claude Code should be running in WSL Ubuntu  
    echo 3. The working directory should be: /mnt/c/path/to/this/folder
    echo.
    echo If Claude Code started successfully, the context menu is working!
    echo If not, check the error messages above.
) else (
    echo ❌ FAILED: Launcher exited with error code %errorlevel%
    echo.
    echo Check the error messages above to see what went wrong.
)

echo.
echo Press any key to exit...
pause 
@echo off
title Simple Debug - Press Enter at Each Step

echo Starting debug...
pause

echo Checking if C:\Scripts exists...
if exist "C:\Scripts" (
    echo YES - C:\Scripts exists
) else (
    echo NO - C:\Scripts does not exist
)
pause

echo Contents of C:\Scripts:
dir "C:\Scripts" 2>nul
if %errorlevel% neq 0 echo Folder empty or does not exist
pause

echo Checking registry for context menu...
echo This checks what the right-click menu actually runs:
reg query "HKEY_CLASSES_ROOT\Directory\Background\shell\OpenInClaude\command" 2>nul
if %errorlevel% neq 0 echo Context menu not found in registry
pause

echo Testing if we can run Python...
python --version
if %errorlevel% neq 0 echo Python not working
pause

echo Testing WSL...
wsl --version
if %errorlevel% neq 0 echo WSL not working
pause

echo All done! Press Enter to close.
pause 
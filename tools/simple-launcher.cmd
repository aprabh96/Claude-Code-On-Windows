@echo off
:: Simple Claude Code Launcher (ChatGPT approach)
:: This is the simpler alternative to the Python launcher

set "WINPATH=%~1"

echo Starting Claude Code in: %WINPATH%

:: Convert Windows path to WSL path
for /f "delims=" %%i in ('wsl.exe wslpath "%WINPATH%"') do set "WSLPATH=%%i"

echo WSL path: %WSLPATH%

:: Launch Claude Code directly in WSL
echo Launching Claude Code...
wsl.exe -d Ubuntu --cd "%WSLPATH%" claude 
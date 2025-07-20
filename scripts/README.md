# Utility Scripts

This folder contains utility scripts for debugging, testing, and maintaining Claude Code integration.

## Scripts Overview

### Main Utilities
- **`reinstall-context-menu.bat`** - Reinstalls the context menu with the latest fixes (run as admin)
- **`fix-context-menu.bat`** - Attempts to fix common context menu issues
- **`test-context-menu.bat`** - Tests if the context menu is working properly

### Debug Tools
- **`debug-context-menu.bat`** - Verbose debugging for context menu issues
- **`simple-debug.bat`** - Basic debugging information
- **`quick-context-menu.bat`** - Quick context menu installation

## Usage

Most scripts should be run as Administrator for proper functionality:

1. Right-click on the desired `.bat` file
2. Select "Run as administrator"
3. Follow the on-screen instructions

## Recommended Workflow

If you're having context menu issues:

1. Run `test-context-menu.bat` first to diagnose the problem
2. If broken, run `reinstall-context-menu.bat` to fix it
3. Use `debug-context-menu.bat` for detailed troubleshooting if needed

These scripts are primarily for developers and advanced users. Regular users should use the main `run.bat` file in the root directory. 
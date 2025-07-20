# Tools Folder

This folder contains additional utilities and technical files for the Claude Code installer.

## 📁 Contents

### Batch Files
- **`install-context-menu-only.bat`** - Install only the context menu (if you already have Claude Code)
- **`uninstall.bat`** - Remove the context menu integration
- **`check-status.bat`** - Check what's installed and what's missing
- **`test-installation.bat`** - Test that everything is working correctly

### Documentation
- **`CHANGELOG.md`** - Complete history of changes and improvements
- **`requirements.txt`** - Python dependencies (none needed - uses standard library only)

## 🎯 When to Use These

### For Most Users
**Just use `run.bat` in the main folder** - it does everything automatically!

### For Advanced Users
- **Already have Claude Code?** → Use `install-context-menu-only.bat`
- **Want to uninstall?** → Use `uninstall.bat`  
- **Something not working?** → Use `check-status.bat` to diagnose
- **Want to test?** → Use `test-installation.bat` to verify

## 🔧 Technical Details

All these tools use the same Python script (`claude_code_installer.py`) with different command-line arguments:

```bash
python claude_code_installer.py --context-only  # Context menu only
python claude_code_installer.py --uninstall     # Uninstall
python claude_code_installer.py --status        # Check status
```

## 💡 Pro Tip

If you're comfortable with command line, you can use the Python script directly instead of the batch files:

```bash
# Show help
python claude_code_installer.py --help

# Full installation with GUI
python claude_code_installer.py

# Console mode
python claude_code_installer.py --console
``` 
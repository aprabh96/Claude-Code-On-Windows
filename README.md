# Claude Code Context Menu Integration for Windows

A modern, robust installer for integrating Claude Code with Windows Explorer context menus. Right-click any folder and launch Claude Code instantly!

## 🚀 **ONE-CLICK SETUP**

**Right-click `run.bat` → "Run as administrator" → Done!** ✨

## ✨ What's New (v2.0)

This project has been **completely overhauled** with a modern Python-based installer that fixes all the previous issues:

- 🚀 **One-click setup** - Just run `run.bat` and everything is automatic
- 🐍 **Python auto-install** - Checks for Python and installs it if needed
- 🎨 **Beautiful GUI** - User-friendly graphical interface  
- 🛡️ **Robust error handling** - Clear error messages and detailed logging  
- 📊 **Real-time status** - See what's installed and what's missing
- 🧹 **Clean directory** - Only essential files in main folder

## 🎯 Features

- **One-Click Integration**: Right-click any folder → "Open in Claude Code"
- **Smart Installation**: Automatically installs Python, WSL, Ubuntu, Node.js, and Claude Code if needed
- **Beautiful GUI**: Modern interface with real-time progress and logging
- **Auto Python Setup**: Downloads and installs Python automatically if missing
- **Clean Organization**: All extra tools moved to `tools/` folder

## 📋 Prerequisites

- **Windows 10/11** (with WSL2 support)
- **Administrator privileges** for installation
- **Python 3.6+** (auto-installed if missing)

## 🚀 Quick Start

### Super Simple (Recommended)

1. **Right-click `run.bat`** → **"Run as administrator"**  
2. **Follow the prompts** (Python will be installed automatically if needed)
3. **Use the GUI** to install everything with one click
4. **Done!** 🎉

### Alternative: Direct Python Usage

If you already have Python:

```bash
# Launch GUI
python claude_code_installer.py

# Or use command line
python claude_code_installer.py --help
```

## 📁 Clean Directory Structure

```
Claude Code On Windows/
├── run.bat                     ← CLICK THIS (main launcher)
├── claude_code_installer.py    ← Python installer with GUI
├── README.md                   ← This file
├── QUICK_START.md             ← 5-minute setup guide
├── LICENSE                     ← MIT license
├── tools/                     ← Extra utilities (optional)
│   ├── install-context-menu-only.bat
│   ├── uninstall.bat
│   ├── check-status.bat
│   ├── test-installation.bat
│   ├── CHANGELOG.md
│   └── requirements.txt
└── legacy/                    ← Old deprecated files
```

**Just focus on `run.bat` - everything else is optional!**

## 🎮 Usage

After installation:

1. **Open Windows Explorer**
2. **Navigate to any folder**
3. **Right-click** in the folder (empty space) or on a folder
4. **Select "Open in Claude Code"**
5. **Claude Code launches** in that directory! 🎉

## 🔧 Advanced Usage

### Command Line Options

```bash
# Show beautiful GUI (default)
python claude_code_installer.py

# Force console mode
python claude_code_installer.py --console

# Install only context menu (skip WSL/Ubuntu setup)
python claude_code_installer.py --context-only

# Uninstall context menu integration
python claude_code_installer.py --uninstall

# Check what's installed
python claude_code_installer.py --status
```

### Tools Folder

Advanced users can use utilities in the `tools/` folder:
- **Context menu only**: `tools/install-context-menu-only.bat`
- **Uninstall**: `tools/uninstall.bat`  
- **Check status**: `tools/check-status.bat`
- **Test setup**: `tools/test-installation.bat`

### Direct WSL Usage

You can also use Claude Code directly in WSL:

```bash
# Open Ubuntu terminal
ubuntu

# Navigate to your project
cd /mnt/c/your/project/path

# Start Claude Code
claude
```

## 🛠️ Troubleshooting

### The GUI Makes Everything Easy!

The new GUI shows you exactly what's installed and what's missing, with real-time progress and clear error messages.

### Common Issues

- **"Python is not installed"** → `run.bat` will install it automatically
- **"Must be run as Administrator"** → Right-click and "Run as administrator"
- **Context menu doesn't appear** → Use `tools/check-status.bat` to diagnose

### Manual Cleanup

If you need to manually remove the context menu:

1. Delete these registry keys:
   - `HKEY_CLASSES_ROOT\Directory\Background\shell\OpenInClaude`
   - `HKEY_CLASSES_ROOT\Directory\shell\OpenInClaude`
2. Delete `C:\Scripts\open_in_claude.py`

## 📊 What Gets Installed

The installer can set up everything you need:

| Component | Purpose | Auto-Installed |
|-----------|---------|---------------|
| **Python** | Runs the installer | ✅ Yes (if missing) |
| **WSL** | Windows Subsystem for Linux | ✅ Yes |
| **Ubuntu** | Linux distribution for WSL | ✅ Yes |
| **Node.js** | JavaScript runtime for Claude Code | ✅ Yes |
| **Claude Code** | The actual Claude Code application | ✅ Yes |
| **Context Menu** | Windows Explorer integration | ✅ Yes |

## 🔒 Security

- **Minimal permissions**: Only requires admin rights for registry modifications
- **No persistent changes**: Uses Python instead of risky PowerShell policies
- **Clean uninstall**: Removes all traces when uninstalling
- **Audit trail**: Comprehensive logging of all actions

## 🆚 What Changed from v1.x

| Old (v1.x) | New (v2.0) | Improvement |
|------------|------------|-------------|
| 6+ batch files | 1 main file (`run.bat`) | Much simpler |
| Complex 3-step process | One-click install | Faster setup |
| No GUI | Beautiful GUI interface | Better UX |
| Manual Python setup | Auto Python install | Zero friction |
| PowerShell execution policies | No PowerShell needed | More secure |
| Manual troubleshooting | Built-in diagnostics | Easier support |
| Cluttered directory | Clean organization | Less confusing |

## 🤝 Contributing

Feel free to submit issues and enhancement requests! The new Python-based architecture makes it much easier to add features and fix issues.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. **Use the GUI** - it shows exactly what's wrong
2. **Check `tools/check-status.bat`** for diagnostics
3. **Review logs**: Check `claude_installer.log` 
4. **Try reinstalling**: Run `run.bat` again
5. **Report issues**: Include log files and error messages

The new architecture provides much better error reporting and diagnostics than the old batch-based system!

---

**TL;DR: Just run `run.bat` as administrator and everything works! 🎯** 
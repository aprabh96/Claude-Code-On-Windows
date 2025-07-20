# 🚀 Quick Start Guide

**Get Claude Code working in Windows Explorer in under 2 minutes!**

## ⚡ Super Quick Install

**Right-click `run.bat` → "Run as administrator" → Done!** 🎉

That's it! The script will:
- ✅ Check for Python (install automatically if missing)  
- ✅ Launch a beautiful GUI
- ✅ Install everything with one click
- ✅ Set up the context menu

## 🎮 How to Use

1. **Open any folder in Windows Explorer**
2. **Right-click** in the folder (or on a folder)  
3. **Click "Open in Claude Code"**
4. **Claude Code launches!** ✨

## 📋 Prerequisites

✅ **Windows 10/11**  
✅ **Administrator access**  
✅ **Internet connection** (for downloading components)

**Python?** Don't worry - `run.bat` installs it automatically if missing!

## 🔧 If You Already Have Claude Code

**Right-click `tools/install-context-menu-only.bat` → "Run as administrator"**

This skips the WSL/Ubuntu setup and just adds the context menu.

## 🖥️ What You'll See

The installer opens a **beautiful GUI** that shows:
- ✅ Real-time status of each component
- 🔄 Progress bar during installation  
- 📝 Detailed log of what's happening
- 🎯 Simple buttons: "Install Everything", "Context Menu Only", "Uninstall"

## 🛠️ Troubleshooting (Rare!)

### "Must run as Administrator"
- Right-click `run.bat`
- Select "Run as administrator"

### "Python is not installed"  
- The script handles this automatically!
- If it fails, go to [python.org](https://python.org) and install manually

### Context menu doesn't appear
- Run `tools/check-status.bat` to see what's wrong
- Try running `run.bat` again

### Something else broke?
- Check `claude_installer.log` for detailed error info
- The GUI shows clear error messages
- Run `tools/uninstall.bat` then `run.bat` for a fresh start

## 📁 What You Get

After running `run.bat`, you'll have:
- ✅ Python (if not already installed)
- ✅ WSL with Ubuntu (if not already installed)
- ✅ Node.js and Claude Code in WSL
- ✅ "Open in Claude Code" in your right-click menu
- ✅ Clear error messages if something goes wrong

## 🆘 Need Help?

1. **The GUI tells you everything!** - Look at the status indicators and log
2. **Run `tools/check-status.bat`** to see what's installed
3. **Check `claude_installer.log`** for detailed error info  
4. **Submit an issue** with your log file

## 💡 Pro Tips

- **First time?** Just use `run.bat` - it handles everything
- **Already have WSL/Claude?** Use `tools/install-context-menu-only.bat`
- **Want to uninstall?** Use `tools/uninstall.bat`
- **Like command line?** Run `python claude_code_installer.py --help`

---

**Bottom line: This is now as simple as running ONE file! No more complex multi-step processes!** 🎯 
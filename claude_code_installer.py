#!/usr/bin/env python3
"""
Claude Code Windows Installer with GUI
A modern, robust installer for Claude Code integration on Windows

This script replaces the fragile batch/PowerShell approach with a single,
comprehensive Python solution that handles:
- WSL/Ubuntu installation and setup
- Claude Code installation  
- Windows context menu integration
- Error handling and logging
- Uninstallation
"""

__version__ = "0.1.0"

import os
import sys
import subprocess
import json
import logging
import argparse
import winreg
from pathlib import Path
from typing import Optional, Tuple, List
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

# First, check for tkinter
try:
    import tkinter
except ImportError:
    print("FATAL ERROR: Python is missing the Tkinter library, which is required for the GUI.")
    print("This is uncommon, but can happen with custom Python installations.")
    print("\nPlease reinstall Python from https://python.org, ensuring the 'tcl/tk and IDLE' feature is selected.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('claude_installer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def colored_print(message: str, color: str = Colors.WHITE) -> None:
    """Print colored message to console"""
    print(f"{color}{message}{Colors.RESET}")

def is_admin() -> bool:
    """Check if running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command: List[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    """Run a command with proper error handling"""
    try:
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture,
            text=True,
            timeout=300  # 5 minute timeout
        )
        if result.stdout:
            logger.debug(f"Command output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        if e.stderr:
            logger.error(f"Error output: {e.stderr}")
        raise
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out: {e}")
        raise

class WSLManager:
    """Handles WSL installation and management"""
    
    def is_wsl_installed(self) -> bool:
        """Check if WSL is installed"""
        try:
            result = run_command(['wsl', '--version'], check=False)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def is_ubuntu_installed(self) -> bool:
        """Check if Ubuntu is installed in WSL"""
        try:
            # Use the same command format that works: wsl -l -v
            result = run_command(['wsl', '-l', '-v'], check=False)
            logger.info(f"WSL list command returned: {result.returncode}")
            logger.info(f"WSL list output (raw): {repr(result.stdout)}")
            
            if result.returncode == 0:
                # WSL sometimes returns UTF-16 output with null bytes, clean it up
                clean_output = result.stdout.replace('\x00', '').strip()
                logger.info(f"WSL list output (cleaned): '{clean_output}'")
                
                # Check if Ubuntu appears in the cleaned output (case-insensitive)
                output_lower = clean_output.lower()
                has_ubuntu = 'ubuntu' in output_lower
                logger.info(f"Checking for 'ubuntu' in cleaned output: {has_ubuntu}")
                return has_ubuntu
            return False
        except FileNotFoundError:
            logger.error("WSL command not found")
            return False
        except Exception as e:
            logger.error(f"Error checking Ubuntu: {e}")
            return False
    
    def install_wsl(self) -> bool:
        """Install WSL"""
        try:
            colored_print("Installing WSL...", Colors.YELLOW)
            run_command(['wsl', '--install', '--no-launch'])
            colored_print("WSL installed successfully!", Colors.GREEN)
            return True
        except Exception as e:
            colored_print(f"Failed to install WSL: {e}", Colors.RED)
            return False
    
    def install_ubuntu(self) -> bool:
        """Install Ubuntu distribution"""
        try:
            colored_print("Installing Ubuntu distribution...", Colors.YELLOW)
            run_command(['wsl', '--install', '-d', 'Ubuntu', '--no-launch'])
            colored_print("Ubuntu installed successfully!", Colors.GREEN)
            return True
        except Exception as e:
            colored_print(f"Failed to install Ubuntu: {e}", Colors.RED)
            return False
    
    def setup_ubuntu_environment(self) -> bool:
        """Setup Ubuntu environment with Node.js and dependencies"""
        try:
            colored_print("Setting up Ubuntu environment...", Colors.YELLOW)
            
            # Update package lists
            colored_print("Updating package lists...", Colors.CYAN)
            run_command(['wsl', '-d', 'Ubuntu', '--', 'sudo', 'apt', 'update', '-y'])
            run_command(['wsl', '-d', 'Ubuntu', '--', 'sudo', 'apt', 'upgrade', '-y'])
            
            # Install essential packages
            colored_print("Installing essential packages...", Colors.CYAN)
            run_command(['wsl', '-d', 'Ubuntu', '--', 'sudo', 'apt', 'install', '-y', 
                        'curl', 'wget', 'git', 'build-essential'])
            
            # Install Node.js and npm
            colored_print("Installing Node.js and npm...", Colors.CYAN)
            run_command(['wsl', '-d', 'Ubuntu', '--', 'curl', '-fsSL', 
                        'https://deb.nodesource.com/setup_18.x', '|', 'sudo', '-E', 'bash', '-'])
            run_command(['wsl', '-d', 'Ubuntu', '--', 'sudo', 'apt', 'install', '-y', 'nodejs'])
            
            # Verify installation
            node_result = run_command(['wsl', '-d', 'Ubuntu', '--', 'node', '--version'])
            npm_result = run_command(['wsl', '-d', 'Ubuntu', '--', 'npm', '--version'])
            
            colored_print(f"Node.js version: {node_result.stdout.strip()}", Colors.GREEN)
            colored_print(f"npm version: {npm_result.stdout.strip()}", Colors.GREEN)
            
            return True
        except Exception as e:
            colored_print(f"Failed to setup Ubuntu environment: {e}", Colors.RED)
            return False

class ClaudeCodeManager:
    """Handles Claude Code installation"""
    
    def is_claude_installed(self) -> bool:
        """Check if Claude Code is installed"""
        try:
            # Use interactive shell since Claude Code often only works in interactive mode
            # This simulates what happens when you type 'ubuntu' then 'claude'
            result = run_command(['wsl', '-d', 'Ubuntu', 'bash', '-ic', 'which claude'], check=False)
            logger.info(f"Interactive 'which claude' returned: {result.returncode}, output: {repr(result.stdout)}")
            
            if result.returncode == 0 and result.stdout.strip():
                return True
            
            # Try running claude --version in interactive mode
            result2 = run_command(['wsl', '-d', 'Ubuntu', 'bash', '-ic', 'claude --version'], check=False)
            logger.info(f"Interactive 'claude --version' returned: {result2.returncode}, output: {repr(result2.stdout)}")
            
            if result2.returncode == 0:
                return True
                
            return False
        except Exception as e:
            logger.error(f"Error checking Claude Code: {e}")
            return False
    
    def install_claude_code(self) -> bool:
        """Install Claude Code in WSL Ubuntu"""
        try:
            colored_print("Installing Claude Code...", Colors.YELLOW)
            
            # Set npm config for Linux
            run_command(['wsl', '-d', 'Ubuntu', '--', 'npm', 'config', 'set', 'os', 'linux'])
            
            # Install Claude Code
            run_command(['wsl', '-d', 'Ubuntu', '--', 'npm', 'install', '-g', 
                        '@anthropic-ai/claude-code', '--force', '--no-os-check'])
            
            # Verify installation
            version_result = run_command(['wsl', '-d', 'Ubuntu', '--', 'claude', '--version'])
            colored_print(f"Claude Code installed successfully!", Colors.GREEN)
            colored_print(f"Version: {version_result.stdout.strip()}", Colors.GREEN)
            
            return True
        except Exception as e:
            colored_print(f"Failed to install Claude Code: {e}", Colors.RED)
            return False

class ContextMenuManager:
    """Handles Windows context menu integration"""
    
    def __init__(self):
        self.scripts_dir = Path("C:/Scripts")
        self.launcher_path = self.scripts_dir / "open_in_claude.cmd"
    
    def is_installed(self) -> bool:
        """Check if context menu is installed"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 
                               r"Directory\Background\shell\OpenInClaude")
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False
    
    def create_launcher_script(self) -> bool:
        """Create the batch launcher script"""
        try:
            # Create Scripts directory
            self.scripts_dir.mkdir(exist_ok=True)
            
            launcher_code = '''@echo off
:: Claude Code Launcher - Batch Version
:: Converts Windows paths to WSL format and launches Claude Code

set "WINPATH=%~1"
if "%WINPATH%"=="" (
    echo ERROR: No path provided to Claude Code launcher
    echo %date% %time% - ERROR: No path provided >> "C:\\Scripts\\claude_launcher_error.log"
    pause
    exit /b 1
)

:: Log the start
echo %date% %time% - Starting Claude Code launcher > "C:\\Scripts\\claude_launcher.log"
echo %date% %time% - Windows path: %WINPATH% >> "C:\\Scripts\\claude_launcher.log"

:: Convert Windows path to WSL format manually
:: Extract drive letter and convert to lowercase
set "DRIVE=%WINPATH:~0,1%"
for %%i in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do call set "DRIVE=%%DRIVE:%%i=%%i%%"
for %%i in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do call set "DRIVE=%%DRIVE:%%i=%%i%%"

:: Get the rest of the path (everything after C:)
set "RESTPATH=%WINPATH:~2%"
:: Replace backslashes with forward slashes
set "RESTPATH=%RESTPATH:\\=/%"

:: Create WSL path
set "WSLPATH=/mnt/%DRIVE%%RESTPATH%"
echo %date% %time% - WSL path: %WSLPATH% >> "C:\\Scripts\\claude_launcher.log"

:: Get folder name for window title
for %%f in ("%WINPATH%") do set "FOLDERNAME=%%~nxf"
if "%FOLDERNAME%"=="" set "FOLDERNAME=Root"

:: Launch Claude Code
echo %date% %time% - Launching Claude Code... >> "C:\\Scripts\\claude_launcher.log"

:: Try Windows Terminal first
wt new-tab --title "Claude Code - %FOLDERNAME%" wsl -d Ubuntu --cd "%WSLPATH%" bash -lic "claude" 2>nul
if %ERRORLEVEL%==0 (
    echo %date% %time% - Windows Terminal launched successfully >> "C:\\Scripts\\claude_launcher.log"
    goto :success
)

:: Fallback to regular cmd
start "Claude Code - %FOLDERNAME%" wsl -d Ubuntu --cd "%WSLPATH%" bash -lic "claude"
if %ERRORLEVEL%==0 (
    echo %date% %time% - CMD launched successfully >> "C:\\Scripts\\claude_launcher.log"
    goto :success
)

:: If we get here, something went wrong
echo %date% %time% - ERROR: Failed to launch Claude Code >> "C:\\Scripts\\claude_launcher_error.log"
pause
exit /b 1

:success
exit /b 0
'''
            
            with open(self.launcher_path, 'w', encoding='utf-8') as f:
                f.write(launcher_code)
            
            colored_print(f"Created launcher script: {self.launcher_path}", Colors.GREEN)
            return True
            
        except Exception as e:
            colored_print(f"Failed to create launcher script: {e}", Colors.RED)
            return False
    
    def install_context_menu(self) -> bool:
        """Install context menu integration"""
        try:
            colored_print("Installing context menu integration...", Colors.YELLOW)
            
            # Create launcher script first
            if not self.create_launcher_script():
                return False
            
            # Registry entries for folder background (right-click in empty space)
            bg_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 
                                    r"Directory\\Background\\shell\\OpenInClaude")
            winreg.SetValue(bg_key, "", winreg.REG_SZ, "Open in Claude Code")
            winreg.SetValueEx(bg_key, "Icon", 0, winreg.REG_SZ, 
                            "C:\\Windows\\System32\\cmd.exe,0")
            
            bg_cmd_key = winreg.CreateKey(bg_key, "command")
            winreg.SetValue(bg_cmd_key, "", winreg.REG_SZ, 
                          f'"{self.launcher_path}" "%V"')
            
            winreg.CloseKey(bg_cmd_key)
            winreg.CloseKey(bg_key)
            
            # Registry entries for folders themselves (right-click on folder)
            folder_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, 
                                        r"Directory\\shell\\OpenInClaude")
            winreg.SetValue(folder_key, "", winreg.REG_SZ, "Open in Claude Code")
            winreg.SetValueEx(folder_key, "Icon", 0, winreg.REG_SZ, 
                            "C:\\Windows\\System32\\cmd.exe,0")
            
            folder_cmd_key = winreg.CreateKey(folder_key, "command")
            winreg.SetValue(folder_cmd_key, "", winreg.REG_SZ, 
                          f'"{self.launcher_path}" "%1"')
            
            winreg.CloseKey(folder_cmd_key)
            winreg.CloseKey(folder_key)
            
            colored_print("Context menu integration installed successfully!", Colors.GREEN)
            return True
            
        except Exception as e:
            colored_print(f"Failed to install context menu: {e}", Colors.RED)
            return False
    
    def uninstall_context_menu(self) -> bool:
        """Remove context menu integration"""
        try:
            colored_print("Removing context menu integration...", Colors.YELLOW)
            
            # Remove registry entries
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 
                               r"Directory\\Background\\shell\\OpenInClaude\\command")
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 
                               r"Directory\\Background\\shell\\OpenInClaude")
            except WindowsError:
                pass  # Key might not exist
            
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 
                               r"Directory\\shell\\OpenInClaude\\command")
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, 
                               r"Directory\\shell\\OpenInClaude")
            except WindowsError:
                pass  # Key might not exist
            
            # Remove launcher script
            if self.launcher_path.exists():
                self.launcher_path.unlink()
                colored_print(f"Removed launcher script: {self.launcher_path}", Colors.GREEN)
            
            # Remove Scripts directory if empty
            try:
                if self.scripts_dir.exists() and not any(self.scripts_dir.iterdir()):
                    self.scripts_dir.rmdir()
                    colored_print("Removed empty Scripts directory", Colors.GREEN)
            except:
                pass  # Directory might not be empty
            
            colored_print("Context menu integration removed successfully!", Colors.GREEN)
            return True
            
        except Exception as e:
            colored_print(f"Failed to remove context menu: {e}", Colors.RED)
            return False

class ClaudeInstallerGUI:
    """GUI interface for Claude Code installer"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Claude Code Windows Setup")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Create managers
        self.wsl_manager = WSLManager()
        self.claude_manager = ClaudeCodeManager()
        self.context_manager = ContextMenuManager()
        
        self.setup_gui()
        self.update_status()
        
    def setup_gui(self):
        """Setup the GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Claude Code Windows Setup", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Installation Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_labels = {}
        components = ["WSL", "Ubuntu", "Claude Code", "Context Menu"]
        for i, component in enumerate(components):
            ttk.Label(status_frame, text=f"{component}:").grid(row=i, column=0, sticky=tk.W, padx=(0, 10))
            self.status_labels[component] = ttk.Label(status_frame, text="Checking...")
            self.status_labels[component].grid(row=i, column=1, sticky=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.install_btn = ttk.Button(buttons_frame, text="Install Missing", 
                                     command=self.install_everything, width=20)
        self.install_btn.grid(row=0, column=0, padx=5)
        
        self.context_btn = ttk.Button(buttons_frame, text="Context Menu Only", 
                                     command=self.install_context_only, width=20)
        self.context_btn.grid(row=0, column=1, padx=5)
        
        self.uninstall_btn = ttk.Button(buttons_frame, text="Uninstall", 
                                       command=self.uninstall, width=20)
        self.uninstall_btn.grid(row=0, column=2, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Log output
        log_frame = ttk.LabelFrame(main_frame, text="Installation Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def log_message(self, message: str):
        """Add message to log display"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_status(self):
        """Update status indicators"""
        # Add debugging info
        wsl_installed = self.wsl_manager.is_wsl_installed()
        ubuntu_installed = self.wsl_manager.is_ubuntu_installed()
        claude_installed = self.claude_manager.is_claude_installed()
        context_installed = self.context_manager.is_installed()
        
        # Log the detection results for debugging
        logger.info(f"WSL detected: {wsl_installed}")
        logger.info(f"Ubuntu detected: {ubuntu_installed}")
        logger.info(f"Claude Code detected: {claude_installed}")
        logger.info(f"Context Menu detected: {context_installed}")
        
        statuses = {
            "WSL": "✓ Installed" if wsl_installed else "✗ Not installed",
            "Ubuntu": "✓ Installed" if ubuntu_installed else "✗ Not installed", 
            "Claude Code": "✓ Installed" if claude_installed else "✗ Not installed",
            "Context Menu": "✓ Installed" if context_installed else "✗ Not installed"
        }
        
        for component, status in statuses.items():
            self.status_labels[component].config(text=status)
            if "✓" in status:
                self.status_labels[component].config(foreground="green")
            else:
                self.status_labels[component].config(foreground="red")
    
    def disable_buttons(self):
        """Disable all buttons during operations"""
        self.install_btn.config(state="disabled")
        self.context_btn.config(state="disabled")
        self.uninstall_btn.config(state="disabled")
        self.progress.start()
        
    def enable_buttons(self):
        """Enable all buttons after operations"""
        self.install_btn.config(state="normal")
        self.context_btn.config(state="normal")
        self.uninstall_btn.config(state="normal")
        self.progress.stop()
        
    def install_everything(self):
        """Install only what's missing - smart installation"""
        def install():
            try:
                self.disable_buttons()
                self.log_message("Checking what needs to be installed...")
                
                if not is_admin():
                    messagebox.showerror("Error", "Administrator privileges required!\nPlease run as Administrator.")
                    return
                
                # Check what's already installed
                wsl_installed = self.wsl_manager.is_wsl_installed()
                ubuntu_installed = self.wsl_manager.is_ubuntu_installed()
                claude_installed = self.claude_manager.is_claude_installed()
                context_installed = self.context_manager.is_installed()
                
                # Count what needs installation
                missing_components = []
                if not wsl_installed:
                    missing_components.append("WSL")
                if not ubuntu_installed:
                    missing_components.append("Ubuntu")
                if not claude_installed:
                    missing_components.append("Claude Code")
                if not context_installed:
                    missing_components.append("Context Menu")
                
                if not missing_components:
                    self.log_message("Everything is already installed!")
                    messagebox.showinfo("All Set!", "Everything is already installed!\n\nYou can right-click in any folder and select 'Open in Claude Code'.")
                    return
                
                self.log_message(f"Installing missing components: {', '.join(missing_components)}")
                
                # Install WSL if needed
                if not wsl_installed:
                    self.log_message("Installing WSL...")
                    if not self.wsl_manager.install_wsl():
                        messagebox.showerror("Error", "WSL installation failed!")
                        return
                    self.log_message("WSL installation complete. You may need to restart.")
                else:
                    self.log_message("✓ WSL already installed, skipping...")
                
                # Install Ubuntu if needed
                if not ubuntu_installed:
                    self.log_message("Installing Ubuntu...")
                    if not self.wsl_manager.install_ubuntu():
                        messagebox.showerror("Error", "Ubuntu installation failed!")
                        return
                else:
                    self.log_message("✓ Ubuntu already installed, skipping...")
                
                # Setup Ubuntu environment and install Claude Code if needed
                if not claude_installed:
                    self.log_message("Setting up Ubuntu environment for Claude Code...")
                    if not self.wsl_manager.setup_ubuntu_environment():
                        messagebox.showerror("Error", "Ubuntu setup failed!")
                        return
                    
                    self.log_message("Installing Claude Code...")
                    if not self.claude_manager.install_claude_code():
                        messagebox.showerror("Error", "Claude Code installation failed!")
                        return
                else:
                    self.log_message("✓ Claude Code already installed, skipping...")
                
                # Install context menu if needed
                if not context_installed:
                    self.log_message("Installing context menu integration...")
                    if not self.context_manager.install_context_menu():
                        messagebox.showerror("Error", "Context menu installation failed!")
                        return
                else:
                    self.log_message("✓ Context menu already installed, skipping...")
                
                self.log_message("Installation complete!")
                messagebox.showinfo("Success", f"Successfully installed: {', '.join(missing_components)}\n\nYou can now right-click in any folder and select 'Open in Claude Code'.")
                
            except Exception as e:
                self.log_message(f"Error: {e}")
                messagebox.showerror("Error", f"Installation failed: {e}")
            finally:
                self.enable_buttons()
                self.update_status()
        
        threading.Thread(target=install, daemon=True).start()
    
    def install_context_only(self):
        """Install only context menu in a separate thread"""
        def install():
            try:
                self.disable_buttons()
                self.log_message("Installing context menu integration...")
                
                if not is_admin():
                    messagebox.showerror("Error", "Administrator privileges required!\nPlease run as Administrator.")
                    return
                
                if not self.context_manager.install_context_menu():
                    messagebox.showerror("Error", "Context menu installation failed!")
                    return
                
                self.log_message("Context menu installation complete!")
                messagebox.showinfo("Success", "Context menu installed successfully!\n\nYou can now right-click in any folder and select 'Open in Claude Code'.")
                
            except Exception as e:
                self.log_message(f"Error: {e}")
                messagebox.showerror("Error", f"Installation failed: {e}")
            finally:
                self.enable_buttons()
                self.update_status()
        
        threading.Thread(target=install, daemon=True).start()
    
    def uninstall(self):
        """Uninstall context menu in a separate thread"""
        def uninstall():
            try:
                self.disable_buttons()
                self.log_message("Uninstalling context menu integration...")
                
                if not is_admin():
                    messagebox.showerror("Error", "Administrator privileges required!\nPlease run as Administrator.")
                    return
                
                if not self.context_manager.uninstall_context_menu():
                    messagebox.showerror("Error", "Uninstallation failed!")
                    return
                
                self.log_message("Uninstallation complete!")
                messagebox.showinfo("Success", "Context menu uninstalled successfully!")
                
            except Exception as e:
                self.log_message(f"Error: {e}")
                messagebox.showerror("Error", f"Uninstallation failed: {e}")
            finally:
                self.enable_buttons()
                self.update_status()
        
        threading.Thread(target=uninstall, daemon=True).start()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

class ClaudeInstaller:
    """Main installer class for command line usage"""
    
    def __init__(self):
        self.wsl_manager = WSLManager()
        self.claude_manager = ClaudeCodeManager()
        self.context_manager = ContextMenuManager()
    
    def check_prerequisites(self) -> bool:
        """Check system prerequisites"""
        colored_print("Checking system prerequisites...", Colors.CYAN)
        
        # Check if running as admin
        if not is_admin():
            colored_print("ERROR: This installer must be run as Administrator!", Colors.RED)
            colored_print("Please run this script as Administrator and try again.", Colors.RED)
            return False
        
        colored_print("✓ Administrator privileges confirmed", Colors.GREEN)
        
        # Check Python version
        if sys.version_info < (3, 6):
            colored_print("ERROR: Python 3.6 or higher is required!", Colors.RED)
            return False
        
        colored_print(f"✓ Python {sys.version.split()[0]} detected", Colors.GREEN)
        
        # Check Windows version (Windows 10 build 18362 or higher for WSL2)
        try:
            import platform
            win_version = platform.version()
            colored_print(f"✓ Windows version: {win_version}", Colors.GREEN)
        except:
            colored_print("Warning: Could not detect Windows version", Colors.YELLOW)
        
        return True
    
    def install_full(self) -> bool:
        """Perform full installation"""
        colored_print("=" * 60, Colors.MAGENTA)
        colored_print("    Claude Code Windows Installer", Colors.MAGENTA)
        colored_print("=" * 60, Colors.MAGENTA)
        
        if not self.check_prerequisites():
            return False
        
        # Install WSL if needed
        if not self.wsl_manager.is_wsl_installed():
            colored_print("WSL not found. Installing WSL...", Colors.YELLOW)
            if not self.wsl_manager.install_wsl():
                return False
            colored_print("WSL installation complete. A restart may be required.", Colors.YELLOW)
            
            restart = input("Do you need to restart your computer now? (y/n): ").lower()
            if restart in ['y', 'yes']:
                colored_print("Please restart your computer and run this installer again.", Colors.YELLOW)
                return False
        else:
            colored_print("✓ WSL is already installed", Colors.GREEN)
        
        # Install Ubuntu if needed
        if not self.wsl_manager.is_ubuntu_installed():
            colored_print("Ubuntu not found. Installing Ubuntu...", Colors.YELLOW)
            if not self.wsl_manager.install_ubuntu():
                return False
        else:
            colored_print("✓ Ubuntu is already installed", Colors.GREEN)
        
        # Setup Ubuntu environment (skip if Claude Code is already installed)
        if self.claude_manager.is_claude_installed():
            colored_print("✓ Claude Code already installed, skipping Ubuntu environment setup", Colors.GREEN)
        else:
            colored_print("Setting up Ubuntu environment for Claude Code installation...", Colors.YELLOW)
            if not self.wsl_manager.setup_ubuntu_environment():
                return False
        
        # Install Claude Code
        if not self.claude_manager.is_claude_installed():
            if not self.claude_manager.install_claude_code():
                return False
        else:
            colored_print("✓ Claude Code is already installed", Colors.GREEN)
        
        # Install context menu
        if not self.context_manager.is_installed():
            if not self.context_manager.install_context_menu():
                return False
        else:
            colored_print("✓ Context menu is already installed", Colors.GREEN)
            update = input("Do you want to update the existing installation? (y/n): ").lower()
            if update in ['y', 'yes']:
                self.context_manager.uninstall_context_menu()
                self.context_manager.install_context_menu()
        
        self.show_success_message()
        return True
    
    def install_context_menu_only(self) -> bool:
        """Install only the context menu integration"""
        colored_print("Installing Claude Code context menu integration...", Colors.CYAN)
        
        if not self.check_prerequisites():
            return False
        
        # Check if Claude Code is installed
        if not self.claude_manager.is_claude_installed():
            colored_print("WARNING: Claude Code not found in WSL Ubuntu!", Colors.YELLOW)
            colored_print("Make sure you have WSL, Ubuntu, and Claude Code installed first.", Colors.YELLOW)
            
            continue_anyway = input("Do you want to continue anyway? (y/n): ").lower()
            if continue_anyway not in ['y', 'yes']:
                return False
        
        return self.context_manager.install_context_menu()
    
    def uninstall(self) -> bool:
        """Uninstall context menu integration"""
        colored_print("Uninstalling Claude Code context menu...", Colors.CYAN)
        
        if not self.check_prerequisites():
            return False
        
        if not self.context_manager.is_installed():
            colored_print("✓ Claude Code context menu is not installed", Colors.GREEN)
            return True
        
        return self.context_manager.uninstall_context_menu()
    
    def show_status(self) -> None:
        """Show installation status"""
        colored_print("=" * 60, Colors.CYAN)
        colored_print("    Claude Code Installation Status", Colors.CYAN)
        colored_print("=" * 60, Colors.CYAN)
        
        # WSL Status with debugging
        wsl_installed = self.wsl_manager.is_wsl_installed()
        wsl_status = "✓ Installed" if wsl_installed else "✗ Not installed"
        colored_print(f"WSL: {wsl_status}", Colors.GREEN if "✓" in wsl_status else Colors.RED)
        
        # Ubuntu Status with debugging  
        ubuntu_installed = self.wsl_manager.is_ubuntu_installed()
        ubuntu_status = "✓ Installed" if ubuntu_installed else "✗ Not installed"
        colored_print(f"Ubuntu: {ubuntu_status}", Colors.GREEN if "✓" in ubuntu_status else Colors.RED)
        
        # If Ubuntu not detected, show debug info
        if not ubuntu_installed:
            try:
                result = run_command(['wsl', '-l', '-v'], check=False)
                clean_output = result.stdout.replace('\x00', '').strip()
                colored_print(f"Debug - WSL list raw output: {repr(result.stdout)}", Colors.YELLOW)
                colored_print(f"Debug - WSL list cleaned output: '{clean_output}'", Colors.YELLOW)
                colored_print(f"Debug - Return code: {result.returncode}", Colors.YELLOW)
                colored_print(f"Debug - Looking for 'ubuntu' in: '{clean_output.lower()}'", Colors.YELLOW)
            except Exception as e:
                colored_print(f"Debug - WSL list command failed: {e}", Colors.RED)
        
        # Claude Code Status
        claude_status = "✓ Installed" if self.claude_manager.is_claude_installed() else "✗ Not installed"
        colored_print(f"Claude Code: {claude_status}", Colors.GREEN if "✓" in claude_status else Colors.RED)
        
        # Context Menu Status
        context_status = "✓ Installed" if self.context_manager.is_installed() else "✗ Not installed"
        colored_print(f"Context Menu: {context_status}", Colors.GREEN if "✓" in context_status else Colors.RED)
    
    def show_success_message(self) -> None:
        """Show installation success message"""
        colored_print("=" * 60, Colors.GREEN)
        colored_print("         Installation Complete!", Colors.GREEN)
        colored_print("=" * 60, Colors.GREEN)
        
        colored_print("\\nHow to use:", Colors.CYAN)
        colored_print("1. Open Windows Explorer", Colors.WHITE)
        colored_print("2. Navigate to any folder", Colors.WHITE)
        colored_print("3. Right-click in the folder (empty space)", Colors.WHITE)
        colored_print("4. Select 'Open in Claude Code'", Colors.WHITE)
        colored_print("5. Claude Code will launch in that directory!", Colors.WHITE)
        
        colored_print("\\nAlternative usage:", Colors.CYAN)
        colored_print("• Open WSL Ubuntu terminal: type 'ubuntu'", Colors.WHITE)
        colored_print("• Navigate to your project: cd /mnt/c/your/project/path", Colors.WHITE)
        colored_print("• Start Claude Code: claude", Colors.WHITE)
        
        colored_print("\\nFor more info: https://docs.anthropic.com/en/docs/claude-code/setup", Colors.CYAN)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Claude Code Windows Installer")
    parser.add_argument('--context-only', action='store_true',
                       help='Install only the context menu integration')
    parser.add_argument('--uninstall', action='store_true',
                       help='Uninstall the context menu integration')
    parser.add_argument('--status', action='store_true',
                       help='Show installation status')
    parser.add_argument('--gui', action='store_true',
                       help='Launch GUI interface')
    parser.add_argument('--console', action='store_true',
                       help='Force console mode')
    
    args = parser.parse_args()
    
    # If no arguments provided and running interactively, launch GUI
    if len(sys.argv) == 1 and not args.console:
        try:
            gui = ClaudeInstallerGUI()
            gui.run()
            return
        except Exception as e:
            print(f"GUI failed to start: {e}")
            print("Falling back to console mode...")
    
    # Console mode
    installer = ClaudeInstaller()
    
    try:
        if args.status:
            installer.show_status()
        elif args.uninstall:
            success = installer.uninstall()
            sys.exit(0 if success else 1)
        elif args.context_only:
            success = installer.install_context_menu_only()
            sys.exit(0 if success else 1)
        elif args.gui:
            gui = ClaudeInstallerGUI()
            gui.run()
        else:
            success = installer.install_full()
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        colored_print("\\nInstallation cancelled by user.", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        colored_print(f"\\nUnexpected error: {e}", Colors.RED)
        logger.exception("Unexpected error occurred")
        sys.exit(1)

if __name__ == "__main__":
    main() 
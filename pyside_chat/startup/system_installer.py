import shutil
import subprocess
import ctypes

# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def offer_add_espeak_to_path():
    espeak_path = shutil.which("espeak-ng")
    if espeak_path:
        print(f"espeak-ng found at: {espeak_path}")
        return
    possible_path = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
    dir_path = r"C:\Program Files\eSpeak NG"
    if os.path.exists(possible_path):
        print("espeak-ng was installed, but is not in your system PATH.")
        answer = input("Would you like to add it to your PATH automatically? (Y/n): ").strip().lower()
        if answer in ("", "y", "yes"):
            print("Adding to system PATH (admin rights required)...")
            result = subprocess.run([
                "powershell", "-Command",
                f"[Environment]::SetEnvironmentVariable('Path', $env:Path + ';{dir_path}', [System.EnvironmentVariableTarget]::Machine)"
            ], capture_output=True, text=True)
            print("PowerShell output (stdout):", result.stdout)
            print("PowerShell output (stderr):", result.stderr)
            print("Added to PATH. You may need to restart your computer or log out and back in for changes to take effect.")
        else:
            print(f"Please add '{dir_path}' to your system PATH manually.")
    else:
        print("espeak-ng not found in PATH or at the default install location. Please install or add to PATH manually.")

def ensure_system_dependencies():
    if sys.platform == "win32":
        # Check if espeak-ng is already available
        if shutil.which("espeak-ng") is not None:
            print("espeak-ng found in PATH.")
            offer_add_espeak_to_path()
            return
            
        # Check if it's installed but not in PATH
        possible_path = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
        if os.path.exists(possible_path):
            print("espeak-ng found at default location but not in PATH.")
            offer_add_espeak_to_path()
            return
            
        # Try to install via Chocolatey if available
        if shutil.which("choco") is not None:
            print("Chocolatey found. Installing espeak-ng via Chocolatey...")
            try:
                subprocess.run([
                    "powershell", "-Command",
                    "choco install espeak-ng -y"
                ], check=True)
                print("espeak-ng installed via Chocolatey.")
                offer_add_espeak_to_path()
                return
            except subprocess.CalledProcessError:
                print("Failed to install espeak-ng via Chocolatey.")
        
        # If Chocolatey is not available, provide manual instructions
        print("\n=== espeak-ng Installation Required ===")
        print("espeak-ng is needed for text-to-speech functionality.")
        print("\nYou have several options to install it:")
        print("\nOption 1: Install Chocolatey first (recommended)")
        print("1. Open PowerShell as Administrator")
        print("2. Run: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
        print("3. Close and reopen PowerShell")
        print("4. Run: choco install espeak-ng -y")
        print("5. Restart your terminal/computer")
        print("6. Run this script again")
        
        print("\nOption 2: Manual download")
        print("1. Download espeak-ng from: https://github.com/espeak-ng/espeak-ng/releases")
        print("2. Extract to C:\\Program Files\\eSpeak NG\\")
        print("3. Add C:\\Program Files\\eSpeak NG\\ to your system PATH")
        print("4. Restart your terminal/computer")
        print("5. Run this script again")
        
        print("\nOption 3: Skip for now")
        print("You can continue without espeak-ng, but text-to-speech will not work.")
        
        answer = input("\nWould you like to try installing Chocolatey now? (y/N): ").strip().lower()
        if answer in ("y", "yes"):
            if not is_admin():
                print("This requires administrator privileges.")
                print("Please run PowerShell as Administrator and execute:")
                print("Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
                print("Then restart your terminal and run this script again.")
            else:
                print("Installing Chocolatey...")
                try:
                    result = subprocess.run([
                        "powershell", "-Command",
                        "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                        "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                        "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
                    ], capture_output=True, text=True)
                    print("Chocolatey installation output:", result.stdout)
                    if result.stderr:
                        print("Chocolatey installation errors:", result.stderr)
                    print("Please restart your terminal and run this script again.")
                except Exception as e:
                    print(f"Chocolatey installation failed: {e}")
                    print("Please follow the manual installation instructions above.")
        else:
            print("Skipping espeak-ng installation. Text-to-speech will not be available.")
            print("You can install it later and run this script again.") 
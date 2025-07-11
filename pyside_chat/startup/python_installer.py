import subprocess
import sys
import os

def install_python_requirements(requirements_path=None):
    # If no path provided, look in the same directory as this script
    if requirements_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print(f"ERROR: requirements file not found: {requirements_path}")
        sys.exit(1)
    print(f"Installing Python dependencies from {requirements_path}...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_path
        ], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            print("ERROR: Failed to install some Python dependencies.")
            sys.exit(result.returncode)
        print("All Python dependencies installed successfully.")
    except Exception as e:
        print(f"ERROR: Exception during pip install: {e}")
        sys.exit(1) 
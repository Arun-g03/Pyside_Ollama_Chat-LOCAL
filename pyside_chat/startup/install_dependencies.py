#!/usr/bin/env python3
# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *


"""
PySide Chat System - Dependency Installation Script

This script installs all required dependencies in stages with proper error handling, progress feedback, and the ability to resume from where it left off if there's an error.
"""

import subprocess
from typing import List, Dict, Tuple, Optional
import shutil
import ctypes

from pyside_chat.startup.system_installer import ensure_system_dependencies
from pyside_chat.startup.python_installer import install_python_requirements


def main():
    print("=== PySide Chat System - Dependency Installation ===")
    ensure_system_dependencies()
    install_python_requirements()  # Let it find requirements.txt automatically
    print("\nAll dependencies installed. You can now run: python main.py")

if __name__ == "__main__":
    main() 
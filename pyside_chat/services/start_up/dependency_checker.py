#!/usr/bin/env python3
"""
Dependency Checker Module

This module provides dependency checking functionality that can be imported
by main.py to verify all required dependencies are available before starting
the application.
"""

import subprocess
import sys
import importlib
import os
from typing import List, Dict, Tuple, Optional

class DependencyChecker:
    """Handles dependency checking and installation."""
    
    def __init__(self):
        self.broken_imports = []
        self.working_imports = []
        self.version_conflicts = []
        self.optional_broken = []  # Track optional dependencies that failed
        
    def test_import(self, module_name: str, description: str) -> Tuple[bool, str, str]:
        """Test if a module can be imported successfully and return version."""
        try:
            module = importlib.import_module(module_name)
            # Try to get version from common attributes
            version = "unknown"
            for attr in ['__version__', 'VERSION', 'version']:
                if hasattr(module, attr):
                    version = str(getattr(module, attr))
                    break
            return True, "Working", version
        except ImportError as e:
            return False, f"Import Error: {e}", "not installed"
        except Exception as e:
            return False, f"Runtime Error: {e}", "error"
    
    def check_core_dependencies(self):
        """Check core application dependencies."""
        # Critical dependencies - app cannot start without these
        critical_modules = [
            ("tqdm", "Progress Bars"),
            ("PySide6", "GUI Framework"),
            ("requests", "HTTP Client"),
            ("pygments", "Syntax Highlighting"),
        ]
        
        # Optional core dependencies - app can start without these
        optional_core_modules = [
            ("edge_tts", "Edge TTS"),
    
            ("pyttsx3", "Local TTS"),
            ("pygame", "Audio Playback"),
            ("keyboard", "Keyboard Input"),
            ("pyenchant", "Spellchecker"),
            ("numpy", "Numerical Computing"),
            ("scipy", "Scientific Computing"),
            ("librosa", "Audio Processing"),
            ("soundfile", "Audio File I/O"),
            ("pydub", "Audio Manipulation")
        ]
        
        # Check critical dependencies
        for module, description in critical_modules:
            success, status, version = self.test_import(module, description)
            if success:
                self.working_imports.append(f"{module} ({version})")
            else:
                self.broken_imports.append(f"{module} ({version})")
        
        # Check optional core dependencies
        for module, description in optional_core_modules:
            success, status, version = self.test_import(module, description)
            if success:
                self.working_imports.append(f"{module} ({version})")
            else:
                self.optional_broken.append(f"{module} ({version})")
    
    def check_ml_dependencies(self):
        """Check machine learning dependencies (all optional)."""
        ml_modules = [
            ("torch", "PyTorch"),
            ("torchaudio", "PyTorch Audio"),
            ("sklearn", "Scikit-learn"),
            ("huggingface_hub", "Hugging Face Hub"),
            ("transformers", "Transformers"),
            ("sentence_transformers", "Sentence Transformers"),
            ("TTS", "Coqui TTS")
        ]
        
        for module, description in ml_modules:
            success, status, version = self.test_import(module, description)
            if success:
                self.working_imports.append(f"{module} ({version})")
            else:
                self.optional_broken.append(f"{module} ({version})")
    
    def check_tts_options(self):
        """Check if at least one TTS option is available."""
        tts_options = ["edge_tts", "gtts", "pyttsx3", "TTS"]
        tts_available = False
        
        for tts in tts_options:
            success, _, version = self.test_import(tts, "")
            if success:
                tts_available = True
                # Don't add to working_imports again if already added in core_dependencies
                if f"{tts} ({version})" not in self.working_imports:
                    self.working_imports.append(f"{tts} ({version})")
        
        if not tts_available:
            self.optional_broken.append("No TTS options available")
    
    def check_package_versions(self):
        """Check for version conflicts."""
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "list"
            ], capture_output=True, text=True, check=True, timeout=60)
            
            packages = result.stdout.strip().split('\n')[2:]  # Skip header
            version_info = {}
            
            for line in packages:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        package = parts[0].lower()
                        version = parts[1]
                        version_info[package] = version
            
            # Check for potential conflicts
            expected_versions = {
                'huggingface-hub': '0.20.3',
                'transformers': '4.35.2',
                'sentence-transformers': '2.2.2',
                'accelerate': '0.25.0'
            }
            
            for package, expected_version in expected_versions.items():
                if package in version_info:
                    actual_version = version_info[package]
                    if actual_version != expected_version:
                        conflict = f"{package}: {actual_version} (expected {expected_version})"
                        self.version_conflicts.append(conflict)
                        
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # If we can't check versions, assume no conflicts
            pass
    
    def run_comprehensive_check(self) -> bool:
        """Run the complete dependency check and return if fixes are needed."""
        self.check_core_dependencies()
        self.check_ml_dependencies()
        self.check_tts_options()
        self.check_package_versions()
        
        # Only critical dependencies block startup
        needs_fixing = len(self.broken_imports) > 0
        return needs_fixing
    
    def get_missing_dependencies(self) -> List[str]:
        """Get list of missing dependencies."""
        return self.broken_imports.copy()
    
    def get_version_conflicts(self) -> List[str]:
        """Get list of version conflicts."""
        return self.version_conflicts.copy()
    
    def run_install_dependencies(self) -> bool:
        """Run the install_dependencies.py script."""
        try:
            # Get the directory of the current script (now in pyside_chat/services/start_up/)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            install_script = os.path.join(current_dir, "install_dependencies.py")
            
            if not os.path.exists(install_script):
                print(f"[ID:0312] Error: install_dependencies.py not found at {install_script}")
                return False
            
            print("[ID:0311] Installing dependencies...")
            result = subprocess.run([
                sys.executable, install_script
            ], capture_output=False, text=True, check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[ID:0310] Failed to install dependencies: {e}")
            return False
        except Exception as e:
            print(f"[ID:0309] Error installing dependencies: {e}")
            return False
    
    def get_dependency_summary(self) -> str:
        """Get a concise summary of dependency status."""
        summary = f"Working: {len(self.working_imports)}, Broken: {len(self.broken_imports)}"
        if self.version_conflicts:
            summary += f", Version conflicts: {len(self.version_conflicts)}"
        return summary


def check_and_install_dependencies(auto_install: bool = True, verbose: bool = False) -> bool:
    """
    Check dependencies and optionally install missing ones.
    
    Args:
        auto_install: If True, automatically run install_dependencies.py if issues found
        verbose: If True, print detailed output
        
    Returns:
        True if all dependencies are working, False otherwise
    """
    if verbose:
        print("[ID:0308] Checking dependencies...")
    
    checker = DependencyChecker()
    needs_fixing = checker.run_comprehensive_check()
    
    if not needs_fixing:
        if verbose:
            print("[ID:0307] All dependencies are working correctly!")
        return True
    
    if verbose:
        print(f"[ID:0306] Dependency issues found: {checker.get_dependency_summary()}")
        if checker.broken_imports:
            print(f"[ID:0305] Missing: {', '.join(checker.broken_imports)}")
        if checker.version_conflicts:
            print(f"[ID:0304] Version conflicts: {len(checker.version_conflicts)}")
    
    if auto_install:
        if verbose:
            print("[ID:0303] Installing missing dependencies...")
        success = checker.run_install_dependencies()
        
        if success:
            if verbose:
                print("[ID:0302] Re-checking dependencies...")
            # Re-check after installation
            checker2 = DependencyChecker()
            final_check = checker2.run_comprehensive_check()
            
            if not final_check:
                if verbose:
                    print("[ID:0301] All dependencies are now working!")
                return True
            else:
                if verbose:
                    print("[ID:0300] Some dependencies may still have issues")
                return False
        else:
            if verbose:
                print("[ID:0299] Failed to install dependencies automatically")
            return False
    else:
        if verbose:
            print("[ID:0298] Run 'python pyside_chat/services/start_up/install_dependencies.py' to install missing dependencies")
        return False


if __name__ == "__main__":
    # Test the dependency checker
    print("[ID:0297] 🔍 Testing Dependency Checker...")
    checker = DependencyChecker()
    needs_fixing = checker.run_comprehensive_check()
    
    print(f"[ID:0296] \nWorking imports ({len(checker.working_imports)}):")
    for imp in checker.working_imports:
        print(f"[ID:0295] ✅ {imp}")
    
    print(f"[ID:0294] \nCritical broken imports ({len(checker.broken_imports)}):")
    for imp in checker.broken_imports:
        print(f"[ID:0293] ❌ {imp}")
    
    print(f"[ID:0292] \nOptional broken imports ({len(checker.optional_broken)}):")
    for imp in checker.optional_broken:
        print(f"[ID:0291] ⚠️  {imp}")
    
    print(f"[ID:0290] \nVersion conflicts ({len(checker.version_conflicts)}):")
    for conflict in checker.version_conflicts:
        print(f"[ID:0289] ⚠️  {conflict}")
    
    print(f"[ID:0288] \nOverall status: {'✅ All good' if not needs_fixing else '❌ Needs fixing'}")
    print(f"[ID:0287] Can start application: {'✅ Yes' if not needs_fixing else '❌ No'}")
    if checker.optional_broken:
        print(f"[ID:0286] Note: {len(checker.optional_broken)} optional features unavailable")

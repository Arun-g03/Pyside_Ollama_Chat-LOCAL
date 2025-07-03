#!/usr/bin/env python3
"""
Comprehensive Dependency Checker and Fixer

This script checks all dependencies, identifies issues, and provides
an option to automatically fix them.
"""

import subprocess
import sys
import importlib
import time
import os
from typing import List, Dict, Tuple, Optional

# Try to import tqdm for progress bars, fallback to simple progress if not available
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Note: tqdm not available, using simple progress display")

class DependencyManager:
    def __init__(self):
        self.broken_imports = []
        self.working_imports = []
        self.version_conflicts = []
        self.fix_commands = []
        
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
    
    def run_pip_command(self, command: str, description: str) -> bool:
        """Run a pip command with better error handling."""
        print(f"Running: {command}")
        try:
            result = subprocess.run(
                command.split(), 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=300  # 5 minute timeout
            )
            print("Success")
            return True
        except subprocess.TimeoutExpired:
            print("Timeout - command took too long")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Failed: {e}")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    def check_core_dependencies(self):
        """Check core application dependencies."""
        print("Checking Core Dependencies...")
        print("=" * 40)
        
        core_modules = [
            ("tqdm", "Progress Bars"),
            ("PySide6", "GUI Framework"),
            ("requests", "HTTP Client"),
            ("pygments", "Syntax Highlighting"),
            ("edge_tts", "Edge TTS"),
            ("gtts", "Google TTS"),
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
        
        if TQDM_AVAILABLE:
            with tqdm(core_modules, desc="Core Dependencies", unit="module") as pbar:
                for module, description in pbar:
                    pbar.set_description(f"Checking {module}")
                    success, status, version = self.test_import(module, description)
                    if success:
                        self.working_imports.append(f"{module} ({version})")
                    else:
                        self.broken_imports.append(f"{module} ({version})")
        else:
            for module, description in core_modules:
                success, status, version = self.test_import(module, description)
                status_icon = "✓" if success else "✗"
                print(f"  {status_icon} {module:<15} ({description:<20}) - {status} [{version}]")
                
                if success:
                    self.working_imports.append(f"{module} ({version})")
                else:
                    self.broken_imports.append(f"{module} ({version})")
    
    def check_ml_dependencies(self):
        """Check machine learning dependencies."""
        print("\nChecking ML Dependencies...")
        print("=" * 40)
        
        ml_modules = [
            ("torch", "PyTorch"),
            ("torchaudio", "PyTorch Audio"),
            ("sklearn", "Scikit-learn"),
            ("huggingface_hub", "Hugging Face Hub"),
            ("transformers", "Transformers"),
            ("sentence_transformers", "Sentence Transformers"),
            ("TTS", "Coqui TTS")
        ]
        
        if TQDM_AVAILABLE:
            with tqdm(ml_modules, desc="ML Dependencies", unit="module") as pbar:
                for module, description in pbar:
                    pbar.set_description(f"Checking {module}")
                    success, status, version = self.test_import(module, description)
                    if success:
                        self.working_imports.append(f"{module} ({version})")
                    else:
                        self.broken_imports.append(f"{module} ({version})")
        else:
            for module, description in ml_modules:
                success, status, version = self.test_import(module, description)
                status_icon = "✓" if success else "✗"
                print(f"  {status_icon} {module:<20} ({description:<20}) - {status} [{version}]")
                
                if success:
                    self.working_imports.append(f"{module} ({version})")
                else:
                    self.broken_imports.append(f"{module} ({version})")
    
    def check_package_versions(self):
        """Check for version conflicts."""
        print("\nChecking Package Versions...")
        print("=" * 40)
        
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
                        print(f"  ✗ {conflict}")
                    else:
                        print(f"  ✓ {package}: {actual_version}")
                else:
                    print(f"  ? {package}: Not installed")
            
            # Check blis and thinc (Coqui TTS dependencies)
            for package in ['blis', 'thinc']:
                if package in version_info:
                    print(f"  ✓ {package}: {version_info[package]}")
                else:
                    print(f"  ? {package}: Not installed")
                    
        except subprocess.CalledProcessError as e:
            print(f"Error checking package versions: {e}")
        except subprocess.TimeoutExpired:
            print("Timeout checking package versions")
    
    def generate_fix_plan(self):
        """Generate a comprehensive fix plan."""
        print("\nGenerating Fix Plan...")
        print("=" * 40)
        
        if not self.broken_imports and not self.version_conflicts:
            print("No issues found - all dependencies are working correctly!")
            return []
        
        fix_steps = []
        
        # Check for numpy binary incompatibility issues
        numpy_issues = any(module in self.broken_imports for module in ['sklearn', 'sentence_transformers'])
        
        # Step 1: Aggressive fix for numpy binary incompatibility
        if numpy_issues:
            fix_steps.append({
                'step': 1,
                'description': 'Fix numpy binary incompatibility',
                'commands': [
                    "pip uninstall numpy scipy scikit-learn sentence-transformers transformers huggingface-hub -y",
                    "pip install numpy==1.24.3 --force-reinstall",
                    "pip install scipy==1.10.1 --force-reinstall",
                    "pip install scikit-learn==1.3.0 --only-binary=all --force-reinstall"
                ]
            })
        
        # Step 2: Install missing packages (excluding those handled in step 1)
        missing_packages = []
        for module_with_version in self.broken_imports:
            # Extract module name from "module (version)" format
            module = module_with_version.split(" (")[0]
            
            if module == "pyenchant":
                # Try pyenchant with specific version for Windows compatibility
                missing_packages.append("pyenchant==3.2.2")
            elif module == "torch":
                missing_packages.append("torch torchaudio --index-url https://download.pytorch.org/whl/cpu")
            elif module not in ['sklearn', 'sentence_transformers']:  # Skip if handled in step 1
                missing_packages.append(module)
        
        if missing_packages:
            fix_steps.append({
                'step': len(fix_steps) + 1,
                'description': 'Install missing packages',
                'commands': [f"pip install {pkg}" for pkg in missing_packages]
            })
        
        # Step 3: Fix version conflicts with more aggressive approach
        if self.version_conflicts:
            fix_steps.append({
                'step': len(fix_steps) + 1,
                'description': 'Fix version conflicts (aggressive)',
                'commands': [
                    "pip uninstall huggingface-hub transformers sentence-transformers accelerate -y",
                    "pip install huggingface-hub==0.20.3 --no-deps",
                    "pip install transformers==4.35.2 --no-deps",
                    "pip install accelerate==0.25.0 --no-deps",
                    "pip install sentence-transformers==2.2.2 --no-deps"
                ]
            })
        
        # Step 4: Special pyenchant fix if still failing
        if any("pyenchant" in module for module in self.broken_imports):
            fix_steps.append({
                'step': len(fix_steps) + 1,
                'description': 'Special pyenchant fix for Windows',
                'commands': [
                    "pip uninstall pyenchant -y",
                    "pip install pyenchant==3.2.2 --no-deps",
                    "pip install pypiwin32"
                ]
            })
        
        # Step 5: Comprehensive fix if still having issues
        if len(self.broken_imports) > 2 or len(self.version_conflicts) > 1:
            fix_steps.append({
                'step': len(fix_steps) + 1,
                'description': 'Comprehensive dependency restoration',
                'commands': [
                    "pip uninstall sentence-transformers transformers huggingface-hub torch torchaudio scikit-learn numpy scipy -y",
                    "pip install numpy==1.24.3",
                    "pip install scipy==1.10.1", 
                    "pip install scikit-learn==1.3.0 --only-binary=all",
                    "pip install torch==2.0.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu",
                    "pip install huggingface-hub==0.20.3",
                    "pip install transformers==4.35.2",
                    "pip install accelerate==0.25.0",
                    "pip install sentence-transformers==2.2.2"
                ]
            })
        
        return fix_steps
    
    def execute_fix_plan(self, fix_steps: List[Dict]):
        """Execute the fix plan."""
        print("\nExecuting Fix Plan...")
        print("=" * 40)
        
        total_steps = sum(len(step['commands']) for step in fix_steps)
        current_step = 0
        
        for step_info in fix_steps:
            print(f"\nStep {step_info['step']}: {step_info['description']}")
            print("-" * 30)
            
            if TQDM_AVAILABLE:
                with tqdm(step_info['commands'], desc=f"Step {step_info['step']}", unit="cmd") as pbar:
                    for command in pbar:
                        current_step += 1
                        pbar.set_description(f"Running: {command.split()[1] if len(command.split()) > 1 else command}")
                        
                        success = self.run_pip_command(command, command)
                        if not success:
                            print(f"Warning: {command} failed, continuing...")
                        
                        time.sleep(0.5)  # Brief pause between commands
            else:
                for command in step_info['commands']:
                    current_step += 1
                    print(f"[{current_step}/{total_steps}] ", end="")
                    
                    success = self.run_pip_command(command, command)
                    if not success:
                        print(f"Warning: {command} failed, continuing...")
                    
                    time.sleep(0.5)  # Brief pause between commands
    
    def run_comprehensive_check(self) -> bool:
        """Run the complete dependency check and return if fixes are needed."""
        print("Comprehensive Dependency Check")
        print("=" * 50)
        print("Analyzing all dependencies...")
        print()
        
        self.check_core_dependencies()
        self.check_ml_dependencies()
        self.check_package_versions()
        
        # Generate report
        print(f"\nSUMMARY:")
        print(f"  Working: {len(self.working_imports)} packages")
        print(f"  Broken: {len(self.broken_imports)} packages")
        print(f"  Version conflicts: {len(self.version_conflicts)} issues")
        
        if self.broken_imports:
            print(f"\nBroken packages: {', '.join(self.broken_imports)}")
        
        if self.version_conflicts:
            print(f"\nVersion conflicts:")
            for conflict in self.version_conflicts:
                print(f"  - {conflict}")
        
        needs_fixing = len(self.broken_imports) > 0 or len(self.version_conflicts) > 0
        
        if needs_fixing:
            fix_steps = self.generate_fix_plan()
            if fix_steps:
                print(f"\nFix plan generated with {len(fix_steps)} steps")
                return True
        
        return False

def main():
    print("PySide Chat Dependency Manager")
    print("=" * 40)
    
    manager = DependencyManager()
    needs_fixing = manager.run_comprehensive_check()
    
    if needs_fixing:
        fix_steps = manager.generate_fix_plan()
        
        print(f"\nWould you like to automatically fix these issues? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response in ['y', 'yes']:
                print(f"\nStarting automatic fix process...")
                manager.execute_fix_plan(fix_steps)
                
                print(f"\nRe-running dependency check...")
                print("=" * 30)
                
                # Re-check after fixes
                manager2 = DependencyManager()
                final_check = manager2.run_comprehensive_check()
                
                if not final_check:
                    print(f"\nAll issues resolved successfully!")
                    print("You can now run: python main.py")
                else:
                    print(f"\nSome issues may still remain")
                    print("Consider running this script again or manual intervention")
            else:
                print(f"\nNo fixes applied. You can run this script again later.")
        except KeyboardInterrupt:
            print(f"\nOperation cancelled by user.")
    else:
        print(f"\nAll dependencies are working correctly!")
        print("You can now run: python main.py")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
PySide Chat Application Packager

This script packages the PySide Chat application into a distributable format.
Supports multiple packaging options: PyInstaller, cx_Freeze, and simple distribution.
"""

# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.pyside_imports import *

from pyside_chat.core.shared_imports.shared_imports import *



class AppPackager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.main_script = self.project_root / "main.py"
        self.app_name = "PySide_Chat"
        self.version = "1.0.0"
        self.author = "PySide Chat Team"
        
        # Packaging options
        self.packagers = {
            "briefcase": self.package_with_briefcase,
            "pyinstaller": self.package_with_pyinstaller,
            "cx_freeze": self.package_with_cx_freeze,
            "dist": self.create_distribution,
            "all": self.package_all
        }
    
    def check_dependencies(self) -> bool:
        """Check if required packaging dependencies are installed."""
        print("🔍 Checking packaging dependencies...")
        
        required_packages = {
            "briefcase": "briefcase",
            "pyinstaller": "PyInstaller",
            "cx_freeze": "cx_Freeze", 
            "setuptools": "setuptools"
        }
        
        missing_packages = []
        
        for package, import_name in required_packages.items():
            try:
                __import__(import_name)
                print(f"  ✅ {package}")
            except ImportError:
                print(f"  ❌ {package} - not installed")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n📦 Installing missing packages...")
            for package in missing_packages:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                 check=True, capture_output=True)
                    print(f"  ✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"  ❌ Failed to install {package}")
                    return False
        
        return True
    
    def create_briefcase_config(self) -> str:
        """Create a Briefcase configuration file (pyproject.toml)."""
        config_content = f'''[tool.briefcase]
project_name = "{self.app_name}"
bundle = "com.example"
version = "{self.version}"
url = "https://example.com/pyside-chat"
license = "BSD license"
author = "{self.author}"
author_email = "author@example.com"

[tool.briefcase.app.{self.app_name.lower().replace('_', '-')}]
formal_name = "{self.app_name}"
description = "PySide Chat Application with AI personalities and TTS"
icon = "pyside_chat/{self.app_name.lower().replace('_', '-')}/resources/{self.app_name.lower().replace('_', '-')}"
sources = ["pyside_chat/{self.app_name.lower().replace('_', '-')}"]
requires = [
    "PySide6>=6.5.0",
    "requests>=2.31.0",
    "pygments>=2.15.0",
    "edge-tts>=6.1.9",
    "gtts>=2.4.0",
    "pyttsx3>=2.90",
    "pygame>=2.5.0",
    "keyboard>=0.13.5",
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "librosa>=0.10.0",
    "soundfile>=0.12.0",
    "pydub>=0.25.1",
    "torch",
    "scikit-learn",
    "sentence-transformers==2.2.2",
    "transformers==4.21.0",
    "huggingface-hub==0.16.4",
    "TTS>=0.22.0",
]

[tool.briefcase.app.{self.app_name.lower().replace('_', '-')}.macOS]
requires = [
    "PySide6>=6.5.0",
    "requests>=2.31.0",
    "pygments>=2.15.0",
    "edge-tts>=6.1.9",
    "gtts>=2.4.0",
    "pyttsx3>=2.90",
    "pygame>=2.5.0",
    "keyboard>=0.13.5",
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "librosa>=0.10.0",
    "soundfile>=0.12.0",
    "pydub>=0.25.1",
    "torch",
    "scikit-learn",
    "sentence-transformers==2.2.2",
    "transformers==4.21.0",
    "huggingface-hub==0.16.4",
    "TTS>=0.22.0",
]

[tool.briefcase.app.{self.app_name.lower().replace('_', '-')}.linux]
requires = [
    "PySide6>=6.5.0",
    "requests>=2.31.0",
    "pygments>=2.15.0",
    "edge-tts>=6.1.9",
    "gtts>=2.4.0",
    "pyttsx3>=2.90",
    "pygame>=2.5.0",
    "keyboard>=0.13.5",
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "librosa>=0.10.0",
    "soundfile>=0.12.0",
    "pydub>=0.25.1",
    "torch",
    "scikit-learn",
    "sentence-transformers==2.2.2",
    "transformers==4.21.0",
    "huggingface-hub==0.16.4",
    "TTS>=0.22.0",
]

[tool.briefcase.app.{self.app_name.lower().replace('_', '-')}.windows]
requires = [
    "PySide6>=6.5.0",
    "requests>=2.31.0",
    "pygments>=2.15.0",
    "edge-tts>=6.1.9",
    "gtts>=2.4.0",
    "pyttsx3>=2.90",
    "pygame>=2.5.0",
    "keyboard>=0.13.5",
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "librosa>=0.10.0",
    "soundfile>=0.12.0",
    "pydub>=0.25.1",
    "torch",
    "scikit-learn",
    "sentence-transformers==2.2.2",
    "transformers==4.21.0",
    "huggingface-hub==0.16.4",
    "TTS>=0.22.0",
]
'''
        config_file = self.project_root / "pyproject.toml"
        with open(config_file, 'w') as f:
            f.write(config_content)
        return str(config_file)
    
    def setup_briefcase_project(self) -> bool:
        """Set up the Briefcase project structure."""
        print("  📁 Setting up Briefcase project structure...")
        
        try:
            # Create pyside_chat directory structure
            pyside_chat_dir = self.project_root / "pyside_chat" / self.app_name.lower().replace('_', '-')
            pyside_chat_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy main.py to pyside_chat
            main_pyside_chat = pyside_chat_dir / "main.py"
            shutil.copy2(self.main_script, main_pyside_chat)
            
            # Copy pyside_chat directory
            pyside_chat_pyside_chat = self.project_root / "pyside_chat"
            if pyside_chat_pyside_chat.exists():
                pyside_chat_dst = pyside_chat_dir / "pyside_chat"
                shutil.copytree(pyside_chat_pyside_chat, pyside_chat_dst, dirs_exist_ok=True)
            
            # Copy other necessary files
            files_to_copy = ["config.json"]
            for file_path in files_to_copy:
                pyside_chat_file = self.project_root / file_path
                if pyside_chat_file.exists():
                    dst_file = pyside_chat_dir / file_path
                    shutil.copy2(pyside_chat_file, dst_file)
            
            # Copy directories
            dirs_to_copy = ["personality_Profiles", "DOCUMENTATION"]
            for dir_path in dirs_to_copy:
                pyside_chat_dir_path = self.project_root / dir_path
                if pyside_chat_dir_path.exists():
                    dst_dir_path = pyside_chat_dir / dir_path
                    shutil.copytree(pyside_chat_dir_path, dst_dir_path, dirs_exist_ok=True)
            
            print("  ✅ Briefcase project structure created")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to set up Briefcase project: {e}")
            return False
    
    def package_with_briefcase(self) -> bool:
        """Package the application using Briefcase."""
        print("📦 Packaging with Briefcase...")
        
        try:
            # Create Briefcase config
            config_file = self.create_briefcase_config()
            print(f"  📄 Created config file: {config_file}")
            
            # Set up project structure
            if not self.setup_briefcase_project():
                return False
            
            # Run Briefcase commands
            app_name = self.app_name.lower().replace('_', '-')
            
            # Create the app
            print(f"  🔨 Creating Briefcase app...")
            cmd_create = [sys.executable, "-m", "briefcase", "new", app_name]
            result = subprocess.run(cmd_create, check=True, capture_output=True, text=True)
            
            # Build the app
            print(f"  🔨 Building Briefcase app...")
            cmd_build = [sys.executable, "-m", "briefcase", "build", app_name]
            result = subprocess.run(cmd_build, check=True, capture_output=True, text=True)
            
            # Create the app
            print(f"  🔨 Creating Briefcase app...")
            cmd_create_app = [sys.executable, "-m", "briefcase", "create", app_name]
            result = subprocess.run(cmd_create_app, check=True, capture_output=True, text=True)
            
            # Check output
            build_dir = self.project_root / "windows" / app_name / "pyside_chat"
            if build_dir.exists():
                print(f"  ✅ Success! Briefcase app created in: {build_dir.parent}")
                return True
            else:
                print(f"  ❌ Failed: Briefcase build directory not found")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Briefcase failed: {e}")
            if e.stderr:
                print(f"     Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False
    
    def create_pyinstaller_spec(self) -> str:
        """Create a PyInstaller spec file for the application."""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('personality_Profiles', 'personality_Profiles'),
        ('pyside_chat', 'pyside_chat'),
        ('DOCUMENTATION', 'DOCUMENTATION'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'requests',
        'pygments',
        'edge_tts',
        'gtts',
        'pyttsx3',
        'pygame',
        'keyboard',
        'numpy',
        'scipy',
        'librosa',
        'soundfile',
        'pydub',
        'torch',
        'sklearn',
        'sentence_transformers',
        'TTS',
        'enchant',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
        spec_file = self.project_root / f"{self.app_name}.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        return str(spec_file)
    
    def package_with_pyinstaller(self) -> bool:
        """Package the application using PyInstaller."""
        print("📦 Packaging with PyInstaller...")
        
        try:
            # Create spec file
            spec_file = self.create_pyinstaller_spec()
            print(f"  📄 Created spec file: {spec_file}")
            
            # Run PyInstaller
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm",
                spec_file
            ]
            
            print(f"  🔨 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Check output
            dist_dir = self.project_root / "dist" / self.app_name
            if dist_dir.exists():
                print(f"  ✅ Success! Executable created in: {dist_dir}")
                return True
            else:
                print(f"  ❌ Failed: dist directory not found")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ PyInstaller failed: {e}")
            if e.stderr:
                print(f"     Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False
    
    def create_setup_cx_freeze(self) -> str:
        """Create a cx_Freeze setup script."""
        setup_content = f'''#!/usr/bin/env python3
import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {{
    "packages": [
        "PySide6", "requests", "pygments", "edge_tts", "gtts", 
        "pyttsx3", "pygame", "keyboard", "numpy", "scipy", 
        "librosa", "soundfile", "pydub", "torch", "sklearn",
        "sentence_transformers", "TTS", "enchant"
    ],
    "excludes": [],
    "include_files": [
        ("config.json", "config.json"),
        ("personality_Profiles", "personality_Profiles"),
        ("pyside_chat", "pyside_chat"),
        ("DOCUMENTATION", "DOCUMENTATION"),
    ],
    "include_msvcr": True,
}}

# Base for Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="{self.app_name}",
    version="{self.version}",
    description="PySide Chat Application",
    author="{self.author}",
    options={{"build_exe": build_exe_options}},
    executables=[
        Executable(
            "main.py", 
            base=base,
            target_name="{self.app_name}.exe",
            icon="icon.ico" if os.path.exists("icon.ico") else None
        )
    ]
)
'''
        setup_file = self.project_root / "setup_cx_freeze.py"
        with open(setup_file, 'w') as f:
            f.write(setup_content)
        return str(setup_file)
    
    def package_with_cx_freeze(self) -> bool:
        """Package the application using cx_Freeze."""
        print("📦 Packaging with cx_Freeze...")
        
        try:
            # Create setup script
            setup_file = self.create_setup_cx_freeze()
            print(f"  📄 Created setup file: {setup_file}")
            
            # Run cx_Freeze
            cmd = [sys.executable, setup_file, "build"]
            print(f"  🔨 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Check output
            build_dir = self.project_root / "build"
            if build_dir.exists():
                print(f"  ✅ Success! Build created in: {build_dir}")
                return True
            else:
                print(f"  ❌ Failed: build directory not found")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  ❌ cx_Freeze failed: {e}")
            if e.stderr:
                print(f"     Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False
    
    def create_distribution(self) -> bool:
        """Create a simple distribution package."""
        print("📦 Creating distribution package...")
        
        try:
            # Create dist directory
            dist_dir = self.project_root / "distribution" / self.app_name
            dist_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy main files
            files_to_copy = [
                "main.py",
                "config.json",
                "README.md",
                "requirements.txt" if (self.project_root / "requirements.txt").exists() else None
            ]
            
            for file_path in files_to_copy:
                if file_path and (self.project_root / file_path).exists():
                    shutil.copy2(self.project_root / file_path, dist_dir)
                    print(f"  📄 Copied: {file_path}")
            
            # Copy directories
            dirs_to_copy = [
                "pyside_chat",
                "personality_Profiles", 
                "DOCUMENTATION"
            ]
            
            for dir_path in dirs_to_copy:
                pyside_chat_dir = self.project_root / dir_path
                if pyside_chat_dir.exists():
                    dst_dir = dist_dir / dir_path
                    shutil.copytree(pyside_chat_dir, dst_dir, dirs_exist_ok=True)
                    print(f"  📁 Copied: {dir_path}")
            
            # Create run script
            if platform.system() == "Windows":
                run_script = dist_dir / "run.bat"
                with open(run_script, 'w') as f:
                    f.write(f'''@echo off
echo Starting {self.app_name}...
python main.py
pause
''')
            else:
                run_script = dist_dir / "run.sh"
                with open(run_script, 'w') as f:
                    f.write(f'''#!/bin/bash
echo "Starting {self.app_name}..."
python3 main.py
''')
                os.chmod(run_script, 0o755)
            
            print(f"  📄 Created run script: {run_script.name}")
            
            # Create requirements file
            requirements_file = dist_dir / "requirements.txt"
            with open(requirements_file, 'w') as f:
                f.write('''# Core dependencies
PySide6>=6.5.0
requests>=2.31.0
pygments>=2.15.0

# TTS options
edge-tts>=6.1.9
gtts>=2.4.0
pyttsx3>=2.90

# Audio processing
pygame>=2.5.0
librosa>=0.10.0
soundfile>=0.12.0
pydub>=0.25.1

# Machine learning
torch
scikit-learn
sentence-transformers==2.2.2
transformers==4.21.0
huggingface-hub==0.16.4

# Optional
keyboard>=0.13.5
pyenchant>=3.2.2
TTS>=0.22.0
''')
            
            print(f"  📄 Created requirements.txt")
            print(f"  ✅ Distribution created in: {dist_dir}")
            return True
            
        except Exception as e:
            print(f"  ❌ Failed to create distribution: {e}")
            return False
    
    def package_all(self) -> bool:
        """Package using all available methods."""
        print("📦 Packaging with all methods...")
        
        results = {}
        
        # Try Briefcase (recommended for PySide apps)
        print("\n🔨 Method 1: Briefcase (Recommended)")
        results['briefcase'] = self.package_with_briefcase()
        
        # Try PyInstaller
        print("\n🔨 Method 2: PyInstaller")
        results['pyinstaller'] = self.package_with_pyinstaller()
        
        # Try cx_Freeze
        print("\n🔨 Method 3: cx_Freeze")
        results['cx_freeze'] = self.package_with_cx_freeze()
        
        # Create distribution
        print("\n🔨 Method 4: Distribution Package")
        results['distribution'] = self.create_distribution()
        
        # Summary
        print(f"\n📊 Packaging Results:")
        for method, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {method}: {status}")
        
        return any(results.values())
    
    def cleanup(self):
        """Clean up temporary files."""
        print("🧹 Cleaning up temporary files...")
        
        temp_files = [
            f"{self.app_name}.spec",
            "setup_cx_freeze.py",
            "pyproject.toml"
        ]
        
        for file_path in temp_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                full_path.unlink()
                print(f"  🗑️ Removed: {file_path}")
    
    def run(self, method: str = "all"):
        """Run the packager with the specified method."""
        print("🚀 PySide Chat Application Packager")
        print("=" * 50)
        
        # Check if main.py exists
        if not self.main_script.exists():
            print(f"❌ Error: main.py not found at {self.main_script}")
            return False
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Failed to install required dependencies")
            return False
        
        # Run packaging
        if method in self.packagers:
            success = self.packagers[method]()
        else:
            print(f"❌ Unknown packaging method: {method}")
            print(f"Available methods: {', '.join(self.packagers.keys())}")
            return False
        
        # Cleanup
        self.cleanup()
        
        if success:
            print(f"\n🎉 Packaging completed successfully!")
            print(f"📁 Check the output directories for your packaged application.")
        else:
            print(f"\n❌ Packaging failed. Check the error messages above.")
        
        return success

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Package PySide Chat Application")
    parser.add_argument(
        "method", 
        nargs="?", 
        default="all",
        choices=["briefcase", "pyinstaller", "cx_freeze", "dist", "all"],
        help="Packaging method to use"
    )
    
    args = parser.parse_args()
    
    packager = AppPackager()
    success = packager.run(args.method)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 
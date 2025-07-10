#!/usr/bin/env python3
"""
PySide Chat System - Dependency Installation Script

This script installs all required dependencies in stages with proper error handling, progress feedback, and the ability to resume from where it left off if there's an error.
"""

import subprocess
import sys
import os
import time
from typing import List, Dict, Tuple, Optional

# Try to import tqdm for progress bars, fallback to simple progress if not available
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Note: tqdm not available, using simple progress display")


class DependencyInstaller:
    """Handles staged installation of dependencies with error recovery."""
    
    def __init__(self):
        self.install_stages = [
            # Progress bar dependency (needed first)
            {
                "name": "tqdm",
                "description": "Progress bars for installation feedback",
                "command": ["pip", "install", "tqdm>=4.65.0"],
                "skip_if_failed": False
            },
            # Core GUI and basic functionality
            {
                "name": "PySide6",
                "description": "GUI Framework",
                "command": ["pip", "install", "PySide6>=6.5.0"],
                "skip_if_failed": False
            },
            {
                "name": "requests",
                "description": "HTTP Client for API calls",
                "command": ["pip", "install", "requests>=2.31.0"],
                "skip_if_failed": False
            },
            {
                "name": "ollama",
                "description": "Official Ollama Python client library",
                "command": ["pip", "install", "ollama>=0.1.7"],
                "skip_if_failed": False
            },
            {
                "name": "pygments",
                "description": "Code syntax highlighting",
                "command": ["pip", "install", "pygments>=2.15.0"],
                "skip_if_failed": False
            },
            {
                "name": "edge-tts",
                "description": "Microsoft Edge TTS (fast and natural)",
                "command": ["pip", "install", "edge-tts>=6.1.9"],
                "skip_if_failed": False
            },

            {
                "name": "playsound",
                "description": "Audio playback for TTS",
                "command": ["pip", "install", "playsound>=1.3.0"],
                "skip_if_failed": False
            },
            {
                "name": "pyttsx3",
                "description": "Local TTS engine",
                "command": ["pip", "install", "pyttsx3>=2.90"],
                "skip_if_failed": False
            },
            {
                "name": "pygame",
                "description": "Audio playback",
                "command": ["pip", "install", "pygame>=2.5.0"],
                "skip_if_failed": False
            },
            {
                "name": "keyboard",
                "description": "Keyboard input handling",
                "command": ["pip", "install", "keyboard>=0.13.5"],
                "skip_if_failed": False
            },
            {
                "name": "pyenchant",
                "description": "Spellchecker functionality",
                "command": ["pip", "install", "pyenchant>=3.2.2"],
                "skip_if_failed": False
            },
            {
                "name": "spellchecker-setup",
                "description": "Setting up spellchecker dictionaries and verification",
                "command": ["python", "-c", "import enchant; print('Spellchecker ready')"],
                "skip_if_failed": True
            },
            {
                "name": "numpy",
                "description": "Numerical computing",
                "command": ["pip", "install", "numpy>=1.21.0"],
                "skip_if_failed": False
            },
            {
                "name": "scipy",
                "description": "Scientific computing",
                "command": ["pip", "install", "scipy>=1.7.0"],
                "skip_if_failed": False
            },
            {
                "name": "librosa",
                "description": "Audio processing library",
                "command": ["pip", "install", "librosa>=0.10.0"],
                "skip_if_failed": False
            },
            {
                "name": "soundfile",
                "description": "Audio file I/O",
                "command": ["pip", "install", "soundfile>=0.12.0"],
                "skip_if_failed": False
            },
            {
                "name": "pydub",
                "description": "Audio manipulation",
                "command": ["pip", "install", "pydub>=0.25.1"],
                "skip_if_failed": False
            },
            # PyTorch and ML packages
            {
                "name": "PyTorch (CPU)",
                "description": "PyTorch with pre-built CPU wheels",
                "command": ["pip", "install", "torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"],
                "skip_if_failed": False
            },
            {
                "name": "scikit-learn",
                "description": "Machine learning library with pre-built wheels",
                "command": ["pip", "install", "scikit-learn", "--only-binary=all"],
                "skip_if_failed": False
            },
            {
                "name": "huggingface-hub",
                "description": "Hugging Face Hub (compatible version for sentence-transformers)",
                "command": ["pip", "install", "huggingface-hub==0.20.3"],
                "skip_if_failed": False
            },
            {
                "name": "transformers",
                "description": "Transformers library (compatible version)",
                "command": ["pip", "install", "transformers==4.35.2"],
                "skip_if_failed": False
            },
            {
                "name": "accelerate",
                "description": "Accelerate library (compatible version)",
                "command": ["pip", "install", "accelerate==0.25.0"],
                "skip_if_failed": False
            },
            {
                "name": "sentence-transformers",
                "description": "Semantic search and embeddings (compatible version)",
                "command": ["pip", "install", "sentence-transformers==2.2.2"],
                "skip_if_failed": True
            },
            {
                "name": "blis-prebuilt",
                "description": "Pre-built blis wheel for Coqui TTS",
                "command": ["pip", "install", "blis==0.7.9", "--only-binary=all"],
                "skip_if_failed": True
            },
            {
                "name": "thinc-prebuilt",
                "description": "Pre-built thinc wheel for Coqui TTS",
                "command": ["pip", "install", "thinc==8.1.10", "--only-binary=all"],
                "skip_if_failed": True
            },
            {
                "name": "Coqui TTS",
                "description": "Advanced TTS with emotion control (local TTS)",
                "command": ["pip", "install", "TTS==0.22.0"],
                "skip_if_failed": True
            },
            {
                "name": "PyAudio",
                "description": "Audio I/O library for recording and playback",
                "command": ["pip", "install", "PyAudio"],
                "skip_if_failed": True
            },
            {
                "name": "sounddevice",
                "description": "Audio library for real-time audio processing",
                "command": ["pip", "install", "sounddevice"],
                "skip_if_failed": True
            },
            {
                "name": "vosk",
                "description": "Offline speech recognition library",
                "command": ["pip", "install", "vosk"],
                "skip_if_failed": True
            },
            {
                "name": "playsound",
                "description": "Simple audio playback library",
                "command": ["pip", "install", "playsound>=1.3.0"],
                "skip_if_failed": True
            },
            {
                "name": "SpeechRecognition",
                "description": "Speech recognition library",
                "command": ["pip", "install", "SpeechRecognition"],
                "skip_if_failed": True
            },
            {
                "name": "pyvis",
                "description": "Network visualization library",
                "command": ["pip", "install", "pyvis"],
                "skip_if_failed": True
            }
        ]
        
        self.failed_stages = []
        self.successful_stages = []
    
    def print_header(self):
        """Print installation header."""
        print("PySide Chat System - Dependency Installation")
        print("=" * 50)
        print("Installing dependencies in stages...")
        print()
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"Error: Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    
    def check_virtual_environment(self) -> bool:
        """Check if running in a virtual environment."""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("Running in virtual environment")
            return True
        else:
            print("Warning: Not running in a virtual environment")
            response = input("Continue anyway? (y/N): ").lower().strip()
            return response in ['y', 'yes']
    
    def upgrade_pip(self) -> bool:
        """Upgrade pip to latest version."""
        print("Upgrading pip...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True,
                check=True
            )
            print("Pip upgraded successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to upgrade pip: {e}")
            return False
    
    def setup_spellchecker(self) -> bool:
        """Set up spellchecker with dictionary verification."""
        print("Setting up spellchecker...")
        
        try:
            import enchant
            print("pyenchant imported successfully")
            
            # Check for available dictionaries
            try:
                available_dicts = enchant.list_dicts()
                if available_dicts:
                    print(f"Available dictionaries: {len(available_dicts)} found")
                    for lang, provider in available_dicts:
                        print(f"  - {lang} ({provider})")
                else:
                    print("No dictionaries found")
                    print("Download from: https://www.abisource.com/projects/enchant/")
                    return False
                
                # Test spellchecker functionality
                try:
                    d = enchant.Dict("en_US")
                    test_word = "test"
                    if d.check(test_word):
                        print(f"Spellchecker test passed: '{test_word}' is valid")
                    else:
                        print(f"Spellchecker test passed: '{test_word}' is invalid (as expected)")
                    return True
                except Exception as e:
                    print(f"Dictionary test failed: {e}")
                    return False
                    
            except Exception as e:
                print(f"Could not check dictionaries: {e}")
                print("Download from: https://www.abisource.com/projects/enchant/")
                return False
                
        except ImportError as e:
            print(f"pyenchant import failed: {e}")
            print("Please install enchant system libraries:")
            print("Windows: Download from https://www.abisource.com/projects/enchant/")
            print("macOS: brew install enchant")
            print("Linux: sudo apt-get install libenchant1c2a")
            return False
    
    def run_stage(self, stage: Dict, stage_num: int, total_stages: int) -> bool:
        """Run a single installation stage."""
        if TQDM_AVAILABLE:
            # Use tqdm progress bar
            with tqdm(total=1, desc=f"[{stage_num}/{total_stages}] {stage['name']}", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
                print(f"Installing: {stage['name']} - {stage['description']}")
                
                start_time = time.time()
                
                # Special handling for spellchecker setup
                if stage['name'] == "spellchecker-setup":
                    success = self.setup_spellchecker()
                    elapsed_time = time.time() - start_time
                    
                    if success:
                        print(f"SUCCESS: Spellchecker setup completed in {elapsed_time:.1f}s")
                        self.successful_stages.append(stage['name'])
                        pbar.update(1)
                        return True
                    else:
                        print(f"SPELLCHECKER SETUP: Incomplete after {elapsed_time:.1f}s")
                        print("Spellchecker will use fallback mode")
                        self.failed_stages.append(stage['name'])
                        pbar.update(1)
                        return True  # Don't stop installation for spellchecker issues
                
                try:
                    # Run the command
                    result = subprocess.run(
                        stage['command'],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    elapsed_time = time.time() - start_time
                    print(f"SUCCESS: {stage['name']} installed in {elapsed_time:.1f}s")
                    
                    self.successful_stages.append(stage['name'])
                    pbar.update(1)
                    return True
                    
                except subprocess.CalledProcessError as e:
                    elapsed_time = time.time() - start_time
                    print(f"FAILED: {stage['name']} after {elapsed_time:.1f}s")
                    print(f"Error code: {e.returncode}")
                    
                    # Show error output
                    if e.stderr:
                        error_lines = e.stderr.strip().split('\n')
                        for line in error_lines[-3:]:  # Last 3 lines
                            if line.strip():
                                print(f"  {line}")
                    
                    self.failed_stages.append(stage['name'])
                    pbar.update(1)
                    
                    if stage.get('skip_if_failed', False):
                        print(f"SKIPPING: {stage['name']} (optional package) - continuing...")
                        return True
                    else:
                        print(f"STOPPING: {stage['name']} is required - installation failed")
                        return False
        else:
            # Fallback to simple progress display
            print(f"Installing: {stage['name']} - {stage['description']}")
            
            start_time = time.time()
            
            # Special handling for spellchecker setup
            if stage['name'] == "spellchecker-setup":
                success = self.setup_spellchecker()
                elapsed_time = time.time() - start_time
                
                if success:
                    print(f"SUCCESS: Spellchecker setup completed in {elapsed_time:.1f}s")
                    self.successful_stages.append(stage['name'])
                    return True
                else:
                    print(f"SPELLCHECKER SETUP: Incomplete after {elapsed_time:.1f}s")
                    print("Spellchecker will use fallback mode")
                    self.failed_stages.append(stage['name'])
                    return True  # Don't stop installation for spellchecker issues
            
            try:
                # Run the command
                result = subprocess.run(
                    stage['command'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                elapsed_time = time.time() - start_time
                print(f"SUCCESS: {stage['name']} installed in {elapsed_time:.1f}s")
                
                self.successful_stages.append(stage['name'])
                return True
                
            except subprocess.CalledProcessError as e:
                elapsed_time = time.time() - start_time
                print(f"FAILED: {stage['name']} after {elapsed_time:.1f}s")
                print(f"Error code: {e.returncode}")
                
                # Show error output
                if e.stderr:
                    error_lines = e.stderr.strip().split('\n')
                    for line in error_lines[-3:]:  # Last 3 lines
                        if line.strip():
                            print(f"  {line}")
                
                self.failed_stages.append(stage['name'])
                
                if stage.get('skip_if_failed', False):
                    print(f"SKIPPING: {stage['name']} (optional package) - continuing...")
                    return True
                else:
                    print(f"STOPPING: {stage['name']} is required - installation failed")
                    return False
    
    def verify_installation(self) -> bool:
        """Verify that key packages can be imported."""
        print("\nVerifying Installation")
        print("=" * 30)
        
        def get_version(module_name):
            """Get version of a module."""
            try:
                module = __import__(module_name)
                for attr in ['__version__', 'VERSION', 'version']:
                    if hasattr(module, attr):
                        return str(getattr(module, attr))
                return "unknown"
            except:
                return "error"
        
        test_imports = [
            ("tqdm", "Progress Bars"),
            ("PySide6", "GUI Framework"),
            ("requests", "HTTP Client"),
            ("ollama", "Ollama Python Client"),
            ("pygments", "Syntax Highlighting"),
            ("edge_tts", "Edge TTS"),
            ("pygame", "Audio Playback"),
            ("keyboard", "Keyboard Input"),
            ("numpy", "Numerical Computing"),
            ("scipy", "Scientific Computing"),
            ("librosa", "Audio Processing"),
            ("soundfile", "Audio File I/O"),
            ("pydub", "Audio Manipulation")
        ]
        
        optional_imports = [
            ("torch", "PyTorch"),
            ("sklearn", "Scikit-learn"),
            ("sentence_transformers", "Sentence Transformers"),
            ("TTS", "Coqui TTS"),
            ("pyaudio", "PyAudio"),
            ("sounddevice", "SoundDevice"),
            ("vosk", "Vosk STT"),
            ("playsound", "PlaySound")
        ]
        
        # Test pyenchant separately since it needs system library
        print("Special packages:")
        try:
            import enchant
            version = get_version("enchant")
            print(f"  pyenchant (Spellchecker) - enchant library available [{version}]")
            # Check if dictionaries are working
            try:
                d = enchant.Dict("en_US")
                print("  Spellchecker dictionaries working")
            except:
                print("  Spellchecker installed but dictionaries missing")
        except ImportError:
            print("  pyenchant (Spellchecker) - installed but enchant library missing")
            print("     Download from: https://www.abisource.com/projects/enchant/")
        
        all_success = True
        
        # Test required imports
        print("Required packages:")
        for module, description in test_imports:
            try:
                __import__(module)
                version = get_version(module)
                print(f"  {module} ({description}) [{version}]")
            except ImportError as e:
                print(f"  {module} ({description}) - {e} [not installed]")
                all_success = False
        
        # Test optional imports
        print("\nOptional packages:")
        for module, description in optional_imports:
            try:
                __import__(module)
                version = get_version(module)
                print(f"  {module} ({description}) [{version}]")
            except ImportError as e:
                print(f"  {module} ({description}) - {e} [not installed]")
        
        return all_success
    
    def print_summary(self):
        """Print installation summary."""
        print("\nINSTALLATION SUMMARY")
        print("=" * 50)
        
        total_stages = len(self.install_stages)
        successful_count = len(self.successful_stages)
        failed_count = len(self.failed_stages)
        success_rate = (successful_count / total_stages) * 100
        
        print(f"Overall Progress: {successful_count}/{total_stages} packages ({success_rate:.1f}%)")
        print()
        
        if self.successful_stages:
            print("SUCCESSFULLY INSTALLED:")
            for i, stage in enumerate(self.successful_stages, 1):
                # Try to get version info for the package
                version_info = ""
                if stage not in ["spellchecker-setup", "blis-prebuilt", "thinc-prebuilt"]:
                    try:
                        # Extract package name from stage name
                        package_name = stage.lower().replace(" (cpu)", "").replace(" ", "-")
                        if package_name == "pytorch":
                            package_name = "torch"
                        elif package_name == "coqui-tts":
                            package_name = "TTS"
                        
                        # Try to get version
                        module = __import__(package_name)
                        for attr in ['__version__', 'VERSION', 'version']:
                            if hasattr(module, attr):
                                version_info = f" [{str(getattr(module, attr))}]"
                                break
                    except:
                        pass
                
                print(f"  {i:2d}. {stage}{version_info}")
        
        if self.failed_stages:
            print(f"\nFAILED TO INSTALL:")
            for i, stage in enumerate(self.failed_stages, 1):
                print(f"  {i:2d}. {stage}")
        
        print(f"\nSTATISTICS:")
        print(f"   Total packages: {total_stages}")
        print(f"   Successful: {successful_count}")
        print(f"   Failed: {failed_count}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        if self.failed_stages:
            print(f"\nNEXT STEPS:")
            print(f"   • Check the error messages above for specific issues")
            print(f"   • Try installing failed packages individually:")
            for stage in self.failed_stages:
                print(f"     pip install {stage}")
            print(f"   • For blis-related errors, try:")
            print(f"     pip install blis==0.7.9 --only-binary=all")
            print(f"   • Run the script again to retry:")
            print(f"     python pyside_chat/services/start_up/install_dependencies.py --retry")
        else:
            print(f"\nALL PACKAGES INSTALLED SUCCESSFULLY!")
            print(f"   You can now run: python main.py")
        
        # Additional notes for common issues
        if successful_count >= 15:  # Most packages installed
            print(f"\nNOTES:")
            print(f"   • Core functionality is ready! You can run the application.")
            if "Coqui TTS" in self.failed_stages:
                print(f"   • Coqui TTS failed - run: python fix_coqui_tts.py")
                print(f"   • Other TTS options (Edge TTS) work but require internet")
            if "spellchecker-setup" in self.failed_stages:
                print(f"   • Spellchecker: Download enchant from https://www.abisource.com/projects/enchant/")
                print(f"   • Spellchecker will use fallback mode until enchant is installed")
            if "sentence-transformers" in self.successful_stages:
                print(f"   • Semantic search is working with compatible package versions")
            if "PyAudio" in self.failed_stages:
                print(f"   • PyAudio failed - audio recording may not work")
                print(f"   • On Windows, you may need Visual C++ Build Tools")
            if "vosk" in self.failed_stages:
                print(f"   • Vosk failed - offline speech recognition will not be available")
                print(f"   • Download Vosk models from: https://alphacephei.com/vosk/models")
            if "sounddevice" in self.failed_stages:
                print(f"   • SoundDevice failed - real-time audio processing may not work")
            print(f"   • For audio processing: Install ffmpeg for pydub (optional)")
            print(f"   • For spellchecker usage: Right-click misspelled words for suggestions")
    
    def install_all(self) -> bool:
        """Run the complete installation process."""
        self.print_header()
        
        # Pre-flight checks
        if not self.check_python_version():
            return False
        
        if not self.check_virtual_environment():
            return False
        
        if not self.upgrade_pip():
            print("Continuing without pip upgrade...")
        
        # Install stages
        print(f"\nStarting installation of {len(self.install_stages)} stages...")
        
        for i, stage in enumerate(self.install_stages, 1):
            if not self.run_stage(stage, i, len(self.install_stages)):
                print(f"\nInstallation failed at stage {i}: {stage['name']}")
                self.print_summary()
                return False
        
        # Verify installation
        verification_success = self.verify_installation()
        
        # Print summary
        self.print_summary()
        
        if verification_success:
            print(f"\nInstallation completed successfully!")
            print(f"   You can now run: python main.py")
        else:
            print(f"\nInstallation completed with some issues.")
            print(f"   Check the summary above for details.")
        
        return verification_success


def main():
    """Main entry point."""
    installer = DependencyInstaller()
    
    # Check for retry flag
    if "--retry" in sys.argv:
        print("Retry mode: Only failed stages will be attempted")
        # TODO: Implement retry logic for specific failed stages
        print("Retry functionality not yet implemented")
        return
    
    success = installer.install_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 
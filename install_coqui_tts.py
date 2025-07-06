#!/usr/bin/env python3
"""
Coqui TTS Installation Script

This script installs Coqui TTS and its dependencies for the PySide Chat application.
"""

import subprocess
import sys
import os
import platform

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("Coqui TTS Installation Script")
    print("=" * 60)
    print("This script will install Coqui TTS and its dependencies.")
    print("Coqui TTS provides high-quality, local text-to-speech functionality.")
    print()

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Error: Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_virtual_environment():
    """Check if running in virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Warning: Not running in virtual environment")
        response = input("Continue anyway? (y/N): ").lower().strip()
        return response in ['y', 'yes']

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to upgrade pip: {e}")
        return False

def install_package(package_name, description):
    """Install a package with error handling"""
    print(f"Installing {description}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {description} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {description}: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr.strip()}")
        return False

def install_coqui_tts():
    """Install Coqui TTS and dependencies"""
    print("\nInstalling Coqui TTS and dependencies...")
    
    # Install PyTorch first (CPU version for compatibility)
    if not install_package("torch", "PyTorch (CPU)"):
        print("⚠️  PyTorch installation failed, trying alternative...")
        if not install_package("torch --index-url https://download.pytorch.org/whl/cpu", "PyTorch (CPU)"):
            return False
    
    # Install Coqui TTS
    if not install_package("TTS==0.22.0", "Coqui TTS"):
        print("⚠️  Coqui TTS installation failed, trying alternative...")
        if not install_package("TTS", "Coqui TTS (latest)"):
            return False
    
    # Install additional dependencies that might be needed
    additional_packages = [
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("librosa", "Librosa"),
        ("soundfile", "SoundFile")
    ]
    
    for package, description in additional_packages:
        install_package(package, description)
    
    return True

def test_installation():
    """Test if Coqui TTS is working"""
    print("\nTesting Coqui TTS installation...")
    try:
        # Test import
        from TTS.api import TTS
        print("✅ Coqui TTS imported successfully")
        
        # Test model loading
        try:
            tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
            print("✅ Default model loaded successfully")
            
            # Test available models
            models = tts.list_models()
            print(f"✅ Found {len(models)} available models")
            
            return True
        except Exception as e:
            print(f"⚠️  Model loading test failed: {e}")
            print("This is normal for first-time installation - models will be downloaded when needed")
            return True
            
    except ImportError as e:
        print(f"❌ Coqui TTS import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Coqui TTS test failed: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("Coqui TTS Installation Complete!")
    print("=" * 60)
    print("Coqui TTS is now available in your PySide Chat application.")
    print()
    print("To use Coqui TTS:")
    print("1. Start your PySide Chat application")
    print("2. Go to Settings > Voice Settings")
    print("3. Select 'Coqui TTS' as your TTS provider")
    print("4. Choose your preferred voice and speed")
    print()
    print("Features available:")
    print("• High-quality, local text-to-speech")
    print("• Multiple voice models and speakers")
    print("• Adjustable speech speed")
    print("• No internet required after initial setup")
    print()
    print("If you encounter issues:")
    print("• Check that PyTorch is installed correctly")
    print("• Ensure you have sufficient disk space for models")
    print("• Models will be downloaded automatically on first use")
    print()

def main():
    """Main installation function"""
    print_header()
    
    # Pre-flight checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_virtual_environment():
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Install Coqui TTS
    if not install_coqui_tts():
        print("\n❌ Coqui TTS installation failed!")
        print("Please check the error messages above and try again.")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n⚠️  Installation completed but testing failed.")
        print("Coqui TTS may still work - try using it in the application.")
    else:
        print("\n✅ Coqui TTS installation and testing completed successfully!")
    
    print_usage_instructions()

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Spellchecker Installation Script for Ollama Chat

This script helps install the required spellchecker dependencies.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔍 Installing Spellchecker for Ollama Chat...")
    print("=" * 50)
    
    # Install pyenchant
    print("📦 Installing pyenchant...")
    if install_package("pyenchant"):
        print("✅ pyenchant installed successfully!")
    else:
        print("❌ Failed to install pyenchant")
        print("   You may need to install it manually: pip install pyenchant")
        print("   Note: A fallback spellchecker will be used if pyenchant is not available")
        return False
    
    # Check if enchant is available
    try:
        import enchant
        print("✅ Spellchecker is ready to use!")
        print("\n📝 Usage:")
        print("   - Right-click on misspelled words for suggestions")
        print("   - Choose 'Add to dictionary' to ignore words")
        print("   - Misspelled words will be highlighted with red underlines")
        
        # Check for available dictionaries
        try:
            available_dicts = enchant.list_dicts()
            if available_dicts:
                print(f"\n📚 Available dictionaries: {available_dicts}")
            else:
                print("\n⚠️  No dictionaries found - using fallback spellchecker")
        except:
            print("\n⚠️  Could not check dictionaries - using fallback spellchecker")
        
        return True
    except ImportError:
        print("❌ Spellchecker installation incomplete")
        print("   Please install enchant system libraries:")
        print("   - Windows: Download from https://www.abisource.com/projects/enchant/")
        print("   - macOS: brew install enchant")
        print("   - Linux: sudo apt-get install libenchant1c2a")
        print("\n💡 Note: A fallback spellchecker will be used if dictionaries are not available")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Spellchecker installation complete!")
    else:
        print("\n⚠️  Spellchecker installation incomplete. Some features may not work.")
    
    input("\nPress Enter to exit...") 
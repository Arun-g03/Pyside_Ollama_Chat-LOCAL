#!/usr/bin/env python3
"""
Spellchecker Installation Script for Ollama Chat

This script helps install the required spellchecker dependencies.
"""

import subprocess
import sys
import os

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from SRC.utils.Logging.Custom_Logger import CustomLogger
    logger = CustomLogger.get_logger(__name__)
except ImportError:
    # Fallback logger if CustomLogger is not available
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    logger.debug("🔍 Installing Spellchecker for Ollama Chat...",print_to_terminal=True)
    logger.debug("=" * 50,print_to_terminal=True)
    
    # Install pyenchant
    logger.debug("📦 Installing pyenchant...",print_to_terminal=True)
    if install_package("pyenchant"):
        logger.debug("✅ pyenchant installed successfully!",print_to_terminal=True)
    else:
        logger.debug("❌ Failed to install pyenchant",print_to_terminal=True)
        logger.debug("   You may need to install it manually: pip install pyenchant",print_to_terminal=True)
        logger.debug("   Note: A fallback spellchecker will be used if pyenchant is not available",print_to_terminal=True)
        return False
    
    # Check if enchant is available
    try:
        import enchant
        logger.debug("✅ Spellchecker is ready to use!",print_to_terminal=True)
        logger.debug("\n📝 Usage:",print_to_terminal=True)
        logger.debug("   - Right-click on misspelled words for suggestions",print_to_terminal=True)
        logger.debug("   - Choose 'Add to dictionary' to ignore words",print_to_terminal=True)
        logger.debug("   - Misspelled words will be highlighted with red underlines",print_to_terminal=True)
        
        # Check for available dictionaries
        try:
            available_dicts = enchant.list_dicts()
            if available_dicts:
                logger.debug(f"\n📚 Available dictionaries: {available_dicts}",print_to_terminal=True)
            else:
                logger.debug("\n⚠️  No dictionaries found - using fallback spellchecker",print_to_terminal=True)
        except:
            logger.debug("\n⚠️  Could not check dictionaries - using fallback spellchecker",print_to_terminal=True)
        
        return True
    except ImportError:
        logger.debug("❌ Spellchecker installation incomplete",print_to_terminal=True)
        logger.debug("   Please install enchant system libraries:",print_to_terminal=True)
        logger.debug("   - Windows: Download from https://www.abisource.com/projects/enchant/",print_to_terminal=True)
        logger.debug("   - macOS: brew install enchant",print_to_terminal=True)
        logger.debug("   - Linux: sudo apt-get install libenchant1c2a",print_to_terminal=True)
        logger.debug("\n💡 Note: A fallback spellchecker will be used if dictionaries are not available",print_to_terminal=True)
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.debug("\n🎉 Spellchecker installation complete!",print_to_terminal=True)
    else:
        logger.debug("\n⚠️  Spellchecker installation incomplete. Some features may not work.",print_to_terminal=True)
    
    input("\nPress Enter to exit...") 
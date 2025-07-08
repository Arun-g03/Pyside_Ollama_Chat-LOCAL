import sys
import argparse
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from pyside_chat.MainApp.ollama_chat import OllamaChat
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger
from pyside_chat.services.start_up.dependency_checker import check_and_install_dependencies

logger = CustomLogger.get_logger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Ollama Chat - Local LLM Chat Application")
    parser.add_argument(
        "--skip-deps", 
        action="store_true", 
        help="Skip dependency checking and installation"
    )
    parser.add_argument(
        "--no-auto-install", 
        action="store_true", 
        help="Check dependencies but don't auto-install missing ones"
    )
    return parser.parse_args()

def check_dependencies(auto_install=True):
    """Check if all required dependencies are available."""
    try:
        # Check dependencies and auto-install if needed
        dependencies_ok = check_and_install_dependencies(auto_install=auto_install)
        
        if not dependencies_ok:
            logger.error("[ID:0326] \n❌ Dependency check failed. Please run:\n"
                        "   python pyside_chat/services/start_up/install_dependencies.py\n"
                        "   or\n"
                        "   python pyside_chat/services/start_up/check_dependencies.py")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"[ID:0325] Error checking dependencies: {str(e)}")
        logger.info(f"[ID:0324] ❌ Error checking dependencies: {str(e)}")
        return False

def main():
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Check dependencies before starting the application (unless skipped)
        if not args.skip_deps:
            logger.info("[ID:0323] 🔍 Checking dependencies...", print_to_terminal=True)
            if not check_dependencies(auto_install=not args.no_auto_install):
                logger.error("[ID:0322] ❌ Cannot start application due to missing dependencies.")
                sys.exit(1)
        else:
            logger.error("[ID:0321] ⚠️  Skipping dependency check (--skip-deps flag used)")
        
        logger.info("[ID:0320] 🚀 Starting QApplication...",print_to_terminal=True)
        app = QApplication(sys.argv)
        logger.info("[ID:0319] Application started",print_to_terminal=True)
        # Set application properties
        app.setApplicationName("Ollama Chat - Local LLM Chat Application")
        app.setApplicationVersion("0.4.0")
        
        logger.info("[ID:0318] 🏗️  Creating main window...",print_to_terminal=True)
        # Create and show the main window
        window = OllamaChat()
        logger.info("[ID:0317] 📱 Showing main window...",print_to_terminal=True)
        window.show()
        
        # Connect the application's aboutToQuit signal to ensure cleanup
        app.aboutToQuit.connect(window.close)
        
        logger.info("[ID:0316] 🔄 Starting application event loop...",print_to_terminal=True)
        # Start the application event loop
        result = app.exec()
        logger.info(f"[ID:0315] 👋 QApplication event loop exited with code: {result}",print_to_terminal=True)
        return result
        
    except Exception as e:
        logger.error(f"[ID:0314] Error in main: {str(e)}",print_to_terminal=True)
        raise

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(f"[ID:0313] Fatal error: {str(e)}",print_to_terminal=True)
        sys.exit(1)

import sys
import argparse
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from pyside_chat.features.ollama.ollama_chat import OllamaChat
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.startup.dependency_checker import check_and_install_dependencies
from pyside_chat.core.threading.threading_service import ThreadingService
import traceback
import time

print("\n\n\nCurrent goal:")
print("1. Get the ollama chat working so we can use text chat")
print("2. Using proper threading architecture for better performance\n\n")

time.sleep(5)
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
            logger.error("[ID:0280] \n❌ Dependency check failed. Please run:\n"
                        "   python pyside_chat/services/start_up/install_dependencies.py\n"
                        "   or\n"
                        "   python pyside_chat/services/start_up/check_dependencies.py")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"[ID:0279] Error checking dependencies: {str(e)}")
        logger.info(f"[ID:0278] ❌ Error checking dependencies: {str(e)}")
        return False

def initialize_threading_system():
    """Initialize the threading system for the application."""
    try:
        logger.info("[DEBUG] Initializing threading system...", print_to_terminal=True)
        
        # Initialize the threading service
        threading_service = ThreadingService()
        
        logger.info("[DEBUG] Threading system initialized successfully", print_to_terminal=True)
        return threading_service
        
    except Exception as e:
        logger.error(f"[DEBUG] Error initializing threading system: {e}")
        logger.error(traceback.format_exc())
        return None

def cleanup_threading_system(threading_service):
    """Clean up the threading system."""
    try:
        if threading_service:
            logger.info("[DEBUG] Cleaning up threading system...", print_to_terminal=True)
            threading_service.cleanup()
            logger.info("[DEBUG] Threading system cleanup completed", print_to_terminal=True)
    except Exception as e:
        logger.error(f"[DEBUG] Error cleaning up threading system: {e}")
        logger.error(traceback.format_exc())

def main():
    threading_service = None
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Check dependencies before starting the application (unless skipped)
        if not args.skip_deps:
            logger.info("[ID:0277] 🔍 Checking dependencies...", print_to_terminal=True)
            if not check_dependencies(auto_install=not args.no_auto_install):
                logger.error("[ID:0276] ❌ Cannot start application due to missing dependencies.")
                sys.exit(1)
        else:
            logger.error("[ID:0275] ⚠️  Skipping dependency check (--skip-deps flag used)")
        
        logger.info("[ID:0274] 🚀 Starting QApplication...",print_to_terminal=True)
        app = QApplication(sys.argv)
        logger.info("[ID:0273] Application started",print_to_terminal=True)
        
        # Initialize threading system
        threading_service = initialize_threading_system()
        
        # Set application properties
        app.setApplicationName("Ollama Chat - Local LLM Chat Application")
        app.setApplicationVersion("0.4.0")
        
        logger.info("[ID:0272] 🏗️  Creating main window...",print_to_terminal=True)
        # Create and show the main window
        window = OllamaChat()
        logger.info("[ID:0271] 📱 Showing main window...",print_to_terminal=True)
        window.show()
        
        # Connect the application's aboutToQuit signal to ensure cleanup
        def cleanup_on_exit():
            try:
                logger.info("[DEBUG] Application about to quit, cleaning up...", print_to_terminal=True)
                
                # Clean up the main window
                if window:
                    window.close()
                
                # Clean up threading system
                cleanup_threading_system(threading_service)
                
                logger.info("[DEBUG] Application cleanup completed", print_to_terminal=True)
                
            except Exception as e:
                logger.error(f"[DEBUG] Error during application cleanup: {e}")
                logger.error(traceback.format_exc())
        
        app.aboutToQuit.connect(cleanup_on_exit)
        
        logger.info("[ID:0270] 🔄 Starting application event loop...",print_to_terminal=True)
        # Start the application event loop
        result = app.exec()
        logger.info(f"[ID:0269] 👋 QApplication event loop exited with code: {result}",print_to_terminal=True)
        return result
        
    except Exception as e:
        logger.error(f"[ID:0268] Error in main: {str(e)}",print_to_terminal=True)
        logger.error(traceback.format_exc())
        
        # Ensure cleanup even on error
        cleanup_threading_system(threading_service)
        raise

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(f"[ID:0266] Fatal error: {str(e)}",print_to_terminal=True)
        logger.error(traceback.format_exc())
        

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from SRC.ollama_chat import OllamaChat
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

def main():
    try:
        app = QApplication(sys.argv)
        logger.info("Application started",print_to_terminal=True)
        # Set application properties
        app.setApplicationName("Ollama Chat - Local LLM Chat Application")
        app.setApplicationVersion("1.0")
        
        # Create and show the main window
        window = OllamaChat()
        window.show()
        
        # Connect the application's aboutToQuit signal to ensure cleanup
        app.aboutToQuit.connect(window.close)
        
        # Start the application event loop
        return app.exec()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

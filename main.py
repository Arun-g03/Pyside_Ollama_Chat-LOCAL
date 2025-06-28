import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from SRC.ollama_chat import OllamaChat

def main():
    app = QApplication(sys.argv)
    print("Application started")
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

if __name__ == "__main__":
    sys.exit(main())

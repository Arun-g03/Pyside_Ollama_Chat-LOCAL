"""
Application Lifecycle Manager - Handles startup, shutdown, and error handling
"""

from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from typing import Optional
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger
from pyside_chat.utils.Logging.logging_helpers import LoggingHelpers
from pyside_chat.utils.prompts import PromptFormatter

logger = CustomLogger.get_logger(__name__)

class AppLifecycleManager:
    """Manages application startup, shutdown, and error handling"""
    
    def __init__(self, main_window: QMainWindow, service_manager, ui_manager, event_handler):
        self.main_window = main_window
        self.service_manager = service_manager
        self.ui_manager = ui_manager
        self.event_handler = event_handler
        
        # State tracking
        self.initialization_complete = False
        self.ollama_error_shown = False
        
    def initialize_application(self):
        """Initialize the application"""
        try:
            logger.info("Starting application initialization...")
            
            # Apply initial theme
            theme = self.service_manager.config_manager.get("theme", "Dark")
            self.ui_manager.apply_theme(theme)
            
            # Mark initialization as complete
            self.initialization_complete = True
            
            # Initial model refresh
            self.event_handler._on_refresh_models()
            
            logger.info("Application initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Error during application initialization: {e}")
            self._show_initialization_error(str(e))
            raise
    
    def handle_show_event(self):
        """Handle application show event"""
        try:
            # Skip if initialization not complete
            if not self.initialization_complete:
                return
            
            # Update window size from config
            width, height = self.service_manager.config_manager.get_window_size()
            if width > 0 and height > 0:
                self.main_window.resize(width, height)
            
            # Apply theme
            theme = self.service_manager.config_manager.get("theme", "Dark")
            self.ui_manager.apply_theme(theme)
            
            logger.info("Application show event handled successfully")
            
        except Exception as e:
            logger.error(f"Error handling show event: {e}")
    
    def handle_close_event(self, event):
        """Handle application close event"""
        try:
            logger.info("Handling application close event...")
            
            # Save current conversation
            conversation_service = self.service_manager.get_conversation_service()
            if conversation_service.get_messages():
                conversation_manager = self.service_manager.get_conversation_manager()
                conversation_manager.auto_save_conversation(
                    conversation_service.get_messages()
                )
            
            # Clean up voice service audio files
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab and hasattr(chat_tab, 'voice_service'):
                chat_tab.voice_service.cleanup_on_exit()
            
            # Save window state
            self.service_manager.config_manager.set_window_size(
                self.main_window.width(), 
                self.main_window.height()
            )
            
            # Clean up services
            self.service_manager.cleanup()
            
            event.accept()
            logger.info("Application close event handled successfully")
            
        except Exception as e:
            error_msg = PromptFormatter.format_error_message("close_error", error=str(e))
            LoggingHelpers.log_error("close", e)
            event.accept()
    
    def show_initialization_error(self, error_message: str):
        """Show initialization error dialog"""
        try:
            QMessageBox.critical(
                self.main_window,
                "Initialization Error",
                f"Failed to initialize application:\n\n{error_message}\n\nPlease check your configuration and try again."
            )
        except Exception as e:
            logger.error(f"Error showing initialization error dialog: {e}")
    
    def show_ollama_connection_error(self, context="general", force_show=False):
        """Show a user-friendly error dialog when Ollama is not running"""
        if not force_show and self.ollama_error_shown:
            return
        if not force_show:
            self.ollama_error_shown = True
            
        download_link = "https://ollama.com/download"
        
        if context == "startup":
            title = "Ollama Not Running"
            message = (
                'Ollama is not running or not accessible.<br><br>'
                'To fix this:<br>'
                '1. Make sure Ollama is installed<br>'
                "2. Start Ollama by running 'ollama serve' in a terminal<br>"
                f'3. Or download from: <a href="{download_link}">{download_link}</a><br><br>'
                "The application will continue to work, but you won't be able to send messages until Ollama is running."
            )
        else:
            title = "Connection Error"
            message = (
                'Cannot connect to Ollama.<br><br>'
                'Please make sure:<br>'
                "1. Ollama is running (run 'ollama serve' in a terminal)<br>"
                '2. Ollama is accessible at http://localhost:11434<br>'
                '3. No firewall is blocking the connection<br>'
                f'4. Download Ollama from: <a href="{download_link}">{download_link}</a><br><br>'
                'Try sending your message again once Ollama is running.'
            )
        
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        msg_box.setText(message)
        msg_box.exec()
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        ollama_service = self.service_manager.get_ollama_service()
        return ollama_service.test_connection()
    
    def is_initialization_complete(self) -> bool:
        """Check if initialization is complete"""
        return self.initialization_complete
    
    def set_ollama_error_shown(self, shown: bool):
        """Set the Ollama error shown flag"""
        self.ollama_error_shown = shown
    
    def get_ollama_error_shown(self) -> bool:
        """Get the Ollama error shown flag"""
        return self.ollama_error_shown 
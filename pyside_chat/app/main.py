from pyside_chat.core.shared_imports.pyside_imports import *
"""
Ollama Chat Main Window - Refactored Version
This is the refactored main window that uses modular components for better separation of concerns.
"""

# Import our modular components
from pyside_chat.app.service_manager import ServiceManager
from pyside_chat.ui.ui_manager import UIManager
from pyside_chat.app.event_bus import EventBus
from pyside_chat.app.app_lifecycle import AppLifecycleManager

# Import required services and controllers
from pyside_chat.config.config_manager import ConfigManager
from pyside_chat.features.chat.chat_controller import ChatController
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class OllamaChat(QMainWindow):
    """Main application window - refactored with modular components"""

    def __init__(self):
        try:
            super().__init__()

            # Initialize configuration
            self.config_manager = ConfigManager()

            # Initialize service manager
            self.service_manager = ServiceManager(self.config_manager)

            # Initialize chat controller
            self.chat_controller = ChatController(
                ollama_service=self.service_manager.get_ollama_service(),
                conversation_service=self.service_manager.get_conversation_service(),
                enhancement_service=self.service_manager.get_enhancement_service(),
                memory_service=self.service_manager.get_memory_service(),
                conversation_manager=self.service_manager.get_conversation_manager(),
                personality_service=self.service_manager.get_personality_service()
            )

            # Initialize UI manager
            self.ui_manager = UIManager(self, self.config_manager)

            # Initialize lifecycle manager first
            self.lifecycle_manager = AppLifecycleManager(
                self,
                self.service_manager,
                self.ui_manager,
                None  # Will set event_handler later
            )

            # Initialize Event Bus (but don't set up connections yet)
            self.event_handler = EventBus(
                self,
                self.service_manager,
                self.ui_manager,
                self.chat_controller,
                self.lifecycle_manager  # Pass lifecycle_manager to event_bus
            )

            # Update lifecycle manager with event_handler reference
            self.lifecycle_manager.event_handler = self.event_handler

            # Setup UI first
            self._setup_ui()

            # Setup connections AFTER UI is fully set up
            self._setup_connections()

            # Initialize application
            self.lifecycle_manager.initialize_application()

            logger.info(
                "[ID:0237] OllamaChat initialization completed successfully")

        except Exception as e:
            import traceback
            logger.error(f'[ID:0236] ❌ Exception in OllamaChat.__init__: {e}')
            logger.error(traceback.format_exc())
            traceback.print_exc()
            raise

    def _setup_ui(self):
        """Setup the UI components"""
        try:
            # Setup UI with services
            self.ui_manager.setup_ui(
                conversation_manager=self.service_manager.get_conversation_manager(),
                summarization_service=self.service_manager.get_summarization_service(),
                memory_enabled=self.service_manager.is_memory_enabled(),
                memory_service=self.service_manager.get_memory_service()
            )

            # Setup menu bar
            self.ui_manager.setup_menu_bar()

            # Set chat tab reference in controller for TTS functionality
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                self.chat_controller.set_chat_tab_reference(chat_tab)
                # Set chat controller reference in chat tab
                chat_tab.set_chat_controller(self.chat_controller)

            # CRITICAL FIX: Reconnect chat tab signals after UI setup
            # This ensures signals are connected even if chat tab is recreated
            self.event_handler.reconnect_chat_tab_signals()

            logger.info("[ID:0234] UI setup completed successfully")

        except Exception as e:
            import traceback
            logger.error(f"[ID:0233] Error setting up UI: {e}")
            logger.error(traceback.format_exc())
            traceback.print_exc()
            raise

    def _setup_connections(self):
        """Setup EventBus connections after UI is fully initialized"""
        try:
            # Ensure UI is fully set up before connecting signals
            if not self.ui_manager.get_chat_tab():
                logger.warning(
                    "[SETUP WARNING] Chat tab not available during connection setup")
                # Wait a bit and try again

            # Now set up connections
            self.event_handler.setup_connections()
            logger.info("[ID:0235] EventBus connections set up successfully")

        except Exception as e:
            import traceback
            logger.error(f"[ID:0232] Error setting up connections: {e}")
            logger.error(traceback.format_exc())
            # Don't raise here - let the application continue

    def showEvent(self, event):
        """Handle application show event"""
        super().showEvent(event)
        self.lifecycle_manager.handle_show_event()

    def closeEvent(self, event):
        """Handle application close event"""
        self.lifecycle_manager.handle_close_event(event)

    def show_ollama_connection_error(self, context="general", force_show=False):
        """Show Ollama connection error dialog"""
        self.lifecycle_manager.show_ollama_connection_error(
            context, force_show)

    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        return self.lifecycle_manager.check_ollama_connection()

    # Public methods for external access to managers
    def get_service_manager(self):
        """Get the service manager"""
        return self.service_manager

    def get_ui_manager(self):
        """Get the UI manager"""
        return self.ui_manager

    def get_event_handler(self):
        """Get the Event Bus"""
        return self.event_handler

    def get_lifecycle_manager(self):
        """Get the lifecycle manager"""
        return self.lifecycle_manager

    def get_chat_controller(self):
        """Get the chat controller"""
        return self.chat_controller

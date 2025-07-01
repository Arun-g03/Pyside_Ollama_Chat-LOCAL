"""
Ollama Chat Main Window - Refactored Version
This shows how the main window would look after extracting functionality into separate modules.
"""

from PySide6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget, QStatusBar,
                               QMenuBar, QMenu, QToolBar, QMessageBox)
from PySide6.QtCore import QTimer, QThread, Qt
from PySide6.QtGui import QIcon, QAction
import os

# Import extracted components
from SRC.ui.chat_tab import ChatTab
from SRC.ui.model_tab import ModelTab
from SRC.ui.personality_tab import PersonalityTab
from SRC.ui.memory_tab import MemoryTab
from SRC.services.ollama_service import OllamaService
from SRC.services.conversation_service import ConversationService
from SRC.services.enhancement_service import EnhancementService
from SRC.services.memory_service import MemoryService
from SRC.models.conversation_metadata import ConversationManager
from SRC.config.config_manager import ConfigManager
from SRC.ui.Widgets.settings_dialog import SettingsDialog
from SRC.services.worker.worker import Worker
from SRC.ui.styles.styles import dark_stylesheet, light_stylesheet
from SRC.utils.Logging.Custom_Logger import CustomLogger

# Import new refactored modules
from SRC.controllers.chat_controller import ChatController
from SRC.utils.prompts import PromptFormatter
from SRC.utils.logging_helpers import LoggingHelpers
from SRC.ui.styles.tab_styles import TabStyles

logger = CustomLogger.get_logger(__name__)

class OllamaChat(QMainWindow):
    """Main application window - simplified after refactoring"""
    
    def __init__(self):
        try:
            super().__init__()
            
            # Initialize configuration
            self.config_manager = ConfigManager()
            
            # Initialize services
            self.setup_services()
            
            # Initialize controller
            self.setup_controller()
            
            # Setup UI
            self.setup_ui()
            self.setup_menu_bar()
            
            # Setup connections
            self.setup_connections()
            
            # Apply styling
            self.apply_dark_theme()
            
            # Initialize state
            self.initialization_complete = False
            self.model_change_in_progress = False
            self.ollama_error_shown = False  # Track if error dialog has been shown
            
            # Setup timers
            self.setup_timers()
            
            # Mark initialization as complete
            self.initialization_complete = True
            
            # Initial model refresh
            self.refresh_models()
        except Exception as e:
            import traceback
            print('❌ Exception in OllamaChat.__init__:', e)
            traceback.print_exc()
            raise
    
    def setup_services(self):
        """Initialize all services"""
        self.ollama_service = OllamaService(self.config_manager.get_ollama_url())
        self.conversation_service = ConversationService(
            self.config_manager.get_history_directory()
        )
        self.enhancement_service = EnhancementService(self.ollama_service)
        self.memory_enabled = self.config_manager.get("memory_enabled", True)
        if self.memory_enabled:
            self.memory_service = MemoryService(
                max_context_messages=self.config_manager.get_max_context_messages()
            )
            self.conversation_service.set_memory_service(self.memory_service)
        else:
            self.memory_service = None
            self.conversation_service.set_memory_service(None)
        self.conversation_manager = ConversationManager(
            self.config_manager.get_history_directory()
        )
        self.session_variables = {
            'history': self.config_manager.is_history_enabled(),
            'wordwrap': self.config_manager.is_wordwrap_enabled(),
            'json_format': self.config_manager.is_json_format_enabled(),
            'verbose': self.config_manager.is_verbose_enabled(),
            'think': self.config_manager.is_think_enabled()
        }
    
    def setup_controller(self):
        """Initialize the chat controller"""
        self.chat_controller = ChatController(
            ollama_service=self.ollama_service,
            conversation_service=self.conversation_service,
            enhancement_service=self.enhancement_service,
            memory_service=self.memory_service,
            conversation_manager=self.conversation_manager
        )
    
    def setup_ui(self):
        """Setup the main UI"""
        # Set window properties
        self.setWindowTitle("Ollama Chat - Local LLM Chat Application")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget with external styling
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(TabStyles.get_tab_style())
        main_layout.addWidget(self.tabs)
        
        # Create and add tabs with reduced coupling
        self.chat_tab = ChatTab(conversation_manager=self.conversation_manager)
        self.model_tab = ModelTab()
        self.personality_tab = PersonalityTab()
        
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.addTab(self.model_tab, "Model Manager")
        self.tabs.addTab(self.personality_tab, "Personalities")
        
        # Conditionally add memory tab
        if self.memory_enabled:
            self.memory_tab = MemoryTab(memory_service=self.memory_service)
            self.memory_tab.set_conversation_service(self.conversation_service)
            self.tabs.addTab(self.memory_tab, "Memory")
        else:
            self.memory_tab = None
        
        # Setup status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_var = PromptFormatter.format_status_message("ready")
        self.status_bar.showMessage(self.status_var)
    
    def setup_menu_bar(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New conversation action
        new_conversation_action = QAction("&New Conversation", self)
        new_conversation_action.setShortcut("Ctrl+N")
        new_conversation_action.setStatusTip("Start a new conversation")
        new_conversation_action.triggered.connect(self.new_conversation)
        file_menu.addAction(new_conversation_action)
        
        # Clear chat action
        clear_chat_action = QAction("&Clear Chat", self)
        clear_chat_action.setShortcut("Ctrl+L")
        clear_chat_action.setStatusTip("Clear the current chat display")
        clear_chat_action.triggered.connect(self.clear_chat)
        file_menu.addAction(clear_chat_action)
        
        file_menu.addSeparator()
        
        # Save chat action
        save_chat_action = QAction("&Save Chat...", self)
        save_chat_action.setShortcut("Ctrl+S")
        save_chat_action.setStatusTip("Save current chat to file")
        save_chat_action.triggered.connect(self.save_chat)
        file_menu.addAction(save_chat_action)
        
        # Load chat action
        load_chat_action = QAction("&Load Chat...", self)
        load_chat_action.setShortcut("Ctrl+O")
        load_chat_action.setStatusTip("Load chat from file")
        load_chat_action.triggered.connect(self.load_chat)
        file_menu.addAction(load_chat_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        # Settings action
        settings_action = QAction("&Settings...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.setStatusTip("Open application settings")
        settings_action.triggered.connect(self.open_settings)
        edit_menu.addAction(settings_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Refresh models action
        refresh_models_action = QAction("&Refresh Models", self)
        refresh_models_action.setStatusTip("Refresh available models from Ollama")
        refresh_models_action.triggered.connect(self.refresh_models)
        tools_menu.addAction(refresh_models_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.setStatusTip("About Ollama Chat")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_connections(self):
        """Setup signal connections between components"""
        # Connect controller signals
        self.chat_controller.status_updated.connect(self.update_status)
        self.chat_controller.error_occurred.connect(self.show_error)
        self.chat_controller.conversation_updated.connect(self.on_conversation_updated)
        
        # Connect Ollama service signals
        self.ollama_service.model_list_updated.connect(self.on_models_updated)
        self.ollama_service.model_operation_progress.connect(self.on_model_operation_progress)
        self.ollama_service.model_operation_error.connect(self.on_model_operation_error)
        
        # Connect chat tab signals
        self.chat_tab.message_sent.connect(self.on_message_sent)
        self.chat_tab.message_cancelled.connect(self.on_message_cancelled)
        self.chat_tab.conversation_selected.connect(self.on_conversation_selected)
        self.chat_tab.conversation_deleted.connect(self.on_conversation_deleted)
        self.chat_tab.conversation_renamed.connect(self.on_conversation_renamed)
        self.chat_tab.new_conversation_requested.connect(self.new_conversation)
        
        # Connect model tab signals
        self.model_tab.model_pull_requested.connect(self.ollama_service.pull_model)
        self.model_tab.model_remove_requested.connect(self.ollama_service.remove_model)
        self.model_tab.model_update_requested.connect(self.ollama_service.update_model)
        
        # Connect personality tab signals
        self.personality_tab.personality_changed.connect(self.on_personality_changed)
        
        # Connect conversation manager signals
        self.conversation_manager.metadata_updated.connect(self.on_conversation_metadata_updated)
    
    def setup_timers(self):
        """Setup timers for delayed operations"""
        self.model_update_timer = QTimer()
        self.model_update_timer.setSingleShot(True)
        self.model_update_timer.timeout.connect(self._delayed_model_update)
    
    def refresh_models(self):
        """Refresh the list of available models"""
        try:
            models = self.ollama_service.get_models()
            if models:
                self.ollama_error_shown = False  # Reset error flag on success
                self.chat_tab.update_model_list(models)
                self.model_tab.update_model_list(models)
            else:
                # No models returned - likely Ollama is not running
                self.show_ollama_connection_error("startup")
        except Exception as e:
            logger.error(f"Error refreshing models: {e}")
            self.show_ollama_connection_error("startup")
        
        # Also refresh personalities
        self.refresh_personalities()
    
    def refresh_personalities(self):
        """Refresh the list of available personalities"""
        try:
            personalities = self.personality_tab.get_available_personalities()
            if personalities:
                self.chat_tab.update_personality_list(personalities)
        except Exception as e:
            LoggingHelpers.log_error("refresh_personalities", e)
    
    def on_models_updated(self, models):
        """Handle model list updates"""
        self.chat_tab.update_model_list(models)
        self.model_tab.update_model_list(models)
        status_msg = PromptFormatter.format_status_message("models_found", count=len(models))
        self.update_status(status_msg)
    
    def on_message_sent(self, message):
        """Handle new message sent from chat tab"""
        # Get current model and temperature from chat tab
        model = self.chat_tab.get_current_model()
        temperature = self.chat_tab.get_temperature()
        
        # Process message through controller
        self.chat_controller.process_user_message(message, model, temperature)
        
        # Send to Ollama for actual processing
        self.send_to_ollama(message, model, temperature)

    def send_to_ollama(self, message, model, temperature):
        """Send message to Ollama and handle response asynchronously"""
        # Always show error dialog if user tries to send a message and Ollama is not running
        if not self.check_ollama_connection():
            self.show_ollama_connection_error("message", force_show=True)
            self.chat_tab.append_to_chat("System", "Failed to send: Could not connect to Ollama.\n Please check the Ollama connection and try again.")
            
            self.chat_tab.stop_streaming()
            return
        
        messages = self.conversation_service.get_messages()
        
        # Use STM+LTM context if memory enabled
        if self.chat_controller.is_memory_active():
            context_messages = self.memory_service.get_context_messages(current_query=message)
        else:
            context_messages = messages
        
        # Detect if this is a new conversation
        is_new_conversation = False
        if context_messages:
            user_messages = [msg for msg in context_messages if msg.get("role") == "user"]
            if len(user_messages) <= 1:
                is_new_conversation = True
                LoggingHelpers.log_conversation_detection(True, "message count")
        
        # Use the explicit new conversation flag if set
        if self.chat_controller.is_new_conversation:
            is_new_conversation = True
            LoggingHelpers.log_conversation_detection(True, "explicit flag")
        
        # Build the system prompt (without hardcoded user info)
        system_prompt = ""
        if context_messages:
            system_prompt = self.personality_tab.personality_model.build_comprehensive_system_prompt(self.memory_service)
        
        # Get dynamic user context messages with conversation status
        user_context_messages = self.personality_tab.personality_model.get_user_context_messages(
            self.memory_service, is_new_conversation
        )
        
        # Filter out any existing system messages from context
        filtered_context = [msg for msg in context_messages if msg.get("role") != "system"]
        
        # Build final context: system prompt + user context + conversation messages
        final_context = []
        
        # Add system prompt first
        if system_prompt:
            final_context.append({"role": "system", "content": system_prompt})
            LoggingHelpers.log_debug(f"System prompt added (length: {len(system_prompt)} chars)")
        
        # Add user context messages
        final_context.extend(user_context_messages)
        if user_context_messages:
            LoggingHelpers.log_debug(f"Added {len(user_context_messages)} user context messages")
        
        # Add conversation messages
        final_context.extend(filtered_context)
        
        context_messages = final_context
        
        # Reset new conversation flag after processing
        if self.chat_controller.is_new_conversation:
            self.chat_controller.is_new_conversation = False
            LoggingHelpers.log_debug("Reset new conversation flag")
        
        # Log the final context being sent to AI
        LoggingHelpers.log_context_messages(context_messages)
        
        # Get current model
        available_models = self.ollama_service.get_models() or []
        chosen_model = model
        
        # Auto model selection using complexity checker
        if model == "Auto":
            from SRC.utils.complexity_analyzer import RequestComplexityAnalyzer
            analyzer = RequestComplexityAnalyzer()
            complexity_metrics = analyzer.analyze_complexity(message, context_messages)
            chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
            # Insert a system message about the chosen model
            system_info = PromptFormatter.format_auto_model_selection_info(chosen_model)
            self.conversation_service.add_message("system", system_info)
            self.chat_tab.append_to_chat("System", system_info)
            context_messages = self.conversation_service.get_context_messages()
        
        # Create worker thread for async communication
        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        
        # Store the chosen model for this response
        self._current_response_model = chosen_model

        # Connect worker signals
        self.worker.stream_chunk_signal.connect(lambda chunk: self.chat_tab.append_response_signal.emit(chunk, self._current_response_model if model == "Auto" else None))
        self.worker.finished_signal.connect(self.on_worker_finished)
        self.worker.update_message_signal.connect(self.on_worker_error)
        
        # Connect thread signals
        self.worker_thread.started.connect(
            lambda: self.worker.run_stream(
                context_messages,
                chosen_model,
                temperature,
                self.config_manager.get_ollama_url(),
                self.config_manager.get_max_tokens(),
                self.config_manager.get_top_p(),
                self.config_manager.get_frequency_penalty(),
                self.config_manager.get_presence_penalty(),
            )
        )
        # Start the worker thread
        self.worker_thread.start()

    def on_worker_finished(self):
        """Handle worker completion"""
        final_response = self.chat_tab.get_current_response()
        
        # Handle response through controller
        self.chat_controller.handle_ai_response(final_response)
        
        # Update UI
        self.chat_tab.streaming_handler.finalize_streaming_message()
        self.on_message_finished()
        
        # Clean up worker
        if hasattr(self, 'worker_thread'):
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread.deleteLater()
            delattr(self, 'worker_thread')
            delattr(self, 'worker')

    def on_worker_error(self, error_message):
        """Handle worker error"""
        self.chat_tab.append_to_chat("System", f"Error: {error_message}")
        self.on_worker_finished()

    def on_message_finished(self):
        """Handle message finished"""
        LoggingHelpers.log_debug("on_message_finished called")
        self.chat_tab.stop_streaming()
    
    def on_message_cancelled(self):
        """Handle message cancellation"""
        # Cancel the Ollama service request
        self.ollama_service.cancel_request()
        
        # Stop the worker thread if it's running
        if hasattr(self, 'worker_thread') and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread.deleteLater()
            delattr(self, 'worker_thread')
            delattr(self, 'worker')
        
        # Update the chat tab
        self.chat_tab.on_message_cancelled()
    
    def on_conversation_selected(self, filepath: str):
        """Handle conversation selection from navigation"""
        self.chat_controller.load_conversation(filepath)
        self.chat_tab.load_conversation(filepath)
    
    def on_conversation_deleted(self, filepath: str):
        """Handle conversation deletion from navigation"""
        self.chat_controller.delete_conversation(filepath)
    
    def on_conversation_renamed(self, old_filepath: str, new_filepath: str):
        """Handle conversation rename from navigation"""
        self.chat_controller.rename_conversation(old_filepath, new_filepath)
        # Update the current conversation file reference in the chat tab
        if self.conversation_manager.get_current_metadata().current_conversation_file == new_filepath:
            self.chat_tab.set_current_conversation_file(new_filepath)
    
    def on_personality_changed(self, personality_name):
        """Handle personality changes"""
        # Update conversation metadata
        self.conversation_manager.get_current_metadata().update_personality(personality_name)
        
        # Clear conversation
        self.conversation_service.clear_conversation()
        
        # Clear chat display to prevent old messages from appearing
        self.chat_tab.clear_chat()
        
        # Update UI
        self.chat_tab.on_personality_changed(personality_name)
        
        # Sync personality selection in chat tab
        if hasattr(self.chat_tab, 'personality_combo'):
            self.chat_tab.personality_combo.setCurrentText(personality_name)
        
        # Show status
        status_msg = PromptFormatter.format_status_message("personality_switched", personality=personality_name)
        self.update_status(status_msg)
    
    def on_model_operation_progress(self, message):
        """Handle model operation progress"""
        self.model_tab.append_status(message)
    
    def on_model_operation_error(self, error):
        """Handle model operation errors"""
        self.model_tab.append_status(f"Error: {error}")
        status_msg = PromptFormatter.format_status_message("model_operation_error", error=error)
        self.update_status(status_msg)
        
        # Show user-friendly error dialog for connection issues
        if "Cannot connect to Ollama" in error or "connection" in error.lower():
            self.show_ollama_connection_error("operation")
    
    def on_conversation_metadata_updated(self):
        """Handle conversation metadata updates"""
        metadata = self.conversation_manager.get_current_metadata()
        self.update_status(metadata.get_display_info())
    
    def on_conversation_updated(self):
        """Handle conversation updates from controller"""
        # Refresh navigation widget
        self.chat_tab.refresh_navigation()
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_var = message
        self.status_bar.showMessage(self.status_var)
    
    def show_error(self, error_message: str):
        """Show error message"""
        QMessageBox.critical(self, "Error", error_message)
    
    def _delayed_model_update(self):
        """Delayed model update to ensure UI is ready"""
        try:
            # Update session variables for new model
            current_model = self.chat_tab.get_current_model()
            if current_model:
                self.session_variables['model'] = current_model
                self.conversation_manager.get_current_metadata().update_model(current_model)
        finally:
            self.model_change_in_progress = False
    
    # Menu action handlers
    def new_conversation(self):
        """Start a new conversation"""
        LoggingHelpers.log_debug("=== NEW CONVERSATION START ===")
        self.chat_controller.start_new_conversation()
        self.chat_tab.clear_chat()
        self.chat_tab.refresh_navigation()
        self.chat_tab.set_current_conversation_file(None)
    
    def clear_chat(self):
        """Clear the chat display"""
        question_text = PromptFormatter.get_menu_text("clear_chat_question")
        reply = QMessageBox.question(
            self, "Clear Chat", question_text,
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.chat_tab.clear_chat()
            status_msg = PromptFormatter.format_status_message("chat_cleared")
            self.update_status(status_msg)
    
    def save_chat(self):
        """Save the current chat to a file"""
        self.chat_tab.save_chat()
    
    def load_chat(self):
        """Load a chat from a file"""
        self.chat_tab.load_chat()
    
    def open_settings(self):
        """Open the settings dialog and update memory features if changed"""
        # Always fetch the latest lists before opening the dialog
        models = self.ollama_service.get_models() or ["llama2"]
        personalities = self.personality_tab.personality_model.get_available_personalities() or ["assistant"]
        dialog = SettingsDialog(self.config_manager, models, personalities, self)
        if dialog.exec():
            memory_enabled_now = self.config_manager.get("memory_enabled", True)
            if memory_enabled_now != self.memory_enabled:
                self.memory_enabled = memory_enabled_now
                self.setup_services()
                self.setup_controller()
                self.setup_ui()
                self.setup_connections()
                self.refresh_models()
            else:
                self.setup_services()
                self.setup_controller()
                self.setup_connections()
                self.refresh_models()
    
    def show_about(self):
        """Show about dialog"""
        about_text = PromptFormatter.get_menu_text("about_text")
        QMessageBox.about(self, "About Ollama Chat", about_text)
    
    def apply_dark_theme(self):
        """Apply dark theme styling"""
        self.setStyleSheet(dark_stylesheet)
    
    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Save current conversation
            if self.conversation_service.get_messages():
                self.conversation_manager.auto_save_conversation(
                    self.conversation_service.get_messages()
                )
            
            # Save window state
            self.config_manager.set_window_size(self.width(), self.height())
            
            event.accept()
            
        except Exception as e:
            error_msg = PromptFormatter.format_error_message("close_error", error=str(e))
            LoggingHelpers.log_error("close", e)
            event.accept()
    
    def showEvent(self, event):
        """Handle application show event"""
        super().showEvent(event)
        
        # Skip if initialization not complete
        if not self.initialization_complete:
            return
            
        # Update window size from config
        width, height = self.config_manager.get_window_size()
        if width > 0 and height > 0:
            self.resize(width, height)

        # Apply theme
        theme = self.config_manager.get("theme", "Dark")
        if theme == "Light":
            self.setStyleSheet(light_stylesheet)
        else:
            self.setStyleSheet(dark_stylesheet)

    def show_ollama_connection_error(self, context="general", force_show=False):
        """Show a user-friendly error dialog when Ollama is not running.
        If force_show is True, always show the dialog (used for explicit user actions).
        Otherwise, only show once per session (used for background/startup checks)."""
        from PySide6.QtCore import Qt
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
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        msg_box.setText(message)
        msg_box.exec()
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        return self.ollama_service.test_connection()
"""
Ollama Chat Main Window - Refactored Version
This shows how the main window would look after extracting functionality into separate modules.
"""

from PySide6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QWidget, QStatusBar,
                               QMenuBar, QMenu, QToolBar, QMessageBox)
from PySide6.QtCore import QTimer, QThread
from PySide6.QtGui import QIcon, QAction
import os

# Import extracted components
from SRC.ui.chat_tab import ChatTab
from SRC.ui.model_tab import ModelTab
from SRC.ui.personality_tab import PersonalityTab
from SRC.services.ollama_service import OllamaService
from SRC.services.conversation_service import ConversationService
from SRC.services.enhancement_service import EnhancementService
from SRC.models.conversation_metadata import ConversationManager
from SRC.config_manager import ConfigManager
from SRC.settings_dialog import SettingsDialog
from SRC.worker import Worker
from SRC.styles import dark_stylesheet, light_stylesheet


class OllamaChat(QMainWindow):
    """Main application window - simplified after refactoring"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        
        # Initialize services
        self.setup_services()
        
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
        
        # Setup timers
        self.setup_timers()
        
        # Mark initialization as complete
        self.initialization_complete = True
        
        # Initial model refresh
        self.refresh_models()
    
    def setup_services(self):
        """Initialize all services"""
        # Ollama service for API communication
        self.ollama_service = OllamaService(self.config_manager.get_ollama_url())
        
        # Conversation service for managing chat state
        self.conversation_service = ConversationService(
            self.config_manager.get_history_directory()
        )
        
        # Enhancement service for response enhancement
        self.enhancement_service = EnhancementService(self.ollama_service)
        
        # Conversation manager for persistence
        self.conversation_manager = ConversationManager(
            self.config_manager.get_history_directory()
        )
        
        # Initialize session variables
        self.session_variables = {
            'history': self.config_manager.is_history_enabled(),
            'wordwrap': self.config_manager.is_wordwrap_enabled(),
            'json_format': self.config_manager.is_json_format_enabled(),
            'verbose': self.config_manager.is_verbose_enabled(),
            'think': self.config_manager.is_think_enabled()
        }
    
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
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 24px;
                margin-right: 2px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
            }
            QTabBar::tab:selected {
                background: #0078d4;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background: #3d3d3d;
                color: #ffffff;
            }
        """)
        main_layout.addWidget(self.tabs)
        
        # Create and add tabs
        self.chat_tab = ChatTab(self, self.conversation_manager)
        self.model_tab = ModelTab(self)
        self.personality_tab = PersonalityTab(self)
        
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.addTab(self.model_tab, "Model Manager")
        self.tabs.addTab(self.personality_tab, "Personalities")
        
        # Setup status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_var = "Ready"
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
        models = self.ollama_service.get_models()
        if models:
            self.chat_tab.update_model_list(models)
            self.model_tab.update_model_list(models)
        
        # Also refresh personalities
        self.refresh_personalities()
    
    def refresh_personalities(self):
        """Refresh the list of available personalities"""
        try:
            personalities = self.personality_tab.get_available_personalities()
            if personalities:
                self.chat_tab.update_personality_list(personalities)
        except Exception as e:
            print(f"Error refreshing personalities: {e}")
    
    def on_models_updated(self, models):
        """Handle model list updates"""
        self.chat_tab.update_model_list(models)
        self.model_tab.update_model_list(models)
        self.status_var = f"Found {len(models)} models"
        self.status_bar.showMessage(self.status_var)
    
    def on_message_sent(self, message):
        """Handle new message sent from chat tab"""
        # Add to conversation
        self.conversation_service.add_message("user", message)
        
        # Send to Ollama
        self.send_to_ollama(message)
    
    def send_to_ollama(self, message):
        """Send message to Ollama and handle response asynchronously"""
        # Always append the user message first if not already present
        messages = self.conversation_service.get_messages()
        if not messages or messages[-1].get("role") != "user" or messages[-1].get("content") != message:
            self.conversation_service.add_message("user", message)
            messages = self.conversation_service.get_messages()
        print("DEBUG: Messages before sending:", messages)
        
        # Add system prompt if needed (at the start)
        if messages:
            system_prompt = self.personality_tab.personality_model.build_comprehensive_system_prompt()
            if system_prompt and (not messages or messages[0].get("role") != "system"):
                messages = [{"role": "system", "content": system_prompt}] + messages
        
        # Get current model
        model = self.chat_tab.get_current_model()
        available_models = self.ollama_service.get_models() or []
        chosen_model = model
        
        # Auto model selection using complexity checker
        if model == "Auto":
            from SRC.complexity_analyzer import RequestComplexityAnalyzer
            analyzer = RequestComplexityAnalyzer()
            # Use only the last user message for complexity
            complexity_metrics = analyzer.analyze_complexity(message, messages)
            chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
            # Insert a system message about the chosen model (after user message, before AI response)
            system_info = f"Using model {chosen_model} (auto-selected based on request complexity)"
            self.conversation_service.add_message("system", system_info)
            self.chat_tab.append_to_chat("System", system_info)
            messages = self.conversation_service.get_messages()
        
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
                messages,
                chosen_model,
                self.chat_tab.get_temperature(),
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
        # Add final response to conversation
        final_response = self.chat_tab.get_current_response()
        self.conversation_service.add_message("assistant", final_response)
        
        # Save conversation and get the filepath
        saved_filepath = self.conversation_manager.auto_save_conversation(
            self.conversation_service.get_messages()
        )
        
        # Update navigation widget with current conversation file
        if saved_filepath:
            self.chat_tab.set_current_conversation_file(saved_filepath)
            self.chat_tab.refresh_navigation()
        
        # Stop streaming and clean up
        self.on_message_finished()
        
        # Clean up worker thread
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
        print("[DEBUG] on_message_finished called")
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
        try:
            # Load the selected conversation
            self.chat_tab.load_conversation(filepath)
            
            # Update conversation service with loaded messages
            conversation, metadata = self.conversation_manager.load_conversation(filepath)
            self.conversation_service.conversation = conversation.copy()
            
            # Update status
            self.status_var = f"Loaded conversation: {metadata.get_display_info()}"
            self.status_bar.showMessage(self.status_var)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load conversation: {str(e)}")
    
    def on_conversation_deleted(self, filepath: str):
        """Handle conversation deletion from navigation"""
        try:
            # If the deleted conversation was the current one, clear the chat
            if (self.conversation_manager.get_current_metadata().current_conversation_file == filepath):
                self.conversation_service.clear_conversation()
                self.chat_tab.clear_chat()
                self.conversation_manager.clear_current_conversation()
            
            # Update status
            self.status_var = "Conversation deleted"
            self.status_bar.showMessage(self.status_var)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to handle conversation deletion: {str(e)}")
    
    def on_conversation_renamed(self, old_filepath: str, new_filepath: str):
        """Handle conversation rename from navigation"""
        try:
            # Update the current conversation file reference in the chat tab
            if self.conversation_manager.get_current_metadata().current_conversation_file == new_filepath:
                self.chat_tab.set_current_conversation_file(new_filepath)
            
            # Update status
            old_name = os.path.basename(old_filepath)
            new_name = os.path.basename(new_filepath)
            self.status_var = f"Renamed conversation: {old_name} → {new_name}"
            self.status_bar.showMessage(self.status_var)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to handle conversation rename: {str(e)}")
    
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
        self.status_var = f"Switched to {personality_name} personality"
        self.status_bar.showMessage(self.status_var)
    
    def on_model_operation_progress(self, message):
        """Handle model operation progress"""
        self.model_tab.append_status(message)
    
    def on_model_operation_error(self, error):
        """Handle model operation errors"""
        self.model_tab.append_status(f"Error: {error}")
        self.status_var = f"Error: {error}"
        self.status_bar.showMessage(self.status_var)
    
    def on_conversation_metadata_updated(self):
        """Handle conversation metadata updates"""
        metadata = self.conversation_manager.get_current_metadata()
        self.status_var = metadata.get_display_info()
        self.status_bar.showMessage(self.status_var)
    
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
        # Immediately start a new conversation without prompt
        # Clear in-memory conversation and UI
        self.conversation_service.clear_conversation()
        self.chat_tab.clear_chat()
        # Forcefully reset conversation manager metadata and file reference
        self.conversation_manager.clear_current_conversation()
        # Double-check: forcibly clear any lingering messages
        self.conversation_service.conversation = []
        # Optionally, reset conversation manager metadata object
        from SRC.models.conversation_metadata import ConversationMetadata
        self.conversation_manager.metadata = ConversationMetadata()
        
        # Refresh navigation widget
        self.chat_tab.refresh_navigation()
        self.chat_tab.set_current_conversation_file(None)
        
        self.status_var = "Started new conversation"
        self.status_bar.showMessage(self.status_var)
    
    def clear_chat(self):
        """Clear the chat display"""
        reply = QMessageBox.question(
            self, "Clear Chat", 
            "Clear the chat display? This will not affect the conversation history.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.chat_tab.clear_chat()
            self.status_var = "Chat display cleared"
            self.status_bar.showMessage(self.status_var)
    
    def save_chat(self):
        """Save the current chat to a file"""
        self.chat_tab.save_chat()
    
    def load_chat(self):
        """Load a chat from a file"""
        self.chat_tab.load_chat()
    
    def open_settings(self):
        """Open the settings dialog"""
        try:
            # Get available models and personalities for the settings dialog
            models = self.ollama_service.get_models() or ["llama2"]
            personalities = self.personality_tab.get_available_personalities() or ["assistant"]
            
            settings_dialog = SettingsDialog(
                self.config_manager, 
                models, 
                personalities, 
                self
            )
            
            if settings_dialog.exec() == SettingsDialog.Accepted:
                # Refresh models if settings changed
                self.refresh_models()
                self.status_var = "Settings updated"
                self.status_bar.showMessage(self.status_var)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open settings: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self, 
            "About Ollama Chat",
            "Ollama Chat\n\n"
            "A modern PySide6-based chat interface for Ollama.\n\n"
            "Features:\n"
            "• Multiple AI personalities\n"
            "• Model management\n"
            "• Conversation history\n"
            "• Spell checking\n"
            "• Dark theme\n\n"
            "Version: 1.0.0"
        )
    
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
            print(f"Error during close: {e}")
            event.accept()
    
    def showEvent(self, event):
        """Handle application show event"""
        super().showEvent(event)
        
        # Refresh models on first show
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
        
        # Refresh models on first show
        if not self.initialization_complete:
            return
            
        # Update window size from config
        width, height = self.config_manager.get_window_size()
        if width > 0 and height > 0:
            self.resize(width, height) 
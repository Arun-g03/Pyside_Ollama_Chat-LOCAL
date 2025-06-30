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
from SRC.ui.memory_tab import MemoryTab
from SRC.services.ollama_service import OllamaService
from SRC.services.conversation_service import ConversationService
from SRC.services.enhancement_service import EnhancementService
from SRC.services.memory_service import MemoryService
from SRC.models.conversation_metadata import ConversationManager
from SRC.config_manager import ConfigManager
from SRC.settings_dialog import SettingsDialog
from SRC.worker import Worker
from SRC.styles import dark_stylesheet, light_stylesheet
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

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
        self.is_new_conversation = False  # Track new conversation state
        
        # Setup timers
        self.setup_timers()
        
        # Mark initialization as complete
        self.initialization_complete = True
        
        # Initial model refresh
        self.refresh_models()
    
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
        
        # Conditionally add memory tab
        if self.memory_enabled:
            self.memory_tab = MemoryTab(self.memory_service)
            self.memory_tab.set_conversation_service(self.conversation_service)
            self.tabs.addTab(self.memory_tab, "Memory")
        else:
            self.memory_tab = None
        
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
            logger.debug(f"Error refreshing personalities: {e}",print_to_terminal=True)
    
    def on_models_updated(self, models):
        """Handle model list updates"""
        self.chat_tab.update_model_list(models)
        self.model_tab.update_model_list(models)
        self.status_var = f"Found {len(models)} models"
        self.status_bar.showMessage(self.status_var)
    
    def on_message_sent(self, message):
        """Handle new message sent from chat tab"""
        logger.debug(f"=== MESSAGE SENT START ===", print_to_terminal=True)
        logger.debug(f"Processing message: '{message}'", print_to_terminal=True)
        
        self.conversation_service.add_message("user", message)
        
        if self.memory_enabled and self.memory_service:
            # Use intelligent message addition
            result = self.memory_service.intelligent_add_message({"role": "user", "content": message})
            logger.debug(f"Memory addition result: {result}", print_to_terminal=True)
            
            # Only do LLM fact extraction for messages that didn't qualify for LTM storage
            if not result.get("ltm_qualified", False):
                logger.debug("Message didn't qualify for LTM, attempting LLM fact extraction", print_to_terminal=True)
                self.extract_and_store_facts(message)
            else:
                logger.debug("Message already qualified for LTM storage, skipping LLM fact extraction", print_to_terminal=True)
        
        self.send_to_ollama(message)
        logger.debug(f"=== MESSAGE SENT END ===", print_to_terminal=True)

    def extract_and_store_facts(self, message):
        """Extract facts from the message using LLM and store in long-term memory"""
        logger.debug(f"=== FACT STORAGE START ===", print_to_terminal=True)
        logger.debug(f"Processing message for fact storage: '{message}'", print_to_terminal=True)
        
        try:
            facts = self.extract_facts_with_llm(message)
            logger.debug(f"Extracted facts: {facts}", print_to_terminal=True)
            
            if facts and isinstance(facts, dict):
                logger.debug(f"Processing {len(facts)} facts for storage", print_to_terminal=True)
                stored_count = 0
                skipped_count = 0
                
                for key, value in facts.items():
                    logger.debug(f"Processing fact: key='{key}', value='{value}'", print_to_terminal=True)
                    
                    # Validate key and value before storing
                    if key and value and isinstance(key, str) and isinstance(value, str):
                        # Clean up the key and value
                        clean_key = key.strip()
                        clean_value = value.strip()
                        logger.debug(f"Cleaned fact: key='{clean_key}', value='{clean_value}'", print_to_terminal=True)
                        
                        if clean_key and clean_value:
                            logger.debug(f"Storing fact: {clean_key} = {clean_value}", print_to_terminal=True)
                            self.memory_service.add_fact(clean_key, clean_value)
                            stored_count += 1
                            logger.debug(f"Successfully stored fact #{stored_count}", print_to_terminal=True)
                        else:
                            logger.debug(f"Skipping fact - empty after cleaning", print_to_terminal=True)
                            skipped_count += 1
                    else:
                        logger.debug(f"Skipping invalid fact: key='{key}' (type: {type(key)}), value='{value}' (type: {type(value)})", print_to_terminal=True)
                        skipped_count += 1
                
                logger.debug(f"Fact storage complete: {stored_count} stored, {skipped_count} skipped", print_to_terminal=True)
            else:
                logger.debug("No valid facts extracted from message", print_to_terminal=True)
                logger.debug(f"Facts type: {type(facts)}, Facts value: {facts}", print_to_terminal=True)
        except Exception as e:
            logger.debug(f"Error in extract_and_store_facts: {e}", print_to_terminal=True)
            logger.debug(f"Exception type: {type(e)}", print_to_terminal=True)
        finally:
            logger.debug(f"=== FACT STORAGE END ===", print_to_terminal=True)

    def extract_facts_with_llm(self, message):
        """Use qwen3:0.6b to extract facts as key-value pairs from a message"""
        import json
        import re
        
        logger.debug(f"=== FACT EXTRACTION START ===", print_to_terminal=True)
        logger.debug(f"Input message: '{message}'", print_to_terminal=True)
        logger.debug(f"Message length: {len(message.strip())} characters", print_to_terminal=True)
        
        # Skip fact extraction for very short messages
        if len(message.strip()) < 5:
            logger.debug(f"Skipping fact extraction - message too short (< 10 chars)", print_to_terminal=True)
            return {}
            
        prompt = (
            "Extract any facts, preferences, or important information from the following message "
            "that should be remembered for future conversations. Return ONLY a valid JSON object with key-value pairs. "
            "If no facts are found, return an empty JSON object {}.\n\n"
            f"Message: \"{message}\""
        )
        
        logger.debug(f"Prompt sent to LLM: '{prompt}'", print_to_terminal=True)
        
        try:
            # Use OllamaService to call qwen3:0.6b
            logger.debug(f"Calling LLM with model: qwen3:0.6b", print_to_terminal=True)
            response_chunks = self.ollama_service.send_chat_message(
                model="qwen3:0.6b",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.0,
                stream=False
            )
            response = "".join(response_chunks).strip()
            
            # Log the raw response for debugging
            logger.debug(f"Raw LLM response: '{response}'", print_to_terminal=True)
            logger.debug(f"Response length: {len(response)} characters", print_to_terminal=True)
            
            # Handle empty response
            if not response:
                logger.debug("Fact extraction: Empty response from LLM", print_to_terminal=True)
                return {}
            
            # Try to extract JSON from the response (in case LLM adds extra text)
            logger.debug("Attempting to extract JSON from response...", print_to_terminal=True)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                logger.debug(f"JSON extracted using regex: '{json_str}'", print_to_terminal=True)
            else:
                # If no JSON found, try to parse the entire response
                json_str = response
                logger.debug(f"No JSON pattern found, using entire response: '{json_str}'", print_to_terminal=True)
            
            # Try to parse the JSON
            try:
                logger.debug("Attempting to parse JSON...", print_to_terminal=True)
                facts = json.loads(json_str)
                logger.debug(f"JSON parsed successfully, type: {type(facts)}", print_to_terminal=True)
                
                if isinstance(facts, dict):
                    logger.debug(f"Fact extraction successful: {facts}", print_to_terminal=True)
                    logger.debug(f"Number of facts extracted: {len(facts)}", print_to_terminal=True)
                    if facts:
                        for key, value in facts.items():
                            logger.debug(f"  Fact: '{key}' = '{value}'", print_to_terminal=True)
                    return facts
                else:
                    logger.debug(f"Fact extraction: Response is not a dict: {type(facts)}", print_to_terminal=True)
                    logger.debug(f"Response value: {facts}", print_to_terminal=True)
                    return {}
            except json.JSONDecodeError as json_error:
                logger.debug(f"Fact extraction JSON decode error: {json_error}", print_to_terminal=True)
                logger.debug(f"Error position: {json_error.pos}", print_to_terminal=True)
                logger.debug(f"Error line: {json_error.lineno}, column: {json_error.colno}", print_to_terminal=True)
                logger.debug(f"Attempted to parse: '{json_str}'", print_to_terminal=True)
                return {}
                
        except Exception as e:
            logger.debug(f"Fact extraction failed with exception: {e}", print_to_terminal=True)
            logger.debug(f"Exception type: {type(e)}", print_to_terminal=True)
            return {}
        finally:
            logger.debug(f"=== FACT EXTRACTION END ===", print_to_terminal=True)

    def send_to_ollama(self, message):
        """Send message to Ollama and handle response asynchronously"""
        messages = self.conversation_service.get_messages()
        if not messages or messages[-1].get("role") != "user" or messages[-1].get("content") != message:
            self.conversation_service.add_message("user", message)
            messages = self.conversation_service.get_messages()
        
        logger.debug(f"DEBUG: Messages before sending: {messages}",print_to_terminal=True)
        
        # Use STM+LTM context if memory enabled
        if self.memory_enabled and self.memory_service:
            # Pass the current message as query for intelligent memory retrieval
            context_messages = self.memory_service.get_context_messages(current_query=message)
        else:
            context_messages = messages
        logger.debug(f"DEBUG: Context messages with memory: {len(context_messages)} total messages",print_to_terminal=True)
        
        # Detect if this is a new conversation
        is_new_conversation = False
        if context_messages:
            # Check if this is the first user message in a conversation
            user_messages = [msg for msg in context_messages if msg.get("role") == "user"]
            if len(user_messages) <= 1:  # Only current message or first message
                is_new_conversation = True
                logger.debug("Detected new conversation", print_to_terminal=True)
        
        # Use the explicit new conversation flag if set
        if self.is_new_conversation:
            is_new_conversation = True
            logger.debug("Using explicit new conversation flag", print_to_terminal=True)
        
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
            logger.debug(f"System prompt added (length: {len(system_prompt)} chars)", print_to_terminal=True)
        
        # Add user context messages
        final_context.extend(user_context_messages)
        if user_context_messages:
            logger.debug(f"Added {len(user_context_messages)} user context messages", print_to_terminal=True)
        
        # Add conversation messages
        final_context.extend(filtered_context)
        
        context_messages = final_context
        
        # Reset new conversation flag after processing
        if self.is_new_conversation:
            self.is_new_conversation = False
            logger.debug("Reset new conversation flag", print_to_terminal=True)
        
        # Log the final context being sent to AI
        logger.debug(f"Final context being sent to AI ({len(context_messages)} messages):", print_to_terminal=True)
        for i, msg in enumerate(context_messages):
            role = msg.get("role", "unknown")
            content_preview = msg.get("content", "")[:100] + "..." if len(msg.get("content", "")) > 100 else msg.get("content", "")
            logger.debug(f"  {i+1}. {role}: {content_preview}", print_to_terminal=True)
        
        # Get current model
        model = self.chat_tab.get_current_model()
        available_models = self.ollama_service.get_models() or []
        chosen_model = model
        
        # Auto model selection using complexity checker
        if model == "Auto":
            from SRC.utils.complexity_analyzer import RequestComplexityAnalyzer
            analyzer = RequestComplexityAnalyzer()
            # Use only the last user message for complexity
            complexity_metrics = analyzer.analyze_complexity(message, context_messages)
            chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
            # Insert a system message about the chosen model (after user message, before AI response)
            system_info = f"Using model {chosen_model} (auto-selected based on request complexity)"
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
        final_response = self.chat_tab.get_current_response()
        self.conversation_service.add_message("assistant", final_response)
        if self.memory_enabled and self.memory_service:
            # Use intelligent message addition for assistant responses
            result = self.memory_service.intelligent_add_message({"role": "assistant", "content": final_response})
            logger.debug(f"Assistant response memory addition result: {result}", print_to_terminal=True)
        logger.info(f"AI: {final_response}")
        saved_filepath = self.conversation_manager.auto_save_conversation(
            self.conversation_service.get_messages()
        )
        if saved_filepath:
            self.chat_tab.set_current_conversation_file(saved_filepath)
            self.chat_tab.refresh_navigation()
        self.chat_tab.streaming_handler.finalize_streaming_message()
        self.on_message_finished()
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
        logger.debug("[DEBUG] on_message_finished called")
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
        logger.debug(f"=== NEW CONVERSATION START ===", print_to_terminal=True)
        """Start a new conversation"""
        # Set new conversation flag
        self.is_new_conversation = True
        
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
                self.setup_ui()
                self.setup_connections()
                self.refresh_models()
            else:
                self.setup_services()
                self.setup_connections()
                self.refresh_models()
    
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
            logger.debug(f"Error during close: {e}",print_to_terminal=True)
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
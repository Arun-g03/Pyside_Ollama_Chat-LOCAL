"""
Event Handler - Manages signal connections and event handling
"""

from PySide6.QtCore import QTimer
from typing import Optional, Callable
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class EventHandler:
    """Manages signal connections and event handling"""
    
    def __init__(self, main_window, service_manager, ui_manager, chat_controller):
        self.main_window = main_window
        self.service_manager = service_manager
        self.ui_manager = ui_manager
        self.chat_controller = chat_controller
        self.worker_thread = None
        self.worker = None
        self._current_response_model = None
        self._tts_finished = False  # Track TTS completion
        
        # Timer for delayed operations
        self.model_update_timer = QTimer()
        self.model_update_timer.setSingleShot(True)
        
        # State tracking
        self.model_change_in_progress = False
        self.ollama_error_shown = False
        
        # Setup connections
        self.setup_connections()
        
    def setup_connections(self):
        """Setup all signal connections between components"""
        try:
            # Connect controller signals
            self.chat_controller.status_updated.connect(self._on_status_updated)
            self.chat_controller.error_occurred.connect(self._on_error_occurred)
            self.chat_controller.conversation_updated.connect(self._on_conversation_updated)
            self.chat_controller.name_generation_requested.connect(self._on_name_generation_requested)
            
            # Connect Ollama service signals
            ollama_service = self.service_manager.get_ollama_service()
            ollama_service.model_list_updated.connect(self._on_models_updated)
            ollama_service.model_operation_progress.connect(self._on_model_operation_progress)
            ollama_service.model_operation_error.connect(self._on_model_operation_error)
            
            # Connect chat tab signals
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.message_sent.connect(self._on_message_sent)
                chat_tab.message_cancelled.connect(self._on_message_cancelled)
                chat_tab.conversation_selected.connect(self._on_conversation_selected)
                chat_tab.conversation_deleted.connect(self._on_conversation_deleted)
                chat_tab.conversation_renamed.connect(self._on_conversation_renamed)
                chat_tab.new_conversation_requested.connect(self._on_new_conversation_requested)
                # Connect append_response_signal to handle streaming chunks in main thread
                chat_tab.append_response_signal.connect(chat_tab.append_response_chunk)
            
            # Connect model tab signals
            model_tab = self.ui_manager.get_model_tab()
            if model_tab:
                model_tab.model_pull_requested.connect(ollama_service.pull_model)
                model_tab.model_remove_requested.connect(ollama_service.remove_model)
                model_tab.model_update_requested.connect(ollama_service.update_model)
            
            # Connect personality tab signals
            personality_tab = self.ui_manager.get_personality_tab()
            if personality_tab:
                personality_tab.personality_changed.connect(self._on_personality_changed)
            
            # Connect conversation manager signals
            conversation_manager = self.service_manager.get_conversation_manager()
            conversation_manager.metadata_updated.connect(self._on_conversation_metadata_updated)
            
            # Connect menu actions
            self._connect_menu_actions()
            
            # Connect timer
            self.model_update_timer.timeout.connect(self._on_delayed_model_update)
            
            logger.info("[ID:0322] All signal connections established successfully")
            
        except Exception as e:
            logger.error(f"[ID:0321] Error setting up connections: {e}")
            raise
    
    def _connect_menu_actions(self):
        """Connect menu actions to their handlers"""
        try:
            # File menu actions
            new_conversation_action = self.ui_manager.get_menu_action('new_conversation')
            if new_conversation_action:
                new_conversation_action.triggered.connect(self._on_new_conversation)
            
            clear_chat_action = self.ui_manager.get_menu_action('clear_chat')
            if clear_chat_action:
                clear_chat_action.triggered.connect(self._on_clear_chat)
            
            save_chat_action = self.ui_manager.get_menu_action('save_chat')
            if save_chat_action:
                save_chat_action.triggered.connect(self._on_save_chat)
            
            load_chat_action = self.ui_manager.get_menu_action('load_chat')
            if load_chat_action:
                load_chat_action.triggered.connect(self._on_load_chat)
            
            exit_action = self.ui_manager.get_menu_action('exit')
            if exit_action:
                exit_action.triggered.connect(self.main_window.close)
            
            # Edit menu actions
            settings_action = self.ui_manager.get_menu_action('settings')
            if settings_action:
                settings_action.triggered.connect(self._on_open_settings)
            
            # Tools menu actions
            refresh_models_action = self.ui_manager.get_menu_action('refresh_models')
            if refresh_models_action:
                refresh_models_action.triggered.connect(self._on_refresh_models)
            
            # Help menu actions
            about_action = self.ui_manager.get_menu_action('about')
            if about_action:
                about_action.triggered.connect(self._on_show_about)
                
        except Exception as e:
            logger.error(f"[ID:0320] Error connecting menu actions: {e}")
    
    def _on_status_updated(self, message: str):
        """Handle status updates from controller"""
        self.ui_manager.update_status(message)
    
    def _on_error_occurred(self, error_message: str):
        """Handle errors from controller"""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self.main_window, "Error", error_message)
    
    def _on_conversation_updated(self):
        """Handle conversation updates from controller"""
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.refresh_navigation()
    
    def _on_name_generation_requested(self, filepath: str):
        """Handle name generation request from controller"""
        logger.info(f"[ID:0319] Name generation requested for: {filepath}")
        
        summarization_service = self.service_manager.get_summarization_service()
        if summarization_service:
            try:
                # Load the conversation
                conversation_manager = self.service_manager.get_conversation_manager()
                conversation, metadata = conversation_manager.load_conversation(filepath)
                logger.info(f"[ID:0318] Loaded conversation with {len(conversation)} messages")
                logger.info(f"[ID:0317] Current AI name: {metadata.ai_generated_name}")
                
                # Only generate name if we don't already have one
                if not metadata.ai_generated_name:
                    logger.info("[ID:0316] No AI name exists, triggering generation...")
                    summarization_service.generate_chat_name(conversation, filepath)
                else:
                    logger.info(f"[ID:0315] AI name already exists: {metadata.ai_generated_name}")
                    
            except Exception as e:
                logger.error(f"[ID:0314] Error triggering name generation: {str(e)}")
        else:
            logger.warning("[ID:0313] No summarization service available")
    
    def _on_models_updated(self, models):
        """Handle model list updates"""
        chat_tab = self.ui_manager.get_chat_tab()
        model_tab = self.ui_manager.get_model_tab()
        
        if chat_tab:
            chat_tab.update_model_list(models)
        if model_tab:
            model_tab.update_model_list(models)
        
        from pyside_chat.utils.prompts import PromptFormatter
        status_msg = PromptFormatter.format_status_message("models_found", count=len(models))
        self.ui_manager.update_status(status_msg)
    
    def _on_message_sent(self, message):
        """Handle new message sent from chat tab"""
        # Get current model and temperature from chat tab
        chat_tab = self.ui_manager.get_chat_tab()
        if not chat_tab:
            return
            
        model = chat_tab.get_current_model()
        temperature = chat_tab.get_temperature()
        
        # Process message through controller
        self.chat_controller.process_user_message(message, model, temperature)
        
        # Send to Ollama for actual processing
        self._send_to_ollama(message, model, temperature)
    
    def _send_to_ollama(self, message, model, temperature):
        """Send message to Ollama and handle response asynchronously"""
        # Check Ollama connection
        if not self._check_ollama_connection():
            self._show_ollama_connection_error("message", force_show=True)
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.append_to_chat("System", "Failed to send: Could not connect to Ollama.\n Please check the Ollama connection and try again.")
                chat_tab.stop_streaming()
            return
        
        # Get conversation service and messages
        conversation_service = self.service_manager.get_conversation_service()
        messages = conversation_service.get_messages()
        
        # Use STM+LTM context if memory enabled
        memory_service = self.service_manager.get_memory_service()
        if self.chat_controller.is_memory_active() and memory_service:
            context_messages = memory_service.get_context_messages(current_query=message)
        else:
            context_messages = messages
        
        # Build system prompt and context
        personality_tab = self.ui_manager.get_personality_tab()
        if personality_tab and personality_tab.personality_model:
            system_prompt = personality_tab.personality_model.build_comprehensive_system_prompt(memory_service)
            user_context_messages = personality_tab.personality_model.get_user_context_messages(
                memory_service, self.chat_controller.is_new_conversation
            )
        else:
            system_prompt = ""
            user_context_messages = []
        
        # Filter out existing system messages
        filtered_context = [msg for msg in context_messages if msg.get("role") != "system"]
        
        # Build final context
        final_context = []
        if system_prompt:
            final_context.append({"role": "system", "content": system_prompt})
        final_context.extend(user_context_messages)
        final_context.extend(filtered_context)
        
        context_messages = final_context
        
        # Reset new conversation flag
        if self.chat_controller.is_new_conversation:
            self.chat_controller.is_new_conversation = False
        
        # Get available models and handle auto selection
        ollama_service = self.service_manager.get_ollama_service()
        available_models = ollama_service.get_models() or []
        chosen_model = model
        
        # Update conversation metadata
        conversation_manager = self.service_manager.get_conversation_manager()
        if model != "Auto":
            conversation_manager.get_current_metadata().update_model(chosen_model)
        
        # Auto model selection
        if model == "Auto":
            from pyside_chat.utils.complexity_analyzer import RequestComplexityAnalyzer
            from pyside_chat.utils.prompts import PromptFormatter
            
            analyzer = RequestComplexityAnalyzer()
            complexity_metrics = analyzer.analyze_complexity(message, context_messages)
            chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
            
            # Insert system message about chosen model
            system_info = PromptFormatter.format_auto_model_selection_info(chosen_model)
            conversation_service.add_message("system", system_info)
            
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.append_to_chat("System", system_info)
            
            context_messages = conversation_service.get_context_messages()
        
        # Update conversation metadata with chosen model
        conversation_manager.get_current_metadata().update_model(chosen_model)
        
        # Create worker thread for async communication
        self._create_worker_thread(context_messages, chosen_model, temperature)
    
    def _create_worker_thread(self, context_messages, chosen_model, temperature):
        """Create and start worker thread for Ollama communication"""
        from PySide6.QtCore import QThread, Qt
        from pyside_chat.services.worker.worker import Worker
        
        # Create worker thread
        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        
        # Store the chosen model for this response
        self._current_response_model = chosen_model
        
        # Connect worker signals with QueuedConnection for thread safety
        self.worker.stream_chunk_signal.connect(self._on_worker_chunk, Qt.ConnectionType.QueuedConnection)
        self.worker.finished_signal.connect(self._on_worker_finished, Qt.ConnectionType.QueuedConnection)
        self.worker.update_message_signal.connect(self._on_worker_error, Qt.ConnectionType.QueuedConnection)
        
        # Connect thread signals
        config_manager = self.service_manager.config_manager
        self.worker_thread.started.connect(
            lambda: self.worker.run_stream(
                context_messages,
                chosen_model,
                temperature,
                config_manager.get_ollama_url(),
                config_manager.get_max_tokens(),
                config_manager.get_top_p(),
                config_manager.get_frequency_penalty(),
                config_manager.get_presence_penalty(),
            )
        )
        
        # Start the worker thread
        self.worker_thread.start()
    
    def _on_worker_chunk(self, chunk):
        """Handle worker chunk signal"""
        self.chat_controller.accumulate_assistant_response(chunk)
        
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.append_response_signal.emit(chunk, self._current_response_model)
    
    def _on_worker_finished(self):
        """Handle worker completion"""
        logger.debug("[ID:0312] Worker finished")
        
        # Mark worker as finished
        if hasattr(self, 'worker'):
            self.worker = None
        
        # Only clean up if TTS is also finished
        if self._tts_finished:
            logger.debug("[ID:0311] Both worker and TTS finished, cleaning up")
            self._cleanup_worker_thread()
        else:
            logger.debug("[ID:0310] Worker finished but TTS still running, waiting for TTS")
            # TTS will call cleanup when it finishes
    
    def _on_tts_finished(self):
        """Handle TTS completion"""
        logger.debug("[ID:0309] TTS finished signal received")
        self._tts_finished = True
        
        # Use QTimer.singleShot to ensure this runs in the main thread
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self._handle_tts_finished_delayed)
    
    def _handle_tts_finished_delayed(self):
        """Handle TTS finished with a delay to ensure proper coordination"""
        try:
            # Check if worker thread is still running
            if hasattr(self, 'worker_thread') and self.worker_thread and self.worker_thread.isRunning():
                logger.debug("[ID:0308] Worker thread still running, waiting for it to finish")
                # Don't clean up yet - let the worker finish naturally
                # The worker will call cleanup when it finishes
                return
            else:
                logger.debug("[ID:0307] Worker thread not running, cleaning up immediately")
                self._cleanup_worker_thread()
        except Exception as e:
            logger.error(f"[ID:0306] Error in delayed TTS finished handling: {e}")
            # Force cleanup on error
            self._cleanup_worker_thread()
    
    def _cleanup_worker_thread(self):
        """Clean up worker thread safely in the main thread"""
        # Only clean up if both worker and TTS are finished
        if not self._tts_finished:
            # TTS not finished yet, wait a bit more but don't recurse
            from PySide6.QtCore import QTimer
            QTimer.singleShot(500, self._cleanup_worker_thread_once)
            return
            
        self._cleanup_worker_thread_once()
    
    def _cleanup_worker_thread_once(self):
        """Clean up worker thread once without recursion"""
        if hasattr(self, 'worker_thread'):
            try:
                # First stop the worker if it's running
                if hasattr(self, 'worker') and self.worker:
                    try:
                        self.worker.stop()
                    except Exception as e:
                        logger.error(f"[ID:0305] Error stopping worker: {e}")
                
                if self.worker_thread and self.worker_thread.isRunning():
                    # Try to quit gracefully first
                    self.worker_thread.quit()
                    
                    # Use a shorter timeout to avoid blocking the UI
                    if not self.worker_thread.wait(2000):  # 2 second timeout
                        logger.warning("[ID:0304] Worker thread did not quit within timeout, marking for deletion")
                        # Don't use terminate() as it can cause crashes
                        # Instead, just mark it for deletion and let it finish naturally
                        self.worker_thread.deleteLater()
                    else:
                        logger.debug("[ID:0303] Worker thread quit successfully")
                        self.worker_thread.deleteLater()
                else:
                    logger.debug("[ID:0302] Worker thread not running, cleaning up")
                    if self.worker_thread:
                        self.worker_thread.deleteLater()
                        
            except Exception as e:
                logger.error(f"[ID:0301] Error cleaning up worker thread: {e}")
            finally:
                # Always clean up references
                if hasattr(self, 'worker_thread'):
                    self.worker_thread = None
                if hasattr(self, 'worker'):
                    self.worker = None
                self._tts_finished = False  # Reset for next time
                
                # Reset streaming state in chat tab
                chat_tab = self.ui_manager.get_chat_tab()
                if chat_tab:
                    chat_tab.stop_streaming()
    
    def _on_worker_error(self, error_message):
        """Handle worker error"""
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.append_to_chat("System", f"Error: {error_message}")
            chat_tab.force_enable_send_button()
        
        self._on_worker_finished()
    
    def _on_message_finished(self):
        """Handle message finished"""
        from pyside_chat.utils.Logging.logging_helpers import LoggingHelpers
        LoggingHelpers.log_debug("on_message_finished called")
        
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.stop_streaming()
    
    def _on_message_cancelled(self):
        """Handle message cancellation"""
        # Cancel the Ollama service request
        ollama_service = self.service_manager.get_ollama_service()
        ollama_service.cancel_request()
        
        # Stop the worker thread if it's running using safe cleanup
        if hasattr(self, 'worker_thread') and self.worker_thread.isRunning():
            from PySide6.QtCore import QTimer
            QTimer.singleShot(0, self._cleanup_worker_thread_once)
        
        # Update the chat tab
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.on_message_cancelled()
            chat_tab.force_enable_send_button()
    
    def _on_conversation_selected(self, filepath: str):
        """Handle conversation selection from navigation"""
        self.chat_controller.load_conversation(filepath)
        
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.load_conversation(filepath)
    
    def _on_conversation_deleted(self, filepath: str):
        """Handle conversation deletion from navigation"""
        self.chat_controller.delete_conversation(filepath)
    
    def _on_conversation_renamed(self, old_filepath: str, new_filepath: str):
        """Handle conversation rename from AI naming"""
        try:
            # Update the chat tab's current conversation file reference
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab and chat_tab.current_conversation_file == old_filepath:
                chat_tab.set_current_conversation_file(new_filepath)
            
            # Update the conversation manager's current file reference
            conversation_manager = self.service_manager.get_conversation_manager()
            if conversation_manager.get_current_metadata().current_conversation_file == old_filepath:
                conversation_manager.get_current_metadata().current_conversation_file = new_filepath
            
            logger.info(f"[ID:0300] Conversation renamed: {old_filepath} -> {new_filepath}")
            
            # Refresh navigation to show updated AI-generated name
            if chat_tab:
                chat_tab.refresh_navigation()
                
        except Exception as e:
            logger.error(f"[ID:0299] Error handling conversation rename: {str(e)}")
    
    def _on_personality_changed(self, personality_name):
        """Handle personality changes"""
        # Update conversation metadata
        conversation_manager = self.service_manager.get_conversation_manager()
        conversation_manager.get_current_metadata().update_personality(personality_name)
        
        # Clear conversation
        conversation_service = self.service_manager.get_conversation_service()
        conversation_service.clear_conversation()
        
        # Clear chat display
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.clear_chat()
            chat_tab.on_personality_changed(personality_name)
            
            # Sync personality selection in chat tab
            if hasattr(chat_tab, 'personality_combo'):
                chat_tab.personality_combo.setCurrentText(personality_name)
        
        # Show status
        from pyside_chat.utils.prompts import PromptFormatter
        status_msg = PromptFormatter.format_status_message("personality_switched", personality=personality_name)
        self.ui_manager.update_status(status_msg)
    
    def _on_model_operation_progress(self, message):
        """Handle model operation progress"""
        model_tab = self.ui_manager.get_model_tab()
        if model_tab:
            model_tab.append_status(message)
    
    def _on_model_operation_error(self, error):
        """Handle model operation errors"""
        model_tab = self.ui_manager.get_model_tab()
        if model_tab:
            model_tab.append_status(f"Error: {error}")
        
        from pyside_chat.utils.prompts import PromptFormatter
        status_msg = PromptFormatter.format_status_message("model_operation_error", error=error)
        self.ui_manager.update_status(status_msg)
        
        # Show user-friendly error dialog for connection issues
        if "Cannot connect to Ollama" in error or "connection" in error.lower():
            self._show_ollama_connection_error("operation")
    
    def _on_conversation_metadata_updated(self):
        """Handle conversation metadata updates"""
        conversation_manager = self.service_manager.get_conversation_manager()
        metadata = conversation_manager.get_current_metadata()
        self.ui_manager.update_status(metadata.get_display_info())
    
    def _on_new_conversation_requested(self):
        """Handle new conversation request"""
        self._on_new_conversation()
    
    def _on_new_conversation(self):
        """Start a new conversation"""
        from pyside_chat.utils.Logging.logging_helpers import LoggingHelpers
        LoggingHelpers.log_debug("=== NEW CONVERSATION START ===")
        
        self.chat_controller.start_new_conversation()
        
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.clear_chat()
            chat_tab.refresh_navigation()
            
            # Set the current conversation file to the one from the controller
            conversation_manager = self.service_manager.get_conversation_manager()
            current_file = conversation_manager.get_current_metadata().current_conversation_file
            chat_tab.set_current_conversation_file(current_file)
    
    def _on_clear_chat(self):
        """Clear the chat display"""
        if self.ui_manager.show_clear_chat_dialog():
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.clear_chat()
            
            from pyside_chat.utils.prompts import PromptFormatter
            status_msg = PromptFormatter.format_status_message("chat_cleared")
            self.ui_manager.update_status(status_msg)
    
    def _on_save_chat(self):
        """Save the current chat to a file"""
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.save_chat()
    
    def _on_load_chat(self):
        """Load a chat from a file"""
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.load_chat()
    
    def _on_open_settings(self):
        """Open the settings dialog"""
        from pyside_chat.ui.Widgets.settings_dialog import SettingsDialog
        
        # Get current lists
        ollama_service = self.service_manager.get_ollama_service()
        models = ollama_service.get_models() or ["llama2"]
        
        personality_tab = self.ui_manager.get_personality_tab()
        personalities = personality_tab.personality_model.get_available_personalities() or ["assistant"]
        
        dialog = SettingsDialog(self.service_manager.config_manager, models, personalities, self.main_window)
        if dialog.exec():
            # Check if memory settings changed
            memory_enabled_now = self.service_manager.config_manager.get("memory_enabled", True)
            if memory_enabled_now != self.service_manager.is_memory_enabled():
                # Reinitialize services
                self.service_manager.reinitialize_services()
                self.chat_controller = self._create_chat_controller()
                self._setup_ui_with_new_services()
                self._on_refresh_models()
            else:
                self.service_manager.reinitialize_services()
                self.chat_controller = self._create_chat_controller()
                self._setup_connections()
                self._on_refresh_models()
    
    def _create_chat_controller(self):
        """Create a new chat controller with current services"""
        from pyside_chat.controllers.chat_controller import ChatController
        
        return ChatController(
            ollama_service=self.service_manager.get_ollama_service(),
            conversation_service=self.service_manager.get_conversation_service(),
            enhancement_service=self.service_manager.get_enhancement_service(),
            memory_service=self.service_manager.get_memory_service(),
            conversation_manager=self.service_manager.get_conversation_manager()
        )
    
    def _setup_ui_with_new_services(self):
        """Setup UI with new services after configuration change"""
        # This would need to be implemented based on your UI structure
        # For now, we'll just re-setup connections
        self._setup_connections()
    
    def _on_refresh_models(self):
        """Refresh the list of available models"""
        try:
            ollama_service = self.service_manager.get_ollama_service()
            models = ollama_service.get_models()
            if models:
                self.ollama_error_shown = False  # Reset error flag on success
                
                chat_tab = self.ui_manager.get_chat_tab()
                model_tab = self.ui_manager.get_model_tab()
                
                if chat_tab:
                    chat_tab.update_model_list(models)
                if model_tab:
                    model_tab.update_model_list(models)
            else:
                # No models returned - likely Ollama is not running
                self._show_ollama_connection_error("startup")
        except Exception as e:
            logger.error(f"[ID:0298] Error refreshing models: {e}")
            self._show_ollama_connection_error("startup")
        
        # Also refresh personalities
        self._on_refresh_personalities()
    
    def _on_refresh_personalities(self):
        """Refresh the list of available personalities"""
        try:
            personality_tab = self.ui_manager.get_personality_tab()
            if personality_tab:
                personalities = personality_tab.get_available_personalities()
                if personalities:
                    chat_tab = self.ui_manager.get_chat_tab()
                    if chat_tab:
                        chat_tab.update_personality_list(personalities)
        except Exception as e:
            from pyside_chat.utils.Logging.logging_helpers import LoggingHelpers
            LoggingHelpers.log_error("refresh_personalities", e)
    
    def _on_show_about(self):
        """Show about dialog"""
        self.ui_manager.show_about_dialog()
    
    def _on_delayed_model_update(self):
        """Delayed model update to ensure UI is ready"""
        try:
            # Update session variables for new model
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                current_model = chat_tab.get_current_model()
                if current_model:
                    session_variables = self.service_manager.get_session_variables()
                    session_variables['model'] = current_model
                    
                    conversation_manager = self.service_manager.get_conversation_manager()
                    conversation_manager.get_current_metadata().update_model(current_model)
        finally:
            self.model_change_in_progress = False
    
    def _check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        ollama_service = self.service_manager.get_ollama_service()
        return ollama_service.test_connection()
    
    def _show_ollama_connection_error(self, context="general", force_show=False):
        """Show a user-friendly error dialog when Ollama is not running"""
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QMessageBox
        
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
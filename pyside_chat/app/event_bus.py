# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *


"""
Event Bus - Manages signal connections and event handling
"""

logger = CustomLogger.get_logger(__name__)
logger.info("Starting Event Bus", print_to_terminal=True)


class EventBus:
    """Manages signal connections and event handling"""

    def __init__(self, main_window, service_manager, ui_manager, chat_controller, lifecycle_manager=None):
        self.main_window = main_window
        self.service_manager = service_manager
        self.ui_manager = ui_manager
        self.chat_controller = chat_controller
        self.lifecycle_manager = lifecycle_manager

        # Set EventBus reference in ChatController to prevent duplicate message processing
        self.chat_controller.set_event_bus_reference(self)

        # Initialize threading service for new architecture
        self.threading_service = get_global_threading_service()

        # Connect threading service signals to event bus handlers
        self.threading_service.chunk_received.connect(self._on_worker_chunk)
        self.threading_service.progress_updated.connect(
            self._on_worker_progress)
        self.threading_service.finished.connect(self._on_worker_finished)
        self.threading_service.error.connect(self._on_worker_error)

        self._current_response_model = None
        self._tts_finished = False  # Track TTS completion

        # Timer for delayed operations
        self.model_update_timer = QTimer()
        self.model_update_timer.setSingleShot(True)

        # State tracking
        self.model_change_in_progress = False
        self.ollama_error_shown = False

        # Chat tab retry mechanism
        self._chat_tab_retry_count = 0
        self._max_chat_tab_retries = 5
        self._chat_tab_retry_timer = QTimer()
        self._chat_tab_retry_timer.setSingleShot(True)
        self._chat_tab_retry_timer.timeout.connect(
            self._retry_chat_tab_connection)

        # Flag to prevent duplicate signal connections
        self._chat_tab_signals_connected = False

        # Note: setup_connections() is now called explicitly after UI setup

    def setup_connections(self):
        """Setup all signal connections between components"""
        try:
            # Connect controller signals
            self.chat_controller.status_updated.connect(
                self._on_status_updated)
            self.chat_controller.error_occurred.connect(
                self._on_error_occurred)
            self.chat_controller.conversation_updated.connect(
                self._on_conversation_updated)
            self.chat_controller.name_generation_requested.connect(
                self._on_name_generation_requested)
            self.chat_controller.message_received.connect(
                self._on_message_received)
            # NOTE: Removed chat_controller.message_sent connection to prevent duplicate message processing

            # Connect Ollama service signals
            ollama_service = self.service_manager.get_ollama_service()
            ollama_service.model_list_updated.connect(self._on_models_updated)
            ollama_service.model_operation_progress.connect(
                self._on_model_operation_progress)
            ollama_service.model_operation_error.connect(
                self._on_model_operation_error)

            # Connect chat tab signals with better error handling
            self._connect_chat_tab_signals()

            # Connect model tab signals
            model_tab = self.ui_manager.get_model_tab()
            if model_tab:
                model_tab.model_pull_requested.connect(
                    ollama_service.pull_model)
                model_tab.model_remove_requested.connect(
                    ollama_service.remove_model)
                model_tab.model_update_requested.connect(
                    ollama_service.update_model)

            # Connect personality tab signals
            personality_tab = self.ui_manager.get_personality_tab()
            if personality_tab:
                personality_tab.personality_changed.connect(
                    self._on_personality_changed)

            # Connect conversation manager signals
            conversation_manager = self.service_manager.get_conversation_manager()
            conversation_manager.metadata_updated.connect(
                self._on_conversation_metadata_updated)

            # Connect conversation service auto-save signal
            conversation_service = self.service_manager.get_conversation_service()
            conversation_service.auto_save_completed.connect(
                self._on_auto_save_completed)
            logger.debug("[EVENT_BUS] Connected auto_save_completed signal")

            # Connect menu actions
            self._connect_menu_actions()

            # Connect timer
            self.model_update_timer.timeout.connect(
                self._on_delayed_model_update)

            logger.info(
                "[ID:0223] All signal connections established successfully")

        except Exception as e:
            logger.error(f"[ID:0222] Error setting up connections: {e}")
            raise

    def _setup_chat_tab_retry(self):
        """Set up chat tab signal connections with a retry mechanism."""
        if self._chat_tab_retry_count >= self._max_chat_tab_retries:
            logger.error(
                f"[EVENT ERROR] Maximum chat tab retry attempts ({self._max_chat_tab_retries}) reached. Giving up.")
            return

        self._chat_tab_retry_count += 1
        logger.debug(
            f"[EVENT DEBUG] Retrying chat tab signal connection (attempt {self._chat_tab_retry_count}/{self._max_chat_tab_retries})...")

        # Schedule retry after a delay
        self._chat_tab_retry_timer.start(1000)  # 1 second delay

    def _retry_chat_tab_connection(self):
        """Attempt to connect to chat tab after delay."""
        try:
            # Check if signals are already connected
            if self._chat_tab_signals_connected:
                logger.debug(
                    "[EVENT DEBUG] Chat tab signals already connected, skipping retry")
                return

            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                logger.debug(
                    "[EVENT DEBUG] Chat tab is now available, connecting signals.")
                # Use the same connection method to ensure consistency and avoid duplicates
                self._connect_chat_tab_signals()
                logger.debug(
                    "[EVENT DEBUG] All chat tab signals connected successfully after retry.")
            else:
                logger.debug(
                    f"[EVENT DEBUG] Chat tab still not available (attempt {self._chat_tab_retry_count}/{self._max_chat_tab_retries}), will retry again.")
                # Schedule another retry
                self._setup_chat_tab_retry()
        except Exception as e:
            logger.error(
                f"[EVENT ERROR] Error in _retry_chat_tab_connection: {e}")
            # Don't retry on error, just log it

    def _connect_menu_actions(self):
        """Connect menu actions to their handlers"""
        try:
            # File menu actions
            new_conversation_action = self.ui_manager.get_menu_action(
                'new_conversation')
            if new_conversation_action:
                new_conversation_action.triggered.connect(
                    self._on_new_conversation)

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
            refresh_models_action = self.ui_manager.get_menu_action(
                'refresh_models')
            if refresh_models_action:
                refresh_models_action.triggered.connect(
                    self._on_refresh_models)

            # Help menu actions
            about_action = self.ui_manager.get_menu_action('about')
            if about_action:
                about_action.triggered.connect(self._on_show_about)

        except Exception as e:
            logger.error(f"[ID:0221] Error connecting menu actions: {e}")

    def _connect_chat_tab_signals(self):
        """Connect chat tab signals with proper error handling"""
        try:
            # Check if signals are already connected to prevent duplicates
            if self._chat_tab_signals_connected:
                logger.debug(
                    "[EVENT DEBUG] Chat tab signals already connected, skipping")
                return

            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                logger.debug("[EVENT DEBUG] Connecting chat tab signals...")

                # CRITICAL FIX: Disconnect any existing connections first to prevent duplicates
                def safe_disconnect(signal):
                    try:
                        if signal and hasattr(signal, 'disconnect'):
                            # Check if signal has any connections before disconnecting
                            if hasattr(signal, 'receivers') and signal.receivers() > 0:
                                signal.disconnect()
                            else:
                                logger.debug(
                                    "[EVENT DEBUG] Signal has no receivers, skipping disconnect")
                    except TypeError:
                        # No existing connection, safe to ignore
                        pass
                    except Exception as e:
                        logger.debug(f"[EVENT DEBUG] Safe disconnect: {e}")

                # Only disconnect if signals exist
                if hasattr(chat_tab, 'message_sent') and chat_tab.message_sent:
                    safe_disconnect(chat_tab.message_sent)
                if hasattr(chat_tab, 'message_cancelled') and chat_tab.message_cancelled:
                    safe_disconnect(chat_tab.message_cancelled)
                if hasattr(chat_tab, 'conversation_selected') and chat_tab.conversation_selected:
                    safe_disconnect(chat_tab.conversation_selected)
                if hasattr(chat_tab, 'conversation_deleted') and chat_tab.conversation_deleted:
                    safe_disconnect(chat_tab.conversation_deleted)
                if hasattr(chat_tab, 'conversation_renamed') and chat_tab.conversation_renamed:
                    safe_disconnect(chat_tab.conversation_renamed)
                if hasattr(chat_tab, 'new_conversation_requested') and chat_tab.new_conversation_requested:
                    safe_disconnect(chat_tab.new_conversation_requested)

                # Connect signals with proper error handling
                signals_to_connect = [
                    (chat_tab.message_sent, self._on_message_sent, "message_sent"),
                    (chat_tab.message_cancelled,
                     self._on_message_cancelled, "message_cancelled"),
                    (chat_tab.conversation_selected,
                     self._on_conversation_selected, "conversation_selected"),
                    (chat_tab.conversation_deleted,
                     self._on_conversation_deleted, "conversation_deleted"),
                    (chat_tab.conversation_renamed,
                     self._on_conversation_renamed, "conversation_renamed"),
                    (chat_tab.new_conversation_requested,
                     self._on_new_conversation_requested, "new_conversation_requested"),
                ]

                for signal, slot, signal_name in signals_to_connect:
                    try:
                        # Check if signal already has connections
                        if hasattr(signal, 'receivers') and signal.receivers() > 0:
                            logger.warning(
                                f"[EVENT DEBUG] Signal {signal_name} already has {signal.receivers()} receivers before connecting")

                        signal.connect(
                            slot, Qt.ConnectionType.QueuedConnection)
                        logger.debug(
                            f"[EVENT DEBUG] Connected {signal_name} signal (now has {signal.receivers()} receivers)")
                    except Exception as e:
                        logger.error(
                            f"[EVENT ERROR] Failed to connect {signal_name} signal: {e}")

                logger.debug(
                    "[EVENT DEBUG] All chat tab signals connected successfully")
                self._chat_tab_signals_connected = True
            else:
                logger.warning(
                    "[EVENT WARNING] Chat tab not available for signal connection - will retry")
                # Set up a retry mechanism to connect when chat tab becomes available
                self._setup_chat_tab_retry()
        except Exception as e:
            logger.error(
                f"[EVENT ERROR] Error connecting chat tab signals: {e}")
            # Set up retry mechanism even on error
            self._setup_chat_tab_retry()

    def _on_status_updated(self, message: str):
        """Handle status updates from controller"""
        self.ui_manager.update_status(message)

    def _on_error_occurred(self, error_message: str):
        """Handle errors from controller"""
        from pyside_chat.ui.utils.message_utils import show_critical_error
        show_critical_error("Application Error",
                            error_message, parent=self.main_window)

    def _on_conversation_updated(self):
        """Handle conversation updates from controller"""
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.refresh_navigation()

    def _on_name_generation_requested(self, filepath: str):
        """Handle name generation request from controller"""
        logger.info(f"[ID:0220] Name generation requested for: {filepath}")

        summarization_service = self.service_manager.get_summarization_service()
        if summarization_service:
            try:
                # Load the conversation
                conversation_manager = self.service_manager.get_conversation_manager()
                conversation, metadata = conversation_manager.load_conversation(
                    filepath)
                logger.info(
                    f"[ID:0219] Loaded conversation with {len(conversation)} messages")
                logger.info(
                    f"[ID:0218] Current AI name: {metadata.ai_generated_name}")

                # Only generate name if we don't already have one
                if not metadata.ai_generated_name:
                    logger.info(
                        "[ID:0217] No AI name exists, triggering generation...")
                    summarization_service.generate_chat_name(
                        conversation, filepath)
                else:
                    logger.info(
                        f"[ID:0216] AI name already exists: {metadata.ai_generated_name}")

            except Exception as e:
                logger.error(
                    f"[ID:0215] Error triggering name generation: {str(e)}")
        else:
            logger.warning("[ID:0214] No summarization service available")

    def _on_models_updated(self, models):
        """Handle model list updates"""
        chat_tab = self.ui_manager.get_chat_tab()
        model_tab = self.ui_manager.get_model_tab()

        if chat_tab:
            chat_tab.update_model_list(models)
        if model_tab:
            model_tab.update_model_list(models)

        from pyside_chat.core.utils.prompts import PromptFormatter
        status_msg = PromptFormatter.format_status_message(
            "models_found", count=len(models))
        self.ui_manager.update_status(status_msg)

    def _on_message_sent(self, message):
        """Handle new message sent from chat tab"""
        try:
            import traceback
            logger.debug(
                f"[EVENT DEBUG] _on_message_sent called with message: '{message}'")
            logger.debug(
                f"[DUPLICATE_DEBUG] _on_message_sent call stack: {traceback.format_stack()[-3:]}")

            # Get current model and temperature from chat tab
            chat_tab = self.ui_manager.get_chat_tab()
            if not chat_tab:
                logger.error("Chat tab not available")
                return

            model = chat_tab.get_current_model()
            temperature = chat_tab.get_temperature()

            # Process message through controller (this adds the message to conversation service and sends to Ollama)
            logger.debug(
                f"[DUPLICATE_DEBUG] About to call process_user_message for: '{message}'")
            self.chat_controller.process_user_message(
                message, model, temperature)
            logger.info(
                f"[ID:0212] Processed user message: {message}", print_to_terminal=True)

            # UI will be updated by conversation service signals
            logger.debug(
                f"[EVENT DEBUG] User message added to conversation service")

            # NOTE: _send_to_ollama is already called by process_user_message, so we don't need to call it again

        except Exception as e:
            logger.error(f"[EVENT ERROR] Error in _on_message_sent: {e}")
            logger.error(f"[EVENT ERROR] Traceback: {traceback.format_exc()}")
            # Try to show error to user
            try:
                chat_tab = self.ui_manager.get_chat_tab()
                if chat_tab:
                    chat_tab.append_to_chat(
                        "System", f"Message processing error: {str(e)}")
            except:
                pass
            self._on_error_occurred(f"Failed to process message: {str(e)}")

    def _send_to_ollama(self, message, model, temperature):
        """Send message to Ollama and handle streaming response"""
        try:
            logger.debug(
                f"[ID:0194] _send_to_ollama called with model: {model}, temperature: {temperature}")

            # Removed guard reset for testing
            # self.chat_controller.reset_ai_response_guard()

            # Check Ollama connection
            if not self._check_ollama_connection():
                # Only show error if not already shown recently
                if not self.lifecycle_manager or not self.lifecycle_manager.get_ollama_error_shown():
                    self._show_ollama_connection_error(
                        "message", force_show=True)
                chat_tab = self.ui_manager.get_chat_tab()
                if chat_tab:
                    chat_tab.append_to_chat(
                        "System", "Failed to send: Could not connect to Ollama.\n Please check the Ollama connection and try again.")
                return

            # Reset error flag on successful connection
            if self.lifecycle_manager:
                self.lifecycle_manager.set_ollama_error_shown(False)

            # Get context messages for the request
            context_messages = self.chat_controller.conversation_service.get_context_messages()

            # Handle model selection (especially for "Auto" model)
            chosen_model = self.chat_controller._select_model(
                model, message, context_messages)
            logger.debug(
                f"[ID:MODEL001] Model selection: {model} -> {chosen_model}")

            # Create streaming message and get its ID
            streaming_message_id = self.chat_controller.start_streaming_response()
            logger.debug(
                f"[ID:STREAM001] Started streaming response with ID: {streaming_message_id}")
            cleaned_messages = self._clean_messages_for_ollama(
                context_messages)
            success = self._start_worker_after_streaming_message(
                cleaned_messages, chosen_model, temperature, streaming_message_id
            )

            if not success:
                logger.error(
                    "[ID:0195A] Failed to create worker thread for Ollama streaming")
                self.chat_controller.conversation_service.finalize_streaming_message()

        except Exception as e:
            logger.error(f"[ID:0194A] Error in _send_to_ollama: {e}")
            logger.error(
                f"[ID:0194B] _send_to_ollama error traceback: {traceback.format_exc()}")
            self.chat_controller.conversation_service.finalize_streaming_message()
            self.chat_controller.error_occurred.emit(
                f"Error sending to Ollama: {str(e)}")

    def _clean_messages_for_ollama(self, messages: List[Dict]) -> List[Dict]:
        """Clean messages for Ollama API (remove internal fields)"""
        cleaned_messages = []
        for message in messages:
            # Only include role and content for Ollama
            cleaned_message = {
                "role": message.get("role", "user"),
                "content": message.get("content", "")
            }
            cleaned_messages.append(cleaned_message)
        return cleaned_messages

    def _start_worker_after_streaming_message(self, context_messages, chosen_model, temperature, streaming_message_id):
        """Start worker thread after streaming message is created to prevent race conditions"""
        try:
            logger.debug(
                f"[ID:0213] Starting worker thread for model: {chosen_model} with streaming_message_id: {streaming_message_id}")

            # Get threading service with persistent thread pool
            if hasattr(self, 'threading_service') and self.threading_service:
                # Start chat streaming using persistent thread pool
                success = self.threading_service.start_chat_streaming(
                    context_messages=context_messages,
                    model=chosen_model,
                    temperature=temperature,
                    config_manager=self.service_manager.config_manager,
                    streaming_message_id=streaming_message_id
                )

                if success:
                    logger.debug(
                        f"[ID:0214] Chat streaming started successfully with persistent thread")
                    logger.debug(
                        "[ID:0195] Successfully created worker thread for Ollama streaming")
                else:
                    logger.error(
                        "[ID:0195A] Failed to create worker thread for Ollama streaming")
                    # Clean up streaming message on failure
                    self.chat_controller.conversation_service.finalize_streaming_message()

                return success
            else:
                logger.error("[ID:0213A] Threading service not available")
                # Clean up streaming message on failure
                self.chat_controller.conversation_service.finalize_streaming_message()
                return False

        except Exception as e:
            logger.error(f"[ID:0213B] Error starting worker thread: {e}")
            # Clean up streaming message on error
            self.chat_controller.conversation_service.finalize_streaming_message()
            return False

    def _create_worker_thread(self, context_messages, chosen_model, temperature, streaming_message_id):
        """Create and start worker thread for Ollama communication using persistent thread pool"""
        try:
            logger.debug(
                f"[ID:0213] Creating worker thread for model: {chosen_model}")

            # Get threading service with persistent thread pool
            if hasattr(self, 'threading_service') and self.threading_service:
                # Start chat streaming using persistent thread pool
                success = self.threading_service.start_chat_streaming(
                    context_messages=context_messages,
                    model=chosen_model,
                    temperature=temperature,
                    config_manager=self.service_manager.config_manager,
                    streaming_message_id=streaming_message_id
                )

                if success:
                    logger.debug(
                        f"[ID:0214] Chat streaming started successfully with persistent thread")

                    # NOTE: Signal connections are already made in __init__ for the new threading system
                    # The old signal connections below are removed to prevent duplicate chunk processing
                    # self.threading_service.chunk_received.connect(
                    #     self._handle_chat_chunk, Qt.ConnectionType.QueuedConnection
                    # )
                    # self.threading_service.progress_updated.connect(
                    #     self._handle_chat_progress, Qt.ConnectionType.QueuedConnection
                    # )
                    # self.threading_service.finished.connect(
                    #     self._handle_chat_finished, Qt.ConnectionType.QueuedConnection
                    # )
                    # self.threading_service.error.connect(
                    #     self._handle_chat_error, Qt.ConnectionType.QueuedConnection
                    # )

                    return True
                else:
                    logger.error(
                        "[ID:0215] Failed to start chat streaming with persistent thread")
                    return False
            else:
                logger.error("[ID:0216] Threading service not available")
                return False

        except Exception as e:
            logger.error(f"[ID:0217] Error creating worker thread: {e}")
            logger.error(
                f"[ID:0218] Worker thread creation error traceback: {traceback.format_exc()}")
            return False

    def _handle_chat_chunk(self, chunk: str):
        """Handle streaming chat chunk"""
        try:
            logger.debug(
                f"[ID:CHUNK001] Received chat chunk - Length: {len(chunk)}")
            logger.debug(
                f"[ID:CHUNK001A] Chunk content preview: '{chunk[:100]}...'")

            # Check if chunk is empty or whitespace
            if not chunk or not chunk.strip():
                logger.warning(
                    f"[ID:CHUNK001B] Received empty or whitespace-only chunk, skipping")
                return

            # No need to create the streaming message here; it is created before the worker starts
            logger.debug(
                f"[ID:CHUNK002] Calling chat_controller.accumulate_assistant_response with chunk length: {len(chunk)}")
            self.chat_controller.accumulate_assistant_response(chunk)

            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                if not hasattr(chat_tab, 'is_streaming') or not chat_tab.is_streaming:
                    logger.debug(
                        "[ID:CHUNK003] Starting UI streaming state for first chunk")
                    chat_tab.start_streaming()
                else:
                    logger.debug(
                        "[ID:CHUNK004] UI already streaming, continuing")
                if not hasattr(chat_tab, 'is_streaming'):
                    chat_tab.is_streaming = True
                QTimer.singleShot(
                    0, lambda: self._update_chat_display_safe(chunk))
            else:
                logger.warning(
                    "[ID:CHUNK005] Chat tab not available for chunk processing")
        except Exception as e:
            logger.error(f"[ID:CHUNK006] Error handling chat chunk: {e}")
            logger.error(
                f"[ID:CHUNK007] Chat chunk error traceback: {traceback.format_exc()}")

    def _handle_chat_progress(self, progress: str):
        """Handle chat progress updates"""
        try:
            logger.debug(
                f"[ID:PROGRESS001] Received chat progress: {progress}")
            QTimer.singleShot(0, lambda: self._update_progress_safe(progress))
        except Exception as e:
            logger.error(f"[ID:PROGRESS002] Error handling chat progress: {e}")

    def _handle_chat_finished(self):
        """Handle chat streaming completion"""
        try:
            logger.debug("[ID:FINISH001] Chat streaming finished")

            # Finalize streaming response
            success = self.chat_controller.finalize_streaming_response()
            if success:
                logger.debug(
                    "[ID:FINISH002] Successfully finalized streaming response")
            else:
                logger.warning(
                    "[ID:FINISH003] Failed to finalize streaming response")

            # NOTE: The following call is redundant and should be removed if no issues arise
            # self.chat_controller.finalize_streaming_response()

            # Handle AI response completion
            self.chat_controller.handle_ai_response()
            logger.debug(
                "[ID:FINISH004] Called chat_controller.handle_ai_response")

            # Clean up UI streaming state
            QTimer.singleShot(0, self._stop_streaming_safe)

        except Exception as e:
            logger.error(f"[ID:FINISH005] Error handling chat finished: {e}")
            logger.error(
                f"[ID:FINISH006] Chat finished error traceback: {traceback.format_exc()}")

    def _handle_chat_error(self, error_message: str):
        """Handle chat streaming error"""
        try:
            logger.error(
                f"[ID:ERROR001] Chat streaming error: {error_message}")

            # Finalize streaming response on error
            self.chat_controller.finalize_streaming_response()

            # Update UI with error
            QTimer.singleShot(
                0, lambda: self._handle_chat_error_safe(error_message))

        except Exception as e:
            logger.error(f"[ID:ERROR002] Error handling chat error: {e}")

    def _handle_chat_error_safe(self, error_message: str):
        """Safely handle chat error in main thread"""
        try:
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                # Stop UI streaming state
                if chat_tab.is_streaming:
                    logger.debug(
                        "[ID:ERROR003] Stopping UI streaming state due to error")
                    chat_tab.stop_streaming()

                from pyside_chat.core.utils.threading_utils import safe_ui_update
                safe_ui_update(chat_tab, 'append_to_chat',
                               "System", f"Error: {error_message}")
                safe_ui_update(chat_tab, 'force_enable_send_button')

        except Exception as e:
            logger.error(
                f"[ID:ERROR004] Error in _handle_chat_error_safe: {e}")

    def stop_chat_streaming(self):
        """Stop chat streaming using persistent thread pool."""
        try:
            if hasattr(self, 'threading_service') and self.threading_service:
                logger.debug("[ID:0226] Stopping chat streaming")
                self.threading_service.stop_chat_streaming()
            else:
                logger.warning(
                    "[ID:0227] Threading service not available for stopping chat")

        except Exception as e:
            logger.error(f"[ID:0228] Error stopping chat streaming: {e}")

    def _on_worker_progress(self, progress_message):
        """Handle worker progress updates"""
        logger.debug(f"[ID:0200] Worker progress: {progress_message}")

        # Update status bar if available
        try:
            main_window = self.ui_manager.get_main_window()
            if main_window and hasattr(main_window, 'statusBar'):
                from pyside_chat.core.utils.threading_utils import safe_ui_update
                safe_ui_update(main_window.statusBar(), 'showMessage',
                               progress_message, 3000)  # Show for 3 seconds
        except Exception as e:
            logger.debug(f"[ID:0199] Could not update status bar: {e}")

    def _on_worker_detailed_error(self, error_message):
        """Handle detailed worker error with logging"""
        logger.error(f"[ID:0199] Worker detailed error: {error_message}")
        logger.error(
            f"[ID:0198] Worker error occurred in thread: {QThread.currentThread().objectName()}")

        # Show error to user
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            from pyside_chat.core.utils.threading_utils import safe_ui_update
            safe_ui_update(chat_tab, 'append_to_chat', "System",
                           f"Worker Error: {error_message}")
            safe_ui_update(chat_tab, 'force_enable_send_button')

        # Trigger cleanup
        self._on_worker_finished()

    def _on_worker_thread_finished(self):
        """Handle worker thread finished signal (legacy method - kept for compatibility)"""
        logger.debug("[ID:0197] Worker thread finished signal received")
        # No cleanup needed - handled by new threading system

    def _on_worker_chunk(self, chunk, model_name, msg_id, chunk_index):
        """Handle a chunk from the worker thread and update the chat display safely with all required info."""
        logger.debug(
            f"[EVENT_BUS_DEBUG] _on_worker_chunk received: chunk='{chunk[:20]}...', model_name='{model_name}', msg_id='{msg_id}', chunk_index={chunk_index}")

        # DEBUG: Check if parameters are valid
        if msg_id == "msg_id_placeholder":
            logger.warning(
                f"[PATCH] Received placeholder msg_id: {msg_id}, this indicates the worker is not getting the real streaming message ID")

        # Validate chunk content
        if not chunk or not chunk.strip():
            logger.warning(
                f"[EVENT_BUS_DEBUG] Received empty or whitespace-only chunk from worker, skipping")
            return

        # CRITICAL FIX: Call accumulate_assistant_response to ensure chunks are properly accumulated
        logger.debug(
            f"[EVENT_BUS_DEBUG] Calling chat_controller.accumulate_assistant_response with chunk length: {len(chunk)}")
        self.chat_controller.accumulate_assistant_response(chunk)

        # Validate message ID
        if not msg_id or msg_id == "None" or msg_id == "msg_id_placeholder":
            logger.error(
                f"[EVENT_BUS_DEBUG] Invalid message ID received: '{msg_id}', this will cause chunk processing to fail")
            logger.error(
                f"[EVENT_BUS_DEBUG] Available streaming message ID: {self.chat_controller.conversation_service.get_streaming_message_id()}")

        QTimer.singleShot(0, lambda: self._update_chat_display_safe(
            chunk, model_name, msg_id, chunk_index))

    def _update_chat_display_safe(self, chunk, model_name=None, msg_id=None, chunk_index=None):
        """Safely update chat display in main thread"""
        try:
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab and hasattr(chat_tab, 'append_response_chunk'):
                if model_name is None or msg_id is None or chunk_index is None:
                    logger.warning(
                        f"[PATCH] Skipping append_response_chunk: model_name, msg_id, or chunk_index missing for chunk: {chunk[:50]}")
                    return
                logger.debug(
                    f"[PATCH] Calling chat_tab.append_response_chunk with chunk: {chunk[:50]}, model_name: {model_name}, msg_id: {msg_id}, chunk_index: {chunk_index}")
                chat_tab.append_response_chunk(
                    chunk, model_name, msg_id, chunk_index)
        except Exception as e:
            logger.error(f"[ID:0196G] Error updating chat display: {e}")

    def _on_worker_progress(self, progress):
        """Handle worker progress signal"""
        try:
            logger.debug(f"[ID:0197] Received worker progress: {progress}")

            # Update UI with progress using main thread

            QTimer.singleShot(0, lambda: self._update_progress_safe(progress))

        except Exception as e:
            logger.error(f"[ID:0198] Error in _on_worker_progress: {e}")

    def _update_progress_safe(self, progress):
        """Safely update progress in main thread"""
        try:
            # Update status bar or progress indicator
            if hasattr(self, 'ui_manager'):
                self.ui_manager.update_status(progress)
        except Exception as e:
            logger.error(f"[ID:0198A] Error updating progress: {e}")

    def _on_worker_finished(self):
        """Handle worker completion"""
        logger.debug("[ID:0193] Worker finished signal received")

        try:
            # CRITICAL FIX: Call _handle_chat_finished to finalize streaming response
            self._handle_chat_finished()

            # Only clean up if TTS is also finished
            if self._tts_finished:
                logger.debug(
                    "[ID:0191] Both worker and TTS finished, cleaning up")
                self._cleanup_worker_thread()
            else:
                logger.debug(
                    "[ID:0190] Worker finished but TTS still running, waiting for TTS")
                # TTS will call cleanup when it finishes

        except Exception as e:
            logger.error(f"[ID:0189] Error in worker finished handler: {e}")
            logger.error(
                f"[ID:0188] Worker finished error traceback: {traceback.format_exc()}")
            # Force cleanup on error
            self._cleanup_worker_thread()

    def _stop_streaming_safe(self):
        """Safely stop streaming in main thread"""
        try:
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab and chat_tab.is_streaming:
                logger.debug("[ID:0193B] Stopping UI streaming state")
                chat_tab.stop_streaming()
        except Exception as e:
            logger.error(f"[ID:0193C] Error stopping streaming: {e}")

    def _on_worker_error(self, error_message):
        """Handle worker error"""
        logger.error(f"[ID:0166] Worker error: {error_message}")

        try:
            # Stop UI streaming state using main thread

            QTimer.singleShot(
                0, lambda: self._handle_worker_error_safe(error_message))

        except Exception as e:
            logger.error(f"[ID:0165] Error handling worker error: {e}")
            logger.error(
                f"[ID:0164] Worker error handler traceback: {traceback.format_exc()}")

    def _handle_worker_error_safe(self, error_message):
        """Safely handle worker error in main thread"""
        try:
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                # Stop UI streaming state
                if chat_tab.is_streaming:
                    logger.debug(
                        "[ID:0166A] Stopping UI streaming state due to error")
                    chat_tab.stop_streaming()

                from pyside_chat.core.utils.threading_utils import safe_ui_update
                safe_ui_update(chat_tab, 'append_to_chat',
                               "System", f"Error: {error_message}")
                safe_ui_update(chat_tab, 'force_enable_send_button')

            self._on_worker_finished()

        except Exception as e:
            logger.error(f"[ID:0165A] Error in _handle_worker_error_safe: {e}")

    def _on_tts_finished(self):
        """Handle TTS completion"""
        logger.debug("[ID:0187] TTS finished signal received")
        self._tts_finished = True

        # Use QTimer.singleShot to ensure this runs in the main thread

    def _handle_tts_finished_delayed(self):
        """Handle TTS finished with a delay to ensure proper coordination"""
        try:
            logger.debug("[ID:0186] Handling TTS finished delayed")

            # Cleanup is handled by the new threading system
            self._cleanup_worker_thread()

        except Exception as e:
            logger.error(
                f"[ID:0183] Error in delayed TTS finished handling: {e}")
            logger.error(
                f"[ID:0182] TTS finished error traceback: {traceback.format_exc()}")
            # Force cleanup on error
            self._cleanup_worker_thread()

    def _cleanup_worker_thread(self):
        """Clean up worker thread safely in the main thread"""
        # Only clean up if both worker and TTS are finished
        if not self._tts_finished:
            # TTS not finished yet, wait a bit more but don't recurse

            logger.debug(
                "[ID:0181] TTS not finished, scheduling cleanup for later")
            QTimer.singleShot(500, self._cleanup_worker_thread_once)
            return

        self._cleanup_worker_thread_once()

    def _cleanup_worker_thread_once(self):
        """Clean up worker thread once without recursion"""
        try:
            logger.debug("[ID:0180] Starting worker thread cleanup")

            # Clean up new threading architecture
            if hasattr(self, 'threading_service'):
                logger.debug(
                    "[ID:0179] Cleaning up new threading architecture")
                self.threading_service.stop_chat_streaming()

        except Exception as e:
            logger.error(f"[ID:0166] Error cleaning up worker thread: {e}")
            logger.error(
                f"[ID:0165] Worker cleanup error traceback: {traceback.format_exc()}")
        finally:
            self._tts_finished = False  # Reset for next time
            logger.debug("[ID:0164] Worker thread cleanup completed")
            # Reset streaming state in chat tab
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                try:
                    chat_tab.stop_streaming()
                except Exception as e:
                    logger.error(
                        f"[ID:0163] Error stopping streaming in cleanup: {e}")

    def _final_worker_cleanup(self):
        """Final cleanup to ensure worker thread is properly destroyed"""
        try:
            logger.debug("[ID:0161] Final worker cleanup completed")
            # No cleanup needed - handled by new threading system
        except Exception as e:
            logger.error(f"[ID:0160] Error in final worker cleanup: {e}")
            logger.error(
                f"[ID:0159] Final cleanup error traceback: {traceback.format_exc()}")

    def _on_message_received(self, response: str):
        """Handle message received signal from chat controller"""
        logger.debug(
            f"[ID:0163] Message received signal received from chat controller with response length: {len(response)}")
        # The chat controller has already handled TTS triggering in _trigger_tts_for_response
        # This signal is just for notification that the AI response is complete
        logger.debug("[ID:0163A] AI response processing completed")

    def _on_message_finished(self):
        """Handle message finished"""
        from pyside_chat.core.logging.helpers import LoggingHelpers
        LoggingHelpers.log_debug("on_message_finished called")

        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.stop_streaming()

    def _on_message_cancelled(self):
        """Handle message cancellation"""
        logger.debug("[ID:0163] Message cancellation requested")

        try:
            # Cancel the Ollama service request
            ollama_service = self.service_manager.get_ollama_service()
            ollama_service.cancel_request()

            # Stop the worker thread if it's running using safe cleanup
            if hasattr(self, 'threading_service'):
                self.threading_service.stop_chat_streaming()

            # Update the chat tab (prevent recursive call)
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                # Call the method directly without triggering signals
                chat_tab.stop_streaming()
                chat_tab.force_enable_send_button()

            logger.debug("[ID:0161] Message cancellation completed")

        except Exception as e:
            logger.error(f"[ID:0160] Error cancelling message: {e}")
            logger.error(
                f"[ID:0159] Message cancellation error traceback: {traceback.format_exc()}")

    def _on_conversation_selected(self, filepath: str):
        """Handle conversation selection from navigation"""
        try:
            # Load conversation in chat tab
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.load_conversation(filepath)

                # CRITICAL FIX: Use ChatDisplay's set_conversation_service method
                if hasattr(chat_tab, 'chat_controller') and hasattr(chat_tab.chat_controller, 'conversation_service'):
                    conversation_service = chat_tab.chat_controller.conversation_service
                    if hasattr(chat_tab, 'chat_display') and hasattr(chat_tab.chat_display, 'set_conversation_service'):
                        chat_tab.chat_display.set_conversation_service(
                            conversation_service)
                        logger.debug(
                            "[EVENT_BUS] Set conversation service in chat display after loading conversation")

        except Exception as e:
            logger.error(f"Error loading conversation {filepath}: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

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

            logger.info(
                f"[ID:0158] Conversation renamed: {old_filepath} -> {new_filepath}")

            # Refresh navigation to show updated AI-generated name
            if chat_tab:
                chat_tab.refresh_navigation()

        except Exception as e:
            logger.error(
                f"[ID:0157] Error handling conversation rename: {str(e)}")

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
        from pyside_chat.core.utils.prompts import PromptFormatter
        status_msg = PromptFormatter.format_status_message(
            "personality_switched", personality=personality_name)
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

        from pyside_chat.core.utils.prompts import PromptFormatter
        status_msg = PromptFormatter.format_status_message(
            "model_operation_error", error=error)
        self.ui_manager.update_status(status_msg)

        # Show user-friendly error dialog for connection issues
        if "Cannot connect to Ollama" in error or "connection" in error.lower():
            # Only show error if not already shown recently
            if not self.lifecycle_manager or not self.lifecycle_manager.get_ollama_error_shown():
                self._show_ollama_connection_error("operation")
        else:
            # Show copy-enabled error dialog for other model operation errors
            from pyside_chat.ui.utils.message_utils import show_operation_error
            show_operation_error(
                "Model Operation", Exception(error), self.main_window)

    def _on_conversation_metadata_updated(self):
        """Handle conversation metadata updates"""
        conversation_manager = self.service_manager.get_conversation_manager()
        metadata = conversation_manager.get_current_metadata()
        self.ui_manager.update_status(metadata.get_display_info())

        # CRITICAL FIX: Refresh navigation widget when conversation metadata is updated
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab:
            chat_tab.refresh_navigation()
            logger.debug(
                f"[NAVIGATION] Refreshed navigation after metadata update for: {metadata.current_conversation_file}")

    def _on_auto_save_completed(self, filepath: str):
        """Handle auto-save completion"""
        logger.debug(f"[AUTO_SAVE] Auto-save completed: {filepath}")

        # Update status to show save completion
        self.ui_manager.update_status(
            f"Conversation saved: {os.path.basename(filepath)}")

        # Force UI refresh to ensure thoughts are displayed
        chat_tab = self.ui_manager.get_chat_tab()
        if chat_tab and hasattr(chat_tab, 'chat_display'):
            # Force sync messages from conversation service to ensure UI shows latest content
            chat_tab.chat_display.sync_messages_from_conversation_service()
            logger.debug(
                f"[AUTO_SAVE] Forced UI refresh after auto-save: {filepath}")
        else:
            logger.warning(
                "[AUTO_SAVE] Chat tab or chat display not available for UI refresh")

    def _on_new_conversation_requested(self):
        """Handle new conversation request"""
        self._on_new_conversation()

    def _on_new_conversation(self):
        """Handle new conversation request"""
        try:
            # Use chat controller's start_new_conversation method to properly clear everything
            if hasattr(self, 'chat_controller') and self.chat_controller:
                self.chat_controller.start_new_conversation()
                logger.debug(
                    "[EVENT_BUS] Called chat controller's start_new_conversation method")
            else:
                # Fallback: Clear the conversation service directly
                conversation_service = self.service_manager.get_conversation_service()
                conversation_service.clear_conversation()
                logger.debug("[EVENT_BUS] Used fallback conversation clearing")

            # Update UI
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.clear_chat()

                # CRITICAL FIX: Use ChatDisplay's set_conversation_service method
                if hasattr(chat_tab, 'chat_display') and hasattr(chat_tab.chat_display, 'set_conversation_service'):
                    conversation_service = self.service_manager.get_conversation_service()
                    chat_tab.chat_display.set_conversation_service(
                        conversation_service)
                    logger.debug(
                        "[EVENT_BUS] Set conversation service in chat display after new conversation")

            # Update status
            from pyside_chat.core.utils.prompts import PromptFormatter
            status_msg = PromptFormatter.format_status_message(
                "new_conversation")
            self.ui_manager.update_status(status_msg)

        except Exception as e:
            logger.error(f"Error creating new conversation: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def _on_clear_chat(self):
        """Clear the chat display"""
        if self.ui_manager.show_clear_chat_dialog():
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab:
                chat_tab.clear_chat()

            from pyside_chat.core.utils.prompts import PromptFormatter
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
        from pyside_chat.ui.dialogs.settings_dialog import SettingsDialog

        # Get current lists
        ollama_service = self.service_manager.get_ollama_service()
        models = ollama_service.get_models() or ["llama2"]

        personality_tab = self.ui_manager.get_personality_tab()
        personalities = personality_tab.personality_model.get_available_personalities() or [
            "assistant"]

        dialog = SettingsDialog(
            self.service_manager.config_manager, models, personalities, self.main_window)
        if dialog.exec():
            # Check if memory settings changed
            memory_enabled_now = self.service_manager.config_manager.get(
                "memory_enabled", True)
            if memory_enabled_now != self.service_manager.is_memory_enabled():
                # Reinitialize services
                self.service_manager.reinitialize_services()
                self.chat_controller = self._create_chat_controller()
                self._setup_ui_with_new_services()
                self._on_refresh_models()
            else:
                self.service_manager.reinitialize_services()
                self.chat_controller = self._create_chat_controller()
                self.setup_connections()
                self._on_refresh_models()

    def _create_chat_controller(self):
        """Create a new chat controller with current services"""
        from pyside_chat.features.chat.chat_controller import ChatController

        return ChatController(
            ollama_service=self.service_manager.get_ollama_service(),
            conversation_service=self.service_manager.get_conversation_service(),
            enhancement_service=self.service_manager.get_enhancement_service(),
            memory_service=self.service_manager.get_memory_service(),
            conversation_manager=self.service_manager.get_conversation_manager(),
            config_manager=self.service_manager.get_config_manager()
        )

    def _setup_ui_with_new_services(self):
        """Setup UI with new services after configuration change"""
        # This would need to be implemented based on your UI structure
        # For now, we'll just re-setup connections
        self.setup_connections()

    def _on_refresh_models(self):
        """Refresh the list of available models"""
        try:
            ollama_service = self.service_manager.get_ollama_service()
            models = ollama_service.get_models()
            if models:
                # Reset error flag on success
                if self.lifecycle_manager:
                    self.lifecycle_manager.set_ollama_error_shown(False)
                else:
                    self.ollama_error_shown = False

                chat_tab = self.ui_manager.get_chat_tab()
                model_tab = self.ui_manager.get_model_tab()

                if chat_tab:
                    chat_tab.update_model_list(models)
                if model_tab:
                    model_tab.update_model_list(models)

                # Log successful connection
                logger.info(
                    "[ID:CONNECTION_SUCCESS] Ollama connection successful, models loaded")
            else:
                # No models returned - likely Ollama is not running
                self._show_ollama_connection_error("startup")
        except Exception as e:
            logger.error(f"[ID:0156] Error refreshing models: {e}")
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
            from pyside_chat.core.logging.helpers import LoggingHelpers
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
        # Delegate to the lifecycle manager's enhanced error dialog
        if self.lifecycle_manager:
            # Sync the error shown flag with lifecycle manager
            if not force_show and self.lifecycle_manager.get_ollama_error_shown():
                return
            if not force_show:
                self.lifecycle_manager.set_ollama_error_shown(True)
            self.lifecycle_manager.show_ollama_connection_error(
                context, force_show)
        else:
            # Fallback to basic dialog if lifecycle manager not available
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
                    "2. Start Ollama by running the Ollama app.exe application<br>"
                    f'3. Or download from: <a href="{download_link}">{download_link}</a><br><br>'
                    "The application will continue to work, but you won't be able to send messages until Ollama is running."
                )
            else:
                title = "Connection Error"
                message = (
                    'Cannot connect to Ollama.<br><br>'
                    'Please make sure:<br>'
                    "1. Ollama is running (start the Ollama app.exe application)<br>"
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

    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            if hasattr(self, 'threading_service'):
                return self.threading_service.get_threading_status()
            else:
                return {}
        except Exception as e:
            logger.error(f"[ID:0152] Error getting threading status: {e}")
            return {}

    def cleanup_on_exit(self):
        """Clean up all resources when application is exiting"""
        try:
            logger.debug("[ID:0151] Starting application exit cleanup")

            # Clean up new threading architecture
            if hasattr(self, 'threading_service'):
                logger.debug("[ID:0150] Cleaning up threading service on exit")

                # Stop chat streaming and wait for completion
                if self.threading_service.chat_streaming_thread and self.threading_service.chat_streaming_thread.isRunning():
                    logger.debug(
                        "[ID:0149] Stopping chat streaming thread on exit")
                    self.threading_service.stop_chat_streaming()

                    # Wait for thread to finish with timeout
                    if self.threading_service.chat_streaming_thread:
                        # 5 second timeout
                        if not self.threading_service.chat_streaming_thread.wait(5000):
                            logger.warning(
                                "[ID:0148] Chat streaming thread did not finish within timeout, terminating")
                            self.threading_service.chat_streaming_thread.terminate()
                            self.threading_service.chat_streaming_thread.wait(
                                2000)

                # Clean up threading service with additional wait
                logger.debug("[ID:0147] Cleaning up threading service")
                self.threading_service.cleanup()

                # Call finalize for robust cleanup
                logger.debug("[ID:0146] Finalizing threading service")
                self.threading_service.finalize()

                # Additional wait to ensure all threads are properly cleaned up
                time.sleep(0.5)  # Small delay to allow cleanup to complete

            # Clean up any running worker threads (legacy cleanup removed)
            # All cleanup is now handled by the new threading system

            logger.debug("[ID:0145] Application exit cleanup completed")

        except Exception as e:
            logger.error(
                f"[ID:0144] Error during application exit cleanup: {e}")
            logger.error(
                f"[ID:0143] Exit cleanup error traceback: {traceback.format_exc()}")

    def reconnect_chat_tab_signals(self):
        """Reconnect chat tab signals when chat tab is recreated"""
        logger.debug(
            "[EVENT DEBUG] Reconnecting chat tab signals after recreation")
        self._connect_chat_tab_signals()

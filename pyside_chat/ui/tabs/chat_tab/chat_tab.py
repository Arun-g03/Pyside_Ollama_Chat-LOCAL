# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.ui.Widgets.chat_navigation import ChatNavigationWidget
from pyside_chat.ui.dialogs.voice_settings_dialog import VoiceSettingsDialog


"""
Main Chat Tab Component - Orchestrates all chat interface components
"""



# Import modular components
from .chat_display import ChatDisplay
from .voice_controls import VoiceControls
from .eq_visualizer import EQVisualizer
from .input_controls import InputControls

logger = CustomLogger.get_logger(__name__)

# Utility function for safe signal disconnection

def safe_disconnect(signal, slot, logger=logger):
    try:
        if signal is not None and hasattr(signal, 'disconnect'):
            try:
                signal.disconnect(slot)
                logger.debug(f"[SAFE DISCONNECT] Disconnected {slot} from {signal}")
            except Exception as e:
                logger.debug(f"[SAFE DISCONNECT] Could not disconnect {slot} from {signal}: {e}")
        else:
            logger.debug(f"[SAFE DISCONNECT] Signal {signal} is None or has no disconnect method, skipping")
    except Exception as e:
        logger.error(f"[SAFE DISCONNECT] Exception during disconnect: {e}")

class ChatTab(QWidget):
    """Main chat interface tab that orchestrates all components"""
    
    # Signals
    message_sent = Signal(str)  # Emitted when user sends a message
    message_cancelled = Signal()  # Emitted when user cancels a message
    conversation_selected = Signal(str)  # Emitted when a conversation is selected
    conversation_deleted = Signal(str)   # Emitted when a conversation is deleted
    conversation_renamed = Signal(str, str)  # Emitted when a conversation is renamed (old_path, new_path)
    new_conversation_requested = Signal() # Emitted when new conversation is requested
    append_response_signal = Signal(str, object)  # chunk, model_name
    speak_text_requested = Signal(str)  # Emitted when TTS is requested
    message_edited = Signal(int, str)  # Emitted when a message is edited
    
    def __init__(self, parent=None, conversation_manager=None, summarization_service=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.conversation_manager = conversation_manager
        self.summarization_service = summarization_service
        self.config_manager = config_manager
        self.current_conversation_file = None
        self.chat_controller = None  # Will be set by parent

        # Initialize components
        self.setup_components()
        
        # Setup UI
        self.setup_ui()
        
        # Setup connections
        self.setup_connections()
        
        # State variables
        self.current_model = None
        self.temperature = 0.7
        self.is_streaming = False
        self.current_response = ""
        self.last_message_type = None  # Track last message type
        self.last_system_message_widget = None  # Track last system message widget (if using custom widgets)
        self.voice_mode = False  # Track voice mode state
        
        # Voice controls state tracking
        self._voice_controls_signals_connected = False  # Track if voice control signals are connected
    
    def setup_components(self):
        """Initialize all modular components"""
        # Initialize voice controls with lazy loading (only when voice mode is activated)
        self.voice_controls = None
        self.voice_controls_initialized = False
        self._voice_controls_signals_connected = False  # Track signal connection state
        
        # Initialize EQ visualizer
        self.eq_visualizer = EQVisualizer(self)
        
        # Initialize input controls
        self.input_controls = InputControls(self)
        
        # Initialize chat display
        self.chat_display = ChatDisplay(self, config_manager=self.config_manager)
        
        # Override AI name method in chat display
        self.chat_display.get_ai_name = self.get_ai_name
        
    def setup_ui(self):
        """Setup the chat interface UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create horizontal splitter for navigation and chat
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(main_splitter)
        
        # Navigation panel (left side)
        if self.conversation_manager:
            self.navigation_widget = ChatNavigationWidget(
                self.conversation_manager, 
                self.summarization_service,
                self
            )
            self.navigation_widget.setMaximumWidth(300)
            self.navigation_widget.setMinimumWidth(200)
            main_splitter.addWidget(self.navigation_widget)
        
        # Chat area (right side)
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create vertical splitter for chat display and controls
        chat_splitter = QSplitter(Qt.Orientation.Vertical)
        chat_layout.addWidget(chat_splitter)
        
        # Chat display area
        chat_display_components = self.chat_display.get_ui_components()
        chat_splitter.addWidget(chat_display_components['scroll_area'])
        
        # Controls area
        input_components = self.input_controls.get_ui_components()
        
        # Create controls widget
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add input controls
        controls_layout.addWidget(input_components['input_widget'])
        controls_layout.addWidget(input_components['settings_widget'])
        
        # Create voice controls widget (will be populated when voice controls are initialized)
        self.voice_controls_widget = QWidget()
        voice_controls_layout = QHBoxLayout(self.voice_controls_widget)
        voice_controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add placeholder widgets that will be replaced when voice controls are initialized
        self.voice_button_placeholder = QPushButton("🎤 Voice")
        self.voice_settings_button_placeholder = QPushButton("⚙️")
        self.audio_level_widget_placeholder = QLabel("")
        
        voice_controls_layout.addWidget(self.voice_button_placeholder)
        voice_controls_layout.addWidget(self.voice_settings_button_placeholder)
        voice_controls_layout.addWidget(self.audio_level_widget_placeholder)
        voice_controls_layout.addStretch()  # Add stretch to push controls to the left
        
        controls_layout.addWidget(self.voice_controls_widget)
        
        # Initially hide voice-related widgets
        self.voice_controls_widget.hide()
        
        # Add controls to splitter
        chat_splitter.addWidget(controls_widget)
        
        # Set splitter proportions
        chat_splitter.setSizes([600, 200])
        main_splitter.setSizes([250, 950])  # Navigation: 250px, Chat: 950px
        
        main_splitter.addWidget(chat_widget)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #232323;
                color: #fff;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 6px;
                background: #232323;
            }
            QTabBar::tab {
                background: #232323;
                color: #fff;
                border: 1px solid #444;
                border-bottom: none;
                border-radius: 6px 6px 0 0;
                padding: 8px 18px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #2d2d2d;
                color: #fff;
                border-bottom: 2px solid #0078d4;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 16px;
                font-weight: bold;
                color: #fff;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background: #232323;
                color: #fff;
            }
            QLabel {
                color: #fff;
                font-size: 14px;
            }
            QComboBox, QSpinBox {
                background-color: #2d2d2d;
                color: #fff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 6px 10px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #232323;
                color: #fff;
                border: 1px solid #555;
                selection-background-color: #0078d4;
            }
            QCheckBox {
                color: #fff;
                font-size: 14px;
                spacing: 8px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 8px 18px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: #232323;
                border: none;
            }
        """)
        
    def setup_connections(self):
        """Setup signal connections between components"""
        try:
            # Connect input controls signals
            self.input_controls.message_sent.connect(self.on_message_sent)
            self.input_controls.message_cancelled.connect(self.on_message_cancelled)
            self.input_controls.input_mode_changed.connect(self.on_input_mode_changed)
            self.input_controls.temperature_changed.connect(self.on_temperature_changed)
            self.input_controls.personality_changed.connect(self.on_personality_changed)
            self.input_controls.model_changed.connect(self.on_model_changed)
            
            # Voice controls signals will be connected when voice controls are initialized
            # Voice mode changes are handled by input mode changes
            
            # Connect chat display signals
            self.chat_display.message_edited.connect(self.on_message_edited)
            
            # Connect EQ visualizer signals
            self.eq_visualizer.eq_mode_changed.connect(self.on_eq_mode_changed)
            
            # Connect navigation widget signals
            if hasattr(self, 'navigation_widget'):
                self.navigation_widget.conversation_selected.connect(self.load_conversation)
                self.navigation_widget.conversation_deleted.connect(self.conversation_deleted.emit)
                self.navigation_widget.conversation_renamed.connect(self.conversation_renamed.emit)
                self.navigation_widget.new_conversation_requested.connect(self.new_conversation_requested.emit)
            
            # CRITICAL FIX: Connection to conversation service signals will be handled in set_chat_controller()
            # to avoid duplicate connections and signal loops
            
            # Voice settings button will be connected when voice controls are initialized
            
            logger.debug("[VOICE DEBUG] Signal connections setup completed successfully")
            
        except Exception as e:
            logger.error(f"[VOICE ERROR] Error setting up signal connections: {e}")
            logger.error(f"[VOICE ERROR] Traceback: {traceback.format_exc()}")
    
    def _on_conversation_updated(self, conversation):
        """Handle updates to the conversation and sync streaming state from conversation service."""
        logger.debug(f"[STATE_SYNC] _on_conversation_updated called. Conversation has {len(conversation)} messages.")
        for i, msg in enumerate(conversation):
            logger.debug(f"[STATE_SYNC] Message {i}: id={msg.get('id')}, role={msg.get('role')}, is_streaming={msg.get('is_streaming')}, content_len={len(msg.get('content', ''))}")
        prev_streaming = getattr(self, 'is_streaming', False)
        self.is_streaming = any(msg.get('is_streaming') for msg in conversation)
        logger.debug(f"[STATE_SYNC] Calculated is_streaming: {self.is_streaming} (was {prev_streaming})")
        # Update UI state based on streaming
        input_components = self.input_controls.get_ui_components()
        logger.debug(f"[STATE_SYNC] send_button id: {id(input_components['send_button'])}, cancel_button id: {id(input_components['cancel_button'])}")
        logger.debug(f"[STATE_SYNC] InputControls send_button id: {id(self.input_controls.send_button)}, cancel_button id: {id(self.input_controls.cancel_button)}")
        if not self.voice_mode:
            input_components['send_button'].setEnabled(not self.is_streaming)
            input_components['cancel_button'].setVisible(self.is_streaming)
            logger.debug(f"[STATE_SYNC] send_button enabled: {input_components['send_button'].isEnabled()}, cancel_button visible: {input_components['cancel_button'].isVisible()}")
            # Force repaint and process events
            input_components['send_button'].repaint()
            input_components['cancel_button'].repaint()
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()
        else:
            logger.debug("[STATE_SYNC] Voice mode: buttons remain hidden")
        self.update()

    def on_message_sent(self, message: str):
        """Handle message sent (text or voice)"""
        import traceback
        logger.debug(f"[VOICE DEBUG] on_message_sent called with message: '{message}', voice_mode: {self.voice_mode}")
        logger.debug(f"[DUPLICATE_DEBUG] on_message_sent call stack: {traceback.format_stack()[-3:]}")
        
        # CRITICAL FIX: Don't add user message to chat here - let the event bus handle it
        # This prevents duplicate messages in the conversation service
        # self.append_to_chat("You", message)  # REMOVED - causes duplication
        
        # Start streaming state
        self.start_streaming()
        
        # Emit signal for parent
        logger.debug(f"[VOICE DEBUG] Emitting message_sent signal for parent")
        self.message_sent.emit(message)
        
        # Instead of directly starting TTS, use the new method
        if self.voice_mode:
            self.finalize_streaming_and_start_tts(message)
        else:
            # Show chat input widgets
            input_components = self.input_controls.get_ui_components()
            
            input_components['message_input'].show()
            input_components['send_button'].show()
            self.voice_controls_widget.hide()
            
            self.voice_mode = False
            self.eq_visualizer.switch_to_chat_display(self.chat_display.scroll_area)
            logger.debug("[VOICE DEBUG] Switched to Chat mode")
    
    def on_message_cancelled(self):
        """Handle message cancelled from input controls"""
        self.stop_streaming()
        self.message_cancelled.emit()
        
    def _ensure_voice_controls_initialized(self):
        """Ensure voice controls are initialized with proper signal management"""
        if not self.voice_controls_initialized:
            try:
                print(f"[DEBUG] Initializing voice controls")
                logger.debug("Initializing voice controls", print_to_terminal=True)
                
                # Initialize voice controls
                self.voice_controls = VoiceControls(self, self.config_manager)
                voice_components = self.voice_controls.get_ui_components()
                
                # Replace the placeholder widgets in the existing voice controls widget
                voice_controls_layout = self.voice_controls_widget.layout()
                if voice_controls_layout:
                    # Clear existing placeholder widgets
                    while voice_controls_layout.count():
                        child = voice_controls_layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    
                    # Add the real voice control components
                    voice_controls_layout.addWidget(voice_components['voice_button'])
                    voice_controls_layout.addWidget(voice_components['voice_settings_button'])
                    voice_controls_layout.addWidget(voice_components['audio_level_widget'])
                    voice_controls_layout.addStretch()  # Add stretch to push controls to the left
                    
                    logger.debug("Voice control components added to existing layout")
                else:
                    logger.error("Voice controls widget has no layout")
                
                # Connect voice control signals to chat tab with proper cleanup
                if not self._voice_controls_signals_connected:
                    print(f"[DEBUG] Connecting voice control signals to chat tab")
                    logger.debug("Connecting voice control signals to chat tab", print_to_terminal=True)
                    
                    # Define signal-slot pairs with names for logging
                    signal_slot_pairs = [
                        (self.voice_controls.voice_input_received, self.on_voice_input_received, "voice_input_received"),
                        (self.voice_controls.voice_input_error, self.on_voice_input_error, "voice_input_error"),
                        (self.voice_controls.tts_started, self.on_tts_started, "tts_started"),
                        (self.voice_controls.tts_finished, self.on_tts_finished, "tts_finished"),
                        (self.voice_controls.tts_error, self.on_tts_error, "tts_error"),
                        (self.voice_controls.recording_started, self.on_recording_started, "recording_started"),
                        (self.voice_controls.recording_stopped, self.on_recording_stopped, "recording_stopped"),
                        (self.voice_controls.recording_error, self.on_recording_error, "recording_error"),
                        (self.voice_controls.voice_processing_started, self.on_voice_processing_started, "voice_processing_started"),
                        (self.voice_controls.voice_processing_finished, self.on_voice_processing_finished, "voice_processing_finished"),
                        (self.voice_controls.audio_level_changed, self.on_audio_level_changed, "audio_level_changed"),
                        (self.voice_controls.eq_bars_changed, self.on_eq_bars_changed, "eq_bars_changed"),
                        (self.voice_controls.user_interrupted, self.on_user_interrupted, "user_interrupted"),
                        (self.voice_controls.request_cancelled, self.on_request_cancelled, "request_cancelled"),
                        (self.voice_controls.voice_status_changed, self.on_voice_status_changed, "voice_status_changed"),
                        (self.voice_controls.eq_visualizer_changed, self.on_eq_visualizer_changed_from_voice_controls, "eq_visualizer_changed"),
                    ]
                    
                    # Connect all signals with QueuedConnection for thread safety

                    for signal, slot, signal_name in signal_slot_pairs:
                        try:
                            # Connect signal directly (PySide6 handles duplicates gracefully)
                            signal.connect(slot, Qt.ConnectionType.QueuedConnection)
                            logger.debug(f"Connected signal {signal_name} to {slot.__name__}")
                        except Exception as e:
                            logger.error(f"Failed to connect signal {signal_name} to {slot.__name__}: {e}")
                    
                    self._voice_controls_signals_connected = True
                
                # Connect voice settings button
                try:
                    # Connect signal directly (PySide6 handles duplicates gracefully)
                    voice_components['voice_settings_button'].clicked.connect(self.open_voice_settings)
                    logger.debug("Connected voice settings button")
                except Exception as e:
                    logger.error(f"Failed to connect voice settings button: {e}")

                self.voice_controls_initialized = True
                print(f"[DEBUG] Voice controls initialized successfully")
                logger.info("Voice controls initialized successfully", print_to_terminal=True)
                
                # Force UI refresh to update button state based on current voice service status
                if self.voice_controls:
                    self.voice_controls.force_ui_refresh()
                
            except Exception as e:
                print(f"[DEBUG] Failed to initialize voice controls: {e}")
                logger.error(f"Failed to initialize voice controls: {e}", print_to_terminal=True)
                self.voice_controls = None
                self.voice_controls_initialized = False
        else:
            print(f"[DEBUG] Voice controls already initialized")
            logger.debug("Voice controls already initialized", print_to_terminal=True)

    def on_voice_status_changed(self, status: str):
        """Update the audio level label or status indicator with the current voice service status"""
        try:
            if self.voice_controls and hasattr(self.voice_controls, 'audio_level_label'):
                self.voice_controls.audio_level_label.setText(f"🎤 {status}")
        except Exception as e:
            logger.error(f"Failed to update voice status indicator: {e}")

    def on_input_mode_changed(self, mode: str):
        """Handle input mode change"""
        logger.debug(f"[VOICE DEBUG] on_input_mode_changed called with mode: {mode}")
        
        if mode == "Chat":
            # If voice controls are initialized and any voice process is running, stop it
            if self.voice_controls_initialized and self.voice_controls and self.voice_controls.voice_service:
                try:
                    if self.voice_controls.voice_service.is_recording or self.voice_controls.voice_service.is_processing_voice:
                        self.voice_controls.voice_service.stop_voice_input()
                except Exception as e:
                    logger.error(f"Failed to stop voice input: {e}")
            
            # Show chat input widgets
            input_components = self.input_controls.get_ui_components()
            
            input_components['message_input'].show()
            input_components['send_button'].show()
            self.voice_controls_widget.hide()
            
            self.voice_mode = False
            self.eq_visualizer.switch_to_chat_display(self.chat_display.scroll_area)
            logger.debug("[VOICE DEBUG] Switched to Chat mode")
            
        elif mode == "Voice":
            # Initialize voice controls if not already initialized
            self._ensure_voice_controls_initialized()
            
            if self.voice_controls_initialized and self.voice_controls:
                # Show voice input widgets immediately
                input_components = self.input_controls.get_ui_components()
                voice_components = self.voice_controls.get_ui_components()
                
                input_components['message_input'].hide()
                input_components['send_button'].hide()
                input_components['cancel_button'].hide()
                voice_components['voice_button'].show()
                voice_components['audio_level_widget'].show()
                voice_components['voice_settings_button'].show()
                self.voice_controls_widget.show()
                
                self.voice_mode = True
                
                # Immediately show "Initializing" status
                if hasattr(self.voice_controls, 'audio_level_label'):
                    self.voice_controls.audio_level_label.setText("🎤 Initializing...")
                
                # Check if voice service is ready
                if not self.voice_controls.is_voice_service_ready():
                    logger.info("Voice service not ready, starting initialization")
                    # The voice controls will handle initialization automatically
                    # Status will be updated via the voice_status_changed signal
                    # Show "Initializing" status immediately
                    self.voice_controls.voice_status_changed.emit("Initializing")
                else:
                    logger.info("Voice service already ready")
                    # Show "Ready" status immediately
                    self.voice_controls.voice_status_changed.emit("Ready")
                
                # Switch to EQ visualizer if enabled
                eq_mode = self.voice_controls.get_voice_settings().get("eq_visualizer", "None")
                if eq_mode != "None":
                    self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.scroll_area, self.voice_mode)
                    logger.debug(f"[VOICE DEBUG] Switched to Voice mode with EQ: {eq_mode}")
                else:
                    logger.debug("[VOICE DEBUG] Switched to Voice mode without EQ")
            else:
                logger.error("Failed to initialize voice controls for voice mode")
                # Show error status
                if hasattr(self.voice_controls, 'audio_level_label'):
                    self.voice_controls.audio_level_label.setText("🎤 Error: Failed to initialize")
    
    def on_temperature_changed(self, temperature: float):
        """Handle temperature change"""
        self.temperature = temperature
        logger.debug(f"Temperature changed to: {self.temperature}")
        
    def on_personality_changed(self, personality_name: str):
        """Handle personality change"""
        logger.debug(f"Personality changed to: {personality_name}")
        
        # Set the personality in the personality service
        try:
            if hasattr(self.parent, 'get_service_manager'):
                service_manager = self.parent.get_service_manager()
                if hasattr(service_manager, 'get_personality_service'):
                    personality_service = service_manager.get_personality_service()
                    if personality_service:
                        success = personality_service.set_current_personality(personality_name)
                        if success:
                            logger.debug(f"Successfully set personality service to: {personality_name}")
                        else:
                            logger.warning(f"Failed to set personality service to: {personality_name}")
        except Exception as e:
            logger.error(f"Error setting personality in service: {e}")
        
        # Update AI name in chat display
        self.chat_display.get_ai_name = self.get_ai_name
        # Update personality name in chat renderer
        self.chat_display.update_personality_name(self.get_ai_name())
        
    def on_model_changed(self, model_name: str):
        """Handle model change"""
        logger.debug(f"Model changed to: {model_name}")
        # Handle model change logic here
        
    def on_eq_mode_changed(self, mode: str):
        """Handle EQ mode change"""
        logger.debug(f"EQ mode changed to: {mode}")
        # Update voice settings if voice controls are initialized
        if self.voice_controls_initialized and self.voice_controls:
            voice_settings = self.voice_controls.get_voice_settings()
            voice_settings["eq_visualizer"] = mode
            self.voice_controls.update_voice_settings(voice_settings)
        
    def on_user_interrupted(self):
        """Handle user interruption during AI response"""
        logger.info("User interruption detected in chat tab")
        
        # Stop current streaming if active
        if self.is_streaming:
            logger.debug("Stopping streaming due to user interruption")
            self.stop_streaming()
            
            # Add interruption message to chat
            self.append_to_chat("System", "User interrupted AI response")
        
        # Reset voice mode state if needed
        if self.voice_mode:
            logger.debug("Resetting voice mode state after interruption")
            # Voice controls will handle restarting voice input

    def on_request_cancelled(self):
        """Handle request cancellation"""
        logger.info("Request cancelled in chat tab")
        
        # Stop current streaming if active
        if self.is_streaming:
            logger.debug("Stopping streaming due to request cancellation")
            self.stop_streaming()
            
            # Add cancellation message to chat
            self.append_to_chat("System", "Request was cancelled")
        
        # Reset voice mode state if needed
        if self.voice_mode:
            logger.debug("Resetting voice mode state after cancellation")
            # Voice controls will handle restarting voice input

    def on_voice_input_received(self, text: str):
        try:
            print(f"[DEBUG] ChatTab received voice input: {text}")
            logger.debug(f"Voice input received in chat tab: {text}", print_to_terminal=True)
            
            # Stop any current streaming
            if self.is_streaming:
                logger.debug("Stopping current streaming to process voice input")
                self.stop_streaming()
            
            # Process the voice input as a user message
            self.process_voice_input(text)
        except Exception as e:
            logger.error(f"Error in on_voice_input_received: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Try to add error message to chat
            try:
                self.append_to_chat("System", f"Error processing voice input: {str(e)}")
            except:
                pass
        
    def on_voice_input_received_direct(self, text: str):
        """Handle voice input received directly from voice service (fallback)"""
        try:
            print(f"[DEBUG] ChatTab received direct voice input: {text}")
            logger.debug(f"Direct voice input received in chat tab: {text}", print_to_terminal=True)
            
            # Stop any current streaming
            if self.is_streaming:
                logger.debug("Stopping current streaming to process direct voice input")
                self.stop_streaming()
            
            # Process the voice input as a user message
            self.process_voice_input(text)
        except Exception as e:
            logger.error(f"Error in on_voice_input_received_direct: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Try to add error message to chat
            try:
                self.append_to_chat("System", f"Error processing direct voice input: {str(e)}")
            except:
                pass

    def process_voice_input(self, text: str):
        """Process voice input as a user message"""
        try:
            print(f"[DEBUG] Processing voice input: '{text}'")
            logger.debug(f"Processing voice input: '{text}'", print_to_terminal=True)
            
            # Validate text before processing
            if not text or not text.strip():
                logger.warning("Empty voice input received, skipping")
                return
            
            # Clean the text (remove extra whitespace, etc.)
            cleaned_text = text.strip()
            
            # Add user message to chat immediately for voice input
            print(f"[DEBUG] Adding voice input to chat display: '{cleaned_text}'")
            logger.debug(f"Adding voice input to chat display: '{cleaned_text}'", print_to_terminal=True)
            self.append_to_chat("You", cleaned_text)
            
            # Start streaming for AI response
            print(f"[DEBUG] Starting streaming for voice input")
            logger.debug("Starting streaming for voice input", print_to_terminal=True)
            self.start_streaming()
            
            # Emit message_sent signal to go through the same event bus system as text input
            # This ensures the message goes through the proper chat controller and conversation service
            print(f"[DEBUG] Emitting message_sent signal for voice input")
            logger.debug("Emitting message_sent signal for voice input", print_to_terminal=True)
            self.message_sent.emit(cleaned_text)
            
            # Add additional debug info
            print(f"[DEBUG] Voice mode: {self.voice_mode}")
            print(f"[DEBUG] Is streaming: {self.is_streaming}")
            logger.debug(f"Voice mode: {self.voice_mode}, Is streaming: {self.is_streaming}", print_to_terminal=True)
                
        except Exception as e:
            print(f"[DEBUG] Error processing voice input: {e}")
            logger.error(f"Error processing voice input: {e}", print_to_terminal=True)
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.append_to_chat("System", f"Error processing voice input: {str(e)}")

    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        try:
            logger.error(f"Voice input error: {error}")
            self.append_to_chat("System", f"Voice input error: {error}")
        except Exception as e:
            logger.error(f"Error in on_voice_input_error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
        
    def on_tts_started(self):
        """Handle TTS started"""
        try:
            # Show EQ visualizer if in voice mode and EQ is enabled
            if self.voice_mode and self.eq_visualizer.get_eq_mode() != "None":
                self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.scroll_area, self.voice_mode)
            # Don't hide chat display - let messages continue to appear
            # The EQ visualizer will overlay on top of the chat display
        except Exception as e:
            logger.error(f"Error in on_tts_started: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    def on_tts_finished(self):
        """Handle TTS finished"""
        # Prevent multiple calls to this method
        if hasattr(self, '_tts_finished_handled') and self._tts_finished_handled:
            return
        self._tts_finished_handled = True
        
        # Reset the flag after a short delay

        QTimer.singleShot(100, lambda: setattr(self, '_tts_finished_handled', False))
        
        logger.debug("TTS finished in chat tab")
        
        # Only restore chat display if not in voice mode with EQ visualizer active
        if not (self.voice_mode and 
                self.eq_visualizer.get_eq_mode() != "None" and 
                self.eq_visualizer.current_eq_widget and 
                self.eq_visualizer.current_eq_widget.isVisible()):
            try:
                self.eq_visualizer.switch_to_chat_display(self.chat_display.scroll_area)
                logger.debug("Successfully restored chat display after TTS finished")
            except Exception as e:
                logger.error(f"Error switching to chat display: {e}")
                # Force show chat display even if EQ visualizer fails
                try:
                    self.chat_display.scroll_area.show()
                    self.chat_display.scroll_area.setVisible(True)
                    self.chat_display.scroll_area.setEnabled(True)
                    logger.debug("Forced chat display to be visible after TTS finished")
                except Exception as e2:
                    logger.error(f"Failed to force show chat display: {e2}")
        else:
            logger.debug("TTS finished but EQ visualizer is active in voice mode, keeping EQ visualizer")
        
        # Don't call Event Bus directly - let the voice service handle it
        # The Event Bus will receive the TTS finished signal from the voice service
        # and handle worker thread cleanup separately
        
        # In voice mode, let the voice controls handle the continuous cycle
        # They will restart voice input after TTS finishes
    
    def on_tts_error(self, error: str):
        """Handle TTS error"""
        try:
            logger.error(f"TTS error: {error}")
            self.append_to_chat("System", f"TTS error: {error}")
        except Exception as e:
            logger.error(f"Error in on_tts_error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
        
    def on_recording_started(self):
        """Handle recording started"""
        try:
            logger.debug("Voice recording started")
        except Exception as e:
            logger.error(f"Error in on_recording_started: {e}")
        
    def on_recording_stopped(self):
        """Handle recording stopped"""
        try:
            logger.debug("Voice recording stopped")
        except Exception as e:
            logger.error(f"Error in on_recording_stopped: {e}")
        
    def on_recording_error(self, error: str):
        """Handle recording error"""
        try:
            logger.error(f"Recording error: {error}")
            self.append_to_chat("System", f"Recording error: {error}")
        except Exception as e:
            logger.error(f"Error in on_recording_error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
        
    def on_voice_processing_started(self):
        """Handle voice processing started"""
        try:
            logger.debug("Voice processing started")
        except Exception as e:
            logger.error(f"Error in on_voice_processing_started: {e}")
        
    def on_voice_processing_finished(self):
        """Handle voice processing finished"""
        try:
            logger.debug("Voice processing finished")
        except Exception as e:
            logger.error(f"Error in on_voice_processing_finished: {e}")
        
    def on_audio_level_changed(self, audio_level: float):
        """Handle audio level changes with throttling to prevent excessive processing"""
        try:
            # Throttle audio level processing to prevent excessive updates
            current_time = time.time()
            if hasattr(self, '_last_audio_level_time'):
                time_diff = current_time - self._last_audio_level_time
                if time_diff < 0.05:  # Only process every 50ms to prevent excessive updates
                    return
            
            self._last_audio_level_time = current_time
            
            logger.debug(f"[EQ DEBUG] on_audio_level_changed called - audio_level: {audio_level:.4f}")
            
            # Update EQ visualizer if in voice mode with EQ enabled
            if self.voice_mode and self.eq_visualizer.get_eq_mode() != "None":
                logger.debug(f"[EQ DEBUG] Calling update_eq_visualizer")
                if self.voice_controls_initialized and self.voice_controls:
                    # Enhanced TTS playing detection
                    tts_playing = self.voice_controls.is_tts_playing()
                    
                    # Additional check: if we're in voice mode and TTS should be playing
                    # but the voice controls don't detect it, we can infer from audio level patterns
                    if not tts_playing and audio_level > 0.05:
                        # If we have significant audio level in voice mode, it's likely TTS
                        # This helps catch cases where TTS detection might be delayed
                        tts_playing = True
                        logger.debug(f"[EQ DEBUG] Inferred TTS playing from audio level: {audio_level:.4f}")
                    
                    # Ensure EQ visualizer is properly initialized for voice mode
                    if not self.eq_visualizer.current_eq_widget:
                        logger.debug(f"[EQ DEBUG] EQ widget not initialized, switching to EQ visualizer")
                        self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.scroll_area, self.voice_mode)
                    
                    logger.debug(f"[EQ DEBUG] TTS playing: {tts_playing}, audio_level: {audio_level:.4f}")
                    self.eq_visualizer.update_eq_visualizer(audio_level, tts_playing)
            else:
                pass
        except Exception as e:
            logger.error(f"Error in on_audio_level_changed: {traceback.format_exc()}")
            raise (f"Error in on_audio_level_changed: {traceback.format_exc()}\n{e}")
        
    def on_eq_bars_changed(self, bar_values):
        """Handle EQ bar array changes and update the EQ visualizer directly"""
        try:
            if (self.voice_mode and 
                self.eq_visualizer.get_eq_mode() != "None" and
                self.eq_visualizer.current_eq_widget):
                # Use the EQ visualizer's safe update method
                self.eq_visualizer._update_eq_widget_safe(bar_values)
            else:
                logger.debug("[EQ DEBUG] EQ visualizer not available or not in voice mode")
        except Exception as e:
            logger.error(f"[EQ DEBUG] Error in on_eq_bars_changed: {e}")
            import traceback
            logger.error(f"[EQ DEBUG] Traceback: {traceback.format_exc()}")

    def on_message_edited(self, message_index: int, new_content: str):
        """Handle message edit"""
        self.message_edited.emit(message_index, new_content)
        
    # Note: Voice mode changes are handled by on_input_mode_changed method
    
    def get_ai_name(self) -> str:
        """Get the AI name based on current personality"""
        # Try to get AI name from the parent window's chat controller
        try:
            if hasattr(self.parent, 'get_chat_controller'):
                chat_controller = self.parent.get_chat_controller()
                if chat_controller:
                    return chat_controller.get_ai_name()
        except Exception as e:
            logger.debug(f"Could not get chat controller: {e}")
        
        # Fallback: try to get the personality service from the parent window
        try:
            if hasattr(self.parent, 'get_service_manager'):
                service_manager = self.parent.get_service_manager()
                if hasattr(service_manager, 'get_personality_service'):
                    personality_service = service_manager.get_personality_service()
                    if personality_service:
                        return personality_service.get_ai_name()
        except Exception as e:
            logger.debug(f"Could not get personality service: {e}")
        
        # Fallback: try to get personality info from personality tab
        try:
            if hasattr(self.parent, 'get_ui_manager'):
                ui_manager = self.parent.get_ui_manager()
                personality_tab = ui_manager.get_personality_tab()
                if personality_tab and hasattr(personality_tab, 'personality_model'):
                    return personality_tab.personality_model.get_ai_name()
        except Exception as e:
            logger.debug(f"Could not get personality model: {e}")
        
        # Final fallback: return the personality name or "AI"
        personality_name = self.get_current_personality()
        return personality_name if personality_name else "AI"
        
    def get_current_personality(self) -> str:
        """Get the currently selected personality"""
        return self.input_controls.get_current_personality()
        
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.input_controls.get_current_model()
        
    def get_temperature(self) -> float:
        """Get the current temperature setting"""
        return self.input_controls.get_temperature()
        
    def get_current_response(self) -> str:
        """Get the current streaming response"""
        return self.input_controls.get_current_response()
        
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        """Append a message to the chat display"""
        logger.debug("Calling chat_display.append_to_chat", print_to_terminal=True)
        self.chat_display.append_to_chat(sender, message, is_code)
        
        logger.debug("chat_display.append_to_chat completed", print_to_terminal=True)
        
        # Force immediate UI update for new messages
        chat_renderer = self.chat_display.get_streaming_handler()
        if chat_renderer and hasattr(chat_renderer, 'request_render'):
            chat_renderer.request_render(immediate=True)
        
    def _force_chat_display_update(self):
        """Force immediate update of the chat display"""
        try:
            # Ensure chat display is visible and updated
            if hasattr(self, 'chat_display') and self.chat_display:
                # Force update of the chat display widget
                if hasattr(self.chat_display, 'chat_display') and self.chat_display.scroll_area:
                    self.chat_display.scroll_area.update()
                    
                    # Ensure scroll to bottom
                    cursor = self.chat_display.scroll_area.textCursor()
                    from PySide6.QtGui import QTextCursor
                    cursor.movePosition(QTextCursor.MoveOperation.End)
                    self.chat_display.scroll_area.setTextCursor(cursor)
                    
                    # Force layout update
                    self.chat_display.scroll_area.updateGeometry()
                    
                # Force update of the scroll area
                if hasattr(self.chat_display, 'scroll_area') and self.chat_display.scroll_area:
                    self.chat_display.scroll_area.update()
                    
        except Exception as e:
            logger.error(f"Error in _force_chat_display_update: {e}")
    
    def append_response_chunk(self, chunk: str, model_name: str = None, msg_id: str = None, chunk_index: int = None):
        """Append a streaming response chunk (single call per chunk, all args required)."""
        logger.debug(f"[CHAT_TAB_DEBUG] append_response_chunk called with chunk: {chunk[:50]}, model_name: {model_name}, msg_id: {msg_id}, chunk_index: {chunk_index}")
        QTimer.singleShot(0, lambda: self._append_response_chunk_safe(chunk, model_name, msg_id, chunk_index))

    def _append_response_chunk_safe(self, chunk: str, model_name: str = None, msg_id: str = None, chunk_index: int = None):
        """Append a streaming response chunk safely in the main thread, now with msg_id and chunk_index support."""
        try:
            logger.debug(f"[CHAT_TAB_DEBUG] _append_response_chunk_safe called with chunk: {chunk[:50]}, model_name: {model_name}, msg_id: {msg_id}, chunk_index: {chunk_index}")
            self._ensure_chat_display_visible()
            if not hasattr(self, 'is_streaming') or not self.is_streaming:
                logger.debug("[PATCH] Starting streaming")
                self.start_streaming()
            if not hasattr(self, 'is_streaming'):
                self.is_streaming = True
            self.current_response += chunk
            if hasattr(self, '_chunk_count'):
                self._chunk_count += 1
            else:
                self._chunk_count = 1
            ai_name = self.get_ai_name()
            label = f"{ai_name} ({model_name})" if model_name else ai_name
            # Only call chat_display.append_response_chunk ONCE per chunk, with all args
            logger.debug(f"[CHAT_TAB_DEBUG] Calling chat_display.append_response_chunk with chunk: {chunk[:50]}, model_name: {model_name}, msg_id: {msg_id}, chunk_index: {chunk_index}")
            self.chat_display.append_response_chunk(chunk, model_name, msg_id, chunk_index=chunk_index)
        except Exception as e:
            logger.error(f"[PATCH] Error in _append_response_chunk_safe: {e}")
            logger.error(f"[PATCH] _append_response_chunk_safe traceback: {traceback.format_exc()}")
    
    def _ensure_chat_display_visible(self):
        """Ensure the chat display is visible for message display"""
        try:
            # Don't force chat display visibility if EQ visualizer is active in voice mode
            if (self.voice_mode and 
                self.eq_visualizer.get_eq_mode() != "None" and 
                self.eq_visualizer.current_eq_widget and 
                self.eq_visualizer.current_eq_widget.isVisible()):
                logger.debug("EQ visualizer is active in voice mode, not forcing chat display visibility")
                return
            
            # Check if chat display is hidden and force it to be visible
            if hasattr(self, 'chat_display') and self.chat_display.scroll_area:
                if not self.chat_display.scroll_area.isVisible():
                    logger.debug("Chat display was hidden, forcing it to be visible")
                    self.chat_display.scroll_area.show()
                    self.chat_display.scroll_area.setVisible(True)
                    self.chat_display.scroll_area.setEnabled(True)
                    
                    # Force layout update
                    self.chat_display.scroll_area.updateGeometry()
                    self.chat_display.scroll_area.update()
                    from pyside_chat.core.utils.threading_utils import safe_process_events_alternative
                    safe_process_events_alternative()
                    logger.debug("Successfully made chat display visible")
        except Exception as e:
            logger.error(f"Error ensuring chat display visibility: {e}")
        
    def start_streaming(self):
        """Start streaming state (UI only updates, no internal is_streaming flag)."""
        QTimer.singleShot(0, self._start_streaming_safe)

    def _start_streaming_safe(self):
        """Start streaming state safely in the main thread (UI only)."""
        input_components = self.input_controls.get_ui_components()
        # Button state now handled by conversation service signals
        self.update()

    def stop_streaming(self):
        """Stop streaming state (UI only updates, no internal is_streaming flag)."""
        logger.debug("[DEBUG] stop_streaming called (UI only)")
        # Finalize streaming message in conversation service
        if hasattr(self, 'chat_controller') and hasattr(self.chat_controller, 'conversation_service'):
            try:
                conversation_service = self.chat_controller.conversation_service
                conversation_service.finalize_streaming_message()
                logger.debug("[ID:STOP001] Finalized streaming message in conversation service")
            except Exception as e:
                logger.error(f"[ID:STOP002] Error finalizing streaming in conversation service: {e}")
                logger.error(f"[ID:STOP003] Stop streaming traceback: {traceback.format_exc()}")
        else:
            streaming_handler = self.chat_display.get_streaming_handler()
            if streaming_handler:
                streaming_handler.finalize_streaming_message()
                logger.debug("[ID:STOP001] Finalized streaming message in streaming handler")
            else:
                logger.warning("[ID:STOP004] No streaming handler found")
        # UI state will be updated by conversation service signals
        self.update()
    
    def force_enable_send_button(self):
        """Force enable the send button and ensure UI is updated"""
        # Use QTimer.singleShot to ensure this method runs in the main thread
        QTimer.singleShot(0, self._force_enable_send_button_safe)

    def _force_enable_send_button_safe(self):
        """Force enable the send button safely in the main thread (emergency UI reset only)"""
        logger.debug("Force enabling send button")
        self.is_streaming = False
        input_components = self.input_controls.get_ui_components()
        # Only manage send/cancel buttons in text mode (emergency UI reset only)
        if not self.voice_mode:
            input_components['send_button'].setEnabled(True)
            input_components['send_button'].setVisible(True)
            input_components['cancel_button'].setVisible(False)
            logger.debug("[VOICE DEBUG] Text mode: force enabled send button (emergency UI reset)")
        else:
            # In voice mode, buttons should remain hidden
            logger.debug("[VOICE DEBUG] Voice mode: buttons remain hidden")
        input_components['send_button'].update()
        input_components['cancel_button'].update()
        from pyside_chat.core.utils.threading_utils import safe_process_events_alternative
        safe_process_events_alternative()
        logger.debug(f"Send button enabled: {input_components['send_button'].isEnabled()}, visible: {input_components['send_button'].isVisible()}")
    
    def clear_chat(self):
        """Clear the chat display and reset all references"""
        try:
            logger.debug("[CHAT_TAB] Clearing chat display and resetting references")
            
            # Clear the chat display
            self.chat_display.clear_chat()
            
            # Reset current conversation file
            self.current_conversation_file = None
            
            logger.debug("[CHAT_TAB] Chat display cleared and references reset successfully")
            
        except Exception as e:
            logger.error(f"[CHAT_TAB] Error clearing chat: {e}")
        
    def update_model_list(self, models: list):
        """Update the model combo box with available models"""
        self.input_controls.update_model_list(models)
    
    def update_personality_list(self, personalities: list):
        """Update the personality combo box with available personalities"""
        self.input_controls.update_personality_list(personalities)
    
    def speak_ai_response(self, text: str):
        """Speak AI response using TTS"""
        logger.debug(f"[CHAT_TAB] speak_ai_response called with text length: {len(text)}")
        logger.debug(f"[CHAT_TAB] voice_mode: {self.voice_mode}, voice_controls_initialized: {self.voice_controls_initialized}")
        
        # Ensure voice controls are initialized if in voice mode
        if self.voice_mode and not self.voice_controls_initialized:
            logger.debug("Voice mode active but voice controls not initialized, initializing now")
            self._ensure_voice_controls_initialized()
        
        if self.voice_controls_initialized and self.voice_controls:
            try:
                logger.debug(f"[CHAT_TAB] Calling voice_controls.speak_ai_response")
                self.voice_controls.speak_ai_response(text)
                logger.debug(f"TTS request sent for AI response: {text[:50]}...")
            except Exception as e:
                logger.error(f"Failed to speak AI response: {e}")
                import traceback
                logger.error(f"TTS error traceback: {traceback.format_exc()}")
        else:
            logger.warning("Voice controls not available for TTS")
            logger.debug(f"[CHAT_TAB] voice_controls_initialized: {self.voice_controls_initialized}, voice_controls: {self.voice_controls}")

    def open_voice_settings(self):
        """Open voice settings dialog"""
        try:
            logger.debug("Opening voice settings dialog")
            print("[DEBUG] Opening voice settings dialog")
            
            # Ensure voice controls are initialized
            self._ensure_voice_controls_initialized()
            
            if not self.voice_controls_initialized or not self.voice_controls:
                logger.warning("Voice controls not available for settings dialog")
                QMessageBox.warning(self, "Voice Settings", "Voice controls are not available.")
                return
            
            logger.debug("Creating VoiceSettingsDialog")
            dialog = VoiceSettingsDialog(self, self.config_manager)
            logger.debug("VoiceSettingsDialog created successfully")
            
            # Get current voice settings
            current_settings = self.voice_controls.get_voice_settings()
            logger.debug(f"Current voice settings: {current_settings}")
            dialog.set_settings(current_settings)
            
            # Connect the settings changed signal
            dialog.settings_changed.connect(self.on_voice_settings_changed)
            # Connect the EQ visualizer changed signal for immediate UI updates
            dialog.eq_visualizer_changed.connect(self.on_eq_visualizer_changed_immediate)
            
            logger.debug("Showing voice settings dialog")
            result = dialog.exec()
            logger.debug(f"Voice settings dialog result: {result}")
            
            if result == QDialog.DialogCode.Accepted:
                # Settings were saved
                new_settings = dialog.get_settings()
                logger.debug(f"New voice settings: {new_settings}")
                self.voice_controls.update_voice_settings(new_settings)
                
                # Update EQ visualizer mode if changed
                new_eq_mode = new_settings.get("eq_visualizer", "None")
                if new_eq_mode != self.eq_visualizer.get_eq_mode():
                    self.eq_visualizer.update_eq_visualizer_mode(new_eq_mode)
                    
        except Exception as e:
            logger.error(f"Error opening voice settings dialog: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            QMessageBox.critical(self, "Error", f"Failed to open voice settings: {str(e)}")
    
    def on_eq_visualizer_changed_immediate(self, eq_mode: str):
        """Handle immediate EQ visualizer changes from the settings dialog"""
        logger.debug(f"[EQ DEBUG] Immediate EQ visualizer change: {eq_mode}")
        
        # Update the EQ visualizer mode immediately
        if eq_mode != self.eq_visualizer.get_eq_mode():
            self.eq_visualizer.update_eq_visualizer_mode(eq_mode)
            
            # If in voice mode, switch to the new EQ visualizer immediately
            if self.voice_mode and eq_mode != "None":
                self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.scroll_area, self.voice_mode)
                logger.debug(f"[EQ DEBUG] Switched to EQ visualizer: {eq_mode}")
            elif self.voice_mode and eq_mode == "None":
                # Switch back to chat display if EQ is disabled
                self.eq_visualizer.switch_to_chat_display(self.chat_display.scroll_area)
                logger.debug("[EQ DEBUG] Switched back to chat display")
    
    def on_eq_visualizer_changed_from_voice_controls(self, eq_mode: str):
        """Handle EQ visualizer changes from voice controls"""
        logger.debug(f"[EQ DEBUG] EQ visualizer change from voice controls: {eq_mode}")
        
        # Update the EQ visualizer mode
        if eq_mode != self.eq_visualizer.get_eq_mode():
            self.eq_visualizer.update_eq_visualizer_mode(eq_mode)
            
            # If in voice mode, switch to the new EQ visualizer immediately
            if self.voice_mode and eq_mode != "None":
                self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.scroll_area, self.voice_mode)
                logger.debug(f"[EQ DEBUG] Switched to EQ visualizer from voice controls: {eq_mode}")
            elif self.voice_mode and eq_mode == "None":
                # Switch back to chat display if EQ is disabled
                self.eq_visualizer.switch_to_chat_display(self.chat_display.scroll_area)
                logger.debug("[EQ DEBUG] Switched back to chat display from voice controls")
    
    def on_voice_settings_changed(self, settings: dict):
        """Handle voice settings changes"""
        # Update voice controls if initialized
        if self.voice_controls_initialized and self.voice_controls:
            self.voice_controls.update_voice_settings(settings)
            
            # Update EQ visualizer mode if changed
            new_eq_mode = settings.get("eq_visualizer", "None")
            if new_eq_mode != self.eq_visualizer.get_eq_mode():
                self.eq_visualizer.update_eq_visualizer_mode(new_eq_mode)
    
    def load_conversation(self, filepath: str):
        """Load a conversation from file"""
        logger.debug(f"[LOAD_DEBUG] Attempting to load conversation: {filepath}")
        
        # Verify chat controller connection first
        self.verify_chat_controller_connection()
        
        try:
            # CRITICAL FIX: Use conversation service to load the conversation
            if hasattr(self, 'chat_controller') and self.chat_controller and hasattr(self.chat_controller, 'conversation_service'):
                # Extract filename from filepath
                import os
                filename = os.path.basename(filepath)
                
                # Load conversation through conversation service
                logger.debug(f"[LOAD_DEBUG] Loading conversation {filename} through conversation service")
                conversation_service = self.chat_controller.conversation_service
                logger.debug(f"[LOAD_DEBUG] Conversation service: {conversation_service}")
                
                # Load the conversation
                loaded_messages = conversation_service.load_conversation(filename)
                logger.debug(f"[LOAD_DEBUG] Loaded {len(loaded_messages)} messages from conversation service")
                
                # Ensure chat display is connected to conversation service
                if hasattr(self, 'chat_display'):
                    self.chat_display.set_conversation_service(conversation_service)
                    logger.debug("[LOAD_DEBUG] Set conversation service in chat display")
                
                # No need to sync manually - the conversation service will emit signals
                # and the chat display will update automatically through the signal connection
                
                logger.debug(f"[LOAD_FIX] Loaded conversation {filename} through conversation service")
            else:
                # Fallback to old method if conversation service not available
                logger.warning("[LOAD_FIX] Conversation service not available, using fallback method")
                logger.debug(f"[LOAD_DEBUG] Chat controller: {getattr(self, 'chat_controller', None)}")
                self._load_conversation_fallback(filepath)
            
            # Set current conversation file
            self.current_conversation_file = filepath
            self.set_current_conversation_file(filepath)
            
            # Load metadata if available
            try:
                from pyside_chat.core.models.conversation_metadata import ConversationMetadata
                metadata = ConversationMetadata.from_file(filepath)

                # Restore settings from metadata
                if metadata.temperature is not None:
                    self.temperature = metadata.temperature
                    input_components = self.input_controls.get_ui_components()
                    input_components['temperature_slider'].setValue(int(metadata.temperature * 100))

                if metadata.model and metadata.model in [self.input_controls.model_combo.itemText(i) for i in range(self.input_controls.model_combo.count())]:
                    self.input_controls.model_combo.setCurrentText(metadata.model)

                if metadata.personality and metadata.personality in [self.input_controls.personality_combo.itemText(i) for i in range(self.input_controls.personality_combo.count())]:
                    self.input_controls.personality_combo.setCurrentText(metadata.personality)

            except Exception as e:
                logger.warning(f"Could not load conversation metadata: {e}")

        except Exception as e:
            logger.error(f"Failed to load conversation: {str(e)}")
            import traceback
            logger.error(f"Load conversation traceback: {traceback.format_exc()}")
            QMessageBox.critical(self, "Error", f"Failed to load conversation: {str(e)}")
    
    def _load_conversation_fallback(self, filepath: str):
        """Fallback method for loading conversation when conversation service is not available"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Determine conversation list
            if isinstance(data, dict):
                conversation = data.get('conversation', [])
            elif isinstance(data, list):
                conversation = data
            else:
                conversation = []

            # Clear current chat
            self.clear_chat()

            # Load messages using the chat display
            for message in conversation:
                if isinstance(message, dict):
                    sender_raw = message.get('sender') or message.get('role', 'Unknown')
                    sender = sender_raw[:1].upper() + sender_raw[1:] if sender_raw else "Unknown"
                    content = message.get('content', '')
                    is_code = message.get('is_code', False)
                elif isinstance(message, str):
                    sender = 'Unknown'
                    content = message
                    is_code = False
                else:
                    continue  # skip unrecognized message types

                # Add message to chat display
                self.chat_display.append_to_chat(sender, content, is_code)

        except Exception as e:
            logger.error(f"Error in fallback conversation loading: {e}")
            raise
    
    def refresh_navigation(self):
        """Refresh the navigation widget"""
        if hasattr(self, 'navigation_widget'):
            self.navigation_widget.refresh_conversations()
    
    def set_current_conversation_file(self, filepath: str):
        """Set the current conversation file in the navigation widget"""
        if hasattr(self, 'navigation_widget'):
            self.navigation_widget.set_current_conversation(filepath)
    
    def set_chat_controller(self, chat_controller):
        """Set the chat controller reference"""
        self.chat_controller = chat_controller
        logger.debug(f"[CHAT_TAB] Chat controller set: {chat_controller}")
        
        # CRITICAL FIX: Connect to conversation service signals when chat controller is set
        if chat_controller and hasattr(chat_controller, 'conversation_service'):
            conversation_service = chat_controller.conversation_service
            logger.debug(f"[CHAT_TAB] Conversation service from controller: {conversation_service}")
            
            # Disconnect any existing connections to prevent signal loops
            try:
                if conversation_service and hasattr(conversation_service, 'conversation_updated'):
                    signal = conversation_service.conversation_updated
                    if signal and hasattr(signal, 'disconnect'):
                        # Check if signal has any connections before disconnecting
                        if hasattr(signal, 'receivers') and signal.receivers() > 0:
                            signal.disconnect()
                        else:
                            logger.debug("[CHAT_TAB] Signal has no receivers, skipping disconnect")
            except TypeError:
                # No existing connection, safe to ignore
                pass
            except Exception as e:
                logger.debug(f"[CHAT_TAB] Safe disconnect: {e}")
            
            # Connect to conversation service signals with a flag to prevent multiple connections
            if not hasattr(self, '_conversation_service_connected'):
                conversation_service.conversation_updated.connect(self._on_conversation_updated)
                self._conversation_service_connected = True
                logger.debug("[CHAT_TAB] Connected to conversation service signals after controller set")
            else:
                logger.debug("[CHAT_TAB] Conversation service already connected, skipping duplicate connection")
            
            # Set conversation service in chat display renderer
            if hasattr(self, 'chat_display'):
                self.chat_display.set_conversation_service(conversation_service)
                logger.debug("[CHAT_TAB] Set conversation service in chat display")
        else:
            logger.warning(f"[CHAT_TAB] Chat controller or conversation service not available: controller={chat_controller}")
    
    def verify_chat_controller_connection(self):
        """Verify that chat controller is properly connected"""
        if hasattr(self, 'chat_controller') and self.chat_controller:
            logger.debug(f"[CHAT_TAB] Chat controller is set: {self.chat_controller}")
            if hasattr(self.chat_controller, 'conversation_service'):
                logger.debug(f"[CHAT_TAB] Conversation service is available: {self.chat_controller.conversation_service}")
                return True
            else:
                logger.warning("[CHAT_TAB] Chat controller has no conversation service")
                return False
        else:
            logger.warning("[CHAT_TAB] Chat controller is not set")
            return False
    
    def get_streaming_handler(self):
        """Get the streaming handler for backward compatibility"""
        return self.chat_display.get_streaming_handler()
    
    @property
    def streaming_handler(self):
        """Property to access streaming handler for backward compatibility"""
        return self.chat_display.get_streaming_handler()

    def finalize_streaming_and_start_tts(self, tts_text):
        """Finalize chat display after streaming, then start TTS playback"""
        logger.debug("[VOICE] Finalizing streaming before starting TTS playback")
        def _finalize_and_start():
            try:
                # Finalize streaming message in the chat display
                streaming_handler = self.chat_display.get_streaming_handler()
                if streaming_handler:
                    streaming_handler.finalize_streaming_message()
                logger.debug("[VOICE] Chat display finalized, starting TTS playback")
                self.speak_ai_response(tts_text)
            except Exception as e:
                logger.error(f"[VOICE] Error finalizing streaming or starting TTS: {e}")
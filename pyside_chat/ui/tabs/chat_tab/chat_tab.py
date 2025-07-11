"""
Main Chat Tab Component - Orchestrates all chat interface components
"""

import sys
import os
import time
import json
import logging
import traceback
from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, Signal, QTimer, QThread, QMutex, QWaitCondition, QEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QScrollArea, QMessageBox,
    QDialog, QPushButton, QLabel
)

from pyside_chat.ui.widgets.chat_navigation import ChatNavigationWidget
from pyside_chat.ui.dialogs.voice_settings_dialog import VoiceSettingsDialog
from pyside_chat.core.models.conversation_metadata import ConversationManager
from pyside_chat.features.ollama.ollama_service import OllamaService
from pyside_chat.core.logging.logger import CustomLogger

# Import modular components
from .chat_display import ChatDisplay
from .voice_controls import VoiceControls
from .eq_visualizer import EQVisualizer
from .input_controls import InputControls

logger = CustomLogger.get_logger(__name__)

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
        
    def setup_components(self):
        """Initialize all modular components"""
        # Initialize voice controls with lazy loading (only when voice mode is activated)
        self.voice_controls = None
        self.voice_controls_initialized = False
        
        # Initialize EQ visualizer
        self.eq_visualizer = EQVisualizer(self)
        
        # Initialize input controls
        self.input_controls = InputControls(self)
        
        # Initialize chat display
        self.chat_display = ChatDisplay(self)
        
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
            
            # Voice settings button will be connected when voice controls are initialized
            
            logger.debug("[VOICE DEBUG] Signal connections setup completed successfully")
            
        except Exception as e:
            logger.error(f"[VOICE ERROR] Error setting up signal connections: {e}")
            logger.error(f"[VOICE ERROR] Traceback: {traceback.format_exc()}")
        
    def on_message_sent(self, message: str):
        """Handle message sent from input controls"""
        logger.debug(f"[VOICE DEBUG] on_message_sent called with message: '{message}', voice_mode: {self.voice_mode}")
        
        # Add user message to chat immediately
        self.append_to_chat("You", message)
        self.start_streaming()
        
        # Emit signal for parent
        logger.debug(f"[VOICE DEBUG] Emitting message_sent signal for parent")
        self.message_sent.emit(message)
        
    def on_message_cancelled(self):
        """Handle message cancelled from input controls"""
        self.stop_streaming()
        self.message_cancelled.emit()
        
    def _ensure_voice_controls_initialized(self):
        """Initialize voice controls if not already initialized"""
        if not self.voice_controls_initialized:
            try:
                logger.info("Initializing voice controls (lazy loading)")
                
                # Import and initialize voice controls
                from pyside_chat.ui.tabs.chat_tab.voice_controls import VoiceControls
                self.voice_controls = VoiceControls(self, self.config_manager)
                
                # Get voice settings and update EQ visualizer
                voice_settings = self.voice_controls.get_voice_settings()
                self.eq_visualizer.update_eq_visualizer_mode(voice_settings.get("eq_visualizer", "None"))
                
                # Replace placeholder widgets with actual voice controls
                voice_components = self.voice_controls.get_ui_components()
                
                # Remove placeholder widgets
                self.voice_button_placeholder.setParent(None)
                self.voice_settings_button_placeholder.setParent(None)
                self.audio_level_widget_placeholder.setParent(None)
                
                # Add actual voice control widgets
                voice_layout = self.voice_controls_widget.layout()
                voice_layout.addWidget(voice_components['voice_button'])
                voice_layout.addWidget(voice_components['voice_settings_button'])
                voice_layout.addWidget(voice_components['audio_level_widget'])
                
                # Connect voice control signals
                self.voice_controls.voice_input_received.connect(self.on_voice_input_received)
                self.voice_controls.voice_input_error.connect(self.on_voice_input_error)
                self.voice_controls.tts_started.connect(self.on_tts_started)
                self.voice_controls.tts_finished.connect(self.on_tts_finished)
                self.voice_controls.tts_error.connect(self.on_tts_error)
                self.voice_controls.recording_started.connect(self.on_recording_started)
                self.voice_controls.recording_stopped.connect(self.on_recording_stopped)
                self.voice_controls.recording_error.connect(self.on_recording_error)
                self.voice_controls.voice_processing_started.connect(self.on_voice_processing_started)
                self.voice_controls.voice_processing_finished.connect(self.on_voice_processing_finished)
                self.voice_controls.audio_level_changed.connect(self.on_audio_level_changed)
                
                # Connect voice settings button
                voice_components = self.voice_controls.get_ui_components()
                voice_components['voice_settings_button'].clicked.connect(self.open_voice_settings)
                
                self.voice_controls_initialized = True
                logger.info("Voice controls initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize voice controls: {e}")
                self.voice_controls = None
                self.voice_controls_initialized = False
    
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
            self.eq_visualizer.switch_to_chat_display(self.chat_display.chat_display)
            logger.debug("[VOICE DEBUG] Switched to Chat mode")
            
        elif mode == "Voice":
            # Initialize voice controls if not already initialized
            self._ensure_voice_controls_initialized()
            
            if self.voice_controls_initialized and self.voice_controls:
                # Show voice input widgets
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
                
                # Switch to EQ visualizer if enabled
                eq_mode = self.voice_controls.get_voice_settings().get("eq_visualizer", "None")
                if eq_mode != "None":
                    self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.chat_display, self.voice_mode)
                    logger.debug(f"[VOICE DEBUG] Switched to Voice mode with EQ: {eq_mode}")
                else:
                    logger.debug("[VOICE DEBUG] Switched to Voice mode without EQ")
            else:
                logger.error("Failed to initialize voice controls for voice mode")
    
    def on_temperature_changed(self, temperature: float):
        """Handle temperature change"""
        self.temperature = temperature
        logger.debug(f"Temperature changed to: {self.temperature}")
        
    def on_personality_changed(self, personality_name: str):
        """Handle personality change"""
        logger.debug(f"Personality changed to: {personality_name}")
        # Handle personality change logic here
        
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
        
    def on_voice_input_received(self, text: str):
        """Handle voice input received"""
        try:
            logger.debug(f"[VOICE DEBUG] on_voice_input_received called with text: '{text}'")
            
            # Log chat processing
            logger.info(f"Chat processing voice input: '{text}'", print_to_terminal=True)
            
            # Add the voice input to the chat
            self.append_to_chat("You", f"[Voice] {text}")
            
            # Send the message through the normal flow
            logger.debug(f"[VOICE DEBUG] Emitting message_sent signal with text: '{text}'")
            self.message_sent.emit(text)
            
            # In voice mode, we don't need to manage UI state here
            # The voice controls will handle the continuous cycle
            
        except Exception as e:
            logger.error(f"[VOICE ERROR] Error in on_voice_input_received: {e}")
            logger.error(f"[VOICE ERROR] Traceback: {traceback.format_exc()}")
            # Try to show error to user
            try:
                self.append_to_chat("System", f"Voice input error: {str(e)}")
            except:
                pass
    
    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        logger.error(f"Voice input error: {error}")
        self.append_to_chat("System", f"Voice input error: {error}")
        
    def on_tts_started(self):
        """Handle TTS started"""
        # Show EQ visualizer if in voice mode and EQ is enabled
        if self.voice_mode and self.eq_visualizer.get_eq_mode() != "None":
            self.eq_visualizer.switch_to_eq_visualizer(self.chat_display.chat_display, self.voice_mode)
        # Don't hide chat display - let messages continue to appear
        # The EQ visualizer will overlay on top of the chat display
    
    def on_tts_finished(self):
        """Handle TTS finished"""
        # Prevent multiple calls to this method
        if hasattr(self, '_tts_finished_handled') and self._tts_finished_handled:
            return
        self._tts_finished_handled = True
        
        # Reset the flag after a short delay
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, lambda: setattr(self, '_tts_finished_handled', False))
        
        logger.debug("TTS finished in chat tab")
        
        # Always restore chat display to ensure messages are visible
        try:
            self.eq_visualizer.switch_to_chat_display(self.chat_display.chat_display)
            logger.debug("Successfully restored chat display after TTS finished")
        except Exception as e:
            logger.error(f"Error switching to chat display: {e}")
            # Force show chat display even if EQ visualizer fails
            try:
                self.chat_display.chat_display.show()
                self.chat_display.chat_display.setVisible(True)
                self.chat_display.chat_display.setEnabled(True)
                logger.debug("Forced chat display to be visible after TTS finished")
            except Exception as e2:
                logger.error(f"Failed to force show chat display: {e2}")
        
        # Don't call Event Bus directly - let the voice service handle it
        # The Event Bus will receive the TTS finished signal from the voice service
        # and handle worker thread cleanup separately
        
        # In voice mode, let the voice controls handle the continuous cycle
        # They will restart voice input after TTS finishes
    
    def on_tts_error(self, error: str):
        """Handle TTS error"""
        logger.error(f"TTS error: {error}")
        
    def on_recording_started(self):
        """Handle recording started"""
        logger.debug("Voice recording started")
        
    def on_recording_stopped(self):
        """Handle recording stopped"""
        logger.debug("Voice recording stopped")
        
    def on_recording_error(self, error: str):
        """Handle recording error"""
        logger.error(f"Recording error: {error}")
        
    def on_voice_processing_started(self):
        """Handle voice processing started"""
        logger.debug("Voice processing started")
        
    def on_voice_processing_finished(self):
        """Handle voice processing finished"""
        logger.debug("Voice processing finished")
        
    def on_audio_level_changed(self, audio_level: float):
        """Handle audio level changes"""
        logger.debug(f"[EQ DEBUG] on_audio_level_changed called - audio_level: {audio_level:.4f}")
        
        # Update EQ visualizer if in voice mode with EQ enabled
        if self.voice_mode and self.eq_visualizer.get_eq_mode() != "None":
            logger.debug(f"[EQ DEBUG] Calling update_eq_visualizer")
            if self.voice_controls_initialized and self.voice_controls:
                tts_playing = self.voice_controls.is_tts_playing()
                self.eq_visualizer.update_eq_visualizer(audio_level, tts_playing)
        else:
            logger.debug(f"[EQ DEBUG] Skipping EQ update - voice_mode: {self.voice_mode}, eq_mode: {self.eq_visualizer.get_eq_mode()}")
        
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
        """Add a message to the chat display"""
        # Always append to chat display - never skip this
        # The EQ visualizer is just a visual overlay, it shouldn't prevent chat messages from appearing
        
        # Ensure chat display is visible for message display
        self._ensure_chat_display_visible()
        
        self.chat_display.append_to_chat(sender, message, is_code)
        
    def append_response_chunk(self, chunk: str, model_name: str = None):
        """Append a streaming response chunk"""
        # Use QTimer.singleShot to ensure this method runs in the main thread
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, lambda: self._append_response_chunk_safe(chunk, model_name))
    
    def _append_response_chunk_safe(self, chunk: str, model_name: str = None):
        """Append a streaming response chunk safely in the main thread"""
        try:
            logger.debug(f"[ID:CT001] _append_response_chunk_safe called - Chunk: {chunk[:50]}...")
            logger.debug(f"[ID:CT002] Model name: {model_name}")
            
            # Always append to chat display - never skip this
            # The EQ visualizer is just a visual overlay, it shouldn't prevent chat messages from appearing
            
            # Ensure chat display is visible for message display
            self._ensure_chat_display_visible()
                
            if not self.is_streaming:
                logger.debug("[ID:CT002A] Starting streaming")
                self.start_streaming()
            self.current_response += chunk  # accumulate here only!
            logger.debug(f"[ID:CT002B] Accumulated response length: {len(self.current_response)}")
            
            # Log the full accumulated message every 10 chunks to reduce log size
            if hasattr(self, '_chunk_count'):
                self._chunk_count += 1
            else:
                self._chunk_count = 1
                
            if self._chunk_count % 10 == 0:
                logger.debug(f"[DEBUG] Streaming progress - chunks: {self._chunk_count}, full message: {self.current_response[:200]}...")
            
            ai_name = self.get_ai_name()
            label = f"{ai_name} ({model_name})" if model_name else ai_name
            streaming_handler = self.chat_display.get_streaming_handler()
            if streaming_handler:
                streaming_handler.update_streaming_message(
                    self.current_response, label, None, False, tag="ai"
                )
                logger.debug(f"[ID:CT003] Updated streaming message with label: {label}")
            else:
                logger.warning("[ID:CT004] No streaming handler found")
                
        except Exception as e:
            logger.error(f"[ID:CT005] Error in _append_response_chunk_safe: {e}")
            logger.error(f"[ID:CT006] _append_response_chunk_safe traceback: {traceback.format_exc()}")
    
    def _ensure_chat_display_visible(self):
        """Ensure the chat display is visible for message display"""
        try:
            # Check if chat display is hidden and force it to be visible
            if hasattr(self, 'chat_display') and self.chat_display.chat_display:
                if not self.chat_display.chat_display.isVisible():
                    logger.debug("Chat display was hidden, forcing it to be visible")
                    self.chat_display.chat_display.show()
                    self.chat_display.chat_display.setVisible(True)
                    self.chat_display.chat_display.setEnabled(True)
                    
                    # Force layout update
                    self.chat_display.chat_display.updateGeometry()
                    self.chat_display.chat_display.update()
                    from PySide6.QtWidgets import QApplication
                    QApplication.processEvents()
                    logger.debug("Successfully made chat display visible")
        except Exception as e:
            logger.error(f"Error ensuring chat display visibility: {e}")
        
    def start_streaming(self):
        """Start streaming state"""
        # Use QTimer.singleShot to ensure this method runs in the main thread
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._start_streaming_safe)
    
    def _start_streaming_safe(self):
        """Start streaming state safely in the main thread"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            self._chunk_count = 0  # Reset chunk counter for new streaming session
            input_components = self.input_controls.get_ui_components()
            
            # Only manage send/cancel buttons in text mode
            if not self.voice_mode:
                input_components['send_button'].setEnabled(False)
                input_components['cancel_button'].setVisible(True)
                logger.debug("[VOICE DEBUG] Text mode: disabled send button, showed cancel button")
            else:
                # In voice mode, buttons should remain hidden
                logger.debug("[VOICE DEBUG] Voice mode: buttons remain hidden during streaming")
            
            ai_name = self.get_ai_name()
            streaming_handler = self.chat_display.get_streaming_handler()
            if streaming_handler:
                streaming_handler.start_streaming_message(ai_name, tag="ai")
            
            # Double-check that the button state is correct (only in text mode)
            if not self.voice_mode and input_components['send_button'].isEnabled():
                logger.warning("Send button was not disabled in text mode, forcing disable")
                input_components['send_button'].setEnabled(False)
                input_components['send_button'].update()
                from PySide6.QtWidgets import QApplication
                QApplication.processEvents()
        
    def stop_streaming(self):
        """Stop streaming state"""
        # Use QTimer.singleShot to ensure this method runs in the main thread
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._stop_streaming_safe)
    
    def _stop_streaming_safe(self):
        """Stop streaming state safely in the main thread"""
        logger.debug("[DEBUG] stop_streaming called. is_streaming: %s, voice_mode: %s", self.is_streaming, self.voice_mode)
        self.is_streaming = False
        input_components = self.input_controls.get_ui_components()
        
        # Only manage send/cancel buttons in text mode
        if not self.voice_mode:
            input_components['send_button'].setEnabled(True)
            input_components['send_button'].setVisible(True)
            input_components['cancel_button'].setVisible(False)
            logger.debug("[VOICE DEBUG] Text mode: enabled send button, hid cancel button")
        else:
            # In voice mode, buttons should remain hidden
            logger.debug("[VOICE DEBUG] Voice mode: buttons remain hidden after streaming")
        
        logger.debug(f"[DEBUG] stop_streaming: send_button enabled? {input_components['send_button'].isEnabled()} visible? {input_components['send_button'].isVisible()} cancel_button visible? {input_components['cancel_button'].isVisible()}")
        
        # Log the final complete message
        if hasattr(self, '_chunk_count') and self._chunk_count > 0:
            logger.debug(f"[DEBUG] Streaming completed - total chunks: {self._chunk_count}, final message: {self.current_response}")
        
        streaming_handler = self.chat_display.get_streaming_handler()
        if streaming_handler:
            streaming_handler.finalize_streaming_message()
        input_components['send_button'].update()
        input_components['cancel_button'].update()
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        
        # Double-check that the button is actually enabled (only in text mode)
        if not self.voice_mode and not input_components['send_button'].isEnabled():
            logger.warning("Send button was not enabled in text mode, forcing enable")
            input_components['send_button'].setEnabled(True)
            input_components['send_button'].update()
            QApplication.processEvents()
    
    def force_enable_send_button(self):
        """Force enable the send button and ensure UI is updated"""
        # Use QTimer.singleShot to ensure this method runs in the main thread
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._force_enable_send_button_safe)
    
    def _force_enable_send_button_safe(self):
        """Force enable the send button safely in the main thread"""
        logger.debug("Force enabling send button")
        self.is_streaming = False
        input_components = self.input_controls.get_ui_components()
        
        # Only manage send/cancel buttons in text mode
        if not self.voice_mode:
            input_components['send_button'].setEnabled(True)
            input_components['send_button'].setVisible(True)
            input_components['cancel_button'].setVisible(False)
            logger.debug("[VOICE DEBUG] Text mode: force enabled send button")
        else:
            # In voice mode, buttons should remain hidden
            logger.debug("[VOICE DEBUG] Voice mode: buttons remain hidden")
        
        input_components['send_button'].update()
        input_components['cancel_button'].update()
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        logger.debug(f"Send button enabled: {input_components['send_button'].isEnabled()}, visible: {input_components['send_button'].isVisible()}")
    
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.clear_chat()
        
    def update_model_list(self, models: list):
        """Update the model combo box with available models"""
        self.input_controls.update_model_list(models)
    
    def update_personality_list(self, personalities: list):
        """Update the personality combo box with available personalities"""
        self.input_controls.update_personality_list(personalities)
    
    def speak_ai_response(self, text: str):
        """Trigger TTS for AI response"""
        logger.debug(f"[VOICE DEBUG] speak_ai_response called with text: '{text[:50]}...', voice_mode: {self.voice_mode}")
        if self.voice_controls_initialized and self.voice_controls:
            self.voice_controls.speak_ai_response(text)
    
    def open_voice_settings(self):
        """Open voice settings dialog"""
        # Ensure voice controls are initialized
        self._ensure_voice_controls_initialized()
        
        if not self.voice_controls_initialized or not self.voice_controls:
            QMessageBox.warning(self, "Voice Settings", "Voice controls are not available.")
            return
        
        dialog = VoiceSettingsDialog(self, self.config_manager)
        dialog.set_settings(self.voice_controls.get_voice_settings())
        
        # Connect the settings changed signal
        dialog.settings_changed.connect(self.on_voice_settings_changed)
        
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Settings were saved
            self.voice_controls.update_voice_settings(dialog.get_settings())
            
            # Update EQ visualizer mode if changed
            new_eq_mode = dialog.get_settings().get("eq_visualizer", "None")
            if new_eq_mode != self.eq_visualizer.get_eq_mode():
                self.eq_visualizer.update_eq_visualizer_mode(new_eq_mode)
    
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
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Clear current chat
            self.clear_chat()
            
            # Load messages
            streaming_handler = self.chat_display.get_streaming_handler()
            if streaming_handler:
                for message in data:
                    sender = message.get('sender', 'Unknown')
                    content = message.get('content', '')
                    is_code = message.get('is_code', False)
                    tag = message.get('tag', 'user' if sender == 'You' else 'ai')
                    
                    streaming_handler.append_message(sender, content, is_code, tag)
            
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
            QMessageBox.critical(self, "Error", f"Failed to load conversation: {str(e)}")
    
    def refresh_navigation(self):
        """Refresh the navigation widget"""
        if hasattr(self, 'navigation_widget'):
            self.navigation_widget.refresh_conversations()
    
    def set_current_conversation_file(self, filepath: str):
        """Set the current conversation file in the navigation widget"""
        if hasattr(self, 'navigation_widget'):
            self.navigation_widget.set_current_conversation(filepath)
    
    def get_streaming_handler(self):
        """Get the streaming handler for backward compatibility"""
        return self.chat_display.get_streaming_handler()
    
    @property
    def streaming_handler(self):
        """Property to access streaming handler for backward compatibility"""
        return self.chat_display.get_streaming_handler() 
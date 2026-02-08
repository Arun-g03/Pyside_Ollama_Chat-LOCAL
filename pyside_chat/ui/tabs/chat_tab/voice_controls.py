# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.utils.threading_utils import *


"""
Voice Controls Component - Voice mode, TTS, STT, and audio level handling
"""

import logging
import traceback
from typing import Dict, Optional

logger = CustomLogger.get_logger(__name__)


def safe_disconnect(signal, slot=None, logger=logger):
    try:
        if signal is not None and hasattr(signal, 'disconnect'):
            try:
                if slot is not None:
                    signal.disconnect(slot)
                    logger.debug(
                        f"[SAFE DISCONNECT] Disconnected {slot} from {signal}")
                else:
                    signal.disconnect()
                    logger.debug(
                        f"[SAFE DISCONNECT] Disconnected all slots from {signal}")
            except Exception as e:
                logger.debug(
                    f"[SAFE DISCONNECT] Could not disconnect {slot} from {signal}: {e}")
        else:
            logger.debug(
                f"[SAFE DISCONNECT] Signal {signal} is None or has no disconnect method, skipping")
    except Exception as e:
        logger.error(f"[SAFE DISCONNECT] Exception during disconnect: {e}")


class VoiceControls(QObject):
    """Voice Controls component for voice mode, TTS, and audio level handling"""

    # Signals
    voice_input_received = Signal(str)  # Emitted when voice input is received
    voice_input_error = Signal(str)  # Emitted when voice input error occurs
    tts_started = Signal()  # Emitted when TTS starts
    tts_finished = Signal()  # Emitted when TTS finishes
    tts_error = Signal(str)  # Emitted when TTS error occurs
    recording_started = Signal()  # Emitted when recording starts
    recording_stopped = Signal()  # Emitted when recording stops
    recording_error = Signal(str)  # Emitted when recording error occurs
    voice_processing_started = Signal()  # Emitted when voice processing starts
    voice_processing_finished = Signal()  # Emitted when voice processing finishes
    audio_level_changed = Signal(float)  # Emitted when audio level changes
    voice_mode_changed = Signal(bool)  # Emitted when voice mode changes
    user_interrupted = Signal()  # Emitted when user interrupts the current AI response
    request_cancelled = Signal()  # Emitted when a request is cancelled
    # New status signal
    # Emitted when voice service status changes
    voice_status_changed = Signal(str)
    # New EQ visualizer signal
    # Emitted when EQ visualizer setting changes
    eq_visualizer_changed = Signal(str)
    eq_bars_changed = Signal(list)  # NEW: EQ bar array for visualization

    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager
        self._voice_signals_connected = False  # Ensure guard flag is always defined

        # Thread safety improvements
        self._mutex = QMutex()
        self._voice_state = {
            'is_recording': False,
            'is_processing': False,
            'is_playing_tts': False
        }

        # Crash recovery mechanisms
        self._crash_recovery_timer = QTimer()
        self._crash_recovery_timer.setSingleShot(True)
        self._crash_recovery_timer.timeout.connect(self._attempt_recovery)
        self._error_count = 0
        self._max_errors = 3
        self._error_reset_timer = QTimer()
        self._error_reset_timer.setSingleShot(True)
        self._error_reset_timer.timeout.connect(self._reset_error_count)

        # Voice service (singleton)
        self.voice_service = None
        self.voice_service_initialized = False

        # Callbacks for when service becomes ready
        self._ready_callbacks = []

        # Add a timer to periodically check button state
        self._ui_refresh_timer = QTimer()
        self._ui_refresh_timer.timeout.connect(self._periodic_ui_refresh)
        self._ui_refresh_timer.start(5000)  # Check every 5 seconds

        # Add a timer to clear last processed voice input
        self._clear_voice_input_timer = QTimer()
        self._clear_voice_input_timer.setSingleShot(True)
        self._clear_voice_input_timer.timeout.connect(
            self._clear_last_voice_input)

        # Load voice settings from config or use defaults
        if self.config_manager:
            self.voice_settings = self.config_manager.get_voice_settings()
        else:
            self.voice_settings = {
                "stt_api": "Vosk",  # Only Vosk is supported
                "tts_api": "Coqui TTS",
                "tts_voice": "en",
                "auto_speak": True,
                "voice_speed": 2,  # Faster default speed
                "recording_timeout": 10.0,
                "silence_duration": 2.0,
                "silence_threshold": 0.005,
                "eq_visualizer": "None"  # Default to no EQ visualizer
            }

        # Initialize voice service
        self._initialize_voice_service()

        # State variables
        self.voice_mode = False
        self.recording_start_time = None

        # UI components
        self.voice_button = None
        self.voice_settings_button = None
        self.audio_level_widget = None
        self.audio_level_label = None
        self.audio_level_meter = None

        # Setup UI components
        self.setup_ui_components()

        # Setup connections
        self.setup_connections()

    def setup_ui_components(self):
        """Setup UI components for voice controls"""
        # Voice button
        self.voice_button = QPushButton("🎤 Start Voice")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ffffff;
            }
        """)

        # Initially disable the button until voice service is ready
        self.voice_button.setEnabled(False)
        self.voice_button.setToolTip("Voice service initializing...")

        # Voice settings button
        self.voice_settings_button = QPushButton("⚙️")
        self.voice_settings_button.setToolTip("Voice Settings")
        self.voice_settings_button.setFixedSize(32, 32)
        self.voice_settings_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)

        # Audio level widget
        self.audio_level_widget = QWidget()
        self.audio_level_widget.setVisible(False)
        self.audio_level_widget.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        audio_layout = QVBoxLayout(self.audio_level_widget)
        audio_layout.setContentsMargins(5, 5, 5, 5)

        # Audio level label
        self.audio_level_label = QLabel("🎤 Ready")
        self.audio_level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_level_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                background-color: #2d2d2d;
                border: 1px solid #555;
                border-radius: 5px;
            }
        """)

        # Audio level meter
        self.audio_level_meter = QProgressBar()
        self.audio_level_meter.setRange(0, 100)
        self.audio_level_meter.setValue(0)
        self.audio_level_meter.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                text-align: center;
                background-color: #1e1e1e;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 2px;
            }
        """)

        audio_layout.addWidget(self.audio_level_label)
        audio_layout.addWidget(self.audio_level_meter)

        # Initially hide voice-related widgets
        self.voice_button.hide()
        self.voice_settings_button.hide()
        self.audio_level_widget.hide()

    def _update_voice_button_state(self, enabled: bool, status: str = ""):
        """Update the voice button state based on voice service status"""
        # Safety check: ensure UI components exist
        if not hasattr(self, 'voice_button') or self.voice_button is None:
            logger.debug(
                "Voice button not available yet, skipping state update",
                print_to_terminal=True)
            return

        logger.info(
            f"Updating voice button state: enabled={enabled}, status='{status}'",
            print_to_terminal=True)

        self.voice_button.setEnabled(enabled)

        if enabled:
            self.voice_button.setToolTip("Click to start voice mode")
            if not self.voice_mode:
                self.voice_button.setText("🎤 Start Voice")
                self.voice_button.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: #ffffff;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 16px;
                        font-size: 14px;
                        font-weight: bold;
                        min-width: 120px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                    QPushButton:pressed {
                        background-color: #1e7e34;
                    }
                    QPushButton:disabled {
                        background-color: #6c757d;
                        color: #ffffff;
                    }
                """)
                logger.info(
                    "Voice button enabled and styled for Start Voice",
                    print_to_terminal=True)
        else:
            tooltip = f"Voice service {status.lower()}" if status else "Voice service not ready"
            self.voice_button.setToolTip(tooltip)
            self.voice_button.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: #ffffff;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 120px;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                    color: #ffffff;
                }
            """)
            logger.info(
                f"Voice button disabled with status: {status}",
                print_to_terminal=True)

    def _update_voice_state(self, key: str, value: bool):
        """Thread-safe voice state update"""
        with QMutexLocker(self._mutex):
            self._voice_state[key] = value

    def is_voice_busy(self) -> bool:
        """Thread-safe check if voice is busy"""
        with QMutexLocker(self._mutex):
            return any(self._voice_state.values())

    def _handle_voice_crash(self):
        """Handle voice service crashes gracefully"""
        logger.error("Voice service crash detected, attempting recovery...")

        # Stop current operations
        self._stop_all_voice_operations()

        # Reset UI state
        self._reset_voice_ui()

        # Attempt recovery after delay
        self._crash_recovery_timer.start(2000)  # 2 second delay

    def _attempt_recovery(self):
        """Attempt to recover voice service"""
        try:
            # Reinitialize voice service
            self._reinitialize_voice_service()
            logger.info("Voice service recovery successful")
        except Exception as e:
            logger.error(f"Voice service recovery failed: {e}")
            self._disable_voice_features()

    def _stop_all_voice_operations(self):
        """Stop all voice operations safely"""
        try:
            voice_service = self.get_voice_service()
            if voice_service:
                if hasattr(voice_service, 'stop_voice_input'):
                    voice_service.stop_voice_input()
                if hasattr(voice_service, 'stop_tts'):
                    voice_service.stop_tts()
        except Exception as e:
            logger.error(f"Error stopping voice operations: {e}")

    def _reset_voice_ui(self):
        """Reset voice UI to safe state"""
        try:
            self.voice_mode = False
            self._reset_voice_button()
            self._update_voice_state('is_recording', False)
            self._update_voice_state('is_processing', False)
            self._update_voice_state('is_playing_tts', False)
        except Exception as e:
            logger.error(f"Error resetting voice UI: {e}")

    def _reinitialize_voice_service(self):
        """Reinitialize voice service (for recovery)"""
        try:
            # Reset signal connection flag to allow reconnection after reinit
            self.reset_voice_signal_connections()
            self.force_reinitialize_voice_service()
            logger.info(
                "Voice service reinitialization triggered for recovery")
        except Exception as e:
            logger.error(f"Error reinitializing voice service: {e}")

    def _disable_voice_features(self):
        """Disable voice features after failed recovery"""
        try:
            self.voice_mode = False
            self._reset_voice_button()
            logger.warning("Voice features disabled due to repeated failures")
        except Exception as e:
            logger.error(f"Error disabling voice features: {e}")

    def _reset_error_count(self):
        """Reset error count after timeout"""
        self._error_count = 0

    def _handle_service_error(self, error: str):
        """Handle service errors with exponential backoff"""
        self._error_count += 1
        logger.error(
            f"Voice service error ({self._error_count}/{self._max_errors}): {error}")

        if self._error_count >= self._max_errors:
            logger.error(
                "Too many voice service errors, disabling voice features")
            self._disable_voice_features()
        else:
            # Reset error count after delay
            self._error_reset_timer.start(5000)  # 5 second delay

    def setup_connections(self):
        """Setup signal connections"""
        # Voice service connections will be established when voice service is
        # lazy loaded

        # Connect voice button
        self.voice_button.clicked.connect(self.toggle_voice_mode)

    def _initialize_voice_service(self):
        """Initialize the voice service with direct connection"""
        try:
            # Immediately emit initializing status
            self.voice_status_changed.emit("Initializing")
            logger.info(
                "Starting voice service initialization",
                print_to_terminal=True)

            # Use consolidated voice service directly
            from pyside_chat.features.voice.voice_service import VoiceService
            self.voice_service = VoiceService.get_instance()
            service_type = "VoiceService"
            print(f"[VOICE CONTROLS] Using {service_type} for direct voice processing")
            logger.info("Using simplified voice service for direct voice processing", print_to_terminal=True)

            # Connect voice service signals directly
            self.voice_service.voice_service_ready.connect(
                self._on_voice_service_ready)
            self.voice_service.voice_input_received.connect(
                self._on_voice_input_received)
            self.voice_service.voice_input_error.connect(
                self._on_voice_input_error)
            self.voice_service.tts_started.connect(
                self._on_tts_started)
            self.voice_service.tts_finished.connect(
                self._on_tts_finished)
            self.voice_service.tts_error.connect(
                self._on_tts_error)
            self.voice_service.recording_started.connect(
                self._on_recording_started)
            self.voice_service.recording_stopped.connect(
                self._on_recording_stopped)
            self.voice_service.recording_error.connect(
                self._on_recording_error)
            self.voice_service.audio_level_changed.connect(
                self._on_audio_level_changed)
            self.voice_service.eq_bars_changed.connect(
                self._on_eq_bars_changed)
            self.voice_service.user_interrupted.connect(
                self.on_user_interrupted)
            self.voice_service.request_cancelled.connect(
                self.on_request_cancelled)

            # Apply initial settings
            self.voice_service.update_settings(self.voice_settings)

            # Check if voice input is ready (STT + Recording)
            # TTS is not required for voice input
            if self.voice_service.is_voice_input_available():
                logger.info(f"{service_type} is ready for voice input", print_to_terminal=True)
                self.voice_status_changed.emit("Ready")
                self.voice_service_initialized = True
                
                # Update button state if UI components are ready
                if hasattr(self, 'voice_button') and self.voice_button is not None:
                    self._update_voice_button_state(True, "Ready")
                    logger.info("Voice button enabled", print_to_terminal=True)
            else:
                logger.info(f"{service_type} is initializing", print_to_terminal=True)
                self.voice_status_changed.emit("Initializing")
                
                # Update button state if UI components are ready
                if hasattr(self, 'voice_button') and self.voice_button is not None:
                    self._update_voice_button_state(False, "Initializing")

            logger.info(f"{service_type} initialization completed", print_to_terminal=True)

        except Exception as e:
            logger.error(
                f"Failed to initialize voice service: {e}",
                print_to_terminal=True)
            self.voice_service = None
            self.voice_status_changed.emit("Error: Failed to initialize service")

    def force_ui_refresh(self):
        """Force UI refresh to update button state based on current voice service status"""
        logger.info(
            "Forcing UI refresh for voice controls",
            print_to_terminal=True)

        if hasattr(self, 'voice_button') and self.voice_button is not None:
            if self.voice_service and self.voice_service.is_voice_input_available():
                logger.info(
                    "Voice input is ready, enabling button",
                    print_to_terminal=True)
                self._update_voice_button_state(True, "Ready")
                self.voice_status_changed.emit("Ready")
            elif self.voice_service and self.voice_service.is_initializing():
                logger.info(
                    "Voice service is initializing, keeping button disabled",
                    print_to_terminal=True)
                self._update_voice_button_state(False, "Initializing")
                self.voice_status_changed.emit("Initializing")
            else:
                logger.info(
                    "Voice service not ready, keeping button disabled",
                    print_to_terminal=True)
                self._update_voice_button_state(False, "Uninitialized")
                self.voice_status_changed.emit("Uninitialized")
        else:
            logger.debug(
                "Voice button not available for UI refresh",
                print_to_terminal=True)

    def _on_voice_service_ready(self):
        """Handle voice service ready signal"""
        logger.info(
            "Simplified voice service ready signal received",
            print_to_terminal=True)
        self.voice_status_changed.emit("Ready")

        # Enable the voice button when service is ready
        logger.info(
            "Calling _update_voice_button_state(True, 'Ready')",
            print_to_terminal=True)
        self._update_voice_button_state(True, "Ready")

        if self.voice_service:
            # Reset signal connection flag for new voice service
            self.reset_voice_signal_connections()
            self.voice_service_initialized = True
            logger.info(
                "Simplified voice service ready and connections established",
                print_to_terminal=True)
        else:
            logger.error(
                "Voice service is None after ready signal",
                print_to_terminal=True)

    def _on_direct_voice_service_ready(self):
        """Handle direct voice service ready signal (from VoiceService)"""
        logger.info(
            "Simplified voice service ready signal received",
            print_to_terminal=True)

        # Enable the voice button when service is ready
        self._update_voice_button_state(True, "Ready")
        self.voice_status_changed.emit("Ready")

        # If we're in voice mode but button was disabled, start voice mode now
        if self.voice_mode and not self.voice_button.isEnabled():
            logger.debug("Voice service ready, starting voice mode")
            self._start_continuous_voice_mode()

    def _periodic_ui_refresh(self):
        """Periodically check and update UI state"""
        # Only refresh if voice controls are initialized and voice button exists
        if (hasattr(self, 'voice_button') and
            self.voice_button is not None and
                self.voice_service):

            # Only update if status changed
            # Check voice input availability (STT + Recording), not full voice service
            current_status = "Ready" if self.voice_service.is_voice_input_available() else "Initializing"
            if not hasattr(
                    self,
                    '_last_periodic_status') or self._last_periodic_status != current_status:
                self._last_periodic_status = current_status
                if current_status == "Ready":
                    self._update_voice_button_state(True, "Ready")
                    self.voice_status_changed.emit("Ready")
                else:
                    self._update_voice_button_state(False, "Initializing")
                    self.voice_status_changed.emit("Initializing")

    def _on_voice_service_error(self, error: str):
        """Handle voice service error signal"""
        logger.error(f"Simplified voice service error: {error}", print_to_terminal=True)
        self.voice_input_error.emit(
            f"Voice service initialization failed: {error}")
        self.voice_status_changed.emit(f"Error: {error}")

        # Keep button disabled on error
        self._update_voice_button_state(False, "Error")

    def _on_voice_service_initializing(self):
        """Handle voice service initializing signal"""
        logger.info(
            "Simplified voice service initialization started",
            print_to_terminal=True)
        self.voice_status_changed.emit("Initializing")

        # Keep button disabled during initialization
        self._update_voice_button_state(False, "Initializing")

    def get_voice_service(self):
        """Get voice service with lazy loading"""
        if not self.voice_service:
            self._initialize_voice_service()

        if self.voice_service:
            # Return the simplified voice service
            return self.voice_service

        logger.warning("Voice service not available")
        return None

    def _setup_voice_connections(self):
        """Setup voice service connections (simplified)"""
        # Connections are now handled directly in _initialize_voice_service
        # This method is kept for compatibility but does nothing
        logger.debug("Voice connections already established in initialization")
        pass

    def _disconnect_voice_signals(self):
        """Disconnect voice service signals with comprehensive error handling"""
        try:
            log_thread_info("Disconnecting voice signals")

            if not self._voice_signals_connected:
                logger.debug(
                    "Voice signals not connected, skipping disconnect")
                return

            if not self.voice_service:
                logger.warning(
                    "Voice service not available for signal disconnection")
                return

            # Disconnect signals with error handling
            try:

                # Disconnect all voice service signals
                safe_signal_disconnect(self.voice_service.voice_input_received)
                safe_signal_disconnect(self.voice_service.voice_input_error)
                safe_signal_disconnect(self.voice_service.tts_started)
                safe_signal_disconnect(self.voice_service.tts_finished)
                safe_signal_disconnect(self.voice_service.tts_error)
                safe_signal_disconnect(self.voice_service.recording_started)
                safe_signal_disconnect(self.voice_service.recording_stopped)
                safe_signal_disconnect(self.voice_service.recording_error)
                safe_signal_disconnect(self.voice_service.audio_level_changed)
                safe_signal_disconnect(self.voice_service.eq_bars_changed)
                safe_signal_disconnect(self.voice_service.voice_status_changed)

                self._voice_signals_connected = False
                logger.info(
                    "Voice service signal connections disconnected successfully")

            except Exception as e:
                logger.error(f"Error disconnecting voice service signals: {e}")
                import traceback
                logger.error(
                    f"Signal disconnection error traceback: {traceback.format_exc()}")

        except Exception as e:
            logger.error(f"Error in _disconnect_voice_signals: {e}")
            import traceback
            logger.error(
                f"Disconnect voice signals error traceback: {traceback.format_exc()}")

    def reset_voice_signal_connections(self):
        """Reset the internal guard flag to allow reconnection if needed (e.g., after re-init)."""
        self._voice_signals_connected = False

    def _is_voice_service_ready(self) -> bool:
        """Check if voice service is ready for voice input"""
        try:
            if self.voice_service:
                # For voice input, we only need STT and Recording, not TTS
                return self.voice_service.is_voice_input_available()
            return False
        except Exception as e:
            logger.error(f"Error checking voice service readiness: {e}")
            return False

    def _validate_voice_service_capabilities(self, voice_service):
        """Validate that voice service has required capabilities"""
        try:
            # Check if simplified voice service has required methods
            required_methods = [
                'start_voice_input',
                'stop_voice_input', 
                'speak_text',
                'stop_tts',
                'is_voice_available',
                'update_settings'
            ]
            
            for method in required_methods:
                if not hasattr(voice_service, method):
                    logger.error(f"Voice service missing required method: {method}")
                    return False
            
            # Check if voice input is available (STT + Recording)
            # TTS is not required for voice input validation
            if not voice_service.is_voice_input_available():
                logger.warning("Voice input not available (STT or Recording not ready)")
                return False
                
            logger.info("Voice service capabilities validated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error validating voice service capabilities: {e}")
            return False

    def reset_voice_service(self):
        """Reset voice service (for reinitialization)"""
        try:
            logger.info("Resetting simplified voice service")
            
            # Disconnect all signals
            self._disconnect_voice_signals()
            
            # Reset state
            self.voice_service_initialized = False
            self.voice_service = None
            
            # Reinitialize
            self._initialize_voice_service()
            
            logger.info("Voice service reset completed")
            
        except Exception as e:
            logger.error(f"Error resetting voice service: {e}")

    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        try:
            logger.debug(f"Toggle voice mode called, current state: {self.voice_mode}")

            if not self.voice_mode:
                # Start voice mode
                logger.debug("Starting voice mode")
                self.voice_mode = True
                logger.debug(f"[VOICE DEBUG] Voice mode set to: {self.voice_mode}")
                self.voice_status_changed.emit("Ready")
                self.voice_button.setText("🎤 Stop Voice")
                self.voice_button.setStyleSheet("""
                    QPushButton {
                        background-color: #dc3545;
                        color: #ffffff;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 16px;
                        font-size: 14px;
                        font-weight: bold;
                        min-width: 120px;
                    }
                    QPushButton:hover {
                        background-color: #c82333;
                    }
                    QPushButton:pressed {
                        background-color: #bd2130;
                    }
                """)
                self.voice_mode_changed.emit(True)

                # Start continuous voice mode
                self._start_continuous_voice_mode()

            else:
                # Stop voice mode with proper cleanup
                logger.debug("Stopping voice mode")
                self.voice_mode = False
                self._reset_voice_button()

                # Clean up voice service state
                try:
                    if self.voice_service:
                        # Disable continuous voice mode
                        self.voice_service.set_continuous_voice_mode(False)

                        # Stop any remaining operations
                        if self.voice_service.is_recording:
                            self.voice_service.stop_voice_input()
                        if self.voice_service.is_playing_tts:
                            self.voice_service.stop_tts()

                        logger.debug("Voice service operations stopped successfully")

                except Exception as e:
                    logger.error(f"Error stopping voice processes: {e}")

                self.voice_mode_changed.emit(False)
                logger.debug("Voice mode stopped successfully")

        except Exception as e:
            logger.error(f"Error in toggle_voice_mode: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Reset to safe state
            self.voice_mode = False
            self._reset_voice_button()
            self.voice_status_changed.emit(f"Error: {str(e)}")

    def _start_continuous_voice_mode(self):
        """Start continuous voice mode cycle"""
        if not self.voice_mode:
            logger.debug(
                "Cannot start continuous voice mode: voice_mode is False")
            return

        logger.debug("Starting continuous voice mode cycle",
                     print_to_terminal=True)

        # Enable continuous voice mode in the voice service
        try:
            if self.voice_service:
                logger.debug(
                    "Voice service available for continuous mode", print_to_terminal=True)

                # Check if voice input (STT + Recording) is available
                # TTS is not required for voice input, only for output
                if not self.voice_service.is_voice_input_available():
                    logger.error(
                        "Voice input not ready yet (STT or Recording not available), cannot start voice input", print_to_terminal=True)
                    self.voice_mode = False
                    self._reset_voice_button()
                    return

                # Validate capabilities
                if not self._validate_voice_service_capabilities(self.voice_service):
                    logger.error(
                        "Voice service missing required capabilities for continuous mode", print_to_terminal=True)
                    self.voice_mode = False
                    self._reset_voice_button()
                    return

                # Set continuous mode
                logger.debug("Setting continuous voice mode",
                             print_to_terminal=True)
                self.voice_service.set_continuous_voice_mode(True)
                logger.debug("Continuous voice mode enabled")

                # Start voice input
                logger.debug("Starting voice input...", print_to_terminal=True)
                
                # Debug which service is being used
                service_type = type(self.voice_service).__name__
                print(f"[VOICE CONTROLS] Starting voice input with {service_type}")
                logger.debug(f"Using voice service type: {service_type}")
                
                self.voice_service.start_voice_input()
                print(f"[VOICE CONTROLS] ✅ Voice input started successfully with {service_type}")
                logger.debug("Voice input started successfully",
                             print_to_terminal=True)
            else:
                logger.error(
                    "Voice service not available for continuous mode", print_to_terminal=True)
                self.voice_mode = False
                self._reset_voice_button()
        except Exception as e:
            logger.error(
                f"Failed to start voice input: {e}", print_to_terminal=True)
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Reset voice mode on error
            self.voice_mode = False
            self._reset_voice_button()

    def _handle_voice_input_safe(self, text: str):
        """Handle voice input safely in the main thread"""
        try:
            print(f"[DEBUG] Voice controls received voice input: '{text}'")
            logger.debug(
                f"Voice controls received voice input: '{text}'", print_to_terminal=True)

            if not self.voice_mode:
                print(f"[DEBUG] Voice mode is False, ignoring voice input")
                logger.debug(
                    "Voice mode is False, ignoring voice input", print_to_terminal=True)
                return

            # Prevent duplicate processing with more robust detection
            current_time = time.time()

            # Initialize tracking variables if they don't exist
            if not hasattr(self, '_last_processed_voice_input'):
                self._last_processed_voice_input = None
            if not hasattr(self, '_last_voice_input_time'):
                self._last_voice_input_time = 0

            # Check for exact duplicate within a short time window (1 second)
            time_diff = current_time - self._last_voice_input_time
            if (self._last_processed_voice_input == text and
                    time_diff < 1.0):  # Increased window to 1 second
                print(
                    f"[DEBUG] Exact duplicate voice input detected within {time_diff:.2f}s, ignoring: '{text}'")
                logger.debug(
                    f"Exact duplicate voice input detected within {time_diff:.2f}s, ignoring: '{text}'", print_to_terminal=True)
                return

            # Check for similar voice input within a longer time window (2 seconds)
            if time_diff < 2.0:  # 2 second window for similar inputs
                if self._is_similar_voice_input(text, self._last_processed_voice_input):
                    print(
                        f"[DEBUG] Similar voice input detected within {time_diff:.1f}s, ignoring: '{text}'")
                    logger.debug(
                        f"Similar voice input detected within {time_diff:.1f}s, ignoring: '{text}'", print_to_terminal=True)
                    return

            # Update tracking variables
            self._last_processed_voice_input = text
            self._last_voice_input_time = current_time

            # Stop any existing timer before starting a new one
            self._clear_voice_input_timer.stop()
            # Clear the last processed voice input after 2 seconds
            self._clear_voice_input_timer.start(2000)

            logger.debug(f"Voice input received in continuous mode: {text}")

            # In non-interruptive mode, we don't stop voice input immediately
            # The voice service will handle stopping during processing and restarting during TTS
            logger.debug(
                "[VOICE DEBUG] Non-interruptive mode: voice input will be managed by voice service")

            # Forward to parent for processing - this goes to ChatTab.process_voice_input()
            print(f"\n🎤 VOICE CONTROLS: Emitting voice_input_received signal: '{text}'\n")
            logger.debug(
                f"Emitting voice_input_received signal with text: '{text}'", print_to_terminal=True)
            logger.debug(
                f"[EMIT] voice_controls.py: voice_input_received.emit({text!r}) from id={id(self)}")
            self.voice_input_received.emit(text)

            # Voice service will handle the flow:
            # 1. Stop voice input during processing
            # 2. Restart voice input during TTS (for non-interruptive mode)
            # 3. Restart voice input after TTS completion

        except Exception as e:
            print(f"[DEBUG] Error in _handle_voice_input_safe: {e}")
            logger.error(
                f"[VOICE ERROR] Error handling voice input: {e}", print_to_terminal=True)
            logger.error(f"[VOICE ERROR] Traceback: {traceback.format_exc()}")
            try:
                self.voice_input_error.emit(f"Voice input error: {str(e)}")
            except:
                pass
            raise

    def _handle_tts_finished_continuous(self):
        """Handle TTS finished in continuous voice mode"""
        if not self.voice_mode:
            return

        logger.debug("TTS finished in continuous voice mode")

        # Restart voice input for continuous mode
        QTimer.singleShot(500, self._restart_voice_input_for_continuous_mode)

    def _restart_voice_input_for_continuous_mode(self):
        """Restart voice input for continuous mode after TTS finishes"""
        if not self.voice_mode:
            return

        try:
            logger.debug("Restarting voice input for continuous mode after TTS")
            voice_service = self.get_voice_service()
            if voice_service:
                voice_service.start_voice_input()
                self.audio_level_label.setText("🎤 Continuous Recording...")
                logger.debug("Voice input restarted for continuous mode")
        except Exception as e:
            logger.error(f"Failed to restart voice input for continuous mode: {e}")

    def _restart_voice_input(self):
        """Restart voice input for continuous mode"""
        if not self.voice_mode:
            return

        try:
            logger.debug("Restarting voice input for continuous mode")
            voice_service = self.get_voice_service()
            voice_service.start_voice_input()
        except Exception as e:
            logger.error(f"Failed to restart voice input: {e}")
            # Reset voice mode on error
            self.voice_mode = False
            self._reset_voice_button()

    def _reset_voice_button(self):
        """Reset voice button to initial state"""
        self.voice_button.setText("🎤 Start Voice")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)

    def on_voice_input_received(self, text: str):
        """Handle voice input received - DEPRECATED: Use _on_voice_input_received instead"""
        # This method is deprecated and should not be used
        # Voice input is now handled directly in _on_voice_input_received
        logger.warning("on_voice_input_received called - this method is deprecated")
        return

    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        try:
            logger.error(f"Voice input error: {error}")

            # Handle service error
            self._handle_service_error(error)

            # Use QTimer.singleShot to ensure UI updates happen in the main thread
            QTimer.singleShot(
                0, lambda: self._handle_voice_input_error_safe(error))
        except Exception as e:
            logger.error(f"Error in on_voice_input_error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def _handle_voice_input_error_safe(self, error: str):
        """Handle voice input error safely in the main thread"""
        try:
            logger.debug(f"Voice input error received: {error}")

            # Check for queue full errors and auto-reset
            if "queue full" in error.lower() or "request queue full" in error.lower():
                logger.warning(
                    "Queue full error detected, attempting auto-reset")
                if self.reset_voice_service():
                    logger.info("Voice service auto-reset successful")
                    # Try to restart voice input if voice mode is still active
                    if self.voice_mode:
                        QTimer.singleShot(
                            1000, self._start_continuous_voice_mode)
                else:
                    logger.error("Voice service auto-reset failed")

            # Emit error signal with user-friendly message
            user_message = error
            if "queue full" in error.lower():
                user_message = "Voice system is busy. Please wait a moment and try again."
            elif "no speech detected" in error.lower():
                user_message = "No speech detected. Please speak clearly."

            self.voice_input_error.emit(user_message)

        except Exception as e:
            logger.error(f"Error handling voice input error: {e}")
            self.voice_input_error.emit(f"Voice input error: {str(e)}")
            raise

    def on_tts_started(self):
        """Handle TTS started"""
        try:
            logger.debug("TTS started")
            self.voice_status_changed.emit("Speaking")
            self.tts_started.emit()
        except Exception as e:
            logger.error(f"Error in on_tts_started: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def on_tts_finished(self):
        """Handle TTS finished"""
        try:
            logger.debug("TTS finished in voice controls")
            self.voice_status_changed.emit("Idle")

            # In continuous voice mode, restart voice input
            if self.voice_mode:
                self._handle_tts_finished_continuous()

            # Forward the signal
            self.tts_finished.emit()
        except Exception as e:
            logger.error(f"Error in on_tts_finished: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def on_tts_error(self, error: str):
        """Handle TTS error"""
        try:
            logger.error(f"TTS error: {error}")
            self.voice_status_changed.emit(f"TTS Error: {error}")

            # Handle service error
            self._handle_service_error(error)

            # Use QTimer.singleShot to ensure UI updates happen in the main thread
            QTimer.singleShot(0, lambda: self._handle_tts_error_safe(error))
        except Exception as e:
            logger.error(f"Error in on_tts_error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def _handle_tts_error_safe(self, error: str):
        """Handle TTS error safely in the main thread"""
        self.tts_error.emit(error)

    def on_recording_started(self):
        """Handle recording started"""
        logger.debug("Voice recording started")
        self.voice_status_changed.emit("Listening")

        # Use QTimer.singleShot to ensure UI updates happen in the main thread
        QTimer.singleShot(0, self._handle_recording_started_safe)

    def _handle_recording_started_safe(self):
        """Handle recording started safely in the main thread"""
        # Show audio level meter
        self.audio_level_widget.setVisible(True)

        # Show different message for continuous mode
        voice_service = self.get_voice_service()
        if voice_service and voice_service.is_continuous_voice_mode():
            self.audio_level_label.setText("🎤 Continuous Recording...")
            self.audio_level_label.setToolTip(
                "Continuous voice mode - recording will restart automatically")
        else:
            self.audio_level_label.setText("🎤 Recording...")
            silence_duration = voice_service.get_silence_duration() if voice_service else 3.0
            self.audio_level_label.setToolTip(
                f"Silence timeout: {silence_duration:.1f}s")

        self.audio_level_meter.setValue(0)

        # Record start time
        self.recording_start_time = time.time()

        self.recording_started.emit()

    def on_recording_stopped(self):
        """Handle recording stopped"""
        logger.debug("Voice recording stopped")
        self.voice_status_changed.emit("Idle")

        # Use QTimer.singleShot to ensure UI updates happen in the main thread
        QTimer.singleShot(0, self._handle_recording_stopped_safe)

    def _handle_recording_stopped_safe(self):
        """Handle recording stopped safely in the main thread"""
        # Only hide audio level meter if not in continuous mode
        voice_service = self.get_voice_service()
        if voice_service and not voice_service.is_continuous_voice_mode():
            self.audio_level_widget.setVisible(False)
            self.audio_level_label.setText("🎤 Ready")
            self.audio_level_meter.setValue(0)
        else:
            # Keep audio level widget visible for continuous mode
            self.audio_level_label.setText("🎤 Processing...")
            self.audio_level_meter.setValue(0)

        self.recording_stopped.emit()

    def on_recording_error(self, error: str):
        """Handle recording error"""
        logger.error(f"Recording error: {error}")
        self.voice_status_changed.emit(f"Recording Error: {error}")

        # Use QTimer.singleShot to ensure UI updates happen in the main thread
        QTimer.singleShot(0, lambda: self._handle_recording_error_safe(error))

    def _handle_recording_error_safe(self, error: str):
        """Handle recording error safely in the main thread"""
        # Only reset voice button state if not in continuous mode
        voice_service = self.get_voice_service()
        if voice_service and not voice_service.is_continuous_voice_mode():
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.audio_level_widget.setVisible(False)
            self.voice_mode_changed.emit(False)
        else:
            # Keep the button as "Stop Voice" for continuous mode
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_button.setToolTip(
                "Continuous voice mode active - click to stop")

        self.recording_error.emit(error)

    def on_voice_processing_started(self):
        """Handle voice processing started"""
        logger.debug("Voice processing started")
        # Keep button as "Stop Voice" during processing
        self.voice_button.setToolTip("Processing voice input...")
        self.voice_processing_started.emit()

    def on_voice_processing_finished(self):
        """Handle voice processing finished"""
        logger.debug("Voice processing finished")
        # Button will be reset to "Start Voice" when voice input is received or error occurs
        self.voice_processing_finished.emit()

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

            logger.debug(
                f"[EQ DEBUG] on_audio_level_changed called - audio_level: {audio_level:.4f}")

            # Enhanced audio level processing for better EQ responsiveness
            # Check if TTS is currently playing
            tts_playing = self.is_tts_playing()

            # Apply additional processing for TTS audio levels
            if tts_playing:
                # TTS audio often needs additional amplification for EQ visualization
                # The streaming audio player already does some enhancement, but we can add more here
                enhanced_level = audio_level * 1.2  # Additional 20% boost for TTS
                logger.debug(
                    f"[EQ DEBUG] TTS playing - enhanced level: {enhanced_level:.4f} (original: {audio_level:.4f})")
                audio_level = enhanced_level

            # Check for interruption during TTS playback
            if tts_playing and self._should_check_for_interruption(audio_level):
                self._handle_potential_interruption(audio_level)

            # Emit signal for parent to handle
            self.audio_level_changed.emit(audio_level)

            # Update EQ bars for visualization
            self._update_eq_bars(audio_level)

            # Use QTimer.singleShot to ensure UI updates happen in the main thread
            QTimer.singleShot(
                0, lambda: self._update_audio_level_ui_safe(audio_level))
        except Exception as e:
            logger.error(f"Error in on_audio_level_changed: {e}")

    def _update_audio_level_ui_safe(self, audio_level: float):
        """Update audio level UI safely in the main thread"""
        try:
            voice_service = self.get_voice_service()

            # Check if recording service is available
            if not voice_service or not hasattr(voice_service, 'recording_service') or not voice_service.recording_service:
                # Fallback for process manager mode
                self.audio_level_label.setText("🎤 Recording...")
                self.audio_level_meter.setValue(int(audio_level * 100))
                logger.debug(
                    f"[EQ DEBUG] Using fallback audio level meter update")
                return

            # Convert to dB
            db_level = voice_service.recording_service.audio_level_to_db(
                audio_level)

            # Update meter (0-100 range)
            # Convert -60dB to 0dB range to 0-100
            meter_value = min(100, max(0, int((db_level + 60) * 1.67)))
            self.audio_level_meter.setValue(meter_value)

            # Update label with dB level
            if audio_level > voice_service.get_silence_threshold():
                if voice_service.is_continuous_voice_mode():
                    self.audio_level_label.setText(
                        f"🎤 Recording... {db_level:.1f} dB")
                else:
                    self.audio_level_label.setText(
                        f"🎤 Recording... {db_level:.1f} dB")
                self.audio_level_label.setStyleSheet("""
                    QLabel {
                        color: #00ff00;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 5px;
                        background-color: #2d2d2d;
                        border: 1px solid #00ff00;
                        border-radius: 5px;
                    }
                """)
            else:
                if voice_service.is_continuous_voice_mode():
                    self.audio_level_label.setText(
                        f"🎤 Listening... {db_level:.1f} dB")
                else:
                    self.audio_level_label.setText(
                        f"🎤 Listening... {db_level:.1f} dB")
                self.audio_level_label.setStyleSheet("""
                    QLabel {
                        color: #ffff00;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 5px;
                        background-color: #2d2d2d;
                        border: 1px solid #ffff00;
                        border-radius: 5px;
                    }
                """)

        except Exception as e:
            logger.error(f"[EQ DEBUG] Error updating audio level: {e}")
            import traceback
            logger.error(
                f"[EQ DEBUG] Audio level error traceback: {traceback.format_exc()}")

    def speak_ai_response(self, text: str):
        """Speak AI response using TTS"""
        try:
            logger.debug(f"speak_ai_response called with text length: {len(text)}")
            logger.debug(f"Text preview: {text[:100]}...")

            # Validate text before TTS
            if not text or not text.strip():
                logger.warning("Empty text provided to speak_ai_response, skipping")
                return

            # Clean the text for TTS (remove markdown, extra whitespace, etc.)
            cleaned_text = text.strip()

            # Remove common markdown and formatting that shouldn't be spoken
            import re
            # Remove markdown code blocks
            cleaned_text = re.sub(r'```[\s\S]*?```', '', cleaned_text)
            # Remove inline code
            cleaned_text = re.sub(r'`([^`]+)`', r'\1', cleaned_text)
            # Remove markdown links but keep the text
            cleaned_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned_text)
            # Remove markdown headers
            cleaned_text = re.sub(r'^#{1,6}\s+', '', cleaned_text, flags=re.MULTILINE)
            # Remove markdown emphasis
            cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_text)  # Bold
            cleaned_text = re.sub(r'__(.*?)__', r'\1', cleaned_text)      # Italic
            cleaned_text = re.sub(r'_(.*?)_', r'\1', cleaned_text)        # Italic
            # Remove extra whitespace
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

            if not cleaned_text:
                logger.warning("Text was empty after cleaning, skipping TTS")
                return

            logger.debug(
                f"Cleaned text for TTS (length: {len(cleaned_text)}): {cleaned_text[:100]}...")

            if not self.voice_service:
                logger.error("Voice service not available for TTS")
                return

            try:
                # Use the voice service's speak_text method with non-streaming mode
                self.voice_service.speak_text(cleaned_text)
                logger.debug(
                    f"TTS request sent for text: {cleaned_text[:50]}...")

            except Exception as e:
                logger.error(f"Failed to speak AI response: {e}")
                import traceback
                logger.error(f"TTS error traceback: {traceback.format_exc()}")

        except Exception as e:
            logger.error(f"Error in speak_ai_response: {e}")
            import traceback
            logger.error(
                f"speak_ai_response error traceback: {traceback.format_exc()}")

    def update_voice_settings(self, settings: dict):
        """Update voice settings"""
        try:
            self.voice_settings.update(settings)

            if self.voice_service:
                self.voice_service.update_settings(settings)
                logger.debug(
                    f"Updated voice service settings: {settings}")
            else:
                logger.warning(
                    "Voice service not available for settings update")
            # Emit EQ visualizer changed signal if EQ setting changes
            if 'eq_visualizer' in settings:
                self.eq_visualizer_changed.emit(settings['eq_visualizer'])
        except Exception as e:
            logger.error(f"Error updating voice settings: {e}")

    def get_voice_settings(self) -> dict:
        """Get current voice settings"""
        try:
            if self.voice_service:
                return self.voice_service.get_settings()
            return self.voice_settings.copy()
        except Exception as e:
            logger.error(f"Error getting voice settings: {e}")
            return self.voice_settings.copy()

    def is_voice_service_ready(self) -> bool:
        """Check if voice service is ready"""
        try:
            if self.voice_service:
                return self.voice_service.is_voice_available()
            return False
        except Exception as e:
            logger.error(f"Error checking if voice service is ready: {e}")
            return False

    def is_voice_service_initializing(self) -> bool:
        """Check if voice service is initializing"""
        try:
            if self.voice_service:
                return self.voice_service.is_initializing()
            return False
        except Exception as e:
            logger.error(
                f"Error checking if voice service is initializing: {e}")
            return False

    def get_voice_service_error(self) -> str:
        """Get the last voice service error"""
        if self.voice_service:
            return self.voice_service.get_last_error() or "No error"
        return "Voice service not available"

    def force_reinitialize_voice_service(self):
        """Force reinitialization of the voice service"""
        # Reset signal connection flag to allow reconnection after reinit
        self.reset_voice_signal_connections()
        if self.voice_service:
            # Reinitialize by getting a fresh instance
            from pyside_chat.features.voice.voice_service import VoiceService
            self.voice_service = VoiceService.get_instance()
            logger.info("Forced voice service reinitialization")
        else:
            logger.warning(
                "Voice service not available for reinitialization")

    def is_voice_mode_active(self) -> bool:
        """Check if voice mode is active"""
        return self.voice_mode

    def is_tts_playing(self) -> bool:
        """Check if TTS is currently playing"""
        if not self.voice_service:
            return False
        try:
            return self.voice_service.is_playing_tts
        except Exception as e:
            logger.error(f"Failed to check TTS playing status: {e}")
            return False

    def can_handle_interruption(self) -> bool:
        """Check if the system can handle user interruptions"""
        if not self.voice_service:
            return False
        try:
            return self.voice_service.voice_settings.get("allow_interruptions", True)
        except Exception as e:
            logger.error(f"Failed to check interruption capability: {e}")
            return False

    def get_interruption_threshold(self) -> float:
        """Get the audio level threshold for interruption detection"""
        if not self.voice_service:
            return 0.5  # Default threshold
        try:
            return self.voice_service.voice_settings.get("interruption_threshold", 0.5)
        except Exception as e:
            logger.error(f"Failed to get interruption threshold: {e}")
            return 0.5

    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'voice_button': self.voice_button,
            'voice_settings_button': self.voice_settings_button,
            'audio_level_widget': self.audio_level_widget
        }

    def on_user_interrupted(self):
        """Handle user interruption during AI response"""
        logger.info("User interruption detected in voice controls")

        # Emit signal for parent to handle
        self.user_interrupted.emit()

        # Update UI to show interruption
        self.audio_level_label.setText("🎤 Interrupted - Listening...")
        self.audio_level_label.setToolTip(
            "User interrupted AI response - ready for new input")

        # In continuous mode, restart voice input after a short delay
        if self.voice_mode:
            QTimer.singleShot(1000, self._restart_voice_input_after_interruption)

    def on_request_cancelled(self):
        """Handle request cancellation"""
        try:
            logger.info("Request cancelled in voice controls")

            # Update UI to show cancellation
            self.audio_level_label.setText("🎤 Cancelled - Ready")
            self.audio_level_label.setToolTip("Previous request was cancelled")

            # In continuous mode, restart voice input after a short delay
            if self.voice_mode:
                self._restart_voice_input_after_cancellation()

        except Exception as e:
            logger.error(f"Error handling request cancellation: {e}")

    def on_eq_bars_changed(self, bar_values):
        """Handle EQ bar array changes from the voice service and forward to parent (chat tab)"""
        self.eq_bars_changed.emit(bar_values)

    def _update_eq_bars(self, audio_level: float):
        """Update EQ bars based on audio level"""
        try:
            # Generate EQ bar values based on audio level
            # Create a simple frequency distribution for visualization
            num_bars = 10
            bar_values = []

            # Create a more realistic frequency distribution
            base_level = audio_level * 100  # Scale to 0-100 range

            for i in range(num_bars):
                # Create a bell curve distribution centered around the middle frequencies
                frequency_factor = 1.0 - \
                    abs(i - (num_bars // 2)) / (num_bars // 2)
                bar_value = base_level * frequency_factor * \
                    (0.5 + 0.5 * audio_level)
                bar_values.append(max(0, min(100, bar_value)))

            # Emit the EQ bars signal
            self.eq_bars_changed.emit(bar_values)

        except Exception as e:
            logger.error(f"[EQ DEBUG] Error in _update_eq_bars: {e}")
            import traceback
            logger.error(f"[EQ DEBUG] Traceback: {traceback.format_exc()}")

    def _restart_voice_input_after_interruption(self):
        """Restart voice input after user interruption"""
        if not self.voice_mode:
            return

        try:
            logger.debug("Restarting voice input after user interruption")
            voice_service = self.get_voice_service()
            if voice_service:
                voice_service.start_voice_input()
                self.audio_level_label.setText("🎤 Continuous Recording...")
                logger.debug("Voice input restarted after interruption")
        except Exception as e:
            logger.error(
                f"Failed to restart voice input after interruption: {e}")

    def _restart_voice_input_after_cancellation(self):
        """Restart voice input after request cancellation"""
        if not self.voice_mode:
            return

        try:
            logger.debug("Restarting voice input after request cancellation")
            voice_service = self.get_voice_service()
            if voice_service:
                voice_service.start_voice_input()
                self.audio_level_label.setText("🎤 Continuous Recording...")
                logger.debug("Voice input restarted after cancellation")
        except Exception as e:
            logger.error(
                f"Failed to restart voice input after cancellation: {e}")

    def _clear_last_voice_input(self):
        """Clear the last processed voice input to allow reprocessing"""
        try:
            if hasattr(self, '_last_processed_voice_input'):
                old_input = self._last_processed_voice_input
                delattr(self, '_last_processed_voice_input')
                logger.debug(
                    f"Cleared last processed voice input: '{old_input}'")
            if hasattr(self, '_last_voice_input_time'):
                delattr(self, '_last_voice_input_time')
                logger.debug("Cleared last voice input time")
        except Exception as e:
            logger.error(f"Error clearing last voice input: {e}")

    def _is_similar_voice_input(self, text1: str, text2: str) -> bool:
        """Check if two voice inputs are similar enough to be considered duplicates"""
        if not text1 or not text2:
            return False

        # Convert to lowercase for comparison
        t1 = text1.lower().strip()
        t2 = text2.lower().strip()

        # Exact match
        if t1 == t2:
            return True

        # Check if one is contained within the other (for partial matches)
        if len(t1) > 10 and len(t2) > 10:  # Only for longer inputs
            if t1 in t2 or t2 in t1:
                return True

        # Check for high similarity using word overlap
        words1 = set(t1.split())
        words2 = set(t2.split())

        if len(words1) > 0 and len(words2) > 0:
            overlap = len(words1.intersection(words2))
            total_words = len(words1.union(words2))
            similarity = overlap / total_words if total_words > 0 else 0

            # Consider similar if more than 70% word overlap
            return similarity > 0.7

        return False

    def _reset_duplicate_detection_state(self):
        """Reset the duplicate detection state for voice input."""
        try:
            if hasattr(self, '_last_processed_voice_input'):
                delattr(self, '_last_processed_voice_input')
            if hasattr(self, '_last_voice_input_time'):
                delattr(self, '_last_voice_input_time')
            if hasattr(self, '_clear_voice_input_timer'):
                self._clear_voice_input_timer.stop()
            logger.debug("Duplicate detection state reset.")
        except Exception as e:
            logger.error(f"Error resetting duplicate detection state: {e}")

    def cleanup(self):
        """Clean up voice controls and disconnect all signals"""
        try:
            logger.debug("Cleaning up voice controls")

            # Disconnect all signals
            self._disconnect_voice_signals()

            # Stop any ongoing operations
            if self.voice_service:
                try:
                    if hasattr(self.voice_service, 'is_recording') and self.voice_service.is_recording:
                        self.voice_service.stop_voice_input()
                    if hasattr(self.voice_service, 'is_playing_tts') and self.voice_service.is_playing_tts:
                        self.voice_service.stop_tts()
                except Exception as e:
                    logger.error(
                        f"Error stopping voice operations during cleanup: {e}")

            # Reset connection flag
            self._voice_signals_connected = False

            logger.debug("Voice controls cleanup completed")

        except Exception as e:
            logger.error(f"Error during voice controls cleanup: {e}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            self.cleanup()
        except Exception as e:
            logger.error(f"Error in voice controls destructor: {e}")

    def _on_voice_input_received(self, text: str):
        """Handle voice input received with comprehensive error handling"""
        try:
            log_thread_info(f"Voice input received: {text}")

            if not text or not text.strip():
                logger.warning("Empty voice input received")
                return

            # Check if TTS is playing and handle interruption
            if self.is_tts_playing():
                logger.info("User speaking over AI - handling interruption")
                self._handle_interruption_during_tts(text)
                return

            # Process the voice input directly here instead of emitting another signal
            # This prevents the double processing issue
            self._handle_voice_input_safe(text)

        except Exception as e:
            logger.error(f"Error in _on_voice_input_received: {e}")
            import traceback
            logger.error(
                f"Voice input received error traceback: {traceback.format_exc()}")

    def _handle_interruption_during_tts(self, text: str):
        """Handle voice input received while TTS is playing"""
        try:
            logger.info(f"Handling interruption during TTS: '{text}'")
            
            # Stop TTS playback
            if self.voice_service:
                self.voice_service.stop_tts()
                logger.debug("TTS stopped due to user interruption")
            
            # Emit interruption signal for parent to handle
            self.user_interrupted.emit()
            
            # Update UI to show interruption
            self.audio_level_label.setText("🎤 Interrupted - Processing...")
            self.audio_level_label.setToolTip("User interrupted AI response - processing new input")
            
            # Process the new voice input after a short delay
            QTimer.singleShot(500, lambda: self._process_interrupted_voice_input(text))
            
        except Exception as e:
            logger.error(f"Error in _handle_interruption_during_tts: {e}")

    def _process_interrupted_voice_input(self, text: str):
        """Process voice input that interrupted TTS"""
        try:
            logger.info(f"Processing interrupted voice input: '{text}'")
            
            # Update UI
            self.audio_level_label.setText("🎤 Processing...")
            
            # Process the voice input normally
            self._handle_voice_input_safe(text)
            
        except Exception as e:
            logger.error(f"Error in _process_interrupted_voice_input: {e}")

    def _on_voice_input_error(self, error: str):
        """Handle voice input error with comprehensive error handling"""
        try:
            log_thread_info(f"Voice input error: {error}")

            # Log the error
            logger.error(f"Voice input error: {error}")

            # Emit error signal with error handling
            try:
                self.voice_input_error.emit(error)
            except Exception as e:
                logger.error(f"Error emitting voice input error signal: {e}")

        except Exception as e:
            logger.error(f"Error in _on_voice_input_error: {e}")
            import traceback
            logger.error(
                f"Voice input error handler traceback: {traceback.format_exc()}")

    def _on_tts_started(self):
        """Handle TTS started with comprehensive error handling"""
        try:
            log_thread_info("TTS started")

            # Update UI state with error handling
            try:
                self.update_voice_status("TTS Playing")
                self.voice_button.setEnabled(False)
                logger.debug("TTS started - voice button disabled")
            except Exception as e:
                logger.error(f"Error updating UI for TTS started: {e}")

        except Exception as e:
            logger.error(f"Error in _on_tts_started: {e}")
            import traceback
            logger.error(
                f"TTS started error traceback: {traceback.format_exc()}")

    def _on_tts_finished(self):
        """Handle TTS finished with comprehensive error handling"""
        try:
            log_thread_info("TTS finished")

            # Update UI state with error handling
            try:
                self.update_voice_status("Ready")
                self.voice_button.setEnabled(True)
                logger.debug("TTS finished - voice button enabled")
                
                # In continuous mode, restart voice input after TTS finishes
                if self.voice_mode:
                    self._handle_tts_finished_continuous()
                    
            except Exception as e:
                logger.error(f"Error updating UI for TTS finished: {e}")

        except Exception as e:
            logger.error(f"Error in _on_tts_finished: {e}")
            import traceback
            logger.error(
                f"TTS finished error traceback: {traceback.format_exc()}")

    def _on_tts_error(self, error: str):
        """Handle TTS error with comprehensive error handling"""
        try:
            log_thread_info(f"TTS error: {error}")

            # Log the error
            logger.error(f"TTS error: {error}")

            # Update UI state with error handling
            try:
                self.update_voice_status("TTS Error")
                self.voice_button.setEnabled(True)
                logger.debug("TTS error - voice button enabled")
            except Exception as e:
                logger.error(f"Error updating UI for TTS error: {e}")

        except Exception as e:
            logger.error(f"Error in _on_tts_error: {e}")
            import traceback
            logger.error(
                f"TTS error handler traceback: {traceback.format_exc()}")

    def _on_recording_started(self):
        """Handle recording started with comprehensive error handling"""
        try:
            log_thread_info("Recording started")

            # Update UI state with error handling
            try:
                self.update_voice_status("Recording")
                self.voice_button.setText("Stop Recording")
                logger.debug("Recording started - UI updated")
            except Exception as e:
                logger.error(f"Error updating UI for recording started: {e}")

        except Exception as e:
            logger.error(f"Error in _on_recording_started: {e}")
            import traceback
            logger.error(
                f"Recording started error traceback: {traceback.format_exc()}")

    def _on_recording_stopped(self):
        """Handle recording stopped with comprehensive error handling"""
        try:
            log_thread_info("Recording stopped")

            # Update UI state with error handling
            try:
                self.update_voice_status("Processing")
                self.voice_button.setText("Start Recording")
                logger.debug("Recording stopped - UI updated")
            except Exception as e:
                logger.error(f"Error updating UI for recording stopped: {e}")

        except Exception as e:
            logger.error(f"Error in _on_recording_stopped: {e}")
            import traceback
            logger.error(
                f"Recording stopped error traceback: {traceback.format_exc()}")

    def _on_recording_error(self, error: str):
        """Handle recording error with comprehensive error handling"""
        try:
            log_thread_info(f"Recording error: {error}")

            # Log the error
            logger.error(f"Recording error: {error}")

            # Update UI state with error handling
            try:
                self.update_voice_status("Recording Error")
                self.voice_button.setText("Start Recording")
                self.voice_button.setEnabled(True)
                logger.debug("Recording error - UI updated")
            except Exception as e:
                logger.error(f"Error updating UI for recording error: {e}")

        except Exception as e:
            logger.error(f"Error in _on_recording_error: {e}")
            import traceback
            logger.error(
                f"Recording error handler traceback: {traceback.format_exc()}")

    def _on_audio_level_changed(self, level: float):
        """Handle audio level changes with comprehensive error handling"""
        try:
            # Update audio level display with error handling
            try:
                if hasattr(self, 'audio_level_label'):
                    self.audio_level_label.setText(f"Level: {level:.2f}")
            except Exception as e:
                logger.error(f"Error updating audio level display: {e}")

        except Exception as e:
            logger.error(f"Error in _on_audio_level_changed: {e}")

    def _should_check_for_interruption(self, audio_level: float) -> bool:
        """Check if we should monitor for user interruption"""
        # Only check for interruption if:
        # 1. We're in voice mode
        # 2. TTS is playing
        # 3. Audio level is above threshold
        # 4. We haven't already triggered an interruption recently
        if not self.voice_mode or not self.is_tts_playing():
            return False
            
        # Check if audio level is above interruption threshold
        interruption_threshold = self.get_interruption_threshold()
        if audio_level < interruption_threshold:
            return False
            
        # Prevent multiple interruptions within a short time
        current_time = time.time()
        if hasattr(self, '_last_interruption_time'):
            time_since_last = current_time - self._last_interruption_time
            if time_since_last < 2.0:  # Minimum 2 seconds between interruptions
                return False
                
        return True

    def _handle_potential_interruption(self, audio_level: float):
        """Handle potential user interruption during TTS playback"""
        try:
            current_time = time.time()
            
            # Initialize interruption tracking if needed
            if not hasattr(self, '_interruption_start_time'):
                self._interruption_start_time = None
            if not hasattr(self, '_interruption_audio_levels'):
                self._interruption_audio_levels = []
                
            # Start tracking interruption if this is the first high audio level
            if self._interruption_start_time is None:
                self._interruption_start_time = current_time
                self._interruption_audio_levels = []
                logger.debug(f"[INTERRUPTION] Starting interruption detection - audio_level: {audio_level:.4f}")
                
            # Track audio levels during potential interruption
            self._interruption_audio_levels.append(audio_level)
            
            # Check if we have enough sustained audio to confirm interruption
            interruption_duration = current_time - self._interruption_start_time
            avg_audio_level = sum(self._interruption_audio_levels) / len(self._interruption_audio_levels)
            
            # Confirm interruption if we have sustained high audio for at least 0.5 seconds
            if interruption_duration >= 0.5 and avg_audio_level > self.get_interruption_threshold():
                self._confirm_interruption()
                
        except Exception as e:
            logger.error(f"Error in _handle_potential_interruption: {e}")

    def _confirm_interruption(self):
        """Confirm and handle user interruption"""
        try:
            logger.info("[INTERRUPTION] User interruption confirmed - stopping TTS and restarting voice input")
            
            # Stop TTS playback
            if self.voice_service:
                self.voice_service.stop_tts()
                
            # Emit interruption signal for parent to handle
            self.user_interrupted.emit()
            
            # Update UI to show interruption
            self.audio_level_label.setText("🎤 Interrupted - Listening...")
            self.audio_level_label.setToolTip("User interrupted AI response - ready for new input")
            
            # In continuous mode, restart voice input after a short delay
            if self.voice_mode:
                QTimer.singleShot(1000, self._restart_voice_input_after_interruption)
                
            # Reset interruption tracking
            self._interruption_start_time = None
            self._interruption_audio_levels = []
            self._last_interruption_time = time.time()
            
        except Exception as e:
            logger.error(f"Error in _confirm_interruption: {e}")

    def _restart_voice_input_after_interruption(self):
        """Restart voice input after user interruption"""
        if not self.voice_mode:
            return

        try:
            logger.debug("Restarting voice input after user interruption")
            voice_service = self.get_voice_service()
            if voice_service:
                voice_service.start_voice_input()
                self.audio_level_label.setText("🎤 Continuous Recording...")
                logger.debug("Voice input restarted after interruption")
        except Exception as e:
            logger.error(
                f"Failed to restart voice input after interruption: {e}")

    def _on_eq_bars_changed(self, bars: list):
        """Handle EQ bars changes with comprehensive error handling"""
        try:
            # Update EQ visualizer with error handling
            try:
                if hasattr(self, 'eq_visualizer') and self.eq_visualizer:
                    self.eq_visualizer.update_bars(bars)
            except Exception as e:
                logger.error(f"Error updating EQ visualizer: {e}")

        except Exception as e:
            logger.error(f"Error in _on_eq_bars_changed: {e}")

    def _on_voice_status_changed(self, status: str):
        """Handle voice status changes with comprehensive error handling"""
        try:
            log_thread_info(f"Voice status changed: {status}")

            # Update status display with error handling
            try:
                self.update_voice_status(status)
            except Exception as e:
                logger.error(f"Error updating voice status: {e}")

        except Exception as e:
            logger.error(f"Error in _on_voice_status_changed: {e}")
            import traceback
            logger.error(
                f"Voice status changed error traceback: {traceback.format_exc()}")

    def update_voice_status(self, status: str):
        """Update voice status with comprehensive error handling"""
        try:
            log_thread_info(f"Updating voice status: {status}")

            # Update status label with error handling
            try:
                if hasattr(self, 'status_label'):
                    self.status_label.setText(f"Status: {status}")
                    logger.debug(f"Voice status updated to: {status}")
            except Exception as e:
                logger.error(f"Error updating status label: {e}")

        except Exception as e:
            logger.error(f"Error in update_voice_status: {e}")
            import traceback
            logger.error(
                f"Update voice status error traceback: {traceback.format_exc()}")

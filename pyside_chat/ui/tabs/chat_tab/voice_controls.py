"""
Voice Controls Component - Voice mode, TTS, STT, and audio level handling
"""

import time
import logging
import traceback
from typing import Dict, Optional
from PySide6.QtCore import QObject, Signal, Qt, QTimer, QMutex, QMutexLocker
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox

from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


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

    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager

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

        # Voice service manager (singleton)
        self.voice_service_manager = None
        self.voice_service = None
        self.voice_service_initialized = False

        # Callbacks for when service becomes ready
        self._ready_callbacks = []

        # Add a timer to periodically check button state
        self._ui_refresh_timer = QTimer()
        self._ui_refresh_timer.timeout.connect(self._periodic_ui_refresh)
        self._ui_refresh_timer.start(5000)  # Check every 5 seconds

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

        # Initialize voice service manager
        self._initialize_voice_service_manager()

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

    def _initialize_voice_service_manager(self):
        """Initialize the voice service manager"""
        try:
            # Immediately emit initializing status
            self.voice_status_changed.emit("Initializing")
            logger.info(
    "Starting voice service manager initialization",
     print_to_terminal=True)

            from pyside_chat.features.voice.voice_service_manager import get_voice_service_manager
            self.voice_service_manager = get_voice_service_manager()

            # Connect manager signals
            self.voice_service_manager.voice_service_ready.connect(
                self._on_voice_service_ready)
            self.voice_service_manager.voice_service_error.connect(
                self._on_voice_service_error)
            self.voice_service_manager.voice_service_initializing.connect(
                self._on_voice_service_initializing)

            # Apply initial settings to manager
            self.voice_service_manager.update_settings(self.voice_settings)

            # Trigger voice service initialization by calling get_voice_service()
            # This will start the initialization process if not already
            # initialized
            logger.info(
    "Triggering voice service initialization",
     print_to_terminal=True)
            voice_service = self.voice_service_manager.get_voice_service()

            # Emit initial status based on current state
            if self.voice_service_manager.is_ready():
                logger.info("Voice service is ready", print_to_terminal=True)
                self.voice_status_changed.emit("Ready")
                # Only update button state if UI components are ready
                if hasattr(
    self,
     'voice_button') and self.voice_button is not None:
                    self._update_voice_button_state(True, "Ready")
                    logger.info("Voice button enabled", print_to_terminal=True)
                if voice_service:
                    self.voice_service = voice_service
                    self.voice_service_initialized = True
                    self._setup_voice_connections()
            elif self.voice_service_manager.is_initializing():
                logger.info(
    "Voice service is initializing",
     print_to_terminal=True)
                self.voice_status_changed.emit("Initializing")
                # Only update button state if UI components are ready
                if hasattr(
    self,
     'voice_button') and self.voice_button is not None:
                    self._update_voice_button_state(False, "Initializing")
            else:
                logger.info(
    "Voice service is uninitialized",
     print_to_terminal=True)
                self.voice_status_changed.emit("Uninitialized")
                # Only update button state if UI components are ready
                if hasattr(
    self,
     'voice_button') and self.voice_button is not None:
                    self._update_voice_button_state(False, "Uninitialized")

            logger.info(
    "Voice service manager initialized",
     print_to_terminal=True)

        except Exception as e:
            logger.error(
    f"Failed to initialize voice service manager: {e}",
     print_to_terminal=True)
            self.voice_service_manager = None
            self.voice_status_changed.emit(
                "Error: Failed to initialize manager")

    def force_ui_refresh(self):
        """Force UI refresh to update button state based on current voice service status"""
        logger.info(
    "Forcing UI refresh for voice controls",
     print_to_terminal=True)

        if hasattr(self, 'voice_button') and self.voice_button is not None:
            if self.voice_service_manager and self.voice_service_manager.is_ready():
                logger.info(
    "Voice service is ready, enabling button",
     print_to_terminal=True)
                self._update_voice_button_state(True, "Ready")
                self.voice_status_changed.emit("Ready")
            elif self.voice_service_manager and self.voice_service_manager.is_initializing():
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
    "Voice service ready signal received",
     print_to_terminal=True)
        self.voice_status_changed.emit("Ready")

        # Enable the voice button when service is ready
        logger.info(
    "Calling _update_voice_button_state(True, 'Ready')",
     print_to_terminal=True)
        self._update_voice_button_state(True, "Ready")

        if self.voice_service_manager:
            self.voice_service = self.voice_service_manager.get_voice_service()
            if self.voice_service:
                self.voice_service_initialized = True
                self._setup_voice_connections()
                logger.info(
    "Voice service ready and connections established",
     print_to_terminal=True)
            else:
                logger.error(
    "Voice service manager returned None service",
     print_to_terminal=True)

    def _on_direct_voice_service_ready(self):
        """Handle direct voice service ready signal (from VoiceService)"""
        logger.info(
    "Voice service ready signal received",
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
        # Only refresh if voice controls are initialized and voice button
        # exists
        if (hasattr(self, 'voice_button') and
            self.voice_button is not None and
            self.voice_service_manager):

            # Only update if status changed
            current_status = "Ready" if self.voice_service_manager.is_ready() else "Initializing"
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
        logger.error(f"Voice service error: {error}", print_to_terminal=True)
        self.voice_input_error.emit(
            f"Voice service initialization failed: {error}")
        self.voice_status_changed.emit(f"Error: {error}")

        # Keep button disabled on error
        self._update_voice_button_state(False, "Error")

    def _on_voice_service_initializing(self):
        """Handle voice service initializing signal"""
        logger.info(
    "Voice service initialization started",
     print_to_terminal=True)
        self.voice_status_changed.emit("Initializing")

        # Keep button disabled during initialization
        self._update_voice_button_state(False, "Initializing")

    def get_voice_service(self):
        """Get voice service with lazy loading"""
        if not self.voice_service_manager:
            self._initialize_voice_service_manager()

        if self.voice_service_manager:
            # Get service from manager (will initialize if needed)
            voice_service = self.voice_service_manager.get_voice_service()

            # Update our local reference if it changed and service is available
            if voice_service and voice_service != self.voice_service:
                print(f"[DEBUG] Voice service type: {type(voice_service).__name__}")
                logger.debug(f"Voice service type: {type(voice_service).__name__}", print_to_terminal=True)
                
                self.voice_service = voice_service
                self.voice_service_initialized = True
                self._setup_voice_connections()

            return self.voice_service

        return None

    def _setup_voice_connections(self):
        """Setup connections for voice service"""
        if not self.voice_service:
            logger.warning(
                "Cannot setup voice connections: voice service is None")
            return

        print(
            f"[DEBUG] Setting up voice connections for service type: {type(self.voice_service).__name__}")
        logger.debug(
    f"Setting up voice connections for service type: {type(self.voice_service).__name__}",
     print_to_terminal=True)

        # Check if voice service is properly initialized
        if not hasattr(self.voice_service, 'voice_input_received'):
            print(f"[DEBUG] Voice service does not have voice_input_received signal")
            logger.warning(
    "Voice service not fully initialized, skipping connections",
     print_to_terminal=True)
            return

        # Check if this is a voice service wrapper - if so, don't connect directly
        # as the wrapper already forwards signals
        service_type = type(self.voice_service).__name__
        if 'Wrapper' in service_type or 'ProcessManager' in service_type:
            print(f"[DEBUG] Voice service is a wrapper ({service_type}), skipping direct connections to avoid duplicates")
            logger.info(
    f"Voice service is a wrapper ({service_type}), skipping direct connections to avoid signal duplication",
     print_to_terminal=True)
            return

        try:
            logger.info(
    "Setting up voice service UI connections...",
     print_to_terminal=True)
            # Wait a moment for signals to be properly initialized
            import time
            time.sleep(0.1)

            # Disconnect any existing connections to avoid duplicates
            # Only disconnect if the signal exists and is not None
            signal_mappings = [
                ('voice_input_received', getattr(
                    self.voice_service, 'voice_input_received', None)),
                ('voice_input_error', getattr(
                    self.voice_service, 'voice_input_error', None)),
                ('tts_started', getattr(self.voice_service, 'tts_started', None)),
                ('tts_finished', getattr(self.voice_service, 'tts_finished', None)),
                ('tts_error', getattr(self.voice_service, 'tts_error', None)),
                ('recording_started', getattr(
                    self.voice_service, 'recording_started', None)),
                ('recording_stopped', getattr(
                    self.voice_service, 'recording_stopped', None)),
                ('recording_error', getattr(
                    self.voice_service, 'recording_error', None)),
                ('voice_processing_started', getattr(
                    self.voice_service, 'voice_processing_started', None)),
                ('voice_processing_finished', getattr(
                    self.voice_service, 'voice_processing_finished', None)),
                ('audio_level_changed', getattr(
                    self.voice_service, 'audio_level_changed', None)),
                ('user_interrupted', getattr(
                    self.voice_service, 'user_interrupted', None)),
                ('request_cancelled', getattr(
                    self.voice_service, 'request_cancelled', None)),
                ('voice_service_ready', getattr(
                    self.voice_service, 'voice_service_ready', None))
            ]

            for signal_name, signal in signal_mappings:
                if signal is not None and hasattr(signal, 'disconnect'):
                    try:
                        signal.disconnect()
                        logger.debug(
                            f"Disconnected existing {signal_name} signal")
                    except Exception as e:
                        logger.debug(
                            f"Could not disconnect {signal_name} signal: {e}")
                else:
                    logger.debug(
                        f"Signal {signal_name} is None or has no disconnect method, skipping disconnect")

            # Connect voice service signals (only if they exist)
            connections_made = 0
            if hasattr(
    self.voice_service,
     'voice_input_received') and self.voice_service.voice_input_received is not None:
                print(f"[DEBUG] Connecting voice_input_received signal")
                logger.debug(
    "Connecting voice_input_received signal",
     print_to_terminal=True)
                self.voice_service.voice_input_received.connect(
                    self.on_voice_input_received)
                connections_made += 1
            else:
                print(f"[DEBUG] voice_input_received signal not available")
                logger.warning(
    "voice_input_received signal not available",
     print_to_terminal=True)

            if hasattr(
    self.voice_service,
     'voice_input_error') and self.voice_service.voice_input_error is not None:
                self.voice_service.voice_input_error.connect(
                    self.on_voice_input_error)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'tts_started') and self.voice_service.tts_started is not None:
                self.voice_service.tts_started.connect(self.on_tts_started)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'tts_finished') and self.voice_service.tts_finished is not None:
                self.voice_service.tts_finished.connect(self.on_tts_finished)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'tts_error') and self.voice_service.tts_error is not None:
                self.voice_service.tts_error.connect(self.on_tts_error)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'recording_started') and self.voice_service.recording_started is not None:
                self.voice_service.recording_started.connect(
                    self.on_recording_started)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'recording_stopped') and self.voice_service.recording_stopped is not None:
                self.voice_service.recording_stopped.connect(
                    self.on_recording_stopped)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'recording_error') and self.voice_service.recording_error is not None:
                self.voice_service.recording_error.connect(
                    self.on_recording_error)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'voice_processing_started') and self.voice_service.voice_processing_started is not None:
                self.voice_service.voice_processing_started.connect(
                    self.on_voice_processing_started)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'voice_processing_finished') and self.voice_service.voice_processing_finished is not None:
                self.voice_service.voice_processing_finished.connect(
                    self.on_voice_processing_finished)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'audio_level_changed') and self.voice_service.audio_level_changed is not None:
                self.voice_service.audio_level_changed.connect(
                    self.on_audio_level_changed)
                connections_made += 1

            # Connect new interruption signals
            if hasattr(
    self.voice_service,
     'user_interrupted') and self.voice_service.user_interrupted is not None:
                self.voice_service.user_interrupted.connect(
                    self.on_user_interrupted)
                connections_made += 1
            if hasattr(
    self.voice_service,
     'request_cancelled') and self.voice_service.request_cancelled is not None:
                self.voice_service.request_cancelled.connect(
                    self.on_request_cancelled)
                connections_made += 1

            # Connect voice service ready signal
            if hasattr(
    self.voice_service,
     'voice_service_ready') and self.voice_service.voice_service_ready is not None:
                self.voice_service.voice_service_ready.connect(
                    self._on_direct_voice_service_ready)
                connections_made += 1

            print(
                f"[DEBUG] Voice service UI connections established: {connections_made} connections made")
            logger.info(
    f"Voice service UI connections established successfully: {connections_made} connections made",
     print_to_terminal=True)

        except Exception as e:
            print(f"[DEBUG] Error setting up voice connections: {e}")
            logger.error(
    f"Error setting up voice connections: {e}",
     print_to_terminal=True)
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")

    def _is_voice_service_ready(self) -> bool:
        """Check if voice service is ready to use"""
        try:
            voice_service = self.get_voice_service()
            if not voice_service:
                    return False

            # Check if voice service is properly initialized
            if hasattr(voice_service, 'is_voice_available'):
                ready = voice_service.is_voice_available()
                logger.debug(
    f"Voice service ready check via is_voice_available: {ready}",
     print_to_terminal=True)
                return ready

            # Fallback check for basic capabilities
            ready = self._validate_voice_service_capabilities(voice_service)
            logger.debug(
    f"Voice service ready check via capabilities validation: {ready}",
     print_to_terminal=True)
            return ready
        except Exception as e:
            logger.error(f"Error checking voice service readiness: {e}")
            return False

    def _validate_voice_service_capabilities(self, voice_service):
        """Validate that the voice service has the required methods"""
        required_methods = [
            'start_voice_input',
            'stop_voice_input',
            'set_continuous_voice_mode',
            'is_recording',
            'is_playing_tts'
        ]

        missing_methods = []
        for method in required_methods:
            if not hasattr(voice_service, method):
                missing_methods.append(method)

        if missing_methods:
            logger.warning(
                f"Voice service missing required methods: {missing_methods}")
            return False

        return True

    def reset_voice_service(self):
        """Force reset the voice service to clear stuck states"""
        logger.debug("Force resetting voice service")
        
        try:
            voice_service = self.get_voice_service()
            if voice_service:
                # Clear the request queue
                if hasattr(voice_service, 'clear_request_queue'):
                    voice_service.clear_request_queue()
                
                # Disable continuous mode
                if hasattr(voice_service, 'set_continuous_voice_mode'):
                    voice_service.set_continuous_voice_mode(False)
                
                # Stop all operations
                if hasattr(voice_service, 'stop_voice_input'):
                    voice_service.stop_voice_input()
                if hasattr(voice_service, 'stop_tts'):
                    voice_service.stop_tts()
                
                logger.debug("Voice service reset successfully")
                return True
            else:
                logger.warning("Voice service not available for reset")
                return False
                
        except Exception as e:
            logger.error(f"Error resetting voice service: {e}")
            return False
    
    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        logger.debug("Toggle voice mode called")

        try:
            if not self.voice_mode:
                # Start voice mode
                    logger.debug("Starting voice mode")
                    self.voice_mode = True

                    # Check if voice service is initialized
                    voice_service = self.get_voice_service()
                    logger.debug(
    f"Voice service obtained: {voice_service is not None}",
     print_to_terminal=True)

                    if not voice_service or not self._is_voice_service_ready():
                        # Voice service not ready, disable button and show
                        # initializing
                        logger.debug(
    "Voice service not ready, disabling button",
     print_to_terminal=True)
                        self._update_voice_button_state(False, "Initializing")
                        self.voice_status_changed.emit("Initializing")
                        return

                    # Voice service is ready, enable button and start voice
                    # mode
                    logger.debug(
    "Voice service is ready, starting voice mode",
     print_to_terminal=True)
                    self._update_voice_button_state(True, "Ready")
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

                # Start continuous voice mode
                    self._start_continuous_voice_mode()
                    logger.debug("Voice mode started successfully")
            else:
                # Stop voice mode
                logger.debug("Stopping voice mode")
                self.voice_mode = False
                self._reset_voice_button()
                
                # Stop any ongoing voice processes and clear queue
                try:
                    voice_service = self.get_voice_service()
                    if voice_service:
                        # Clear the entire request queue and reset state
                        if hasattr(voice_service, 'clear_request_queue'):
                            voice_service.clear_request_queue()
                            logger.debug("Request queue cleared successfully")
                        
                        # Also disable continuous voice mode as backup
                        if hasattr(voice_service, 'set_continuous_voice_mode'):
                            voice_service.set_continuous_voice_mode(False)
                        
                        # Stop any remaining operations as backup
                        if hasattr(voice_service, 'is_recording') and voice_service.is_recording:
                            voice_service.stop_voice_input()
                        if hasattr(voice_service, 'is_playing_tts') and voice_service.is_playing_tts:
                            voice_service.stop_tts()
                except Exception as e:
                    logger.error(f"Error stopping voice processes: {e}")
                
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
            logger.debug("Cannot start continuous voice mode: voice_mode is False")
            return
        
        logger.debug("Starting continuous voice mode cycle", print_to_terminal=True)
        
        # Enable continuous voice mode in the voice service
        try:
            voice_service = self.get_voice_service()
            if voice_service:
                logger.debug("Voice service available for continuous mode", print_to_terminal=True)
                
                # Check if voice service is actually ready
                if hasattr(voice_service, 'is_voice_available'):
                    if not voice_service.is_voice_available():
                        logger.error("Voice service not ready yet, cannot start voice input", print_to_terminal=True)
                        self.voice_mode = False
                        self._reset_voice_button()
                        return
                
                # Validate capabilities
                if not self._validate_voice_service_capabilities(voice_service):
                    logger.error("Voice service missing required capabilities for continuous mode", print_to_terminal=True)
                    self.voice_mode = False
                    self._reset_voice_button()
                    return
                
                # Set continuous mode
                logger.debug("Setting continuous voice mode", print_to_terminal=True)
                voice_service.set_continuous_voice_mode(True)
                logger.debug("Continuous voice mode enabled")
                
                # Start voice input
                logger.debug("Starting voice input...", print_to_terminal=True)
                voice_service.start_voice_input()
                logger.debug("Voice input started successfully", print_to_terminal=True)
            else:
                logger.error("Voice service not available for continuous mode", print_to_terminal=True)
                self.voice_mode = False
                self._reset_voice_button()
        except Exception as e:
            logger.error(f"Failed to start voice input: {e}", print_to_terminal=True)
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Reset voice mode on error
            self.voice_mode = False
            self._reset_voice_button()
    
    def _handle_voice_input_safe(self, text: str):
        """Handle voice input safely in the main thread"""
        try:
            print(f"[DEBUG] Voice controls received voice input: '{text}'")
            logger.debug(f"Voice controls received voice input: '{text}'", print_to_terminal=True)
            
            if not self.voice_mode:
                print(f"[DEBUG] Voice mode is False, ignoring voice input")
                logger.debug("Voice mode is False, ignoring voice input", print_to_terminal=True)
                return
            
            logger.debug(f"Voice input received in continuous mode: {text}")
            
            # In non-interruptive mode, we don't stop voice input immediately
            # The voice service will handle stopping during processing and restarting during TTS
            logger.debug("[VOICE DEBUG] Non-interruptive mode: voice input will be managed by voice service")
            
            # Forward to parent for processing
            print(f"[DEBUG] Emitting voice_input_received signal with text: '{text}'")
            logger.debug(f"Emitting voice_input_received signal with text: '{text}'", print_to_terminal=True)
            self.voice_input_received.emit(text)
            
            # Voice service will handle the flow:
            # 1. Stop voice input during processing
            # 2. Restart voice input during TTS (for non-interruptive mode)
            # 3. Restart voice input after TTS completion
            
        except Exception as e:
            print(f"[DEBUG] Error in _handle_voice_input_safe: {e}")
            logger.error(f"[VOICE ERROR] Error handling voice input: {e}", print_to_terminal=True)
            logger.error(f"[VOICE ERROR] Traceback: {traceback.format_exc()}")
            # Try to emit error signal
            try:
                self.voice_input_error.emit(f"Voice input error: {str(e)}")
            except:
                pass
    
    def _handle_tts_finished_continuous(self):
        """Handle TTS finished in continuous voice mode"""
        if not self.voice_mode:
            return
        
        logger.debug("TTS finished in continuous voice mode")
        
        # In non-interruptive mode, voice service handles restarting voice input
        # No need to manually restart here as the voice service will do it
        logger.debug("[VOICE DEBUG] Non-interruptive mode: voice service will restart voice input")
    
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
        """Handle voice input received"""
        logger.debug(f"Voice input received: {text}")
        
        # Use QTimer.singleShot to ensure this runs in the main thread
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, lambda: self._handle_voice_input_safe(text))
    
    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        logger.error(f"Voice input error: {error}")
        
        # Handle service error
        self._handle_service_error(error)
        
        # Use QTimer.singleShot to ensure UI updates happen in the main thread
        QTimer.singleShot(0, lambda: self._handle_voice_input_error_safe(error))
    
    def _handle_voice_input_error_safe(self, error: str):
        """Handle voice input error safely in the main thread"""
        try:
            logger.debug(f"Voice input error received: {error}")
            
            # Check for queue full errors and auto-reset
            if "queue full" in error.lower() or "request queue full" in error.lower():
                logger.warning("Queue full error detected, attempting auto-reset")
                if self.reset_voice_service():
                    logger.info("Voice service auto-reset successful")
                    # Try to restart voice input if voice mode is still active
                    if self.voice_mode:
                        QTimer.singleShot(1000, self._start_continuous_voice_mode)
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
    
    def on_tts_started(self):
        """Handle TTS started"""
        logger.debug("TTS started")
        self.voice_status_changed.emit("Speaking")
        self.tts_started.emit()
    
    def on_tts_finished(self):
        """Handle TTS finished"""
        logger.debug("TTS finished in voice controls")
        self.voice_status_changed.emit("Idle")
        
        # In continuous voice mode, restart voice input
        if self.voice_mode:
            self._handle_tts_finished_continuous()
        
        # Forward the signal
        self.tts_finished.emit()
    
    def on_tts_error(self, error: str):
        """Handle TTS error"""
        logger.error(f"TTS error: {error}")
        self.voice_status_changed.emit(f"TTS Error: {error}")
        
        # Handle service error
        self._handle_service_error(error)
        
        # Use QTimer.singleShot to ensure UI updates happen in the main thread
        QTimer.singleShot(0, lambda: self._handle_tts_error_safe(error))
    
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
            self.audio_level_label.setToolTip("Continuous voice mode - recording will restart automatically")
        else:
            self.audio_level_label.setText("🎤 Recording...")
            silence_duration = voice_service.get_silence_duration() if voice_service else 3.0
            self.audio_level_label.setToolTip(f"Silence timeout: {silence_duration:.1f}s")
        
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
            self.voice_button.setToolTip("Continuous voice mode active - click to stop")
        
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
        """Handle audio level changes"""
        logger.debug(f"[EQ DEBUG] on_audio_level_changed called - audio_level: {audio_level:.4f}")
        
        # Emit signal for parent to handle
        self.audio_level_changed.emit(audio_level)
        
        # Use QTimer.singleShot to ensure UI updates happen in the main thread
        QTimer.singleShot(0, lambda: self._update_audio_level_ui_safe(audio_level))
    
    def _update_audio_level_ui_safe(self, audio_level: float):
        """Update audio level UI safely in the main thread"""
        try:
            voice_service = self.get_voice_service()
            
            # Check if recording service is available
            if not voice_service or not hasattr(voice_service, 'recording_service') or not voice_service.recording_service:
                # Fallback for process manager mode
                self.audio_level_label.setText("🎤 Recording...")
                self.audio_level_meter.setValue(int(audio_level * 100))
                logger.debug(f"[EQ DEBUG] Using fallback audio level meter update")
                return
            
            # Convert to dB
            db_level = voice_service.recording_service.audio_level_to_db(audio_level)
            
            # Update meter (0-100 range)
            meter_value = min(100, max(0, int((db_level + 60) * 1.67)))  # Convert -60dB to 0dB range to 0-100
            self.audio_level_meter.setValue(meter_value)
            
            # Update label with dB level
            if audio_level > voice_service.get_silence_threshold():
                if voice_service.is_continuous_voice_mode():
                    self.audio_level_label.setText(f"🎤 Recording... {db_level:.1f} dB")
                else:
                    self.audio_level_label.setText(f"🎤 Recording... {db_level:.1f} dB")
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
                    self.audio_level_label.setText(f"🎤 Listening... {db_level:.1f} dB")
                else:
                    self.audio_level_label.setText(f"🎤 Listening... {db_level:.1f} dB")
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
            logger.error(f"[EQ DEBUG] Audio level error traceback: {traceback.format_exc()}")
    
    def speak_ai_response(self, text: str):
        """Speak AI response using TTS"""
        voice_service = self.get_voice_service()
        if not voice_service:
            logger.error("Voice service not available for TTS")
            return
            
        try:
            # Check if we can handle new TTS requests
            if hasattr(voice_service, 'can_handle_new_request') and not voice_service.can_handle_new_request():
                logger.warning("Cannot handle new TTS request - queue full")
                return
                
            voice_service.speak_text(text)
            logger.debug(f"TTS request sent for text: {text[:50]}...")
        except Exception as e:
            logger.error(f"Failed to speak AI response: {e}")
    
    def update_voice_settings(self, settings: dict):
        """Update voice settings"""
        self.voice_settings.update(settings)
        
        if self.voice_service_manager:
            self.voice_service_manager.update_settings(settings)
            logger.debug(f"Updated voice service manager settings: {settings}")
        else:
            logger.warning("Voice service manager not available for settings update")
    
    def get_voice_settings(self) -> dict:
        """Get current voice settings"""
        if self.voice_service_manager:
            return self.voice_service_manager.get_settings()
        return self.voice_settings.copy()
    
    def is_voice_service_ready(self) -> bool:
        """Check if voice service is ready"""
        if self.voice_service_manager:
            return self.voice_service_manager.is_ready()
        return False

    def is_voice_service_initializing(self) -> bool:
        """Check if voice service is initializing"""
        if self.voice_service_manager:
            return self.voice_service_manager.is_initializing()
        return False

    def get_voice_service_error(self) -> str:
        """Get the last voice service error"""
        if self.voice_service_manager:
            return self.voice_service_manager.get_last_error() or "No error"
        return "Voice service manager not available"

    def force_reinitialize_voice_service(self):
        """Force reinitialization of the voice service"""
        if self.voice_service_manager:
            self.voice_service_manager.force_reinitialize()
            logger.info("Forced voice service reinitialization")
        else:
            logger.warning("Voice service manager not available for reinitialization")
    
    def is_voice_mode_active(self) -> bool:
        """Check if voice mode is active"""
        return self.voice_mode
    
    def is_tts_playing(self) -> bool:
        """Check if TTS is currently playing"""
        voice_service = self.get_voice_service()
        if not voice_service:
            return False
        try:
            return voice_service.is_playing_tts
        except Exception as e:
            logger.error(f"Failed to check TTS playing status: {e}")
            return False
    
    def can_handle_interruption(self) -> bool:
        """Check if the system can handle user interruptions"""
        voice_service = self.get_voice_service()
        if not voice_service:
            return False
        try:
            return voice_service.voice_settings.get("allow_interruptions", True)
        except Exception as e:
            logger.error(f"Failed to check interruption capability: {e}")
            return False

    def get_interruption_threshold(self) -> float:
        """Get the audio level threshold for interruption detection"""
        voice_service = self.get_voice_service()
        if not voice_service:
            return 0.5  # Default threshold
        try:
            return voice_service.voice_settings.get("interruption_threshold", 0.5)
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
        self.audio_level_label.setToolTip("User interrupted AI response - ready for new input")
        
        # In continuous mode, restart voice input after a short delay
        if self.voice_mode:
            from PySide6.QtCore import QTimer
            QTimer.singleShot(500, self._restart_voice_input_after_interruption)

    def on_request_cancelled(self):
        """Handle request cancellation"""
        logger.info("Request cancelled in voice controls")
        
        # Update UI to show cancellation
        self.audio_level_label.setText("🎤 Cancelled - Ready")
        self.audio_level_label.setToolTip("Previous request was cancelled")
        
        # In continuous mode, restart voice input after a short delay
        if self.voice_mode:
            from PySide6.QtCore import QTimer
            QTimer.singleShot(1000, self._restart_voice_input_after_cancellation)

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
            logger.error(f"Failed to restart voice input after interruption: {e}")

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
            logger.error(f"Failed to restart voice input after cancellation: {e}") 
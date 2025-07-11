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
        
        # Voice service will be lazy loaded when needed
        self.voice_service = None
        self.voice_service_initialized = False
        
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
        
        # Update voice service with initial settings (only if service is available)
        voice_service = self.get_voice_service()
        if voice_service:
            try:
                voice_service.update_settings(self.voice_settings)
            except Exception as e:
                logger.error(f"Failed to update voice service settings: {e}")
        
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
        """)
        
        # Voice settings button
        self.voice_settings_button = QPushButton("⚙️")
        self.voice_settings_button.setToolTip("Voice Settings")
        self.voice_settings_button.setFixedSize(32, 32)
        self.voice_settings_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        # Audio level widget
        self.audio_level_widget = QWidget()
        audio_level_layout = QVBoxLayout(self.audio_level_widget)
        audio_level_layout.setContentsMargins(0, 0, 0, 0)
        
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
                background-color: #00ff00;
                border-radius: 2px;
            }
        """)
        
        audio_level_layout.addWidget(self.audio_level_label)
        audio_level_layout.addWidget(self.audio_level_meter)
        
        # Initially hide voice-related widgets
        self.voice_button.hide()
        self.voice_settings_button.hide()
        self.audio_level_widget.hide()
        
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
        """Reinitialize voice service"""
        try:
            # This would need to be implemented based on how voice service is initialized
            logger.info("Voice service reinitialization not implemented yet")
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
        logger.error(f"Voice service error ({self._error_count}/{self._max_errors}): {error}")
        
        if self._error_count >= self._max_errors:
            logger.error("Too many voice service errors, disabling voice features")
            self._disable_voice_features()
        else:
            # Reset error count after delay
            self._error_reset_timer.start(5000)  # 5 second delay
    
    def setup_connections(self):
        """Setup signal connections"""
        # Voice service connections will be established when voice service is lazy loaded
        
        # Connect voice button
        self.voice_button.clicked.connect(self.toggle_voice_mode)
        
    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        voice_service = self.get_voice_service()
        if not voice_service:
            logger.error("Voice service not available")
            return
        
        if not self.voice_mode:
            # Start voice mode
            self.voice_mode = True
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
            
            logger.debug("Voice mode started")
        else:
            # Stop voice mode
            self.voice_mode = False
            self._reset_voice_button()
            
            # Stop any ongoing voice processes
            try:
                voice_service = self.get_voice_service()
                # Disable continuous voice mode first
                voice_service.set_continuous_voice_mode(False)
                
                if voice_service.is_recording:
                    voice_service.stop_voice_input()
                if voice_service.is_playing_tts:
                    voice_service.stop_tts()
            except Exception as e:
                logger.error(f"Error stopping voice processes: {e}")
            
            logger.debug("Voice mode stopped")
    
    def _start_continuous_voice_mode(self):
        """Start continuous voice mode cycle"""
        if not self.voice_mode:
            return
        
        logger.debug("Starting continuous voice mode cycle")
        
        # Enable continuous voice mode in the voice service
        try:
            voice_service = self.get_voice_service()
            voice_service.set_continuous_voice_mode(True)
            voice_service.start_voice_input()
        except Exception as e:
            logger.error(f"Failed to start voice input: {e}")
            # Reset voice mode on error
            self.voice_mode = False
            self._reset_voice_button()
    
    def _handle_voice_input_safe(self, text: str):
        """Handle voice input safely in the main thread"""
        try:
            if not self.voice_mode:
                return
            
            logger.debug(f"Voice input received in continuous mode: {text}")
            
            # Stop voice input to prevent feedback loop during AI response
            logger.debug("[VOICE DEBUG] Stopping voice input to prevent feedback loop")
            try:
                voice_service = self.get_voice_service()
                if voice_service and hasattr(voice_service, 'stop_voice_input'):
                    voice_service.stop_voice_input()
                    logger.debug("[VOICE DEBUG] Voice input stopped successfully")
            except Exception as e:
                logger.error(f"[VOICE ERROR] Failed to stop voice input: {e}")
            
            # Forward to parent for processing
            self.voice_input_received.emit(text)
            
            # Voice input will be restarted after TTS finishes
            # This prevents the system from picking up the TTS output
            
        except Exception as e:
            logger.error(f"[VOICE ERROR] Error handling voice input: {e}")
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
        
        logger.debug("TTS finished in continuous voice mode, restarting voice input")
        
        # Restart voice input after TTS finishes to prevent feedback loop
        try:
            voice_service = self.get_voice_service()
            if voice_service and hasattr(voice_service, 'start_voice_input'):
                voice_service.start_voice_input()
                logger.debug("[VOICE DEBUG] Voice input restarted successfully after TTS")
            else:
                logger.warning("[VOICE DEBUG] Voice service not available for restart")
        except Exception as e:
            logger.error(f"[VOICE ERROR] Failed to restart voice input after TTS: {e}")
    
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
        self.voice_input_error.emit(error)
        
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
    
    def on_tts_started(self):
        """Handle TTS started"""
        logger.debug("TTS started")
        self.tts_started.emit()
    
    def on_tts_finished(self):
        """Handle TTS finished"""
        logger.debug("TTS finished in voice controls")
        
        # In continuous voice mode, restart voice input
        if self.voice_mode:
            self._handle_tts_finished_continuous()
        
        # Forward the signal
        self.tts_finished.emit()
    
    def on_tts_error(self, error: str):
        """Handle TTS error"""
        logger.error(f"TTS error: {error}")
        
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
            voice_service.speak_text(text)
        except Exception as e:
            logger.error(f"Failed to speak AI response: {e}")
    
    def update_voice_settings(self, settings: dict):
        """Update voice settings"""
        self.voice_settings.update(settings)
        voice_service = self.get_voice_service()
        if voice_service:
            try:
                voice_service.update_settings(settings)
            except Exception as e:
                logger.error(f"Failed to update voice service settings: {e}")
    
    def get_voice_settings(self) -> dict:
        """Get current voice settings"""
        return self.voice_settings.copy()
    
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
    
    def get_voice_service(self):
        """Get voice service with lazy loading"""
        if not self.voice_service_initialized:
            self._initialize_voice_service()
        return self.voice_service
    
    def _initialize_voice_service(self):
        """Initialize voice service only when needed"""
        if self.voice_service_initialized:
            return
            
        try:
            logger.info("Initializing voice service (lazy loading)")
            
            # Try to get voice service from service manager first
            if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'get_service_manager'):
                service_manager = self.parent.parent.get_service_manager()
                if hasattr(service_manager, 'get_voice_service'):
                    self.voice_service = service_manager.get_voice_service()
                    self.voice_service_initialized = True
                    logger.info("Voice service initialized via service manager")
                    return
            
            # Fallback to direct initialization
            try:
                from pyside_chat.features.voice.voice_service_wrapper import VoiceServiceWrapper
                self.voice_service = VoiceServiceWrapper(use_separate_process=True)
                logger.info("Voice service wrapper initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize voice service wrapper: {e}")
                try:
                    # Fallback to direct service
                    from pyside_chat.features.voice.voice_service import VoiceService
                    self.voice_service = VoiceService()
                    logger.info("Voice service initialized with direct service (fallback)")
                except Exception as e2:
                    logger.error(f"Failed to initialize direct voice service: {e2}")
                    self.voice_service = None
                    return
            
            self.voice_service_initialized = True
            
            # Setup connections if voice service is available
            if self.voice_service:
                self._setup_voice_connections()
                
        except Exception as e:
            logger.error(f"Error in voice service initialization: {e}")
            self.voice_service = None
            self.voice_service_initialized = False
    
    def _setup_voice_connections(self):
        """Setup connections for voice service"""
        try:
            if self.voice_service:
                # Connect voice service signals
                self.voice_service.voice_input_received.connect(self.on_voice_input_received)
                self.voice_service.voice_input_error.connect(self.on_voice_input_error)
                self.voice_service.tts_started.connect(self.on_tts_started)
                self.voice_service.tts_finished.connect(self.on_tts_finished)
                self.voice_service.tts_error.connect(self.on_tts_error)
                self.voice_service.recording_started.connect(self.on_recording_started)
                self.voice_service.recording_stopped.connect(self.on_recording_stopped)
                self.voice_service.recording_error.connect(self.on_recording_error)
                self.voice_service.voice_processing_started.connect(self.on_voice_processing_started)
                self.voice_service.voice_processing_finished.connect(self.on_voice_processing_finished)
                self.voice_service.audio_level_changed.connect(self.on_audio_level_changed)
                logger.info("Voice service connections established")
        except Exception as e:
            logger.error(f"Error setting up voice connections: {e}")
    
    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'voice_button': self.voice_button,
            'voice_settings_button': self.voice_settings_button,
            'audio_level_widget': self.audio_level_widget
        } 
"""
Voice Controls Component - Voice mode, TTS, STT, and audio level handling
"""

import time
import logging
from typing import Dict, Optional
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar

from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

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
        
        # Initialize voice service
        from pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service_wrapper import VoiceServiceWrapper
        self.voice_service = VoiceServiceWrapper(use_separate_process=True)
        
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
        
        # Update voice service with initial settings
        self.voice_service.update_settings(self.voice_settings)
        
        # State variables
        self.voice_mode = False
        self.recording_start_time = None
        
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
        
    def setup_connections(self):
        """Setup signal connections"""
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
        
        # Connect recording service audio level signal
        if hasattr(self.voice_service, 'recording_service'):
            self.voice_service.recording_service.audio_level_changed.connect(self.on_audio_level_changed)
        
        # Connect voice button
        self.voice_button.clicked.connect(self.toggle_voice_mode)
        
    def toggle_voice_mode(self):
        """Toggle voice mode on/off"""
        logger.debug(f"[EQ DEBUG] toggle_voice_mode called - current voice_mode: {self.voice_mode}")
        
        if not self.voice_mode:
            logger.debug(f"[EQ DEBUG] Starting voice mode")
            # Start voice input with continuous mode enabled
            self.voice_service.set_continuous_voice_mode(True)
            self.voice_service.start_voice_input()
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_mode = True
            self.voice_mode_changed.emit(True)
        else:
            logger.debug(f"[EQ DEBUG] Stopping voice mode")
            # Stop voice input and disable continuous mode
            self.voice_service.set_continuous_voice_mode(False)
            self.voice_service.stop_voice_input()
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.voice_mode_changed.emit(False)
    
    def _reset_voice_button(self):
        """Reset voice button to ready state"""
        self.voice_mode = False
        self.voice_service.set_continuous_voice_mode(False)  # Disable continuous mode
        stt_api = self.voice_settings.get('stt_api', 'Unknown')
        tts_api = self.voice_settings.get('tts_api', 'Unknown')
        self.voice_button.setText("🎤 Start Voice")
        self.voice_button.setToolTip(f"Start voice recording\nSTT: {stt_api}\nTTS: {tts_api}")
        self.voice_button.setEnabled(True)
        self.voice_mode_changed.emit(False)
    
    def on_voice_input_received(self, text: str):
        """Handle voice input converted to text"""
        logger.debug(f"Voice input received: {text}")
        
        # Emit signal for parent to handle
        self.voice_input_received.emit(text)
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.audio_level_widget.setVisible(False)
            self.voice_mode_changed.emit(False)
        else:
            # Keep the button as "Stop Voice" for continuous mode
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_button.setToolTip("Continuous voice mode active - click to stop")
    
    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        logger.error(f"Voice input error: {error}")
        
        # Emit signal for parent to handle
        self.voice_input_error.emit(error)
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
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
        logger.debug("TTS finished")
        self.tts_finished.emit()
    
    def on_tts_error(self, error: str):
        """Handle TTS error"""
        logger.error(f"TTS error: {error}")
        self.tts_error.emit(error)
    
    def on_recording_started(self):
        """Handle recording started"""
        logger.debug("Voice recording started")
        
        # Show audio level meter
        self.audio_level_widget.setVisible(True)
        
        # Show different message for continuous mode
        if self.voice_service.is_continuous_voice_mode():
            self.audio_level_label.setText("🎤 Continuous Recording...")
            self.audio_level_label.setToolTip("Continuous voice mode - recording will restart automatically")
        else:
            self.audio_level_label.setText("🎤 Recording...")
            silence_duration = self.voice_service.get_silence_duration()
            self.audio_level_label.setToolTip(f"Silence timeout: {silence_duration:.1f}s")
        
        self.audio_level_meter.setValue(0)
        
        # Record start time
        self.recording_start_time = time.time()
        
        self.recording_started.emit()
    
    def on_recording_stopped(self):
        """Handle recording stopped"""
        logger.debug("Voice recording stopped")
        
        # Only hide audio level meter if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
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
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
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
        
        # Also handle the existing audio level meter logic
        try:
            # Check if recording service is available
            if not hasattr(self.voice_service, 'recording_service') or not self.voice_service.recording_service:
                # Fallback for process manager mode
                self.audio_level_label.setText("🎤 Recording...")
                self.audio_level_meter.setValue(int(audio_level * 100))
                logger.debug(f"[EQ DEBUG] Using fallback audio level meter update")
                return
            
            # Convert to dB
            db_level = self.voice_service.recording_service.audio_level_to_db(audio_level)
            
            # Update meter (0-100 range)
            meter_value = min(100, max(0, int((db_level + 60) * 1.67)))  # Convert -60dB to 0dB range to 0-100
            self.audio_level_meter.setValue(meter_value)
            
            # Update label with dB level
            if audio_level > self.voice_service.get_silence_threshold():
                if self.voice_service.is_continuous_voice_mode():
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
                if self.voice_service.is_continuous_voice_mode():
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
        """Trigger TTS for AI response"""
        if self.voice_mode and self.voice_settings.get("auto_speak", True):
            from pyside_chat.ui.styles.message_formatter import MessageFormatter
            plain_text = MessageFormatter.to_plain_text(text)
            logger.debug(f"Speaking AI response (plain): {plain_text[:50]}...")
            self.voice_service.speak_text(plain_text)
        elif self.voice_settings.get("auto_speak", True):
            # Also speak in chat mode if auto_speak is enabled
            from pyside_chat.ui.styles.message_formatter import MessageFormatter
            plain_text = MessageFormatter.to_plain_text(text)
            logger.debug(f"Speaking AI response in chat mode: {plain_text[:50]}...")
            self.voice_service.speak_text(plain_text)
    
    def update_voice_settings(self, settings: dict):
        """Update voice settings"""
        self.voice_settings.update(settings)
        self.voice_service.update_settings(settings)
    
    def get_voice_settings(self) -> dict:
        """Get current voice settings"""
        return self.voice_settings.copy()
    
    def is_voice_mode_active(self) -> bool:
        """Check if voice mode is active"""
        return self.voice_mode
    
    def is_tts_playing(self) -> bool:
        """Check if TTS is currently playing"""
        return hasattr(self.voice_service, 'is_playing_tts') and self.voice_service.is_playing_tts
    
    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'voice_button': self.voice_button,
            'voice_settings_button': self.voice_settings_button,
            'audio_level_widget': self.audio_level_widget
        } 
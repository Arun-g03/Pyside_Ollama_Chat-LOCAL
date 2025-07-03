"""
Voice Settings Dialog

Allows users to configure voice input/output settings including:
- STT (Speech-to-Text) API selection
- TTS (Text-to-Speech) API selection  
- Voice selection for TTS
- Internet connectivity checks
"""

import os
from typing import Dict, List, Optional
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QGroupBox, QCheckBox,
                               QMessageBox, QProgressBar, QTextEdit, QTabWidget, QWidget, QSpinBox, QDoubleSpinBox)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QFont

from pyside_chat.utils.internet_connection import test_internet_connection
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class InternetCheckThread(QThread):
    """Thread for checking internet connectivity"""
    check_completed = Signal(bool, str)
    
    def run(self):
        try:
            is_connected = test_internet_connection()
            status = "Connected" if is_connected else "Not connected"
            self.check_completed.emit(is_connected, status)
        except Exception as e:
            self.check_completed.emit(False, f"Error: {str(e)}")


class VoiceSettingsDialog(QDialog):
    """Dialog for configuring voice settings"""
    
    # Signals
    settings_changed = Signal(dict)  # Emitted when settings are changed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Voice Settings")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Voice API configurations
        self.stt_apis = {
            "Google Speech Recognition": {
                "requires_internet": True,
                "description": "High accuracy, free tier available (60 min/month)",
                "voices": []
            },
            "Vosk (Offline)": {
                "requires_internet": False,
                "description": "Offline speech recognition, good accuracy",
                "voices": []
            }
        }
        
        self.tts_apis = {
            "Google TTS": {
                "requires_internet": True,
                "description": "High quality, many voices",
                "voices": [
                    "en", "en-US", "en-GB", "en-AU", "en-CA", "en-IN", "en-IE", "en-ZA"
                ]
            },
            "Azure Speech": {
                "requires_internet": True,
                "description": "Microsoft's TTS service",
                "voices": [
                    "en-US-AriaNeural", "en-US-DavisNeural", "en-US-GuyNeural", "en-US-JennyNeural",
                    "en-US-SaraNeural", "en-US-TonyNeural", "en-GB-RyanNeural", "en-GB-SoniaNeural"
                ]
            },
            "OpenAI TTS": {
                "requires_internet": True,
                "description": "OpenAI's TTS service",
                "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
            },
            "Local TTS": {
                "requires_internet": False,
                "description": "Offline TTS (requires model download)",
                "voices": ["default"]
            },
            "eSpeak": {
                "requires_internet": False,
                "description": "Offline TTS, robotic but fast",
                "voices": ["en", "en-us", "en-gb", "en-sc", "en-uk"]
            }
        }
        
        # Current settings
        self.current_settings = {
            "stt_api": "Google Speech Recognition",
            "tts_api": "Google TTS",
            "tts_voice": "en",
            "auto_speak": True,
            "voice_speed": 1.0,
            "recording_timeout": 10.0,
            "silence_duration": 2.0,
            "silence_threshold": 0.005
        }
        
        # Internet status
        self.internet_available = False
        
        self.setup_ui()
        self.setup_connections()
        self.check_internet_connection()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # STT Tab
        stt_tab = self.create_stt_tab()
        tab_widget.addTab(stt_tab, "Speech-to-Text")
        
        # TTS Tab
        tts_tab = self.create_tts_tab()
        tab_widget.addTab(tts_tab, "Text-to-Speech")
        
        # General Tab
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "General")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.test_button = QPushButton("Test Settings")
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        button_layout.addWidget(self.test_button)
        
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #232323;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background: #232323;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444;
                padding: 8px 16px;
            }
            QTabBar::tab:selected {
                background: #0078d4;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #0078d4;
            }
            QLabel {
                color: #ffffff;
            }
            QCheckBox {
                color: #ffffff;
            }
        """)
        
    def create_stt_tab(self):
        """Create the STT configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Internet status
        internet_group = QGroupBox("Internet Connection")
        internet_layout = QVBoxLayout(internet_group)
        
        self.internet_status_label = QLabel("Checking internet connection...")
        self.internet_status_label.setStyleSheet("color: #ffa500;")
        internet_layout.addWidget(self.internet_status_label)
        
        self.refresh_internet_button = QPushButton("Refresh")
        self.refresh_internet_button.setMaximumWidth(100)
        internet_layout.addWidget(self.refresh_internet_button)
        
        layout.addWidget(internet_group)
        
        # STT API selection
        stt_group = QGroupBox("Speech-to-Text API")
        stt_layout = QVBoxLayout(stt_group)
        
        stt_layout.addWidget(QLabel("Select STT API:"))
        
        self.stt_api_combo = QComboBox()
        for api_name, api_info in self.stt_apis.items():
            self.stt_api_combo.addItem(api_name)
        stt_layout.addWidget(self.stt_api_combo)
        
        self.stt_description_label = QLabel("")
        self.stt_description_label.setWordWrap(True)
        self.stt_description_label.setStyleSheet("color: #ccc; font-style: italic;")
        stt_layout.addWidget(self.stt_description_label)
        
        layout.addWidget(stt_group)
        layout.addStretch()
        
        return widget
        
    def create_tts_tab(self):
        """Create the TTS configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # TTS API selection
        tts_group = QGroupBox("Text-to-Speech API")
        tts_layout = QVBoxLayout(tts_group)
        
        tts_layout.addWidget(QLabel("Select TTS API:"))
        
        self.tts_api_combo = QComboBox()
        for api_name, api_info in self.tts_apis.items():
            self.tts_api_combo.addItem(api_name)
        tts_layout.addWidget(self.tts_api_combo)
        
        self.tts_description_label = QLabel("")
        self.tts_description_label.setWordWrap(True)
        self.tts_description_label.setStyleSheet("color: #ccc; font-style: italic;")
        tts_layout.addWidget(self.tts_description_label)
        
        # Voice selection
        voice_group = QGroupBox("Voice Selection")
        voice_layout = QVBoxLayout(voice_group)
        
        voice_layout.addWidget(QLabel("Select Voice:"))
        
        self.voice_combo = QComboBox()
        voice_layout.addWidget(self.voice_combo)
        
        layout.addWidget(tts_group)
        layout.addWidget(voice_group)
        layout.addStretch()
        
        return widget
        
    def create_general_tab(self):
        """Create the general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # General settings
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout(general_group)
        
        self.auto_speak_checkbox = QCheckBox("Automatically speak AI responses")
        self.auto_speak_checkbox.setChecked(True)
        general_layout.addWidget(self.auto_speak_checkbox)
        
        # Recording timeout setting
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Recording Timeout (seconds):"))
        
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 60)
        self.timeout_spinbox.setValue(10)
        self.timeout_spinbox.setToolTip("Maximum recording duration before auto-stop (fallback)")
        self.timeout_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addStretch()
        
        general_layout.addLayout(timeout_layout)
        
        # Audio Gate Settings
        audio_gate_group = QGroupBox("Audio Gate Settings")
        audio_gate_layout = QVBoxLayout(audio_gate_group)
        
        # Silence duration setting
        silence_duration_layout = QHBoxLayout()
        silence_duration_layout.addWidget(QLabel("Silence Duration (seconds):"))
        
        self.silence_duration_spinbox = QSpinBox()
        self.silence_duration_spinbox.setRange(1, 10)
        self.silence_duration_spinbox.setValue(2)
        self.silence_duration_spinbox.setToolTip("Duration of silence before auto-stop")
        self.silence_duration_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        silence_duration_layout.addWidget(self.silence_duration_spinbox)
        silence_duration_layout.addStretch()
        
        audio_gate_layout.addLayout(silence_duration_layout)
        
        # Silence threshold setting
        silence_threshold_layout = QHBoxLayout()
        silence_threshold_layout.addWidget(QLabel("Silence Threshold:"))
        
        self.silence_threshold_spinbox = QDoubleSpinBox()
        self.silence_threshold_spinbox.setRange(0.0001, 1)
        self.silence_threshold_spinbox.setSingleStep(0.001)
        self.silence_threshold_spinbox.setDecimals(4)
        self.silence_threshold_spinbox.setValue(0.005)
        self.silence_threshold_spinbox.setToolTip("Audio level threshold for silence detection (0.0001–1, lower = more sensitive)")
        self.silence_threshold_spinbox.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        silence_threshold_layout.addWidget(self.silence_threshold_spinbox)
        silence_threshold_layout.addStretch()
        
        audio_gate_layout.addLayout(silence_threshold_layout)
        
        layout.addWidget(audio_gate_group)
        
        layout.addWidget(general_group)
        layout.addStretch()
        
        return widget
        
    def setup_connections(self):
        """Setup signal connections"""
        self.stt_api_combo.currentTextChanged.connect(self.on_stt_api_changed)
        self.tts_api_combo.currentTextChanged.connect(self.on_tts_api_changed)
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)
        self.refresh_internet_button.clicked.connect(self.check_internet_connection)
        self.test_button.clicked.connect(self.test_settings)
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save_settings)
        
    def check_internet_connection(self):
        """Check internet connectivity"""
        self.internet_status_label.setText("Checking internet connection...")
        self.internet_status_label.setStyleSheet("color: #ffa500;")
        
        self.internet_thread = InternetCheckThread()
        self.internet_thread.check_completed.connect(self.on_internet_check_completed)
        self.internet_thread.start()
        
    def on_internet_check_completed(self, is_connected: bool, status: str):
        """Handle internet check completion"""
        self.internet_available = is_connected
        
        if is_connected:
            self.internet_status_label.setText("✅ Internet connection available")
            self.internet_status_label.setStyleSheet("color: #4caf50;")
        else:
            self.internet_status_label.setText("❌ No internet connection")
            self.internet_status_label.setStyleSheet("color: #f44336;")
            
        # Update API availability
        self.update_api_availability()
        
    def update_api_availability(self):
        """Update API availability based on internet connection"""
        for i in range(self.stt_api_combo.count()):
            api_name = self.stt_api_combo.itemText(i)
            api_info = self.stt_apis.get(api_name, {})
            
            if api_info.get("requires_internet", False) and not self.internet_available:
                # Disable internet-required APIs when offline
                self.stt_api_combo.setItemText(i, f"{api_name} (Offline)")
            else:
                self.stt_api_combo.setItemText(i, api_name)
                
        for i in range(self.tts_api_combo.count()):
            api_name = self.tts_api_combo.itemText(i)
            api_info = self.tts_apis.get(api_name, {})
            
            if api_info.get("requires_internet", False) and not self.internet_available:
                # Disable internet-required APIs when offline
                self.tts_api_combo.setItemText(i, f"{api_name} (Offline)")
            else:
                self.tts_api_combo.setItemText(i, api_name)
                
    def on_stt_api_changed(self, api_name: str):
        """Handle STT API selection change"""
        # Remove "(Offline)" suffix if present
        clean_name = api_name.replace(" (Offline)", "")
        api_info = self.stt_apis.get(clean_name, {})
        
        description = api_info.get("description", "")
        if api_info.get("requires_internet", False) and not self.internet_available:
            description += " (Requires internet connection)"
            
        self.stt_description_label.setText(description)
        
    def on_tts_api_changed(self, api_name: str):
        """Handle TTS API selection change"""
        # Remove "(Offline)" suffix if present
        clean_name = api_name.replace(" (Offline)", "")
        api_info = self.tts_apis.get(clean_name, {})
        
        description = api_info.get("description", "")
        if api_info.get("requires_internet", False) and not self.internet_available:
            description += " (Requires internet connection)"
            
        self.tts_description_label.setText(description)
        
        # Update voice options
        self.voice_combo.clear()
        voices = api_info.get("voices", [])
        for voice in voices:
            self.voice_combo.addItem(voice)
            
    def on_voice_changed(self, voice: str):
        """Handle voice selection change"""
        pass  # Can be used for voice preview
        
    def test_settings(self):
        """Test the current voice settings"""
        try:
            # Test microphone access
            import pyaudio
            audio = pyaudio.PyAudio()
            
            # Try to open a test stream
            test_stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            
            # Read a small sample
            data = test_stream.read(1024, exception_on_overflow=False)
            test_stream.close()
            audio.terminate()
            
            # Calculate audio level
            import struct
            import math
            samples = struct.unpack(f'{len(data)//2}h', data)
            if samples:
                rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))
                normalized_rms = rms / 32768.0
                db_level = 20 * math.log10(normalized_rms) if normalized_rms > 0 else -60
                
                QMessageBox.information(
                    self, 
                    "Microphone Test", 
                    f"Microphone test successful!\n\n"
                    f"Audio Level: {normalized_rms:.4f}\n"
                    f"dB Level: {db_level:.1f} dB\n\n"
                    f"Your microphone is working correctly."
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Microphone Test", 
                    "Microphone test completed but no audio detected.\n\n"
                    "Please check your microphone settings and try speaking."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Microphone Test Failed", 
                f"Failed to access microphone:\n\n{str(e)}\n\n"
                "Please check your microphone permissions and settings."
            )
        
    def save_settings(self):
        """Save the current settings"""
        settings = {
            "stt_api": self.stt_api_combo.currentText().replace(" (Offline)", ""),
            "tts_api": self.tts_api_combo.currentText().replace(" (Offline)", ""),
            "tts_voice": self.voice_combo.currentText(),
            "auto_speak": self.auto_speak_checkbox.isChecked(),
            "voice_speed": 1.0,  # TODO: Add speed control
            "recording_timeout": self.timeout_spinbox.value(),
            "silence_duration": self.silence_duration_spinbox.value(),
            "silence_threshold": self.silence_threshold_spinbox.value()
        }
        
        self.current_settings = settings
        self.settings_changed.emit(settings)
        self.accept()
        
    def get_settings(self) -> dict:
        """Get current settings"""
        return self.current_settings.copy()
        
    def set_settings(self, settings: dict):
        """Set current settings"""
        self.current_settings = settings.copy()
        
        # Update UI with settings
        if "stt_api" in settings:
            index = self.stt_api_combo.findText(settings["stt_api"])
            if index >= 0:
                self.stt_api_combo.setCurrentIndex(index)
                
        if "tts_api" in settings:
            index = self.tts_api_combo.findText(settings["tts_api"])
            if index >= 0:
                self.tts_api_combo.setCurrentIndex(index)
                
        if "tts_voice" in settings:
            index = self.voice_combo.findText(settings["tts_voice"])
            if index >= 0:
                self.voice_combo.setCurrentIndex(index)
                
        if "auto_speak" in settings:
            self.auto_speak_checkbox.setChecked(settings["auto_speak"])
            
        if "recording_timeout" in settings:
            self.timeout_spinbox.setValue(int(settings["recording_timeout"]))
            
        if "silence_duration" in settings:
            self.silence_duration_spinbox.setValue(int(settings["silence_duration"]))
            
        if "silence_threshold" in settings:
            self.silence_threshold_spinbox.setValue(float(settings["silence_threshold"])) 
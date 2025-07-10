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

from pyside_chat.core.utils.internet_checker import test_internet_connection
from pyside_chat.core.logging.logger import CustomLogger

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
    
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.setWindowTitle("Voice Settings")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.config_manager = config_manager
        
        # Voice API configurations
        self.stt_apis = {
            "Vosk (Offline)": {
                "requires_internet": False,
                "description": "Offline speech recognition, good accuracy",
                "voices": []
            }
        }
        
        self.tts_apis = {
            "Coqui TTS": {
                "requires_internet": False,
                "description": "High-quality local TTS with emotion control and multi-speaker support",
                "voices": ["default"]
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
            "stt_api": "Vosk (Offline)",
            "tts_api": "Coqui TTS",
            "tts_voice": "default",
            "auto_speak": True,
            "voice_speed": 1.0,
            "recording_timeout": 10.0,
            "silence_duration": 2.0,
            "silence_threshold": 0.005,
            "coqui_model": "tts_models/en/vctk/vits",
            "coqui_speaker": "ED",
            "eq_visualizer": "None",
            "tts_streaming": True  # Enable streaming by default
        }
        
        # Internet status
        self.internet_available = False
        
        # Add EQ visualizer selection to General tab
        self.eq_types = ["None", "Circle EQ", "Bar EQ", "Waveform EQ", "Waveform Gradient", "Waveform Blue Gradient"]
        self.eq_selector = QComboBox(self)
        self.eq_selector.addItems(self.eq_types)
        self.eq_selector.setCurrentIndex(0)
        
        self.setup_ui()
        self.setup_connections()
        self.check_internet_connection()
        
        # Load settings from config if available
        if self.config_manager:
            config_settings = self.config_manager.get_voice_settings()
            self.current_settings.update(config_settings)
        
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
        
        # Coqui TTS specific controls
        self.coqui_controls = QWidget()
        coqui_layout = QVBoxLayout(self.coqui_controls)
        
        # Model selection for Coqui TTS
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self.on_coqui_model_changed)
        model_layout.addWidget(self.model_combo)
        
        # Download button for selected model
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_selected_model)
        self.download_button.setVisible(False)
        model_layout.addWidget(self.download_button)
        
        coqui_layout.addLayout(model_layout)
        
        # Speaker selection for Coqui TTS
        speaker_layout = QHBoxLayout()
        speaker_layout.addWidget(QLabel("Speaker:"))
        self.speaker_combo = QComboBox()
        self.speaker_combo.currentTextChanged.connect(self.on_coqui_speaker_changed)
        speaker_layout.addWidget(self.speaker_combo)
        
        coqui_layout.addLayout(speaker_layout)
        
        # Model info label
        self.model_info_label = QLabel("")
        self.model_info_label.setWordWrap(True)
        self.model_info_label.setStyleSheet("color: #ccc; font-style: italic;")
        coqui_layout.addWidget(self.model_info_label)
        
        self.coqui_controls.setVisible(False)
        voice_layout.addWidget(self.coqui_controls)
        
        # Standard voice selection (for other TTS APIs)
        self.standard_voice_widget = QWidget()
        self.standard_voice_layout = QVBoxLayout(self.standard_voice_widget)
        self.standard_voice_layout.addWidget(QLabel("Select Voice:"))
        
        self.voice_combo = QComboBox()
        self.standard_voice_layout.addWidget(self.voice_combo)
        
        voice_layout.addWidget(self.standard_voice_widget)
        
        # TTS Streaming Settings
        streaming_group = QGroupBox("TTS Streaming Settings")
        streaming_layout = QVBoxLayout(streaming_group)
        
        self.streaming_checkbox = QCheckBox("Enable streaming synthesis")
        self.streaming_checkbox.setChecked(True)
        self.streaming_checkbox.setToolTip("Enable real-time streaming TTS synthesis for faster response")
        streaming_layout.addWidget(self.streaming_checkbox)
        
        # Streaming description
        streaming_description = QLabel(
            "Streaming synthesis starts playing audio immediately as text is processed, "
            "rather than waiting for the entire audio to be generated first. "
            "This provides faster response times, especially for longer texts."
        )
        streaming_description.setWordWrap(True)
        streaming_description.setStyleSheet("color: #ccc; font-size: 11px; margin-top: 5px;")
        streaming_layout.addWidget(streaming_description)
        
        layout.addWidget(tts_group)
        layout.addWidget(voice_group)
        layout.addWidget(streaming_group)
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
        
        # Add sensitivity indicator
        self.sensitivity_label = QLabel("(Balanced)")
        self.sensitivity_label.setStyleSheet("color: #00ff00; font-style: italic;")
        silence_threshold_layout.addWidget(self.sensitivity_label)
        
        silence_threshold_layout.addStretch()
        
        audio_gate_layout.addLayout(silence_threshold_layout)
        
        # Add description for silence threshold
        threshold_description = QLabel(
            "Lower values = more sensitive (detects quieter sounds)\n"
            "Higher values = less sensitive (only detects louder sounds)\n"
            "Recommended: 0.001-0.01 for quiet environments, 0.01-0.05 for normal use"
        )
        threshold_description.setWordWrap(True)
        threshold_description.setStyleSheet("color: #ccc; font-size: 11px; margin-top: 5px;")
        audio_gate_layout.addWidget(threshold_description)
        
        layout.addWidget(audio_gate_group)
        
        # EQ Visualizer Settings
        eq_group = QGroupBox("EQ Visualizer Settings")
        eq_layout = QVBoxLayout(eq_group)
        
        # EQ Visualizer dropdown
        eq_selector_layout = QHBoxLayout()
        eq_selector_layout.addWidget(QLabel("EQ Visualizer:"))
        
        self.eq_selector.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                selection-background-color: #0078d4;
            }
        """)
        eq_selector_layout.addWidget(self.eq_selector)
        eq_selector_layout.addStretch()
        
        eq_layout.addLayout(eq_selector_layout)
        
        # Add description for EQ visualizer
        eq_description = QLabel(
            "Select an EQ visualizer to display during voice interactions.\n"
            "• None: No visualizer\n"
            "• Circle EQ: Circular frequency display\n"
            "• Bar EQ: Traditional bar equalizer\n"
            "• Waveform EQ: Connected points with audio reactivity\n"
            "• Waveform Gradient: Smooth gradient fills\n"
            "• Waveform Blue Gradient: Blue-themed gradient visualizer"
        )
        eq_description.setWordWrap(True)
        eq_description.setStyleSheet("color: #ccc; font-size: 11px; margin-top: 5px;")
        eq_layout.addWidget(eq_description)
        
        layout.addWidget(eq_group)
        layout.addWidget(general_group)
        layout.addStretch()
        
        return widget
        
    def setup_connections(self):
        """Setup signal connections"""
        self.stt_api_combo.currentTextChanged.connect(self.on_stt_api_changed)
        self.tts_api_combo.currentTextChanged.connect(self.on_tts_api_changed)
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)
        self.silence_threshold_spinbox.valueChanged.connect(self.on_silence_threshold_changed)
        self.eq_selector.currentTextChanged.connect(self.on_eq_visualizer_changed)
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
        
        if clean_name == "Coqui TTS":
            # Show Coqui TTS controls and hide standard voice selection
            self.coqui_controls.setVisible(True)
            self.standard_voice_widget.setVisible(False)
            
            # Load Coqui TTS models
            self.load_coqui_models()
        else:
            # Hide Coqui TTS controls and show standard voice selection
            self.coqui_controls.setVisible(False)
            self.standard_voice_widget.setVisible(True)
            
            # Use predefined voices for other APIs
            voices = api_info.get("voices", [])
            for voice in voices:
                self.voice_combo.addItem(voice)
            
    def on_voice_changed(self, voice: str):
        """Handle voice selection change"""
        pass
        
    def on_eq_visualizer_changed(self, eq_type: str):
        """Handle EQ visualizer selection change"""
        # Update the current settings
        self.current_settings["eq_visualizer"] = eq_type
        logger.info(f"EQ visualizer changed to: {eq_type}")  # Can be used for voice preview
    
    def load_coqui_models(self):
        """Load available Coqui TTS models"""
        try:
            from pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service import CoquiTTSService
            
            self.coqui_service = CoquiTTSService()
            self.available_models = self.coqui_service.get_available_models()
            
            self.model_combo.clear()
            for model in self.available_models:
                # Check if model is downloaded
                if self.coqui_service.is_model_downloaded(model):
                    self.model_combo.addItem(f"✅ {model}")
                else:
                    size = self.coqui_service.get_model_download_size(model)
                    self.model_combo.addItem(f"⬇️ {model} ({size})")
            
            if self.available_models:
                self.model_combo.setCurrentIndex(0)
                self.on_coqui_model_changed(self.model_combo.currentText())
            
            logger.info(f"Loaded {len(self.available_models)} Coqui TTS models")
            
        except Exception as e:
            logger.error(f"Failed to load Coqui TTS models: {e}")
            self.model_info_label.setText(f"Failed to load models: {str(e)}")
    
    def on_coqui_model_changed(self, model_text: str):
        """Handle Coqui TTS model selection"""
        try:
            # Extract model name from display text
            model_name = model_text.replace("✅ ", "").replace("⬇️ ", "").split(" (")[0]
            
            # Check if model is downloaded
            is_downloaded = self.coqui_service.is_model_downloaded(model_name)
            
            if is_downloaded:
                self.model_info_label.setText(f"✅ Model '{model_name}' is downloaded and ready to use")
                self.download_button.setVisible(False)
                
                # Load speakers for this model
                self.load_coqui_speakers(model_name)
            else:
                size = self.coqui_service.get_model_download_size(model_name)
                self.model_info_label.setText(f"⬇️ Model '{model_name}' needs to be downloaded ({size})")
                self.download_button.setVisible(True)
                
                # Clear speakers
                self.speaker_combo.clear()
            
            # Store selected model
            self.selected_coqui_model = model_name
            
        except Exception as e:
            logger.error(f"Failed to handle Coqui model change: {e}")
            self.model_info_label.setText(f"Error: {str(e)}")
    
    def load_coqui_speakers(self, model_name: str):
        """Load available speakers for the selected model"""
        try:
            if self.coqui_service.load_model(model_name):
                self.speaker_combo.clear()
                if self.coqui_service.is_multi_speaker():
                    speakers = self.coqui_service.available_voices
                    for speaker in speakers:
                        self.speaker_combo.addItem(speaker)
                    self.speaker_combo.setCurrentIndex(0)
                    self.model_info_label.setText(f"Found {len(speakers)} speakers for model '{model_name}'")
                else:
                    # Single-speaker model
                    self.speaker_combo.addItem("default")
                    self.model_info_label.setText(f"Model '{model_name}' has no multiple speakers (single voice)")
                logger.info(f"Loaded {len(self.coqui_service.available_voices) if self.coqui_service.available_voices else 1} speakers for model '{model_name}'")
            else:
                self.speaker_combo.clear()
                self.model_info_label.setText(f"Failed to load model '{model_name}'")
        except Exception as e:
            logger.error(f"Failed to load Coqui speakers: {e}")
            self.model_info_label.setText(f"Error loading speakers: {str(e)}")
    
    def on_coqui_speaker_changed(self, speaker_name: str):
        """Handle Coqui TTS speaker selection"""
        self.selected_coqui_speaker = speaker_name
        logger.info(f"Selected Coqui TTS speaker: {speaker_name}")
    
    def download_selected_model(self):
        """Download the selected Coqui TTS model"""
        if not hasattr(self, 'selected_coqui_model') or not self.selected_coqui_model:
            return
        
        model_name = self.selected_coqui_model
        
        reply = QMessageBox.question(
            self, 
            "Download Model", 
            f"Download model '{model_name}'?\n\n"
            "This may take several minutes depending on your internet connection.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.start_coqui_download(model_name)
    
    def start_coqui_download(self, model_name: str):
        """Start downloading a Coqui TTS model"""
        try:
            from pyside_chat.ui.Widgets.coqui_model_dialog import ModelDownloadThread
            
            self.download_button.setEnabled(False)
            self.download_button.setText("Downloading...")
            
            self.download_thread = ModelDownloadThread(model_name)
            self.download_thread.download_completed.connect(self.on_coqui_download_completed)
            self.download_thread.start()
            
            self.model_info_label.setText(f"Downloading {model_name}...")
            
        except Exception as e:
            logger.error(f"Failed to start Coqui download: {e}")
            QMessageBox.critical(self, "Download Error", f"Failed to start download:\n{str(e)}")
            self.download_button.setEnabled(True)
            self.download_button.setText("Download")
    
    def on_coqui_download_completed(self, success: bool, message: str):
        """Handle Coqui TTS download completion"""
        self.download_button.setEnabled(True)
        self.download_button.setText("Download")
        
        if success:
            self.model_info_label.setText(f"✅ {message}")
            # Reload models to update download status
            self.load_coqui_models()
            QMessageBox.information(self, "Download Complete", message)
        else:
            self.model_info_label.setText(f"❌ {message}")
            QMessageBox.critical(self, "Download Failed", message)
        
    def on_silence_threshold_changed(self, value: float):
        """Handle silence threshold value change"""
        if value <= 0.001:
            self.sensitivity_label.setText("(Very Sensitive)")
            self.sensitivity_label.setStyleSheet("color: #ff0000; font-style: italic;")
        elif value <= 0.005:
            self.sensitivity_label.setText("(Sensitive)")
            self.sensitivity_label.setStyleSheet("color: #ff6600; font-style: italic;")
        elif value <= 0.01:
            self.sensitivity_label.setText("(Balanced)")
            self.sensitivity_label.setStyleSheet("color: #00ff00; font-style: italic;")
        elif value <= 0.05:
            self.sensitivity_label.setText("(Less Sensitive)")
            self.sensitivity_label.setStyleSheet("color: #ffff00; font-style: italic;")
        else:
            self.sensitivity_label.setText("(Not Sensitive)")
            self.sensitivity_label.setStyleSheet("color: #00ffff; font-style: italic;")
        
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
            "silence_threshold": self.silence_threshold_spinbox.value(),
            "coqui_model": getattr(self, "selected_coqui_model", self.model_combo.currentText() if hasattr(self, "model_combo") else None),
            "coqui_speaker": getattr(self, "selected_coqui_speaker", self.speaker_combo.currentText() if hasattr(self, "speaker_combo") else None),
            "eq_visualizer": self.eq_selector.currentText(),
            "tts_streaming": self.streaming_checkbox.isChecked()
        }
        
        self.current_settings = settings
        self.settings_changed.emit(settings)
        
        # Save settings to config if config manager is available
        if self.config_manager:
            self.config_manager.set_voice_settings(settings)
        
        self.accept()
        
        # --- NEW: Lock in model and speaker ---
        # Assuming you have access to your TTS service here:
        if hasattr(self, "coqui_service") and self.selected_coqui_model:
            self.coqui_service.load_model(self.selected_coqui_model)
            if self.selected_coqui_speaker:
                self.coqui_service.set_voice(self.selected_coqui_speaker)
        
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
            # Update sensitivity indicator
            self.on_silence_threshold_changed(float(settings["silence_threshold"]))
            
        if "tts_streaming" in settings:
            self.streaming_checkbox.setChecked(settings["tts_streaming"])
            
        if "eq_visualizer" in settings:
            index = self.eq_selector.findText(settings["eq_visualizer"])
            if index >= 0:
                self.eq_selector.setCurrentIndex(index)
            else:
                # Default to "None" if the setting is not found
                self.eq_selector.setCurrentIndex(0)
        
        # Handle Coqui TTS model and speaker settings
        if "coqui_model" in settings and settings["coqui_model"]:
            self.selected_coqui_model = settings["coqui_model"]
            # Load models first if not already loaded
            if not hasattr(self, "coqui_service"):
                self.load_coqui_models()
            
            # Find and select the model in the combo box
            if hasattr(self, "model_combo"):
                for i in range(self.model_combo.count()):
                    model_text = self.model_combo.itemText(i)
                    model_name = model_text.replace("✅ ", "").replace("⬇️ ", "").split(" (")[0]
                    if model_name == settings["coqui_model"]:
                        self.model_combo.setCurrentIndex(i)
                        self.on_coqui_model_changed(model_text)
                        break
        
        if "coqui_speaker" in settings and settings["coqui_speaker"]:
            self.selected_coqui_speaker = settings["coqui_speaker"]
            # Find and select the speaker in the combo box
            if hasattr(self, "speaker_combo"):
                for i in range(self.speaker_combo.count()):
                    if self.speaker_combo.itemText(i) == settings["coqui_speaker"]:
                        self.speaker_combo.setCurrentIndex(i)
                        break

    def on_tts_settings_changed(self, settings):
        # ... other settings ...
        model = settings.get("coqui_model")
        speaker = settings.get("coqui_speaker")
        if model:
            self.main_tts_service.load_model(model)
            if speaker:
                self.main_tts_service.set_voice(speaker) 
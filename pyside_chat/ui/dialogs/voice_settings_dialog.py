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
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QGroupBox,
    QCheckBox,
    QMessageBox,
    QProgressBar,
    QTextEdit,
    QTabWidget,
    QWidget,
    QSpinBox,
    QDoubleSpinBox)
from PySide6.QtCore import Qt, Signal, QThread, QObject, QTimer
from PySide6.QtGui import QFont
# Added for QApplication.processEvents()
from PySide6.QtWidgets import QApplication

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
                "voices": ["default"]},
            "Azure Speech": {
                "requires_internet": True,
                "description": "Microsoft's TTS service",
                "voices": [
                    "en-US-AriaNeural",
                    "en-US-DavisNeural",
                    "en-US-GuyNeural",
                    "en-US-JennyNeural",
                    "en-US-SaraNeural",
                    "en-US-TonyNeural",
                    "en-GB-RyanNeural",
                    "en-GB-SoniaNeural"]},
            "OpenAI TTS": {
                "requires_internet": True,
                "description": "OpenAI's TTS service",
                "voices": [
                    "alloy",
                    "echo",
                    "fable",
                    "onyx",
                    "nova",
                    "shimmer"]},
            "Local TTS": {
                "requires_internet": False,
                "description": "Offline TTS (requires model download)",
                "voices": ["default"]},
            "eSpeak": {
                "requires_internet": False,
                "description": "Offline TTS, robotic but fast",
                "voices": [
                    "en",
                    "en-us",
                    "en-gb",
                    "en-sc",
                    "en-uk"]}}

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
            "tts_streaming": True,  # Enable streaming by default
            "allow_interruptions": True,  # Allow user interruptions
            "interruption_threshold": 0.5
        }

        # Internet status
        self.internet_available = False

        # Add EQ visualizer selection to General tab
        self.eq_types = [
            "None",
            "Circle EQ",
            "Bar EQ",
            "Waveform EQ",
            "Waveform Gradient",
            "Waveform Blue Gradient"]
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

        # --- Ensure TTS panel is correct on open ---
        # After all widgets are created, trigger the TTS API change logic
        current_tts_api = self.tts_api_combo.currentText()
        self.on_tts_api_changed(current_tts_api)

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
        self.stt_description_label.setStyleSheet(
            "color: #ccc; font-style: italic;")
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
        self.tts_description_label.setStyleSheet(
            "color: #ccc; font-style: italic;")
        tts_layout.addWidget(self.tts_description_label)

        # Voice selection group
        voice_group = QGroupBox("Voice Selection")
        voice_layout = QVBoxLayout(voice_group)

        # Coqui controls (always present, only visible for Coqui)
        self.coqui_controls = QWidget()
        coqui_layout = QVBoxLayout(self.coqui_controls)

        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(
            self.on_coqui_model_changed)
        model_layout.addWidget(self.model_combo)
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_selected_model)
        self.download_button.setVisible(False)
        model_layout.addWidget(self.download_button)
        coqui_layout.addLayout(model_layout)

        # Speaker selection
        speaker_layout = QHBoxLayout()
        speaker_layout.addWidget(QLabel("Speaker:"))
        self.speaker_combo = QComboBox()
        self.speaker_combo.currentTextChanged.connect(
            self.on_coqui_speaker_changed)
        speaker_layout.addWidget(self.speaker_combo)
        self.preview_speaker_button = QPushButton("🎵 Preview")
        self.preview_speaker_button.setToolTip(
            "Preview the selected speaker's voice")
        self.preview_speaker_button.clicked.connect(
            self.preview_selected_speaker)
        self.preview_speaker_button.setEnabled(False)
        speaker_layout.addWidget(self.preview_speaker_button)
        coqui_layout.addLayout(speaker_layout)

        self.speaker_info_label = QLabel("")
        self.speaker_info_label.setWordWrap(True)
        self.speaker_info_label.setStyleSheet(
            "color: #ccc; font-style: italic; margin-top: 5px;")
        coqui_layout.addWidget(self.speaker_info_label)

        self.speaker_filter_widget = QWidget()
        speaker_filter_layout = QHBoxLayout(self.speaker_filter_widget)
        speaker_filter_layout.setContentsMargins(0, 0, 0, 0)
        speaker_filter_layout.addWidget(QLabel("Filter:"))
        self.speaker_filter_combo = QComboBox()
        self.speaker_filter_combo.addItems(
            ["All Speakers", "Male", "Female", "English", "American", "British"])
        self.speaker_filter_combo.currentTextChanged.connect(
            self.filter_speakers)
        speaker_filter_layout.addWidget(self.speaker_filter_combo)
        self.speaker_filter_widget.setVisible(False)
        coqui_layout.addWidget(self.speaker_filter_widget)

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
        self.streaming_checkbox.setToolTip(
            "Enable real-time streaming TTS synthesis for faster response")
        streaming_layout.addWidget(self.streaming_checkbox)

        # Streaming description
        streaming_description = QLabel(
            "Streaming synthesis starts playing audio immediately as text is processed, "
            "rather than waiting for the entire audio to be generated first. "
            "This provides faster response times, especially for longer texts.")
        streaming_description.setWordWrap(True)
        streaming_description.setStyleSheet(
            "color: #ccc; font-size: 11px; margin-top: 5px;")
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

        # General settings group
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout(general_group)
        self.auto_speak_checkbox = QCheckBox(
            "Automatically speak AI responses")
        self.auto_speak_checkbox.setChecked(True)
        general_layout.addWidget(self.auto_speak_checkbox)
        layout.addWidget(general_group)

        # Interruption settings group (always visible)
        interruption_group = QGroupBox("Interruption Settings")
        interruption_layout = QVBoxLayout(interruption_group)
        self.allow_interruptions_checkbox = QCheckBox(
            "Allow user to interrupt AI responses")
        self.allow_interruptions_checkbox.setChecked(True)
        self.allow_interruptions_checkbox.setToolTip(
            "Enable this to allow users to interrupt AI responses by speaking")
        interruption_layout.addWidget(self.allow_interruptions_checkbox)
        # Interruption threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Interruption Threshold:"))
        self.interruption_threshold_spinbox = QDoubleSpinBox()
        self.interruption_threshold_spinbox.setRange(0.1, 1.0)
        self.interruption_threshold_spinbox.setSingleStep(0.1)
        self.interruption_threshold_spinbox.setValue(0.5)
        self.interruption_threshold_spinbox.setToolTip(
            "Audio level threshold for detecting user interruptions (higher = more sensitive)")
        threshold_layout.addWidget(self.interruption_threshold_spinbox)
        threshold_layout.addStretch()
        interruption_layout.addLayout(threshold_layout)
        layout.addWidget(interruption_group)

        # Recording timeout
        timeout_group = QGroupBox("Recording Timeout")
        timeout_layout = QHBoxLayout(timeout_group)
        timeout_layout.addWidget(QLabel("Recording Timeout (seconds):"))
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(1, 60)
        self.timeout_spinbox.setValue(10)
        self.timeout_spinbox.setToolTip(
            "Maximum recording duration before auto-stop (fallback)")
        timeout_layout.addWidget(self.timeout_spinbox)
        timeout_layout.addStretch()
        layout.addWidget(timeout_group)

        # Audio Gate Settings
        audio_gate_group = QGroupBox("Audio Gate Settings")
        audio_gate_layout = QVBoxLayout(audio_gate_group)

        # Silence duration setting
        silence_duration_layout = QHBoxLayout()
        silence_duration_layout.addWidget(
            QLabel("Silence Duration (seconds):"))

        self.silence_duration_spinbox = QSpinBox()
        self.silence_duration_spinbox.setRange(1, 10)
        self.silence_duration_spinbox.setValue(2)
        self.silence_duration_spinbox.setToolTip(
            "Duration of silence before auto-stop")
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
        self.silence_threshold_spinbox.setRange(0.001, 0.1)
        self.silence_threshold_spinbox.setSingleStep(0.001)
        self.silence_threshold_spinbox.setValue(0.005)
        self.silence_threshold_spinbox.setDecimals(3)
        self.silence_threshold_spinbox.setToolTip(
            "Audio level threshold for detecting silence (lower = more sensitive)")
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

        # Sensitivity indicator
        self.sensitivity_label = QLabel("Sensitivity: Medium")
        self.sensitivity_label.setStyleSheet(
            "color: #ccc; font-style: italic;")
        audio_gate_layout.addWidget(self.sensitivity_label)

        general_layout.addWidget(audio_gate_group)

        # EQ Visualizer selection
        eq_group = QGroupBox("EQ Visualizer")
        eq_layout = QHBoxLayout(eq_group)
        eq_label = QLabel("Select EQ Visualizer:")
        eq_layout.addWidget(eq_label)
        self.eq_selector.setMinimumWidth(180)
        eq_layout.addWidget(self.eq_selector)
        eq_layout.addStretch()
        general_layout.addWidget(eq_group)

        # TTS Streaming Settings
        tts_streaming_group = QGroupBox("TTS Streaming Settings")
        tts_streaming_layout = QVBoxLayout(tts_streaming_group)

        self.streaming_checkbox = QCheckBox("Enable streaming TTS")
        self.streaming_checkbox.setChecked(True)
        self.streaming_checkbox.setToolTip(
            "Use streaming TTS for better responsiveness")
        tts_streaming_layout.addWidget(self.streaming_checkbox)

        general_layout.addWidget(tts_streaming_group)

        # Internet connectivity
        internet_group = QGroupBox("Internet Connectivity")
        internet_layout = QVBoxLayout(internet_group)

        self.internet_status_label = QLabel("Checking internet connection...")
        self.internet_status_label.setStyleSheet("color: #ffa500;")
        internet_layout.addWidget(self.internet_status_label)

        self.refresh_internet_button = QPushButton("Refresh Connection Status")
        self.refresh_internet_button.setStyleSheet("""
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
        internet_layout.addWidget(self.refresh_internet_button)

        general_layout.addWidget(internet_group)

        layout.addWidget(general_group)
        layout.addStretch()

        return widget

    def setup_connections(self):
        """Setup signal connections"""
        self.stt_api_combo.currentTextChanged.connect(self.on_stt_api_changed)
        self.tts_api_combo.currentTextChanged.connect(self.on_tts_api_changed)
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)
        self.silence_threshold_spinbox.valueChanged.connect(
            self.on_silence_threshold_changed)
        self.eq_selector.currentTextChanged.connect(
            self.on_eq_visualizer_changed)
        self.refresh_internet_button.clicked.connect(
            self.check_internet_connection)
        self.test_button.clicked.connect(self.test_settings)
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save_settings)

    def check_internet_connection(self):
        """Check internet connectivity"""
        self.internet_status_label.setText("Checking internet connection...")
        self.internet_status_label.setStyleSheet("color: #ffa500;")

        self.internet_thread = InternetCheckThread()
        self.internet_thread.check_completed.connect(
            self.on_internet_check_completed)
        self.internet_thread.start()

    def on_internet_check_completed(self, is_connected: bool, status: str):
        """Handle internet check completion"""
        self.internet_available = is_connected

        if is_connected:
            self.internet_status_label.setText(
                "✅ Internet connection available")
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

            if api_info.get(
                "requires_internet",
                    False) and not self.internet_available:
                # Disable internet-required APIs when offline
                self.stt_api_combo.setItemText(i, f"{api_name} (Offline)")
            else:
                self.stt_api_combo.setItemText(i, api_name)

        for i in range(self.tts_api_combo.count()):
            api_name = self.tts_api_combo.itemText(i)
            api_info = self.tts_apis.get(api_name, {})

            if api_info.get(
                "requires_internet",
                    False) and not self.internet_available:
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
        if api_info.get(
            "requires_internet",
                False) and not self.internet_available:
            description += " (Requires internet connection)"

        self.stt_description_label.setText(description)

    def refresh_coqui_ui(self, force_refresh_service=False):
        """Refresh Coqui TTS UI, reusing the service if possible and updating models/speakers."""
        try:
            # Only fetch or instantiate if needed or forced
            if force_refresh_service or not hasattr(self, 'coqui_service') or self.coqui_service is None:
                from pyside_chat.features.voice.tts.coqui_tts_service import CoquiTTSService
                self.coqui_service = CoquiTTSService.get_instance()  # Singleton enforced in class

            # Disconnect previous signal to avoid duplicates
            try:
                self.coqui_service.voices_loaded.disconnect(self._on_voices_loaded)
            except Exception:
                pass
            self.coqui_service.voices_loaded.connect(self._on_voices_loaded)

            # Always refresh model list from backend
            if hasattr(self.coqui_service, 'get_available_models'):
                self.available_models = self.coqui_service.get_available_models()
            else:
                self.available_models = ["tts_models/en/vctk/vits"]
            self.model_combo.clear()
            for model in self.available_models:
                is_downloaded = hasattr(self.coqui_service, 'is_model_downloaded') and self.coqui_service.is_model_downloaded(model)
                size = "Unknown"
                if hasattr(self.coqui_service, 'get_model_download_size'):
                    size = self.coqui_service.get_model_download_size(model)
                if is_downloaded:
                    self.model_combo.addItem(f"✅ {model}")
                else:
                    self.model_combo.addItem(f"⬇️ {model} ({size})")
            if self.available_models:
                self.model_combo.setCurrentIndex(0)
                self.on_coqui_model_changed(self.model_combo.currentText())
            else:
                self.model_info_label.setText("No Coqui models available.")
                self.speaker_combo.clear()
                self.speaker_combo.addItem("No speakers available")
                self.speaker_combo.setEnabled(False)
            logger.info(f"[refresh_coqui_ui] Loaded {len(self.available_models)} Coqui TTS models")
        except Exception as e:
            logger.error(f"[refresh_coqui_ui] Failed to refresh Coqui TTS UI: {e}")
            self.model_info_label.setText(f"Failed to load models: {str(e)}")
            self.speaker_combo.clear()
            self.speaker_combo.addItem("No speakers available")
            self.speaker_combo.setEnabled(False)

    def _on_voices_loaded(self, speakers):
        """Slot to update speaker list when voices_loaded fires."""
        self.speaker_combo.clear()
        self.speaker_combo.setEnabled(False)
        self.speaker_info_label.setText("Loading speakers...")
        if speakers:
            for speaker in speakers:
                clean_speaker = speaker.strip()
                speaker_info = self.get_speaker_info(clean_speaker, getattr(self, 'selected_coqui_model', ''))
                display_name = speaker_info.get('display_name', clean_speaker)
                self.speaker_combo.addItem(display_name, clean_speaker)
            self.speaker_combo.setCurrentIndex(0)
            self.speaker_combo.setEnabled(True)
            self.speaker_info_label.setText(f"✅ Model loaded with {len(speakers)} speakers.")
            self.speaker_filter_widget.setVisible(True)
            self.preview_speaker_button.setEnabled(True)
            # Restore speaker selection if needed
            if hasattr(self, 'selected_coqui_speaker') and self.selected_coqui_speaker:
                for i in range(self.speaker_combo.count()):
                    if self.speaker_combo.itemData(i) == self.selected_coqui_speaker:
                        self.speaker_combo.setCurrentIndex(i)
                        break
        else:
            self.speaker_combo.addItem("No speakers available")
            self.speaker_combo.setEnabled(False)
            self.speaker_info_label.setText("No speakers found for this model.")
            self.speaker_filter_widget.setVisible(False)
            self.preview_speaker_button.setEnabled(False)

    def on_tts_api_changed(self, api_name: str):
        """Handle TTS API selection change"""
        # Remove "(Offline)" suffix if present
        clean_name = api_name.replace(" (Offline)", "")
        api_info = self.tts_apis.get(clean_name, {})

        description = api_info.get("description", "")
        if api_info.get(
            "requires_internet",
                False) and not self.internet_available:
            description += " (Requires internet connection)"

        self.tts_description_label.setText(description)

        # Update voice options
        self.voice_combo.clear()

        if clean_name == "Coqui TTS":
            # Always show Coqui controls, even for single-speaker models
            self.coqui_controls.setVisible(True)
            self.standard_voice_widget.setVisible(False)

            # Refresh Coqui TTS UI (reuse service if possible)
            self.refresh_coqui_ui(force_refresh_service=False)
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
        # Can be used for voice preview
        logger.info(f"EQ visualizer changed to: {eq_type}")

    def load_coqui_models(self):
        """DEPRECATED: Use refresh_coqui_ui instead."""
        self.refresh_coqui_ui(force_refresh_service=False)

    def on_coqui_model_changed(self, model_text: str):
        """Handle Coqui TTS model selection"""
        try:
            model_name = model_text.replace(
                "✅ ",
                "").replace(
                "⬇️ ",
                "").split(" (")[0]
            is_downloaded = hasattr(
                self.coqui_service,
                'is_model_downloaded') and self.coqui_service.is_model_downloaded(model_name)
            if is_downloaded:
                self.model_info_label.setText(
                    f"✅ Model '{model_name}' is downloaded and ready to use")
                self.download_button.setVisible(False)
                self.load_coqui_speakers(model_name)
            else:
                size = "Unknown"
                if hasattr(self.coqui_service, 'get_model_download_size'):
                    size = self.coqui_service.get_model_download_size(
                        model_name)
                self.model_info_label.setText(
                    f"⬇️ Model '{model_name}' needs to be downloaded ({size})")
                self.download_button.setVisible(True)
                self.speaker_combo.clear()
                self.speaker_combo.addItem("No speakers available")
                self.speaker_combo.setEnabled(False)
            self.selected_coqui_model = model_name
        except Exception as e:
            logger.error(f"Failed to handle Coqui model change: {e}")
            self.model_info_label.setText(f"Error: {str(e)}")
            self.speaker_combo.clear()
            self.speaker_combo.addItem("No speakers available")
            self.speaker_combo.setEnabled(False)

    def load_coqui_speakers(self, model_name: str):
        """Load available speakers for the selected model with enhanced information (now async via voices_loaded)."""
        # Just trigger model load; speakers will be updated via voices_loaded
        if hasattr(self.coqui_service, 'load_model'):
            self.coqui_service.load_model(model_name)

    def get_speaker_info(self, speaker_name: str, model_name: str) -> dict:
        """Get speaker information for display"""
        try:
            # Try to get speaker info from TTS service
            if hasattr(self.coqui_service, 'get_speaker_info'):
                return self.coqui_service.get_speaker_info(
                    speaker_name, model_name)

            # Fallback to basic info
            speaker_info = {
                'display_name': speaker_name,
                'gender': 'Unknown',
                'accent': 'Unknown',
                'language': 'English'
            }

            # Try to extract info from speaker name
            speaker_lower = speaker_name.lower()

            # Gender detection
            if any(
                gender in speaker_lower for gender in [
                    'male',
                    'm',
                    'man',
                    'guy']):
                speaker_info['gender'] = 'Male'
            elif any(gender in speaker_lower for gender in ['female', 'f', 'woman', 'lady']):
                speaker_info['gender'] = 'Female'

            # Accent detection
            if any(
                accent in speaker_lower for accent in [
                    'american',
                    'us',
                    'usa']):
                speaker_info['accent'] = 'American'
            elif any(accent in speaker_lower for accent in ['british', 'uk', 'england']):
                speaker_info['accent'] = 'British'
            elif any(accent in speaker_lower for accent in ['australian', 'aus']):
                speaker_info['accent'] = 'Australian'

            # Create display name
            if speaker_info['gender'] != 'Unknown' and speaker_info['accent'] != 'Unknown':
                speaker_info[
                    'display_name'] = f"{speaker_info['accent']} {speaker_info['gender']} ({speaker_name})"
            elif speaker_info['gender'] != 'Unknown':
                speaker_info['display_name'] = f"{speaker_info['gender']} Voice ({speaker_name})"
            elif speaker_info['accent'] != 'Unknown':
                speaker_info['display_name'] = f"{speaker_info['accent']} Voice ({speaker_name})"
            else:
                speaker_info['display_name'] = f"Voice {speaker_name}"

            return speaker_info

        except Exception as e:
            logger.error(f"Failed to get speaker info for {speaker_name}: {e}")
            return {
                'display_name': speaker_name,
                'gender': 'Unknown',
                'accent': 'Unknown',
                'language': 'English'}

    def filter_speakers(self, filter_type: str):
        """Filter speakers based on selected criteria"""
        if not hasattr(self, 'all_speakers') or not self.all_speakers:
            return

        self.speaker_combo.clear()

        if filter_type == "All Speakers":
            # Show all speakers
            for speaker in self.all_speakers:
                speaker_info = self.get_speaker_info(
                    speaker, self.selected_coqui_model)
                display_name = speaker_info.get('display_name', speaker)
                self.speaker_combo.addItem(display_name, speaker)
        else:
            # Filter speakers based on criteria
            filtered_speakers = []
            for speaker in self.all_speakers:
                speaker_info = self.get_speaker_info(
                    speaker, self.selected_coqui_model)

                if filter_type == "Male" and speaker_info['gender'] == 'Male':
                    filtered_speakers.append(speaker)
                elif filter_type == "Female" and speaker_info['gender'] == 'Female':
                    filtered_speakers.append(speaker)
                elif filter_type == "English" and speaker_info['language'] == 'English':
                    filtered_speakers.append(speaker)
                elif filter_type == "American" and speaker_info['accent'] == 'American':
                    filtered_speakers.append(speaker)
                elif filter_type == "British" and speaker_info['accent'] == 'British':
                    filtered_speakers.append(speaker)

            # Add filtered speakers
            for speaker in filtered_speakers:
                speaker_info = self.get_speaker_info(
                    speaker, self.selected_coqui_model)
                display_name = speaker_info.get('display_name', speaker)
                self.speaker_combo.addItem(display_name, speaker)

            # Update info label
            if filtered_speakers:
                self.speaker_info_label.setText(
                    f"Found {len(filtered_speakers)} speakers matching '{filter_type}' filter")
            else:
                self.speaker_info_label.setText(
                    f"No speakers found matching '{filter_type}' filter")

        # Enable/disable preview button based on available speakers
        self.preview_speaker_button.setEnabled(self.speaker_combo.count() > 0)

    def on_coqui_speaker_changed(self, speaker_name: str):
        """Handle Coqui TTS speaker selection"""
        # Get the actual speaker name from combo box data
        current_index = self.speaker_combo.currentIndex()
        if current_index >= 0:
            actual_speaker_name = self.speaker_combo.itemData(current_index)
            if actual_speaker_name:
                self.selected_coqui_speaker = actual_speaker_name
            else:
                self.selected_coqui_speaker = speaker_name
        else:
            self.selected_coqui_speaker = speaker_name

        logger.info(
            f"Selected Coqui TTS speaker: {self.selected_coqui_speaker}")

        # Enable preview button if we have a valid speaker
        self.preview_speaker_button.setEnabled(
            bool(self.selected_coqui_speaker))

        # Update speaker info display
        if hasattr(
                self,
                'selected_coqui_model') and self.selected_coqui_speaker:
            speaker_info = self.get_speaker_info(
                self.selected_coqui_speaker, self.selected_coqui_model)
            info_text = f"Selected: {speaker_info['display_name']}\n"
            info_text += f"Gender: {speaker_info['gender']}\n"
            info_text += f"Accent: {speaker_info['accent']}\n"
            info_text += f"Language: {speaker_info['language']}"
            self.speaker_info_label.setText(info_text)

    def preview_selected_speaker(self):
        """Preview the selected speaker's voice"""
        if not hasattr(
                self,
                'selected_coqui_speaker') or not self.selected_coqui_speaker:
            QMessageBox.warning(
                self,
                "No Speaker Selected",
                "Please select a speaker to preview.")
            return

        try:
            # Disable preview button while previewing
            self.preview_speaker_button.setEnabled(False)
            self.preview_speaker_button.setText("Previewing...")

            # Create a simple TTS service for preview
            from pyside_chat.features.voice.tts.tts_service import TTSService
            preview_tts = TTSService.get_instance()

            # Load the model and set the speaker
            if hasattr(
                    self,
                    'selected_coqui_model') and self.selected_coqui_model:
                preview_tts.set_coqui_model(self.selected_coqui_model)
                preview_tts.update_voice(self.selected_coqui_speaker)

            # Generate a short preview text
            preview_text = "Hello, this is a voice preview. How do I sound?"

            # Use non-streaming mode for preview to avoid complexity
            preview_tts.speak_text_non_streaming(preview_text)

            # Re-enable the preview button after a short delay
            QTimer.singleShot(
                3000, lambda: self.preview_speaker_button.setText("🎵 Preview"))
            QTimer.singleShot(
                3000, lambda: self.preview_speaker_button.setEnabled(True))

        except Exception as e:
            logger.error(f"Failed to start voice preview: {e}")
            QMessageBox.critical(
                self,
                "Preview Error",
                f"Failed to start voice preview:\n{str(e)}")
            self.preview_speaker_button.setEnabled(True)
            self.preview_speaker_button.setText("🎵 Preview")

    def download_selected_model(self):
        """Download the selected Coqui TTS model and refresh lists after download"""
        try:
            model_text = self.model_combo.currentText()
            model_name = model_text.replace(
                "✅ ",
                "").replace(
                "⬇️ ",
                "").split(" (")[0]
            if hasattr(self.coqui_service, 'download_model'):
                self.model_info_label.setText(
                    f"Downloading model '{model_name}'...")
                QApplication.processEvents()
                success = self.coqui_service.download_model(model_name)
                if success:
                    self.model_info_label.setText(
                        f"✅ Model '{model_name}' downloaded successfully.")
                    self.refresh_coqui_ui(force_refresh_service=False)  # Refresh models and speakers
                else:
                    self.model_info_label.setText(
                        f"❌ Failed to download model '{model_name}'")
        except Exception as e:
            logger.error(f"Failed to download Coqui model: {e}")
            self.model_info_label.setText(
                f"❌ Error downloading model: {str(e)}")

    def on_silence_threshold_changed(self, value: float):
        """Handle silence threshold value change"""
        if value <= 0.001:
            self.sensitivity_label.setText("(Very Sensitive)")
            self.sensitivity_label.setStyleSheet(
                "color: #ff0000; font-style: italic;")
        elif value <= 0.005:
            self.sensitivity_label.setText("(Sensitive)")
            self.sensitivity_label.setStyleSheet(
                "color: #ff6600; font-style: italic;")
        elif value <= 0.01:
            self.sensitivity_label.setText("(Balanced)")
            self.sensitivity_label.setStyleSheet(
                "color: #00ff00; font-style: italic;")
        elif value <= 0.05:
            self.sensitivity_label.setText("(Less Sensitive)")
            self.sensitivity_label.setStyleSheet(
                "color: #ffff00; font-style: italic;")
        else:
            self.sensitivity_label.setText("(Not Sensitive)")
            self.sensitivity_label.setStyleSheet(
                "color: #00ffff; font-style: italic;")

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
                rms = math.sqrt(
                    sum(sample * sample for sample in samples) / len(samples))
                normalized_rms = rms / 32768.0
                db_level = 20 * \
                    math.log10(normalized_rms) if normalized_rms > 0 else -60

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
        # Get actual speaker ID from combo data if possible
        coqui_speaker = None
        if hasattr(self, "speaker_combo"):
            try:
                idx = self.speaker_combo.currentIndex()
                if idx >= 0:
                    coqui_speaker = self.speaker_combo.itemData(idx)
                if not coqui_speaker:
                    coqui_speaker = self.speaker_combo.currentText()
            except RuntimeError as e:
                logger.warning(f"Failed to get speaker combo data: {e}")
                coqui_speaker = None

        # Safely get widget values with error handling
        def safe_get_text(widget, default=""):
            if hasattr(self, widget) and getattr(self, widget):
                try:
                    return getattr(self, widget).currentText()
                except RuntimeError as e:
                    logger.warning(f"Failed to get text from {widget}: {e}")
                    return default
            return default

        def safe_get_checked(widget, default=False):
            if hasattr(self, widget) and getattr(self, widget):
                try:
                    return getattr(self, widget).isChecked()
                except RuntimeError as e:
                    logger.warning(
                        f"Failed to get checked state from {widget}: {e}")
                    return default
            return default

        def safe_get_value(widget, default=0):
            if hasattr(self, widget) and getattr(self, widget):
                try:
                    return getattr(self, widget).value()
                except RuntimeError as e:
                    logger.warning(f"Failed to get value from {widget}: {e}")
                    return default
            return default

        settings = {
            "stt_api": safe_get_text("stt_api_combo").replace(" (Offline)", ""),
            "tts_api": safe_get_text("tts_api_combo").replace(" (Offline)", ""),
            "tts_voice": safe_get_text("voice_combo"),
            "auto_speak": safe_get_checked("auto_speak_checkbox", True),
            "voice_speed": 1.0,  # TODO: Add speed control
            "recording_timeout": safe_get_value("timeout_spinbox", 10.0),
            "silence_duration": safe_get_value("silence_duration_spinbox", 2.0),
            "silence_threshold": safe_get_value("silence_threshold_spinbox", 0.005),
            "coqui_model": getattr(self, "selected_coqui_model", safe_get_text("model_combo") if hasattr(self, "model_combo") else None),
            "coqui_speaker": coqui_speaker,
            "eq_visualizer": safe_get_text("eq_selector", "None"),
            "tts_streaming": safe_get_checked("streaming_checkbox", True),
            "allow_interruptions": safe_get_checked("allow_interruptions_checkbox", True),
            "interruption_threshold": safe_get_value("interruption_threshold_spinbox", 0.5)
        }
        self.current_settings = settings
        self.settings_changed.emit(settings)
        if self.config_manager:
            self.config_manager.set_voice_settings(settings)
        self.accept()
        if hasattr(self, "coqui_service") and self.selected_coqui_model:
            try:
                # Use the correct method for TTSService
                if hasattr(self.coqui_service, 'load_coqui_model'):
                    self.coqui_service.load_coqui_model(
                        self.selected_coqui_model)
                elif hasattr(self.coqui_service, 'load_model'):
                    self.coqui_service.load_model(self.selected_coqui_model)

                if coqui_speaker and hasattr(
                        self.coqui_service, 'update_voice'):
                    self.coqui_service.update_voice(coqui_speaker)
                elif coqui_speaker and hasattr(self.coqui_service, 'set_voice'):
                    self.coqui_service.set_voice(coqui_speaker)
            except Exception as e:
                logger.warning(f"Failed to load Coqui model or set voice: {e}")

    def get_settings(self) -> dict:
        """Get current settings"""
        return self.current_settings.copy()

    def set_settings(self, settings: dict):
        """Set current settings"""
        self.current_settings = settings.copy()
        # Always refresh Coqui UI when restoring settings
        if "tts_api" in settings and settings["tts_api"] == "Coqui TTS":
            self.refresh_coqui_ui(force_refresh_service=False)

        if "stt_api" in settings and hasattr(self, "stt_api_combo"):
            try:
                index = self.stt_api_combo.findText(settings["stt_api"])
                if index >= 0:
                    self.stt_api_combo.setCurrentIndex(index)
            except RuntimeError as e:
                logger.warning(f"Failed to set stt_api combo: {e}")

        if "tts_api" in settings and hasattr(self, "tts_api_combo"):
            try:
                index = self.tts_api_combo.findText(settings["tts_api"])
                if index >= 0:
                    self.tts_api_combo.setCurrentIndex(index)
            except RuntimeError as e:
                logger.warning(f"Failed to set tts_api combo: {e}")

        if "tts_voice" in settings and hasattr(self, "voice_combo"):
            try:
                index = self.voice_combo.findText(settings["tts_voice"])
                if index >= 0:
                    self.voice_combo.setCurrentIndex(index)
            except RuntimeError as e:
                logger.warning(f"Failed to set tts_voice combo: {e}")

        if "auto_speak" in settings and hasattr(self, "auto_speak_checkbox"):
            try:
                self.auto_speak_checkbox.setChecked(settings["auto_speak"])
            except RuntimeError as e:
                logger.warning(f"Failed to set auto_speak checkbox: {e}")

        if "recording_timeout" in settings:
            self.timeout_spinbox.setValue(int(settings["recording_timeout"]))

        if "silence_duration" in settings:
            self.silence_duration_spinbox.setValue(
                int(settings["silence_duration"]))

        if "silence_threshold" in settings:
            self.silence_threshold_spinbox.setValue(
                float(settings["silence_threshold"]))
            # Update sensitivity indicator
            self.on_silence_threshold_changed(
                float(settings["silence_threshold"]))

        if "tts_streaming" in settings:
            self.streaming_checkbox.setChecked(settings["tts_streaming"])

        if "allow_interruptions" in settings and hasattr(
                self, "allow_interruptions_checkbox"):
            try:
                self.allow_interruptions_checkbox.setChecked(
                    settings["allow_interruptions"])
            except RuntimeError as e:
                logger.warning(
                    f"Failed to set allow_interruptions checkbox: {e}")
                # Widget might be deleted, skip this setting

        if "interruption_threshold" in settings and hasattr(
                self, "interruption_threshold_spinbox"):
            try:
                self.interruption_threshold_spinbox.setValue(
                    float(settings["interruption_threshold"]))
            except RuntimeError as e:
                logger.warning(
                    f"Failed to set interruption_threshold spinbox: {e}")
                # Widget might be deleted, skip this setting

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
                    model_name = model_text.replace(
                        "✅ ", "").replace(
                        "⬇️ ", "").split(" (")[0]
                    if model_name == settings["coqui_model"]:
                        self.model_combo.setCurrentIndex(i)
                        self.on_coqui_model_changed(model_text)
                        break

        if "coqui_speaker" in settings and settings["coqui_speaker"]:
            self.selected_coqui_speaker = settings["coqui_speaker"]
            # Find and select the speaker in the combo box by data (actual
            # speaker ID)
            if hasattr(self, "speaker_combo"):
                found = False
                for i in range(self.speaker_combo.count()):
                    if self.speaker_combo.itemData(
                            i) == settings["coqui_speaker"]:
                        self.speaker_combo.setCurrentIndex(i)
                        found = True
                        break
                if not found:
                    # Fallback: try by display text
                    for i in range(self.speaker_combo.count()):
                        if self.speaker_combo.itemText(
                                i) == settings["coqui_speaker"]:
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

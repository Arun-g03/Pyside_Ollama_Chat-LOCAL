"""
Chat Tab - Extracted from ollama_chat.py
Handles the main chat interface, message display, and user input.
"""

import random
import time
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                               QPushButton, QComboBox, QSlider, QLabel, QSplitter,
                               QScrollArea, QFrame, QMenuBar, QMenu,
                               QFileDialog, QMessageBox, QProgressBar)
from PySide6.QtCore import Signal, Qt, QTimer, QThread, QEvent, QCoreApplication
from PySide6.QtGui import QTextCursor, QFont, QAction

from pyside_chat.ui.spellchecker_widget import SpellCheckerTextEdit
from pyside_chat.ui.Widgets.chat_navigation import ChatNavigationWidget
from pyside_chat.ui.Widgets.voice_settings_dialog import VoiceSettingsDialog
from pyside_chat.utils.message_formatter import MessageFormatter
from pyside_chat.utils.streaming_handler import StreamingHandler
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger
from pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service import VoiceService

logger = CustomLogger.get_logger(__name__)

class ChatTab(QWidget):
    """Main chat interface tab"""
    
    # Signals
    message_sent = Signal(str)  # Emitted when user sends a message
    message_cancelled = Signal()  # Emitted when user cancels a message
    conversation_selected = Signal(str)  # Emitted when a conversation is selected
    conversation_deleted = Signal(str)   # Emitted when a conversation is deleted
    conversation_renamed = Signal(str, str)  # Emitted when a conversation is renamed (old_path, new_path)
    new_conversation_requested = Signal() # Emitted when new conversation is requested
    append_response_signal = Signal(str, object)  # chunk, model_name
    speak_text_requested = Signal(str)  # Emitted when TTS is requested
    
    def __init__(self, parent=None, conversation_manager=None, summarization_service=None):
        super().__init__(parent)
        self.parent = parent
        self.conversation_manager = conversation_manager
        self.summarization_service = summarization_service
        self.current_conversation_file = None

        # Initialize voice service and settings FIRST
        self.voice_service = VoiceService()
        self.voice_settings = {
            "stt_api": "Google Speech Recognition",
            "tts_api": "Google TTS",
            "tts_voice": "en",
            "auto_speak": True,
            "voice_speed": 15,  # Faster default speed
            "recording_timeout": 10.0,
            "silence_duration": 2.0,
            "silence_threshold": 0.005
        }
        
        # Update voice service with initial settings
        self.voice_service.update_settings(self.voice_settings)

        self.setup_ui()
        self.setup_streaming_handler()
        
        # State variables
        self.current_model = None
        self.temperature = 0.7
        self.is_streaming = False
        self.current_response = ""
        self.last_message_type = None  # Track last message type
        self.last_system_message_widget = None  # Track last system message widget (if using custom widgets)
        self.voice_mode = False  # Track voice mode state
        
        self.setup_connections()
        
        # Apply sleek style to all QSplitters in this tab
        self.setStyleSheet("""
            QSplitter::handle {
                background: #232323;
                border: none;
                width: 3px;
                border-radius: 2px;
            }
            QSplitter::handle:hover {
                background: #444444;
            }
        """)
        
    def setup_ui(self):
        """Setup the chat interface UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create horizontal splitter for navigation and chat
        main_splitter = QSplitter(Qt.Horizontal)
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
        chat_splitter = QSplitter(Qt.Vertical)
        chat_layout.addWidget(chat_splitter)
        
        # Chat display area
        self.setup_chat_display(chat_splitter)
        
        # Controls area
        self.setup_controls(chat_splitter)
        
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
        
    def setup_chat_display(self, parent):
        """Setup the chat display area"""
        # Chat display widget
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.4;
            }
        """)

        self.input_layout = QHBoxLayout()
        
        # Scroll area for chat display
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.chat_display)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        parent.addWidget(scroll_area)
        
    def setup_controls(self, parent):
        """Setup the controls area"""
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        
        # Model and settings row
        settings_layout = QHBoxLayout()
        
        # Model selector
        model_label = QLabel("Model:")
        model_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        settings_layout.addWidget(model_label)
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(150)
        self.model_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                selection-background-color: #0078d4;
            }
        """)
        settings_layout.addWidget(self.model_combo)
        
        # Personality selector
        personality_label = QLabel("Personality:")
        personality_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        settings_layout.addWidget(personality_label)
        self.personality_combo = QComboBox()
        self.personality_combo.setMinimumWidth(150)
        self.personality_combo.setToolTip("Select AI personality")
        self.personality_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                selection-background-color: #0078d4;
            }
        """)
        settings_layout.addWidget(self.personality_combo)
        
        # Temperature slider
        temperature_label = QLabel("Temperature:")
        temperature_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        settings_layout.addWidget(temperature_label)
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setRange(0, 20)
        self.temperature_slider.setValue(7)
        self.temperature_slider.setToolTip("Temperature: 0.0 to 2.0")
        self.temperature_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 8px;
                background: #2d2d2d;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #0078d4;
                border: 1px solid #0078d4;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #106ebe;
            }
            QSlider::sub-page:horizontal {
                background: #0078d4;
                border-radius: 4px;
            }
        """)
        settings_layout.addWidget(self.temperature_slider)
        
        self.temperature_label = QLabel("0.7")
        self.temperature_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                min-width: 30px;
            }
        """)
        settings_layout.addWidget(self.temperature_label)
        
        # Connect temperature slider
        self.temperature_slider.valueChanged.connect(self.on_temperature_changed)
        
        settings_layout.addStretch()
        controls_layout.addLayout(settings_layout)
        
        # Input area
        self.input_layout = QHBoxLayout()
        
        # Mode selector dropdown
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Chat", "Voice"])
        self.mode_combo.setMinimumWidth(80)
        self.mode_combo.setToolTip("Select input mode: Chat (text) or Voice")
        self.mode_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                selection-background-color: #0078d4;
            }
        """)
        self.input_layout.addWidget(self.mode_combo)
        
        # Message input
        self.message_input = SpellCheckerTextEdit()
        
        self.message_input.setMinimumHeight(40)  # Allow shrinking but not too small
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        self.input_layout.addWidget(self.message_input)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setMinimumHeight(40)
        self.send_button.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        self.input_layout.addWidget(self.send_button)
        
        # Voice mode button
        self.voice_button = QPushButton("🎤 Start Voice")
        self.voice_button.setMinimumHeight(40)
        self.voice_button.setCheckable(False)  # Not checkable since we handle state manually
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #1d1d1d;
            }
            QPushButton:checked {
                background-color: #d83b01;
                border-color: #d83b01;
            }
            QPushButton:checked:hover {
                background-color: #b02e01;
            }
        """)
        self.input_layout.addWidget(self.voice_button)
        
        # Audio level meter (hidden by default)
        self.audio_level_widget = QWidget()
        audio_level_layout = QVBoxLayout(self.audio_level_widget)
        audio_level_layout.setContentsMargins(0, 0, 0, 0)
        
        # Audio level label
        self.audio_level_label = QLabel("🎤 Ready")
        self.audio_level_label.setAlignment(Qt.AlignCenter)
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
        audio_level_layout.addWidget(self.audio_level_label)
        
        # Audio level meter
        self.audio_level_meter = QProgressBar()
        self.audio_level_meter.setRange(0, 100)
        self.audio_level_meter.setValue(0)
        self.audio_level_meter.setTextVisible(False)
        self.audio_level_meter.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                background-color: #1a1a1a;
                height: 8px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:0.5 #ffff00, stop:1 #ff0000);
                border-radius: 2px;
            }
        """)
        audio_level_layout.addWidget(self.audio_level_meter)
        
        self.audio_level_widget.setVisible(False)
        self.input_layout.addWidget(self.audio_level_widget)
        
        # Voice settings button
        self.voice_settings_button = QPushButton("⚙️")
        self.voice_settings_button.setMinimumHeight(40)
        self.voice_settings_button.setMaximumWidth(50)
        self.voice_settings_button.setToolTip("Voice Settings")
        self.voice_settings_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #1d1d1d;
            }
        """)
        self.input_layout.addWidget(self.voice_settings_button)
        
        # Cancel button (hidden by default)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.setVisible(False)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #d83b01;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b02e01;
            }
            QPushButton:pressed {
                background-color: #8a2301;
            }
        """)
        self.input_layout.addWidget(self.cancel_button)
        
        controls_layout.addLayout(self.input_layout)
        
        parent.addWidget(controls_widget)
        
        # Set initial mode
        self.set_input_mode("Chat")
        self.mode_combo.currentTextChanged.connect(self.set_input_mode)
        
    def setup_streaming_handler(self):
        """Setup the streaming handler"""
        ai_name = self.get_ai_name()
        self.streaming_handler = StreamingHandler(self.chat_display, ai_name)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect send button
        self.send_button.clicked.connect(self.send_message)
        
        # Connect cancel button
        self.cancel_button.clicked.connect(self.cancel_message)
        
        # Connect voice mode button
        self.voice_button.clicked.connect(self.toggle_voice_mode)
        
        # Connect voice settings button
        self.voice_settings_button.clicked.connect(self.open_voice_settings)
        
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
        
        # Connect audio level signal
        self.voice_service.recording_service.audio_level_changed.connect(self.on_audio_level_changed)
        
        # Connect enter key in message input
        self.message_input.installEventFilter(self)
        
        # Connect personality combo
        self.personality_combo.currentTextChanged.connect(self.on_personality_combo_changed)
        
        # Connect navigation widget signals
        if hasattr(self, 'navigation_widget'):
            self.navigation_widget.conversation_selected.connect(self.conversation_selected.emit)
            self.navigation_widget.conversation_deleted.connect(self.conversation_deleted.emit)
            self.navigation_widget.conversation_renamed.connect(self.conversation_renamed.emit)
            self.navigation_widget.new_conversation_requested.connect(self.new_conversation_requested.emit)
        # Thread-safe response appending
        self.append_response_signal.connect(self.append_response_chunk)
        
        # Connect TTS signal
        self.speak_text_requested.connect(self.voice_service.speak_text)
        
    def eventFilter(self, obj, event):
        """Handle key events in message input"""
        if obj == self.message_input and event.type() == QEvent.Type.KeyPress:
            # Enter (Return) sends the message
            if event.key() == Qt.Key.Key_Return and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                self.send_message()
                return True
            # Shift+Enter inserts a new line
            elif event.key() == Qt.Key.Key_Return and (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                cursor = self.message_input.textCursor()
                cursor.insertText("\n")
                return True
        return super().eventFilter(obj, event)
        
    def send_message(self):
        """Send the current message"""
        message = self.message_input.toPlainText().strip()
        if not message:
            return
        
        # Add user message to chat immediately
        self.append_to_chat("You", message)
        
        # Clear input
        self.message_input.clear()
        
        # Start streaming state BEFORE emitting signal
        self.start_streaming()
        
        # Emit signal
        self.message_sent.emit(message)
        
    def cancel_message(self):
        """Cancel the current message"""
        self.stop_streaming()
        self.message_cancelled.emit()
        
    def toggle_voice_mode(self):
        if not self.voice_mode:
            # Start voice input with continuous mode enabled
            self.voice_service.set_continuous_voice_mode(True)
            self.voice_service.start_voice_input()
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_mode = True
            self.enforce_voice_mode_ui()
        else:
            # Stop voice input and disable continuous mode
            self.voice_service.set_continuous_voice_mode(False)
            self.voice_service.stop_voice_input()
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.enforce_voice_mode_ui()
    
    def _reset_voice_button(self):
        """Reset voice button to ready state"""
        self.voice_mode = False
        self.voice_service.set_continuous_voice_mode(False)  # Disable continuous mode
        self.message_input.setVisible(False)
        self.send_button.setVisible(False)
        stt_api = self.voice_settings.get('stt_api', 'Unknown')
        tts_api = self.voice_settings.get('tts_api', 'Unknown')
        self.voice_button.setText("🎤 Start Voice")
        self.voice_button.setToolTip(f"Start voice recording\nSTT: {stt_api}\nTTS: {tts_api}")
        self.voice_button.setEnabled(True)
    
    def on_voice_input_received(self, text: str):
        """Handle voice input converted to text"""
        logger.debug(f"Voice input received: {text}")
        
        # Add the voice input to the chat
        self.append_to_chat("You", f"[Voice] {text}")
        
        # Send the message through the normal flow
        self.message_sent.emit(text)
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.audio_level_widget.setVisible(False)
        else:
            # Keep the button as "Stop Voice" for continuous mode
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_button.setToolTip("Continuous voice mode active - click to stop")
    
    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        logger.error(f"Voice input error: {error}")
        self.append_to_chat("System", f"Voice input error: {error}")
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.audio_level_widget.setVisible(False)
        else:
            # Keep the button as "Stop Voice" for continuous mode
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_button.setToolTip("Continuous voice mode active - click to stop")
        # TODO: Show error message to user
    
    def on_tts_started(self):
        """Handle TTS started"""
        logger.debug("TTS started")
        # TODO: Show TTS indicator in UI
    
    def on_tts_finished(self):
        """Handle TTS finished"""
        logger.debug("TTS finished")
        # TODO: Hide TTS indicator in UI
    
    def on_tts_error(self, error: str):
        """Handle TTS error"""
        logger.error(f"TTS error: {error}")
        # TODO: Show error message to user
    
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
    
    def on_audio_level_changed(self, audio_level: float):
        """Handle audio level changes"""
        try:
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
            logger.error(f"Error updating audio level: {e}")
    
    def on_recording_error(self, error: str):
        """Handle recording error"""
        logger.error(f"Recording error: {error}")
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.audio_level_widget.setVisible(False)
        else:
            # Keep the button as "Stop Voice" for continuous mode
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_button.setToolTip("Continuous voice mode active - click to stop")
        # TODO: Show error message to user
    
    def on_voice_processing_started(self):
        """Handle voice processing started"""
        logger.debug("Voice processing started")
        # Keep button as "Stop Voice" during processing
        self.voice_button.setToolTip("Processing voice input...")
    
    def on_voice_processing_finished(self):
        """Handle voice processing finished"""
        logger.debug("Voice processing finished")
        # Button will be reset to "Start Voice" when voice input is received or error occurs
    
    def speak_ai_response(self, text: str):
        """Trigger TTS for AI response"""
        if self.voice_mode and self.voice_settings.get("auto_speak", True):
            logger.debug(f"Speaking AI response: {text[:50]}...")
            self.speak_text_requested.emit(text)
    
    def open_voice_settings(self):
        """Open the voice settings dialog"""
        dialog = VoiceSettingsDialog(self)
        dialog.set_settings(self.voice_settings)
        
        if dialog.exec():
            # Settings were saved
            new_settings = dialog.get_settings()
            self.voice_settings = new_settings
            logger.debug(f"Voice settings updated: {new_settings}")
            
            # Update voice service with new settings
            self.voice_service.update_settings(new_settings)
        
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        """Add a message to the chat display"""
        tag = "user" if sender == "You" else "ai"
        # If sender is System and message is a personality switch
        if sender == "System" and message.startswith("Switched to "):
            if self.last_message_type == "system_switch":
                # Update the last system switch message instead of appending
                self.streaming_handler.update_last_system_switch(message)
                return
            else:
                self.last_message_type = "system_switch"
        else:
            self.last_message_type = tag
        self.streaming_handler.append_message(sender, message, is_code, tag)
        
    def append_response_chunk(self, chunk: str, model_name: str = None):
        """Append a streaming response chunk"""
        if not self.is_streaming:
            self.start_streaming()
        self.current_response += chunk  # accumulate here only!
        ai_name = self.get_ai_name()
        label = f"{ai_name} ({model_name})" if model_name else ai_name
        self.streaming_handler.update_streaming_message(
            self.current_response, label, None, False, tag="ai"
        )
        
        
    def start_streaming(self):
        """Start streaming state"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            self.send_button.setEnabled(False)
            self.cancel_button.setVisible(True)
            ai_name = self.get_ai_name()
            self.streaming_handler.start_streaming_message(ai_name, tag="ai")
            
            # Double-check that the button is actually disabled
            if self.send_button.isEnabled():
                logger.warning("Send button was not disabled, forcing disable")
                self.send_button.setEnabled(False)
                self.send_button.update()
                from PySide6.QtWidgets import QApplication
                QApplication.processEvents()
        
    def stop_streaming(self):
        """Stop streaming state"""
        logger.debug("[DEBUG] stop_streaming called. is_streaming: %s", self.is_streaming)
        self.is_streaming = False
        self.send_button.setEnabled(True)
        self.cancel_button.setVisible(False)
        logger.debug(f"[DEBUG] stop_streaming: send_button enabled? {self.send_button.isEnabled()} cancel_button visible? {self.cancel_button.isVisible()}")
        self.streaming_handler.finalize_streaming_message()
        self.send_button.update()
        self.cancel_button.update()
        self.chat_display.update()
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        
        # Double-check that the button is actually enabled
        if not self.send_button.isEnabled():
            logger.warning("Send button was not enabled, forcing enable")
            self.send_button.setEnabled(True)
            self.send_button.update()
            QApplication.processEvents()
        
    def on_temperature_changed(self, value):
        """Handle temperature slider change"""
        self.temperature = value / 10.0
        self.temperature_label.setText(f"{self.temperature:.1f}")
        
    def update_model_list(self, models: list):
        """Update the model dropdown"""
        current_model = self.model_combo.currentText()
        self.model_combo.clear()
        self.model_combo.addItem("Auto")
        self.model_combo.addItems(models)
        # Restore previous selection if it still exists
        if current_model and current_model in ["Auto"] + models:
            self.model_combo.setCurrentText(current_model)
        elif models:
            self.model_combo.setCurrentIndex(0)
        self.current_model = self.model_combo.currentText()
    
    def update_personality_list(self, personalities: list):
        """Update the personality dropdown"""
        current_personality = self.personality_combo.currentText()
        
        self.personality_combo.clear()
        self.personality_combo.addItems(personalities)
        logger.debug(f"DEBUG: personalities: {personalities}")
        
        # Set default personality to "Specialists.assistant" if available, otherwise use first available
        if "Specialists.assistant" in personalities:
            self.personality_combo.setCurrentText("Specialists.assistant")
        elif current_personality and current_personality in personalities:
            self.personality_combo.setCurrentText(current_personality)
        elif personalities:
            self.personality_combo.setCurrentIndex(0)
    
    def on_personality_combo_changed(self, personality_name: str):
        """Handle personality selection change in combo box"""
        if personality_name:
            # Emit signal to parent to handle personality change
            if hasattr(self.parent, 'on_personality_changed'):
                self.parent.on_personality_changed(personality_name)
            
    def on_personality_changed(self, personality_name: str):
        """Handle personality change"""
        ai_name = self.get_ai_name()
        self.append_to_chat("System", f"Switched to {personality_name} personality - {ai_name}")
        # Update streaming handler's AI name
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.update_ai_name(ai_name)
        
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.model_combo.currentText()
        
    def get_temperature(self) -> float:
        """Get the current temperature setting"""
        return self.temperature
        
    def get_current_response(self) -> str:
        """Get the current response text"""
        return self.current_response
        
    def get_current_personality(self) -> str:
        """Get the currently selected personality"""
        return self.personality_combo.currentText()
        
    def get_ai_name(self) -> str:
        """Get the AI's name from the current personality"""
        try:
            if hasattr(self.parent, 'personality_model') and self.parent.personality_model:
                return self.parent.personality_model.get_ai_name()
        except Exception as e:
            logger.debug(f"Error getting AI name: {e}", print_to_terminal=True)
        return "Assistant"  # Fallback
        
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.clear()
        # Also clear the streaming handler's internal messages list
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.cleanup()
        
        # List of intro messages to randomly choose from
        intro_messages = [
            "What can I help you with today?",
            "What's on your mind?",
            "What's your top priority right now?",
            "Where would you like to begin?",
            "Ready to dive in?",
            "How can I support you today?",
            "What's one thing I can take off your plate?",
            "Need help figuring something out?",
            "Is there anything you're stuck on?",
            "What are we working on today?",
            "What goal are we aiming for right now?",
            "Let's get started — where should we begin?",
            "What direction are you thinking of taking?",
            "What would be most useful to you right now?",
            "Tell me what you're working on today."
        ]

        
        # Select a random intro message
        selected_message = random.choice(intro_messages)
        intro_message = f"<span style='color:#aaa;font-style:italic;'>{selected_message}</span>"
        self.chat_display.insertHtml(intro_message)
        self.chat_display.insertHtml("<br>")
        
    def save_chat(self):
        """Save the current chat to a file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Chat", "", "HTML Files (*.html);;Text Files (*.txt)"
        )
        if filename:
            try:
                if filename.endswith('.html'):
                    content = self.chat_display.toHtml()
                else:
                    content = self.chat_display.toPlainText()
                    
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                QMessageBox.information(self, "Success", "Chat saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save chat: {str(e)}")
                
    def load_chat(self):
        """Load a chat from a file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Chat", "", "HTML Files (*.html);;Text Files (*.txt)"
        )
        if filename:
            try:
                # Clear the streaming handler before loading new content
                if hasattr(self, 'streaming_handler'):
                    self.streaming_handler.cleanup()
                
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if filename.endswith('.html'):
                    self.chat_display.setHtml(content)
                else:
                    self.chat_display.setPlainText(content)
                    
                QMessageBox.information(self, "Success", "Chat loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load chat: {str(e)}")
    
    def load_conversation(self, filepath: str):
        """Load a conversation from the conversation manager"""
        try:
            if self.conversation_manager:
                conversation, metadata = self.conversation_manager.load_conversation(filepath)
                
                # Clear current chat display
                self.clear_chat()
                # Clear in-memory conversation history
                if hasattr(self.parent, 'conversation_service'):
                    self.parent.conversation_service.clear_conversation()
                
                # Display conversation messages
                for message in conversation:
                    role = message.get("role", "unknown")
                    content = message.get("content", "")
                    
                    if role == "user":
                        self.append_to_chat("You", content)
                    elif role == "assistant":
                        ai_name = self.get_ai_name()
                        self.append_to_chat(ai_name, content)
                    elif role == "system":
                        self.append_to_chat("System", content)
                
                # Update navigation widget
                if hasattr(self, 'navigation_widget'):
                    self.navigation_widget.set_current_conversation(filepath)
                
                # Update current conversation file reference
                self.current_conversation_file = filepath
                
                # Update model and personality if available in metadata
                if metadata.model and metadata.model in [self.model_combo.itemText(i) for i in range(self.model_combo.count())]:
                    self.model_combo.setCurrentText(metadata.model)
                
                if metadata.personality and metadata.personality in [self.personality_combo.itemText(i) for i in range(self.personality_combo.count())]:
                    self.personality_combo.setCurrentText(metadata.personality)
                
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

    def on_message_cancelled(self):
        """Handle message cancellation"""
        self.stop_streaming()
        self.streaming_handler.remove_streaming_placeholder()
    
    def force_enable_send_button(self):
        """Force enable the send button and ensure UI is updated"""
        logger.debug("Force enabling send button")
        self.is_streaming = False
        self.send_button.setEnabled(True)
        self.cancel_button.setVisible(False)
        self.send_button.update()
        self.cancel_button.update()
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        logger.debug(f"Send button enabled: {self.send_button.isEnabled()}")

    def set_input_mode(self, mode):
        if mode == "Chat":
            # If any voice process is running, stop it
            if hasattr(self, "voice_service") and (self.voice_service.is_recording or self.voice_service.is_processing_voice):
                self.voice_service.stop_voice_input()
            # Re-add widgets if not present
            if self.input_layout.indexOf(self.message_input) == -1:
                self.input_layout.insertWidget(1, self.message_input)
            if self.input_layout.indexOf(self.send_button) == -1:
                self.input_layout.insertWidget(2, self.send_button)
            self.message_input.show()
            self.send_button.show()
            self.voice_button.hide()
            self.audio_level_widget.hide()
            self.voice_settings_button.hide()
            self.voice_mode = False
        elif mode == "Voice":
            # Remove chat widgets from layout
            self.input_layout.removeWidget(self.message_input)
            self.input_layout.removeWidget(self.send_button)
            self.message_input.hide()
            self.send_button.hide()
            self.voice_button.show()
            self.audio_level_widget.show()
            self.voice_settings_button.show()
            self.voice_mode = True
        # Force layout update
        self.input_layout.update()
        self.update()
        self.enforce_voice_mode_ui()
   
    def enforce_voice_mode_ui(self):
        """Ensure chat input and send button are always hidden in Voice mode."""
        if self.voice_mode:
            self.message_input.hide()
            self.send_button.hide()
            if hasattr(self.input_layout, 'removeWidget'):
                self.input_layout.removeWidget(self.message_input)
                self.input_layout.removeWidget(self.send_button)
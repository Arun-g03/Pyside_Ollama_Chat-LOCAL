"""
Chat Tab - Extracted from ollama_chat.py
Handles the main chat interface, message display, and user input.
"""

import sys
import os
import time
import json
import logging
from typing import Optional, Dict, Any
from PySide6.QtCore import Qt, Signal, QTimer, QThread, QMutex, QWaitCondition, QEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
    QLabel, QComboBox, QSpinBox, QSplitter, QScrollArea, QMessageBox,
    QProgressBar, QGroupBox, QCheckBox, QSlider, QFrame, QSizePolicy, QDialog
)
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QPalette

# Import EQ visualizer components
from pyside_chat.ui.Audio_visualisers.eq_orchestrator import map_frequency_to_bars
from pyside_chat.ui.Audio_visualisers.eq_widgets.circle_eq_widget import CircleEQWidget
from pyside_chat.ui.Audio_visualisers.eq_widgets.bar_eq_widget import BarEQWidget
from pyside_chat.ui.Audio_visualisers.eq_widgets.circular_net_eq_widget import CircularNetEQWidget
from pyside_chat.ui.Audio_visualisers.eq_widgets.circular_gradient_eq_widget import CircularGradientEQWidget

from pyside_chat.ui.Widgets.chat_navigation import ChatNavigationWidget
from pyside_chat.ui.Widgets.voice_settings_dialog import VoiceSettingsDialog
from pyside_chat.services.conversation_service import ConversationService
from pyside_chat.services.ollama_service import OllamaService
from pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service import VoiceService
from pyside_chat.utils.streaming_handler import StreamingHandler
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

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
    message_edited = Signal(int, str)  # Emitted when a message is edited
    
    def __init__(self, parent=None, conversation_manager=None, summarization_service=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.conversation_manager = conversation_manager
        self.summarization_service = summarization_service
        self.config_manager = config_manager
        self.current_conversation_file = None

        # Initialize voice service and settings FIRST
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

        # Initialize EQ visualizer widgets
        self.eq_widgets = {}
        self.current_eq_widget = None
        self.eq_visualizer_mode = "None"
        self.stored_chat_display = None  # Store the original chat display when switching to EQ

        self.setup_ui()
        
        # State variables
        self.current_model = None
        self.temperature = 0.7
        self.is_streaming = False
        self.current_response = ""
        self.last_message_type = None  # Track last message type
        self.last_system_message_widget = None  # Track last system message widget (if using custom widgets)
        self.voice_mode = False  # Track voice mode state
        
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
        
        # Initialize EQ visualizer widgets
        self.setup_eq_visualizers()
        
        # Setup streaming handler after chat display is created
        self.setup_streaming_handler()
        
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
        
        # Setup connections after all UI components are created
        self.setup_connections()
        
    def setup_eq_visualizers(self):
        """Initialize EQ visualizer widgets"""
        # Create EQ widgets
        self.eq_widgets = {
            "Circle EQ": CircleEQWidget(),
            "Bar EQ": BarEQWidget(),
            "Waveform EQ": CircularNetEQWidget(),  # Use CircularNetEQWidget for Waveform EQ
            "Waveform Gradient": CircularGradientEQWidget(),  # Use CircularGradientEQWidget for Waveform Gradient
            "Waveform Blue Gradient": CircularGradientEQWidget()  # Use CircularGradientEQWidget for Waveform Blue Gradient
        }
        
        # Set initial EQ visualizer mode
        self.eq_visualizer_mode = self.voice_settings.get("eq_visualizer", "None")
        
    def setup_chat_display(self, parent):
        """Setup the chat display area"""
        # Chat display widget
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setLineWrapMode(QTextEdit.WidgetWidth)
        self.chat_display.setMouseTracking(True)  # Enable mouse tracking for hover events
        self.chat_display.mouseMoveEvent = self.chat_display_mouse_move_event
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
        
        # Initialize hover state
        self.hover_message_index = None
        self.edit_button_widget = None
        
    def chat_display_mouse_move_event(self, event):
        """Handle mouse move events to show/hide edit buttons"""
        # Call the original mouseMoveEvent
        super(self.chat_display.__class__, self.chat_display).mouseMoveEvent(event)
        
        # Check if we're hovering over a user message
        cursor = self.chat_display.cursorForPosition(event.pos())
        block = cursor.block()
        block_text = block.text()
        
        # Check if this block contains a user message by looking for "You:" at the start
        if block_text.strip().startswith("You:"):
            # Find the corresponding message index by counting user messages
            if hasattr(self, 'streaming_handler'):
                user_message_count = 0
                for message in self.streaming_handler.get_messages():
                    if message.get('sender') == 'You':
                        user_message_count += 1
                        if block_text.strip() == f"You: {message.get('content', '')}".strip():
                            # Show edit button for this message
                            self.show_edit_button(event.pos(), user_message_count - 1)
                            return
        else:
            # Hide edit button if not hovering over user message
            self.hide_edit_button()
        
    def show_edit_button(self, pos, message_index):
        """Show edit button for a specific message"""
        if hasattr(self, 'edit_button_widget') and self.edit_button_widget:
            self.edit_button_widget.hide()
            self.edit_button_widget.deleteLater()
        
        # Create edit button
        from PySide6.QtWidgets import QPushButton
        self.edit_button_widget = QPushButton("✏️", self.chat_display)
        self.edit_button_widget.setFixedSize(24, 24)
        self.edit_button_widget.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        
        # Position the button near the mouse cursor
        button_pos = self.chat_display.mapFromGlobal(self.mapToGlobal(pos))
        button_pos.setX(button_pos.x() + 10)
        button_pos.setY(button_pos.y() - 12)
        self.edit_button_widget.move(button_pos)
        
        # Connect button click
        self.edit_button_widget.clicked.connect(lambda: self.edit_message_at_index(message_index))
        
        self.edit_button_widget.show()
        self.hover_message_index = message_index
        
    def hide_edit_button(self):
        """Hide the edit button"""
        if hasattr(self, 'edit_button_widget') and self.edit_button_widget:
            self.edit_button_widget.hide()
            self.edit_button_widget.deleteLater()
            self.edit_button_widget = None
        self.hover_message_index = None
        
    def edit_message_at_index(self, message_index):
        """Edit message at specific index"""
        if hasattr(self, 'streaming_handler'):
            messages = self.streaming_handler.get_messages()
            user_messages = [msg for msg in messages if msg.get('sender') == 'You']
            
            if 0 <= message_index < len(user_messages):
                message = user_messages[message_index]
                current_content = message.get('content', '')
                self.show_message_edit_dialog(message_index, current_content)
        
    def setup_controls(self, parent):
        """Setup the controls area"""
        # Controls widget
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(10, 10, 10, 10)

        # Input area
        input_widget = QWidget()
        self.input_layout = QHBoxLayout(input_widget)
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        # --- Restore Input Mode Dropdown ---
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
        self.mode_combo.currentTextChanged.connect(self.set_input_mode)

        # Message input
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(80)
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
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
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

        # Cancel button (initially hidden)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setVisible(False)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #d83b01;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
        """)
        self.input_layout.addWidget(self.cancel_button)

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
        self.input_layout.addWidget(self.voice_button)

        # --- Restore Voice Settings Button ---
        self.voice_settings_button = QPushButton("Settings⚙️")
        self.voice_settings_button.setToolTip("Voice Settings")
        self.voice_settings_button.setFixedSize(32, 32)
        self.voice_settings_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.input_layout.addWidget(self.voice_settings_button)

        # Audio level widget
        self.audio_level_widget = QWidget()
        audio_level_layout = QVBoxLayout(self.audio_level_widget)
        audio_level_layout.setContentsMargins(0, 0, 0, 0)
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
        self.input_layout.addWidget(self.audio_level_widget)

        # Initially hide voice-related widgets
        self.voice_button.hide()
        self.voice_settings_button.hide()
        self.audio_level_widget.hide()

        # Settings area
        settings_widget = QWidget()
        settings_layout = QHBoxLayout(settings_widget)
        settings_layout.setContentsMargins(0, 0, 0, 0)

        # Model selection
        model_group = QGroupBox("Model")
        model_layout = QVBoxLayout(model_group)
        self.model_combo = QComboBox()
        self.model_combo.addItems(["Auto"])
        model_layout.addWidget(self.model_combo)

        # Personality selection
        personality_group = QGroupBox("Personality")
        personality_layout = QVBoxLayout(personality_group)
        self.personality_combo = QComboBox()
        self.personality_combo.addItems(["Specialists.assistant"])
        personality_layout.addWidget(self.personality_combo)

        # Temperature control
        temperature_group = QGroupBox("Temperature")
        temperature_layout = QVBoxLayout(temperature_group)
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(70)  # Default to 0.7
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
        """)
        self.temperature_label = QLabel("0.7")
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
        """)
        temperature_layout.addWidget(self.temperature_slider)
        temperature_layout.addWidget(self.temperature_label)

        # Add groups to settings layout
        settings_layout.addWidget(model_group)
        settings_layout.addWidget(personality_group)
        settings_layout.addWidget(temperature_group)

        # Add widgets to controls layout
        controls_layout.addWidget(input_widget)
        controls_layout.addWidget(settings_widget)

        # Add controls to parent
        parent.addWidget(controls_widget)

        # Install event filter for message input
        self.message_input.installEventFilter(self)

        # Set initial mode
        self.set_input_mode("Chat")
        self.mode_combo.setCurrentText("Chat")
        
    def setup_streaming_handler(self):
        """Setup the streaming handler for chat display"""
        if hasattr(self, 'chat_display'):
            ai_name = self.get_ai_name()
            self.streaming_handler = StreamingHandler(self.chat_display, ai_name)
        
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
        
        # Connect recording service audio level signal to EQ visualizer
        if hasattr(self.voice_service, 'recording_service'):
            self.voice_service.recording_service.audio_level_changed.connect(self.on_audio_level_changed)
        
        # Connect streaming handler signals (only if streaming handler exists)
        if hasattr(self, 'streaming_handler') and self.streaming_handler:
            self.streaming_handler.message_edited.connect(self.on_message_edited)
        
        # Connect navigation widget signals
        if hasattr(self, 'navigation_widget'):
            self.navigation_widget.conversation_selected.connect(self.load_conversation)
            self.navigation_widget.conversation_deleted.connect(self.conversation_deleted.emit)
            self.navigation_widget.conversation_renamed.connect(self.conversation_renamed.emit)
            self.navigation_widget.new_conversation_requested.connect(self.new_conversation_requested.emit)
        
        # Connect voice button
        if hasattr(self, 'voice_button'):
            self.voice_button.clicked.connect(self.toggle_voice_mode)
        
        # Connect voice settings button
        if hasattr(self, 'voice_settings_button'):
            self.voice_settings_button.clicked.connect(self.open_voice_settings)
        
        # Connect send button
        if hasattr(self, 'send_button'):
            self.send_button.clicked.connect(self.send_message)
        
        # Connect cancel button
        if hasattr(self, 'cancel_button'):
            self.cancel_button.clicked.connect(self.cancel_message)
        
        # Connect temperature slider
        if hasattr(self, 'temperature_slider'):
            self.temperature_slider.valueChanged.connect(self.on_temperature_changed)
        
        # Connect personality combo
        if hasattr(self, 'personality_combo'):
            self.personality_combo.currentTextChanged.connect(self.on_personality_combo_changed)
        
        # Connect model combo
        if hasattr(self, 'model_combo'):
            self.model_combo.currentTextChanged.connect(self.on_model_changed)
        
        # Connect message input event filter
        if hasattr(self, 'message_input'):
            self.message_input.installEventFilter(self)
    
    def switch_to_eq_visualizer(self):
        """Switch the chat display to EQ visualizer mode"""
        logger.debug(f"[EQ DEBUG] switch_to_eq_visualizer called - voice_mode: {self.voice_mode}, eq_visualizer_mode: {self.eq_visualizer_mode}")
        
        # Don't switch if already showing an EQ widget
        if self.current_eq_widget and self.current_eq_widget.isVisible():
            logger.debug(f"[EQ DEBUG] EQ widget already visible, skipping switch")
            return
        
        if not self.voice_mode or self.eq_visualizer_mode == "None":
            logger.debug(f"[EQ DEBUG] Skipping EQ switch - voice_mode: {self.voice_mode}, eq_visualizer_mode: {self.eq_visualizer_mode}")
            return
            
        # Get the current EQ widget
        if self.eq_visualizer_mode in self.eq_widgets:
            self.current_eq_widget = self.eq_widgets[self.eq_visualizer_mode]
            logger.debug(f"[EQ DEBUG] Selected EQ widget: {self.eq_visualizer_mode}")
            
            # Find the scroll area containing the chat display
            scroll_area = self.chat_display.parent()
            logger.debug(f"[EQ DEBUG] Chat display parent found: {scroll_area is not None}, type: {type(scroll_area)}")
            
            if scroll_area:
                # Check if parent is a QScrollArea
                from PySide6.QtWidgets import QScrollArea
                if isinstance(scroll_area, QScrollArea):
                    logger.debug(f"[EQ DEBUG] Parent is QScrollArea, current widget: {scroll_area.widget()}")
                    
                    # Store the current widget (chat display) and replace with EQ widget
                    current_widget = scroll_area.widget()
                    scroll_area.takeWidget()
                    logger.debug(f"[EQ DEBUG] Removed current widget from scroll area")
                    
                    scroll_area.setWidget(self.current_eq_widget)
                    logger.debug(f"[EQ DEBUG] Set EQ widget in scroll area")
                    
                    # Store the chat display for later restoration
                    self.stored_chat_display = current_widget
                else:
                    logger.debug(f"[EQ DEBUG] Parent is not QScrollArea, it's: {type(scroll_area)}")
                    # Try to find the scroll area in the parent hierarchy
                    current_parent = scroll_area
                    scroll_area = None
                    while current_parent:
                        if isinstance(current_parent, QScrollArea):
                            scroll_area = current_parent
                            break
                        current_parent = current_parent.parent()
                    
                    if scroll_area:
                        logger.debug(f"[EQ DEBUG] Found QScrollArea in parent hierarchy, current widget: {scroll_area.widget()}")
                        scroll_area.takeWidget()
                        logger.debug(f"[EQ DEBUG] Removed current widget from scroll area")
                        
                        scroll_area.setWidget(self.current_eq_widget)
                        logger.debug(f"[EQ DEBUG] Set EQ widget in scroll area")
                        
                        # Store the chat display for later restoration
                        self.stored_chat_display = scroll_area.widget()
                    else:
                        logger.error(f"[EQ DEBUG] Could not find QScrollArea in parent hierarchy")
                        return
                
                self.current_eq_widget.show()
                self.chat_display.hide()
                logger.debug(f"[EQ DEBUG] Showed EQ widget, hid chat display")
                
                # Ensure chat display is completely hidden and doesn't interfere
                self.chat_display.setVisible(False)
                self.chat_display.setEnabled(False)
                logger.debug(f"[EQ DEBUG] Disabled chat display completely")
                
                # Force layout update
                scroll_area.updateGeometry()
                scroll_area.update()
                self.current_eq_widget.updateGeometry()
                self.current_eq_widget.update()
                logger.debug(f"[EQ DEBUG] Forced layout updates")
                
                # Start the EQ animation
                try:
                    self.current_eq_widget.start_animation()
                    logger.debug(f"[EQ DEBUG] Started EQ animation")
                except Exception as e:
                    logger.error(f"[EQ DEBUG] Error starting EQ animation: {e}")
                
                # Force a complete repaint
                from PySide6.QtWidgets import QApplication
                QApplication.processEvents()
                logger.debug(f"[EQ DEBUG] Processed events")
                
                logger.debug(f"[EQ DEBUG] Successfully switched to EQ visualizer: {self.eq_visualizer_mode}")
            else:
                logger.error(f"[EQ DEBUG] No scroll area found for chat display")
        else:
            logger.error(f"[EQ DEBUG] EQ visualizer mode '{self.eq_visualizer_mode}' not found in available widgets: {list(self.eq_widgets.keys())}")
    
    def switch_to_chat_display(self):
        """Switch back to chat display mode"""
        logger.debug(f"[EQ DEBUG] switch_to_chat_display called - current_eq_widget: {self.current_eq_widget is not None}")
        
        # Don't switch if already showing chat display
        if self.chat_display and self.chat_display.isVisible():
            logger.debug(f"[EQ DEBUG] Chat display already visible, skipping switch")
            return
        
        if self.current_eq_widget:
            logger.debug(f"[EQ DEBUG] Stopping EQ animation")
            # Stop the EQ animation
            try:
                self.current_eq_widget.stop_animation()
                logger.debug(f"[EQ DEBUG] EQ animation stopped")
            except Exception as e:
                logger.error(f"[EQ DEBUG] Error stopping EQ animation: {e}")
            
            # Find the scroll area and restore the chat display
            scroll_area = self.current_eq_widget.parent()
            logger.debug(f"[EQ DEBUG] EQ widget parent found: {scroll_area is not None}, type: {type(scroll_area)}")
            
            if scroll_area:
                # Check if parent is a QScrollArea
                from PySide6.QtWidgets import QScrollArea
                if isinstance(scroll_area, QScrollArea):
                    logger.debug(f"[EQ DEBUG] Parent is QScrollArea, current widget: {scroll_area.widget()}")
                    
                    scroll_area.takeWidget()
                    logger.debug(f"[EQ DEBUG] Removed EQ widget from scroll area")
                    
                    # Restore the stored chat display
                    if hasattr(self, 'stored_chat_display') and self.stored_chat_display:
                        scroll_area.setWidget(self.stored_chat_display)
                        logger.debug(f"[EQ DEBUG] Restored stored chat display in scroll area")
                        # Update the chat_display reference
                        self.chat_display = self.stored_chat_display
                        self.stored_chat_display = None
                    else:
                        scroll_area.setWidget(self.chat_display)
                        logger.debug(f"[EQ DEBUG] Set chat display in scroll area")
                else:
                    logger.debug(f"[EQ DEBUG] Parent is not QScrollArea, it's: {type(scroll_area)}")
                    # Try to find the scroll area in the parent hierarchy
                    current_parent = scroll_area
                    scroll_area = None
                    while current_parent:
                        if isinstance(current_parent, QScrollArea):
                            scroll_area = current_parent
                            break
                        current_parent = current_parent.parent()
                    
                    if scroll_area:
                        logger.debug(f"[EQ DEBUG] Found QScrollArea in parent hierarchy, current widget: {scroll_area.widget()}")
                        scroll_area.takeWidget()
                        logger.debug(f"[EQ DEBUG] Removed EQ widget from scroll area")
                        
                        # Restore the stored chat display
                        if hasattr(self, 'stored_chat_display') and self.stored_chat_display:
                            scroll_area.setWidget(self.stored_chat_display)
                            logger.debug(f"[EQ DEBUG] Restored stored chat display in scroll area")
                            # Update the chat_display reference
                            self.chat_display = self.stored_chat_display
                            self.stored_chat_display = None
                        else:
                            scroll_area.setWidget(self.chat_display)
                            logger.debug(f"[EQ DEBUG] Set chat display in scroll area")
                    else:
                        logger.error(f"[EQ DEBUG] Could not find QScrollArea in parent hierarchy")
                        return
                
                self.current_eq_widget.hide()
                self.chat_display.show()
                self.chat_display.setVisible(True)
                self.chat_display.setEnabled(True)
                logger.debug(f"[EQ DEBUG] Hid EQ widget, showed and enabled chat display")
                
                # Force layout update
                scroll_area.updateGeometry()
                scroll_area.update()
                self.chat_display.updateGeometry()
                self.chat_display.update()
                logger.debug(f"[EQ DEBUG] Forced layout updates")
                
                # Force a complete repaint
                from PySide6.QtWidgets import QApplication
                QApplication.processEvents()
                logger.debug(f"[EQ DEBUG] Processed events")
                
                self.current_eq_widget = None
                logger.debug("[EQ DEBUG] Successfully switched back to chat display")
            else:
                logger.error(f"[EQ DEBUG] No scroll area found for EQ widget")
        else:
            logger.debug(f"[EQ DEBUG] No current EQ widget to switch from")
    
    def update_eq_visualizer(self, audio_level):
        """Update the EQ visualizer with audio level data."""
        logger.debug(f"[EQ DEBUG] update_eq_visualizer called with audio_level: {audio_level:.4f}")
        logger.debug(f"[EQ DEBUG] current_eq_widget exists: {self.current_eq_widget is not None}")
        logger.debug(f"[EQ DEBUG] current_eq_widget type: {type(self.current_eq_widget)}")
        
        if not self.current_eq_widget or not hasattr(self.current_eq_widget, 'set_eq_bars'):
            logger.debug("[EQ DEBUG] No EQ visualizer available")
            return
            
        try:
            logger.debug(f"[EQ DEBUG] Received audio level: {audio_level:.4f}")
            
            # Process audio level based on source (TTS vs microphone)
            tts_playing = hasattr(self.voice_service, 'is_playing_tts') and self.voice_service.is_playing_tts
            if tts_playing:
                # TTS audio levels need more amplification for better EQ response
                base_level = audio_level * 15.0  # Higher amplification for TTS
                logger.debug(f"[EQ DEBUG] TTS playing - base level: {base_level:.4f}")
            else:
                # Microphone levels need more amplification
                base_level = audio_level * 20.0  # Much higher amplification for microphone
                logger.debug(f"[EQ DEBUG] Microphone input - base level: {base_level:.4f}")
            
            # Generate frequency-based bar values for 24 bars (matching BarEQWidget default)
            bar_values = []
            num_bars = 24  # Match BarEQWidget.DEFAULT_NUM_BARS
            
            # Define frequency bands for 24 bars (20Hz to 20kHz)
            # Each bar represents a specific frequency range
            frequency_bands = [
                (20, 100),      # Bar 0: Sub-bass (20-100 Hz)
                (100, 200),     # Bar 1: Bass (100-200 Hz)
                (200, 300),     # Bar 2: Bass (200-300 Hz)
                (300, 400),     # Bar 3: Bass (300-400 Hz)
                (400, 600),     # Bar 4: Low-mid (400-600 Hz)
                (600, 800),     # Bar 5: Low-mid (600-800 Hz)
                (800, 1000),    # Bar 6: Mid (800-1000 Hz)
                (1000, 1200),   # Bar 7: Mid (1000-1200 Hz)
                (1200, 1500),   # Bar 8: Mid (1200-1500 Hz)
                (1500, 2000),   # Bar 9: Mid (1500-2000 Hz)
                (2000, 2500),   # Bar 10: Upper-mid (2000-2500 Hz)
                (2500, 3000),   # Bar 11: Upper-mid (2500-3000 Hz)
                (3000, 4000),   # Bar 12: Presence (3000-4000 Hz)
                (4000, 5000),   # Bar 13: Presence (4000-5000 Hz)
                (5000, 6000),   # Bar 14: Presence (5000-6000 Hz)
                (6000, 8000),   # Bar 15: Brilliance (6000-8000 Hz)
                (8000, 10000),  # Bar 16: Brilliance (8000-10000 Hz)
                (10000, 12000), # Bar 17: High (10000-12000 Hz)
                (12000, 14000), # Bar 18: High (12000-14000 Hz)
                (14000, 16000), # Bar 19: High (14000-16000 Hz)
                (16000, 18000), # Bar 20: Ultra-high (16000-18000 Hz)
                (18000, 19000), # Bar 21: Ultra-high (18000-19000 Hz)
                (19000, 19500), # Bar 22: Air (19000-19500 Hz)
                (19500, 20000)  # Bar 23: Air (19500-20000 Hz)
            ]
            
            for i, (low_freq, high_freq) in enumerate(frequency_bands):
                # Calculate frequency response based on audio level
                # Different frequency bands respond differently to the same audio level
                
                # Base response from audio level
                base_response = base_level
                
                # Create more dynamic frequency-specific responses
                # Each bar should respond differently to create realistic EQ movement
                if i < 6:  # Bass frequencies (0-5) - 25% of bars
                    # Bass bars respond more to lower frequencies
                    freq_multiplier = 1.5 + (i * 0.1)  # Increasing response for bass
                elif i < 12:  # Low-mid frequencies (6-11) - 25% of bars
                    # Low-mid bars have moderate response
                    freq_multiplier = 1.0 + ((i - 6) * 0.05)
                elif i < 18:  # Mid frequencies (12-17) - 25% of bars
                    # Mid bars have varied response
                    freq_multiplier = 0.8 + ((i - 12) * 0.1)
                else:  # Upper frequencies (18-23) - 25% of bars
                    # Upper bars are more sensitive to changes
                    freq_multiplier = 1.2 + ((i - 18) * 0.15)
                
                # Add frequency-specific variations based on audio level
                # Higher audio levels should affect different frequency ranges differently
                if audio_level > 0.1:  # High audio level
                    if i < 6:  # Bass gets more prominent
                        freq_multiplier *= 1.3
                    elif i > 18:  # High frequencies get more sensitive
                        freq_multiplier *= 1.4
                elif audio_level > 0.05:  # Medium audio level
                    if i >= 6 and i < 18:  # Mid frequencies get more response
                        freq_multiplier *= 1.2
                
                # Calculate final value for this frequency band
                value = base_response * freq_multiplier
                
                # Add some randomness for natural movement
                import random
                value *= (0.7 + 0.6 * random.random())  # More variation
                
                # Clamp to valid range (0.1 to 1.0 as expected by BarEQWidget)
                value = max(0.1, min(1.0, value))
                bar_values.append(value)
            
            logger.debug(f"[EQ DEBUG] Generated {len(bar_values)} bar values: {[f'{v:.3f}' for v in bar_values]}")
            
            # Update the EQ visualizer
            self.current_eq_widget.set_eq_bars(bar_values)
            logger.debug(f"[EQ DEBUG] Sent {len(bar_values)} bar values to EQ widget")
            
        except Exception as e:
            logger.error(f"[EQ DEBUG] Error updating EQ visualizer: {e}")
            import traceback
            logger.error(f"[EQ DEBUG] EQ error traceback: {traceback.format_exc()}")
    
    def on_audio_level_changed(self, audio_level: float):
        """Handle audio level changes for EQ visualizer"""
        logger.debug(f"[EQ DEBUG] on_audio_level_changed called - audio_level: {audio_level:.4f}, voice_mode: {self.voice_mode}, eq_mode: {self.eq_visualizer_mode}")
        
        # Update EQ visualizer if in voice mode with EQ enabled
        if self.voice_mode and self.eq_visualizer_mode != "None":
            logger.debug(f"[EQ DEBUG] Calling update_eq_visualizer")
            self.update_eq_visualizer(audio_level)
        else:
            logger.debug(f"[EQ DEBUG] Skipping EQ update - voice_mode: {self.voice_mode}, eq_mode: {self.eq_visualizer_mode}")
        
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
        
    def on_temperature_changed(self, value):
        """Handle temperature slider value change"""
        self.temperature = value / 100.0  # Convert from 0-100 to 0.0-1.0
        logger.debug(f"Temperature changed to: {self.temperature}")
        
    def update_model_list(self, models: list):
        """Update the model combo box with available models"""
        if hasattr(self, 'model_combo'):
            current_model = self.model_combo.currentText()
            self.model_combo.clear()
            self.model_combo.addItems(models)
            # Try to restore the previously selected model
            if current_model and current_model in models:
                self.model_combo.setCurrentText(current_model)
            elif models:
                self.model_combo.setCurrentIndex(0)
    
    def update_personality_list(self, personalities: list):
        """Update the personality combo box with available personalities"""
        if hasattr(self, 'personality_combo'):
            current_personality = self.personality_combo.currentText()
            self.personality_combo.clear()
            self.personality_combo.addItems(personalities)
            # Try to restore the previously selected personality
            if current_personality and current_personality in personalities:
                self.personality_combo.setCurrentText(current_personality)
            elif personalities:
                self.personality_combo.setCurrentIndex(0)
    
    def on_personality_combo_changed(self, personality_name: str):
        """Handle personality combo box change"""
        if personality_name:
            self.on_personality_changed(personality_name)
            
    def on_personality_changed(self, personality_name: str):
        """Handle personality change"""
        logger.debug(f"Personality changed to: {personality_name}")
        # Emit signal or handle personality change logic here
    
    def on_model_changed(self, model_name: str):
        """Handle model combo box change"""
        logger.debug(f"Model changed to: {model_name}")
        # Handle model change logic here
        
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.model_combo.currentText() if hasattr(self, 'model_combo') else ""
        
    def get_temperature(self) -> float:
        """Get the current temperature setting"""
        return self.temperature
        
    def get_current_response(self) -> str:
        """Get the current streaming response"""
        return self.current_response
        
    def get_current_personality(self) -> str:
        """Get the currently selected personality"""
        return self.personality_combo.currentText() if hasattr(self, 'personality_combo') else ""
        
    def get_ai_name(self) -> str:
        """Get the AI name based on current personality"""
        personality = self.get_current_personality()
        if personality:
            return personality
        return "AI"
        
    def clear_chat(self):
        """Clear the chat display"""
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.clear_chat()
        if hasattr(self, 'chat_display'):
            self.chat_display.clear()
        
    def save_chat(self):
        """Save the current chat"""
        if not self.current_conversation_file:
            # Create new conversation
            from PySide6.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Chat", "", "JSON Files (*.json)"
            )
            if file_path:
                self.current_conversation_file = file_path
                self.set_current_conversation_file(file_path)
        
        if self.current_conversation_file:
            try:
                # Get chat content from streaming handler
                if hasattr(self, 'streaming_handler'):
                    messages = self.streaming_handler.get_messages()
                    
                    # Save to file
                    with open(self.current_conversation_file, 'w', encoding='utf-8') as f:
                        json.dump(messages, f, indent=2, ensure_ascii=False)
                    
                    logger.debug(f"Chat saved to: {self.current_conversation_file}")
                    
                    # Refresh navigation
                    self.refresh_navigation()
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save chat: {str(e)}")
                
    def load_chat(self):
        """Load a chat from file"""
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Chat", "", "JSON Files (*.json)"
        )
        if file_path:
            self.load_conversation(file_path)
    
    def load_conversation(self, filepath: str):
        """Load a conversation from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Clear current chat
            self.clear_chat()
            
            # Load messages
            if hasattr(self, 'streaming_handler'):
                for message in data:
                    sender = message.get('sender', 'Unknown')
                    content = message.get('content', '')
                    is_code = message.get('is_code', False)
                    tag = message.get('tag', 'user' if sender == 'You' else 'ai')
                    
                    self.streaming_handler.append_message(sender, content, is_code, tag)
            
            # Set current conversation file
            self.current_conversation_file = filepath
            self.set_current_conversation_file(filepath)
            
            # Load metadata if available
            try:
                from pyside_chat.models.conversation_metadata import ConversationMetadata
                metadata = ConversationMetadata.from_file(filepath)
                
                # Restore settings from metadata
                if metadata.temperature is not None:
                    self.temperature = metadata.temperature
                    if hasattr(self, 'temperature_slider'):
                        self.temperature_slider.setValue(int(metadata.temperature * 100))
                
                if metadata.model and metadata.model in [self.model_combo.itemText(i) for i in range(self.model_combo.count())]:
                    self.model_combo.setCurrentText(metadata.model)
                
                if metadata.personality and metadata.personality in [self.personality_combo.itemText(i) for i in range(self.personality_combo.count())]:
                    self.personality_combo.setCurrentText(metadata.personality)
                
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

    def on_message_cancelled(self):
        """Handle message cancellation"""
        self.stop_streaming()
        if hasattr(self, 'streaming_handler') and self.streaming_handler:
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
            self.switch_to_chat_display()
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
            
            # Switch to EQ visualizer if enabled
            if self.eq_visualizer_mode != "None":
                self.switch_to_eq_visualizer()
        # Force layout update
        self.input_layout.update()
        self.update()
        self.enforce_voice_mode_ui()

    def open_tts_settings(self):
        from pyside_chat.ui.Widgets.voice_settings_dialog import VoiceSettingsDialog
        dialog = VoiceSettingsDialog(self)
        # Connect the settings_changed signal to a handler that updates the main TTS service
        dialog.settings_changed.connect(self.on_tts_settings_changed)
        dialog.exec()

    def on_tts_settings_changed(self, settings):
        # Update the main TTS service with the selected model and speaker
        model = settings.get("coqui_model")
        speaker = settings.get("coqui_speaker")
        if hasattr(self, "tts_service") and model:
            self.tts_service.load_model(model)
            if speaker:
                self.tts_service.set_voice(speaker)

    def show_message_edit_dialog(self, message_index: int, current_content: str):
        """Show dialog to edit a message"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Message")
        dialog.setModal(True)
        dialog.setMinimumSize(400, 200)
        
        layout = QVBoxLayout(dialog)
        
        # Label
        label = QLabel("Edit your message:")
        layout.addWidget(label)
        
        # Text editor
        text_edit = QTextEdit()
        text_edit.setPlainText(current_content)
        text_edit.setMaximumHeight(100)
        layout.addWidget(text_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_message_edit(dialog, message_index, text_edit.toPlainText()))
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # Style the dialog
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #444;
            }
        """)
        
        dialog.exec()
        
    def save_message_edit(self, dialog, message_index: int, new_content: str):
        """Save the edited message"""
        if new_content.strip():
            if hasattr(self, 'streaming_handler'):
                success = self.streaming_handler.edit_message(message_index, new_content.strip())
                if success:
                    # Emit signal to notify parent about the edit
                    self.message_edited.emit(message_index, new_content.strip())
                    dialog.accept()
                else:
                    from PySide6.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Error", "Failed to edit message.")
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Message cannot be empty.")

    def on_message_edited(self, message_index: int, new_content: str):
        """Handle message edit"""
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.edit_message(message_index, new_content)
    
    def is_eq_visualizer_active(self):
        """Check if EQ visualizer should be active"""
        tts_playing = hasattr(self.voice_service, 'is_playing_tts') and self.voice_service.is_playing_tts
        return ((self.voice_mode or tts_playing) and 
                self.eq_visualizer_mode != "None" and 
                self.current_eq_widget is not None)

    def update_eq_visualizer_mode(self, mode: str):
        """Update the EQ visualizer mode and switch display if needed"""
        logger.debug(f"[EQ DEBUG] update_eq_visualizer_mode called - new_mode: {mode}, current_mode: {self.eq_visualizer_mode}, voice_mode: {self.voice_mode}")
        
        # If we're switching from one EQ mode to another while voice is active, 
        # we need to properly restore the chat display first
        
            
        
        self.eq_visualizer_mode = mode
        
        # Update voice service settings
        self.voice_settings["eq_visualizer"] = mode
        self.voice_service.update_settings(self.voice_settings)
        logger.debug(f"[EQ DEBUG] Updated voice service settings with eq_visualizer: {mode}")
        
        # Switch display based on current voice mode
        if self.voice_mode:
            logger.debug(f"[EQ DEBUG] Voice mode is active, switching display")
            if mode == "None":
                logger.debug(f"[EQ DEBUG] Switching to chat display (mode is None)")
                self.switch_to_chat_display()
            else:
                logger.debug(f"[EQ DEBUG] Switching to EQ visualizer (mode is {mode})")
                self.switch_to_eq_visualizer()
        else:
            logger.debug(f"[EQ DEBUG] Voice mode not active, not switching display")
        
        logger.debug(f"[EQ DEBUG] EQ visualizer mode updated to: {mode}")
    
    def toggle_voice_mode(self):
        logger.debug(f"[EQ DEBUG] toggle_voice_mode called - current voice_mode: {self.voice_mode}, eq_visualizer_mode: {self.eq_visualizer_mode}")
        
        if not self.voice_mode:
            logger.debug(f"[EQ DEBUG] Starting voice mode")
            # Start voice input with continuous mode enabled
            self.voice_service.set_continuous_voice_mode(True)
            self.voice_service.start_voice_input()
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_mode = True
            self.enforce_voice_mode_ui()
            
            # Switch to EQ visualizer if enabled
            if self.eq_visualizer_mode != "None":
                logger.debug(f"[EQ DEBUG] Switching to EQ visualizer on voice start")
                self.switch_to_eq_visualizer()
            else:
                logger.debug(f"[EQ DEBUG] No EQ visualizer enabled, staying with chat display")
        else:
            logger.debug(f"[EQ DEBUG] Stopping voice mode")
            # Stop voice input and disable continuous mode
            self.voice_service.set_continuous_voice_mode(False)
            self.voice_service.stop_voice_input()
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.enforce_voice_mode_ui()
            
            # Switch back to chat display
            logger.debug(f"[EQ DEBUG] Switching back to chat display on voice stop")
            self.switch_to_chat_display()
    
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
        
        # Switch back to chat display
        self.switch_to_chat_display()
    
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
            self.switch_to_chat_display()
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
            self.switch_to_chat_display()
        else:
            # Keep the button as "Stop Voice" for continuous mode
            self.voice_button.setText("🎤 Stop Voice")
            self.voice_button.setToolTip("Continuous voice mode active - click to stop")
        # TODO: Show error message to user
    
    def on_tts_started(self):
        if hasattr(self, 'chat_display'):
            self.chat_display.hide()
    
    def on_tts_finished(self):
        if hasattr(self, 'chat_display'):
            self.chat_display.show()
    
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
    
    def on_recording_error(self, error: str):
        """Handle recording error"""
        logger.error(f"Recording error: {error}")
        
        # Only reset voice button state if not in continuous mode
        if not self.voice_service.is_continuous_voice_mode():
            self.voice_button.setText("🎤 Start Voice")
            self.voice_mode = False
            self.audio_level_widget.setVisible(False)
            self.switch_to_chat_display()
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
    
    def open_voice_settings(self):
        """Open voice settings dialog"""
        dialog = VoiceSettingsDialog(self, self.config_manager)
        dialog.set_settings(self.voice_settings)
        
        # Connect the settings changed signal
        dialog.settings_changed.connect(self.on_voice_settings_changed)
        
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            # Settings were saved
            self.voice_settings = dialog.get_settings()
            self.voice_service.update_settings(self.voice_settings)
            
            # Update EQ visualizer mode if changed
            new_eq_mode = self.voice_settings.get("eq_visualizer", "None")
            if new_eq_mode != self.eq_visualizer_mode:
                self.update_eq_visualizer_mode(new_eq_mode)
    
    def on_voice_settings_changed(self, settings: dict):
        """Handle voice settings changes"""
        # Update local settings
        self.voice_settings.update(settings)
        
        # Update voice service
        self.voice_service.update_settings(settings)
        
        # Update EQ visualizer mode if changed
        new_eq_mode = settings.get("eq_visualizer", "None")
        if new_eq_mode != self.eq_visualizer_mode:
            self.update_eq_visualizer_mode(new_eq_mode)
    
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
    
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        """Add a message to the chat display"""
        # Don't append to chat if EQ visualizer is active
        if self.is_eq_visualizer_active():
            logger.debug(f"[EQ DEBUG] Skipping chat append - EQ visualizer is active")
            return
            
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
        # Don't append response chunks if EQ visualizer is active
        if self.is_eq_visualizer_active():
            logger.debug(f"[EQ DEBUG] Skipping response chunk append - EQ visualizer is active")
            return
            
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

    def enforce_voice_mode_ui(self):
        """Ensure chat input and send button are always hidden in Voice mode."""
        if self.voice_mode:
            self.message_input.hide()
            self.send_button.hide()
            if hasattr(self.input_layout, 'removeWidget'):
                self.input_layout.removeWidget(self.message_input)
                self.input_layout.removeWidget(self.send_button)
    
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

    
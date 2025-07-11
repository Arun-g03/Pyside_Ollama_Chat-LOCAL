"""
Input Controls Component - Message input, send/cancel buttons, and settings
"""

import logging
from typing import Dict, Optional
from PySide6.QtCore import QObject, Signal, QEvent, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
    QLabel, QComboBox, QSpinBox, QGroupBox, QSlider
)

from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class InputControls(QObject):
    """Input Controls component for message input and settings"""
    
    # Signals
    message_sent = Signal(str)  # Emitted when user sends a message
    message_cancelled = Signal()  # Emitted when user cancels a message
    input_mode_changed = Signal(str)  # Emitted when input mode changes
    temperature_changed = Signal(float)  # Emitted when temperature changes
    personality_changed = Signal(str)  # Emitted when personality changes
    model_changed = Signal(str)  # Emitted when model changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # State variables
        self.is_streaming = False
        self.current_response = ""
        self.temperature = 0.7
        
        # Setup UI components
        self.setup_ui_components()
        
        # Setup connections
        self.setup_connections()
        
    def setup_ui_components(self):
        """Setup UI components for input controls"""
        # Input area
        self.input_widget = QWidget()
        self.input_layout = QHBoxLayout(self.input_widget)
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        # Input mode dropdown
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

        # Settings area
        self.settings_widget = QWidget()
        settings_layout = QHBoxLayout(self.settings_widget)
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
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
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
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        # Install event filter for message input
        self.message_input.installEventFilter(self)

        # Set initial mode
        self.set_input_mode("Chat")
        self.mode_combo.setCurrentText("Chat")
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect buttons
        self.send_button.clicked.connect(self.send_message)
        self.cancel_button.clicked.connect(self.cancel_message)
        
        # Connect temperature slider
        self.temperature_slider.valueChanged.connect(self.on_temperature_changed)
        
        # Connect personality combo
        self.personality_combo.currentTextChanged.connect(self.on_personality_combo_changed)
        
        # Connect model combo
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        
        # Connect mode combo
        self.mode_combo.currentTextChanged.connect(self.set_input_mode)
        
    def set_input_mode(self, mode):
        """Set the input mode (Chat or Voice)"""
        logger.debug(f"Setting input mode to: {mode}")
        
        if mode == "Chat":
            # Show text input controls
            self.message_input.show()
            self.send_button.show()
            self.cancel_button.hide()  # Hide cancel button in chat mode initially
            logger.debug("[VOICE DEBUG] Chat mode: showed message input and send button")
        elif mode == "Voice":
            # Hide text input controls completely in voice mode
            self.message_input.hide()
            self.send_button.hide()
            self.cancel_button.hide()
            logger.debug("[VOICE DEBUG] Voice mode: hid message input, send button, and cancel button")
        
        self.input_mode_changed.emit(mode)
    
    def on_temperature_changed(self, value):
        """Handle temperature slider value change"""
        self.temperature = value / 100.0  # Convert from 0-100 to 0.0-1.0
        self.temperature_label.setText(f"{self.temperature:.1f}")
        logger.debug(f"Temperature changed to: {self.temperature}")
        self.temperature_changed.emit(self.temperature)
    
    def on_personality_combo_changed(self, personality_name: str):
        """Handle personality combo box change"""
        if personality_name:
            logger.debug(f"Personality changed to: {personality_name}")
            self.personality_changed.emit(personality_name)
            
    def on_model_changed(self, model_name: str):
        """Handle model combo box change"""
        logger.debug(f"Model changed to: {model_name}")
        self.model_changed.emit(model_name)
    
    def send_message(self):
        """Send the current message"""
        try:
            message = self.message_input.toPlainText().strip()
            if not message:
                return
                
            # Clear input
            self.message_input.clear()
            
            # Start streaming state
            self.start_streaming()
            
            # Emit signal
            self.message_sent.emit(message)
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            # Ensure we're not left in a bad state
            self.stop_streaming()
        
    def cancel_message(self):
        """Cancel the current message"""
        self.stop_streaming()
        self.message_cancelled.emit()
    
    def start_streaming(self):
        """Start streaming state"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            
            # Only manage send/cancel buttons if we're in chat mode
            if self.mode_combo.currentText() == "Chat":
                self.send_button.setEnabled(False)
                self.cancel_button.setVisible(True)
                logger.debug("[VOICE DEBUG] Chat mode streaming: disabled send button, showed cancel button")
            else:
                # In voice mode, buttons should remain hidden
                logger.debug("[VOICE DEBUG] Voice mode streaming: buttons remain hidden")
            
            # Double-check that the button is actually disabled
            if self.mode_combo.currentText() == "Chat" and self.send_button.isEnabled():
                logger.warning("Send button was not disabled, forcing disable")
                self.send_button.setEnabled(False)
                self.send_button.update()
                from PySide6.QtWidgets import QApplication
                QApplication.processEvents()
    
    def stop_streaming(self):
        """Stop streaming state"""
        logger.debug("[DEBUG] stop_streaming called. is_streaming: %s", self.is_streaming)
        self.is_streaming = False
        
        # Only manage send/cancel buttons if we're in chat mode
        if self.mode_combo.currentText() == "Chat":
            self.send_button.setEnabled(True)
            self.cancel_button.setVisible(False)
            logger.debug(f"[DEBUG] stop_streaming: send_button enabled? {self.send_button.isEnabled()} cancel_button visible? {self.cancel_button.isVisible()}")
        else:
            # In voice mode, buttons should remain hidden
            logger.debug("[VOICE DEBUG] Voice mode streaming stopped: buttons remain hidden")
        
        self.send_button.update()
        self.cancel_button.update()
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        
        # Double-check that the button is actually enabled (only in chat mode)
        if self.mode_combo.currentText() == "Chat" and not self.send_button.isEnabled():
            logger.warning("Send button was not enabled, forcing enable")
            self.send_button.setEnabled(True)
            self.send_button.update()
            QApplication.processEvents()
    
    def force_enable_send_button(self):
        """Force enable the send button and ensure UI is updated"""
        logger.debug("Force enabling send button")
        self.is_streaming = False
        
        # Only manage send/cancel buttons if we're in chat mode
        if self.mode_combo.currentText() == "Chat":
            self.send_button.setEnabled(True)
            self.cancel_button.setVisible(False)
            logger.debug("[VOICE DEBUG] Chat mode: enabled send button, hid cancel button")
        else:
            # In voice mode, buttons should remain hidden
            logger.debug("[VOICE DEBUG] Voice mode: buttons remain hidden")
        
        self.send_button.update()
        self.cancel_button.update()
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        logger.debug(f"Send button enabled: {self.send_button.isEnabled()}")
    
    def update_model_list(self, models: list):
        """Update the model combo box with available models, always including 'Auto' as the first option"""
        current_model = self.model_combo.currentText()
        self.model_combo.clear()
        all_models = ["Auto"] + [m for m in models if m != "Auto"]
        self.model_combo.addItems(all_models)
        # Try to restore the previously selected model
        if current_model and current_model in all_models:
            self.model_combo.setCurrentText(current_model)
        elif all_models:
            self.model_combo.setCurrentIndex(0)
    
    def update_personality_list(self, personalities: list):
        """Update the personality combo box with available personalities"""
        current_personality = self.personality_combo.currentText()
        self.personality_combo.clear()
        self.personality_combo.addItems(personalities)
        # Try to restore the previously selected personality
        if current_personality and current_personality in personalities:
            self.personality_combo.setCurrentText(current_personality)
        elif personalities:
            self.personality_combo.setCurrentIndex(0)
    
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.model_combo.currentText()
        
    def get_temperature(self) -> float:
        """Get the current temperature setting"""
        return self.temperature
        
    def get_current_response(self) -> str:
        """Get the current streaming response"""
        return self.current_response
        
    def get_current_personality(self) -> str:
        """Get the currently selected personality"""
        return self.personality_combo.currentText()
    
    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'input_widget': self.input_widget,
            'settings_widget': self.settings_widget,
            'message_input': self.message_input,
            'send_button': self.send_button,
            'cancel_button': self.cancel_button,
            'mode_combo': self.mode_combo,
            'model_combo': self.model_combo,
            'personality_combo': self.personality_combo,
            'temperature_slider': self.temperature_slider
        }
    
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
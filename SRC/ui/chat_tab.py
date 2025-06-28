"""
Chat Tab - Extracted from ollama_chat.py
Handles the main chat interface, message display, and user input.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                               QPushButton, QComboBox, QSlider, QLabel, QSplitter,
                               QScrollArea, QFrame, QMenuBar, QMenu,
                               QFileDialog, QMessageBox, QProgressBar)
from PySide6.QtCore import Signal, Qt, QTimer, QThread, QEvent
from PySide6.QtGui import QTextCursor, QFont, QAction

from SRC.ui.spellchecker_widget import SpellCheckerTextEdit
from SRC.utils.message_formatter import MessageFormatter
from SRC.utils.streaming_handler import StreamingHandler


class ChatTab(QWidget):
    """Main chat interface tab"""
    
    # Signals
    message_sent = Signal(str)  # Emitted when user sends a message
    message_cancelled = Signal()  # Emitted when user cancels a message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.setup_streaming_handler()
        self.setup_connections()
        
        # State variables
        self.current_model = None
        self.temperature = 0.7
        self.is_streaming = False
        self.current_response = ""
        
        
    def setup_ui(self):
        """Setup the chat interface UI"""
        layout = QVBoxLayout(self)
        
        # Create splitter for chat and controls
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)
        
        # Chat display area
        self.setup_chat_display(splitter)
        
        # Controls area
        self.setup_controls(splitter)
        
        # Set splitter proportions
        splitter.setSizes([600, 200])
        
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
        settings_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(150)
        settings_layout.addWidget(self.model_combo)
        
        # Personality selector
        settings_layout.addWidget(QLabel("Personality:"))
        self.personality_combo = QComboBox()
        self.personality_combo.setMinimumWidth(150)
        self.personality_combo.setToolTip("Select AI personality")
        settings_layout.addWidget(self.personality_combo)
        
        # Temperature slider
        settings_layout.addWidget(QLabel("Temperature:"))
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setRange(0, 20)
        self.temperature_slider.setValue(7)
        self.temperature_slider.setToolTip("Temperature: 0.0 to 2.0")
        settings_layout.addWidget(self.temperature_slider)
        
        self.temperature_label = QLabel("0.7")
        settings_layout.addWidget(self.temperature_label)
        
        # Connect temperature slider
        self.temperature_slider.valueChanged.connect(self.on_temperature_changed)
        
        settings_layout.addStretch()
        controls_layout.addLayout(settings_layout)
        
        # Input area
        input_layout = QHBoxLayout()
        
        # Message input
        self.message_input = SpellCheckerTextEdit()
        self.message_input.setMaximumHeight(100)
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
        input_layout.addWidget(self.message_input)
        
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
        input_layout.addWidget(self.send_button)
        
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
        input_layout.addWidget(self.cancel_button)
        
        controls_layout.addLayout(input_layout)
        
        parent.addWidget(controls_widget)
        
    def setup_streaming_handler(self):
        """Setup the streaming response handler"""
        self.streaming_handler = StreamingHandler(self.chat_display)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect send button
        self.send_button.clicked.connect(self.send_message)
        
        # Connect cancel button
        self.cancel_button.clicked.connect(self.cancel_message)
        
        # Connect enter key in message input
        self.message_input.installEventFilter(self)
        
        # Connect personality combo
        self.personality_combo.currentTextChanged.connect(self.on_personality_combo_changed)
        
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
        
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        """Add a message to the chat display"""
        tag = "user" if sender == "You" else "ai"
        self.streaming_handler.append_message(sender, message, is_code, tag)
        
    def append_response_chunk(self, chunk: str):
        """Append a streaming response chunk"""
        if not self.is_streaming:
            self.start_streaming()
        self.current_response += chunk
        self.streaming_handler.update_streaming_message(
            self.current_response, "Assistant", None, False, tag="ai"
        )
        
    def start_streaming(self):
        """Start streaming state"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            self.send_button.setEnabled(False)
            self.cancel_button.setVisible(True)
            self.streaming_handler.start_streaming_message("Assistant", tag="ai")
        
    def stop_streaming(self):
        """Stop streaming state"""
        if self.is_streaming:  # Only change state if currently streaming
            self.is_streaming = False
            self.send_button.setEnabled(True)
            self.cancel_button.setVisible(False)
            self.streaming_handler.finalize_streaming_message()
        
    def on_temperature_changed(self, value):
        """Handle temperature slider change"""
        self.temperature = value / 10.0
        self.temperature_label.setText(f"{self.temperature:.1f}")
        
    def update_model_list(self, models: list):
        """Update the model dropdown"""
        current_model = self.model_combo.currentText()
        
        self.model_combo.clear()
        self.model_combo.addItems(models)
        
        # Restore previous selection if it still exists
        if current_model and current_model in models:
            self.model_combo.setCurrentText(current_model)
        elif models:
            self.model_combo.setCurrentIndex(0)
            
        self.current_model = self.model_combo.currentText()
    
    def update_personality_list(self, personalities: list):
        """Update the personality dropdown"""
        current_personality = self.personality_combo.currentText()
        
        self.personality_combo.clear()
        self.personality_combo.addItems(personalities)
        
        # Restore previous selection if it still exists
        if current_personality and current_personality in personalities:
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
        # Add system message about personality change
        self.append_to_chat("System", f"Switched to {personality_name} personality")
        
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
        
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.clear()
        
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
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if filename.endswith('.html'):
                    self.chat_display.setHtml(content)
                else:
                    self.chat_display.setPlainText(content)
                    
                QMessageBox.information(self, "Success", "Chat loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load chat: {str(e)}")

    def on_message_cancelled(self):
        """Handle message cancellation"""
        self.stop_streaming()
        self.streaming_handler.remove_streaming_placeholder()

    def on_message_cancelled(self):
        """Handle message cancellation"""
        self.stop_streaming() 
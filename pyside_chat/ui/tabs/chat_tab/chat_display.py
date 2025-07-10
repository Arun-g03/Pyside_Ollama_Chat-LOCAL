"""
Chat Display Component - Message display and editing functionality
"""

import logging
from typing import Optional
from PySide6.QtCore import QObject, Signal, QEvent, Qt
from PySide6.QtWidgets import QTextEdit, QScrollArea, QPushButton
from PySide6.QtGui import QTextCursor

from pyside_chat.core.utils.streaming_handler import StreamingHandler
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class ChatDisplay(QObject):
    """Chat Display component for message display and editing"""
    
    # Signals
    message_edited = Signal(int, str)  # Emitted when a message is edited
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Setup UI components
        self.setup_ui_components()
        
        # Setup streaming handler
        self.setup_streaming_handler()
        
        # Initialize hover state
        self.hover_message_index = None
        self.edit_button_widget = None
        
    def setup_ui_components(self):
        """Setup UI components for chat display"""
        # Chat display widget
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
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

        # Scroll area for chat display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.chat_display)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
    def setup_streaming_handler(self):
        """Setup the streaming handler for chat display"""
        if hasattr(self, 'chat_display'):
            ai_name = self.get_ai_name()
            self.streaming_handler = StreamingHandler(self.chat_display, ai_name)
            self.streaming_handler.message_edited.connect(self.on_message_edited)
        
    def get_ai_name(self) -> str:
        """Get the AI name - this should be overridden by parent"""
        return "AI"
        
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
        button_pos = self.chat_display.mapFromGlobal(self.chat_display.mapToGlobal(pos))
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
    
    def show_message_edit_dialog(self, message_index: int, current_content: str):
        """Show dialog to edit a message"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
        
        dialog = QDialog(self.parent)
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
                    QMessageBox.warning(self.parent, "Error", "Failed to edit message.")
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self.parent, "Error", "Message cannot be empty.")

    def on_message_edited(self, message_index: int, new_content: str):
        """Handle message edit"""
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.edit_message(message_index, new_content)
    
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        """Add a message to the chat display"""
        tag = "user" if sender == "You" else "ai"
        # If sender is System and message is a personality switch
        if sender == "System" and message.startswith("Switched to "):
            if hasattr(self, 'last_message_type') and self.last_message_type == "system_switch":
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
        if not hasattr(self, 'is_streaming'):
            self.is_streaming = False
            
        if not self.is_streaming:
            self.start_streaming()
            
        if not hasattr(self, 'current_response'):
            self.current_response = ""
            
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
            ai_name = self.get_ai_name()
            self.streaming_handler.start_streaming_message(ai_name, tag="ai")
            
    def stop_streaming(self):
        """Stop streaming state"""
        logger.debug("[DEBUG] stop_streaming called. is_streaming: %s", self.is_streaming)
        self.is_streaming = False
        self.streaming_handler.finalize_streaming_message()
        
    def clear_chat(self):
        """Clear the chat display"""
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.clear_chat()
        if hasattr(self, 'chat_display'):
            self.chat_display.clear()
    
    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'chat_display': self.chat_display,
            'scroll_area': self.scroll_area
        }
    
    def get_streaming_handler(self):
        """Get the streaming handler"""
        return self.streaming_handler if hasattr(self, 'streaming_handler') else None 
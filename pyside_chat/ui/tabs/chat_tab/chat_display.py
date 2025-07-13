"""
Chat Display Component - Message display and editing functionality
"""

import logging
from typing import Optional
from PySide6.QtCore import QObject, Signal, QEvent, Qt
from PySide6.QtWidgets import QTextEdit, QScrollArea, QPushButton
from PySide6.QtGui import QTextCursor

from pyside_chat.ui.tabs.chat_tab.chat_renderer import ChatRenderer
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class ChatDisplay(QObject):
    """Chat Display component for message display and editing"""
    
    # Signals
    message_edited = Signal(int, str)  # Emitted when a message is edited
    
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager
        
        # Setup UI components
        self.setup_ui_components()
        
        # Setup chat renderer
        self.setup_chat_renderer()
        
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
        
    def setup_chat_renderer(self):
        """Setup the chat renderer for chat display"""
        if hasattr(self, 'chat_display'):
            ai_name = self.get_ai_name()
            self.chat_renderer = ChatRenderer(self.chat_display, ai_name, config_manager=self.config_manager)
            self.chat_renderer.render_completed.connect(self.on_render_completed)
            self.chat_renderer.render_error.connect(self.on_render_error)
            
            # Setup streaming handler for business logic only (no render callback)
            from pyside_chat.core.utils.streaming_handler import StreamingHandler
            self.streaming_handler = StreamingHandler(render_callback=None, ai_name=ai_name)
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
            if hasattr(self, 'chat_renderer'):
                user_message_count = 0
                for message in self.chat_renderer.get_messages():
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
        if hasattr(self, 'chat_renderer'):
            messages = self.chat_renderer.get_messages()
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
            if hasattr(self, 'chat_renderer'):
                success = self.chat_renderer.edit_message(message_index, new_content.strip())
                if success:
                    # Also update the streaming handler for consistency
                    if hasattr(self, 'streaming_handler'):
                        self.streaming_handler.edit_message(message_index, new_content.strip())
                    # Emit signal to notify parent about the edit
                    self.message_edited.emit(message_index, new_content.strip())
                    dialog.accept()
                else:
                    from pyside_chat.ui.utils.message_utils import show_operation_error
                    show_operation_error("Edit Message", Exception("Failed to edit message"), self.parent)
        else:
            from pyside_chat.ui.utils.message_utils import show_validation_error
            show_validation_error("message", "Message cannot be empty", self.parent)

    def on_render_completed(self):
        """Handle completion of rendering"""
        logger.debug("Chat rendering completed.")
        self.force_update_display()

    def on_render_error(self, error_message: str):
        """Handle rendering errors"""
        logger.error(f"Chat rendering error: {error_message}")
        from pyside_chat.ui.dialogs.error_dialog import show_error_dialog
        show_error_dialog(
            title="Chat Rendering Error",
            message="Failed to render chat display",
            details=error_message,
            parent=self.parent
        )
    
    def on_message_edited(self, message_index: int, new_content: str):
        """Handle message edit from streaming handler"""
        logger.debug(f"Message edited: index={message_index}, content='{new_content[:50]}...'")
        # Sync the edit to the renderer
        if hasattr(self, 'chat_renderer') and self.chat_renderer:
            self.chat_renderer.edit_message(message_index, new_content)
    
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        """Add a message to the chat display"""
        tag = "user" if sender == "You" else "ai"
        # If sender is System and message is a personality switch
        if sender == "System" and message.startswith("Switched to "):
            if hasattr(self, 'last_message_type') and self.last_message_type == "system_switch":
                # Update the last system switch message instead of appending
                self.chat_renderer.update_last_system_switch(message)
                return
            else:
                self.last_message_type = "system_switch"
        else:
            self.last_message_type = tag
        
        # Ensure chat renderer exists
        if not hasattr(self, 'chat_renderer') or not self.chat_renderer:
            logger.error("Chat renderer not available for chat display")
            return
            
        # Add message to renderer and sync with streaming handler
        message_id = self.chat_renderer.add_message(sender, message, is_code, False, tag)
        self.streaming_handler.append_message(sender, message, is_code, tag)
        self.chat_renderer.request_render()
        
    def force_update_display(self):
        """Force an immediate update of the chat display"""
        try:
            # Ensure we're in the main thread
            from PySide6.QtCore import QTimer
            
            # Force immediate update using thread-safe alternative
            QTimer.singleShot(0, self._force_render_display)
                
        except Exception as e:
            logger.error(f"Error in force_update_display: {e}")
    
    def _force_render_display(self):
        """Force render the chat display immediately"""
        try:
            if hasattr(self, 'chat_renderer') and self.chat_renderer:
                # Force immediate render without throttling
                self.chat_renderer.request_render(immediate=True)
                
                # Ensure scroll to bottom
                if hasattr(self, 'chat_display') and self.chat_display:
                    cursor = self.chat_display.textCursor()
                    cursor.movePosition(cursor.End)
                    self.chat_display.setTextCursor(cursor)
                    
                    # Force update using thread-safe alternative
                    self.chat_display.update()
                    
        except Exception as e:
            logger.error(f"Error in _force_render_display: {e}")
    
    def append_response_chunk(self, chunk: str, model_name: str = None):
        """Append a streaming response chunk"""
        if not hasattr(self, 'is_streaming'):
            self.is_streaming = False
            
        if not self.is_streaming:
            self.start_streaming()
            
        if not hasattr(self, 'current_response'):
            self.current_response = ""
            
        # For typewriter effect: accumulate for logging but pass individual chunks to renderer
        self.current_response += chunk  # accumulate here for logging only!
        ai_name = self.get_ai_name()
        label = f"{ai_name} ({model_name})" if model_name else ai_name
        
        # Ensure chat renderer exists
        if hasattr(self, 'chat_renderer') and self.chat_renderer:
            # CRITICAL FIX: Pass the individual chunk for typewriter effect
            # The renderer will append it to the existing content
            self.chat_renderer.update_streaming_message(
                chunk, "ai", None, False, tag="ai", append=True
            )
        else:
            logger.error("Chat renderer not available for response chunk")
        
    def start_streaming(self):
        """Start streaming state"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            ai_name = self.get_ai_name()
            
            # Ensure chat renderer exists
            if hasattr(self, 'chat_renderer') and self.chat_renderer:
                self.chat_renderer.start_streaming_message(ai_name, tag="ai")
            else:
                logger.error("Chat renderer not available for streaming start")
            
    def stop_streaming(self):
        """Stop streaming state"""
        logger.debug("[DEBUG] stop_streaming called. is_streaming: %s", self.is_streaming)
        self.is_streaming = False
        
        # Ensure chat renderer exists
        if hasattr(self, 'chat_renderer') and self.chat_renderer:
            self.chat_renderer.finalize_streaming_message()
        else:
            logger.error("Chat renderer not available for streaming stop")
        
    def clear_chat(self):
        """Clear the chat display"""
        if hasattr(self, 'streaming_handler'):
            self.streaming_handler.clear_messages()
        if hasattr(self, 'chat_renderer'):
            self.chat_renderer.clear_messages()
        if hasattr(self, 'chat_display'):
            self.chat_display.clear()
            # Force update after clearing
            self.force_update_display()
    
    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'chat_display': self.chat_display,
            'scroll_area': self.scroll_area
        }
    
    def get_streaming_handler(self):
        """Get the streaming handler (now returns chat renderer for compatibility)"""
        return self.chat_renderer if hasattr(self, 'chat_renderer') else None 
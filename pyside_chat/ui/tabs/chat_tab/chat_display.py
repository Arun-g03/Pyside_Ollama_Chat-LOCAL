from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.ui.themes.chat_styles import ChatStyles, ChatBubbleWidget
from pyside_chat.ui.themes.system_message_manager import SystemMessageManager
from PySide6.QtWidgets import QSpacerItem, QSizePolicy

"""
Chat Display - Widget-based chat display with custom bubble widgets
"""

import logging
import traceback
import time
from typing import List, Dict, Optional

logger = CustomLogger.get_logger(__name__)

class ChatDisplay(QWidget):
    """Widget-based chat display using custom bubble widgets"""
    
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager
        
        # State variables
        self.conversation_service = None
        self.personality_name = "Assistant"
        
        # Setup UI
        self.setup_ui()
        
        # Setup connections
        self.setup_connections()
        
        logger.debug("[CHAT_DISPLAY] Chat display initialized")
    
    def setup_ui(self):
        """Setup the UI components"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)
        
        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget to hold messages
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(8)
        
        # Add spacer to push messages to top
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.messages_layout.addItem(self.spacer)
        
        self.scroll_area.setWidget(self.messages_widget)
        self.main_layout.addWidget(self.scroll_area)
        
        # Set background color
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QScrollArea {
                border: none;
                background-color: #1e1e1e;
            }
        """)
    
    def setup_connections(self):
        """Setup signal connections"""
        pass  # Will be connected by chat tab
    
    def get_ai_name(self) -> str:
        """Get the current AI name from personality service"""
        try:
            if hasattr(self.parent, 'get_service_manager'):
                service_manager = self.parent.get_service_manager()
                if hasattr(service_manager, 'get_personality_service'):
                    personality_service = service_manager.get_personality_service()
                    if personality_service:
                        return personality_service.get_current_personality_name()
        except Exception as e:
            logger.debug(f"Error getting AI name: {e}")
        
        return self.personality_name
    
    def update_personality_name(self, personality_name: str):
        """Update the personality name"""
        self.personality_name = personality_name
        logger.debug(f"[CHAT_DISPLAY] Updated personality name to: {personality_name}")
    
    def set_conversation_service(self, conversation_service):
        """Set the conversation service reference"""
        logger.debug(f"[CHAT_DISPLAY] Setting conversation service: {conversation_service}")
        self.conversation_service = conversation_service
        
        # Connect to conversation service updates
        if conversation_service:
            conversation_service.conversation_updated.connect(self._on_conversation_updated)
            logger.debug("[CHAT_DISPLAY] Connected to conversation service updates")
            
            # Test: Get messages immediately to verify connection
            try:
                messages = conversation_service.get_messages()
                if messages:
                    self.render_conversation(messages)
                    logger.debug(f"[CHAT_DISPLAY] Rendered {len(messages)} initial messages")
            except Exception as e:
                logger.debug(f"[CHAT_DISPLAY] Error getting initial messages: {e}")
    
    def _on_conversation_updated(self, messages):
        """Handle conversation updates"""
        try:
            logger.debug(f"[CHAT_DISPLAY] Conversation updated with {len(messages)} messages")
            self.render_conversation(messages)
        except Exception as e:
            logger.error(f"Error handling conversation update: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
    
    def render_conversation(self, conversation: List[Dict], scroll_to_bottom: bool = True):
        """Render the entire conversation using custom bubble widgets"""
        try:
            logger.debug(f"[CHAT_DISPLAY] Rendering conversation with {len(conversation)} messages")
            
            # Clear existing messages
            self._clear_messages()
            
            # Add messages
            for i, message in enumerate(conversation):
                self._add_message_widget(message, i)
            
            logger.debug(f"[CHAT_DISPLAY] Finished rendering conversation")
            
            # Scroll to bottom if requested
            if scroll_to_bottom:
                self._scroll_to_bottom()
                
        except Exception as e:
            logger.error(f"Error rendering conversation: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
    
    def _clear_messages(self):
        """Clear all message widgets"""
        # Remove all widgets except the spacer
        while self.messages_layout.count() > 1:
            child = self.messages_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _add_message_widget(self, message: Dict, index: int):
        """Add a single message widget"""
        try:
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            thought = message.get('thought', '')
            
            logger.debug(f"[CHAT_DISPLAY] Adding message widget: role={role}, content={content[:50]}..., thought={bool(thought)}")
            
            # Handle thoughts first
            if role == 'assistant' and thought:
                # Add thought bubble
                thought_sender = f"{self.personality_name}'s Thoughts"
                thought_widget = ChatBubbleWidget(thought_sender, thought, False, 'thought')
                self.messages_layout.insertWidget(index, thought_widget)
                
                # Add main message
                message_widget = ChatBubbleWidget(self.personality_name, content, False, 'message')
                self.messages_layout.insertWidget(index + 1, message_widget)
            else:
                # Handle regular messages
                if role == 'user':
                    message_widget = ChatBubbleWidget("You", content, True, 'message')
                elif role == 'system':
                    message_widget = ChatBubbleWidget("System", content, False, 'system')
                elif role == 'assistant':
                    message_widget = ChatBubbleWidget(self.personality_name, content, False, 'message')
                else:
                    # Fallback
                    message_widget = ChatBubbleWidget(role.title(), content, False, 'message')
                
                self.messages_layout.insertWidget(index, message_widget)
                
            logger.debug(f"[CHAT_DISPLAY] Successfully added message widget for role: {role}")
                
        except Exception as e:
            logger.error(f"Error adding message widget: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
    
    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        try:
            # Use QTimer to ensure scrolling happens after layout update
            QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            ))
        except Exception as e:
            logger.debug(f"Error scrolling to bottom: {e}")
    
    def add_message(self, sender: str, content: str, message_idx: int = None):
        """Add a single message to the display"""
        try:
            # Create message widget
            if sender == "You":
                message_widget = ChatBubbleWidget(sender, content, True, 'message')
            elif sender == "System":
                message_widget = ChatBubbleWidget(sender, content, False, 'system')
            else:
                message_widget = ChatBubbleWidget(sender, content, False, 'message')
            
            # Add to layout
            self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_widget)
            
            # Scroll to bottom
            self._scroll_to_bottom()
            
        except Exception as e:
            logger.error(f"Error adding message: {e}")
    
    def clear_display(self):
        """Clear the chat display"""
        self._clear_messages()
    
    def emergency_reset(self):
        """Emergency reset of the chat display"""
        try:
            self.clear_display()
            logger.debug("[CHAT_DISPLAY] Emergency reset completed")
        except Exception as e:
            logger.error(f"Error during emergency reset: {e}")
    
    def get_ui_components(self):
        """Get UI components for integration with chat tab"""
        return {
            'scroll_area': self.scroll_area,
            'widget': self
        }


        
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
            if hasattr(self, 'conversation_service') and self.conversation_service:
                messages = self.conversation_service.get_messages()
                user_message_count = 0
                for message in messages:
                    if message.get('role') == 'user':
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
        self.edit_button_widget.setStyleSheet(ChatStyles.get_edit_button_stylesheet())
        
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
        if hasattr(self, 'conversation_service') and self.conversation_service:
            messages = self.conversation_service.get_messages()
            user_messages = [msg for msg in messages if msg.get('role') == 'user']
            
            if 0 <= message_index < len(user_messages):
                message = user_messages[message_index]
                current_content = message.get('content', '')
                self.show_message_edit_dialog(message_index, current_content)
    
    def show_message_edit_dialog(self, message_index: int, current_content: str):
        """Show dialog to edit a message"""

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
        
        # Style the dialog using unified styling
        dialog.setStyleSheet(ChatStyles.get_edit_dialog_stylesheet())
        cancel_button.setStyleSheet(ChatStyles.get_cancel_button_stylesheet())
        
        dialog.exec()
        
    def save_message_edit(self, dialog, message_index: int, new_content: str):
        """Save the edited message"""
        if new_content.strip():
            # Emit signal to notify parent about the edit
            self.message_edited.emit(message_index, new_content.strip())
            dialog.accept()
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
        # UI will be updated by conversation service signals
    
    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        import traceback
        
        tag = "user" if sender == "You" else "ai"
        # If sender is System and message is a personality switch
        if sender == "System" and message.startswith("Switched to "):
            if hasattr(self, 'last_message_type') and self.last_message_type == "system_switch":
                # Update the last system switch message instead of appending
                logger.warning("[PATCH] System switch update path should be handled by conversation service only.", print_to_terminal=True)
                return
            else:
                self.last_message_type = "system_switch"
        else:
            self.last_message_type = tag
        # Always use conversation service - no fallback needed
        if not hasattr(self.parent, 'chat_controller') or not hasattr(self.parent.chat_controller, 'conversation_service'):
            logger.error("[PATCH] Conversation service not available for message creation - this should not happen!")
            return
            
        conversation_service = self.parent.chat_controller.conversation_service
        # Convert sender format for conversation service
        role = "user" if sender == "You" else "assistant" if sender == "AI" else "system"
        conversation_service.add_message(role, message)
        # UI will be updated by conversation service signals
    
    def force_update_display(self):
        """Force an immediate update of the chat display"""
        try:
            # Ensure we're in the main thread

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
                    cursor.movePosition(QTextCursor.MoveOperation.End)
                    self.chat_display.setTextCursor(cursor)
                    
                    # Force update using thread-safe alternative
                    self.chat_display.update()
                    
        except Exception as e:
            logger.error(f"Error in _force_render_display: {e}")
    
    def append_response_chunk(self, chunk: str, model_name: str = None, msg_id: str = None, chunk_index: int = None):
        """Append a streaming response chunk, now with msg_id and chunk_index support and duplicate guard."""
        import traceback
        try:
            logger.debug(f"[PATCH] append_response_chunk called with chunk: {chunk[:50]}, model_name: {model_name}, msg_id: {msg_id}, chunk_index: {chunk_index}")
            
            # Validate chunk content
            if not chunk or not chunk.strip():
                logger.warning(f"[PATCH] Received empty or whitespace-only chunk in append_response_chunk, skipping")
                return
            
            # Validate message ID
            if not msg_id or msg_id == "None" or msg_id == "msg_id_placeholder":
                logger.error(f"[PATCH] Invalid message ID received in append_response_chunk: '{msg_id}'")
                logger.error(f"[PATCH] This will cause the chunk to not be properly associated with a streaming message")
            
            if not hasattr(self, '_last_chunk_index'):
                self._last_chunk_index = -1
            # Guard: Only process if chunk_index is new
            if chunk_index is not None and chunk_index <= self._last_chunk_index:
                logger.warning(f"[PATCH] Duplicate or out-of-order chunk_index {chunk_index} (last: {self._last_chunk_index}), ignoring chunk.")
                return
            self._last_chunk_index = chunk_index if chunk_index is not None else self._last_chunk_index
            if not hasattr(self, 'is_streaming'):
                self.is_streaming = False
            if not self.is_streaming:
                self.start_streaming()
            if not hasattr(self, 'current_response'):
                self.current_response = ""
            self.current_response += chunk
            ai_name = self.get_ai_name()
            label = f"{ai_name} ({model_name})" if model_name else ai_name
            
            # UI will be updated by conversation service signals
            
        except Exception as e:
            logger.error(f"[PATCH] Error in append_response_chunk: {e}")
            logger.error(traceback.format_exc())
    def start_streaming(self):
        """Start streaming state"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            ai_name = self.get_ai_name()
            
            # UI will be updated by conversation service signals
            
    def stop_streaming(self):
        """Stop streaming state"""
        logger.debug("[DEBUG] stop_streaming called. is_streaming: %s", self.is_streaming)
        self.is_streaming = False
        
        # Always use conversation service - no fallback needed
        if not hasattr(self.parent, 'chat_controller') or not hasattr(self.parent.chat_controller, 'conversation_service'):
            logger.error("[PATCH] Conversation service not available for streaming stop - this should not happen!")
            return
            
        conversation_service = self.parent.chat_controller.conversation_service
        conversation_service.finalize_streaming_message()
        
        # UI will be updated by conversation service signals
        
    def clear_chat(self):
        """Clear the chat display"""
        if hasattr(self, 'chat_renderer'):
            self.chat_renderer.clear_chat()
        if hasattr(self, 'chat_display'):
            self.chat_display.clear()
            # Force update after clearing
            self.force_update_display()
    
    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'chat_display': self.scroll_area,  # For backward compatibility
            'scroll_area': self.scroll_area
        }
    
    def get_streaming_handler(self):
        """Get the streaming handler (now returns chat renderer for compatibility)"""
        return self.chat_renderer if hasattr(self, 'chat_renderer') else None 
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *

from pyside_chat.ui.tabs.chat_tab.chat_renderer import ChatRenderer

"""
Chat Display Component - Message display and editing functionality
"""



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
            
            # CRITICAL FIX: Sync messages from conversation service to renderer
            # This ensures the renderer uses the same message list as the conversation service
            self._sync_messages_from_conversation_service()
    
    def _sync_messages_from_conversation_service(self):
        """Sync messages from conversation service to renderer to prevent duplicates"""
        try:
            if hasattr(self.parent, 'chat_controller') and hasattr(self.parent.chat_controller, 'conversation_service'):
                conversation_service = self.parent.chat_controller.conversation_service
                messages = conversation_service.get_messages()
                
                # DEBUG: Log the raw conversation service messages with actual content
                logger.debug(f"[SYNC_DEBUG] Raw conversation service messages: " + 
                           ", ".join([f"{{role: {msg.get('role')}, content_len: {len(msg.get('content', ''))}, content_preview: '{msg.get('content', '')[:50]}', is_streaming: {msg.get('is_streaming')}, id: {msg.get('id')}}}" for msg in messages]), print_to_terminal=True)
                
                # Get the AI name from the personality
                ai_name = self.get_ai_name()
                logger.debug(f"[SYNC_DEBUG] Using AI name: {ai_name}", print_to_terminal=True)
                
                renderer_messages = []
                for i, msg in enumerate(messages):
                    # Convert role to sender name
                    role = msg.get('role', 'unknown')
                    if role == 'assistant':
                        sender = ai_name  # Use personality name for assistant messages
                    elif role == 'user':
                        sender = 'You'  # Use 'You' for user messages
                    elif role == 'system':
                        sender = 'System'  # Use 'System' for system messages
                    else:
                        sender = role  # Fallback to role name
                    
                    renderer_msg = {
                        'sender': sender,
                        'content': msg.get('content', ''),
                        'is_code': msg.get('is_code', False),
                        'is_streaming': msg.get('is_streaming', False),
                        'tag': 'ai' if role == 'assistant' else 'user',
                        'message_id': msg.get('id', '')
                    }
                    renderer_messages.append(renderer_msg)
                    
                    # DEBUG: Log each converted message with actual content
                    logger.debug(f"[SYNC_DEBUG] Converted message {i}: {{sender: {renderer_msg['sender']}, content_len: {len(renderer_msg['content'])}, content_preview: '{renderer_msg['content'][:50]}', is_streaming: {renderer_msg['is_streaming']}, message_id: {renderer_msg['message_id']}}}", print_to_terminal=True)
                
                # Only filter out streaming messages that are truly empty (no content at all)
                renderer_messages = [m for m in renderer_messages if not (m.get('is_streaming') and not m.get('content'))]
                logger.debug(f"[PATCH] Renderer message list after conversion: " + ', '.join([f"{{id: {m.get('message_id')}, sender: {m['sender']}, is_streaming: {m.get('is_streaming')}, content: {m['content'][:30]}}}" for m in renderer_messages]), print_to_terminal=True)
                if hasattr(self, 'chat_renderer') and self.chat_renderer:
                    self.chat_renderer.sync_messages_from_conversation(renderer_messages)
                    logger.debug(f"[SYNC] Synced {len(renderer_messages)} messages from conversation service to renderer")
        except Exception as e:
            logger.error(f"Error syncing messages from conversation service: {e}")
    
    def sync_messages_from_conversation_service(self):
        
        import traceback
        stack = ''.join(traceback.format_stack(limit=10))
        logger.debug(f"[ID:CT001] caller traceback:\n{stack}", print_to_terminal=True)
        """Public method to sync messages from conversation service to renderer"""
        self._sync_messages_from_conversation_service()
    
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
        # Always sync after update
        self._sync_messages_from_conversation_service()
    
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
            # Always use conversation service - no fallback needed
            if not hasattr(self.parent, 'chat_controller') or not hasattr(self.parent.chat_controller, 'conversation_service'):
                logger.error("[PATCH] Conversation service not available - this should not happen!")
                return
                
            conversation_service = self.parent.chat_controller.conversation_service
            logger.debug(f"[CHAT_DISPLAY_DEBUG] About to call conversation_service.update_streaming_message with chunk: {chunk[:50]}, msg_id: {msg_id}, chunk_index: {chunk_index}")
            success = conversation_service.update_streaming_message(chunk, append=True, msg_id=msg_id, chunk_index=chunk_index)
            logger.debug(f"[CHAT_DISPLAY_DEBUG] conversation_service.update_streaming_message returned: {success}")
            
            if not success:
                logger.error("[PATCH] conversation_service.update_streaming_message failed!")
                logger.error(f"[PATCH] Failed to update streaming message with chunk: {chunk[:50]}, msg_id: {msg_id}")
            
            # CRITICAL FIX: Don't call _sync_messages_from_conversation_service() here
            # The conversation service already emits conversation_updated which should trigger UI updates
            # Calling _sync_messages_from_conversation_service() here creates an infinite loop
        except Exception as e:
            logger.error(f"[PATCH] Error in append_response_chunk: {e}")
            logger.error(traceback.format_exc())
    def start_streaming(self):
        """Start streaming state"""
        if not self.is_streaming:  # Only change state if not already streaming
            self.is_streaming = True
            self.current_response = ""
            ai_name = self.get_ai_name()
            
            # CRITICAL FIX: Don't create a new streaming message here
            # The streaming message should already be created by the event bus
            # Just sync the existing messages from conversation service to renderer
            self._sync_messages_from_conversation_service()
            
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
        
        # Sync messages from conversation service to renderer
        self._sync_messages_from_conversation_service()
        
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
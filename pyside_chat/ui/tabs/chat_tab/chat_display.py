from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.ui.themes.chat_styles import ChatStyles, ChatBubbleWidget
from pyside_chat.ui.themes.system_message_manager import SystemMessageManager
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QMenu, QApplication, QTextEdit
from PySide6.QtGui import QAction, QTextCursor, QShortcut, QKeySequence
from PySide6.QtCore import QTimer

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

    # Signals
    # Emitted when a message is edited (message_index, new_content)
    message_edited = Signal(int, str)

    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager

        # State variables
        self.conversation_service = None
        self.personality_name = "Assistant"

        # Hidden text edit for selection and copy functionality
        self.selection_text_edit = QTextEdit()
        self.selection_text_edit.setVisible(False)
        self.selection_text_edit.setMaximumHeight(0)
        self.selection_text_edit.setMaximumWidth(0)

        # Configure text edit for selection highlighting
        self.selection_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
                selection-background-color: #2b5797;
                selection-color: #ffffff;
            }
        """)

        # Setup UI
        self.setup_ui()

        # Setup connections
        self.setup_connections()

    # ============================================================================
    # INITIALIZATION AND SETUP METHODS
    # ============================================================================

    def setup_ui(self):
        """Setup the UI components"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Widget to hold messages
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(8)

        # Add spacer to push messages to top
        self.spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.messages_layout.addItem(self.spacer)

        self.scroll_area.setWidget(self.messages_widget)
        self.main_layout.addWidget(self.scroll_area)

        # Add hidden text edit to layout (for selection functionality)
        self.main_layout.addWidget(self.selection_text_edit)

        # Add loading wave widget
        from pyside_chat.ui.animations.loading_wave_widget import LoadingWaveWidget
        self.loading_widget = LoadingWaveWidget(self, num_dots=4, dot_size=6, spacing=10)
        self.loading_widget.setVisible(False)
        self.main_layout.addWidget(self.loading_widget)

        # Make the chat display focusable for selection
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Setup keyboard shortcuts
        self._setup_keyboard_shortcuts()

        # Enable mouse tracking for selection
        self.setMouseTracking(True)

        # Connect text edit selection changes
        self.selection_text_edit.selectionChanged.connect(
            self._on_selection_changed)

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

        # Handle resize events to update bubble layouts
        self.resizeEvent = self._handle_resize

    def setup_connections(self):
        """Setup signal connections"""
        pass  # Will be connected by chat tab

    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for the chat display"""
        try:
            # Select All shortcut (Ctrl+A)
            select_all_shortcut = QShortcut(
                QKeySequence.StandardKey.SelectAll, self)
            select_all_shortcut.activated.connect(self._select_all_text)

            # Copy shortcut (Ctrl+C)
            copy_shortcut = QShortcut(QKeySequence.StandardKey.Copy, self)
            copy_shortcut.activated.connect(self._copy_selected_text)

            logger.debug("Keyboard shortcuts setup completed")
        except Exception as e:
            logger.error(f"Error setting up keyboard shortcuts: {e}")

        logger.debug("[CHAT_DISPLAY] Chat display initialized")

    # ============================================================================
    # SELECTION AND COPY FUNCTIONALITY
    # ============================================================================

    def _select_all_text(self):
        """Select all text in the chat display"""
        try:
            # Update the hidden text edit with current conversation
            self._update_selection_text()

            # Select all text in the hidden text edit
            cursor = self.selection_text_edit.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            self.selection_text_edit.setTextCursor(cursor)

            # Show the text edit temporarily to display selection
            self._show_selection_text_edit()

            logger.debug("Selected all text in chat display")
        except Exception as e:
            logger.error(f"Error selecting all text: {e}")

    def _copy_selected_text(self):
        """Copy selected text from the hidden text edit"""
        try:
            # Update the hidden text edit with current conversation
            self._update_selection_text()

            # Get selected text from the hidden text edit
            cursor = self.selection_text_edit.textCursor()
            selected_text = cursor.selectedText()

            if selected_text:
                # Show the text edit to display current selection
                self._show_selection_text_edit()

                # Copy selected text to clipboard
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_text)
                logger.debug(
                    f"Copied selected text: {len(selected_text)} characters")
            else:
                # If no text is selected, copy all text
                self._copy_all_messages()

        except Exception as e:
            logger.error(f"Error copying selected text: {e}")

    def _update_selection_text(self):
        """Update the hidden text edit with current conversation text"""
        try:
            if not self.conversation_service:
                return

            messages = self.conversation_service.get_messages()
            if not messages:
                return

            # Format messages as text for selection
            formatted_text = self._format_messages_for_copy(messages)

            # Update the hidden text edit
            self.selection_text_edit.setPlainText(formatted_text)

        except Exception as e:
            logger.error(f"Error updating selection text: {e}")

    def _copy_all_messages(self):
        """Copy all messages to clipboard"""
        try:
            if not self.conversation_service:
                logger.warning("No conversation service available for copying")
                return

            messages = self.conversation_service.get_messages()
            if not messages:
                logger.warning("No messages to copy")
                return

            # Format all messages as text
            formatted_text = self._format_messages_for_copy(messages)

            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(formatted_text)

            logger.debug("Copied all messages to clipboard")

        except Exception as e:
            logger.error(f"Error copying all messages: {e}")

    def _format_messages_for_copy(self, messages: List[Dict]) -> str:
        """Format messages as plain text for copying"""
        try:
            formatted_lines = []

            for message in messages:
                role = message.get('role', 'unknown')
                content = message.get('content', '')
                thought = message.get('thought', '')
                personality = message.get('personality', None)

                # Format sender name
                if role == 'assistant' and personality:
                    sender = personality
                elif role == 'user':
                    sender = "You"
                elif role == 'system':
                    sender = "System"
                else:
                    sender = role.title()

                # Add thought if present
                if role == 'assistant' and thought:
                    formatted_lines.append(f"{sender}'s Thoughts: {thought}")
                    # Empty line between thought and message
                    formatted_lines.append("")

                # Add main message
                formatted_lines.append(f"{sender}: {content}")
                formatted_lines.append("")  # Empty line between messages

            return "\n".join(formatted_lines)

        except Exception as e:
            logger.error(f"Error formatting messages for copy: {e}")
            return "Error formatting messages"

    def _show_selection_text_edit(self):
        """Show the text edit widget for selection visibility"""
        try:
            # Make text edit visible and properly sized
            self.selection_text_edit.setVisible(True)
            self.selection_text_edit.setMaximumHeight(
                200)  # Show a reasonable height
            self.selection_text_edit.setMaximumWidth(
                400)   # Show a reasonable width

            # Position it at the bottom of the chat display
            self.selection_text_edit.setGeometry(
                10, self.height() - 220, 380, 200)

            # Set focus to the text edit so selection is visible
            self.selection_text_edit.setFocus()

            # Set up a timer to hide it after a few seconds
            QTimer.singleShot(3000, self._hide_selection_text_edit)

        except Exception as e:
            logger.error(f"Error showing selection text edit: {e}")

    def _hide_selection_text_edit(self):
        """Hide the text edit widget"""
        try:
            self.selection_text_edit.setVisible(False)
            self.selection_text_edit.setMaximumHeight(0)
            self.selection_text_edit.setMaximumWidth(0)

            # Return focus to the chat display
            self.setFocus()

        except Exception as e:
            logger.error(f"Error hiding selection text edit: {e}")

    def _on_selection_changed(self):
        """Handle when text selection changes in the text edit"""
        try:
            cursor = self.selection_text_edit.textCursor()
            selected_text = cursor.selectedText()

            if selected_text:
                # If there's a selection, show the text edit
                self._show_selection_text_edit()
            else:
                # If no selection, hide the text edit after a delay
                QTimer.singleShot(1000, self._hide_selection_text_edit)

        except Exception as e:
            logger.error(f"Error handling selection change: {e}")

    # ============================================================================
    # CONTEXT MENU FUNCTIONALITY
    # ============================================================================

    def contextMenuEvent(self, event):
        """Handle right-click context menu"""
        try:
            # Create context menu
            context_menu = QMenu(self)

            # Add Select All action
            select_all_action = QAction("Select All", self)
            select_all_action.triggered.connect(self._select_all_text)
            context_menu.addAction(select_all_action)

            # Add Copy action
            copy_action = QAction("Copy", self)
            copy_action.triggered.connect(self._copy_selected_text)
            context_menu.addAction(copy_action)

            # Check if there's currently selected text
            cursor = self.selection_text_edit.textCursor()
            selected_text = cursor.selectedText()
            if selected_text:
                copy_action.setText(
                    f"Copy ({len(selected_text)} characters selected)")

            # Add separator
            context_menu.addSeparator()

            # Add Copy All Messages action
            copy_all_action = QAction("Copy All Messages", self)
            copy_all_action.triggered.connect(self._copy_all_messages)
            context_menu.addAction(copy_all_action)

            # Show the context menu at cursor position
            context_menu.exec(event.globalPos())

        except Exception as e:
            logger.error(f"Error showing context menu: {e}")

    # ============================================================================
    # CONVERSATION MANAGEMENT
    # ============================================================================

    def set_conversation_service(self, conversation_service):
        """Set the conversation service reference"""
        logger.debug(
            f"[CHAT_DISPLAY] Setting conversation service: {conversation_service}")

        # Disconnect from previous conversation service if exists
        if hasattr(self, 'conversation_service') and self.conversation_service:
            try:
                self.conversation_service.conversation_updated.disconnect(
                    self._on_conversation_updated)
                logger.debug(
                    "[CHAT_DISPLAY] Disconnected from previous conversation service")
            except TypeError:
                # No existing connection, safe to ignore
                pass
            except Exception as e:
                logger.debug(f"[CHAT_DISPLAY] Safe disconnect: {e}")

        self.conversation_service = conversation_service

        # Connect to conversation service updates
        if conversation_service:
            conversation_service.conversation_updated.connect(
                self._on_conversation_updated)
            logger.debug(
                "[CHAT_DISPLAY] Connected to conversation service updates")

            # Test: Get messages immediately to verify connection
            try:
                messages = conversation_service.get_messages()
                if messages:
                    self.render_conversation(messages)
                    logger.debug(
                        f"[CHAT_DISPLAY] Rendered {len(messages)} initial messages")
            except Exception as e:
                logger.debug(
                    f"[CHAT_DISPLAY] Error getting initial messages: {e}")

    def _on_conversation_updated(self, messages):
        """Handle conversation updates"""
        try:
            logger.debug(
                f"[CHAT_DISPLAY] Conversation updated with {len(messages)} messages")
            self.render_conversation(messages)
        except Exception as e:
            logger.error(f"Error handling conversation update: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def render_conversation(self, conversation: List[Dict], scroll_to_bottom: bool = True):
        """Render the entire conversation using custom bubble widgets"""
        try:
            logger.debug(
                f"[CHAT_DISPLAY] Rendering conversation with {len(conversation)} messages")

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

    def add_message(self, sender: str, content: str, message_idx: int = None):
        """Add a single message to the display"""
        try:
            # Create message widget
            if sender == "You":
                message_widget = ChatBubbleWidget(
                    sender, content, True, 'message')
            elif sender == "System":
                message_widget = ChatBubbleWidget(
                    sender, content, False, 'system')
            else:
                message_widget = ChatBubbleWidget(
                    sender, content, False, 'message')

            # Add to layout
            self.messages_layout.insertWidget(
                self.messages_layout.count() - 1, message_widget)

            # Scroll to bottom
            self._scroll_to_bottom()

        except Exception as e:
            logger.error(f"Error adding message: {e}")

    def append_to_chat(self, sender: str, message: str, is_code: bool = False):
        import traceback

        tag = "user" if sender == "You" else "ai"
        # If sender is System and message is a personality switch
        if sender == "System" and message.startswith("Switched to "):
            if hasattr(self, 'last_message_type') and self.last_message_type == "system_switch":
                # Update the last system switch message instead of appending
                logger.warning(
                    "[PATCH] System switch update path should be handled by conversation service only.", print_to_terminal=True)
                return
            else:
                self.last_message_type = "system_switch"
        else:
            self.last_message_type = tag
        # Always use conversation service - no fallback needed
        if not hasattr(self.parent, 'chat_controller') or not hasattr(self.parent.chat_controller, 'conversation_service'):
            logger.error(
                "[PATCH] Conversation service not available for message creation - this should not happen!")
            return

        conversation_service = self.parent.chat_controller.conversation_service
        # Convert sender format for conversation service
        role = "user" if sender == "You" else "assistant" if sender == "AI" else "system"
        conversation_service.add_message(role, message)
        # UI will be updated by conversation service signals

    def clear_chat(self):
        """Clear the chat display"""
        if hasattr(self, 'chat_renderer'):
            self.chat_renderer.clear_chat()
        if hasattr(self, 'chat_display'):
            self.chat_display.clear()
            # Force update after clearing
            self.force_update_display()

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

    # ============================================================================
    # MESSAGE RENDERING
    # ============================================================================

    def _clear_messages(self):
        """Clear all message widgets"""
        # Remove all widgets except the spacer
        while self.messages_layout.count() > 1:
            child = self.messages_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _add_message_widget(self, message: Dict, index: int):
        try:
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            thought = message.get('thought', '')
            personality = message.get('personality', None)

            # Compose sender label
            if role == 'assistant' and personality:
                sender_label = f"{personality}"
            elif role == 'user':
                sender_label = "You"
            elif role == 'system':
                sender_label = "System"
            else:
                sender_label = role.title()

            # Handle thoughts first
            if role == 'assistant' and thought:
                thought_sender = f"{sender_label}'s Thoughts"
                thought_widget = ChatBubbleWidget(
                    thought_sender, thought, False, 'thought')
                # Insert before the spacer (at the end of existing messages)
                self.messages_layout.insertWidget(
                    self.messages_layout.count() - 1, thought_widget)
                message_widget = ChatBubbleWidget(
                    sender_label, content, False, 'message')
                # Insert before the spacer (at the end of existing messages)
                self.messages_layout.insertWidget(
                    self.messages_layout.count() - 1, message_widget)
            else:
                if role == 'user':
                    message_widget = ChatBubbleWidget(
                        sender_label, content, True, 'message')
                elif role == 'system':
                    message_widget = ChatBubbleWidget(
                        sender_label, content, False, 'system')
                elif role == 'assistant':
                    message_widget = ChatBubbleWidget(
                        sender_label, content, False, 'message')
                else:
                    message_widget = ChatBubbleWidget(
                        sender_label, content, False, 'message')
                # Insert before the spacer (at the end of existing messages)
                self.messages_layout.insertWidget(
                    self.messages_layout.count() - 1, message_widget)
            logger.debug(
                f"[CHAT_DISPLAY] Successfully added message widget for role: {role}")
        except Exception as e:
            logger.error(f"Error adding message widget: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        try:
            # Use QTimer to ensure scrolling happens after layout update
            # Increased delay to ensure layout is fully updated
            QTimer.singleShot(150, lambda: self._perform_scroll_to_bottom())
        except Exception as e:
            logger.debug(f"Error scrolling to bottom: {e}")
    
    def _perform_scroll_to_bottom(self):
        """Perform the actual scroll to bottom operation"""
        try:
            scroll_bar = self.scroll_area.verticalScrollBar()
            if scroll_bar:
                scroll_bar.setValue(scroll_bar.maximum())
                logger.debug("Scrolled to bottom successfully")
            else:
                logger.warning("Scroll bar not available")
        except Exception as e:
            logger.debug(f"Error in _perform_scroll_to_bottom: {e}")
            # Fallback: try again after a short delay
            QTimer.singleShot(50, lambda: self._perform_scroll_to_bottom())

    def _handle_resize(self, event):
        """Handle resize events to update bubble layouts"""
        super().resizeEvent(event)
        # Update all bubble widgets to recalculate their sizes
        for i in range(self.messages_layout.count()):
            item = self.messages_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, 'update'):
                    widget.update()

    # ============================================================================
    # STREAMING FUNCTIONALITY
    # ============================================================================

    def show_loading_animation_for_ai_response(self):
        """Show the loading animation and set a flag to hide it on first AI chunk."""
        self._waiting_for_first_chunk = True
        self.show_loading_animation()

    def append_response_chunk(self, chunk: str, model_name: str = None, msg_id: str = None, chunk_index: int = None):
        """Append a streaming response chunk, now with msg_id and chunk_index support and duplicate guard."""
        import traceback
        try:
            logger.debug(
                f"[PATCH] append_response_chunk called with chunk: {chunk[:50]}, model_name: {model_name}, msg_id: {msg_id}, chunk_index: {chunk_index}")

            # Hide loading animation on first AI chunk
            if getattr(self, '_waiting_for_first_chunk', False):
                self.hide_loading_animation()
                self._waiting_for_first_chunk = False

            # Validate chunk content
            if not chunk or not chunk.strip():
                logger.warning(
                    f"[PATCH] Received empty or whitespace-only chunk in append_response_chunk, skipping")
                return

            # Validate message ID
            if not msg_id or msg_id == "None" or msg_id == "msg_id_placeholder":
                logger.error(
                    f"[PATCH] Invalid message ID received in append_response_chunk: '{msg_id}'")
                logger.error(
                    f"[PATCH] This will cause the chunk to not be properly associated with a streaming message")

            if not hasattr(self, '_last_chunk_index'):
                self._last_chunk_index = -1
            # Guard: Only process if chunk_index is new
            if chunk_index is not None and chunk_index <= self._last_chunk_index:
                logger.warning(
                    f"[PATCH] Duplicate or out-of-order chunk_index {chunk_index} (last: {self._last_chunk_index}), ignoring chunk.")
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

            # Scroll to bottom after each chunk to keep the latest content visible
            self._scroll_to_bottom()

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

            # Show loading animation
            self.show_loading_animation()

            # UI will be updated by conversation service signals

    def stop_streaming(self):
        """Stop streaming state"""
        logger.debug(
            "[DEBUG] stop_streaming called. is_streaming: %s", self.is_streaming)
        self.is_streaming = False

        # Hide loading animation
        self.hide_loading_animation()

        # Always use conversation service - no fallback needed
        if not hasattr(self.parent, 'chat_controller') or not hasattr(self.parent.chat_controller, 'conversation_service'):
            logger.error(
                "[PATCH] Conversation service not available for streaming stop - this should not happen!")
            return

        conversation_service = self.parent.chat_controller.conversation_service
        conversation_service.finalize_streaming_message()

        # Scroll to bottom when streaming stops to ensure final message is visible
        self._scroll_to_bottom()

        # UI will be updated by conversation service signals

    def show_loading_animation(self):
        """Show the loading wave animation"""
        if hasattr(self, 'loading_widget'):
            self.loading_widget.setVisible(True)
            self.loading_widget.start_animation()
            logger.debug("Loading animation started")

    def hide_loading_animation(self):
        """Hide the loading wave animation"""
        if hasattr(self, 'loading_widget'):
            self.loading_widget.stop_animation()
            self.loading_widget.setVisible(False)
            logger.debug("Loading animation stopped")

    # ============================================================================
    # UI EVENTS AND INTERACTIONS
    # ============================================================================

    def mousePressEvent(self, event):
        """Handle mouse press events for selection"""
        try:
            # Set focus to this widget when clicked
            self.setFocus()

            # Update selection text when clicked
            self._update_selection_text()

            # Call parent method
            super().mousePressEvent(event)

        except Exception as e:
            logger.error(f"Error in mouse press event: {e}")

    def focusInEvent(self, event):
        """Handle focus in events"""
        try:
            # Update selection text when focused
            self._update_selection_text()
            super().focusInEvent(event)
        except Exception as e:
            logger.error(f"Error in focus in event: {e}")

    def chat_display_mouse_move_event(self, event):
        """Handle mouse move events to show/hide edit buttons"""
        # Call the original mouseMoveEvent
        super(self.chat_display.__class__,
              self.chat_display).mouseMoveEvent(event)

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
                            self.show_edit_button(
                                event.pos(), user_message_count - 1)
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
        self.edit_button_widget.setStyleSheet(
            ChatStyles.get_edit_button_stylesheet())

        # Position the button near the mouse cursor
        button_pos = self.chat_display.mapFromGlobal(
            self.chat_display.mapToGlobal(pos))
        button_pos.setX(button_pos.x() + 10)
        button_pos.setY(button_pos.y() - 12)
        self.edit_button_widget.move(button_pos)

        # Connect button click
        self.edit_button_widget.clicked.connect(
            lambda: self.edit_message_at_index(message_index))

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
            user_messages = [
                msg for msg in messages if msg.get('role') == 'user']

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
        save_button.clicked.connect(lambda: self.save_message_edit(
            dialog, message_index, text_edit.toPlainText()))
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
            show_validation_error(
                "message", "Message cannot be empty", self.parent)

    # ============================================================================
    # UTILITY AND HELPER METHODS
    # ============================================================================

    def get_ai_name(self) -> str:
        """Get the current AI name from personality service"""
        try:
            if hasattr(self.parent, 'get_service_manager'):
                service_manager = self.parent.get_service_manager()
                if hasattr(service_manager, 'get_personality_service'):
                    personality_service = service_manager.get_personality_service()
                    if personality_service:
                        return personality_service.get_selected_model()
        except Exception as e:
            logger.debug(f"Error getting AI name: {e}")

        return self.personality_name

    def update_personality_name(self, personality_name: str):
        """Update the personality name"""
        self.personality_name = personality_name
        logger.debug(
            f"[CHAT_DISPLAY] Updated personality name to: {personality_name}")

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

    def get_ui_components(self):
        """Get UI components for integration with chat tab"""
        return {
            'scroll_area': self.scroll_area,
            'widget': self
        }

    def get_ui_components(self) -> dict:
        """Get UI components for integration with parent"""
        return {
            'chat_display': self.scroll_area,  # For backward compatibility
            'scroll_area': self.scroll_area
        }

    def get_streaming_handler(self):
        """Get the streaming handler (now returns chat renderer for compatibility)"""
        return self.chat_renderer if hasattr(self, 'chat_renderer') else None

    # ============================================================================
    # EVENT HANDLERS AND CALLBACKS
    # ============================================================================

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
        logger.debug(
            f"Message edited: index={message_index}, content='{new_content[:50]}...'")
        # UI will be updated by conversation service signals

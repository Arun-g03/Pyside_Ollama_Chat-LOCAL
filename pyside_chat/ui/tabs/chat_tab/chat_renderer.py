from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from html import escape
# Import ChatStyles directly - no need for MessageFormatter here anymore
from pyside_chat.ui.themes.chat_styles import ChatStyles
from pyside_chat.ui.themes.system_message_manager import SystemMessageManager

"""
Chat Renderer - Localized rendering system for chat display
"""

import logging
import traceback
import time
from typing import List, Dict, Optional

logger = CustomLogger.get_logger(__name__)


class ChatRenderer(QObject):
    """Localized chat renderer that handles all UI rendering logic"""

    def __init__(self, text_edit: QTextEdit, personality_name: str = None):
        super().__init__()
        self.text_edit = text_edit
        self.personality_name = personality_name or "Assistant"
        self.system_message_manager = SystemMessageManager()
        self.last_render_time = 0
        self.render_debounce_ms = 100  # Debounce renders to avoid excessive updates

        # Initialize the text edit with proper styling
        self._setup_text_edit()

    def set_personality_name(self, personality_name: str):
        """Set the personality name for display in thoughts"""
        self.personality_name = personality_name or "Assistant"

    def _setup_text_edit(self):
        """Setup the text edit with proper styling"""
        self.text_edit.setStyleSheet(ChatStyles.get_common_styles())
        # QTextEdit doesn't have setOpenExternalLinks/setOpenLinks methods
        # These are only available in QTextBrowser

    def render_conversation(self, conversation: List[Dict], scroll_to_bottom: bool = True):
        """
        Render the entire conversation with proper styling and formatting.
        This is the main orchestration method.
        """
        try:
            # Debounce rapid renders
            current_time = time.time() * 1000
            if current_time - self.last_render_time < self.render_debounce_ms:
                return

            self.last_render_time = current_time

            # Generate the HTML content
            html_content = self._generate_conversation_html(conversation)

            # Display the content
            self._display_html_content(html_content, scroll_to_bottom)

        except Exception as e:
            logger.error(f"Error rendering conversation: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")

    def _generate_conversation_html(self, conversation: List[Dict]) -> str:
        """
        Generate HTML for the entire conversation.
        This handles data preparation, transformation, and HTML generation in one place.
        """
        html_parts = []

        for i, message in enumerate(conversation):
            try:
                # Extract message data - conversation service uses 'role' not 'sender'
                role = message.get('role', 'unknown')
                content = message.get('content', '')
                message_idx = message.get('message_idx', i)
                thought = message.get('thought', '')  # Check for thought field

                # Transform role to display sender
                display_sender = self._get_display_sender(role)

                # For assistant messages with thoughts, render thought first, then main message
                if role == 'assistant' and thought:
                    # Render thought bubble first with personality name
                    thought_sender = f"{self.personality_name}'s Thoughts"
                    thought_html = self._generate_single_message_html(
                        thought_sender, thought, message_idx)
                    if thought_html:
                        html_parts.append(thought_html)

                    # Then render the main assistant message with extra top margin
                    message_html = self._generate_single_message_html(
                        display_sender, content, message_idx)
                    if message_html:
                        # Add extra top margin to separate thought from main message
                        message_html = message_html.replace(
                            'margin: 8px 0;', 'margin: 16px 0 8px 0;')
                        html_parts.append(message_html)
                else:
                    # Generate HTML for this message based on its type
                    message_html = self._generate_single_message_html(
                        display_sender, content, message_idx)

                    if message_html:
                        html_parts.append(message_html)

            except Exception as e:
                logger.error(f"Error processing message {i}: {e}")
                continue

        return '\n'.join(html_parts)

    def _get_display_sender(self, role: str) -> str:
        """Transform role names to display sender names"""
        # Use personality name for all AI-related messages
        if role.lower() in ['assistant', 'thinking', 'thoughts']:
            if role.lower() == 'thoughts':
                return f"{self.personality_name}'s Thoughts"
            else:
                return self.personality_name

        sender_mapping = {
            'user': 'You',
            'system': 'System'
        }
        return sender_mapping.get(role.lower(), role.title())

    def _generate_single_message_html(self, sender: str, content: str, message_idx: int) -> str:
        """
        Generate HTML for a single message based on its type.
        This is the core display logic.
        """
        try:
            # Handle different message types
            if sender == "You":
                return ChatStyles.get_user_bubble_html(sender, content, message_idx)

            elif sender == "System":
                # Use system message manager for proper styling
                style_type = self.system_message_manager.get_style_for_message(
                    content)
                return ChatStyles.get_system_message_html(content, message_idx, style_type)

            elif "Thoughts" in sender:
                # Handle thoughts with personality name
                return ChatStyles.get_thought_bubble_html(content, message_idx, sender)

            elif sender == "Thinking":
                return ChatStyles.get_thinking_bubble_html(content, message_idx)

            elif sender == "AI":
                # AI Assistant messages - apply content formatting first
                formatted_content = ChatStyles.format_message_content(
                    content, sender)
                return ChatStyles.get_ai_bubble_html(sender, formatted_content, message_idx)

        except Exception as e:
            logger.error(f"Error generating HTML for message: {e}")
            # Fallback to simple text
            return f"<p><b>{escape(sender)}:</b> {escape(content)}</p>"

    def _display_html_content(self, html_content: str, scroll_to_bottom: bool = True):
        """
        Display the HTML content in the text edit.
        This handles the actual display logic.
        """
        try:
            # Set the HTML content
            self.text_edit.setHtml(html_content)

            # Scroll to bottom if requested
            if scroll_to_bottom:
                self._scroll_to_bottom()

        except Exception as e:
            logger.error(f"Error displaying HTML content: {e}")
            # Fallback to plain text
            self.text_edit.setPlainText(html_content)

    def _scroll_to_bottom(self):
        """Scroll the text edit to the bottom"""
        try:
            scrollbar = self.text_edit.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            logger.debug(f"Error scrolling to bottom: {e}")

    def add_message(self, sender: str, content: str, message_idx: int = None):
        """
        Add a single message to the display.
        This is for real-time message addition.
        """
        try:
            if message_idx is None:
                message_idx = self._get_next_message_idx()

            display_sender = self._get_display_sender(sender)
            message_html = self._generate_single_message_html(
                display_sender, content, message_idx)

            if message_html:
                # Append to existing content
                current_html = self.text_edit.toHtml()
                new_html = current_html + '\n' + message_html
                self.text_edit.setHtml(new_html)
                self._scroll_to_bottom()

        except Exception as e:
            logger.error(f"Error adding message: {e}")

    def _get_next_message_idx(self) -> int:
        """Get the next message index for new messages"""
        # Simple implementation - could be enhanced with proper tracking
        return int(time.time() * 1000)

    def clear_display(self):
        """Clear the chat display"""
        try:
            self.text_edit.clear()
        except Exception as e:
            logger.error(f"Error clearing display: {e}")

    def emergency_reset(self):
        """
        Emergency reset method for handling critical rendering issues.
        This is the flow control method.
        """
        try:
            logger.warning("Performing emergency reset of chat renderer")
            self.clear_display()
            self.last_render_time = 0
            self._setup_text_edit()
        except Exception as e:
            logger.error(f"Error during emergency reset: {e}")

    def update_system_message_style(self, style_type: str):
        """Update system message display style"""
        try:
            self.system_message_manager.update_style(style_type)
        except Exception as e:
            logger.error(f"Error updating system message style: {e}")

    def get_current_content(self) -> str:
        """Get the current HTML content of the display"""
        try:
            return self.text_edit.toHtml()
        except Exception as e:
            logger.error(f"Error getting current content: {e}")
            return ""

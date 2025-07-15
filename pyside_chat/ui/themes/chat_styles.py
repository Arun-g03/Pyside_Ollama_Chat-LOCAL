"""
Chat Styles - Unified styling system for chat components
Consolidates all chat styling logic in one place for consistency and maintainability.
"""

from typing import Dict, Any
from html import escape
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QSizePolicy
from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPainterPath
import logging

logger = logging.getLogger(__name__)

class ChatBubbleWidget(QWidget):
    """Custom chat bubble widget with rounded corners using QPainter"""
    
    def __init__(self, sender: str, content: str, is_user: bool = False, 
                 bubble_type: str = 'message', parent=None):
        super().__init__(parent)
        self.sender = sender
        self.content = content
        self.is_user = is_user
        self.bubble_type = bubble_type
        
        # Colors based on bubble type
        self.colors = self._get_colors()
        
        # Setup layout
        self.setup_layout()
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
    def _get_colors(self):
        """Get colors based on bubble type"""
        if self.bubble_type == 'thought':
            return {
                'background': QColor('#3a3a3a'),
                'text': QColor('#ffffff'),
                'border': QColor('#555555')
            }
        elif self.bubble_type == 'thinking':
            return {
                'background': QColor('#4a4a4a'),
                'text': QColor('#ffffff'),
                'border': QColor('#666666')
            }
        elif self.bubble_type == 'system':
            return {
                'background': QColor('#2d2d2d'),
                'text': QColor('#cccccc'),
                'border': QColor('#444444')
            }
        elif self.is_user:
            return {
                'background': QColor('#2b5797'),
                'text': QColor('#ffffff'),
                'border': QColor('#1e3a5f')
            }
        else:  # AI message
            return {
                'background': QColor('#404040'),
                'text': QColor('#ffffff'),
                'border': QColor('#555555')
            }
    
    def setup_layout(self):
        """Setup the widget layout"""
        # Create content label
        self.content_label = QLabel(self)
        self.content_label.setWordWrap(True)
        self.content_label.setTextFormat(Qt.TextFormat.RichText)
        
        # Format content based on bubble type
        if self.bubble_type == 'system':
            formatted_content = f"<b>System:</b> {escape(self.content)}"
        elif self.bubble_type in ['thought', 'thinking']:
            formatted_content = f"<b>{self.sender}:</b> {self.content}"
        else:
            formatted_content = f"<b>{self.sender}:</b> {self.content}"
        
        self.content_label.setText(formatted_content)
        
        # Set text color and make background transparent
        self.content_label.setStyleSheet(f"color: {self.colors['text'].name()}; background: transparent; border: none;")
        
        # Set maximum width for the content label (like messaging apps)
        max_width = 400  # Maximum bubble width
        self.content_label.setMaximumWidth(max_width)
        
        # No layout needed since we position manually in paintEvent
    
    def paintEvent(self, event):
        """Custom paint event to draw rounded bubble"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get content label size and position
        content_size = self.content_label.sizeHint()
        
        # Calculate bubble dimensions based on content
        padding = 16  # Padding around content
        bubble_width = min(content_size.width() + padding, 400)  # Max width like messaging apps
        bubble_height = content_size.height() + padding
        
        # Calculate bubble position based on alignment
        if self.is_user:
            # User messages: align to right
            bubble_x = self.width() - bubble_width - 8
        elif self.bubble_type == 'system':
            # System messages: left align
            bubble_x = 8
        else:
            # AI messages: align to left
            bubble_x = 8
        
        bubble_y = 4  # Small top margin
        
        # Position content label within bubble
        content_x = bubble_x + padding // 2
        content_y = bubble_y + padding // 2
        self.content_label.setGeometry(content_x, content_y, content_size.width(), content_size.height())
        
        # Create rounded rectangle path for the bubble
        path = QPainterPath()
        radius = 16
        
        # Draw rounded rectangle around content
        path.addRoundedRect(bubble_x, bubble_y, bubble_width, bubble_height, radius, radius)
        
        # Fill background
        painter.fillPath(path, QBrush(self.colors['background']))
        
        # Draw border
        pen = QPen(self.colors['border'], 1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Add shadow effect (simple)
        if self.bubble_type == 'message':
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(bubble_x + 2, bubble_y + 2, bubble_width - 4, bubble_height - 4, radius, radius)
            painter.fillPath(shadow_path, QBrush(QColor(0, 0, 0, 30)))
    
    def sizeHint(self):
        """Provide size hint for the widget"""
        content_size = self.content_label.sizeHint()
        padding = 16
        bubble_width = min(content_size.width() + padding, 400)
        bubble_height = content_size.height() + padding
        
        return QSize(bubble_width + 16, bubble_height + 8)  # Add margins

class ChatStyles:
    """Centralized chat styling system"""
    
    # Color scheme
    COLORS = {
        'user_bubble': '#2b5797',
        'user_text': '#ffffff',
        'ai_bubble': '#404040',
        'ai_text': '#ffffff',
        'system_bubble': '#2d2d2d',
        'system_text': '#cccccc',
        'thought_bubble': '#3a3a3a',
        'thought_text': '#ffffff',
        'thinking_bubble': '#4a4a4a',
        'thinking_text': '#ffffff',
        'border': '#555555',
        'border_dark': '#444444',
        'code_background': '#1e1e1e',
        'code_text': '#dcdcdc',
        'code_border': '#444444',
        'inline_code_bg': '#2d2d2d',
        'inline_code_text': '#e6e6e6',
        'cursor': '#ffffff'
    }
    
    @classmethod
    def _get_base_bubble_style(cls, tag: str, is_streaming: bool = False) -> str:
        """Returns common CSS for message bubbles."""
        base_style = "max-width: 600px; display: table; word-break: break-word; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"
        if tag == 'user':
            return f"background-color: {cls.COLORS['user_bubble']}; color: {cls.COLORS['user_text']}; border-radius: 16px; padding: 12px 18px; {base_style}"
        elif tag == 'ai':
            return f"background-color: {cls.COLORS['ai_bubble']}; color: {cls.COLORS['ai_text']}; border-radius: 16px; padding: 12px 18px; {base_style}"
        # No default for 'system' as it's handled differently
        return ""

    @classmethod
    def get_user_bubble_html(cls, sender: str, content: str, message_idx: int) -> str:
        """Generate HTML for user message bubble"""
        return (
            f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            f"<td align='right' width='30%'></td>"
            f"<td align='right' width='70%'>"
            f"<div style='background-color: {cls.COLORS['user_bubble']}; color: {cls.COLORS['user_text']}; "
            f"padding: 12px 18px; margin: 8px 0; max-width: 100%; "
            f"word-break: break-word; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.3); "
            f"border: 2px solid {cls.COLORS['user_bubble']}; border-radius: 20px;'>"
            f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
            f"<p style='margin: 0;'><b>{escape(sender)}:</b> {escape(content)}</p>"
            f"</div>"
            f"</td>"
            f"</tr></table>"
        )

    @classmethod
    def get_ai_bubble_html(cls, sender: str, content: str, message_idx: int, extra_top_margin: str = '') -> str:
        """Generate HTML for AI message bubble"""
        margin_style = f"margin: 8px 0; {extra_top_margin}" if extra_top_margin else "margin: 8px 0;"
        return (
            f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            f"<td align='left' width='70%'>"
            f"<div style='background-color: {cls.COLORS['ai_bubble']}; color: {cls.COLORS['ai_text']}; "
            f"padding: 12px 18px; {margin_style}; max-width: 100%; "
            f"word-break: break-word; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.3); "
            f"border: 2px solid {cls.COLORS['ai_bubble']}; border-radius: 20px;'>"
            f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
            f"<p style='margin: 0;'><b>{escape(sender)}:</b> {content}</p>"
            f"</div>"
            f"</td>"
            f"<td align='left' width='30%'></td>"
            f"</tr></table>"
        )

    @classmethod
    def get_system_message_html(cls, content: str, message_idx: int, style_type: str = 'compact') -> str:
        """Generate HTML for system messages with different style options"""
        if style_type == 'hidden':
            return ""
        elif style_type == 'compact':
            return (
                f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
                f"<td align='center'>"
                f"<div style='background-color: {cls.COLORS['system_bubble']}; padding: 8px 12px; "
                f"margin: 8px 0; font-size: 11px; color: {cls.COLORS['system_text']}; "
                f"border-left: 3px solid {cls.COLORS['border_dark']}; max-width: 80%; display: inline-block; "
                f"border: 1px solid {cls.COLORS['system_bubble']}; border-radius: 15px;'>"
                f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
                f"{escape(content)}"
                f"</div>"
                f"</td>"
                f"</tr></table>"
            )
        elif style_type == 'full_width':
            return (
                f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
                f"<td align='center'>"
                f"<div style='background-color: {cls.COLORS['system_bubble']}; padding: 8px 15px; "
                f"margin: 10px 0; color: {cls.COLORS['system_text']}; border-left: 4px solid {cls.COLORS['border_dark']}; max-width: 90%; display: inline-block; "
                f"border: 1px solid {cls.COLORS['system_bubble']}; border-radius: 15px;'>"
                f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
                f"<b>System:</b> {escape(content)}"
                f"</div>"
                f"</td>"
                f"</tr></table>"
            )
        elif style_type == 'centered':
            return (
                f"<div style='text-align: center; margin: 10px 0;'>"
                f"<span style='background-color: {cls.COLORS['system_bubble']}; color: {cls.COLORS['system_text']}; "
                f"padding: 5px 15px; border-radius: 15px; font-size: 12px; border: 1px solid {cls.COLORS['border']};'>"
                f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
                f"{escape(content)}"
                f"</span>"
                f"</div>"
            )
        else:
            # Default compact style
            return cls.get_system_message_html(content, message_idx, 'compact')

    @classmethod
    def get_code_block_html(cls, highlighted_code: str, language: str = None) -> str:
        """Generate HTML for code blocks"""
        language_label = ""
        if language:
            language_label = f'<div style="background-color: #1e1e1e; color: #dcdcdc; padding: 5px 10px; border-bottom: 1px solid #444; font-family: monospace; font-size: 11px; text-transform: uppercase;">{language}</div>'
        
        return (
            f'<div style="background-color: {cls.COLORS["code_background"]}; border-radius: 5px; overflow: hidden; margin: 10px 0; border: 1px solid {cls.COLORS["code_border"]};">'
            f'{language_label}'
            f'<div style="padding: 10px; color: {cls.COLORS["code_text"]}; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto;">{highlighted_code}</div>'
            '</div>'
        )

    @classmethod
    def get_inline_code_html(cls, code: str) -> str:
        """Generate HTML for inline code"""
        return f'<code style="background-color: {cls.COLORS["inline_code_bg"]}; color: {cls.COLORS["inline_code_text"]}; padding: 2px 4px; border-radius: 3px; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 12px;">{escape(code)}</code>'

    @classmethod
    def get_thinking_bubble_html(cls, content: str, message_idx: int) -> str:
        """Generate HTML for thinking/processing messages"""
        return (
            f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            f"<td align='left' width='70%'>"
            f"<div style='background-color: {cls.COLORS['thinking_bubble']}; padding: 10px 14px; "
            f"margin: 8px 0; color: {cls.COLORS['thinking_text']}; "
            f"border-left: 3px solid {cls.COLORS['border']}; font-style: italic; max-width: 100%; "
            f"word-break: break-word; line-height: 1.5; "
            f"border: 1px solid {cls.COLORS['thinking_bubble']}; border-radius: 15px;'>"
            f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
            f"<b>Thinking:</b> {escape(content)}"
            f"</div>"
            f"</td>"
            f"<td align='left' width='30%'></td>"
            f"</tr></table>"
        )

    @classmethod
    def get_thought_bubble_html(cls, content: str, message_idx: int, sender: str = "Assistant's Thoughts") -> str:
        """Generate HTML for thought messages"""
        return (
            f"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            f"<td align='left' width='70%'>"
            f"<div style='background-color: {cls.COLORS['thought_bubble']}; padding: 10px 14px; "
            f"margin: 8px 0; color: {cls.COLORS['thought_text']}; "
            f"border-left: 3px solid {cls.COLORS['border']}; max-width: 100%; "
            f"word-break: break-word; line-height: 1.5; "
            f"border: 1px solid {cls.COLORS['thought_bubble']}; border-radius: 15px;'>"
            f"<span style='display:none' data-msg-idx='{message_idx}'></span>"
            f"<b>{sender}:</b> {content}"
            f"</div>"
            f"</td>"
            f"<td align='left' width='30%'></td>"
            f"</tr></table>"
        )

    @classmethod
    def get_streaming_cursor_html(cls) -> str:
        """Generate HTML for streaming cursor"""
        return f'<span style="color: {cls.COLORS["cursor"]}; animation: blink 1s infinite;">|</span>'

    @classmethod
    def get_common_styles(cls) -> str:
        """Get common CSS styles for the chat display"""
        return f"""
        <style>
        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}
        
        .chat-container {{
            background-color: #1a1a1a;
            color: {cls.COLORS['ai_text']};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }}
        
        .message-bubble {{
            margin: 8px 0;
            word-wrap: break-word;
        }}
        
        .code-block {{
            background-color: {cls.COLORS['code_background']};
            border-radius: 5px;
            overflow: hidden;
            margin: 10px 0;
            border: 1px solid {cls.COLORS['code_border']};
        }}
        
        .inline-code {{
            background-color: {cls.COLORS['inline_code_bg']};
            color: {cls.COLORS['inline_code_text']};
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 12px;
        }}
        </style>
        """

    @classmethod
    def format_message_content(cls, content: str, sender: str) -> str:
        """
        Format message content based on sender type.
        This method delegates to MessageFormatter for content processing.
        """
        # Import here to avoid circular dependency
        from pyside_chat.ui.themes.message_formatter import MessageFormatter
        
        if sender == "You":
            # For user messages, just escape the content
            return escape(content)
        elif sender == "System":
            # For system messages, apply minimal formatting
            return f"<i style='color: {cls.COLORS['system_text']};'>{escape(content)}</i>"
        else:
            # For AI messages, apply full formatting
            return MessageFormatter.cleanup_message(sender, content, False)
    
    @classmethod
    def get_chat_display_stylesheet(cls) -> str:
        """Get the main chat display stylesheet"""
        return """
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
        """
    
    @classmethod
    def get_edit_button_stylesheet(cls) -> str:
        """Get edit button stylesheet"""
        return """
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
        """
    
    @classmethod
    def get_edit_dialog_stylesheet(cls) -> str:
        """Get edit dialog stylesheet"""
        return """
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
        """
    
    @classmethod
    def get_cancel_button_stylesheet(cls) -> str:
        """Get cancel button stylesheet"""
        return """
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
        """ 
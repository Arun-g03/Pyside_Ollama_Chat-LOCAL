"""
Streaming Handler - Extracted from ollama_chat.py
Handles streaming response processing and display updates.
"""

from PySide6.QtWidgets import QTextEdit, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from pyside_chat.utils.message_formatter import MessageFormatter
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class StreamingHandler:
    """Handles streaming response processing and display updates"""
    
    def __init__(self, chat_display: QTextEdit, ai_name: str = "Assistant"):
        self.chat_display = chat_display
        self.messages = []  # List of dicts: {sender, content, is_code, is_streaming, tag}
        self._stream_buffer = None
        self._stream_timer = QTimer()
        self._stream_timer.setInterval(50)  # ms
        self._stream_timer.timeout.connect(self._flush_stream_buffer)
        self.ai_name = ai_name
        #global incrementor
        #self.incrementor = 0


    def append_message(self, sender: str, content: str, is_code: bool = False, tag: str = "ai"):
        """Append a new message (user or system) and re-render chat display"""
        self.messages.append({
            'sender': sender,
            'content': content,
            'is_code': is_code,
            'is_streaming': False,
            'tag': tag
        })
        logger.debug("[DEBUG][append_message] messages: %s", ', '.join(f"{m['sender']} streaming={m['is_streaming']} len={len(m['content'])}" for m in self.messages))
        self._render_chat_display()
        self.chat_display.update()
        QTimer.singleShot(0, self._render_chat_display)

    def start_streaming_message(self, sender: str, tag: str = "ai"):
        """Append a streaming placeholder message and re-render chat display"""
        self.messages.append({
            'sender': sender,
            'content': '',
            'is_code': False,
            'is_streaming': True,
            'tag': tag
        })
        self._render_chat_display()

    def update_streaming_message(self, content: str, sender: str, message_id: str = None, is_code: bool = False, tag: str = "ai"):
        """Update the last streaming message and re-render chat display (throttled)"""
        self._stream_buffer = (content, is_code, tag)
        #self.incrementor = self.incrementor + 1
        
        #logger.debug(f"{self.incrementor}[DEBUG][update_streaming_message] before update messages: %s", ', '.join(f"{m['sender']} streaming={m['is_streaming']} len={len(m['content'])}" for m in self.messages))
        if not self._stream_timer.isActive():
            self._stream_timer.start()

    def _flush_stream_buffer(self):
        if self._stream_buffer is None:
            return
        content, is_code, tag = self._stream_buffer
        self._stream_buffer = None
        # Find the last streaming message
        for msg in reversed(self.messages):
            if msg['is_streaming']:
                msg['content'] = content
                msg['is_code'] = is_code
                msg['tag'] = tag
                break
        self._render_chat_display()
        # If still streaming, keep timer running; else, stop
        if not any(msg['is_streaming'] for msg in self.messages):
            self._stream_timer.stop()

    def finalize_streaming_message(self):
        """Mark the last streaming message as complete and re-render chat display (flush buffer)"""
        logger.debug("[DEBUG][finalize_streaming_message] before finalize messages: %s", ', '.join(f"{m['sender']} streaming={m['is_streaming']} len={len(m['content'])}" for m in self.messages))
        self._flush_stream_buffer()
        # Always re-render, even if no message was streaming
        found_streaming = False
        for i in range(len(self.messages) - 1, -1, -1):
            msg = self.messages[i]
            if msg['is_streaming']:
                msg['is_streaming'] = False
                found_streaming = True
                logger.debug(f"[DEBUG][finalize_streaming_message] Final AI response content: {msg['content']}", print_to_terminal=True)
                # Remove the message if its content is empty or only whitespace
                if not msg['content'] or msg['content'].strip() == '':
                    del self.messages[i]
                break
        logger.debug("[DEBUG][finalize_streaming_message] after finalize messages: %s", ', '.join(f"{m['sender']} streaming={m['is_streaming']} len={len(m['content'])}" for m in self.messages))
        self._render_chat_display()
        self.chat_display.update()

    def update_last_system_switch(self, message: str):
        """Update the last system switch message ("Switched to ...") and re-render chat display"""
        for msg in reversed(self.messages):
            if msg['sender'] == 'System' and msg['content'].startswith('Switched to '):
                msg['content'] = message
                break
        self._render_chat_display()

    def _render_chat_display(self):
        """Re-render the entire chat display from the message list using tables for alignment and content-width bubbles"""
        
        self.chat_display.clear()
        prev_was_thinking = False
        for msg in self.messages:
            sender = msg['sender']
            content = msg['content']
            is_code = msg['is_code']
            is_streaming = msg['is_streaming']
            tag = msg.get('tag', 'ai')
            # Format content
            if is_streaming:
                if not content:
                    # Distinct 'thinking' block for AI
                    if tag == 'ai':
                        html = f"""
                        <table width='100%' cellspacing='0' cellpadding='0'><tr>
                          <td align='left'>
                            <div style='background-color: #23272e; color: #aaa; border-radius: 8px; padding: 10px 16px; margin: 8px 0; max-width: 500px; min-width: 60px; display: inline-block; word-break: break-word; border: 2px dashed #888; font-style: italic;'>
                              💭 Thinking...
                            </div>
                          </td>
                          <td></td>
                        </tr></table>
                        """
                    else:
                        html = f"<div style='color: #888; font-style: italic;'>Thinking...</div>"
                    self.chat_display.insertHtml(html)
                    self.chat_display.insertHtml("<br>")
                    prev_was_thinking = True
                    continue
                else:
                    # Format streaming AI messages just like finalized ones
                    if tag == 'ai':
                        thoughts, main_answer = MessageFormatter.split_thoughts_and_answer(content)
                        if thoughts:
                            # Render thoughts block first
                            thoughts_html = f"""
                            <table width='100%' cellspacing='0' cellpadding='0'><tr>
                              <td align='left'>
                                <div style='background-color: #23272e; color: #aaa; border-radius: 8px; padding: 10px 16px; margin: 8px 0 4px 0; max-width: 500px; min-width: 60px; display: inline-block; word-break: break-word; border: 2px dashed #888; font-style: italic;'>
                                  <b style='color: #aaa;'>{self.ai_name} Thoughts💭:</b><br> {MessageFormatter.handle_html_tags(thoughts)}
                                </div>
                              </td>
                              <td></td>
                            </tr></table>
                            """
                            self.chat_display.insertHtml(thoughts_html)
                            self.chat_display.insertHtml("<br>")
                            content = main_answer
                    formatted_content = MessageFormatter.detect_and_format_code(content)
                    formatted_content = MessageFormatter.handle_html_tags(formatted_content)
            elif is_code:
                formatted_content = MessageFormatter.syntax_highlight_code(content)
            else:
                # Check for <think>...</think> in AI messages
                if tag == 'ai':
                    thoughts, main_answer = MessageFormatter.split_thoughts_and_answer(content)
                    if thoughts:
                        # Render thoughts block first
                        thoughts_html = f"""
                        <table width='100%' cellspacing='0' cellpadding='0'><tr>
                          <td align='left'>
                            <div style='background-color: #23272e; color: #aaa; border-radius: 8px; padding: 10px 16px; margin: 8px 0 4px 0; max-width: 500px; min-width: 60px; display: inline-block; word-break: break-word; border: 2px dashed #888; font-style: italic;'>
                              <b style='color: #aaa;'>{self.ai_name} Thoughts💭:</b><br> {MessageFormatter.handle_html_tags(thoughts)}
                            </div>
                          </td>
                          <td></td>
                        </tr></table>
                        """
                        self.chat_display.insertHtml(thoughts_html)
                        self.chat_display.insertHtml("<br>")
                        # Now render the main answer as the AI bubble
                        content = main_answer
                formatted_content = MessageFormatter.detect_and_format_code(content)
                formatted_content = MessageFormatter.handle_html_tags(formatted_content)

            # Bubble style for content-width
            bubble_style = "max-width: 500px; min-width: 60px; display: inline-block; word-break: break-word;"

            # Table-based alignment
            extra_top_margin = ''
            if tag == 'ai' and not is_streaming and prev_was_thinking:
                extra_top_margin = 'margin-top: 24px;'
            if tag == 'user':
                html = f"""
                <table width='100%' cellspacing='0' cellpadding='0'><tr>
                  <td></td>
                  <td align='right'>
                    <div style='background-color: #1a3a5d; color: #fff; border-radius: 8px; padding: 10px 16px; margin: 8px 0; {bubble_style}'>
                      <b>{sender}:</b> {formatted_content}
                    </div>
                  </td>
                </tr></table>
                """
            elif tag == 'ai':
                html = f"""
                <table width='100%' cellspacing='0' cellpadding='0'><tr>
                  <td align='left'>
                    <div style='background-color: #23272e; color: #fff; border-radius: 8px; padding: 10px 16px; {extra_top_margin} margin: 8px 0; {bubble_style}'>
                      <b>{sender}:</b> {formatted_content}
                    </div>
                  </td>
                  <td></td>
                </tr></table>
                """
            else:
                html = f"""
                <div style='background-color: #1e1e1e; color: #fff; border-radius: 5px; padding: 10px 16px; margin: 8px 0;'><b>{sender}:</b> {formatted_content}</div>
                """
            self.chat_display.insertHtml(html)
            self.chat_display.insertHtml("<br>")
            prev_was_thinking = False
        self.chat_display.ensureCursorVisible()
        logger.debug(f"[DEBUG] _render_chat_display finished. Message count: {len(self.messages)}", print_to_terminal=False)

    def remove_streaming_placeholder(self):
        """Remove the last streaming message (if any) and re-render chat display"""
        for i in range(len(self.messages) - 1, -1, -1):
            if self.messages[i]['is_streaming']:
                del self.messages[i]
                break
        self._render_chat_display()

    def cleanup(self):
        self.messages.clear()
        self._render_chat_display()
    
    def update_ai_name(self, ai_name: str):
        """Update the AI name used for thoughts display"""
        self.ai_name = ai_name 
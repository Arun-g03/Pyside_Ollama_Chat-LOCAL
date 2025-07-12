"""
Streaming Handler - Extracted from ollama_chat.py
Handles streaming response processing and display updates.
"""

from PySide6.QtWidgets import QTextEdit, QApplication
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from pyside_chat.ui.themes.message_formatter import MessageFormatter
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.threading.thread_pool_manager import ThreadPoolManager
from pyside_chat.core.threading.qrunnable_tasks import StreamingUpdateTask
import time
import traceback

logger = CustomLogger.get_logger(__name__)


class StreamingHandler(QObject):
    """Handles streaming response processing and display updates using proper threading architecture"""
    
    # Signal emitted when a message is edited
    message_edited = Signal(int, str)  # message_index, new_content
    
    def __init__(self, chat_display: QTextEdit, ai_name: str = "Assistant"):
        super().__init__()
        self.chat_display = chat_display
        self.messages = []  # List of dicts: {sender, content, is_code, is_streaming, tag, message_id}
        self._stream_buffer = None
        self._stream_timer = QTimer()
        self._stream_timer.setInterval(50)  # ms
        self._stream_timer.timeout.connect(self._flush_stream_buffer)
        self.ai_name = ai_name
        self._message_counter = 0  # For generating unique message IDs
        
        # Initialize thread pool manager for streaming updates
        self.thread_pool_manager = ThreadPoolManager()
        
        # Track active streaming tasks
        self._active_streaming_tasks = set()

    def _get_next_message_id(self):
        """Generate a unique message ID"""
        self._message_counter += 1
        return f"msg_{self._message_counter}"

    def _flush_stream_buffer(self):
        """Flush the stream buffer and update the display using thread pool"""
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
        
        # Use thread pool for UI update
        self._schedule_ui_update()

    def _schedule_ui_update(self):
        """Schedule UI update using thread pool manager"""
        try:
            # Create streaming update task
            task = StreamingUpdateTask(
                target=self._render_chat_display_safe,
                callback=self._on_ui_update_complete
            )
            
            # Submit to thread pool
            task_id = self.thread_pool_manager.start_task(task)
            self._active_streaming_tasks.add(task_id)
            
            logger.debug(f"[DEBUG] Scheduled UI update task: {task_id}")
            
        except Exception as e:
            logger.error(f"Error scheduling UI update: {e}")
            # Fallback to direct update
            QTimer.singleShot(0, self._render_chat_display_safe)

    def _on_ui_update_complete(self, task_id):
        """Callback when UI update task completes"""
        if task_id in self._active_streaming_tasks:
            self._active_streaming_tasks.remove(task_id)
        logger.debug(f"[DEBUG] UI update task completed: {task_id}")

    def append_message(self, sender: str, content: str, is_code: bool = False, tag: str = "ai"):
        """Append a new message (user or system) and re-render chat display"""
        message_id = self._get_next_message_id()
        self.messages.append({
            'sender': sender,
            'content': content,
            'is_code': is_code,
            'is_streaming': False,
            'tag': tag,
            'message_id': message_id
        })
        logger.debug("[DEBUG][append_message] messages: %s", ', '.join(f"{m['sender']} streaming={m['is_streaming']} len={len(m['content'])}" for m in self.messages))
        
        # Use thread pool for UI update
        self._schedule_ui_update()

    def start_streaming_message(self, sender: str, tag: str = "ai"):
        """Append a streaming placeholder message and re-render chat display"""
        message_id = self._get_next_message_id()
        self.messages.append({
            'sender': sender,
            'content': '',
            'is_code': False,
            'is_streaming': True,
            'tag': tag,
            'message_id': message_id
        })
        
        # Use thread pool for UI update
        self._schedule_ui_update()

    def edit_message(self, message_index: int, new_content: str):
        """Edit a specific message by index"""
        if 0 <= message_index < len(self.messages):
            old_content = self.messages[message_index]['content']
            self.messages[message_index]['content'] = new_content
            logger.debug(f"[DEBUG][edit_message] Edited message {message_index}: '{old_content}' -> '{new_content}'")
            
            # Use thread pool for UI update
            self._schedule_ui_update()
            
            # Emit signal for external handling (e.g., conversation saving)
            self.message_edited.emit(message_index, new_content)
            return True
        return False

    def get_message_by_id(self, message_id: str):
        """Get message index by message_id"""
        for i, msg in enumerate(self.messages):
            if msg.get('message_id') == message_id:
                return i
        return -1

    def get_editable_messages(self):
        """Get list of messages that can be edited (non-streaming, non-system)"""
        editable = []
        for i, msg in enumerate(self.messages):
            if not msg['is_streaming'] and msg['sender'] == 'You':
                editable.append({
                    'index': i,
                    'message_id': msg.get('message_id'),
                    'content': msg['content'],
                    'sender': msg['sender']
                })
        return editable

    def get_messages(self):
        """Get all messages as a list of dictionaries"""
        return self.messages.copy()

    def _render_chat_display(self):
        """Re-render the entire chat display from the message list using tables for alignment and content-width bubbles"""
        
        # Use thread pool for UI update
        self._schedule_ui_update()
    
    def _render_chat_display_safe(self):
        """Re-render the chat display safely in the main thread"""
        try:
            # Ensure we're in the main thread
            current_thread = QApplication.instance().thread()
            main_thread = self.chat_display.thread()
            
            logger.debug(f"[ID:0600] Render display safe - Current thread: {current_thread.objectName() or 'unnamed'}")
            logger.debug(f"[ID:0601] Render display safe - Main thread: {main_thread.objectName() or 'unnamed'}")
            
            if current_thread != main_thread:
                # If we're not in the main thread, schedule this for the main thread
                logger.debug("[ID:0602] Not in main thread, scheduling render for main thread")
                QTimer.singleShot(0, self._render_chat_display_safe)
                return
            
            logger.debug(f"[ID:0603] Rendering chat display in main thread - Messages: {len(self.messages)}")
            
            self.chat_display.clear()
            prev_was_thinking = False
            
            for msg in self.messages:
                sender = msg['sender']
                content = msg['content']
                is_code = msg['is_code']
                is_streaming = msg['is_streaming']
                tag = msg.get('tag', 'ai')
                message_id = msg.get('message_id', '')
                
                # Format content
                formatted_content = ''  # Ensure it's always defined
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
                                      <b style='color: #aaa;'>{self.ai_name} Thoughts💭:</b><br> {MessageFormatter.format_markdown(thoughts)}
                                    </div>
                                  </td>
                                  <td></td>
                                </tr></table>
                                """
                                self.chat_display.insertHtml(thoughts_html)
                                self.chat_display.insertHtml("<br>")
                                content = main_answer
                        formatted_content = MessageFormatter.detect_and_format_code(content)
                        formatted_content = MessageFormatter.format_markdown(formatted_content)
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
                                  <b style='color: #aaa;'>{self.ai_name} Thoughts💭:</b><br> {MessageFormatter.format_markdown(thoughts)}
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
                        formatted_content = MessageFormatter.format_markdown(formatted_content)
                # Fallback: if still not set, just escape the content
                if not formatted_content:
                    from html import escape
                    formatted_content = escape(content)

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
                          <span style='display:none' data-msg-idx='{self.messages.index(msg)}'></span>
                          <b>{sender}:</b> {formatted_content}
                        </div>
                      </td>
                    </tr></table>
                    """
                else:  # AI or system message
                    html = f"""
                    <table width='100%' cellspacing='0' cellpadding='0'><tr>
                      <td align='left'>
                        <div style='background-color: #2d3748; color: #e2e8f0; border-radius: 8px; padding: 10px 16px; margin: 8px 0; {bubble_style} {extra_top_margin}'>
                          <span style='display:none' data-msg-idx='{self.messages.index(msg)}'></span>
                          <b>{sender}:</b> {formatted_content}
                        </div>
                      </td>
                      <td></td>
                    </tr></table>
                    """
                
                self.chat_display.insertHtml(html)
                self.chat_display.insertHtml("<br>")
                prev_was_thinking = False
            
            # Scroll to bottom
            cursor = self.chat_display.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.chat_display.setTextCursor(cursor)
            
        except Exception as e:
            logger.error(f"Error in _render_chat_display_safe: {e}")
            logger.error(traceback.format_exc())

    def _safe_ui_update(self, update_func):
        """Safely execute UI updates using thread pool"""
        try:
            # Create UI update task
            task = StreamingUpdateTask(
                target=update_func,
                callback=self._on_ui_update_complete
            )
            
            # Submit to thread pool
            task_id = self.thread_pool_manager.start_task(task)
            self._active_streaming_tasks.add(task_id)
            
            logger.debug(f"[DEBUG] Scheduled safe UI update task: {task_id}")
            
        except Exception as e:
            logger.error(f"Error scheduling safe UI update: {e}")
            # Fallback to direct update
            QTimer.singleShot(0, update_func)

    def update_streaming_message(self, content: str, sender: str, message_id: str = None, is_code: bool = False, tag: str = "ai"):
        """Update the content of the last streaming message"""
        try:
            # Find the last streaming message
            for msg in reversed(self.messages):
                if msg['is_streaming']:
                    msg['content'] = content
                    msg['is_code'] = is_code
                    msg['tag'] = tag
                    break
            
            # Use thread pool for UI update
            self._schedule_ui_update()
            
        except Exception as e:
            logger.error(f"Error updating streaming message: {e}")
            logger.error(traceback.format_exc())

    def finalize_streaming_message(self):
        """Mark the last streaming message as finalized"""
        try:
            # Find the last streaming message and mark it as not streaming
            for msg in reversed(self.messages):
                if msg['is_streaming']:
                    msg['is_streaming'] = False
                    logger.debug(f"[DEBUG] Finalized streaming message: {msg.get('message_id', 'unknown')}")
                    break
            
            # Use thread pool for UI update
            self._schedule_ui_update()
            
        except Exception as e:
            logger.error(f"Error finalizing streaming message: {e}")
            logger.error(traceback.format_exc())

    def update_last_system_switch(self, message: str):
        """Update the last system message with new content"""
        try:
            # Find the last system message
            for msg in reversed(self.messages):
                if msg['sender'] == 'System':
                    msg['content'] = message
                    break
            
            # Use thread pool for UI update
            self._schedule_ui_update()
            
        except Exception as e:
            logger.error(f"Error updating last system message: {e}")
            logger.error(traceback.format_exc())

    def remove_streaming_placeholder(self):
        """Remove the last streaming placeholder message"""
        try:
            # Find and remove the last streaming message
            for i in range(len(self.messages) - 1, -1, -1):
                if self.messages[i]['is_streaming']:
                    removed_msg = self.messages.pop(i)
                    logger.debug(f"[DEBUG] Removed streaming placeholder: {removed_msg.get('message_id', 'unknown')}")
                    break
            
            # Use thread pool for UI update
            self._schedule_ui_update()
            
        except Exception as e:
            logger.error(f"Error removing streaming placeholder: {e}")
            logger.error(traceback.format_exc())

    def cleanup(self):
        """Clean up resources and stop all active tasks"""
        try:
            # Stop stream timer
            if self._stream_timer.isActive():
                self._stream_timer.stop()
            
            # Wait for active streaming tasks to complete
            if self._active_streaming_tasks:
                logger.debug(f"[DEBUG] Waiting for {len(self._active_streaming_tasks)} active streaming tasks to complete")
                self.thread_pool_manager.wait_for_all_tasks(timeout=5.0)
            
            # Clean up thread pool manager
            if self.thread_pool_manager:
                self.thread_pool_manager.shutdown()
            
            logger.debug("[DEBUG] Streaming handler cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during streaming handler cleanup: {e}")
            logger.error(traceback.format_exc())

    def clear_chat(self):
        """Clear all messages and reset the chat display"""
        try:
            self.messages.clear()
            self._stream_buffer = None
            if self._stream_timer.isActive():
                self._stream_timer.stop()
            
            # Use thread pool for UI update
            self._schedule_ui_update()
            
        except Exception as e:
            logger.error(f"Error clearing chat: {e}")
            logger.error(traceback.format_exc())

    def update_ai_name(self, ai_name: str):
        """Update the AI name used in message formatting"""
        self.ai_name = ai_name 
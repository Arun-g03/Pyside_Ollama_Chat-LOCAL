from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.ui.themes.message_formatter import MessageFormatter

"""
Chat Renderer - Localized rendering system for chat display
"""

import logging
import traceback
from typing import List, Dict, Optional

logger = CustomLogger.get_logger(__name__)

class ChatRenderer(QObject):
    """Localized chat renderer that handles all UI rendering logic"""
    
    # Signals
    render_completed = Signal()  # Emitted when render completes
    render_error = Signal(str)   # Emitted when render fails
    
    def __init__(self, chat_display: QTextEdit, ai_name: str = "Assistant", config_manager=None):
        super().__init__()
        self.chat_display = chat_display
        self.ai_name = ai_name
        
        # Rendering state management
        self._is_rendering = False
        self._render_timer = QTimer()
        self._render_timer.setInterval(16)  # 16ms debounce (60fps) for faster response
        self._render_timer.setSingleShot(True)
        self._render_timer.timeout.connect(self._execute_render)
        
        # Emergency reset timer
        self._emergency_reset_timer = QTimer()
        self._emergency_reset_timer.setInterval(500)  # 500ms emergency reset (reduced from 1000ms)
        self._emergency_reset_timer.setSingleShot(True)
        self._emergency_reset_timer.timeout.connect(self._emergency_reset)
        
        # Typewriter effect timer - adds small delay between chunks
        self._typewriter_timer = QTimer()
        self._typewriter_timer.setInterval(10)  # 10ms delay for smoother typewriter effect
        self._typewriter_timer.setSingleShot(True)
        self._typewriter_timer.timeout.connect(self._process_typewriter_chunk)
        self._pending_chunk = None
        
        # Render counter to detect excessive renders
        self._render_counter = 0
        self._max_renders_per_second = 60  # Increased limit for smoother UI
        self._last_render_time = 0
        
        # Message storage (moved from StreamingHandler)
        self.messages: List[Dict] = []
        self._message_counter = 0
        
        self.config_manager = config_manager
        
    def _get_next_message_id(self) -> str:
        """Generate a unique message ID"""
        self._message_counter += 1
        return f"msg_{self._message_counter}"
    
    def add_message(self, sender: str, content: str, is_code: bool = False, 
                   is_streaming: bool = False, tag: str = "ai") -> str:
        """Add a message to the renderer's storage"""
        message_id = self._get_next_message_id()
        message = {
            'sender': sender,
            'content': content,
            'is_code': is_code,
            'is_streaming': is_streaming,
            'tag': tag,
            'message_id': message_id
        }
        self.messages.append(message)
        logger.debug(f"[DEBUG] Added message from {sender}: '{content[:50]}...'")
        return message_id
    
    def append_message(self, sender: str, content: str, is_code: bool = False, tag: str = "ai"):
        """Append a new message and request render"""
        message_id = self.add_message(sender, content, is_code, False, tag)
        # Use immediate render for new messages to ensure they appear quickly
        self.request_render(immediate=True)
        return message_id
    
    def edit_message(self, message_index: int, new_content: str) -> bool:
        """Edit a specific message by index"""
        if 0 <= message_index < len(self.messages):
            old_content = self.messages[message_index]['content']
            self.messages[message_index]['content'] = new_content
            logger.debug(f"[DEBUG][edit_message] Edited message {message_index}: '{old_content}' -> '{new_content}'")
            
            # Use immediate render for edits to show changes quickly
            self.request_render(immediate=True)
            return True
        return False
    
    def update_last_system_switch(self, message: str):
        """Update the last system message with new content"""
        try:
            # Find the last system message
            for msg in reversed(self.messages):
                if msg['sender'] == 'System':
                    msg['content'] = message
                    break
            
            # Use immediate render for system updates to show changes quickly
            self.request_render(immediate=True)
            
        except Exception as e:
            logger.error(f"Error updating last system message: {e}")
            logger.error(traceback.format_exc())
    
    def _get_current_streaming_message(self):
        """Return the current (last) streaming message, or None if not found."""
        for msg in reversed(self.messages):
            if msg.get('is_streaming'):
                return msg
        return None

    def start_streaming_message(self, sender: str, tag: str = "ai") -> str:
        logger.debug(f"[DEBUG] Starting streaming message from {sender} with tag {tag}")
        """Start a streaming message and finalize any previous one."""
        # Finalize any previous streaming message
        for msg in reversed(self.messages):
            if msg.get('is_streaming'):
                msg['is_streaming'] = False
        message_id = self.add_message(sender, "", False, True, tag)
        self.request_render(immediate=True)
        return message_id
    
    def _process_typewriter_chunk(self):
        logger.debug(f"[DEBUG] Processing typewriter chunk")
        """Process a chunk with typewriter effect delay"""
        if self._pending_chunk:
            chunk, sender, message_id, is_code, tag, append = self._pending_chunk
            self._pending_chunk = None
            streaming_msg = self._get_current_streaming_message()
            if streaming_msg is not None:
                logger.debug(f"[TYPEWRITER] Appending chunk: '{chunk}' to streaming message. Current content: '{streaming_msg['content']}'")
            # Find the last streaming message
            for msg in reversed(self.messages):
                if msg['is_streaming']:
                    if append:
                        msg['content'] += chunk
                    else:
                        msg['content'] = chunk
                    msg['is_code'] = is_code
                    msg['tag'] = tag
                    break
            # Force immediate render for streaming messages to ensure real-time updates
            self.request_render(immediate=True)
    
    def update_streaming_message(self, content: str, sender: str, message_id: str = None, 
                               is_code: bool = False, tag: str = "ai", append: bool = True):
        """Update the content of the current streaming message with typewriter effect, or instantly if disabled."""
        try:
            typewriter_enabled = self.config_manager.get("typewriter_enabled", True) if self.config_manager else True
            streaming_msg = self._get_current_streaming_message()
            if not typewriter_enabled:
                # Instantly append chunk and render, skip timer
                if streaming_msg is not None:
                    if append:
                        streaming_msg['content'] += content
                    else:
                        streaming_msg['content'] = content
                    streaming_msg['is_code'] = is_code
                    streaming_msg['tag'] = tag
                    self.request_render(immediate=True)
                else:
                    self.start_streaming_message(sender, tag)
                    self.update_streaming_message(content, sender, message_id, is_code, tag, append)
                return
            # Typewriter effect as before
            if streaming_msg is not None:
                # Store the chunk for typewriter processing - DON'T update content immediately
                self._pending_chunk = (content, sender, message_id, is_code, tag, append)
                if not self._typewriter_timer.isActive():
                    self._typewriter_timer.start()
            else:
                # If no streaming message, start one
                self.start_streaming_message(sender, tag)
                self.update_streaming_message(content, sender, message_id, is_code, tag, append)
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
            
            # Use immediate render for finalization to show completion quickly
            self.request_render(immediate=True)
            
        except Exception as e:
            logger.error(f"Error finalizing streaming message: {e}")
            logger.error(traceback.format_exc())
    
    def clear_chat(self):
        """Clear all messages and render"""
        self.clear_messages()
        # Use immediate render for clearing to show empty state quickly
        self.request_render(immediate=True)
    
    def update_message(self, message_id: str, content: str, is_code: bool = False, tag: str = "ai"):
        """Update an existing message"""
        for msg in self.messages:
            if msg.get('message_id') == message_id:
                msg['content'] = content
                msg['is_code'] = is_code
                msg['tag'] = tag
                break
    
    def get_messages(self) -> List[Dict]:
        """Get all messages"""
        return self.messages.copy()
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages.clear()
        self._message_counter = 0
    
    def sync_messages_from_handler(self, handler_messages: List[Dict]):
        """Sync messages from the streaming handler"""
        self.messages = handler_messages.copy()
        logger.debug(f"[DEBUG] Synced {len(self.messages)} messages from handler")
    
    def request_render(self, immediate: bool = False):
        """Request a render - unified entry point"""
        try:
            # If already rendering, don't schedule another render
            if self._is_rendering:
                logger.debug("[DEBUG] Already rendering, skipping request")
                return
            
            # If immediate render requested, execute now
            if immediate:
                logger.debug("[DEBUG] Executing immediate render")
                self._is_rendering = True
                self._render_chat_display()
                self._is_rendering = False
            else:
                # Otherwise, schedule with debouncing
                logger.debug("[DEBUG] Scheduling debounced render")
                if not self._render_timer.isActive():
                    self._render_timer.start()
                    
        except Exception as e:
            logger.error(f"[ERROR] Error in request_render: {e}")
            logger.error(traceback.format_exc())
            self._is_rendering = False
    
    def _execute_render(self):
        """Execute the actual render - simplified and unified"""
        try:
            # Prevent excessive renders
            self._render_counter += 1
            if self._render_counter > self._max_renders_per_second:
                logger.warning(f"[WARNING] Excessive renders detected: {self._render_counter}. Triggering emergency reset.")
                self._emergency_reset()
                return
                
            # Set rendering flag and start emergency reset timer
            self._is_rendering = True
            self._emergency_reset_timer.start()
            
            # Execute the render
            self._render_chat_display()
            
        except Exception as e:
            logger.error(f"[ERROR] Error in _execute_render: {e}")
            logger.error(traceback.format_exc())
            self.render_error.emit(str(e))
        finally:
            # Reset rendering flag
            self._is_rendering = False
            
            # Stop emergency reset timer
            if self._emergency_reset_timer.isActive():
                self._emergency_reset_timer.stop()
            
            # Emit completion signal
            self.render_completed.emit()
    
    def _emergency_reset(self):
        """Emergency reset if render gets stuck"""
        logger.debug("[DEBUG] Emergency reset triggered")
        self._is_rendering = False
        self._render_counter = 0
        self._last_render_time = 0
        if self._render_timer.isActive():
            self._render_timer.stop()
        
        # Reset render counter periodically

    def _reset_render_counter(self):
        """Reset the render counter periodically"""
        self._render_counter = 0
    
    def _render_chat_display(self):
        """Render the chat display with all messages"""
        try:

            current_thread = QApplication.instance().thread()
            main_thread = self.chat_display.thread()
            
            if current_thread != main_thread:
                self._is_rendering = False
                QTimer.singleShot(0, self._render_chat_display)
                return
            
            self.chat_display.clear()
            prev_was_thinking = False
            
            for msg in self.messages:
                sender = msg['sender']
                content = msg['content']
                is_code = msg['is_code']
                is_streaming = msg['is_streaming']
                tag = msg.get('tag', 'ai')
                message_id = msg.get('message_id', '')
                
                if is_streaming:
                    logger.debug(f"[RENDER] Streaming message for {sender}: '{content}'")

                # Format content
                formatted_content = ''
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
                                # Now render the main answer as the AI bubble
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
            logger.error(f"Error in _render_chat_display: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self._render_timer.isActive():
                self._render_timer.stop()
            if self._emergency_reset_timer.isActive():
                self._emergency_reset_timer.stop()
            self._is_rendering = False
            logger.debug("[DEBUG] Chat renderer cleanup completed")
        except Exception as e:
            logger.error(f"[ERROR] Error during cleanup: {e}")
            logger.error(traceback.format_exc()) 
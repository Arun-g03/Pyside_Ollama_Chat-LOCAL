from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.ui.themes.message_formatter import MessageFormatter

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
        self._emergency_reset_timer.setInterval(500)  # 500ms emergency reset
        self._emergency_reset_timer.setSingleShot(True)
        self._emergency_reset_timer.timeout.connect(self._emergency_reset)
        
        # Render counter to detect excessive renders
        self._render_counter = 0
        self._max_renders_per_second = 60
        self._last_render_time = 0
        
        self.config_manager = config_manager
        
        # Reference to conversation service (single source of truth)
        self.conversation_service = None
        
    def set_conversation_service(self, conversation_service):
        """Set the conversation service reference for single source of truth"""
        logger.debug(f"[RENDERER] Setting conversation service: {conversation_service}")
        self.conversation_service = conversation_service
        logger.debug("[RENDERER] Set conversation service reference")
        
        # Test: Get messages immediately to verify connection
        if conversation_service:
            messages = conversation_service.get_messages()
            logger.debug(f"[RENDERER] Test: Conversation service has {len(messages)} messages")
        else:
            logger.warning("[RENDERER] Conversation service is None")
    
    def get_messages(self) -> List[Dict]:
        """Get messages from conversation service (single source of truth)"""
        if not self.conversation_service:
            logger.warning("[RENDERER] No conversation service available, returning empty list")
            return []
        
        messages = self.conversation_service.get_messages()
        logger.debug(f"[RENDERER] Retrieved {len(messages)} messages from conversation service")
        
        # Debug: Print each message
        for i, msg in enumerate(messages):
            logger.debug(f"[RENDERER] Message {i}: role={msg.get('role')}, content_len={len(msg.get('content', ''))}, id={msg.get('id')}")
        
        return messages
    
    def get_renderable_messages(self) -> List[Dict]:
        """Get messages formatted for rendering (converts role to sender names)"""
        if not self.conversation_service:
            return []
        
        conversation_messages = self.conversation_service.get_messages()
        renderable_messages = []
        
        for msg in conversation_messages:
            # Convert role to sender name
            role = msg.get('role', 'unknown')
            if role == 'assistant':
                sender = self.ai_name
            elif role == 'user':
                sender = 'You'
            elif role == 'system':
                sender = 'System'
            else:
                sender = role
            
            renderable_msg = {
                'sender': sender,
                'content': msg.get('content', ''),
                'is_code': msg.get('is_code', False),
                'is_streaming': msg.get('is_streaming', False),
                'tag': 'ai' if role == 'assistant' else 'user',
                'message_id': msg.get('id', ''),
                'thought': msg.get('thought', '')
            }
            renderable_messages.append(renderable_msg)
        
        logger.debug(f"[RENDERER] Converted {len(renderable_messages)} messages for rendering")
        return renderable_messages
    
    def clear_chat(self):
        """Clear all messages and render"""
        if self.conversation_service:
            self.conversation_service.clear_conversation()
        self.request_render(immediate=True)
    
    def request_render(self, immediate: bool = False):
        """Request a render of the current conversation"""
        if immediate:
            self._execute_render()
        else:
            self._render_timer.start()
    
    def _execute_render(self):
        """Execute the actual rendering"""
        if self._is_rendering:
            logger.debug("[RENDERER] Render already in progress, skipping")
            return
        
        # Emergency stop if too many renders in a short time
        current_time = time.time()
        if current_time - self._last_render_time < 0.1:  # Less than 100ms between renders
            self._render_counter += 1
            if self._render_counter > 10:  # More than 10 rapid renders
                logger.warning("[RENDERER] Too many rapid renders detected, stopping render loop")
                self._emergency_reset_timer.start()
                return
        else:
            self._render_counter = 0
        
        self._last_render_time = current_time
        self._is_rendering = True
        
        try:
            self._render_chat_display()
            self.render_completed.emit()
        except Exception as e:
            logger.error(f"Error during render: {e}")
            self.render_error.emit(str(e))
        finally:
            self._is_rendering = False
    
    def _emergency_reset(self):
        """Emergency reset if rendering gets stuck"""
        logger.warning("[RENDERER] Emergency reset triggered")
        self._is_rendering = False
        self._render_timer.stop()
    
    def _render_chat_display(self):
        """Render the chat display with all messages from conversation service"""
        try:
            # Get messages from conversation service (single source of truth)
            messages = self.get_renderable_messages()
            
            # Debug: Print all message IDs, content lengths, and streaming status before rendering
            logger.debug(f"[RENDER_TRACE] [ChatRenderer] Message list before render: " +
                         ", ".join([f"{{id: {msg.get('message_id') or msg.get('id')}, sender: {msg['sender']}, content_len: {len(msg['content'])}, is_streaming: {msg.get('is_streaming')}}}" for msg in messages]), print_to_terminal=True)
            
            current_thread = QApplication.instance().thread()
            main_thread = self.chat_display.thread()
            
            if current_thread != main_thread:
                self._is_rendering = False
                QTimer.singleShot(0, self._render_chat_display)
                return
            
            self.chat_display.clear()
            prev_was_thinking = False
            
            for msg in messages:
                sender = msg['sender']
                content = msg['content']
                is_code = msg['is_code']
                is_streaming = msg['is_streaming']
                tag = msg.get('tag', 'ai')
                message_id = msg.get('message_id', '')
                thought = msg.get('thought', '')
                
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
                        # Show streaming content with cursor
                        formatted_content = f"{content}<span style='color: #888;'>|</span>"
                else:
                    # Non-streaming content
                    if is_code:
                        formatted_content = f"<pre><code>{content}</code></pre>"
                    else:
                        # Handle thoughts if present
                        if thought and tag == 'ai':
                            # Show thought in a subtle way
                            thought_html = f"""
                            <div style='background-color: #1a1a1a; color: #666; border-radius: 4px; padding: 8px 12px; margin: 4px 0; font-size: 12px; font-style: italic; border-left: 3px solid #444;'>
                                💭 {thought}
                            </div>
                            """
                            self.chat_display.insertHtml(thought_html)
                        
                        # Format regular content
                        from html import escape
                        formatted_content = escape(content)

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
                          <span style='display:none' data-msg-idx='{messages.index(msg)}'></span>
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
                          <span style='display:none' data-msg-idx='{messages.index(msg)}'></span>
                          <b>{sender}:</b> {formatted_content}
                        </div>
                      </td>
                      <td></td>
                    </tr></table>
                    """
                
                self.chat_display.insertHtml(html)
                self.chat_display.insertHtml("<br>")
                
                # Update thinking state
                if is_streaming and not content:
                    prev_was_thinking = True
                else:
                    prev_was_thinking = False
            
            # Scroll to bottom
            self.chat_display.verticalScrollBar().setValue(
                self.chat_display.verticalScrollBar().maximum()
            )
            
        except Exception as e:
            logger.error(f"Error in _render_chat_display: {e}")
            logger.error(traceback.format_exc())
            self.render_error.emit(str(e)) 
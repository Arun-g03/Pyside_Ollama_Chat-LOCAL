"""
Streaming Handler - Business logic for message streaming and management
"""

import logging
import traceback
from typing import List, Dict, Optional, Callable
from PySide6.QtCore import QObject, Signal, QTimer

from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class StreamingHandler(QObject):
    """Streaming Handler - Business logic for message management and streaming"""
    
    # Signals
    message_edited = Signal(int, str)  # Emitted when a message is edited
    
    def __init__(self, render_callback: Callable = None, ai_name: str = "Assistant"):
        super().__init__()
        self.render_callback = render_callback
        self.ai_name = ai_name
        
        # Message storage
        self.messages: List[Dict] = []
        self._message_counter = 0
        
        # Streaming state
        self._stream_buffer = None
        self._stream_timer = QTimer()
        self._stream_timer.setInterval(50)  # ms
        self._stream_timer.timeout.connect(self._flush_stream_buffer)
        
        # Typewriter effect timer - adds small delay between chunks
        self._typewriter_timer = QTimer()
        self._typewriter_timer.setInterval(10)  # 10ms delay for smoother typewriter effect
        self._typewriter_timer.setSingleShot(True)
        self._typewriter_timer.timeout.connect(self._process_typewriter_chunk)
        self._pending_chunk = None
    
    def _get_next_message_id(self) -> str:
        """Generate a unique message ID"""
        self._message_counter += 1
        return f"msg_{self._message_counter}"
    
    def set_render_callback(self, callback: Callable):
        """Set the render callback for UI updates"""
        self.render_callback = callback
    
    def sync_messages_to_renderer(self, renderer):
        """Sync messages to the renderer"""
        if renderer and hasattr(renderer, 'sync_messages_from_handler'):
            renderer.sync_messages_from_handler(self.messages)
    
    def _request_render(self, immediate: bool = False):
        """Request a render through the callback"""
        if self.render_callback:
            try:
                self.render_callback(immediate)
            except Exception as e:
                logger.error(f"Error in render callback: {e}")
                logger.error(traceback.format_exc())
    
    def _flush_stream_buffer(self):
        """Flush the stream buffer"""
        try:
            if self._stream_buffer is None:
                return
            
            # Process stream buffer
            content = self._stream_buffer
            self._stream_buffer = None
            
            # Update the last streaming message
            self.update_streaming_message(content, self.ai_name)
            
        except Exception as e:
            logger.error(f"Error in _flush_stream_buffer: {e}")
            logger.error(traceback.format_exc())
    
    def append_message(self, sender: str, content: str, is_code: bool = False, tag: str = "ai"):
        """Append a new message (user or system)"""
        try:
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
            
            # Request render
            self._request_render()
            
        except Exception as e:
            logger.error(f"Error in append_message: {e}")
            raise
    
    def edit_message(self, message_index: int, new_content: str) -> bool:
        """Edit a specific message by index"""
        if 0 <= message_index < len(self.messages):
            old_content = self.messages[message_index]['content']
            self.messages[message_index]['content'] = new_content
            logger.debug(f"[DEBUG][edit_message] Edited message {message_index}: '{old_content}' -> '{new_content}'")
            
            # Request render
            self._request_render()
            
            # Emit signal for external handling (e.g., conversation saving)
            self.message_edited.emit(message_index, new_content)
            return True
        return False
    
    def get_message_by_id(self, message_id: str) -> int:
        """Get message index by message_id"""
        for i, msg in enumerate(self.messages):
            if msg.get('message_id') == message_id:
                return i
        return -1
    
    def get_editable_messages(self) -> List[Dict]:
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
    
    def get_messages(self) -> List[Dict]:
        """Get all messages as a list of dictionaries"""
        return self.messages.copy()
    
    def start_streaming_message(self, sender: str, tag: str = "ai"):
        """Start a streaming message"""
        message_id = self._get_next_message_id()
        self.messages.append({
            'sender': sender,
            'content': '',
            'is_code': False,
            'is_streaming': True,
            'tag': tag,
            'message_id': message_id
        })
        
        # Request render
        self._request_render()
    
    def _process_typewriter_chunk(self):
        """Process a chunk with typewriter effect delay"""
        if self._pending_chunk:
            chunk, sender, message_id, is_code, tag, append = self._pending_chunk
            self._pending_chunk = None
            
            # Find the last streaming message
            for msg in reversed(self.messages):
                if msg['is_streaming']:
                    if append:
                        # For typewriter effect: append the new content to existing content
                        msg['content'] += chunk
                    else:
                        # For replacement: replace the entire content
                        msg['content'] = chunk
                    msg['is_code'] = is_code
                    msg['tag'] = tag
                    break
            
            # Force immediate render for streaming messages
            self._request_render(immediate=True)
    
    def update_streaming_message(self, content: str, sender: str, message_id: str = None, 
                               is_code: bool = False, tag: str = "ai", append: bool = True):
        """Update the content of the last streaming message with typewriter effect"""
        try:
            # Store the chunk for typewriter processing
            self._pending_chunk = (content, sender, message_id, is_code, tag, append)
            
            # Start the typewriter timer if not already running
            if not self._typewriter_timer.isActive():
                self._typewriter_timer.start()
            
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
            
            # Request render
            self._request_render()
            
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
            
            # Request render
            self._request_render()
            
        except Exception as e:
            logger.error(f"Error updating last system message: {e}")
            logger.error(traceback.format_exc())
    
    def remove_streaming_placeholder(self):
        """Remove the last streaming placeholder message"""
        try:
            # Find and remove the last streaming message
            for i in range(len(self.messages) - 1, -1, -1):
                if self.messages[i]['is_streaming']:
                    del self.messages[i]
                    logger.debug("[DEBUG] Removed streaming placeholder")
                    break
            
            # Request render
            self._request_render()
            
        except Exception as e:
            logger.error(f"Error removing streaming placeholder: {e}")
            logger.error(traceback.format_exc())
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages.clear()
        self._message_counter = 0
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self._stream_timer.isActive():
                self._stream_timer.stop()
            logger.debug("[DEBUG] Streaming handler cleanup completed")
        except Exception as e:
            logger.error(f"[ERROR] Error during cleanup: {e}")
            logger.error(traceback.format_exc()) 
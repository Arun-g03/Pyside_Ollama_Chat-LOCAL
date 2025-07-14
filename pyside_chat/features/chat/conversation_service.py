# Shared imports

from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.pyside_imports import *

"""
Conversation Service - Extracted from ollama_chat.py
Handles conversation state, adding/loading/saving/clearing messages, and persistence.
"""


logger = CustomLogger.get_logger(__name__)

class ConversationService(QObject):
    """Service for managing conversation state and persistence"""
    
    conversation_updated = Signal(list)  # Emits the updated conversation
    auto_save_completed = Signal(str)  # Emits the saved filepath when auto-save completes
    
    def __init__(self, history_dir: str = "User_history/Chat_history", memory_service=None):
        super().__init__()
        self.history_dir = history_dir
        self.memory_service = memory_service
        self.conversation = []  # List of message dicts: {"role": ..., "content": ..., "id": ...}
        self.metadata = {}
        self.current_conversation_id = None
        self._message_counter = 0  # Counter for generating unique message IDs
        self._streaming_message_id = None  # Track current streaming message ID
        self._current_filename = None  # Track the current conversation file
        self.conversation_manager = None  # Will be set by the service manager
        os.makedirs(self.history_dir, exist_ok=True)
    
    def set_memory_service(self, memory_service):
        """Set the memory service for integration"""
        self.memory_service = memory_service
    
    def set_conversation_manager(self, conversation_manager):
        """Set the conversation manager for unified saving"""
        self.conversation_manager = conversation_manager
    
    def _get_next_message_id(self) -> str:
        """Generate a unique message ID"""
        self._message_counter += 1
        return f"msg_{self._message_counter}"
    
    def add_message(self, role: str, content: str, message_id: Optional[str] = None):
        """Add a message to the conversation"""
        # CRITICAL FIX: Prevent empty messages from being added
        if not content or not content.strip():
            logger.warning(f"[EMPTY_MESSAGE] Attempted to add empty {role} message - ignoring")
            return None
            
        if not message_id:
            message_id = self._get_next_message_id()
        
        # Always set is_streaming to False for user/system messages
        message = {
            "role": role, 
            "content": content,
            "id": message_id,
            "is_streaming": False
        }
        # Add thought field for assistant messages
        if role == "assistant":
            message["thought"] = ""
        self.conversation.append(message)
        
        # Add to memory if it's a user message or assistant response
        if self.memory_service and role in ["user", "assistant"]:
            self._add_to_memory(role, content)
        
        self.conversation_updated.emit(self.conversation)
        logger.debug(f"[ID:0019] DEBUG: Added message to conversation: {message}", print_to_terminal=True)
        logger.debug(f"[ID:0018] DEBUG: Total conversation length: {len(self.conversation)}")
        logger.debug(f"[ID:0017] DEBUG: Conversation contents: {[msg.get('role', 'unknown') for msg in self.conversation]}")
        
        return message_id
    
    def start_streaming_message(self, role: str = "assistant") -> str:
        """Start a new streaming message, finalizing any previous one first and resetting streaming state."""
        # Finalize any previous streaming message (with or without content)
        if self._streaming_message_id:
            self.finalize_streaming_message()
        # Reset streaming state
        self._streaming_message_id = None
        logger.debug("[CS_STREAM_RESET] Reset _streaming_message_id before starting new streaming message")
        message_id = self._get_next_message_id()
        message = {
            "role": role,
            "content": "",
            "id": message_id,
            "is_streaming": True
        }
        # Add thought field for assistant messages
        if role == "assistant":
            message["thought"] = ""
        self.conversation.append(message)
        self._streaming_message_id = message_id
        self.conversation_updated.emit(self.conversation)
        logger.debug(f"[CS_STREAM_START] Started new streaming message: {message_id}")
        return message_id
    
    def update_streaming_message(self, chunk: str, append: bool = True, msg_id: str = None, chunk_index: int = None) -> bool:
        """Update the streaming message with a new chunk"""
        try:
            logger.debug(f"[CS_DEBUG] update_streaming_message called with chunk: '{chunk[:50]}...', append: {append}, msg_id: {msg_id}, chunk_index: {chunk_index}")
            
            # Find the streaming message
            target_id = msg_id if msg_id else self._streaming_message_id
            if not target_id:
                logger.error(f"[CS_DEBUG] No target message ID found for streaming update")
                logger.error(f"[CS_DEBUG] Available message IDs: {[msg.get('id') for msg in self.conversation]}")
                return False
                
            # Find the message to update
            target_message = None
            for msg in self.conversation:
                if msg.get('id') == target_id:
                    target_message = msg
                    break
                    
            if not target_message:
                logger.error(f"[CS_DEBUG] Target message {target_id} not found in conversation")
                logger.error(f"[CS_DEBUG] Available message IDs: {[msg.get('id') for msg in self.conversation]}")
                logger.error(f"[CS_DEBUG] This indicates a streaming message ID mismatch!")
                return False
                
            # Log the message state before update
            old_content_length = len(target_message.get('content', ''))
            logger.debug(f"[CS_DEBUG] Before update - Message {target_id}: content_length={old_content_length}, is_streaming={target_message.get('is_streaming')}")
            
            # Update the message content
            if append:
                target_message['content'] += chunk
            else:
                target_message['content'] = chunk
                
            # Update chunk index if provided
            if chunk_index is not None:
                target_message['chunk_index'] = chunk_index
                
            # Log the message state after update
            new_content_length = len(target_message['content'])
            logger.debug(f"[CS_DEBUG] After update - Message {target_id}: content_length={new_content_length}, chunk_index={chunk_index}")
            logger.debug(f"[CS_DEBUG] Content change: +{len(chunk)} chars (from {old_content_length} to {new_content_length})")
            
            return True
            
        except Exception as e:
            logger.error(f"[CS_DEBUG] Error updating streaming message: {e}")
            logger.error(f"[CS_DEBUG] Error traceback: {traceback.format_exc()}")
            return False
    
    def finalize_streaming_message(self) -> bool:
        """Finalize the current streaming message"""
        logger.debug(f"[STREAM_FINALIZE] Attempting to finalize streaming message: {self._streaming_message_id}")
        logger.debug(f"[STREAM_FINALIZE] Current conversation has {len(self.conversation)} messages")
        
        # Debug: Log all messages to see their state
        for i, msg in enumerate(self.conversation):
            logger.debug(f"[STREAM_FINALIZE] Message {i}: id={msg.get('id')}, role={msg.get('role')}, is_streaming={msg.get('is_streaming')}, content_len={len(msg.get('content', ''))}")
        
        if not self._streaming_message_id:
            logger.warning("[STREAM_FINALIZE] No streaming message to finalize")
            return False
        
        for msg in self.conversation:
            if msg.get('id') == self._streaming_message_id and msg.get('is_streaming', False):
                msg['is_streaming'] = False
                # No legacy <think> migration needed; 'thought' is always used
                logger.debug(f"[STREAM_FINALIZE] Finalized streaming message: {msg['id']}")
                self._streaming_message_id = None
                self.conversation_updated.emit(self.conversation)
                return True
        logger.warning(f"[STREAM_FINALIZE] Streaming message id {self._streaming_message_id} not found or already finalized")
        self._streaming_message_id = None
        return False
    
    def get_streaming_message_id(self) -> Optional[str]:
        """Get the current streaming message ID"""
        return self._streaming_message_id
    
    def get_streaming_message_with_content(self) -> Optional[Dict]:
        """Get the streaming message that has actual content"""
        for message in reversed(self.conversation):
            if message.get("is_streaming", False) and message.get("content", "").strip():
                return message
        return None
    
    def get_message_by_id(self, message_id: str) -> Optional[Dict]:
        """Get a message by its ID"""
        for message in self.conversation:
            if message.get("id") == message_id:
                return message
        return None
    
    def update_message_by_id(self, message_id: str, content: str) -> bool:
        """Update a message's content by ID"""
        message = self.get_message_by_id(message_id)
        if message:
            message["content"] = content
            self.conversation_updated.emit(self.conversation)
            return True
        return False

    def _add_to_memory(self, role: str, content: str):
        """Add message to memory service"""
        if not self.current_conversation_id:
            self.current_conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine importance based on role and content length
        importance = 0.5  # Default
        if role == "user":
            importance = min(0.8, 0.3 + (len(content) / 1000) * 0.5)  # Longer user messages are more important
        elif role == "assistant":
            importance = min(0.7, 0.2 + (len(content) / 2000) * 0.5)  # Longer assistant responses are more important
        
        # Add tags based on content
        tags = []
        if "code" in content.lower() or "```" in content:
            tags.append("code")
        if "error" in content.lower() or "problem" in content.lower():
            tags.append("problem-solving")
        if "help" in content.lower() or "assist" in content.lower():
            tags.append("assistance")
        
        memory_type = "conversation"
        if role == "user":
            memory_type = "user_input"
        elif role == "assistant":
            memory_type = "assistant_response"
        
        self.memory_service.add_memory(
            content=content,
            conversation_id=self.current_conversation_id,
            importance=importance,
            tags=tags,
            memory_type=memory_type
        )
    
    def get_messages(self) -> List[Dict]:
        """Get the current conversation messages"""
        logger.debug(f"[ID:0016] DEBUG: get_messages called, returning {len(self.conversation)} messages")
        logger.debug(f"[ID:0015] DEBUG: Message roles: {[msg.get('role', 'unknown') for msg in self.conversation]}")
        
        # DEBUG: Log the actual content of each message
        for i, msg in enumerate(self.conversation):
            logger.debug(f"[CS_DEBUG] Message {i}: {{role: {msg.get('role')}, content_len: {len(msg.get('content', ''))}, content_preview: '{msg.get('content', '')[:50]}', is_streaming: {msg.get('is_streaming')}, id: {msg.get('id')}}}", print_to_terminal=True)
        
        # --- MIGRATION LOGIC: Extract <think>...</think> to 'thought' field if needed (for legacy/finalized messages) ---
        import re
        for msg in self.conversation:
            if msg.get("role") == "assistant" and 'thought' in msg and not msg['thought'] and '<think>' in msg['content'] and '</think>' in msg['content']:
                match = re.search(r'<think>(.*?)</think>', msg['content'], re.DOTALL)
                if match:
                    msg['thought'] = match.group(1).strip()
                    msg['content'] = re.sub(r'<think>.*?</think>', '', msg['content'], flags=re.DOTALL).lstrip('\n')
        # --- END MIGRATION LOGIC ---
        return self.conversation.copy()
    
    def get_context_messages(self) -> List[Dict]:
        """Get messages for context window, including relevant memories"""
        if self.memory_service:
            return self.memory_service.get_context_messages()
        else:
            return self.conversation.copy()
    
    def load_conversation(self, filename: str) -> List[Dict]:
        """Load a conversation from a file"""
        if self.conversation_manager:
            # Use conversation manager to load the conversation
            filepath = os.path.join(self.history_dir, filename)
            try:
                conversation, metadata = self.conversation_manager.load_conversation(filepath)
                self.conversation = conversation
                self.metadata = metadata.to_dict() if hasattr(metadata, 'to_dict') else {}
                
                # Set conversation ID for memory tracking
                self.current_conversation_id = filename.replace(".json", "")
                
                # CRITICAL FIX: Clear any existing streaming state when loading a conversation
                self._streaming_message_id = None
                
                # Ensure all messages have IDs (for backward compatibility)
                for message in self.conversation:
                    if "id" not in message:
                        message["id"] = self._get_next_message_id()
                
                # CRITICAL FIX: Finalize any streaming messages in the loaded conversation
                for message in self.conversation:
                    if message.get("is_streaming", False):
                        logger.debug(f"[LOAD_FIX] Finalizing streaming message {message.get('id')} from loaded conversation")
                        message["is_streaming"] = False
                
                # Update message counter to avoid ID conflicts
                max_id = 0
                if self.conversation:
                    for message in self.conversation:
                        if "id" in message and message["id"].startswith("msg_"):
                            try:
                                msg_num = int(message["id"].split("_")[1])
                                max_id = max(max_id, msg_num)
                            except (ValueError, IndexError):
                                pass
                    self._message_counter = max_id
                
                logger.debug(f"[LOAD_FIX] Loaded conversation with {len(self.conversation)} messages, max_id: {max_id}")
                self.conversation_updated.emit(self.conversation)
                return self.conversation
                
            except Exception as e:
                logger.error(f"[LOAD_ERROR] Failed to load conversation: {e}")
                return []
        else:
            # Fallback to direct file loading if conversation manager is not available
            filepath = os.path.join(self.history_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Handle both old format (just conversation list) and new format (with metadata)
            if isinstance(data, list):
                self.conversation = data
                self.metadata = {}
            else:
                self.conversation = data.get("conversation", [])
                self.metadata = data.get("metadata", {})
            
            # Set conversation ID for memory tracking
            self.current_conversation_id = filename.replace(".json", "")
            
            # CRITICAL FIX: Clear any existing streaming state when loading a conversation
            self._streaming_message_id = None
            
            # Ensure all messages have IDs (for backward compatibility)
            for message in self.conversation:
                if "id" not in message:
                    message["id"] = self._get_next_message_id()
            
            # CRITICAL FIX: Finalize any streaming messages in the loaded conversation
            for message in self.conversation:
                if message.get("is_streaming", False):
                    logger.debug(f"[LOAD_FIX] Finalizing streaming message {message.get('id')} from loaded conversation")
                    message["is_streaming"] = False
            
            # Update message counter to avoid ID conflicts
            max_id = 0
            if self.conversation:
                for message in self.conversation:
                    if "id" in message and message["id"].startswith("msg_"):
                        try:
                            msg_num = int(message["id"].split("_")[1])
                            max_id = max(max_id, msg_num)
                        except (ValueError, IndexError):
                            pass
                self._message_counter = max_id
            
            logger.debug(f"[LOAD_FIX] Loaded conversation with {len(self.conversation)} messages, max_id: {max_id}")
            self.conversation_updated.emit(self.conversation)
            return self.conversation
    
    def clear_conversation(self):
        """Clear the current conversation"""
        self.conversation = []
        self.metadata = {}
        self.current_conversation_id = None
        self._streaming_message_id = None
        self._message_counter = 0
        self._current_filename = None
        self.conversation_updated.emit(self.conversation) 

    def get_streaming_message(self) -> Optional[Dict]:
        """Get the current streaming message"""
        if not self._streaming_message_id:
            return None
        return self.get_message_by_id(self._streaming_message_id)
    
    def update_streaming_message_content(self, content: str) -> bool:
        """Update the content field of the current streaming message"""
        streaming_message = self.get_streaming_message()
        if streaming_message:
            streaming_message['content'] = content
            self.conversation_updated.emit(self.conversation)
            return True
        return False
    
    def update_streaming_message_thought(self, thought: str) -> bool:
        """Update the thought field of the current streaming message"""
        streaming_message = self.get_streaming_message()
        if streaming_message:
            streaming_message['thought'] = thought
            self.conversation_updated.emit(self.conversation)
            return True
        return False
    
    def get_streaming_message_thought(self) -> Optional[str]:
        """Get the thought field of the current streaming message"""
        streaming_message = self.get_streaming_message()
        if streaming_message:
            return streaming_message.get('thought', '')
        return None
    
    def get_streaming_message_content(self) -> Optional[str]:
        """Get the content field of the current streaming message"""
        streaming_message = self.get_streaming_message()
        if streaming_message:
            return streaming_message.get('content', '')
        return None 
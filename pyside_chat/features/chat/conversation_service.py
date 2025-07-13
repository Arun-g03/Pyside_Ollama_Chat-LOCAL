"""
Conversation Service - Extracted from ollama_chat.py
Handles conversation state, adding/loading/saving/clearing messages, and persistence.
"""

import os
import json
from typing import List, Dict, Optional
from PySide6.QtCore import QObject, Signal
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class ConversationService(QObject):
    """Service for managing conversation state and persistence"""
    
    conversation_updated = Signal(list)  # Emits the updated conversation
    
    def __init__(self, history_dir: str = "User_history/Chat_history", memory_service=None):
        super().__init__()
        self.history_dir = history_dir
        self.memory_service = memory_service
        self.conversation = []  # List of message dicts: {"role": ..., "content": ...}
        self.metadata = {}
        self.current_conversation_id = None
        os.makedirs(self.history_dir, exist_ok=True)
    
    def set_memory_service(self, memory_service):
        """Set the memory service for integration"""
        self.memory_service = memory_service
    
    def add_message(self, role: str, content: str, message_id: Optional[str] = None):
        """Add a message to the conversation"""
        message = {"role": role, "content": content}
        if message_id:
            message["id"] = message_id
        self.conversation.append(message)
        
        # Add to memory if it's a user message or assistant response
        if self.memory_service and role in ["user", "assistant"]:
            self._add_to_memory(role, content)
        
        self.conversation_updated.emit(self.conversation)
        logger.debug(f"[ID:0019] DEBUG: Added message to conversation: {message}", print_to_terminal=True)
        logger.debug(f"[ID:0018] DEBUG: Total conversation length: {len(self.conversation)}")
        logger.debug(f"[ID:0017] DEBUG: Conversation contents: {[msg.get('role', 'unknown') for msg in self.conversation]}")

    def _add_to_memory(self, role: str, content: str):
        """Add message to memory service"""
        if not self.current_conversation_id:
            from datetime import datetime
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
        return self.conversation.copy()
    
    def get_context_messages(self) -> List[Dict]:
        """Get messages for context window, including relevant memories"""
        if self.memory_service:
            return self.memory_service.get_context_messages()
        else:
            return self.conversation.copy()
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """Save the conversation to a file"""
        if not filename:
            from datetime import datetime
            filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.history_dir, filename)
        
        # Create save data with metadata
        save_data = {
            "metadata": {
                "created": self.metadata.get("created"),
                "last_modified": datetime.now().isoformat(),
                "model": self.metadata.get("model"),
                "personality": self.metadata.get("personality"),
                "message_count": len(self.conversation),
                "auto_save_enabled": True
            },
            "conversation": self.conversation
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        # Create summary if conversation is long enough
        if self.memory_service and len(self.conversation) >= 10:
            self.memory_service.summarize_conversation(self.conversation, self.current_conversation_id)
        
        return filepath
    
    def load_conversation(self, filename: str) -> List[Dict]:
        """Load a conversation from a file"""
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
        
        self.conversation_updated.emit(self.conversation)
        return self.conversation
    
    def clear_conversation(self):
        """Clear the current conversation"""
        self.conversation = []
        self.metadata = {}
        self.current_conversation_id = None
        self.conversation_updated.emit(self.conversation)
    
    def auto_save(self):
        """Auto-save the current conversation (overwrites last file)"""
        # This is a placeholder; in a real app, you'd track the current file
        self.save_conversation() 
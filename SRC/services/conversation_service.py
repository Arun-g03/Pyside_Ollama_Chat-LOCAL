"""
Conversation Service - Extracted from ollama_chat.py
Handles conversation state, adding/loading/saving/clearing messages, and persistence.
"""

import os
import json
from typing import List, Dict, Optional
from PySide6.QtCore import QObject, Signal
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class ConversationService(QObject):
    """Service for managing conversation state and persistence"""
    
    conversation_updated = Signal(list)  # Emits the updated conversation
    
    def __init__(self, history_dir: str = "chat_history"):
        super().__init__()
        self.history_dir = history_dir
        self.conversation = []  # List of message dicts: {"role": ..., "content": ...}
        self.metadata = {}
        os.makedirs(self.history_dir, exist_ok=True)
    
    def add_message(self, role: str, content: str, message_id: Optional[str] = None):
        """Add a message to the conversation"""
        message = {"role": role, "content": content}
        if message_id:
            message["id"] = message_id
        self.conversation.append(message)
        self.conversation_updated.emit(self.conversation)
        logger.debug(f"DEBUG: Added message to conversation: {message}")

    
    def get_messages(self) -> List[Dict]:
        """Get the current conversation messages"""
        return self.conversation.copy()
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """Save the conversation to a file"""
        if not filename:
            from datetime import datetime
            filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.history_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.conversation, f, indent=2, ensure_ascii=False)
        return filepath
    
    def load_conversation(self, filename: str) -> List[Dict]:
        """Load a conversation from a file"""
        filepath = os.path.join(self.history_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            self.conversation = json.load(f)
        self.conversation_updated.emit(self.conversation)
        return self.conversation
    
    def clear_conversation(self):
        """Clear the current conversation"""
        self.conversation = []
        self.conversation_updated.emit(self.conversation)
    
    def auto_save(self):
        """Auto-save the current conversation (overwrites last file)"""
        # This is a placeholder; in a real app, you'd track the current file
        self.save_conversation() 
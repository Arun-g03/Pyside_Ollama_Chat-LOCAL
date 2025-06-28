"""
Conversation Metadata Model - Extracted from ollama_chat.py
Handles conversation metadata and persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import json
import os
from PySide6.QtCore import QObject, Signal


@dataclass
class ConversationMetadata:
    """Data class for storing conversation metadata"""
    
    created: Optional[str] = None
    last_modified: Optional[str] = None
    model: Optional[str] = None
    personality: Optional[str] = None
    message_count: int = 0
    current_conversation_file: Optional[str] = None
    auto_save_enabled: bool = True
    
    def __post_init__(self):
        """Initialize default values after object creation"""
        if self.created is None:
            self.created = datetime.now().isoformat()
        if self.last_modified is None:
            self.last_modified = datetime.now().isoformat()
    
    def update_timestamp(self) -> None:
        """Update the last modified timestamp"""
        self.last_modified = datetime.now().isoformat()
    
    def update_message_count(self, count: int) -> None:
        """Update the message count"""
        self.message_count = count
        self.update_timestamp()
    
    def update_model(self, model: str) -> None:
        """Update the model information"""
        self.model = model
        self.update_timestamp()
    
    def update_personality(self, personality: str) -> None:
        """Update the personality information"""
        self.personality = personality
        self.update_timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for JSON serialization"""
        return {
            "created": self.created,
            "last_modified": self.last_modified,
            "model": self.model,
            "personality": self.personality,
            "message_count": self.message_count,
            "auto_save_enabled": self.auto_save_enabled
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationMetadata':
        """Create metadata from dictionary"""
        return cls(
            created=data.get("created"),
            last_modified=data.get("last_modified"),
            model=data.get("model"),
            personality=data.get("personality"),
            message_count=data.get("message_count", 0),
            auto_save_enabled=data.get("auto_save_enabled", True)
        )
    
    def reset(self) -> None:
        """Reset metadata to initial state"""
        self.created = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()
        self.model = None
        self.personality = None
        self.message_count = 0
        self.current_conversation_file = None
    
    def get_formatted_created_time(self) -> str:
        """Get formatted creation time for display"""
        if self.created:
            try:
                created_dt = datetime.fromisoformat(self.created)
                return created_dt.strftime("%Y-%m-%d %H:%M")
            except:
                return self.created
        return "Unknown"
    
    def get_formatted_modified_time(self) -> str:
        """Get formatted last modified time for display"""
        if self.last_modified:
            try:
                modified_dt = datetime.fromisoformat(self.last_modified)
                return modified_dt.strftime("%Y-%m-%d %H:%M")
            except:
                return self.last_modified
        return "Unknown"
    
    def get_display_info(self) -> str:
        """Get formatted display information"""
        created_str = self.get_formatted_created_time()
        model_str = self.model or "Unknown"
        personality_str = self.personality or "Unknown"
        
        return f"Messages: {self.message_count} | Model: {model_str} | Personality: {personality_str} | Created: {created_str}"


class ConversationManager(QObject):
    """Manager for handling conversation persistence and metadata"""
    
    # Signals
    metadata_updated = Signal()  # Emitted when metadata is updated
    
    def __init__(self, history_dir: str = "chat_history"):
        super().__init__()
        self.history_dir = history_dir
        self.metadata = ConversationMetadata()
        
        # Create history directory if it doesn't exist
        os.makedirs(self.history_dir, exist_ok=True)
    
    def save_conversation(self, conversation: list, filename: Optional[str] = None) -> str:
        """
        Save conversation with metadata to file
        
        Args:
            conversation: List of conversation messages
            filename: Optional filename, will generate one if not provided
            
        Returns:
            Path to saved file
        """
        # Update metadata
        self.metadata.update_message_count(len(conversation))
        self.metadata.update_timestamp()
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = self.metadata.model or "unknown"
            filename = f"{model_name}_{timestamp}.json"
        
        filepath = os.path.join(self.history_dir, filename)
        
        # Prepare save data
        save_data = {
            "metadata": self.metadata.to_dict(),
            "conversation": conversation
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        self.metadata.current_conversation_file = filepath
        self.metadata_updated.emit()
        return filepath
    
    def load_conversation(self, filepath: str) -> tuple[list, ConversationMetadata]:
        """
        Load conversation and metadata from file
        
        Args:
            filepath: Path to conversation file
            
        Returns:
            Tuple of (conversation, metadata)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old format (just conversation) and new format (with metadata)
            if isinstance(data, list):
                # Old format - just conversation array
                conversation = data
                metadata = ConversationMetadata()
            else:
                # New format - with metadata
                conversation = data.get("conversation", [])
                metadata = ConversationMetadata.from_dict(data.get("metadata", {}))
            
            # Update current file path
            metadata.current_conversation_file = filepath
            
            return conversation, metadata
            
        except Exception as e:
            raise ValueError(f"Failed to load conversation: {str(e)}")
    
    def auto_save_conversation(self, conversation: list) -> Optional[str]:
        """
        Auto-save conversation if enabled
        
        Args:
            conversation: List of conversation messages
            
        Returns:
            Path to saved file if saved, None otherwise
        """
        if not self.metadata.auto_save_enabled or not conversation:
            return None
        
        # Update metadata
        self.metadata.update_message_count(len(conversation))
        
        # Create filename if not exists
        if not self.metadata.current_conversation_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.metadata.current_conversation_file = os.path.join(
                self.history_dir, f"conversation_{timestamp}.json"
            )
        
        # Save conversation with metadata
        try:
            save_data = {
                "metadata": self.metadata.to_dict(),
                "conversation": conversation
            }
            with open(self.metadata.current_conversation_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            self.metadata_updated.emit()
            return self.metadata.current_conversation_file
            
        except Exception as e:
            print(f"Auto-save failed: {e}")
            return None
    
    def list_conversations(self) -> list[tuple[str, ConversationMetadata]]:
        """
        List all saved conversations with their metadata
        
        Returns:
            List of tuples (filepath, metadata)
        """
        conversations = []
        
        if not os.path.exists(self.history_dir):
            return conversations
        
        for filename in os.listdir(self.history_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.history_dir, filename)
                try:
                    conversation, metadata = self.load_conversation(filepath)
                    conversations.append((filepath, metadata))
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    # Add with basic metadata even if corrupted
                    basic_metadata = ConversationMetadata()
                    basic_metadata.current_conversation_file = filepath
                    conversations.append((filepath, basic_metadata))
        
        # Sort by last modified time (newest first)
        conversations.sort(key=lambda x: x[1].last_modified or "", reverse=True)
        return conversations
    
    def delete_conversation(self, filepath: str) -> bool:
        """
        Delete a conversation file
        
        Args:
            filepath: Path to conversation file
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"Failed to delete {filepath}: {e}")
            return False
    
    def rename_conversation(self, old_filepath: str, new_filepath: str) -> bool:
        """
        Rename a conversation file and update references
        
        Args:
            old_filepath: Original file path
            new_filepath: New file path
            
        Returns:
            True if renamed successfully, False otherwise
        """
        try:
            # Rename the file
            os.rename(old_filepath, new_filepath)
            
            # Update current conversation file reference if this was the current one
            if self.metadata.current_conversation_file == old_filepath:
                self.metadata.current_conversation_file = new_filepath
                self.metadata_updated.emit()
            
            return True
        except Exception as e:
            print(f"Failed to rename {old_filepath} to {new_filepath}: {e}")
            return False
    
    def clear_current_conversation(self) -> None:
        """Clear current conversation metadata"""
        self.metadata.reset()
        self.metadata_updated.emit()
    
    def get_current_metadata(self) -> ConversationMetadata:
        """Get current metadata"""
        return self.metadata
    
    def set_auto_save_enabled(self, enabled: bool) -> None:
        """Enable or disable auto-save"""
        self.metadata.auto_save_enabled = enabled
        self.metadata_updated.emit() 
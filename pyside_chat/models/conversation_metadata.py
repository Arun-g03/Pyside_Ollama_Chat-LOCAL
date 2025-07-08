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
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


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
    ai_generated_name: Optional[str] = None  # AI-generated name for the conversation
    
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
    
    def update_ai_generated_name(self, name: str) -> None:
        """Update the AI-generated name"""
        self.ai_generated_name = name
        self.update_timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for JSON serialization"""
        return {
            "created": self.created,
            "last_modified": self.last_modified,
            "model": self.model,
            "personality": self.personality,
            "message_count": self.message_count,
            "auto_save_enabled": self.auto_save_enabled,
            "ai_generated_name": self.ai_generated_name
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
            auto_save_enabled=data.get("auto_save_enabled", True),
            ai_generated_name=data.get("ai_generated_name")
        )
    
    def reset(self) -> None:
        """Reset metadata to initial state"""
        self.created = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()
        self.model = None
        self.personality = None
        self.message_count = 0
        self.current_conversation_file = None
        self.ai_generated_name = None
    
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
    
    def get_display_name(self) -> str:
        """Get the display name for the conversation"""
        return self.ai_generated_name if self.ai_generated_name else "New Chat"


class ConversationManager(QObject):
    """Manager for handling conversation persistence and metadata"""
    
    # Signals
    metadata_updated = Signal()  # Emitted when metadata is updated
    
    def __init__(self, history_dir: str = "User_history/Chat_history"):
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
    
    def update_conversation_name(self, filepath: str, ai_generated_name: str) -> Optional[str]:
        """
        Update the AI-generated name for a conversation and rename the file
        
        Args:
            filepath: Path to the conversation file
            ai_generated_name: The AI-generated name
            
        Returns:
            New filepath if successful, None otherwise
        """
        try:
            logger.debug(f"[ID:0210] Updating conversation name for {filepath} to '{ai_generated_name}'")
            
            # Load the conversation
            conversation, metadata = self.load_conversation(filepath)
            logger.debug(f"[ID:0209] Loaded conversation with {len(conversation)} messages")
            logger.debug(f"[ID:0208] Original metadata ai_generated_name: {metadata.ai_generated_name}")
            
            # Update the AI-generated name
            metadata.update_ai_generated_name(ai_generated_name)
            logger.debug(f"[ID:0207] Updated metadata ai_generated_name: {metadata.ai_generated_name}")
            
            # Create a safe filename from the AI-generated name
            safe_filename = self._create_safe_filename(ai_generated_name)
            logger.debug(f"[ID:0206] Created safe filename: {safe_filename}")
            
            # Generate new filepath
            new_filepath = os.path.join(self.history_dir, safe_filename)
            logger.debug(f"[ID:0205] New filepath: {new_filepath}")
            
            # Check if new filename already exists
            if os.path.exists(new_filepath) and new_filepath != filepath:
                # Add timestamp to make it unique
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name_without_ext = os.path.splitext(safe_filename)[0]
                safe_filename = f"{name_without_ext}_{timestamp}.json"
                new_filepath = os.path.join(self.history_dir, safe_filename)
                logger.debug(f"[ID:0204] File exists, using timestamped filename: {new_filepath}")
            
            # Save the updated conversation to the new file
            save_data = {
                "metadata": metadata.to_dict(),
                "conversation": conversation
            }
            
            logger.debug(f"[ID:0203] Saving with metadata: {save_data['metadata']}")
            
            with open(new_filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            # Delete the old file if it's different from the new one
            if new_filepath != filepath:
                try:
                    os.remove(filepath)
                    logger.debug(f"[ID:0202] Deleted old file: {filepath}")
                except Exception as e:
                    logger.warning(f"[ID:0201] Failed to remove old file {filepath}: {e}")
            
            # Update current conversation file reference if this was the current one
            if self.metadata.current_conversation_file == filepath:
                self.metadata.current_conversation_file = new_filepath
                logger.debug(f"[ID:0200] Updated current conversation file reference to: {new_filepath}")
            
            self.metadata_updated.emit()
            logger.debug(f"[ID:0199] Successfully updated conversation name, returning: {new_filepath}")
            return new_filepath
            
        except Exception as e:
            logger.error(f"[ID:0198] Failed to update conversation name: {str(e)}")
            return None
    
    def _create_safe_filename(self, ai_generated_name: str) -> str:
        """
        Create a safe filename from the AI-generated name
        
        Args:
            ai_generated_name: The AI-generated name
            
        Returns:
            Safe filename with .json extension and timestamp
        """
        # Remove or replace invalid characters
        import re
        
        # Replace invalid filename characters with underscores
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', ai_generated_name)
        
        # Replace multiple spaces/underscores with single underscore
        safe_name = re.sub(r'[_\s]+', '_', safe_name)
        
        # Remove leading/trailing underscores and spaces
        safe_name = safe_name.strip('_ ')
        
        # Limit length to avoid filesystem issues (leave room for timestamp)
        if len(safe_name) > 80:
            safe_name = safe_name[:80]
        
        # Ensure it's not empty
        if not safe_name:
            safe_name = "unnamed_conversation"
        
        # Add timestamp to ensure uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = f"{safe_name}_{timestamp}"
        
        # Add .json extension
        if not safe_name.endswith('.json'):
            safe_name += '.json'
        
        return safe_name
    
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
        logger.debug(f"[ID:0197] Auto-save attempt - enabled: {self.metadata.auto_save_enabled}, conversation length: {len(conversation) if conversation else 0}")
        
        if not self.metadata.auto_save_enabled:
            logger.debug("[ID:0196] Auto-save skipped: auto_save_enabled is False")
            return None
            
        # Skip saving if conversation is empty and we already have a file with content
        if not conversation and self.metadata.current_conversation_file and os.path.exists(self.metadata.current_conversation_file):
            try:
                with open(self.metadata.current_conversation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    existing_conversation = data.get("conversation", []) if isinstance(data, dict) else data
                    if len(existing_conversation) > 0:
                        logger.debug("[ID:0195] Auto-save skipped: conversation is empty and existing file has content")
                        return None
            except:
                pass  # If we can't read the file, proceed with saving

        # Create filename if not exists (new conversation)
        if not self.metadata.current_conversation_file:
            if self.metadata.ai_generated_name:
                safe_filename = self._create_safe_filename(self.metadata.ai_generated_name)
                self.metadata.current_conversation_file = os.path.join(
                    self.history_dir, safe_filename
                )
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.metadata.current_conversation_file = os.path.join(
                    self.history_dir, f"conversation_{timestamp}.json"
                )
        
        # Preserve existing AI-generated name if the file already exists
        if self.metadata.current_conversation_file and os.path.exists(self.metadata.current_conversation_file):
            try:
                with open(self.metadata.current_conversation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "metadata" in data:
                        existing_ai_name = data["metadata"].get("ai_generated_name")
                        if existing_ai_name and not self.metadata.ai_generated_name:
                            logger.debug(f"[ID:0194] Preserving existing AI name: {existing_ai_name}")
                            self.metadata.update_ai_generated_name(existing_ai_name)
            except Exception as e:
                logger.debug(f"[ID:0193] Could not read existing file for AI name preservation: {e}")
        
        # Update metadata
        self.metadata.update_message_count(len(conversation))
        
        # Save conversation with metadata
        try:
            save_data = {
                "metadata": self.metadata.to_dict(),
                "conversation": conversation
            }
            with open(self.metadata.current_conversation_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            self.metadata_updated.emit()
            logger.debug(f"[ID:0192] Auto-save successful: {self.metadata.current_conversation_file}")
            return self.metadata.current_conversation_file
            
        except Exception as e:
            logger.debug(f"[ID:0191] Auto-save failed: {e}",print_to_terminal=True)
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
                    logger.debug(f"[ID:0190] Error reading {filename}: {e}",print_to_terminal=True)
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
            logger.debug(f"[ID:0189] Failed to delete {filepath}: {e}",print_to_terminal=True)
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
            logger.debug(f"[ID:0188] Failed to rename {old_filepath} to {new_filepath}: {e}",print_to_terminal=True)
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
    
    def find_blank_conversation(self) -> Optional[str]:
        """
        Find the most recent blank conversation (0 messages)
        
        Returns:
            Filepath of the most recent blank conversation, or None if none found
        """
        conversations = self.list_conversations()
        
        # Look for conversations with 0 messages
        blank_conversations = [
            (filepath, metadata) for filepath, metadata in conversations 
            if metadata.message_count == 0
        ]
        
        if blank_conversations:
            # Return the most recent blank conversation (first in the sorted list)
            return blank_conversations[0][0]
        
        return None 
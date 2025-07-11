"""
Personality Service - Main personality management service

This module provides the main interface for personality management,
coordinating between the loader, formatter, and other components.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import os

from pyside_chat.features.personality.models.personality_types import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
from pyside_chat.features.personality.loader import PersonalityLoader
from pyside_chat.features.personality.formatter import PersonalityFormatter
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class PersonalityService:
    """Main service for managing AI personalities"""
    
    def __init__(self, personalities_dir: str = "pyside_chat/Personalities/personality_Profiles"):
        self.personalities_dir = personalities_dir
        self.personalities: Dict[str, Dict[str, Any]] = {}
        self.personality_file_paths: Dict[str, str] = {}  # Track file paths for each personality
        self.current_personality: Optional[str] = None
        
        # Initialize components
        self.loader = PersonalityLoader(personalities_dir)
        self.formatter = PersonalityFormatter()
        
        # Load personalities
        self._initialize_personalities()
    
    def _initialize_personalities(self):
        """Initialize personalities by loading from files"""
        self.personalities = {}
        self.personality_file_paths = {}
        
        # Load all personalities and track their file paths
        all_personalities = self.loader.load_all_personalities()
        all_file_paths = self.loader.find_personality_files()
        
        for filepath in all_file_paths:
            personality_name = self.loader.extract_personality_name(filepath)
            if personality_name in all_personalities:
                self.personalities[personality_name] = all_personalities[personality_name]
                self.personality_file_paths[personality_name] = filepath
        
        # Set default current personality if available
        if self.personalities:
            # Prefer assistant personality, otherwise use first available
            if "assistant" in self.personalities:
                self.current_personality = "assistant"
            else:
                self.current_personality = list(self.personalities.keys())[0]
    
    def is_system_personality(self, name: str) -> bool:
        """Check if a personality is a system personality (read-only)"""
        if name not in self.personality_file_paths:
            return False
        
        filepath = self.personality_file_paths[name]
        # System personalities are those NOT in the Custom folder
        return "Custom" not in filepath
    
    def is_custom_personality(self, name: str) -> bool:
        """Check if a personality is a custom personality (editable/deletable)"""
        return not self.is_system_personality(name)
    
    def get_system_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Get system personalities (read-only)"""
        system_personalities = {}
        for name, personality_data in self.personalities.items():
            if self.is_system_personality(name):
                system_personalities[name] = personality_data
        return system_personalities
    
    def get_custom_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Get custom personalities (editable/deletable)"""
        custom_personalities = {}
        for name, personality_data in self.personalities.items():
            if self.is_custom_personality(name):
                custom_personalities[name] = personality_data
        return custom_personalities
    
    def get_available_personalities(self) -> List[str]:
        """Get list of all available personality names"""
        return sorted(list(self.personalities.keys()))
    
    def get_personality(self, name: str) -> Optional[Dict[str, Any]]:
        """Get personality by name"""
        return self.personalities.get(name)
    
    def set_current_personality(self, name: str) -> bool:
        """Set the current active personality"""
        if name in self.personalities:
            self.current_personality = name
            return True
        return False
    
    def get_current_personality(self) -> Optional[Dict[str, Any]]:
        """Get the current active personality"""
        if self.current_personality:
            return self.get_personality(self.current_personality)
        return None
    
    def create_custom_personality(self, name: str, traits: PersonalityTraits, prompt: PersonalityPrompt, 
                                 config: PersonalityConfig = None, metadata: PersonalityMetadata = None) -> bool:
        """Create a new custom personality in the Custom folder"""
        try:
            # Ensure the personality name doesn't conflict with system personalities
            if name in self.personalities and self.is_system_personality(name):
                logger.debug(f"Cannot create custom personality '{name}' - name conflicts with system personality",print_to_terminal=True)
                return False
            
            # Create personality data
            personality_data = self.loader.create_personality_data(traits, prompt, config, metadata)
            
            # Ensure custom personalities are saved to the Custom folder
            custom_name = f"Custom.{name}" if not name.startswith("Custom.") else name
            
            # Save to file in Custom folder
            if self.loader.save_personality_to_file(custom_name, personality_data):
                # Add to memory
                self.personalities[custom_name] = personality_data
                # Update file path tracking
                filepath = self.loader.find_personality_file_by_name(custom_name)
                if filepath:
                    self.personality_file_paths[custom_name] = filepath
                return True
            return False
        except Exception as e:
            logger.debug(f"Error creating personality {name}: {e}",print_to_terminal=True)
            return False
    
    def delete_custom_personality(self, name: str) -> bool:
        """Delete a custom personality (only if it's in the Custom folder)"""
        if name not in self.personalities:
            return False
        
        # Check if it's a system personality
        if self.is_system_personality(name):
            logger.debug(f"Cannot delete system personality '{name}'",print_to_terminal=True)
            return False
        
        try:
            # Delete file
            if self.loader.delete_personality_file(name):
                # Remove from memory
                del self.personalities[name]
                if name in self.personality_file_paths:
                    del self.personality_file_paths[name]
                
                # Update current personality if it was deleted
                if self.current_personality == name:
                    if self.personalities:
                        self.current_personality = list(self.personalities.keys())[0]
                    else:
                        self.current_personality = None
                
                return True
            return False
        except Exception as e:
            logger.debug(f"Error deleting personality {name}: {e}",print_to_terminal=True)
            return False
    
    def update_custom_personality(self, name: str, traits: PersonalityTraits, prompt: PersonalityPrompt, 
                                 config: PersonalityConfig = None, metadata: PersonalityMetadata = None) -> bool:
        """Update a custom personality (only if it's in the Custom folder)"""
        if name not in self.personalities:
            return False
        
        # Check if it's a system personality
        if self.is_system_personality(name):
            logger.debug(f"Cannot update system personality '{name}'",print_to_terminal=True)
            return False
        
        try:
            # Create updated personality data
            personality_data = self.loader.create_personality_data(traits, prompt, config, metadata)
            
            # Save to file
            if self.loader.save_personality_to_file(name, personality_data):
                # Update in memory
                self.personalities[name] = personality_data
                return True
            return False
        except Exception as e:
            logger.debug(f"Error updating personality {name}: {e}",print_to_terminal=True)
            return False
    
    def refresh_personalities(self) -> bool:
        """Refresh personalities from disk, reloading all JSON files"""
        try:
            # Store current personality to restore it after refresh
            current_personality = self.current_personality
            
            # Reload personalities
            self._initialize_personalities()
            
            # Restore current personality if it still exists
            if current_personality and current_personality in self.personalities:
                self.current_personality = current_personality
            elif self.personalities:
                # Set to first available personality if current one no longer exists
                self.current_personality = list(self.personalities.keys())[0]
            
            return True
        except Exception as e:
            logger.debug(f"Error refreshing personalities: {e}",print_to_terminal=True)
            return False
    
    def format_prompt_with_personality(self, user_input: str, context: str = "") -> str:
        """Format a prompt using the current personality's prompt templates"""
        current_personality = self.get_current_personality()
        if not current_personality:
            # Default to assistant personality if available, otherwise use first available
            if "assistant" in self.personalities:
                current_personality = self.personalities["assistant"]
            elif self.personalities:
                # Use the first available personality
                first_personality_name = list(self.personalities.keys())[0]
                current_personality = self.personalities[first_personality_name]
            else:
                # No personalities available, return user input as-is
                return user_input
        
        return self.formatter.format_prompt_with_personality(current_personality, user_input, context)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current personality"""
        current_personality = self.get_current_personality()
        if current_personality:
            return self.formatter.get_system_prompt(current_personality)
        
        # Fallback to assistant personality if available, otherwise use first available
        if "assistant" in self.personalities:
            return self.formatter.get_system_prompt(self.personalities["assistant"])
        elif self.personalities:
            # Use the first available personality
            first_personality_name = list(self.personalities.keys())[0]
            return self.formatter.get_system_prompt(self.personalities[first_personality_name])
        else:
            # No personalities available, return empty string
            return ""
    
    def get_personality_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a personality"""
        personality = self.get_personality(name)
        return self.formatter.get_personality_info(personality)
    
    def get_personality_config(self, name: str = None) -> Optional[PersonalityConfig]:
        """Get configuration for a personality"""
        if name is None:
            name = self.current_personality
        
        personality = self.get_personality(name)
        if personality and "config" in personality:
            config_data = personality["config"]
            return PersonalityConfig(**config_data)
        return None
    
    def update_personality_metadata(self, name: str, **kwargs) -> bool:
        """Update metadata for a personality"""
        personality = self.get_personality(name)
        if not personality:
            return False
        
        # Get current metadata or create new
        metadata_data = personality.get("metadata", {})
        metadata = PersonalityMetadata(**metadata_data)
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
        
        # Update last modified
        metadata.last_modified = datetime.now().isoformat()
        
        # Save back to personality
        personality["metadata"] = metadata.__dict__
        
        # Save to file
        return self.loader.save_personality_to_file(name, personality)
    
    def build_comprehensive_system_prompt(self, memory_service=None) -> str:
        """Build a comprehensive system prompt with pronoun guidance"""
        current_personality = self.get_current_personality()
        if not current_personality:
            return ""
        
        # Get base system prompt from formatter
        base_prompt = self.formatter.build_comprehensive_system_prompt(current_personality)
        
        return base_prompt
    
    def get_user_context_messages(self, memory_service=None, is_new_conversation=False) -> List[Dict]:
        """Get dynamic user context messages that should be added to conversation"""
        context_messages = []
        
        # Get current personality for AI name
        current_personality = self.get_current_personality()
        ai_name = "AI Assistant"
        if current_personality and "traits" in current_personality:
            ai_name = current_personality["traits"].get("name", "AI Assistant")
        
        if memory_service:
            try:
                user_info = memory_service.get_user_info()
                if user_info:
                    # Create context messages for user information
                    context_text = "USER CONTEXT:\n"
                    
                    # Add conversation context
                    if is_new_conversation:
                        context_text += "CONVERSATION STATUS: This is a NEW conversation.\n"
                        context_text += f"- Introduce yourself as '{ai_name}' and greet the user\n"
                    else:
                        context_text += "CONVERSATION STATUS: Continuing existing conversation.\n"
                    
                    context_text += "\nUSER INFORMATION:\n"
                    
                    if "name" in user_info:
                        context_text += f"- Name: {user_info['name']}\n"
                    
                    if "location" in user_info:
                        context_text += f"- Location: {user_info['location']}\n"
                    
                    # Add preferences
                    preferences = {k: v for k, v in user_info.items() if k.startswith('favorite_') or k.startswith('preference_')}
                    if preferences:
                        context_text += "- Preferences:\n"
                        for key, value in preferences.items():
                            if key.startswith('favorite_'):
                                category = key.replace('favorite_', '')
                                context_text += f"  * Favorite {category}: {value}\n"
                            elif key.startswith('preference_'):
                                category = key.replace('preference_', '')
                                context_text += f"  * {category}: {value}\n"
                    
                    context_text += "\nINSTRUCTIONS:"
                    context_text += "\n- Use this information to personalize responses"
                    context_text += f"\n- When asked about your name, say 'My name is {ai_name}'"
                    context_text += f"\n- When asked about the user's name, say 'Your name is {user_info.get('name', 'unknown')}'"
                    context_text += f"\n- Never say you don't have a name or that you're just an AI assistant"
                    context_text += f"\n- Always identify yourself as '{ai_name}'"
                    
                    if is_new_conversation:
                        context_text += f"\n- Introduce yourself as '{ai_name}' and be welcoming"
                    
                    context_messages.append({
                        "role": "system", 
                        "content": context_text.strip()
                    })
                    
                    logger.debug(f"Generated user context messages: {user_info}", print_to_terminal=True)
                    logger.debug(f"New conversation: {is_new_conversation}", print_to_terminal=True)
                    logger.debug(f"User context content: {context_text.strip()}", print_to_terminal=True)
                        
            except Exception as e:
                logger.debug(f"Error generating user context: {e}", print_to_terminal=True)
        
        return context_messages
    
    def get_personality_categories(self) -> List[str]:
        """Get list of all personality categories"""
        categories = set()
        
        for personality_data in self.personalities.values():
            metadata = personality_data.get("metadata", {})
            category = metadata.get("category", "general")
            categories.add(category)
        
        return sorted(list(categories))
    
    def get_personalities_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Get personalities by category"""
        categorized_personalities = {}
        
        for name, personality_data in self.personalities.items():
            metadata = personality_data.get("metadata", {})
            personality_category = metadata.get("category", "general")
            
            if personality_category == category:
                categorized_personalities[name] = personality_data
        
        return categorized_personalities
    
    def get_personalities_by_folder(self, folder_name: str) -> Dict[str, Dict[str, Any]]:
        """Get personalities by folder name"""
        folder_personalities = {}
        
        for name, personality_data in self.personalities.items():
            if name.startswith(folder_name + "."):
                folder_personalities[name] = personality_data
        
        return folder_personalities
    
    def search_personalities(self, query: str) -> List[str]:
        """Search personalities by name, description, or tags"""
        query = query.lower()
        matching_personalities = []
        
        for name, personality_data in self.personalities.items():
            traits = personality_data.get("traits", {})
            metadata = personality_data.get("metadata", {})
            
            # Search in name
            if query in name.lower():
                matching_personalities.append(name)
                continue
            
            # Search in description
            description = traits.get("description", "").lower()
            if query in description:
                matching_personalities.append(name)
                continue
            
            # Search in tags
            tags = metadata.get("tags", [])
            for tag in tags:
                if query in tag.lower():
                    matching_personalities.append(name)
                    break
        
        return matching_personalities
    
    def get_selected_model(self) -> str:
        """Get the currently selected personality name"""
        return self.current_personality or ""
    
    def get_ai_name(self) -> str:
        """Get the AI's name from the current personality"""
        current_personality = self.get_current_personality()
        if current_personality and "traits" in current_personality:
            return current_personality["traits"].get("name", "AI Assistant")
        return "AI Assistant" 

    def get_temperature(self) -> float:
        """Get the temperature for the current personality, or default to 0.7"""
        current_personality = self.get_current_personality()
        if current_personality and 'temperature' in current_personality:
            return float(current_personality['temperature'])
        return 0.7 
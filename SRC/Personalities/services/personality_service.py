"""
Personality Service - Main personality management service

This module provides the main interface for personality management,
coordinating between the loader, formatter, and other components.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from ..models import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
from ..services.personality_loader import PersonalityLoader
from ..utils.personality_formatter import PersonalityFormatter


class PersonalityService:
    """Main service for managing AI personalities"""
    
    def __init__(self, personalities_dir: str = "personalities"):
        self.personalities_dir = personalities_dir
        self.personalities: Dict[str, Dict[str, Any]] = {}
        self.current_personality: Optional[str] = None
        
        # Initialize components
        self.loader = PersonalityLoader(personalities_dir)
        self.formatter = PersonalityFormatter()
        
        # Load personalities
        self._initialize_personalities()
    
    def _initialize_personalities(self):
        """Initialize personalities by loading from files"""
        self.personalities = self.loader.load_all_personalities()
        
        # Set default current personality if available
        if self.personalities:
            # Prefer assistant personality, otherwise use first available
            if "assistant" in self.personalities:
                self.current_personality = "assistant"
            else:
                self.current_personality = list(self.personalities.keys())[0]
    
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
        """Create a new custom personality"""
        try:
            # Create personality data
            personality_data = self.loader.create_personality_data(traits, prompt, config, metadata)
            
            # Save to file
            if self.loader.save_personality_to_file(name, personality_data):
                # Add to memory
                self.personalities[name] = personality_data
                return True
            return False
        except Exception as e:
            print(f"Error creating personality {name}: {e}")
            return False
    
    def delete_custom_personality(self, name: str) -> bool:
        """Delete a custom personality"""
        if name in self.personalities:
            try:
                # Delete file
                if self.loader.delete_personality_file(name):
                    # Remove from memory
                    del self.personalities[name]
                    
                    # Update current personality if it was deleted
                    if self.current_personality == name:
                        if self.personalities:
                            self.current_personality = list(self.personalities.keys())[0]
                        else:
                            self.current_personality = None
                    
                    return True
                return False
            except Exception as e:
                print(f"Error deleting personality {name}: {e}")
                return False
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
            print(f"Error refreshing personalities: {e}")
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
    
    def build_comprehensive_system_prompt(self) -> str:
        """Build a comprehensive system prompt with pronoun guidance"""
        current_personality = self.get_current_personality()
        if not current_personality:
            return ""
        
        return self.formatter.build_comprehensive_system_prompt(current_personality)
    
    def get_custom_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Get custom personalities (personalities not in default categories)"""
        custom_personalities = {}
        
        for name, personality_data in self.personalities.items():
            # Check if this is a custom personality (not in default categories)
            metadata = personality_data.get("metadata", {})
            category = metadata.get("category", "general")
            
            # Consider it custom if it's not in a standard category
            if category not in ["assistant", "creative", "technical", "friendly", "professional"]:
                custom_personalities[name] = personality_data
        
        return custom_personalities
    
    def get_personalities_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Get personalities by category"""
        categorized_personalities = {}
        
        for name, personality_data in self.personalities.items():
            metadata = personality_data.get("metadata", {})
            personality_category = metadata.get("category", "general")
            
            if personality_category == category:
                categorized_personalities[name] = personality_data
        
        return categorized_personalities
    
    def get_personality_categories(self) -> List[str]:
        """Get list of all personality categories"""
        categories = set()
        
        for personality_data in self.personalities.values():
            metadata = personality_data.get("metadata", {})
            category = metadata.get("category", "general")
            categories.add(category)
        
        return sorted(list(categories))
    
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
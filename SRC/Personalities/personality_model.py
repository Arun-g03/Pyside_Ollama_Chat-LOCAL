"""
Refactored Personality Model - Main interface for personality management

This module provides the main interface for personality management using
the refactored modular components. It maintains backward compatibility
with the original PersonalityModel interface.
"""

from typing import Dict, List, Optional, Any

from .models import (
    PersonalityType, PersonalityTraits, PersonalityConfig, 
    PersonalityMetadata, PersonalityPrompt, PersonalityPronouns
)
from .services.personality_service import PersonalityService


class PersonalityModel:
    """
    Main class for managing AI personalities
    
    This is the refactored version that uses modular components while
    maintaining the same interface as the original PersonalityModel.
    """
    
    def __init__(self, personalities_dir: str = "SRC/Personalities/personality_Profiles"):
        self.personalities_dir = personalities_dir
        self.service = PersonalityService(personalities_dir)
        
        # Backward compatibility: expose personalities and current_personality
        self.personalities = self.service.personalities
        self.current_personality = self.service.current_personality
        self.custom_personalities = {}  # Legacy support
    
    def _initialize_default_personalities(self):
        """Initialize the default personality set - now handled by service"""
        # This method is kept for backward compatibility but delegates to service
        self.service._initialize_personalities()
        self.personalities = self.service.personalities
        self.current_personality = self.service.current_personality
    
    def _find_personality_files(self, directory: str) -> List[str]:
        """Find personality files - now handled by loader"""
        return self.service.loader.find_personality_files(directory)
    
    def _extract_personality_name(self, filepath: str) -> str:
        """Extract personality name - now handled by loader"""
        return self.service.loader.extract_personality_name(filepath)
    
    def _load_custom_personalities(self):
        """Load custom personalities - now handled by service"""
        # This method is kept for backward compatibility but is no longer needed
        pass
    
    def get_available_personalities(self) -> List[str]:
        """Get list of all available personality names"""
        return self.service.get_available_personalities()
    
    def get_personality(self, name: str) -> Optional[Dict[str, Any]]:
        """Get personality by name"""
        return self.service.get_personality(name)
    
    def set_current_personality(self, name: str) -> bool:
        """Set the current active personality"""
        result = self.service.set_current_personality(name)
        if result:
            self.current_personality = self.service.current_personality
        return result
    
    def get_current_personality(self) -> Optional[Dict[str, Any]]:
        """Get the current active personality"""
        return self.service.get_current_personality()
    
    def create_custom_personality(self, name: str, traits: PersonalityTraits, prompt: PersonalityPrompt, 
                                 config: PersonalityConfig = None, metadata: PersonalityMetadata = None) -> bool:
        """Create a new custom personality"""
        result = self.service.create_custom_personality(name, traits, prompt, config, metadata)
        if result:
            # Update local references
            self.personalities = self.service.personalities
        return result
    
    def delete_custom_personality(self, name: str) -> bool:
        """Delete a custom personality"""
        result = self.service.delete_custom_personality(name)
        if result:
            # Update local references
            self.personalities = self.service.personalities
            self.current_personality = self.service.current_personality
        return result
    
    def _find_personality_file_by_name(self, personality_name: str) -> Optional[str]:
        """Find personality file by name - now handled by loader"""
        return self.service.loader.find_personality_file_by_name(personality_name)
    
    def refresh_personalities(self) -> bool:
        """Refresh personalities from disk"""
        result = self.service.refresh_personalities()
        if result:
            # Update local references
            self.personalities = self.service.personalities
            self.current_personality = self.service.current_personality
        return result
    
    def format_prompt_with_personality(self, user_input: str, context: str = "") -> str:
        """Format a prompt using the current personality's prompt templates"""
        return self.service.format_prompt_with_personality(user_input, context)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current personality"""
        return self.service.get_system_prompt()
    
    def get_personality_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a personality"""
        return self.service.get_personality_info(name)
    
    def get_personality_config(self, name: str = None) -> Optional[PersonalityConfig]:
        """Get configuration for a personality"""
        return self.service.get_personality_config(name)
    
    def update_personality_metadata(self, name: str, **kwargs) -> bool:
        """Update metadata for a personality"""
        return self.service.update_personality_metadata(name, **kwargs)
    
    def build_comprehensive_system_prompt(self, memory_service=None) -> str:
        """Build a comprehensive system prompt with pronoun guidance and user information from memory"""
        return self.service.build_comprehensive_system_prompt(memory_service)
    
    def get_user_context_messages(self, memory_service=None, is_new_conversation=False) -> List[Dict]:
        """Get dynamic user context messages that should be added to conversation"""
        return self.service.get_user_context_messages(memory_service, is_new_conversation)
    
    def get_custom_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Get custom personalities - for backward compatibility"""
        # Use the improved service implementation
        return self.service.get_custom_personalities()
    
    def get_system_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Get system personalities (read-only)"""
        return self.service.get_system_personalities()
    
    def is_system_personality(self, name: str) -> bool:
        """Check if a personality is a system personality (read-only)"""
        return self.service.is_system_personality(name)
    
    def is_custom_personality(self, name: str) -> bool:
        """Check if a personality is a custom personality (editable/deletable)"""
        return self.service.is_custom_personality(name)
    
    def update_custom_personality(self, name: str, traits: PersonalityTraits, prompt: PersonalityPrompt, 
                                 config: PersonalityConfig = None, metadata: PersonalityMetadata = None) -> bool:
        """Update a custom personality (only if it's in the Custom folder)"""
        result = self.service.update_custom_personality(name, traits, prompt, config, metadata)
        if result:
            # Update local references
            self.personalities = self.service.personalities
        return result
    
    def save_custom_personality(self, name: str, personality_data: Dict[str, Any]) -> bool:
        """Save a custom personality - for backward compatibility"""
        # This method delegates to the loader's save method
        return self.service.loader.save_personality_to_file(name, personality_data)
    
    def get_personalities_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """Get personalities by category"""
        return self.service.get_personalities_by_category(category)
    
    def get_personality_categories(self) -> List[str]:
        """Get list of all personality categories"""
        return self.service.get_personality_categories()
    
    def search_personalities(self, query: str) -> List[str]:
        """Search personalities by name, description, or tags"""
        return self.service.search_personalities(query)
    
    # Additional convenience methods
    def get_selected_model(self) -> str:
        """Get the currently selected personality name"""
        return self.service.get_selected_model()
    
    def get_ai_name(self) -> str:
        """Get the AI's name from the current personality"""
        return self.service.get_ai_name()
    
    def get_personality_loader(self):
        """Get access to the personality loader for advanced operations"""
        return self.service.loader
    
    def get_personality_formatter(self):
        """Get access to the personality formatter for advanced operations"""
        return self.service.formatter 
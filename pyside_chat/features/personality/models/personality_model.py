"""
Refactored Personality Model - Main interface for personality management

This module provides the main interface for personality management using
the refactored modular components. It maintains backward compatibility
with the original PersonalityModel interface.
"""

from typing import Dict, List, Optional, Any


from pyside_chat.features.personality.services.personality_service import PersonalityService


class PersonalityModel(PersonalityService):
    """
    Main class for managing AI personalities
    
    This is the refactored version that inherits from PersonalityService while
    maintaining the same interface as the original PersonalityModel.
    """
    
    def __init__(self, personalities_dir: str = "pyside_chat/features/personality/profiles"):
        try:
            super().__init__(personalities_dir)
            
            # Backward compatibility: expose personalities and current_personality
            self.personalities = self.personalities
            self.current_personality = self.current_personality
            self.custom_personalities = {}  # Legacy support
        except Exception as e:
            # Initialize with empty values if initialization fails
            self.personalities = {}
            self.current_personality = None
            self.custom_personalities = {}
            raise RuntimeError(f"Failed to initialize personality model: {str(e)}") from e
    @property
    def service(self):
        """Backward compatibility: return self as the service"""
        return self
    
    def _initialize_default_personalities(self):
        """Initialize the default personality set - now handled by service"""
        # This method is kept for backward compatibility but delegates to service
        self._initialize_personalities()
        self.personalities = self.personalities
        self.current_personality = self.current_personality
    
    def _find_personality_files(self, directory: str) -> List[str]:
        """Find personality files - now handled by loader"""
        return self.loader.find_personality_files(directory)
    
    def _extract_personality_name(self, filepath: str) -> str:
        """Extract personality name - now handled by loader"""
        return self.loader.extract_personality_name(filepath)
    
    def _load_custom_personalities(self):
        """Load custom personalities - now handled by service"""
        # This method is kept for backward compatibility but is no longer needed
        pass
    
    def _find_personality_file_by_name(self, personality_name: str) -> Optional[str]:
        """Find personality file by name - now handled by loader"""
        return self.loader.find_personality_file_by_name(personality_name)
    
    def save_custom_personality(self, name: str, personality_data: Dict[str, Any]) -> bool:
        """Save a custom personality - for backward compatibility"""
        # This method delegates to the loader's save method
        return self.loader.save_personality_to_file(name, personality_data)
    
    # Additional convenience methods
    def get_personality_loader(self):
        """Get access to the personality loader for advanced operations"""
        return self.loader
    
    def get_personality_formatter(self):
        """Get access to the personality formatter for advanced operations"""
        return self.formatter 
    
    def get_system_personalities(self):
        """Return a list of system personality names (for UI compatibility)"""
        return list(super().get_system_personalities().keys())

    def get_custom_personalities(self):
        """Return a list of custom personality names (for UI compatibility)"""
        return list(super().get_custom_personalities().keys())
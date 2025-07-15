"""
System Message Configuration - Manages user preferences for system message display
"""

import json
import os
from typing import Dict, Any
from pyside_chat.ui.themes.system_message_manager import SystemMessageManager, SystemMessageType

class SystemMessageConfig:
    """Configuration manager for system message display preferences"""
    
    def __init__(self, config_file: str = "system_message_config.json"):
        self.config_file = config_file
        self.preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict[str, str]:
        """Load system message preferences from file"""
        default_preferences = {
            "model_selection": "compact",
            "personality_switch": "full_width", 
            "memory_update": "hidden",
            "error": "full_width",
            "info": "compact",
            "warning": "centered",
            "debug": "hidden"
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_prefs = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_preferences.items():
                        if key not in loaded_prefs:
                            loaded_prefs[key] = value
                    return loaded_prefs
            else:
                return default_preferences
        except Exception as e:
            print(f"Error loading system message config: {e}")
            return default_preferences
    
    def _save_preferences(self):
        """Save system message preferences to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving system message config: {e}")
    
    def get_style(self, message_type: str) -> str:
        """Get the display style for a message type"""
        return self.preferences.get(message_type, "compact")
    
    def set_style(self, message_type: str, style: str):
        """Set the display style for a message type"""
        if style in ["compact", "full_width", "centered", "hidden", "default"]:
            self.preferences[message_type] = style
            # Update the SystemMessageManager
            try:
                enum_type = SystemMessageType(message_type)
                SystemMessageManager.update_default_style(enum_type, style)
            except ValueError:
                pass  # Unknown message type, just store in preferences
            self._save_preferences()
    
    def get_all_preferences(self) -> Dict[str, str]:
        """Get all current preferences"""
        return self.preferences.copy()
    
    def reset_to_defaults(self):
        """Reset all preferences to default values"""
        self.preferences = {
            "model_selection": "compact",
            "personality_switch": "full_width", 
            "memory_update": "hidden",
            "error": "full_width",
            "info": "compact",
            "warning": "centered",
            "debug": "hidden"
        }
        self._save_preferences()
        
        # Update SystemMessageManager defaults
        for msg_type in SystemMessageType:
            SystemMessageManager.update_default_style(msg_type, self.preferences[msg_type.value])
    
    def get_available_styles(self) -> list:
        """Get list of available styling options"""
        return ["compact", "full_width", "centered", "hidden", "default"]
    
    def get_message_type_descriptions(self) -> Dict[str, str]:
        """Get descriptions for each message type"""
        return {
            "model_selection": "Model selection and auto-selection messages",
            "personality_switch": "Personality change notifications", 
            "memory_update": "Memory and fact storage updates",
            "error": "Error messages and exceptions",
            "info": "General information messages",
            "warning": "Warning and caution messages",
            "debug": "Debug and development messages"
        } 
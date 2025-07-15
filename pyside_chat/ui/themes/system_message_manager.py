"""
System Message Manager - Handles different types of system messages with appropriate styling
"""

from enum import Enum
from typing import Dict, Any, Optional
from pyside_chat.ui.themes.chat_styles import ChatStyles

class SystemMessageType(Enum):
    """Types of system messages with different display styles"""
    MODEL_SELECTION = "model_selection"
    PERSONALITY_SWITCH = "personality_switch"
    MEMORY_UPDATE = "memory_update"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    DEBUG = "debug"

class SystemMessageManager:
    """Manages system messages with appropriate styling based on type"""
    
    # Default styling preferences
    DEFAULT_STYLES = {
        SystemMessageType.MODEL_SELECTION: "compact",
        SystemMessageType.PERSONALITY_SWITCH: "full_width",
        SystemMessageType.MEMORY_UPDATE: "hidden",  # Don't show memory updates by default
        SystemMessageType.ERROR: "full_width",
        SystemMessageType.INFO: "compact",
        SystemMessageType.WARNING: "centered",
        SystemMessageType.DEBUG: "hidden",  # Don't show debug messages by default
    }
    
    # Message type detection patterns
    MESSAGE_PATTERNS = {
        SystemMessageType.MODEL_SELECTION: [
            "Using model",
            "Auto-selected",
            "Model selected",
            "Switched to model"
        ],
        SystemMessageType.PERSONALITY_SWITCH: [
            "Switched to personality",
            "Personality changed",
            "Using personality"
        ],
        SystemMessageType.MEMORY_UPDATE: [
            "Memory updated",
            "Fact stored",
            "Memory operation"
        ],
        SystemMessageType.ERROR: [
            "Error:",
            "Failed:",
            "Exception:",
            "Error occurred"
        ],
        SystemMessageType.WARNING: [
            "Warning:",
            "Caution:",
            "Note:"
        ],
        SystemMessageType.DEBUG: [
            "DEBUG:",
            "Debug:",
            "[DEBUG]"
        ]
    }
    
    @staticmethod
    def detect_message_type(content: str) -> SystemMessageType:
        """Detect the type of system message based on content"""
        content_lower = content.lower()
        
        for msg_type, patterns in SystemMessageManager.MESSAGE_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    return msg_type
        
        # Default to INFO if no specific pattern matches
        return SystemMessageType.INFO
    
    @staticmethod
    def get_styling_method(message_type: SystemMessageType) -> str:
        """Get the styling method for a message type"""
        return SystemMessageManager.DEFAULT_STYLES.get(message_type, "compact")
    
    @staticmethod
    def format_system_message(content: str, message_index: int = 0, 
                            message_type: Optional[SystemMessageType] = None,
                            force_style: Optional[str] = None) -> str:
        """Format a system message with appropriate styling"""
        
        # Detect message type if not provided
        if message_type is None:
            message_type = SystemMessageManager.detect_message_type(content)
        
        # Determine styling method
        if force_style:
            styling_method = force_style
        else:
            styling_method = SystemMessageManager.get_styling_method(message_type)
        
        # Apply appropriate styling
        if styling_method == "compact":
            return ChatStyles.get_system_bubble_compact_html(content, message_index)
        elif styling_method == "full_width":
            return ChatStyles.get_system_bubble_full_width_html(content, message_index)
        elif styling_method == "centered":
            return ChatStyles.get_system_bubble_centered_html(content, message_index)
        elif styling_method == "hidden":
            return ChatStyles.get_system_bubble_hidden_html(content, message_index)
        else:
            # Default to standard system bubble
            return ChatStyles.get_system_bubble_html(content, message_index)
    
    @staticmethod
    def should_display_message(message_type: SystemMessageType) -> bool:
        """Check if a message type should be displayed"""
        styling_method = SystemMessageManager.get_styling_method(message_type)
        return styling_method != "hidden"
    
    @staticmethod
    def update_default_style(message_type: SystemMessageType, new_style: str):
        """Update the default styling for a message type"""
        if new_style in ["compact", "full_width", "centered", "hidden", "default"]:
            SystemMessageManager.DEFAULT_STYLES[message_type] = new_style
    
    @staticmethod
    def get_all_message_types() -> Dict[str, str]:
        """Get all message types and their current styling"""
        return {
            msg_type.value: SystemMessageManager.get_styling_method(msg_type)
            for msg_type in SystemMessageType
        }
    
    @staticmethod
    def get_style_for_message(content: str) -> str:
        """Get the appropriate style for a system message (for backward compatibility)"""
        message_type = SystemMessageManager.detect_message_type(content)
        return SystemMessageManager.get_styling_method(message_type) 
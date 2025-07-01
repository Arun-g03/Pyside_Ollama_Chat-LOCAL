"""
Prompt Templates Module

This module centralizes all prompt templates used throughout the application.
Prompts can be easily modified, localized, or extended without touching business logic.
"""

from typing import Dict, Any


class PromptTemplates:
    """Centralized prompt templates for the application"""
    
    # Fact extraction prompts
    FACT_EXTRACTION = {
        "system": (
            "Extract any facts, preferences, or important information from the following message "
            "that should be remembered for future conversations. Return ONLY a valid JSON object with key-value pairs. "
            "If no facts are found, return an empty JSON object {}."
        ),
        "user_template": "Message: \"{message}\""
    }
    
    # Auto model selection prompts
    AUTO_MODEL_SELECTION = {
        "system_info": "Using model {model} (auto-selected based on request complexity)"
    }
    
    # Conversation prompts
    CONVERSATION = {
        "new_conversation_detected": "Detected new conversation",
        "explicit_new_conversation": "Using explicit new conversation flag",
        "new_conversation_reset": "Reset new conversation flag"
    }
    
    # Memory prompts
    MEMORY = {
        "ltm_qualified": "Message already qualified for LTM storage, skipping LLM fact extraction",
        "ltm_not_qualified": "Message didn't qualify for LTM, attempting LLM fact extraction",
        "fact_storage_start": "=== FACT STORAGE START ===",
        "fact_storage_end": "=== FACT STORAGE END ===",
        "fact_extraction_start": "=== FACT EXTRACTION START ===",
        "fact_extraction_end": "=== FACT EXTRACTION END ==="
    }
    
    # Error messages
    ERRORS = {
        "conversation_load_failed": "Failed to load conversation: {error}",
        "conversation_delete_failed": "Failed to handle conversation deletion: {error}",
        "conversation_rename_failed": "Failed to handle conversation rename: {error}",
        "close_error": "Error during close: {error}"
    }
    
    # Status messages
    STATUS = {
        "ready": "Ready",
        "models_found": "Found {count} models",
        "conversation_loaded": "Loaded conversation: {info}",
        "conversation_deleted": "Conversation deleted",
        "conversation_renamed": "Renamed conversation: {old} → {new}",
        "personality_switched": "Switched to {personality} personality",
        "new_conversation_started": "Started new conversation",
        "chat_cleared": "Chat display cleared",
        "model_operation_error": "Error: {error}"
    }
    
    # Menu actions
    MENU = {
        "clear_chat_question": "Clear the chat display? This will not affect the conversation history.",
        "about_text": """Ollama Chat

A modern PySide6-based chat interface for Ollama.

Features:
• Multiple AI personalities
• Model management
• Conversation history
• Spell checking
• Dark theme

Version: 1.0.0"""
    }


class PromptFormatter:
    """Utility class for formatting prompts with dynamic content"""
    
    @staticmethod
    def format_fact_extraction_prompt(message: str) -> str:
        """Format the fact extraction prompt with the given message"""
        system_prompt = PromptTemplates.FACT_EXTRACTION["system"]
        user_prompt = PromptTemplates.FACT_EXTRACTION["user_template"].format(message=message)
        return f"{system_prompt}\n\n{user_prompt}"
    
    @staticmethod
    def format_auto_model_selection_info(model: str) -> str:
        """Format auto model selection info message"""
        return PromptTemplates.AUTO_MODEL_SELECTION["system_info"].format(model=model)
    
    @staticmethod
    def format_conversation_status(status_key: str, **kwargs) -> str:
        """Format conversation status message"""
        template = PromptTemplates.CONVERSATION.get(status_key, status_key)
        return template.format(**kwargs) if kwargs else template
    
    @staticmethod
    def format_memory_status(status_key: str) -> str:
        """Format memory status message"""
        return PromptTemplates.MEMORY.get(status_key, status_key)
    
    @staticmethod
    def format_error_message(error_key: str, **kwargs) -> str:
        """Format error message"""
        template = PromptTemplates.ERRORS.get(error_key, error_key)
        return template.format(**kwargs)
    
    @staticmethod
    def format_status_message(status_key: str, **kwargs) -> str:
        """Format status message"""
        template = PromptTemplates.STATUS.get(status_key, status_key)
        return template.format(**kwargs)
    
    @staticmethod
    def get_menu_text(menu_key: str) -> str:
        """Get menu text"""
        return PromptTemplates.MENU.get(menu_key, menu_key) 
"""
Logging Helpers Module

This module provides centralized logging utilities to standardize log formats
and reduce code duplication throughout the application.
"""

from typing import Dict, Any, Optional
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class LoggingHelpers:
    """Centralized logging utilities for consistent log formatting"""
    
    @staticmethod
    def log_message_sent(message: str) -> None:
        """Log message sent event"""
        logger.debug("=== MESSAGE SENT START ===", print_to_terminal=True)
        logger.debug(f"Processing message: '{message}'", print_to_terminal=True)
    
    @staticmethod
    def log_message_sent_end() -> None:
        """Log message sent end event"""
        logger.debug("=== MESSAGE SENT END ===", print_to_terminal=True)
    
    @staticmethod
    def log_fact_storage_start(message: str) -> None:
        """Log fact storage start"""
        logger.debug("=== FACT STORAGE START ===", print_to_terminal=True)
        logger.debug(f"Processing message for fact storage: '{message}'", print_to_terminal=True)
    
    @staticmethod
    def log_fact_storage_end() -> None:
        """Log fact storage end"""
        logger.debug("=== FACT STORAGE END ===", print_to_terminal=True)
    
    @staticmethod
    def log_fact_extraction_start(message: str) -> None:
        """Log fact extraction start"""
        logger.debug("=== FACT EXTRACTION START ===", print_to_terminal=True)
        logger.debug(f"Input message: '{message}'", print_to_terminal=True)
        logger.debug(f"Message length: {len(message.strip())} characters", print_to_terminal=True)
    
    @staticmethod
    def log_fact_extraction_end() -> None:
        """Log fact extraction end"""
        logger.debug("=== FACT EXTRACTION END ===", print_to_terminal=True)
    
    @staticmethod
    def log_memory_result(result: Dict[str, Any]) -> None:
        """Log memory operation result"""
        logger.debug(f"Memory addition result: {result}", print_to_terminal=True)
    
    @staticmethod
    def log_memory_ltm_status(qualified: bool) -> None:
        """Log LTM qualification status"""
        if qualified:
            logger.debug("Message already qualified for LTM storage, skipping LLM fact extraction", print_to_terminal=True)
        else:
            logger.debug("Message didn't qualify for LTM, attempting LLM fact extraction", print_to_terminal=True)
    
    @staticmethod
    def log_fact_processing(key: str, value: str, stored_count: int) -> None:
        """Log individual fact processing"""
        logger.debug(f"Processing fact: key='{key}', value='{value}'", print_to_terminal=True)
        logger.debug(f"Storing fact: {key} = {value}", print_to_terminal=True)
        logger.debug(f"Successfully stored fact #{stored_count}", print_to_terminal=True)
    
    @staticmethod
    def log_fact_skipped(reason: str, key: Optional[str] = None, value: Optional[str] = None) -> None:
        """Log skipped fact with reason"""
        if key and value:
            logger.debug(f"Skipping fact - {reason}: key='{key}' (type: {type(key)}), value='{value}' (type: {type(value)})", print_to_terminal=True)
        else:
            logger.debug(f"Skipping fact - {reason}", print_to_terminal=True)
    
    @staticmethod
    def log_fact_storage_summary(stored_count: int, skipped_count: int) -> None:
        """Log fact storage summary"""
        logger.debug(f"Fact storage complete: {stored_count} stored, {skipped_count} skipped", print_to_terminal=True)
    
    @staticmethod
    def log_fact_extraction_result(facts: Dict[str, Any]) -> None:
        """Log fact extraction result"""
        if facts and isinstance(facts, dict):
            logger.debug(f"Extracted facts: {facts}", print_to_terminal=True)
            logger.debug(f"Processing {len(facts)} facts for storage", print_to_terminal=True)
        else:
            logger.debug("No valid facts extracted from message", print_to_terminal=True)
            logger.debug(f"Facts type: {type(facts)}, Facts value: {facts}", print_to_terminal=True)
    
    @staticmethod
    def log_llm_call(model: str, prompt: str) -> None:
        """Log LLM call details"""
        logger.debug(f"Calling LLM with model: {model}", print_to_terminal=True)
        logger.debug(f"Prompt sent to LLM: '{prompt}'", print_to_terminal=True)
    
    @staticmethod
    def log_llm_response(response: str) -> None:
        """Log LLM response details"""
        logger.debug(f"Raw LLM response: '{response}'", print_to_terminal=True)
        logger.debug(f"Response length: {len(response)} characters", print_to_terminal=True)
    
    @staticmethod
    def log_json_extraction(json_str: str, method: str) -> None:
        """Log JSON extraction attempt"""
        logger.debug(f"JSON extracted using {method}: '{json_str}'", print_to_terminal=True)
    
    @staticmethod
    def log_json_parsing_success(facts: Dict[str, Any]) -> None:
        """Log successful JSON parsing"""
        logger.debug("JSON parsed successfully, type: {type(facts)}", print_to_terminal=True)
        logger.debug(f"Fact extraction successful: {facts}", print_to_terminal=True)
        logger.debug(f"Number of facts extracted: {len(facts)}", print_to_terminal=True)
        if facts:
            for key, value in facts.items():
                logger.debug(f"  Fact: '{key}' = '{value}'", print_to_terminal=True)
    
    @staticmethod
    def log_json_parsing_error(error: Exception, json_str: str) -> None:
        """Log JSON parsing error"""
        logger.debug(f"Fact extraction JSON decode error: {error}", print_to_terminal=True)
        logger.debug(f"Error position: {error.pos}", print_to_terminal=True)
        logger.debug(f"Error line: {error.lineno}, column: {error.colno}", print_to_terminal=True)
        logger.debug(f"Attempted to parse: '{json_str}'", print_to_terminal=True)
    
    @staticmethod
    def log_conversation_detection(is_new: bool, method: str) -> None:
        """Log conversation detection"""
        if is_new:
            logger.debug(f"Detected new conversation ({method})", print_to_terminal=True)
    
    @staticmethod
    def log_context_messages(context_messages: list) -> None:
        """Log context messages being sent to AI"""
        logger.debug(f"Final context being sent to AI ({len(context_messages)} messages):", print_to_terminal=True)
        for i, msg in enumerate(context_messages):
            role = msg.get("role", "unknown")
            content_preview = msg.get("content", "")[:100] + "..." if len(msg.get("content", "")) > 100 else msg.get("content", "")
            logger.debug(f"  {i+1}. {role}: {content_preview}", print_to_terminal=True)
    
    @staticmethod
    def log_error(operation: str, error: Exception) -> None:
        """Log error with operation context"""
        logger.debug(f"Error in {operation}: {error}", print_to_terminal=True)
        logger.debug(f"Exception type: {type(error)}", print_to_terminal=True)
    
    @staticmethod
    def log_debug(message: str) -> None:
        """Log debug message"""
        logger.debug(message, print_to_terminal=True) 
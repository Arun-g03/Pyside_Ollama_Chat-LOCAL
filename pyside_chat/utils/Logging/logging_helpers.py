"""
Logging Helpers Module

This module provides centralized logging utilities to standardize log formats
and reduce code duplication throughout the application.
"""

from typing import Dict, Any, Optional
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class LoggingHelpers:
    """Centralized logging utilities for consistent log formatting"""
    
    @staticmethod
    def log_message_sent(message: str) -> None:
        """Log message sent event"""
        logger.debug("[ID:0278] === MESSAGE SENT START ===", print_to_terminal=True)
        logger.debug(f"[ID:0277] Processing message: '{message}'", print_to_terminal=True)
    
    @staticmethod
    def log_message_sent_end() -> None:
        """Log message sent end event"""
        logger.debug("[ID:0276] === MESSAGE SENT END ===", print_to_terminal=True)
    
    @staticmethod
    def log_fact_storage_start(message: str) -> None:
        """Log fact storage start"""
        logger.debug("[ID:0275] === FACT STORAGE START ===", print_to_terminal=True)
        logger.debug(f"[ID:0274] Processing message for fact storage: '{message}'", print_to_terminal=True)
    
    @staticmethod
    def log_fact_storage_end() -> None:
        """Log fact storage end"""
        logger.debug("[ID:0273] === FACT STORAGE END ===", print_to_terminal=True)
    
    @staticmethod
    def log_fact_extraction_start(message: str) -> None:
        """Log fact extraction start"""
        logger.debug("[ID:0272] === FACT EXTRACTION START ===", print_to_terminal=True)
        logger.debug(f"[ID:0271] Input message: '{message}'", print_to_terminal=True)
        logger.debug(f"[ID:0270] Message length: {len(message.strip())} characters", print_to_terminal=True)
    
    @staticmethod
    def log_fact_extraction_end() -> None:
        """Log fact extraction end"""
        logger.debug("[ID:0269] === FACT EXTRACTION END ===", print_to_terminal=True)
    
    @staticmethod
    def log_memory_result(result: Dict[str, Any]) -> None:
        """Log memory operation result"""
        logger.debug(f"[ID:0268] Memory addition result: {result}", print_to_terminal=True)
    
    @staticmethod
    def log_memory_ltm_status(qualified: bool) -> None:
        """Log LTM qualification status"""
        if qualified:
            logger.debug("[ID:0267] Message already qualified for LTM storage, skipping LLM fact extraction", print_to_terminal=True)
        else:
            logger.debug("[ID:0266] Message didn't qualify for LTM, attempting LLM fact extraction", print_to_terminal=True)
    
    @staticmethod
    def log_fact_processing(key: str, value: str, stored_count: int) -> None:
        """Log individual fact processing"""
        logger.debug(f"[ID:0265] Processing fact: key='{key}', value='{value}'", print_to_terminal=True)
        logger.debug(f"[ID:0264] Storing fact: {key} = {value}", print_to_terminal=True)
        logger.debug(f"[ID:0263] Successfully stored fact #{stored_count}", print_to_terminal=True)
    
    @staticmethod
    def log_fact_skipped(reason: str, key: Optional[str] = None, value: Optional[str] = None) -> None:
        """Log skipped fact with reason"""
        if key and value:
            logger.debug(f"[ID:0262] Skipping fact - {reason}: key='{key}' (type: {type(key)}), value='{value}' (type: {type(value)})", print_to_terminal=True)
        else:
            logger.debug(f"[ID:0261] Skipping fact - {reason}", print_to_terminal=True)
    
    @staticmethod
    def log_fact_storage_summary(stored_count: int, skipped_count: int) -> None:
        """Log fact storage summary"""
        logger.debug(f"[ID:0260] Fact storage complete: {stored_count} stored, {skipped_count} skipped", print_to_terminal=True)
    
    @staticmethod
    def log_fact_extraction_result(facts: Dict[str, Any]) -> None:
        """Log fact extraction result"""
        if facts and isinstance(facts, dict):
            logger.debug(f"[ID:0259] Extracted facts: {facts}", print_to_terminal=True)
            logger.debug(f"[ID:0258] Processing {len(facts)} facts for storage", print_to_terminal=True)
        else:
            logger.debug("[ID:0257] No valid facts extracted from message", print_to_terminal=True)
            logger.debug(f"[ID:0256] Facts type: {type(facts)}, Facts value: {facts}", print_to_terminal=True)
    
    @staticmethod
    def log_llm_call(model: str, prompt: str) -> None:
        """Log LLM call details"""
        logger.debug(f"[ID:0255] Calling LLM with model: {model}", print_to_terminal=True)
        logger.debug(f"[ID:0254] Prompt sent to LLM: '{prompt}'", print_to_terminal=True)
    
    @staticmethod
    def log_llm_response(response: str) -> None:
        """Log LLM response details"""
        logger.debug(f"[ID:0253] Raw LLM response: '{response}'", print_to_terminal=True)
        logger.debug(f"[ID:0252] Response length: {len(response)} characters", print_to_terminal=True)
    
    @staticmethod
    def log_json_extraction(json_str: str, method: str) -> None:
        """Log JSON extraction attempt"""
        logger.debug(f"[ID:0251] JSON extracted using {method}: '{json_str}'", print_to_terminal=True)
    
    @staticmethod
    def log_json_parsing_success(facts: Dict[str, Any]) -> None:
        """Log successful JSON parsing"""
        logger.debug("[ID:0250] JSON parsed successfully, type: {type(facts)}", print_to_terminal=True)
        logger.debug(f"[ID:0249] Fact extraction successful: {facts}", print_to_terminal=True)
        logger.debug(f"[ID:0248] Number of facts extracted: {len(facts)}", print_to_terminal=True)
        if facts:
            for key, value in facts.items():
                logger.debug(f"[ID:0247]   Fact: '{key}' = '{value}'", print_to_terminal=True)
    
    @staticmethod
    def log_json_parsing_error(error: Exception, json_str: str) -> None:
        """Log JSON parsing error"""
        logger.debug(f"[ID:0246] Fact extraction JSON decode error: {error}", print_to_terminal=True)
        logger.debug(f"[ID:0245] Error position: {error.pos}", print_to_terminal=True)
        logger.debug(f"[ID:0244] Error line: {error.lineno}, column: {error.colno}", print_to_terminal=True)
        logger.debug(f"[ID:0243] Attempted to parse: '{json_str}'", print_to_terminal=True)
    
    @staticmethod
    def log_conversation_detection(is_new: bool, method: str) -> None:
        """Log conversation detection"""
        if is_new:
            logger.debug(f"[ID:0242] Detected new conversation ({method})", print_to_terminal=True)
    
    @staticmethod
    def log_context_messages(context_messages: list) -> None:
        """Log context messages being sent to AI"""
        logger.debug(f"[ID:0241] Final context being sent to AI ({len(context_messages)} messages):", print_to_terminal=True)
        for i, msg in enumerate(context_messages):
            role = msg.get("role", "unknown")
            content_preview = msg.get("content", "")[:100] + "..." if len(msg.get("content", "")) > 100 else msg.get("content", "")
            logger.debug(f"[ID:0240]   {i+1}. {role}: {content_preview}", print_to_terminal=True)
    
    @staticmethod
    def log_error(operation: str, error: Exception) -> None:
        """Log error with operation context"""
        logger.debug(f"[ID:0239] Error in {operation}: {error}", print_to_terminal=True)
        logger.debug(f"[ID:0238] Exception type: {type(error)}", print_to_terminal=True)
    
    @staticmethod
    def log_debug(message: str) -> None:
        """Log debug message"""
        logger.debug(message, print_to_terminal=True)

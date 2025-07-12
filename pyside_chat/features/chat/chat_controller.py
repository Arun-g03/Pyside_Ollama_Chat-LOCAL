"""
Chat Controller Module

This module implements the mediator pattern to separate business logic from UI components.
It handles communication between different services and UI components.
"""

import os
from typing import Dict, Any, Optional, List
from PySide6.QtCore import QObject, Signal
import re

from pyside_chat.features.ollama.ollama_service import OllamaService
from pyside_chat.features.chat.conversation_service import ConversationService
from pyside_chat.features.chat.enhancers.enhancement_service import EnhancementService
from pyside_chat.features.memory.memory_service import MemoryService
from pyside_chat.core.models.conversation_metadata import ConversationManager
from pyside_chat.core.utils.prompts import PromptFormatter
from pyside_chat.core.logging.helpers import LoggingHelpers
from pyside_chat.features.chat.complexity_analyser.complexity_analyzer import RequestComplexityAnalyzer
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

def remove_emojis(text):
    # This regex matches most emojis, including symbols and pictographs
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U00002600-\U000026FF"  # Misc symbols
        "\U00002B50-\U00002B55"  # Stars
        "\U00002300-\U000023FF"  # Misc technical
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

class ChatController(QObject):
    """Controller class that mediates between UI components and business logic"""
    
    # Signals for UI updates
    message_sent = Signal(str)
    message_received = Signal(str)
    conversation_updated = Signal()
    status_updated = Signal(str)
    error_occurred = Signal(str)
    name_generation_requested = Signal(str)  # Emitted when name generation is requested (filepath)
    
    def __init__(self, 
                 ollama_service: OllamaService,
                 conversation_service: ConversationService,
                 enhancement_service: EnhancementService,
                 memory_service: Optional[MemoryService],
                 conversation_manager: ConversationManager,
                 personality_service=None):
        super().__init__()
        
        self.ollama_service = ollama_service
        self.conversation_service = conversation_service
        self.enhancement_service = enhancement_service
        self.memory_service = memory_service
        self.conversation_manager = conversation_manager
        self.personality_service = personality_service
        
        # State tracking
        self.is_new_conversation = False
        self.current_model = None
        self.current_temperature = 0.7
        self._pending_assistant_response = ""  # Accumulate assistant response here
        
    def is_memory_active(self) -> bool:
        """Check if memory is enabled and available"""
        return self.memory_service is not None
    
    def process_user_message(self, message: str, model: str, temperature: float) -> None:
        """Process a user message through the complete pipeline"""
        try:
            LoggingHelpers.log_message_sent(len(message))
            
            # Update current settings
            self.current_model = model
            self.current_temperature = temperature
            
            # Check if this is the first message in a new conversation
            messages = self.conversation_service.get_messages()
            if len(messages) == 0 and not self.is_new_conversation:
                # This is the first message and we haven't explicitly started a new conversation
                self.start_new_conversation()
                LoggingHelpers.log_debug("Auto-started new conversation for first message")
            
            # Add message to conversation
            self.conversation_service.add_message("user", message)
            
            # Reset the new conversation flag after adding the first message
            if self.is_new_conversation:
                self.is_new_conversation = False
                LoggingHelpers.log_debug("Reset is_new_conversation flag after first message")
            
            # Handle memory operations
            if self.is_memory_active():
                self._handle_memory_operations(message)
            
            # Send to Ollama
            self._send_to_ollama(message, model, temperature)
            
            LoggingHelpers.log_message_sent_end(len(message), 0)  # Message length, response length (will be updated later)
            
        except Exception as e:
            LoggingHelpers.log_exception_with_context("process_user_message", e)
            self.error_occurred.emit(f"Error processing message: {str(e)}")
    
    def _handle_memory_operations(self, message: str) -> None:
        """Handle memory-related operations for a message"""
        # Use intelligent message addition
        result = self.memory_service.intelligent_add_message({"role": "user", "content": message})
        LoggingHelpers.log_memory_result(message[:50], 1)  # Log with message preview and count
        
        # Only do LLM fact extraction for messages that didn't qualify for LTM storage
        if not result.get("ltm_qualified", False):
            LoggingHelpers.log_memory_ltm_status(0, 1)  # No LTM, 1 STM
            self._extract_and_store_facts(message)
        else:
            LoggingHelpers.log_memory_ltm_status(1, 1)  # 1 LTM, 1 STM
    
    def _extract_and_store_facts(self, message: str) -> None:
        """Extract facts from the message using LLM and store in long-term memory"""
        LoggingHelpers.log_fact_storage_start("user_message", 1)
        
        try:
            # Skip fact extraction for very short messages to prevent lockup
            if len(message.strip()) < 10:
                LoggingHelpers.log_debug("Skipping fact extraction - message too short (< 10 chars)")
                return
            
            facts = self._extract_facts_with_llm(message)
            LoggingHelpers.log_fact_extraction_result([facts] if facts else [])
            
            if facts and isinstance(facts, dict):
                self._store_extracted_facts(facts)
            else:
                LoggingHelpers.log_debug("No valid facts extracted from message")
                
        except Exception as e:
            LoggingHelpers.log_exception_with_context("extract_and_store_facts", e, {"message": message})
        finally:
            LoggingHelpers.log_fact_storage_end("user_message", 0)  # 0 facts stored by default
    
    def _extract_facts_with_llm(self, message: str) -> Dict[str, str]:
        """Use qwen3:0.6b to extract facts as key-value pairs from a message"""
        import json
        import re
        
        LoggingHelpers.log_fact_extraction_start(message)
        
        # Skip fact extraction for very short messages
        if len(message.strip()) < 5:
            LoggingHelpers.log_debug("Skipping fact extraction - message too short (< 5 chars)")
            return {}
        
        prompt = PromptFormatter.format_fact_extraction_prompt(message)
        LoggingHelpers.log_llm_call("qwen3:0.6b", len(prompt))
        
        try:
            # Use OllamaService to call qwen3:0.6b with timeout
            import threading
            import time
            
            response = ""
            response_chunks = []
            extraction_complete = threading.Event()
            extraction_error = None
            
            def extract_facts():
                nonlocal response, response_chunks, extraction_error
                try:
                    chunks = self.ollama_service.send_chat_message(
                        model="qwen3:0.6b",
                        messages=[{"role": "system", "content": prompt}],
                        temperature=0.0,
                        stream=True
                    )
                    response_chunks = list(chunks)
                    response = "".join(response_chunks).strip()
                except Exception as e:
                    extraction_error = e
                finally:
                    extraction_complete.set()
            
            # Start fact extraction in a separate thread with timeout
            extraction_thread = threading.Thread(target=extract_facts, daemon=True)
            extraction_thread.start()
            
            # Wait for extraction to complete with timeout
            if not extraction_complete.wait(timeout=10.0):  # 10 second timeout
                logger.warning("Fact extraction timed out, skipping")
                return {}
            
            if extraction_error:
                logger.error(f"Fact extraction error: {extraction_error}")
                return {}
            
            LoggingHelpers.log_llm_response("qwen3:0.6b", len(response))
            
            # Handle empty response
            if not response:
                LoggingHelpers.log_debug("Fact extraction: Empty response from LLM")
                return {}
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                LoggingHelpers.log_json_extraction({"extracted": json_str})
            else:
                json_str = response
                LoggingHelpers.log_json_extraction({"full_response": json_str})
            
            # Try to parse the JSON
            try:
                facts = json.loads(json_str)
                
                if isinstance(facts, dict):
                    LoggingHelpers.log_json_parsing_success(str(facts)[:100])
                    return facts
                else:
                    LoggingHelpers.log_debug(f"Fact extraction: Response is not a dict: {type(facts)}")
                    return {}
                    
            except json.JSONDecodeError as json_error:
                LoggingHelpers.log_json_parsing_error(json_error, json_str)
                return {}
                
        except Exception as e:
            LoggingHelpers.log_exception_with_context("fact_extraction", e, {"message": message})
            return {}
        finally:
            LoggingHelpers.log_fact_extraction_end(0)  # 0 facts extracted by default
    
    def _store_extracted_facts(self, facts: Dict[str, str]) -> None:
        """Store extracted facts in memory"""
        stored_count = 0
        skipped_count = 0
        
        for key, value in facts.items():
            # Validate key and value before storing
            if key and value and isinstance(key, str) and isinstance(value, str):
                # Clean up the key and value
                clean_key = key.strip()
                clean_value = value.strip()
                
                if clean_key and clean_value:
                    LoggingHelpers.log_fact_processing(clean_key, stored_count + 1)
                    self.memory_service.add_fact(clean_key, clean_value)
                    stored_count += 1
                else:
                    LoggingHelpers.log_fact_skipped("empty after cleaning")
                    skipped_count += 1
            else:
                LoggingHelpers.log_fact_skipped("invalid format")
                skipped_count += 1
        
        LoggingHelpers.log_fact_storage_summary(stored_count + skipped_count, stored_count)
    
    def _send_to_ollama(self, message: str, model: str, temperature: float) -> None:
        """Send message to Ollama and handle response"""
        messages = self.conversation_service.get_messages()
        
        # Use STM+LTM context if memory enabled
        if self.is_memory_active():
            context_messages = self.memory_service.get_context_messages(current_query=message)
        else:
            context_messages = messages
        
        # Detect if this is a new conversation
        is_new_conversation = self._detect_new_conversation(context_messages)
        
        # Build the final context
        final_context = self._build_context(context_messages, is_new_conversation)
        
        # Auto model selection
        chosen_model = self._select_model(model, message, final_context)
        
        # Emit signal for UI to handle the actual Ollama call
        self.message_sent.emit(message)
        
        # Update status
        self.status_updated.emit(f"Processing with {chosen_model}")
    
    def _detect_new_conversation(self, context_messages: List[Dict[str, Any]]) -> bool:
        """Detect if this is a new conversation"""
        if self.is_new_conversation:
            LoggingHelpers.log_conversation_detection("explicit flag")
            return True
        
        if context_messages:
            user_messages = [msg for msg in context_messages if msg.get("role") == "user"]
            if len(user_messages) <= 1:
                LoggingHelpers.log_conversation_detection("message count")
                return True
        
        return False
    
    def _build_context(self, context_messages: List[Dict[str, Any]], is_new_conversation: bool) -> List[Dict[str, Any]]:
        """Build the final context for the AI"""
        # This would integrate with personality system
        # For now, return the context messages as-is
        return context_messages
    
    def _select_model(self, requested_model: str, message: str, context_messages: List[Dict[str, Any]]) -> str:
        """Select the appropriate model for the request"""
        if requested_model == "Auto":
            analyzer = RequestComplexityAnalyzer()
            complexity_metrics = analyzer.analyze_complexity(message, context_messages)
            available_models = self.ollama_service.get_models() or []
            chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
            
            # Add system message about model selection
            system_info = PromptFormatter.format_auto_model_selection_info(chosen_model)
            self.conversation_service.add_message("system", system_info)
            
            # Update conversation metadata with the chosen model
            self.conversation_manager.get_current_metadata().update_model(chosen_model)
            
            return chosen_model
        
        # Update conversation metadata with the requested model
        self.conversation_manager.get_current_metadata().update_model(requested_model)
        return requested_model
    
    def accumulate_assistant_response(self, chunk: str):
        """Accumulate assistant response chunk."""
        self._pending_assistant_response += chunk

    def clear_pending_assistant_response(self):
        self._pending_assistant_response = ""

    def handle_ai_response(self) -> None:
        """Handle AI response completion using accumulated response."""
        response = self._pending_assistant_response
        logger.debug(f"[ID:0155] DEBUG: handle_ai_response called with response length: {len(response)}")
        self.conversation_service.add_message("assistant", response)
        self.clear_pending_assistant_response()
        if self.is_memory_active():
            result = self.memory_service.intelligent_add_message({"role": "assistant", "content": response})
            LoggingHelpers.log_memory_result(response[:50], 1)  # Log with response preview and count
        messages = self.conversation_service.get_messages()
        logger.debug(f"[ID:0154] DEBUG: About to auto-save conversation with {len(messages)} messages")
        logger.debug(f"[ID:0153] DEBUG: Current conversation file: {self.conversation_manager.get_current_metadata().current_conversation_file}")
        saved_filepath = self.conversation_manager.auto_save_conversation(messages)
        if saved_filepath:
            logger.debug(f"[ID:0152] DEBUG: Conversation saved to: {saved_filepath}")
            self._trigger_name_generation(saved_filepath)
        else:
            logger.debug("[ID:0151] DEBUG: Auto-save returned None - conversation not saved")
        self.message_received.emit(response)
        self.conversation_updated.emit()
        self.status_updated.emit("Ready")
        
        # Trigger TTS for AI response if voice mode is active
        self._trigger_tts_for_response(response)
    
    def _trigger_tts_for_response(self, response: str) -> None:
        """Trigger TTS for AI response if voice mode is active"""
        try:
            logger.debug(f"[ID:0148A] _trigger_tts_for_response called with response length: {len(response)}")
            
            # Check if voice mode is active before triggering TTS
            if hasattr(self, '_chat_tab_reference') and self._chat_tab_reference:
                logger.debug("[ID:0148B] Chat tab reference available")
                # Check if voice mode is active in the chat tab
                if hasattr(self._chat_tab_reference, 'voice_mode') and self._chat_tab_reference.voice_mode:
                    logger.debug("[ID:0148C] Voice mode is active, proceeding with TTS")
                    # Remove all <think>...</think> blocks
                    spoken_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
                    # Remove emojis
                    spoken_text = remove_emojis(spoken_text)
                    logger.debug(f"[ID:0148D] Calling speak_ai_response with text length: {len(spoken_text)}")
                    self._chat_tab_reference.speak_ai_response(spoken_text)
                    logger.debug(f"[ID:0150] TTS triggered for AI response (length: {len(spoken_text)})")
                else:
                    logger.debug("[ID:0149A] Voice mode not active, skipping TTS")
            else:
                logger.debug("[ID:0149] No chat tab reference available for TTS")
        except Exception as e:
            logger.error(f"[ID:0148] Error triggering TTS for AI response: {e}")
            import traceback
            logger.error(f"[ID:0148E] TTS error traceback: {traceback.format_exc()}")
    
    def set_chat_tab_reference(self, chat_tab):
        """Set reference to chat tab for TTS functionality"""
        self._chat_tab_reference = chat_tab
    
    def get_ai_name(self) -> str:
        """Get the AI name from the current personality"""
        try:
            if self.personality_service:
                return self.personality_service.get_ai_name()
        except Exception as e:
            logger.error(f"Error getting AI name from personality service: {e}", print_to_terminal = True)
        return "AI Assistant"
    
    def _trigger_name_generation(self, filepath: str) -> None:
        """Trigger AI name generation for a conversation"""
        logger.debug(f"[ID:0147] DEBUG: Triggering name generation for: {filepath}")
        # Emit signal for UI to handle name generation
        self.name_generation_requested.emit(filepath)
        
    
    def start_new_conversation(self) -> None:
        """Start a new conversation"""
        logger.debug("[ID:0146] DEBUG: start_new_conversation called")
        
        # Check if there's already a blank conversation we can reuse
        existing_blank = self.conversation_manager.find_blank_conversation()
        if existing_blank:
            logger.debug(f"[ID:0145] DEBUG: Found existing blank conversation: {existing_blank}")
            # Use the existing blank conversation instead of creating a new one
            self.is_new_conversation = True
            self.conversation_service.clear_conversation()
            
            # Set the current conversation file to the existing blank one
            self.conversation_manager.get_current_metadata().current_conversation_file = existing_blank
            logger.debug(f"[ID:0144] DEBUG: Reusing existing blank conversation: {existing_blank}")
            
            # Emit signals to update UI
            self.conversation_updated.emit()
            self.status_updated.emit("Reused existing blank conversation")
            return
        
        # No blank conversation found, create a new one
        logger.debug("[ID:0143] DEBUG: No blank conversation found, creating new one")
        self.is_new_conversation = True
        self.conversation_service.clear_conversation()
        self.conversation_manager.clear_current_conversation()
        
        # Initialize a new conversation file for auto-saving
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filepath = os.path.join(
            self.conversation_manager.history_dir, 
            f"conversation_{timestamp}.json"
        )
        self.conversation_manager.get_current_metadata().current_conversation_file = new_filepath
        logger.debug(f"[ID:0142] DEBUG: Set new conversation file: {new_filepath}")
        
        # Create the initial empty conversation file
        saved_filepath = self.conversation_manager.auto_save_conversation([])
        if saved_filepath:
            logger.debug(f"[ID:0141] DEBUG: Initial conversation file created: {saved_filepath}")
        else:
            logger.debug("[ID:0140] DEBUG: Failed to create initial conversation file")
        
        self.conversation_updated.emit()
        self.status_updated.emit("Started new conversation")
    
    def clear_conversation(self) -> None:
        """Clear the current conversation"""
        self.conversation_service.clear_conversation()
        self.conversation_updated.emit()
        self.status_updated.emit("Conversation cleared")
    
    def load_conversation(self, filepath: str) -> None:
        """Load a conversation from file"""
        try:
            conversation, metadata = self.conversation_manager.load_conversation(filepath)
            self.conversation_service.conversation = conversation.copy()
            
            # Update current metadata with loaded metadata
            current_metadata = self.conversation_manager.get_current_metadata()
            current_metadata.created = metadata.created
            current_metadata.last_modified = metadata.last_modified
            current_metadata.model = metadata.model
            current_metadata.personality = metadata.personality
            current_metadata.message_count = metadata.message_count
            current_metadata.current_conversation_file = filepath
            current_metadata.ai_generated_name = metadata.ai_generated_name
            
            self.conversation_updated.emit()
            self.status_updated.emit(f"Loaded conversation: {metadata.get_display_info()}")
        except Exception as e:
            error_msg = PromptFormatter.format_error_message("conversation_load_failed", error=str(e))
            self.error_occurred.emit(error_msg)
    
    def delete_conversation(self, filepath: str) -> None:
        """Delete a conversation"""
        try:
            if (self.conversation_manager.get_current_metadata().current_conversation_file == filepath):
                self.conversation_service.clear_conversation()
                self.conversation_manager.clear_current_conversation()
                self.conversation_updated.emit()
            
            self.status_updated.emit("Conversation deleted")
        except Exception as e:
            error_msg = PromptFormatter.format_error_message("conversation_delete_failed", error=str(e))
            self.error_occurred.emit(error_msg)
    
    def rename_conversation(self, old_filepath: str, new_filepath: str) -> None:
        """Handle conversation rename"""
        try:
            if self.conversation_manager.get_current_metadata().current_conversation_file == new_filepath:
                self.conversation_updated.emit()
            
            old_name = old_filepath.split('/')[-1] if '/' in old_filepath else old_filepath
            new_name = new_filepath.split('/')[-1] if '/' in new_filepath else new_filepath
            status_msg = PromptFormatter.format_status_message("conversation_renamed", old=old_name, new=new_name)
            self.status_updated.emit(status_msg)
        except Exception as e:
            error_msg = PromptFormatter.format_error_message("conversation_rename_failed", error=str(e))
            self.error_occurred.emit(error_msg) 
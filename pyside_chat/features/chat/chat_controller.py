# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *

from pyside_chat.features.ollama.ollama_service import OllamaService
from pyside_chat.features.chat.conversation_service import ConversationService
from pyside_chat.features.chat.enhancers.enhancement_service import EnhancementService
from pyside_chat.features.memory.memory_service import MemoryService
from pyside_chat.core.models.conversation_metadata import ConversationManager
from pyside_chat.core.utils.prompts import PromptFormatter
from pyside_chat.features.chat.complexity_analyser.complexity_analyzer import RequestComplexityAnalyzer

"""
Chat Controller Module

This module implements the mediator pattern to separate business logic from UI components.
It handles communication between different services and UI components.
"""

from typing import Dict, Any, Optional, List
import os

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
                 personality_service=None,
                 config_manager=None):
        super().__init__()
        
        # Store service references
        self.ollama_service = ollama_service
        self.conversation_service = conversation_service
        self.enhancement_service = enhancement_service
        self.memory_service = memory_service
        self.conversation_manager = conversation_manager
        self.personality_service = personality_service
        self.config_manager = config_manager
        
        # Initialize streaming state variables
        self._streaming_thoughts_buffer = ''
        self._in_think_block = False
        self._think_completed = False  # Initialize the missing attribute
        self._last_streaming_chunk = ""
        self._last_streaming_msg_id = None
        
        # Initialize pending response buffer
        self._pending_assistant_response = ""
        
        # Track if this is a new conversation
        self.is_new_conversation = True
        
        # Chat tab reference for TTS functionality
        self.chat_tab_reference = None
        
        logger.debug("[ID:0156] ChatController initialized successfully")
    
    def is_memory_active(self) -> bool:
        """Check if memory is enabled and available"""
        return self.memory_service is not None
    
    def process_user_message(self, message: str, model: str, temperature: float) -> None:
        """Process a user message and send to Ollama"""
        try:
            # CRITICAL FIX: Prevent empty messages from being processed
            if not message or not message.strip():
                logger.warning("[EMPTY_MESSAGE] Attempted to process empty user message - ignoring")
                return
            logger.debug(f"[ID:0157] DEBUG: process_user_message called with message: {message}", print_to_terminal=True)
            
            
            # Check if this is the first message in a new conversation
            if not self.conversation_service.get_messages():
                # This is the first message and we haven't explicitly started a new conversation
                self.start_new_conversation()
                LoggingHelpers.log_debug("Auto-started new conversation for first message")
            
            # Add message to conversation
            self.conversation_service.add_message("user", message)
            
            # CRITICAL FIX: Auto-save conversation after adding user message
            messages = self.conversation_service.get_messages()
            logger.debug(f"[AUTO_SAVE] Auto-saving conversation with {len(messages)} messages after user message")
            saved_filepath = self.conversation_manager.auto_save_conversation(messages)
            if saved_filepath:
                logger.debug(f"[AUTO_SAVE] Conversation saved to: {saved_filepath}")
                # Trigger name generation for new conversations
                if self.is_new_conversation:
                    self._trigger_name_generation(saved_filepath)
            else:
                logger.warning("[AUTO_SAVE] Failed to auto-save conversation after user message")
            
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
            # Use ThreadingService for fact extraction instead of direct threading
            from pyside_chat.core.threading.threading_service import get_global_threading_service
            threading_service = get_global_threading_service()
            
            # Create a simple fact extraction task using the threading service
            # This will be handled by the thread pool manager
            response = ""
            response_chunks = []
            
            # Use the Ollama service directly for fact extraction
            chunks = self.ollama_service.send_chat_message(
                model="qwen3:0.6b",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.0,
                stream=True
            )
            
            # Collect all chunks
            for chunk in chunks:
                response_chunks.append(chunk)
                response += chunk
            
            response = response.strip()
            
            # Parse the response as JSON
            try:
                # Try to extract JSON from the response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    facts = json.loads(json_match.group())
                    LoggingHelpers.log_fact_extraction_result([facts])
                    return facts
                else:
                    LoggingHelpers.log_debug("No JSON found in fact extraction response")
                    return {}
                    
            except json.JSONDecodeError as e:
                LoggingHelpers.log_debug(f"Failed to parse fact extraction response as JSON: {e}")
                return {}
                
        except Exception as e:
            LoggingHelpers.log_exception_with_context("extract_facts_with_llm", e, {"message": message})
            return {}
    
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
        
        # Note: Model selection is now handled by the event bus
        # to prevent duplicate system messages
        
        # Emit signal for UI to handle the actual Ollama call
        self.message_sent.emit(message)
        
        # Update status
        self.status_updated.emit(f"Processing with {model}")
    
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
        """Accumulate assistant response chunk, handling <think> blocks during streaming."""
        try:
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] accumulate_assistant_response called with chunk length: {len(chunk)}")
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] Chunk content preview: '{chunk[:50]}...'")
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] Full chunk content: '{chunk}'")
            
            # Check if chunk is empty or whitespace
            if not chunk or not chunk.strip():
                logger.warning(f"[CHAT_CONTROLLER_DEBUG] Received empty or whitespace-only chunk, skipping accumulation")
                return
            
            # Check typewriter setting - if disabled, accumulate in separate buffer
            typewriter_enabled = self.config_manager.get("typewriter_enabled", False) if self.config_manager else False
            if not typewriter_enabled:
                # Accumulate in separate buffer for typewriter-disabled mode
                if not hasattr(self, '_typewriter_disabled_buffer'):
                    self._typewriter_disabled_buffer = ""
                self._typewriter_disabled_buffer += chunk
                logger.debug(f"[CHAT_CONTROLLER_DEBUG] Typewriter disabled, accumulated in buffer: '{chunk[:50]}...'")
                return
            
            # Check for malformed output (repeating patterns that suggest AI malfunction)
            if len(chunk) > 10:
                # Check for repeating patterns like "wordword" or "phrase phrase"
                import re
                # More comprehensive pattern detection
                repeating_pattern = re.search(r'(\w+)\1{2,}', chunk)  # 3 or more repetitions
                double_word_pattern = re.search(r'(\w+)\s+\1', chunk)  # repeated words with space
                if repeating_pattern or double_word_pattern:
                    logger.warning(f"[CHAT_CONTROLLER_DEBUG] Detected repeating pattern in chunk: '{chunk[:50]}...'")
                    logger.warning(f"[CHAT_CONTROLLER_DEBUG] Pattern type: repeating={repeating_pattern}, double_word={double_word_pattern}")
                    return  # Skip this chunk to prevent corruption
            
            # Initialize streaming state if needed
            if self._last_streaming_msg_id is None:
                streaming_message_id = self.conversation_service.get_streaming_message_id()
                if streaming_message_id:
                    self._last_streaming_msg_id = streaming_message_id
            
            # Check for qwen model format: "Thinking..." and "...done thinking."
            if not self._in_think_block and "Thinking..." in chunk:
                # Start of qwen thinking format
                self._in_think_block = True
                self._think_completed = False
                self._streaming_thoughts_buffer = ""
                logger.debug(f"[CHAT_CONTROLLER_DEBUG] Started qwen thinking format")
                return
            
            # If we're in a think block, accumulate in thought buffer and check for closing tag
            if self._in_think_block:
                self._streaming_thoughts_buffer += chunk
                logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added to thought buffer: '{chunk[:20]}...'")
                
                # Check for qwen thinking end: "...done thinking."
                if "...done thinking." in self._streaming_thoughts_buffer:
                    # Split the buffer at "...done thinking."
                    parts = self._streaming_thoughts_buffer.split("...done thinking.", 1)
                    
                    # The first part is the thought content (without "...done thinking.")
                    thought_content = parts[0].strip()
                    
                    # The second part (if any) is content that came after "...done thinking."
                    content_after_think = parts[1].strip() if len(parts) > 1 else ""
                    
                    # Store the thought
                    self.conversation_service.update_streaming_message_thought(thought_content)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Completed qwen thought: '{thought_content[:50]}...'")
                    
                    # Reset think block state
                    self._in_think_block = False
                    self._think_completed = True
                    self._streaming_thoughts_buffer = ""
                    
                    # If there's content after "...done thinking.", add it to the main message
                    if content_after_think:
                        self.conversation_service.update_streaming_message_content(content_after_think)
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added to main message after qwen thinking: '{content_after_think[:50]}...'")
                    
                    return
                
                # Check if we have a complete </think> tag in the accumulated buffer (for other models)
                elif '</think>' in self._streaming_thoughts_buffer:
                    # Use MessageFormatter to properly split the accumulated buffer
                    from pyside_chat.ui.themes.message_formatter import MessageFormatter
                    full_buffer = self._streaming_thoughts_buffer
                    thoughts, answer = MessageFormatter.split_thoughts_and_answer(full_buffer)
                    
                    if thoughts is not None:
                        # Store the thoughts
                        self.conversation_service.update_streaming_message_thought(thoughts)
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Completed thought: '{thoughts[:50]}...'")
                        
                        # Reset think block state
                        self._in_think_block = False
                        self._think_completed = True
                        self._streaming_thoughts_buffer = ""
                        
                        # Add the answer to the main message
                        if answer:
                            self.conversation_service.update_streaming_message_content(answer)
                            logger.debug(f"[CHAT_CONTROLLER_DEBUG] Started main message after </think>: '{answer[:50]}...'")
                    else:
                        # Fallback to old logic if MessageFormatter doesn't find <think> tags
                        parts = self._streaming_thoughts_buffer.split('</think>', 1)
                        thought_content = parts[0].strip()
                        content_after_think = parts[1].strip() if len(parts) > 1 else ""
                        
                        self.conversation_service.update_streaming_message_thought(thought_content)
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Completed thought (fallback): '{thought_content[:50]}...'")
                        
                        self._in_think_block = False
                        self._think_completed = True
                        self._streaming_thoughts_buffer = ""
                        
                        if content_after_think:
                            self.conversation_service.update_streaming_message_content(content_after_think)
                            logger.debug(f"[CHAT_CONTROLLER_DEBUG] Started main message after </think> (fallback): '{content_after_think[:50]}...'")
                    
                    return
                
                # If we're still in think block but think is completed, accumulate in main message
                elif self._think_completed:
                    # We're out of think block, add to main message
                    # Since we're in post-think mode, just append to the main message
                    current_content = self.conversation_service.get_streaming_message_content()
                    new_content = current_content + chunk
                    self.conversation_service.update_streaming_message_content(new_content)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Appended to main message (post-think): '{chunk[:20]}...'")
                    return
                
                # Still in think block, check if this chunk contains the transition to response
                else:
                    # Check if this chunk contains a transition from thinking to responding
                    # Look for patterns that indicate the start of the actual response
                    response_start_patterns = [
                        r'Hello!', r'Hi!', r'Hey!', r'Hello,', r'Hi,', r'Hey,',
                        r'That\'s interesting!', r'That\'s great!', r'That\'s cool!',
                        r'How\'s your day', r'How are you', r'What can I help',
                        r'[A-Z][a-z]+!',  # Words starting with capital letter followed by !
                        r'[A-Z][a-z]+,'   # Words starting with capital letter followed by ,
                    ]
                    
                    for pattern in response_start_patterns:
                        match = re.search(pattern, chunk)
                        if match:
                            # Found a response start, split the chunk
                            response_start = match.start()
                            thought_part = chunk[:response_start].strip()
                            response_part = chunk[response_start:].strip()
                            
                            # Add the thought part to the thought buffer
                            if thought_part:
                                self._streaming_thoughts_buffer += thought_part
                                logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added final thought part: '{thought_part[:20]}...'")
                            
                            # Store the completed thought
                            thought_content = self._streaming_thoughts_buffer.strip()
                            self.conversation_service.update_streaming_message_thought(thought_content)
                            logger.debug(f"[CHAT_CONTROLLER_DEBUG] Completed thought: '{thought_content[:50]}...'")
                            
                            # Reset think block state
                            self._in_think_block = False
                            self._think_completed = True
                            self._streaming_thoughts_buffer = ""
                            
                            # Add the response part to the main message
                            if response_part:
                                self.conversation_service.update_streaming_message_content(response_part)
                                logger.debug(f"[CHAT_CONTROLLER_DEBUG] Started response: '{response_part[:50]}...'")
                            
                            return
                    
                    # No response transition found, continue accumulating in thought buffer
                    self._streaming_thoughts_buffer += chunk
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added to thought buffer: '{chunk[:20]}...'")
                    return
            
            # If we're not in a think block, check if this chunk starts a new think block
            if not self._in_think_block:
                # Check if this chunk starts a new think block
                if '<think>' in chunk:
                    # Split at <think> to get content before and after
                    parts = chunk.split('<think>', 1)
                    
                    # If there's content before <think>, add it to main message
                    if parts[0].strip():
                        self.conversation_service.update_streaming_message_content(parts[0].strip())
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added to main message before <think>: '{parts[0].strip()[:20]}...'")
                    
                    # Start accumulating in thought buffer
                    self._in_think_block = True
                    self._think_completed = False
                    self._streaming_thoughts_buffer = parts[1] if len(parts) > 1 else ""
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Started thought buffer: '{self._streaming_thoughts_buffer[:20]}...'")
                    return
                
                # If think is completed, add to main message
                elif self._think_completed:
                    self.conversation_service.update_streaming_message_content(chunk)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added to main message (think completed): '{chunk[:20]}...'")
                    return
                
                # Regular content, add to main message
                else:
                    # Use the MessageFormatter to check if this chunk contains <think> tags
                    from pyside_chat.ui.themes.message_formatter import MessageFormatter
                    thoughts, answer = MessageFormatter.split_thoughts_and_answer(chunk)
                    
                    if thoughts is not None:
                        # This chunk contains <think> tags, process it properly
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Found <think> tags in chunk, thoughts: '{thoughts[:50]}...', answer: '{answer[:50]}...'")
                        
                        # Store the thoughts
                        self.conversation_service.update_streaming_message_thought(thoughts)
                        
                        # Add the answer to the main message
                        if answer:
                            self.conversation_service.update_streaming_message_content(answer)
                        
                        # Mark think as completed
                        self._think_completed = True
                        return
                    else:
                        # No <think> tags, add to main message
                        self.conversation_service.update_streaming_message_content(chunk)
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added to main message: '{chunk[:20]}...'")
                        return
            
        except Exception as e:
            logger.error(f"[CHAT_CONTROLLER_ERROR] Error in accumulate_assistant_response: {str(e)}")
            logger.error(f"[CHAT_CONTROLLER_ERROR] Chunk was: '{chunk[:100]}...'")
            # Don't crash the application, just log the error

    def clear_pending_assistant_response(self):
        self._pending_assistant_response = ""

    def start_streaming_response(self) -> str:
        """Start a new streaming assistant response, resetting streaming state."""
        # Check typewriter setting
        typewriter_enabled = self.config_manager.get("typewriter_enabled", False) if self.config_manager else False
        
        # Reset streaming state variables
        self._in_think_block = False
        self._think_completed = False
        self._streaming_thoughts_buffer = ""
        self._last_streaming_chunk = ""
        self._last_streaming_msg_id = None
        
        # Clear typewriter disabled buffer if it exists
        if hasattr(self, '_typewriter_disabled_buffer'):
            self._typewriter_disabled_buffer = ""
        
        logger.debug(f"[STREAM_RESET] Reset streaming state for new assistant response (typewriter: {typewriter_enabled})")
        
        if typewriter_enabled:
            # Start new streaming message only when typewriter is enabled
            return self.conversation_service.start_streaming_message("assistant")
        else:
            # Don't create streaming message when typewriter is disabled
            logger.debug("[STREAM_RESET] Typewriter disabled, skipping streaming message creation")
            return None

    def finalize_streaming_response(self) -> bool:
        """Finalize the current streaming response, merging any buffered thoughts if present."""
        try:
            # Check typewriter setting
            typewriter_enabled = self.config_manager.get("typewriter_enabled", False) if self.config_manager else False
            
            if not typewriter_enabled and hasattr(self, '_typewriter_disabled_buffer') and self._typewriter_disabled_buffer:
                # Typewriter disabled: process the complete accumulated response
                complete_response = self._typewriter_disabled_buffer
                logger.debug(f"[CHAT_CONTROLLER_DEBUG] Typewriter disabled, processing complete response: '{complete_response[:100]}...'")
                
                # Use MessageFormatter to properly split thoughts and answer
                from pyside_chat.ui.themes.message_formatter import MessageFormatter
                thoughts, answer = MessageFormatter.split_thoughts_and_answer(complete_response)
                
                # Add the complete message to conversation service
                if thoughts and answer:
                    # Add message with thoughts
                    self.conversation_service.add_message("assistant", answer, thought=thoughts)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added complete message with thoughts: '{answer[:50]}...'")
                elif answer:
                    # Add message without thoughts
                    self.conversation_service.add_message("assistant", answer)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added complete message: '{answer[:50]}...'")
                else:
                    # Fallback: add the complete response as-is
                    self.conversation_service.add_message("assistant", complete_response)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Added complete response as fallback: '{complete_response[:50]}...'")
                
                # Clear the buffer
                self._typewriter_disabled_buffer = ""
                return True
            elif not typewriter_enabled:
                # Typewriter disabled but no buffer content - nothing to do
                logger.debug("[CHAT_CONTROLLER_DEBUG] Typewriter disabled but no buffer content")
                return True
            
            streaming_message_id = self.conversation_service.get_streaming_message_id()
            current_msg = self.conversation_service.get_message_by_id(streaming_message_id) if streaming_message_id else None
            
            # Debug logging
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] finalize_streaming_response called")
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] _in_think_block: {getattr(self, '_in_think_block', False)}")
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] _think_completed: {getattr(self, '_think_completed', False)}")
            logger.debug(f"[CHAT_CONTROLLER_DEBUG] _streaming_thoughts_buffer length: {len(getattr(self, '_streaming_thoughts_buffer', ''))}")
            if hasattr(self, '_streaming_thoughts_buffer') and self._streaming_thoughts_buffer:
                logger.debug(f"[CHAT_CONTROLLER_DEBUG] _streaming_thoughts_buffer preview: '{self._streaming_thoughts_buffer[:100]}...'")
            
            # Handle case where entire response was in think block
            if current_msg is not None and self._in_think_block and self._streaming_thoughts_buffer.strip():
                # Use MessageFormatter to properly split the accumulated buffer
                from pyside_chat.ui.themes.message_formatter import MessageFormatter
                full_buffer = self._streaming_thoughts_buffer.strip()
                thoughts, answer = MessageFormatter.split_thoughts_and_answer(full_buffer)
                
                if thoughts is not None:
                    # Store the thoughts
                    self.conversation_service.update_streaming_message_thought(thoughts)
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] Completed thought: '{thoughts[:50]}...'")
                    
                    # Add the answer to the main message
                    if answer:
                        self.conversation_service.update_streaming_message_content(answer)
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] Final answer: '{answer[:50]}...'")
                    else:
                        # If no answer found, use a default response
                        self.conversation_service.update_streaming_message_content("I'm here to help! How can I assist you today?")
                        logger.debug(f"[CHAT_CONTROLLER_DEBUG] No answer found, using default response")
                else:
                    # Fallback: treat entire buffer as thought and use default response
                    self.conversation_service.update_streaming_message_thought(full_buffer)
                    self.conversation_service.update_streaming_message_content("I'm here to help! How can I assist you today?")
                    logger.debug(f"[CHAT_CONTROLLER_DEBUG] No <think> tags found, using fallback")
                
                # Reset the thought buffer and state after processing
                self._streaming_thoughts_buffer = ''
                self._in_think_block = False
                self._think_completed = True
            
            elif ((hasattr(self, '_streaming_thoughts_buffer') and self._streaming_thoughts_buffer.strip()) or getattr(self, '_in_think_block', False)) and current_msg is not None:
                # Store any remaining thought in the thought field
                remaining_thought = self._streaming_thoughts_buffer.strip()
                if remaining_thought:
                    current_thought = current_msg.get('thought', '')
                    new_thought = current_thought + remaining_thought
                    self.conversation_service.update_streaming_message_thought(new_thought)
                self._streaming_thoughts_buffer = ''
                self._in_think_block = False
                self.conversation_service.conversation_updated.emit(self.conversation_service.conversation)
            
            # Ensure message content is never empty
            if current_msg is not None and not current_msg['content']:
                current_msg['content'] = ''
                self.conversation_service.conversation_updated.emit(self.conversation_service.conversation)
            
            # Finalize via conversation service only (do not call super())
            success = self.conversation_service.finalize_streaming_message()
            if success:
                logger.debug("[ID:STREAM002] Successfully finalized streaming response")
            else:
                logger.warning("[ID:STREAM003] Failed to finalize streaming response")
            return success
        except Exception as e:
            logger.error(f"[CHAT_CONTROLLER_ERROR] Error in finalize_streaming_response: {str(e)}")
            # Don't crash the application, just log the error
            # Try to reset state anyway
            try:
                self.reset_streaming_state()
            except:
                pass
            return False

    def handle_ai_response(self) -> None:
        """Handle AI response completion using accumulated response."""
        # Check typewriter setting
        typewriter_enabled = self.config_manager.get("typewriter_enabled", False) if self.config_manager else False
        
        if not typewriter_enabled and hasattr(self, '_typewriter_disabled_buffer') and self._typewriter_disabled_buffer:
            # Typewriter disabled: process the complete accumulated response
            complete_response = self._typewriter_disabled_buffer
            logger.debug(f"[HANDLE_AI_RESPONSE] Typewriter disabled, processing complete response: '{complete_response[:100]}...'")
            
            # Use MessageFormatter to properly split thoughts and answer
            from pyside_chat.ui.themes.message_formatter import MessageFormatter
            thoughts, answer = MessageFormatter.split_thoughts_and_answer(complete_response)
            
            # Add the complete message to conversation service
            if thoughts and answer:
                # Add message with thoughts
                self.conversation_service.add_message("assistant", answer, thought=thoughts)
                response_content = answer
                logger.debug(f"[HANDLE_AI_RESPONSE] Added complete message with thoughts: '{answer[:50]}...'")
            elif answer:
                # Add message without thoughts
                self.conversation_service.add_message("assistant", answer)
                response_content = answer
                logger.debug(f"[HANDLE_AI_RESPONSE] Added complete message: '{answer[:50]}...'")
            else:
                # Fallback: add the complete response as-is
                self.conversation_service.add_message("assistant", complete_response)
                response_content = complete_response
                logger.debug(f"[HANDLE_AI_RESPONSE] Added complete response as fallback: '{complete_response[:50]}...'")
            
            # Clear the buffer
            self._typewriter_disabled_buffer = ""
        else:
            # Typewriter enabled: handle normal streaming response
            response_content = ""
            
            # Find the streaming message with actual content
            streaming_message_with_content = self.conversation_service.get_streaming_message_with_content()
            
            if streaming_message_with_content:
                # Finalize the message with content
                message_id = streaming_message_with_content["id"]
                logger.debug(f"[ID:0156] Found streaming message with content: {message_id}, content length: {len(streaming_message_with_content['content'])}")
                
                # Update the streaming message ID to the one with content
                self.conversation_service._streaming_message_id = message_id
                
                # Finalize the streaming response
                self.finalize_streaming_response()
                response_content = streaming_message_with_content["content"]
            else:
                # Check if there's a current streaming message ID (might be empty)
                streaming_id = self.conversation_service.get_streaming_message_id()
                if streaming_id:
                    self.finalize_streaming_response()
                    response_msg = self.conversation_service.get_message_by_id(streaming_id)
                    if response_msg:
                        response_content = response_msg["content"]
                    else:
                        response_content = self._pending_assistant_response
                else:
                    # Add the assistant response to the conversation service
                    response_content = self._pending_assistant_response
                    if response_content.strip():
                        self.conversation_service.add_message("assistant", response_content)

        logger.debug(f"[ID:0155] DEBUG: handle_ai_response called with response length: {len(response_content)}")
        self.clear_pending_assistant_response()
        if self.is_memory_active():
            result = self.memory_service.intelligent_add_message({"role": "assistant", "content": response_content})
            LoggingHelpers.log_memory_result(response_content[:50], 1)  # Log with response preview and count
        messages = self.conversation_service.get_messages()
        logger.debug(f"[ID:0154] DEBUG: About to auto-save conversation with {len(messages)} messages")
        logger.debug(f"[ID:0153] DEBUG: Current conversation file: {self.conversation_manager.get_current_metadata().current_conversation_file}")
        saved_filepath = self.conversation_manager.auto_save_conversation(messages)
        if saved_filepath:
            logger.debug(f"[ID:0152] DEBUG: Conversation saved to: {saved_filepath}")
            self._trigger_name_generation(saved_filepath)
        else:
            logger.debug("[ID:0151] DEBUG: Auto-save returned None - conversation not saved")
        self.message_received.emit(response_content)
        self.conversation_updated.emit()
        self.status_updated.emit("Ready")
        voice_mode = getattr(getattr(self, '_chat_tab_reference', None), 'voice_mode', None)
        if voice_mode:
            self._trigger_tts_for_response(response_content)
        else:
            logger.debug("[ID:0151] DEBUG: Voice mode not active, skipping TTS")
            logger.debug(f"[ID:0151A] Voice mode value: {voice_mode if voice_mode is not None else 'Not set (no _chat_tab_reference or no voice_mode attribute)'}")
    def _trigger_tts_for_response(self, response: str) -> None:
        """Trigger TTS for AI response if voice mode is active"""
        try:
            logger.debug(f"[ID:0148A] _trigger_tts_for_response called with response length: {len(response)}")
            logger.debug(f"[ID:0148B] Response preview: {response[:100]}...")
            
            # Check if voice mode is active before triggering TTS
            if hasattr(self, '_chat_tab_reference') and self._chat_tab_reference:
                logger.debug("[ID:0148C] Chat tab reference available")
                # Check if voice mode is active in the chat tab
                if hasattr(self._chat_tab_reference, 'voice_mode') and self._chat_tab_reference.voice_mode:
                    logger.debug("[ID:0148D] Voice mode is active, proceeding with TTS")
                    # Remove all <think>...</think> blocks
                    spoken_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
                    # Remove emojis
                    spoken_text = remove_emojis(spoken_text)
                    logger.debug(f"[ID:0148E] Calling speak_ai_response with text length: {len(spoken_text)}")
                    logger.debug(f"[ID:0148F] Spoken text preview: {spoken_text[:100]}...")
                    self._chat_tab_reference.speak_ai_response(spoken_text)
                    logger.debug(f"[ID:0150] TTS triggered for AI response (length: {len(spoken_text)})")
                else:
                    logger.debug("[ID:0149A] Voice mode not active, skipping TTS")
                    logger.debug(f"[ID:0149B] Voice mode value: {getattr(self._chat_tab_reference, 'voice_mode', 'Not set')}")
            else:
                logger.debug("[ID:0149] No chat tab reference available for TTS")
                logger.debug(f"[ID:0149C] Has _chat_tab_reference: {hasattr(self, '_chat_tab_reference')}")
                if hasattr(self, '_chat_tab_reference'):
                    logger.debug(f"[ID:0149D] _chat_tab_reference value: {self._chat_tab_reference}")
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
        
    def reset_streaming_state(self):
        """Reset all streaming state variables for a clean start"""
        self._streaming_thoughts_buffer = ''
        self._in_think_block = False
        self._think_completed = False
        self._last_streaming_chunk = ""
        self._last_streaming_msg_id = None
        self._pending_assistant_response = ""
        if hasattr(self, '_typewriter_disabled_buffer'):
            self._typewriter_disabled_buffer = ""
        logger.debug("[STREAM_RESET] Reset all streaming state variables")

    def start_new_conversation(self) -> None:
        """Start a new conversation"""
        try:
            logger.debug("[ID:0146] DEBUG: start_new_conversation called")
            
            # Reset streaming state for clean start
            self.reset_streaming_state()
            
            # Clear the current conversation
            self.conversation_service.clear_conversation()
            
            # Reset new conversation flag
            self.is_new_conversation = True
            
            # Create a new conversation file
            new_filepath = self.conversation_manager.create_new_conversation()
            if new_filepath:
                logger.debug(f"[ID:0142] DEBUG: Set new conversation file: {new_filepath}")
                logger.debug(f"[ID:0141] DEBUG: Initial conversation file created: {new_filepath}")
                
                # Trigger name generation for the new conversation
                self.name_generation_requested.emit(new_filepath)
            else:
                logger.error("[ID:0140] DEBUG: Failed to create new conversation file")
                
        except Exception as e:
            logger.error(f"[ID:0139] Error starting new conversation: {e}")
            self.error_occurred.emit(f"Failed to start new conversation: {str(e)}")

    def clear_conversation(self) -> None:
        """Clear the current conversation"""
        try:
            logger.debug("[ID:0145] DEBUG: clear_conversation called")
            
            # Reset streaming state for clean start
            self.reset_streaming_state()
            
            # Clear the conversation
            self.conversation_service.clear_conversation()
            
            # Reset new conversation flag
            self.is_new_conversation = True
            
            logger.debug("[ID:0144] DEBUG: Conversation cleared successfully")
            
        except Exception as e:
            logger.error(f"[ID:0143] Error clearing conversation: {e}")
            self.error_occurred.emit(f"Failed to clear conversation: {str(e)}")
    
    def load_conversation(self, filepath: str) -> None:
        """Load a conversation from file"""
        try:
            # CRITICAL FIX: Use conversation service's load_conversation method to properly reset state
            filename = os.path.basename(filepath)
            self.conversation_service.load_conversation(filename)
            
            # Get metadata from conversation manager
            conversation, metadata = self.conversation_manager.load_conversation(filepath)
            
            # Update current metadata with loaded metadata
            current_metadata = self.conversation_manager.get_current_metadata()
            current_metadata.created = metadata.created
            current_metadata.last_modified = metadata.last_modified
            current_metadata.model = metadata.model
            current_metadata.personality = metadata.personality
            current_metadata.message_count = metadata.message_count
            current_metadata.current_conversation_file = filepath
            current_metadata.ai_generated_name = metadata.ai_generated_name
            
            logger.debug(f"[LOAD_FIX] Loaded conversation with {len(self.conversation_service.conversation)} messages")
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

    def reset_ai_response_guard(self):
        """Reset the AI response guard for a new streaming session."""
        self._ai_response_handled = False 
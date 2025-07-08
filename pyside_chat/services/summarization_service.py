"""
Summarization Service
Handles AI-powered conversation summarization for generating chat names.
"""

import json
from typing import List, Dict, Optional
from PySide6.QtCore import QObject, Signal
from pyside_chat.services.ollama_service import OllamaService
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class SummarizationService(QObject):
    """Service for generating AI-powered conversation summaries and names"""
    
    # Signals
    summarization_completed = Signal(str, str)  # Emits (filepath, generated_name)
    summarization_failed = Signal(str, str)     # Emits (filepath, error_message)
    
    def __init__(self, ollama_service: OllamaService):
        super().__init__()
        self.ollama_service = ollama_service
        self.summarization_model = "Auto"  # Use auto mode to select smallest model
        self.min_messages_for_summarization = 3   # Reduced minimum messages for testing
        
    def generate_chat_name(self, conversation: List[Dict], filepath: str) -> None:
        """
        Generate an AI-powered name for a conversation
        
        Args:
            conversation: List of conversation messages
            filepath: Path to the conversation file
        """
        try:
            logger.info(f"[ID:0194] Starting name generation for conversation: {filepath}")
            logger.info(f"[ID:0193] Conversation has {len(conversation)} messages, minimum required: {self.min_messages_for_summarization}")
            
            # Check if we have enough messages to summarize
            if len(conversation) < self.min_messages_for_summarization:
                logger.debug(f"[ID:0192] Not enough messages ({len(conversation)}) for summarization")
                return
            
            # Extract user messages for summarization
            user_messages = [msg.get('content', '') for msg in conversation if msg.get('role') == 'user']
            if not user_messages:
                logger.debug("[ID:0191] No user messages found for summarization")
                return
            
            # Check if the conversation has enough substance for meaningful naming
            if not self._has_enough_substance(user_messages):
                logger.debug("[ID:0190] Conversation lacks sufficient substance for meaningful naming")
                return
            
            logger.info(f"[ID:0189] Found {len(user_messages)} user messages for summarization")
            logger.info(f"[ID:0188] User messages: {user_messages}")
            
            # Create summarization prompt
            prompt = self._create_summarization_prompt(user_messages)
            logger.info(f"[ID:0187] Summarization prompt: {prompt}")
            
            # Send to Ollama for summarization
            messages = [{"role": "user", "content": prompt}]
            
            # Use auto mode to select the smallest available model for summarization
            if self.summarization_model == "Auto":
                from pyside_chat.utils.complexity_analyzer import RequestComplexityAnalyzer
                analyzer = RequestComplexityAnalyzer()
                
                # Get available models
                available_models = self.ollama_service.get_models()
                if not available_models:
                    logger.warning("[ID:0186] No models available for summarization")
                    self.summarization_failed.emit(filepath, "No models available")
                    return
                
                # Analyze complexity (summarization is a simple task)
                complexity_metrics = analyzer.analyze_complexity(prompt)
                chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
                
                logger.info(f"[ID:0185] Auto-selected model for summarization: {chosen_model}")
            else:
                chosen_model = self.summarization_model
            
            logger.info(f"[ID:0184] Sending summarization request to model: {chosen_model}")
            logger.info(f"[ID:0183] Request messages: {messages}")
            
            # Use the selected model for summarization
            response = ""
            for chunk in self.ollama_service.send_chat_message(
                model=chosen_model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent results
                stream=True
            ):
                response += chunk
            
            logger.info(f"[ID:0182] Raw AI response: '{response}'")
            
            # Clean and validate the response
            generated_name = self._clean_generated_name(response)
            logger.info(f"[ID:0181] Cleaned generated name: '{generated_name}'")
            
            if generated_name:
                logger.info(f"[ID:0180] Generated chat name: {generated_name}")
                self.summarization_completed.emit(filepath, generated_name)
            else:
                logger.warning("[ID:0179] Failed to generate valid chat name")
                logger.warning(f"[ID:0178] Raw response was: '{response}'")
                self.summarization_failed.emit(filepath, "Failed to generate valid name")
                
        except Exception as e:
            logger.error(f"[ID:0177] Error generating chat name: {str(e)}")
            self.summarization_failed.emit(filepath, str(e))
    
    def _create_summarization_prompt(self, user_messages: List[str]) -> str:
        """Create a prompt for generating a concise chat name"""
        # Take the first few user messages to understand the conversation topic
        sample_messages = user_messages[:5]  # Limit to first 5 messages
        messages_text = "\n".join([f"- {msg}" for msg in sample_messages])
        
        prompt = f"""Based on the following user messages from a conversation, generate a meaningful, descriptive name (3-6 words) that captures the main topic or theme.

IMPORTANT GUIDELINES:
- The name should be clear, specific, and professional
- Avoid generic terms like "conversation", "chat", "discussion"
- Avoid random or nonsensical combinations
- Focus on the actual subject matter or problem being discussed
- If the conversation lacks a clear topic, do not generate a name

User messages:
{messages_text}

Generate a concise, meaningful name that accurately describes what this conversation is about. If the conversation lacks substance or clear topic, respond with "NO_TOPIC". Return only the name or "NO_TOPIC", nothing else."""

        logger.debug(f"[ID:0176] Created summarization prompt with {len(sample_messages)} sample messages")
        logger.debug(f"[ID:0175] Sample messages: {sample_messages}")
        
        return prompt
    
    def _clean_generated_name(self, response: str) -> Optional[str]:
        """Clean and validate the generated name"""
        logger.debug(f"[ID:0174] Cleaning response: '{response}'")
        
        if not response:
            logger.debug("[ID:0173] Response is empty")
            return None
        
        # Clean the response
        name = response.strip()
        logger.debug(f"[ID:0172] After strip: '{name}'")
        
        # Remove <think> tags and their content
        import re
        name = re.sub(r'<think>.*?</think>', '', name, flags=re.DOTALL)
        name = name.strip()
        logger.debug(f"[ID:0171] After removing <think> tags: '{name}'")
        
        # Remove common prefixes/suffixes that models might add
        prefixes_to_remove = [
            "The conversation is about:",
            "This conversation is about:",
            "Name:",
            "Title:",
            "Chat name:",
            "Generated name:"
        ]
        
        for prefix in prefixes_to_remove:
            if name.lower().startswith(prefix.lower()):
                name = name[len(prefix):].strip()
                logger.debug(f"[ID:0170] Removed prefix '{prefix}', result: '{name}'")
        
        # Remove quotes if present
        name = name.strip('"\'')
        logger.debug(f"[ID:0169] After quote removal: '{name}'")
        
        # Check for NO_TOPIC response
        if name.upper() == "NO_TOPIC":
            logger.debug("[ID:0168] AI indicated no clear topic found")
            return None
        
        # Validate the name length
        if len(name) < 3:
            logger.debug(f"[ID:0167] Name too short ({len(name)} chars): '{name}'")
            return None
        
        if len(name) > 50:
            logger.debug(f"[ID:0166] Name too long ({len(name)} chars): '{name}'")
            return None
        
        # Check if it's not just generic responses
        generic_responses = [
            "conversation", "chat", "discussion", "talk", "dialogue",
            "new chat", "chat session", "conversation about", "discussion about"
        ]
        
        name_lower = name.lower()
        
        # Check generic responses
        for generic in generic_responses:
            if generic in name_lower:
                logger.debug(f"[ID:0165] Name contains generic term '{generic}': '{name}'")
                return None
        
        # Use AI to evaluate name quality instead of hardcoded patterns
        if not self._ai_evaluate_name_quality(name):
            logger.debug(f"[ID:0164] AI determined name '{name}' is not suitable")
            return None
        
        logger.debug(f"[ID:0163] Final cleaned name: '{name}'")
        return name
    
    def _has_enough_substance(self, user_messages: List[str]) -> bool:
        """
        Check if the conversation has enough substance for meaningful naming
        Uses AI to evaluate conversation quality instead of hardcoded patterns
        
        Args:
            user_messages: List of user messages
            
        Returns:
            True if conversation has enough substance, False otherwise
        """
        if len(user_messages) < 3:
            return False
        
        # Use AI to evaluate conversation quality
        return self._ai_evaluate_conversation_quality(user_messages)
    
    def _ai_evaluate_conversation_quality(self, user_messages: List[str]) -> bool:
        """
        Use AI to evaluate if a conversation has enough substance for naming
        
        Args:
            user_messages: List of user messages
            
        Returns:
            True if conversation has enough substance, False otherwise
        """
        try:
            # Take a sample of messages for evaluation
            sample_messages = user_messages[:5]  # Limit to first 5 messages
            messages_text = "\n".join([f"- {msg}" for msg in sample_messages])
            
            prompt = f"""Evaluate if this conversation has enough substance to warrant a meaningful name.

Consider:
- Does it have a clear topic or theme?
- Are the messages coherent and related?
- Is there enough depth to generate a descriptive name?
- Are the messages mostly greetings, random thoughts, or actual discussion?

User messages:
{messages_text}

Respond with only "YES" if the conversation has enough substance for naming, or "NO" if it lacks substance (e.g., mostly greetings, random thoughts, or no clear topic)."""

            # Use auto mode to select the smallest available model for evaluation
            if self.summarization_model == "Auto":
                from pyside_chat.utils.complexity_analyzer import RequestComplexityAnalyzer
                analyzer = RequestComplexityAnalyzer()
                
                # Get available models
                available_models = self.ollama_service.get_models()
                if not available_models:
                    logger.warning("[ID:0162] No models available for quality evaluation")
                    return False
                
                # Analyze complexity (evaluation is a simple task)
                complexity_metrics = analyzer.analyze_complexity(prompt)
                chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
                
                logger.debug(f"[ID:0161] Auto-selected model for quality evaluation: {chosen_model}")
            else:
                chosen_model = self.summarization_model
            
            # Send evaluation request
            messages = [{"role": "user", "content": prompt}]
            response = ""
            
            for chunk in self.ollama_service.send_chat_message(
                model=chosen_model,
                messages=messages,
                temperature=0.1,  # Very low temperature for consistent evaluation
                stream=True
            ):
                response += chunk
            
            # Clean and evaluate response
            response = response.strip().upper()
            logger.debug(f"[ID:0160] Quality evaluation response: '{response}'")
            
            # Check for positive evaluation
            if "YES" in response:
                logger.debug("[ID:0159] AI determined conversation has sufficient substance")
                return True
            else:
                logger.debug("[ID:0158] AI determined conversation lacks sufficient substance")
                return False
                
        except Exception as e:
            logger.error(f"[ID:0157] Error evaluating conversation quality: {str(e)}")
            # Fallback to basic checks if AI evaluation fails
            return self._fallback_quality_check(user_messages)
    
    def _fallback_quality_check(self, user_messages: List[str]) -> bool:
        """
        Fallback quality check if AI evaluation fails
        
        Args:
            user_messages: List of user messages
            
        Returns:
            True if conversation has enough substance, False otherwise
        """
        # Simple fallback: check for minimum length and non-greeting messages
        substantial_messages = 0
        
        for message in user_messages:
            message_lower = message.lower().strip()
            
            # Skip very short messages
            if len(message_lower) < 10:
                continue
            
            # Skip obvious greetings
            if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey', 'how are you', 'thanks', 'bye']):
                continue
            
            substantial_messages += 1
        
        logger.debug(f"[ID:0156] Fallback check: {substantial_messages} substantial messages out of {len(user_messages)} total")
        return substantial_messages >= 2
    
    def _ai_evaluate_name_quality(self, name: str) -> bool:
        """
        Use AI to evaluate if a generated name is suitable
        
        Args:
            name: The generated name to evaluate
            
        Returns:
            True if name is suitable, False otherwise
        """
        try:
            prompt = f"""Evaluate if this conversation name is suitable and meaningful.

Consider:
- Is it descriptive and specific?
- Does it avoid generic terms like "conversation", "chat", "discussion"?
- Is it professional and clear?
- Does it avoid random or nonsensical combinations?
- Is it appropriate for a conversation file name?

Name: "{name}"

Respond with only "YES" if the name is suitable, or "NO" if it's not suitable (e.g., too generic, random, or inappropriate)."""

            # Use auto mode to select the smallest available model for evaluation
            if self.summarization_model == "Auto":
                from pyside_chat.utils.complexity_analyzer import RequestComplexityAnalyzer
                analyzer = RequestComplexityAnalyzer()
                
                # Get available models
                available_models = self.ollama_service.get_models()
                if not available_models:
                    logger.warning("[ID:0155] No models available for name quality evaluation")
                    return False
                
                # Analyze complexity (evaluation is a simple task)
                complexity_metrics = analyzer.analyze_complexity(prompt)
                chosen_model = analyzer.get_model_recommendation(complexity_metrics, available_models)
                
                logger.debug(f"[ID:0154] Auto-selected model for name quality evaluation: {chosen_model}")
            else:
                chosen_model = self.summarization_model
            
            # Send evaluation request
            messages = [{"role": "user", "content": prompt}]
            response = ""
            
            for chunk in self.ollama_service.send_chat_message(
                model=chosen_model,
                messages=messages,
                temperature=0.1,  # Very low temperature for consistent evaluation
                stream=True
            ):
                response += chunk
            
            # Clean and evaluate response
            response = response.strip().upper()
            logger.debug(f"[ID:0153] Name quality evaluation response: '{response}'")
            
            # Check for positive evaluation
            if "YES" in response:
                logger.debug("[ID:0152] AI determined name is suitable")
                return True
            else:
                logger.debug("[ID:0151] AI determined name is not suitable")
                return False
                
        except Exception as e:
            logger.error(f"[ID:0150] Error evaluating name quality: {str(e)}")
            # Fallback: accept the name if AI evaluation fails
            return True
    
    def set_summarization_model(self, model: str) -> None:
        """Set the model to use for summarization"""
        self.summarization_model = model
    
    def set_min_messages_threshold(self, threshold: int) -> None:
        """Set the minimum number of messages required for summarization"""
        self.min_messages_for_summarization = threshold 
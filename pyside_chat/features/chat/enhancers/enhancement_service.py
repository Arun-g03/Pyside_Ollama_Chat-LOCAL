"""
Enhancement Service - Extracted from ollama_chat.py
Handles response enhancement and follow-up detection.
"""

from typing import Optional


class EnhancementService:
    """Service for response enhancement and follow-up detection"""

    def __init__(self, ollama_service):
        self.ollama_service = ollama_service

    def should_enhance_response(self, response: str) -> bool:
        """Determine if a response should be enhanced (placeholder logic)"""
        # Example: Enhance if response is short or ends with a question
        if not response:
            return False
        if len(response.split()) < 10:
            return True
        if response.strip().endswith('?'):
            return True
        return False

    def detect_follow_up_question(self, response: str) -> Optional[str]:
        """Detect a follow-up question in the response (placeholder logic)"""
        # Example: Return the last sentence if it ends with a question mark
        sentences = response.split('.')
        for sentence in reversed(sentences):
            if '?' in sentence:
                return sentence.strip()
        return None

    def generate_enhanced_response(self, original_response: str, context: str = "") -> str:
        """Generate an enhanced response (placeholder logic)"""
        # Example: Add a follow-up suggestion
        if not original_response:
            return ""
        enhanced = original_response
        follow_up = self.detect_follow_up_question(original_response)
        if follow_up:
            enhanced += f"\n\nWould you like to know more about this?"
        return enhanced

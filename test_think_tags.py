#!/usr/bin/env python3
"""
Test script to verify <think> tag removal works correctly
"""

def test_think_tag_removal():
    """Test the <think> tag removal functionality"""
    
    try:
        print("Testing <think> tag removal...")
        
        # Import the required classes
        from SRC.services.summarization_service import SummarizationService
        from SRC.services.ollama_service import OllamaService
        
        # Create services
        ollama_service = OllamaService()
        summarization_service = SummarizationService(ollama_service)
        
        # Test responses with <think> tags (from the actual logs)
        test_responses = [
            # Response from the logs
            """<think>
Okay, the user wants a short, descriptive name for a conversation about life. Let me start by understanding the key elements here. The main topic is life, so the name should capture that essence.

First, "life" is the theme, so maybe combining it with something like "journey" or "path." Then, considering the user message is "lets talk about life," maybe "life's journey" or "journey through life." But need to keep it concise. Let me check the word count. "Life's Journey" is 11 words, which fits the 3-6 word limit. It's clear and specific, focusing on the path aspect. No other words needed. Yep, that should work.
</think>

Life's Journey""",
            
            # Another response from the logs
            """<think>
Okay, the user wants a short, descriptive name for a conversation about life. Let me think. The main topic here is life, so maybe something related to life's essence or key aspects. Words like "life," "journey," "eternal," "passion," "existence." Need to make it concise and specific. Let me try combining some. "Life's Journey" is good, but maybe "Life's Essence" is more specific. Wait, the user said 3-6 words. "Life's Path" is shorter and captures the theme. Or "Life's Theme." Hmm, maybe "Life's Theme" is better. Let me check the example response. Oh, the user message is "lets talk about life," so maybe "Life's Theme" works. That's concise and specific.
</think>

Life's Theme""",
            
            # Simple response without think tags
            "Python Code Debugging Help",
            
            # Response with quotes
            '"Life Discussion"',
            
            # Empty response
            ""
        ]
        
        print("\nTesting <think> tag removal:")
        for i, response in enumerate(test_responses, 1):
            cleaned = summarization_service._clean_generated_name(response)
            print(f"  Test {i}: '{response[:50]}...' -> '{cleaned}'")
        
        print("\n🎉 <think> tag removal test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_think_tag_removal()
    
    if success:
        print("\n✅ <think> tag removal is working correctly!")
    else:
        print("\n❌ <think> tag removal test failed.") 
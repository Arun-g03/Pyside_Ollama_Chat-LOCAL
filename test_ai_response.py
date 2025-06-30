#!/usr/bin/env python3
"""
Test script to simulate the exact conversation and debug AI response issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SRC.Personalities.personality_model_refactored import PersonalityModel

def test_ai_response():
    """Test the exact conversation scenario that's failing"""
    print("Testing AI Response to 'whats my name?'")
    print("=" * 50)
    
    # Initialize personality model
    personality_model = PersonalityModel()
    
    # Set to Aunt personality
    personality_model.set_current_personality("Family members.aunt")
    
    # Get AI name
    ai_name = personality_model.get_ai_name()
    print(f"AI Name: {ai_name}")
    
    # Get system prompt
    system_prompt = personality_model.build_comprehensive_system_prompt()
    print(f"\nSystem Prompt Length: {len(system_prompt)}")
    print(f"System Prompt Preview:")
    print(system_prompt[:500] + "...")
    
    # Mock memory service with user info
    class MockMemoryService:
        def get_user_info(self):
            return {"name": "Bob"}
    
    mock_memory = MockMemoryService()
    
    # Test user context messages for continuing conversation
    context_messages = personality_model.get_user_context_messages(mock_memory, is_new_conversation=False)
    
    if context_messages:
        context_content = context_messages[0]["content"]
        print(f"\nContext Message Length: {len(context_content)}")
        print(f"Context Message Preview:")
        print(context_content[:300] + "...")
        
        # Check for key instructions
        key_checks = [
            "Your name is Bob",
            "My name is Aunt",
            "When asked about your name, say 'My name is Aunt'",
            "When asked about the user's name, say 'Your name is Bob'"
        ]
        
        print("\nKey Instructions Check:")
        for check in key_checks:
            if check in context_content:
                print(f"✓ Found: {check}")
            else:
                print(f"✗ Missing: {check}")
    
    # Simulate the conversation context that might be confusing the AI
    print("\n" + "=" * 50)
    print("Simulating Problematic Conversation Context")
    print("=" * 50)
    
    # This is the kind of conversation history that might be confusing the AI
    problematic_context = [
        {"role": "user", "content": "whats my name?"},
        {"role": "assistant", "content": ""},  # Empty response
        {"role": "user", "content": "yes"},
        {"role": "assistant", "content": "Sure, let me check the conversation context first. You said 'whats my name' earlier. So I responded with 'Bob'. Is that correct?"},
        {"role": "user", "content": "whats my name?"},
        {"role": "assistant", "content": ""},  # Empty response
        {"role": "user", "content": "whats my name? im the user"},
        {"role": "assistant", "content": "Yes, I'm Bob. What can I do for you?"},  # Confusing response
    ]
    
    print("Problematic conversation history:")
    for i, msg in enumerate(problematic_context):
        print(f"{i+1}. {msg['role']}: {msg['content'][:50]}...")
    
    print("\nThe issue is that the AI is getting confused by:")
    print("1. Empty assistant responses")
    print("2. Confusing responses like 'Yes, I'm Bob' (AI saying it's Bob)")
    print("3. Mixed up identity in conversation history")
    
    print("\n" + "=" * 50)
    print("Recommended Fixes")
    print("=" * 50)
    print("1. Clear conversation history when switching personalities")
    print("2. Add more explicit identity instructions")
    print("3. Filter out confusing responses from context")
    print("4. Use a larger, more capable model")

if __name__ == "__main__":
    test_ai_response() 
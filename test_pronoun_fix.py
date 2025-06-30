#!/usr/bin/env python3
"""
Test script to verify pronoun fix and AI identity
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SRC.Personalities.personality_model_refactored import PersonalityModel

def test_ai_identity():
    """Test AI identity and pronoun handling"""
    print("Testing AI Identity and Pronoun Handling")
    print("=" * 50)
    
    # Initialize personality model
    personality_model = PersonalityModel()
    
    # Test with Aunt personality
    personality_model.set_current_personality("Family members.aunt")
    
    # Get AI name
    ai_name = personality_model.get_ai_name()
    print(f"AI Name: {ai_name}")
    
    # Get system prompt
    system_prompt = personality_model.build_comprehensive_system_prompt()
    print(f"\nSystem Prompt Length: {len(system_prompt)}")
    
    # Check for key identity instructions
    identity_checks = [
        "You are Aunt",
        "Use 'I' and 'my' when referring to yourself",
        "Use 'you' and 'your' when referring to the user",
        "Never confuse your identity with the user's identity"
    ]
    
    print("\nIdentity Instructions Check:")
    for check in identity_checks:
        if check in system_prompt:
            print(f"✓ Found: {check}")
        else:
            print(f"✗ Missing: {check}")
    
    # Test user context messages
    print("\n" + "=" * 50)
    print("Testing User Context Messages")
    print("=" * 50)
    
    # Mock memory service with user info
    class MockMemoryService:
        def get_user_info(self):
            return {"name": "Bob"}
    
    mock_memory = MockMemoryService()
    context_messages = personality_model.get_user_context_messages(mock_memory, is_new_conversation=True)
    
    if context_messages:
        context_content = context_messages[0]["content"]
        print(f"Context Message Length: {len(context_content)}")
        
        # Check for key instructions
        context_checks = [
            "Your name is Bob",
            "My name is Aunt",
            "Always be clear about who is who",
            "Introduce yourself as 'Aunt'"
        ]
        
        print("\nContext Instructions Check:")
        for check in context_checks:
            if check in context_content:
                print(f"✓ Found: {check}")
            else:
                print(f"✗ Missing: {check}")
        
        # Show first 300 characters of context
        print(f"\nFirst 300 characters of context:")
        print(context_content[:300] + "...")
    else:
        print("No context messages generated")

if __name__ == "__main__":
    test_ai_identity() 
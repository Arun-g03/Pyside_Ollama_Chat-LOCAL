#!/usr/bin/env python3
"""
Test script to verify simplified prompts work better
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SRC.Personalities.personality_model_refactored import PersonalityModel

def test_simplified_prompts():
    """Test that simplified prompts are clearer and less confusing"""
    print("Testing Simplified Prompts")
    print("=" * 40)
    
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
    
    # Check for simplified identity instructions
    identity_checks = [
        "You are Aunt",
        "Your name is Aunt",
        "Use 'I' and 'my' when referring to yourself",
        "Use 'you' and 'your' when referring to the user"
    ]
    
    print("\nSimplified Identity Instructions Check:")
    for check in identity_checks:
        if check in system_prompt:
            print(f"✓ Found: {check}")
        else:
            print(f"✗ Missing: {check}")
    
    # Check that we removed confusing instructions
    removed_checks = [
        "Never confuse your identity",
        "ROLE CLARIFICATION",
        "When the user says 'my name is X'",
        "Always maintain this distinction clearly"
    ]
    
    print("\nRemoved Confusing Instructions Check:")
    for check in removed_checks:
        if check in system_prompt:
            print(f"✗ Still present: {check}")
        else:
            print(f"✓ Removed: {check}")
    
    # Test user context messages
    print("\n" + "=" * 40)
    print("Testing Simplified User Context Messages")
    print("=" * 40)
    
    # Mock memory service with user info
    class MockMemoryService:
        def get_user_info(self):
            return {"name": "Bob"}
    
    mock_memory = MockMemoryService()
    context_messages = personality_model.get_user_context_messages(mock_memory, is_new_conversation=True)
    
    if context_messages:
        context_content = context_messages[0]["content"]
        print(f"Context Message Length: {len(context_content)}")
        
        # Check for simplified instructions
        context_checks = [
            "Your name is Bob",
            "My name is Aunt",
            "Introduce yourself as 'Aunt'"
        ]
        
        print("\nSimplified Context Instructions Check:")
        for check in context_checks:
            if check in context_content:
                print(f"✓ Found: {check}")
            else:
                print(f"✗ Missing: {check}")
        
        # Check that we removed redundant instructions
        removed_context_checks = [
            "Always be clear about who is who",
            "If the user says 'my name is X'",
            "Start your first response with a greeting like"
        ]
        
        print("\nRemoved Redundant Context Instructions Check:")
        for check in removed_context_checks:
            if check in context_content:
                print(f"✗ Still present: {check}")
            else:
                print(f"✓ Removed: {check}")
        
        # Show first 200 characters of context
        print(f"\nFirst 200 characters of simplified context:")
        print(context_content[:200] + "...")
    else:
        print("No context messages generated")

if __name__ == "__main__":
    test_simplified_prompts() 
#!/usr/bin/env python3
"""
Test script to verify AI name functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from SRC.Personalities.personality_model_refactored import PersonalityModel

def test_ai_names():
    """Test that different personalities have proper names"""
    print("Testing AI Name Functionality")
    print("=" * 40)
    
    # Initialize personality model
    personality_model = PersonalityModel()
    
    # Test getting AI name for different personalities
    test_personalities = [
        "Specialists.assistant",
        "Specialists.creative", 
        "Specialists.technical",
        "Professions.Code Ninja",
        "Professions.Space Explorer",
        "Historic people.William Shakespeare"
    ]
    
    for personality_name in test_personalities:
        try:
            # Set the personality
            success = personality_model.set_current_personality(personality_name)
            if success:
                ai_name = personality_model.get_ai_name()
                print(f"✓ {personality_name}: {ai_name}")
            else:
                print(f"✗ {personality_name}: Failed to set personality")
        except Exception as e:
            print(f"✗ {personality_name}: Error - {e}")
    
    print("\n" + "=" * 40)
    print("Testing system prompt with AI name")
    print("=" * 40)
    
    # Test system prompt for assistant personality
    personality_model.set_current_personality("Specialists.assistant")
    system_prompt = personality_model.build_comprehensive_system_prompt()
    
    # Check if AI name is in the system prompt
    ai_name = personality_model.get_ai_name()
    if ai_name in system_prompt:
        print(f"✓ AI name '{ai_name}' found in system prompt")
    else:
        print(f"✗ AI name '{ai_name}' not found in system prompt")
    
    # Show first few lines of system prompt
    print(f"\nFirst 200 characters of system prompt:")
    print(system_prompt[:200] + "...")

if __name__ == "__main__":
    test_ai_names() 
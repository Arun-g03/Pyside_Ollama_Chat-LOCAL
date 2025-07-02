#!/usr/bin/env python3
"""
Test script for AI-generated filename behavior
Tests the new filename generation using AI names + timestamps
"""

import sys
import os
from datetime import datetime

# Add the SRC directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'SRC'))

from models.conversation_metadata import ConversationManager

def test_filename_generation():
    """Test the filename generation functionality"""
    print("=== Testing AI-Generated Filename Creation ===")
    
    # Initialize conversation manager
    conversation_manager = ConversationManager()
    
    # Test AI-generated names
    test_names = [
        "Python Programming Help",
        "Machine Learning Discussion",
        "Web Development Tips",
        "Data Science Project",
        "Code Review Session",
        "Algorithm Optimization",
        "Database Design",
        "API Integration Help",
        "Frontend Development",
        "Backend Architecture"
    ]
    
    print("Testing filename generation for various AI-generated names:")
    print("-" * 60)
    
    for name in test_names:
        safe_filename = conversation_manager._create_safe_filename(name)
        print(f"'{name}' -> '{safe_filename}'")
    
    print("\n" + "-" * 60)
    print("Testing edge cases:")
    
    # Test edge cases
    edge_cases = [
        "Very Long Name That Exceeds The Maximum Length Limit And Should Be Truncated",
        "Name with special chars: < > : \" / \\ | ? *",
        "Name with   multiple    spaces",
        "Name_with_underscores",
        "",
        "A",
        "Name with numbers 123 and symbols @#$%"
    ]
    
    for name in edge_cases:
        safe_filename = conversation_manager._create_safe_filename(name)
        print(f"'{name}' -> '{safe_filename}'")

def test_auto_save_with_ai_name():
    """Test auto-save behavior with AI-generated names"""
    print("\n=== Testing Auto-Save with AI Names ===")
    
    # Initialize conversation manager
    conversation_manager = ConversationManager()
    
    # Simulate a conversation with AI-generated name
    sample_conversation = [
        {"role": "user", "content": "Can you help me with Python programming?"},
        {"role": "assistant", "content": "Of course! I'd be happy to help with Python programming."},
        {"role": "user", "content": "I need to learn about classes and objects."},
        {"role": "assistant", "content": "Great! Classes and objects are fundamental concepts in Python."},
        {"role": "user", "content": "How do I create a class?"},
        {"role": "assistant", "content": "To create a class in Python, you use the 'class' keyword."}
    ]
    
    # Set AI-generated name in metadata
    conversation_manager.metadata.update_ai_generated_name("Python Programming Help")
    
    print(f"AI-generated name: {conversation_manager.metadata.ai_generated_name}")
    print(f"Current conversation file: {conversation_manager.metadata.current_conversation_file}")
    
    # Test auto-save (this would normally be called by the system)
    # For testing, we'll just show what the filename would be
    if conversation_manager.metadata.ai_generated_name:
        safe_filename = conversation_manager._create_safe_filename(conversation_manager.metadata.ai_generated_name)
        expected_filepath = os.path.join(conversation_manager.history_dir, safe_filename)
        print(f"Expected filepath: {expected_filepath}")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        expected_filepath = os.path.join(conversation_manager.history_dir, f"conversation_{timestamp}.json")
        print(f"Expected filepath (no AI name): {expected_filepath}")

def test_file_renaming():
    """Test the file renaming functionality"""
    print("\n=== Testing File Renaming ===")
    
    # Initialize conversation manager
    conversation_manager = ConversationManager()
    
    # Simulate an existing conversation file
    old_filepath = os.path.join(conversation_manager.history_dir, "conversation_20241201_120000.json")
    
    print(f"Old filepath: {old_filepath}")
    
    # Test renaming with AI-generated name
    new_ai_name = "Machine Learning Discussion"
    print(f"New AI name: {new_ai_name}")
    
    # Show what the new filename would be
    safe_filename = conversation_manager._create_safe_filename(new_ai_name)
    new_filepath = os.path.join(conversation_manager.history_dir, safe_filename)
    print(f"New filepath: {new_filepath}")
    
    # Show the difference
    old_filename = os.path.basename(old_filepath)
    new_filename = os.path.basename(new_filepath)
    print(f"Filename change: '{old_filename}' -> '{new_filename}'")

if __name__ == "__main__":
    print("Testing AI-Generated Filename System")
    print("=" * 60)
    
    test_filename_generation()
    test_auto_save_with_ai_name()
    test_file_renaming()
    
    print("\n" + "=" * 60)
    print("Summary of improvements:")
    print("1. AI-generated names are now used in filenames")
    print("2. Timestamps are added to ensure uniqueness")
    print("3. Special characters are safely handled")
    print("4. Filenames are limited to reasonable lengths")
    print("5. Files are automatically renamed when AI names are generated")
    print("6. Both new files and existing files benefit from AI naming") 
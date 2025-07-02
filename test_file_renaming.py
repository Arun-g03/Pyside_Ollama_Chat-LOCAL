#!/usr/bin/env python3
"""
Test script to verify the file renaming functionality works correctly
"""

import os
import json
import tempfile
import shutil
from datetime import datetime

def test_file_renaming():
    """Test the file renaming functionality"""
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()
    print(f"Created test directory: {test_dir}")
    
    try:
        # Import the required classes
        from SRC.models.conversation_metadata import ConversationManager, ConversationMetadata
        from SRC.services.summarization_service import SummarizationService
        from SRC.services.ollama_service import OllamaService
        
        # Create a conversation manager with the test directory
        conversation_manager = ConversationManager(test_dir)
        
        # Create a sample conversation
        sample_conversation = [
            {"role": "user", "content": "How do I debug Python code?"},
            {"role": "assistant", "content": "You can use print statements or a debugger like pdb."},
            {"role": "user", "content": "Can you show me an example?"},
            {"role": "assistant", "content": "Here's a simple example with pdb..."}
        ]
        
        # Save the conversation
        filepath = conversation_manager.save_conversation(sample_conversation)
        print(f"Saved conversation to: {filepath}")
        
        # Verify the file exists
        if os.path.exists(filepath):
            print(f"✓ File exists: {os.path.basename(filepath)}")
        else:
            print(f"❌ File does not exist: {filepath}")
            return False
        
        # Test the filename creation function
        test_names = [
            "Python Code Debugging Help",
            "Recipe for Chocolate Cake",
            "Travel Planning to Japan",
            "Math Homework Assistance",
            "Book Recommendations",
            "Invalid/Characters?*<>",
            "Very Long Name That Should Be Truncated To Avoid Filesystem Issues And Ensure Proper Handling Of Long Filenames In Various Operating Systems",
            ""
        ]
        
        print("\nTesting filename creation:")
        for name in test_names:
            safe_filename = conversation_manager._create_safe_filename(name)
            print(f"  '{name}' -> '{safe_filename}'")
        
        # Test updating conversation name (this should rename the file)
        ai_generated_name = "Python Code Debugging Help"
        print(f"\nTesting conversation name update with: '{ai_generated_name}'")
        
        success = conversation_manager.update_conversation_name(filepath, ai_generated_name)
        
        if success:
            print("✓ Conversation name updated successfully")
            
            # Check if the file was renamed
            new_filepath = conversation_manager.get_current_metadata().current_conversation_file
            print(f"New filepath: {new_filepath}")
            
            if os.path.exists(new_filepath):
                print(f"✓ New file exists: {os.path.basename(new_filepath)}")
                
                # Verify the old file is gone
                if not os.path.exists(filepath):
                    print(f"✓ Old file removed: {os.path.basename(filepath)}")
                else:
                    print(f"⚠️  Old file still exists: {os.path.basename(filepath)}")
                
                # Load and verify the content
                conversation, metadata = conversation_manager.load_conversation(new_filepath)
                print(f"✓ Loaded conversation with {len(conversation)} messages")
                print(f"✓ AI generated name: {metadata.ai_generated_name}")
                
                return True
            else:
                print(f"❌ New file does not exist: {new_filepath}")
                return False
        else:
            print("❌ Failed to update conversation name")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    finally:
        # Clean up
        try:
            shutil.rmtree(test_dir)
            print(f"\nCleaned up test directory: {test_dir}")
        except Exception as e:
            print(f"Warning: Failed to clean up test directory: {e}")

if __name__ == "__main__":
    print("Testing file renaming functionality...")
    success = test_file_renaming()
    
    if success:
        print("\n🎉 All tests passed! File renaming is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the implementation.") 
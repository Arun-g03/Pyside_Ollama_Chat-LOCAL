#!/usr/bin/env python3
"""
Test script to verify chat fixes work properly
"""

import sys
import os
import time
import traceback

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_streaming_handler_fixes():
    """Test the streaming handler fixes"""
    print("Testing streaming handler fixes...")
    
    try:
        from PySide6.QtWidgets import QApplication, QTextEdit
        from pyside_chat.core.utils.streaming_handler import StreamingHandler
        
        # Create a minimal QApplication if one doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create a test chat display
        chat_display = QTextEdit()
        streaming_handler = StreamingHandler(chat_display, "Test AI")
        
        # Test 1: Start streaming message
        print("Test 1: Starting streaming message...")
        streaming_handler.start_streaming_message("Test AI", "ai")
        
        # Test 2: Update with thought content
        print("Test 2: Updating with thought content...")
        test_content = "<think>This is a test thought</think>\nHello, this is a test response!"
        streaming_handler.update_streaming_message(test_content, "Test AI", tag="ai")
        
        # Test 3: Force UI update
        print("Test 3: Testing force UI update...")
        streaming_handler.force_ui_update()
        
        print("✅ All streaming handler tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Streaming handler test failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_chat_tab_fixes():
    """Test the chat tab fixes"""
    print("Testing chat tab fixes...")
    
    try:
        from PySide6.QtWidgets import QApplication
        from pyside_chat.ui.tabs.chat_tab.chat_tab import ChatTab
        
        # Create a minimal QApplication if one doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create a test chat tab
        chat_tab = ChatTab()
        
        # Test 1: Append response chunk safely
        print("Test 1: Testing append response chunk...")
        chat_tab._append_response_chunk_safe("Test chunk", "test-model")
        
        # Test 2: Start streaming
        print("Test 2: Testing start streaming...")
        chat_tab.start_streaming()
        
        # Test 3: Stop streaming
        print("Test 3: Testing stop streaming...")
        chat_tab.stop_streaming()
        
        print("✅ All chat tab tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Chat tab test failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Run all tests"""
    print("Running chat fixes tests...")
    print("=" * 50)
    
    success = True
    
    # Test streaming handler fixes
    if not test_streaming_handler_fixes():
        success = False
    
    print()
    
    # Test chat tab fixes
    if not test_chat_tab_fixes():
        success = False
    
    print()
    print("=" * 50)
    
    if success:
        print("✅ All tests passed! The fixes should work properly.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
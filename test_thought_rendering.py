#!/usr/bin/env python3
"""
Test script to verify thought rendering functionality
"""

from pyside_chat.ui.tabs.chat_tab.chat_renderer import ChatRenderer
from pyside_chat.ui.themes.chat_styles import ChatStyles
from PySide6.QtWidgets import QApplication, QTextEdit
import sys

def test_thought_rendering():
    """Test thought rendering functionality"""
    
    # Create a simple QApplication
    app = QApplication(sys.argv)
    
    # Create a text edit widget
    text_edit = QTextEdit()
    
    # Create the renderer
    renderer = ChatRenderer(text_edit)
    
    # Test conversation with thoughts
    test_conversation = [
        {
            "role": "user",
            "content": "What is 2+2?",
            "message_idx": 0
        },
        {
            "role": "assistant", 
            "content": "The answer is 4.",
            "thought": "The user is asking a simple arithmetic question. I should provide a direct and clear answer.",
            "message_idx": 1
        },
        {
            "role": "system",
            "content": "Using model qwen3:0.6b (auto-selected based on request complexity)",
            "message_idx": 2
        }
    ]
    
    # Render the conversation
    renderer.render_conversation(test_conversation)
    
    # Get the HTML content
    html_content = text_edit.toHtml()
    
    print("=== Thought Rendering Test ===")
    print("HTML Content:")
    print(html_content)
    
    # Check if thought bubble is present
    if "Assistant's Thoughts" in html_content:
        print("✅ Thought bubble found!")
    else:
        print("❌ Thought bubble not found!")
    
    # Check if main assistant message is present
    if "Assistant: The answer is 4." in html_content:
        print("✅ Main assistant message found!")
    else:
        print("❌ Main assistant message not found!")
    
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_thought_rendering() 
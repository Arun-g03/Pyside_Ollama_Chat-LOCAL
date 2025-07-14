#!/usr/bin/env python3
"""
Test script to verify the typewriter effect fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton
from PySide6.QtCore import QTimer
import time

from pyside_chat.ui.tabs.chat_tab.chat_renderer import ChatRenderer

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typewriter Effect Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create text edit for chat display
        self.chat_display = QTextEdit()
        layout.addWidget(self.chat_display)
        
        # Create test button
        test_button = QPushButton("Test Typewriter Effect")
        test_button.clicked.connect(self.test_typewriter)
        layout.addWidget(test_button)
        
        # Create chat renderer
        self.chat_renderer = ChatRenderer(self.chat_display, "Assistant")
        
        # Connect render completed signal
        self.chat_renderer.render_completed.connect(self.on_render_completed)
        
    def test_typewriter(self):
        """Test the typewriter effect with simulated chunks"""
        print("Starting typewriter effect test...")
        
        # Start streaming message
        self.chat_renderer.start_streaming_message("Assistant", "ai")
        
        # Simulate chunks arriving
        test_chunks = [
            "Hello! ",
            "I'm ",
            "testing ",
            "the ",
            "typewriter ",
            "effect. ",
            "Each ",
            "word ",
            "should ",
            "appear ",
            "one ",
            "at ",
            "a ",
            "time.",
            
        ]
        
        # Send chunks with small delays
        for i, chunk in enumerate(test_chunks):
            QTimer.singleShot(i * 100, lambda c=chunk: self.send_chunk(c))
            
        # Finalize after all chunks
        QTimer.singleShot(len(test_chunks) * 100 + 500, self.finalize_message)
        
    def send_chunk(self, chunk):
        """Send a chunk to the renderer"""
        print(f"Sending chunk: '{chunk}'")
        self.chat_renderer.update_streaming_message(chunk, "Assistant", None, False, "ai", True)
        
    def finalize_message(self):
        """Finalize the streaming message"""
        print("Finalizing message...")
        self.chat_renderer.finalize_streaming_message()
        
    def on_render_completed(self):
        """Handle render completion"""
        print("Render completed")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test script for Coqui TTS streaming synthesis
"""

import sys
import os
import time

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service import CoquiTTSService
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


def test_streaming_tts():
    """Test the streaming TTS functionality"""
    print("Testing Coqui TTS streaming synthesis...")
    
    # Create the TTS service
    tts_service = CoquiTTSService()
    
    if not tts_service.is_available():
        print("❌ Coqui TTS service is not available")
        return False
    
    print("✅ Coqui TTS service is available")
    
    # Test text
    test_text = "Hello! This is a test of streaming text-to-speech synthesis. The audio should start playing immediately as the text is being processed, rather than waiting for the entire audio to be generated first."
    
    print(f"Testing with text: {test_text[:50]}...")
    
    # Test streaming synthesis
    print("\n🎵 Testing streaming synthesis...")
    tts_service.speak_text(test_text, use_streaming=True)
    
    # Wait for completion
    time.sleep(10)
    
    # Test non-streaming synthesis
    print("\n🎵 Testing non-streaming synthesis...")
    tts_service.speak_text(test_text, use_streaming=False)
    
    # Wait for completion
    time.sleep(10)
    
    print("\n✅ Streaming TTS test completed!")
    return True


def main():
    """Main test function"""
    app = QApplication(sys.argv)
    
    try:
        success = test_streaming_tts()
        if success:
            print("\n🎉 All tests passed!")
        else:
            print("\n❌ Some tests failed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up
    app.quit()


if __name__ == "__main__":
    main() 
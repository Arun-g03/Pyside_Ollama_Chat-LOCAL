#!/usr/bin/env python3
"""
Test script to verify voice service initialization
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.features.voice.voice_service import VoiceService

logger = CustomLogger.get_logger(__name__)

def test_voice_service_initialization():
    """Test that voice service properly initializes STT and TTS services"""
    print("Testing voice service initialization...")
    
    try:
        # Create voice service (should auto-initialize services)
        voice_service = VoiceService()
        
        # Check if services are available
        print(f"STT Service: {voice_service.stt_service is not None}")
        print(f"TTS Service: {voice_service.tts_service is not None}")
        print(f"Recording Service: {voice_service.recording_service is not None}")
        print(f"Voice Available: {voice_service.is_voice_available()}")
        
        if voice_service.is_voice_available():
            print("✅ Voice service initialization successful!")
            return True
        else:
            print("❌ Voice service initialization failed - services not available")
            return False
            
    except Exception as e:
        print(f"❌ Voice service initialization failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_voice_service_initialization()
    sys.exit(0 if success else 1) 
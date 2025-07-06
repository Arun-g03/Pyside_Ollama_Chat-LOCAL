#!/usr/bin/env python3
"""
Test script for Coqui TTS multi-speaker models
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


def test_multispeaker_tts():
    """Test multi-speaker TTS functionality"""
    print("Testing Coqui TTS multi-speaker models...")
    
    # Create the TTS service
    tts_service = CoquiTTSService()
    
    if not tts_service.is_available():
        print("❌ Coqui TTS service is not available")
        return False
    
    print("✅ Coqui TTS service is available")
    
    # Test multi-speaker model
    model_name = "tts_models/en/vctk/vits"
    
    print(f"\n🔄 Loading multi-speaker model: {model_name}")
    success = tts_service.load_model(model_name)
    
    if not success:
        print(f"❌ Failed to load model: {model_name}")
        return False
    
    print(f"✅ Model loaded successfully")
    print(f"📊 Available voices: {tts_service.available_voices}")
    print(f"🎤 Current voice: {tts_service.current_voice}")
    print(f"🔊 Is multi-speaker: {tts_service.is_multi_speaker()}")
    
    # Test text
    test_text = "Hello! This is a test of multi-speaker text-to-speech synthesis."
    
    print(f"\n🎵 Testing with current voice: {tts_service.current_voice}")
    tts_service.speak_text(test_text, use_streaming=False)
    
    # Wait for completion
    time.sleep(5)
    
    # Test different voices if available
    if len(tts_service.available_voices) > 1:
        for i, voice in enumerate(tts_service.available_voices[:3]):  # Test first 3 voices
            print(f"\n🎵 Testing voice {i+1}: {voice}")
            tts_service.set_voice(voice)
            tts_service.speak_text(f"Hello! This is voice {voice} speaking.", use_streaming=False)
            time.sleep(3)
    
    print("\n✅ Multi-speaker TTS test completed!")
    return True


def test_single_speaker_tts():
    """Test single-speaker TTS functionality for comparison"""
    print("\n" + "="*50)
    print("Testing single-speaker model for comparison...")
    
    # Create a new TTS service instance
    tts_service = CoquiTTSService()
    
    # Test single-speaker model
    model_name = "tts_models/en/ljspeech/glow-tts"
    
    print(f"\n🔄 Loading single-speaker model: {model_name}")
    success = tts_service.load_model(model_name)
    
    if not success:
        print(f"❌ Failed to load model: {model_name}")
        return False
    
    print(f"✅ Model loaded successfully")
    print(f"📊 Available voices: {tts_service.available_voices}")
    print(f"🎤 Current voice: {tts_service.current_voice}")
    print(f"🔊 Is multi-speaker: {tts_service.is_multi_speaker()}")
    
    # Test text
    test_text = "Hello! This is a test of single-speaker text-to-speech synthesis."
    
    print(f"\n🎵 Testing single-speaker model")
    tts_service.speak_text(test_text, use_streaming=False)
    
    # Wait for completion
    time.sleep(5)
    
    print("\n✅ Single-speaker TTS test completed!")
    return True


def main():
    """Main test function"""
    app = QApplication(sys.argv)
    
    try:
        # Test multi-speaker model
        success1 = test_multispeaker_tts()
        
        # Test single-speaker model for comparison
        success2 = test_single_speaker_tts()
        
        if success1 and success2:
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
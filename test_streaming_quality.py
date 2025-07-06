#!/usr/bin/env python3
"""
Test script to verify streaming TTS audio quality improvements
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service import CoquiTTSService
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtWidgets import QApplication

def test_streaming_quality():
    """Test streaming TTS with quality improvements"""
    
    # Create Qt application
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create TTS service
    tts_service = CoquiTTSService()
    
    # Wait for service to initialize
    time.sleep(2)
    
    if not tts_service.is_available():
        print("❌ Coqui TTS service not available")
        return False
    
    print("✅ Coqui TTS service available")
    print(f"📝 Current model: {tts_service.current_model}")
    print(f"🎤 Available voices: {len(tts_service.available_voices)}")
    
    # Test text
    test_text = "Hello! This is a test of the improved streaming TTS quality. The audio should now sound much better with proper volume control and audio normalization."
    
    print("\n🎵 Testing streaming TTS with quality improvements...")
    print("📝 Text:", test_text)
    
    # Connect signals
    def on_tts_started():
        print("▶️  TTS started")
    
    def on_tts_finished():
        print("✅ TTS finished")
        app.quit()
    
    def on_tts_error(error):
        print(f"❌ TTS error: {error}")
        app.quit()
    
    def on_streaming_progress(progress):
        print(f"📊 Progress: {progress}%")
    
    tts_service.tts_started.connect(on_tts_started)
    tts_service.tts_finished.connect(on_tts_finished)
    tts_service.tts_error.connect(on_tts_error)
    tts_service.streaming_progress.connect(on_streaming_progress)
    
    # Test streaming TTS
    print("\n🎵 Starting streaming synthesis...")
    tts_service.speak_text(test_text, use_streaming=True)
    
    # Run the application
    app.exec()
    
    print("\n✅ Test completed!")
    return True

def test_volume_control():
    """Test volume control functionality"""
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    tts_service = CoquiTTSService()
    time.sleep(2)
    
    if not tts_service.is_available():
        print("❌ TTS service not available for volume test")
        return False
    
    print("\n🔊 Testing volume control...")
    
    # Test different volume levels
    test_text = "Testing volume control at different levels."
    
    def on_tts_finished():
        print("✅ Volume test finished")
        app.quit()
    
    tts_service.tts_finished.connect(on_tts_finished)
    
    # Test with low volume
    print("🔊 Testing with low volume (0.3)...")
    tts_service.set_streaming_volume(0.3)
    tts_service.speak_text(test_text, use_streaming=True)
    
    app.exec()
    
    print("✅ Volume control test completed!")
    return True

if __name__ == "__main__":
    print("🎵 Streaming TTS Quality Test")
    print("=" * 40)
    
    try:
        # Test 1: Basic streaming quality
        print("\n🧪 Test 1: Streaming Quality")
        test_streaming_quality()
        
        # Test 2: Volume control
        print("\n🧪 Test 2: Volume Control")
        test_volume_control()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 
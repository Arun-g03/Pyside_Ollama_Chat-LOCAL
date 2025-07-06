#!/usr/bin/env python3
"""
Test script to compare streaming vs non-streaming TTS quality
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service import CoquiTTSService
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtWidgets import QApplication

def test_comparison():
    """Test streaming vs non-streaming TTS"""
    
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
    
    # Test text
    test_text = "Hello! This is a comparison test between streaming and non-streaming TTS. The streaming version should now have improved audio quality with proper volume control."
    
    print("\n🎵 TTS Quality Comparison Test")
    print("=" * 50)
    
    # Connect signals
    def on_tts_started():
        print("▶️  TTS started")
    
    def on_tts_finished():
        print("✅ TTS finished")
        # Schedule next test after a delay
        QTimer.singleShot(2000, run_next_test)
    
    def on_tts_error(error):
        print(f"❌ TTS error: {error}")
        app.quit()
    
    tts_service.tts_started.connect(on_tts_started)
    tts_service.tts_finished.connect(on_tts_finished)
    tts_service.tts_error.connect(on_tts_error)
    
    test_count = 0
    
    def run_next_test():
        nonlocal test_count
        test_count += 1
        
        if test_count == 1:
            print("\n🔊 Test 1: Non-Streaming TTS (Original method)")
            print("📝 This should sound like the original quality...")
            tts_service.speak_text(test_text, use_streaming=False)
            
        elif test_count == 2:
            print("\n🎵 Test 2: Streaming TTS (Improved quality)")
            print("📝 This should sound better with improved volume control...")
            tts_service.speak_text(test_text, use_streaming=True)
            
        else:
            print("\n🎉 Comparison test completed!")
            print("\n💡 Summary:")
            print("   - Non-streaming: Original audio quality")
            print("   - Streaming: Improved quality with volume control and normalization")
            app.quit()
    
    # Start the first test
    run_next_test()
    
    # Run the application
    app.exec()
    
    print("\n✅ Comparison test completed!")
    return True

if __name__ == "__main__":
    print("🎵 Streaming vs Non-Streaming TTS Comparison")
    print("=" * 55)
    
    try:
        test_comparison()
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 
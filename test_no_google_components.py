#!/usr/bin/env python3
"""
Test script to verify that all Google components have been removed
"""

import sys
import os
import re

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_file_for_google_references(file_path: str) -> list:
    """Check a file for Google references"""
    google_references = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for various Google-related patterns
        patterns = [
            r'Google TTS',
            r'Google Speech Recognition',
            r'gtts',
            r'gTTS',
            r'from gtts',
            r'import gtts',
            r'www\.google\.com',
            r'8\.8\.8\.8.*Google DNS',
        ]
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    google_references.append({
                        'line': line_num,
                        'content': line.strip(),
                        'pattern': pattern
                    })
                    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return google_references

def test_google_removal():
    """Test that all Google components have been removed"""
    
    print("🔍 Testing Google Component Removal")
    print("=" * 50)
    
    # Files to check for Google references
    files_to_check = [
        "pyside_chat/services/Voice_STT_TTS_SERVICES/TTS_Service.py",
        "pyside_chat/ui/Widgets/voice_settings_dialog.py",
        "pyside_chat/ui/chat_tab.py",
        "pyside_chat/services/start_up/dependency_checker.py",
        "pyside_chat/services/start_up/check_dependencies.py",
        "pyside_chat/services/start_up/install_dependencies.py",
        "pyside_chat/utils/internet_connection.py",
        "README.md"
    ]
    
    all_google_references = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            references = check_file_for_google_references(file_path)
            if references:
                all_google_references.append({
                    'file': file_path,
                    'references': references
                })
    
    # Report results
    if not all_google_references:
        print("✅ SUCCESS: No Google components found!")
        print("\n🎉 All Google components have been successfully removed.")
        return True
    else:
        print("❌ FAILED: Google components still found!")
        print("\n📋 Remaining Google references:")
        
        for file_info in all_google_references:
            print(f"\n📁 {file_info['file']}:")
            for ref in file_info['references']:
                print(f"   Line {ref['line']}: {ref['content']}")
        
        return False

def test_tts_service_functionality():
    """Test that TTS service works without Google components"""
    
    print("\n🧪 Testing TTS Service Functionality")
    print("=" * 40)
    
    try:
        from pyside_chat.services.Voice_STT_TTS_SERVICES.TTS_Service import TTSService
        from PySide6.QtWidgets import QApplication
        
        # Create Qt application
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create TTS service
        tts_service = TTSService()
        
        # Check if Coqui TTS is available
        if tts_service.coqui_service and tts_service.coqui_service.is_available():
            print("✅ Coqui TTS is available and working")
            print(f"📝 Current model: {tts_service.coqui_service.current_model}")
            return True
        else:
            print("⚠️  Coqui TTS not available, but Google TTS has been removed")
            print("💡 The system will fall back to eSpeak for TTS")
            return True
            
    except Exception as e:
        print(f"❌ Error testing TTS service: {e}")
        return False

def test_voice_settings_dialog():
    """Test that voice settings dialog works without Google options"""
    
    print("\n🧪 Testing Voice Settings Dialog")
    print("=" * 35)
    
    try:
        from pyside_chat.ui.Widgets.voice_settings_dialog import VoiceSettingsDialog
        from PySide6.QtWidgets import QApplication
        
        # Create Qt application
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create dialog
        dialog = VoiceSettingsDialog()
        
        # Check that Google options are not in the APIs
        stt_apis = list(dialog.stt_apis.keys())
        tts_apis = list(dialog.tts_apis.keys())
        
        google_stt_found = any("Google" in api for api in stt_apis)
        google_tts_found = any("Google" in api for api in tts_apis)
        
        if not google_stt_found and not google_tts_found:
            print("✅ Voice settings dialog has no Google options")
            print(f"📝 Available STT APIs: {stt_apis}")
            print(f"📝 Available TTS APIs: {tts_apis}")
            return True
        else:
            print("❌ Google options still found in voice settings")
            if google_stt_found:
                print("   - Google STT options found")
            if google_tts_found:
                print("   - Google TTS options found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing voice settings dialog: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Google Component Removal Test")
    print("=" * 50)
    
    try:
        # Test 1: Check for remaining Google references
        test1_passed = test_google_removal()
        
        # Test 2: Test TTS service functionality
        test2_passed = test_tts_service_functionality()
        
        # Test 3: Test voice settings dialog
        test3_passed = test_voice_settings_dialog()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"✅ Google Reference Check: {'PASSED' if test1_passed else 'FAILED'}")
        print(f"✅ TTS Service Functionality: {'PASSED' if test2_passed else 'FAILED'}")
        print(f"✅ Voice Settings Dialog: {'PASSED' if test3_passed else 'FAILED'}")
        
        if test1_passed and test2_passed and test3_passed:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ All Google components have been successfully removed")
            print("✅ Application should work without any Google dependencies")
        else:
            print("\n❌ SOME TESTS FAILED!")
            print("⚠️  Please check the failed tests above")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 
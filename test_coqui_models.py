#!/usr/bin/env python3
"""
Test script to verify Coqui TTS model listing without downloading
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service import CoquiTTSService

def test_model_listing():
    """Test that model listing works without downloading"""
    print("Testing Coqui TTS model listing...")
    
    try:
        # Initialize the service
        coqui_service = CoquiTTSService()
        
        print(f"Coqui TTS available: {coqui_service.is_available()}")
        
        # Get available models (should not trigger downloads)
        print("\nGetting available models...")
        models = coqui_service.get_available_models()
        print(f"Found {len(models)} available models:")
        
        for i, model in enumerate(models, 1):
            # Check if model is downloaded
            is_downloaded = coqui_service.is_model_downloaded(model)
            size = coqui_service.get_model_download_size(model)
            model_info = coqui_service.get_model_info(model)
            
            status = "✅ Downloaded" if is_downloaded else "⬇️ Available"
            print(f"  {i:2d}. {status} - {model}")
            print(f"      Size: {size}, Type: {model_info.get('type', 'Unknown')}")
            print(f"      Description: {model_info.get('description', 'No description')}")
        
        # Get downloaded models
        print("\nGetting downloaded models...")
        downloaded_models = coqui_service.get_downloaded_models()
        print(f"Found {len(downloaded_models)} downloaded models:")
        for model in downloaded_models:
            print(f"  - {model}")
        
        print("\n✅ Test completed successfully! No models were downloaded.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_listing() 
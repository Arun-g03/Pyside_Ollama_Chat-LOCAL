"""
Voice Module - Consolidated Architecture

Core Components:
- VoiceService: Main voice functionality (STT, TTS, Recording)
- Audio: Recording service
- TTS: Text-to-speech services (Coqui TTS)
- STT: Speech-to-text services (Vosk)

Simplified structure with all functionality consolidated into essential components.
"""

# Core voice service
from .voice_service import VoiceService

# Audio components
from .audio.recording_service import RecordingService

# TTS components
from .tts.coqui_tts_service import CoquiTTSService

# STT components
from .stt.stt_service import STTService

# Convenience functions
def get_voice_service():
    """Get the voice service instance"""
    return VoiceService.get_instance()

__all__ = [
    'VoiceService',
    'RecordingService',
    'CoquiTTSService',
    'STTService',
    'get_voice_service'
]

import os
import subprocess
import platform
from PySide6.QtCore import QObject, Signal, QTimer, Qt
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

# Import Coqui TTS service
try:
    from .coqui_tts_service import CoquiTTSService
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False

class TTSService(QObject):
    """Text-to-Speech service for converting text to speech
    
    Always use TTSService.get_instance() to access the singleton instance.
    Do NOT instantiate directly.
    """
    # Signals
    tts_started = Signal()
    tts_finished = Signal()
    tts_error = Signal(str)
    audio_level_changed = Signal(float)  # Audio level for EQ visualization

    # Singleton instance
    _instance = None
    
    @staticmethod
    def get_instance():
        """Get the singleton instance of TTSService"""
        if TTSService._instance is None:
            TTSService._instance = TTSService()
        return TTSService._instance

    def __init__(self):
        super().__init__()
        self.available = self._check_availability()
        self.media_player = None
        self.audio_output = None
        self.current_audio_file = None
        self.current_voice = "en"
        self.current_api = "Coqui TTS"
        self.speech_speed = 1.0  # Speed multiplier (1.0 = normal, 1.5 = faster, 0.5 = slower)
        
        # Initialize Coqui TTS service if available
        self.coqui_service = None
        if COQUI_AVAILABLE:
            try:
                # Always use the singleton accessor
                self.coqui_service = CoquiTTSService.get_instance()
                # Connect Coqui TTS signals with QueuedConnection for thread safety
                self.coqui_service.tts_started.connect(self.tts_started.emit, Qt.ConnectionType.QueuedConnection)
                self.coqui_service.tts_finished.connect(self.tts_finished.emit, Qt.ConnectionType.QueuedConnection)
                self.coqui_service.tts_error.connect(self.tts_error.emit, Qt.ConnectionType.QueuedConnection)
                self.coqui_service.audio_level_changed.connect(self.audio_level_changed.emit, Qt.ConnectionType.QueuedConnection)
            except Exception as e:
                logger.error(f"Failed to initialize Coqui TTS service: {e}")

    def _check_availability(self) -> bool:
        try:
            # TODO: Implement actual availability check based on chosen TTS provider
            # For now, assume it's available
            return True
        except Exception as e:
            logger.error(f"TTS service not available: {e}")
            return False

    def is_available(self) -> bool:
        return self.available
    
    def is_initialized(self) -> bool:
        """Check if TTS service is properly initialized"""
        return self.available and (self.coqui_service is not None or self.media_player is not None)

    def speak_text(self, text: str):
        try:
            logger.debug(f"Converting text to speech: {text[:50]}...")
            self.tts_started.emit()
            
            # Use Coqui TTS if available
            if self.coqui_service and self.coqui_service.is_available():
                # Use streaming by default for Coqui TTS
                self.coqui_service.speak_text(text, use_streaming=True)
            else:
                self._speak_with_espeak(text)
        except Exception as e:
            logger.error(f"TTS conversion failed: {e}")
            self.tts_error.emit(f"TTS conversion failed: {str(e)}")

    def speak_text_streaming(self, text: str):
        """Convert text to speech using streaming synthesis (Coqui TTS only)"""
        try:
            logger.debug(f"Converting text to speech with streaming: {text[:50]}...")
            self.tts_started.emit()
            
            # Use Coqui TTS with streaming if available
            if self.coqui_service and self.coqui_service.is_available():
                self.coqui_service.speak_text(text, use_streaming=True)
            else:
                # Fall back to non-streaming for other TTS providers
                self.speak_text(text)
        except Exception as e:
            logger.error(f"Streaming TTS conversion failed: {e}")
            self.tts_error.emit(f"Streaming TTS conversion failed: {str(e)}")
    
    def speak_text_non_streaming(self, text: str):
        """Convert text to speech using non-streaming synthesis"""
        try:
            logger.debug(f"Converting text to speech (non-streaming): {text[:50]}...")
            self.tts_started.emit()
            
            # Use Coqui TTS if available
            if self.coqui_service and self.coqui_service.is_available():
                self.coqui_service.speak_text(text, use_streaming=False)
            else:
                self._speak_with_espeak(text)
        except Exception as e:
            logger.error(f"TTS conversion failed: {e}")
            self.tts_error.emit(f"TTS conversion failed: {str(e)}")



    def _speak_with_espeak(self, text: str):
        try:
            if platform.system() == "Windows":
                cmd = ["espeak", text]
            else:
                cmd = ["espeak", text]
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Calculate estimated duration for eSpeak as well
            word_count = len(text.split())
            base_duration_per_word = 0.24  # Base duration per word
            estimated_duration = max(0.5, word_count * base_duration_per_word / self.speech_speed)
            
            # Use a timer to emit finished signal after estimated duration
            QTimer.singleShot(int(estimated_duration * 1000) + 500, self.tts_finished.emit)
            
            logger.debug(f"eSpeak TTS started with estimated duration: {estimated_duration:.1f}s for {word_count} words")
        except Exception as e:
            logger.error(f"eSpeak failed: {e}")
            self.tts_finished.emit()

    

    def _simulate_tts_finished(self):
        self.tts_finished.emit()

    def stop_playback(self):
        # Stop Coqui TTS if using it
        if self.coqui_service:
            self.coqui_service.stop_playback()
        else:
            if self.media_player:
                self.media_player.stop()
            self.tts_finished.emit()

    def update_api(self, api_name: str):
        logger.debug(f"TTS API updated to: {api_name}")
        self.current_api = api_name
        
        # Update Coqui TTS settings if available
        if self.coqui_service:
            self.coqui_service.set_speed(self.speech_speed)

    def update_voice(self, voice_name: str):
        logger.debug(f"TTS voice updated to: {voice_name}")
        self.current_voice = voice_name
        
        # Update Coqui TTS voice if available
        if self.coqui_service:
            self.coqui_service.set_voice(voice_name)

    def update_speed(self, speed: float):
        """Update speech speed (1.0 = normal, 1.5 = faster, 0.5 = slower)"""
        self.speech_speed = max(0.5, min(3.0, speed))  # Clamp between 0.5x and 3.0x speed
        logger.debug(f"TTS speed updated to: {self.speech_speed}x")
        
        # Update Coqui TTS speed if using Coqui
        if self.current_api == "Coqui TTS" and self.coqui_service:
            self.coqui_service.set_speed(self.speech_speed)
    
    def is_coqui_available(self) -> bool:
        """Check if Coqui TTS is available"""
        return COQUI_AVAILABLE and self.coqui_service and self.coqui_service.is_available()
    
    def get_coqui_models(self) -> list:
        """Get available Coqui TTS models"""
        if self.coqui_service:
            return self.coqui_service.get_available_models()
        return []
    
    def get_coqui_voices(self) -> list:
        """Get available Coqui TTS voices for current model"""
        if self.coqui_service:
            return self.coqui_service.get_available_voices()
        return []
    
    def get_coqui_model_info(self) -> dict:
        """Get information about the current Coqui TTS model"""
        if self.coqui_service:
            return self.coqui_service.get_current_model_info()
        return {}
    
    def load_coqui_model(self, model_name: str) -> bool:
        """Load a specific Coqui TTS model"""
        if self.coqui_service:
            return self.coqui_service.load_model(model_name)
        return False
    
    def set_coqui_model(self, model_name: str) -> bool:
        """Set the Coqui TTS model to use"""
        if self.coqui_service and self.current_api == "Coqui TTS":
            success = self.coqui_service.load_model(model_name)
            if success:
                logger.info(f"Set Coqui TTS model to: {model_name}")
            return success
        return False
    
    def cleanup(self):
        """Cleanup TTS service resources"""
        try:
            if self.coqui_service:
                self.coqui_service.cleanup()
            if self.media_player:
                self.media_player.stop()
                self.media_player = None
            if self.audio_output:
                self.audio_output = None
            logger.debug("TTS service cleanup completed")
        except Exception as e:
            logger.error(f"Error during TTS service cleanup: {e}")

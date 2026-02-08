"""
Consolidated Voice Service

This is the main voice service that handles all voice functionality:
- Speech-to-Text (STT) for voice input
- Text-to-Speech (TTS) for AI responses
- Voice recording and playback
- Threading integration for non-blocking operations
"""

from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.audio_imports import *
from pyside_chat.core.utils.threading_utils import log_thread_info

logger = CustomLogger.get_logger(__name__)


class VoiceService(QObject):
    """Consolidated voice service for handling all voice functionality"""
    
    # Signals
    voice_input_received = Signal(str)
    voice_input_error = Signal(str)
    tts_started = Signal()
    tts_finished = Signal()
    tts_error = Signal(str)
    recording_started = Signal()
    recording_stopped = Signal()
    recording_error = Signal(str)
    voice_processing_started = Signal()
    voice_processing_finished = Signal()
    audio_level_changed = Signal(float)
    eq_bars_changed = Signal(list)
    user_interrupted = Signal()
    request_cancelled = Signal()
    voice_status_changed = Signal(str)
    voice_service_ready = Signal()

    _instance = None

    @staticmethod
    def get_instance():
        """Get the singleton instance"""
        if VoiceService._instance is None:
            VoiceService._instance = VoiceService()
        return VoiceService._instance

    def __init__(self):
        super().__init__()

        # Services
        self.recording_service = None
        self.stt_service = None
        self.tts_service = None

        # State tracking
        self.is_recording = False
        self.is_processing_voice = False
        self.is_playing_tts = False
        self.continuous_voice_mode = False

        # Settings
        self.voice_settings = {
            "stt_api": "Vosk (Offline)",
            "tts_api": "Coqui TTS",
            "tts_voice": "default",
            "auto_speak": True,
            "voice_speed": 1.0,
            "recording_timeout": 10.0,
            "silence_duration": 2.0,
            "silence_threshold": 0.005,
            "coqui_model": "tts_models/en/vctk/vits",
            "coqui_speaker": "ED",
            "eq_visualizer": "None",
            "tts_streaming": True,
            "allow_interruptions": True,
            "interruption_threshold": 0.5
        }
        
        # Initialize services
        self._initialize_services()

        # Setup connections
        self._setup_connections()

        logger.info("VoiceService initialized successfully")

    def _initialize_services(self):
        """Initialize voice services"""
        try:
            # Initialize recording service
            logger.info("Initializing recording service...")
            print("[VOICE_INIT] Initializing recording service...")
            from .audio.recording_service import RecordingService
            self.recording_service = RecordingService()
            print(f"[VOICE_INIT] Recording service created: {self.recording_service}")
            print(f"[VOICE_INIT] Recording service available: {self.recording_service.is_available() if self.recording_service else 'None'}")
            
            # Initialize STT service
            logger.info("Initializing STT service...")
            print("[VOICE_INIT] Initializing STT service...")
            from .stt.stt_service import STTService
            self.stt_service = STTService()
            print(f"[VOICE_INIT] STT service created: {self.stt_service}")
            print(f"[VOICE_INIT] STT service available: {self.stt_service.is_available() if self.stt_service else 'None'}")
            
            # Initialize TTS service
            logger.info("Initializing TTS service...")
            print("[VOICE_INIT] Initializing TTS service...")
            from .tts.coqui_tts_service import CoquiTTSService
            self.tts_service = CoquiTTSService.get_instance()
            print(f"[VOICE_INIT] TTS service created: {self.tts_service}")
            print(f"[VOICE_INIT] TTS service available: {self.tts_service.is_available() if self.tts_service else 'None'}")
            
            logger.info("All voice services initialized successfully")
            print("[VOICE_INIT] All voice services initialized successfully")
            self.voice_service_ready.emit()
            
        except Exception as e:
            logger.error(f"Failed to initialize voice services: {e}")
            print(f"[VOICE_INIT] ❌ Failed to initialize voice services: {e}")
            self.voice_input_error.emit(f"Voice service initialization failed: {str(e)}")

    def _setup_connections(self):
        """Setup signal connections"""
        try:
            # Connect STT service signals
            if self.stt_service:
                self.stt_service.text_received.connect(self._on_stt_text_received)
                self.stt_service.error_occurred.connect(self._on_stt_error)

            # Connect TTS service signals
            if self.tts_service:
                self.tts_service.tts_started.connect(self._on_tts_started)
                self.tts_service.tts_finished.connect(self._on_tts_finished)
                self.tts_service.tts_error.connect(self._on_tts_error)
                self.tts_service.audio_level_changed.connect(self.audio_level_changed.emit)
                self.tts_service.eq_bars_changed.connect(self.eq_bars_changed.emit)

            # Connect recording service signals
            if self.recording_service:
                self.recording_service.recording_started.connect(self._on_recording_started)
                self.recording_service.recording_stopped.connect(self._on_recording_stopped)
                self.recording_service.recording_error.connect(self._on_recording_error)
                self.recording_service.audio_level_changed.connect(self._on_audio_level_changed)
                self.recording_service.eq_bars_changed.connect(self.eq_bars_changed.emit)
                self.recording_service.recording_auto_stopped.connect(self._on_recording_auto_stopped)
                
            logger.info("Voice service connections established")
        except Exception as e:
            
            logger.error(f"Failed to setup voice service connections: {e}")

    def is_voice_available(self) -> bool:
        """Check if voice functionality is available"""
        stt_ready = self.stt_service and self.stt_service.is_initialized()
        tts_ready = self.tts_service and self.tts_service.is_initialized()
        recording_ready = self.recording_service and self.recording_service.is_initialized()
        if stt_ready:
            print((f"\033[32m[VOICE_AVAILABILITY] STT ready: {stt_ready}\033[0m"))
        if tts_ready:
            print((f"\033[32m[VOICE_AVAILABILITY] TTS ready: {tts_ready}\033[0m"))
        if recording_ready:
            print((f"\033[32m[VOICE_AVAILABILITY] Recording ready: {recording_ready}\033[0m"))
        
        if not stt_ready:
            print(f"[VOICE_AVAILABILITY] STT service: {self.stt_service}")
            if self.stt_service:
                print(f"[VOICE_AVAILABILITY] STT initialized: {self.stt_service.is_initialized()}")
        
        if not tts_ready:
            print(f"[VOICE_AVAILABILITY] TTS service: {self.tts_service}")
            if self.tts_service:
                print((f"\033[31m[VOICE_AVAILABILITY] TTS initialized: {self.tts_service.is_initialized()}\033[0m"))
        
        if not recording_ready:
            print(f"[VOICE_AVAILABILITY] Recording service: {self.recording_service}")
            if self.recording_service:
                print(f"[VOICE_AVAILABILITY] Recording initialized: {self.recording_service.is_initialized()}")

        return stt_ready and tts_ready and recording_ready

    def is_voice_input_available(self) -> bool:
        """Check if voice input (STT + Recording) is available"""
        stt_ready = self.stt_service and self.stt_service.is_initialized()
        recording_ready = self.recording_service and self.recording_service.is_initialized()
        return stt_ready and recording_ready

    def is_initializing(self) -> bool:
        """Check if voice service is currently initializing"""
        # Service is initializing if it exists but is not yet fully available
        # This means at least one of the sub-services is not yet initialized
        if not self.is_voice_available():
            # Check if any services exist (initialization has started)
            has_services = (self.stt_service is not None or 
                          self.tts_service is not None or 
                          self.recording_service is not None)
            return has_services
        return False

    def start_voice_input(self):
        """Start voice recording"""
        try:
            if not self.recording_service:
                logger.error("Recording service not available")
                self.voice_input_error.emit("Recording service not available")
                return

            if self.is_recording:
                logger.debug("Already recording, skipping")
                return

            print(f"[VOICE SERVICE] 🎤 Starting voice input...")
            logger.debug("Starting voice input")
            self.recording_service.start_recording()
            self.is_recording = True
            print(f"[VOICE SERVICE] ✅ Voice input started successfully")

        except Exception as e:
            print(f"[VOICE SERVICE] ❌ Error starting voice input: {e}")
            logger.error(f"Error starting voice input: {e}")
            self.voice_input_error.emit(f"Failed to start voice input: {str(e)}")

    def stop_voice_input(self):
        """Stop voice recording"""
        try:
            if not self.recording_service or not self.is_recording:
                return

            logger.debug("Stopping voice input")
            self.recording_service.stop_recording()
            self.is_recording = False

        except Exception as e:
            logger.error(f"Error stopping voice input: {e}")

    def speak_text(self, text: str):
        """Speak text using TTS"""
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided to speak_text")
                return

            if not self.tts_service:
                logger.error("TTS service not available")
                self.tts_error.emit("TTS service not available")
                return
                
            logger.debug(f"Speaking text: {text[:50]}...")
            # Use non-streaming mode for better compatibility
            self.tts_service.speak_text(text, use_streaming=False)

        except Exception as e:
            logger.error(f"Error in speak_text: {e}")
            self.tts_error.emit(f"TTS failed: {str(e)}")

    def stop_tts(self):
        """Stop TTS playback"""
        try:
            if self.tts_service:
                self.tts_service.stop_playback()
        except Exception as e:
            logger.error(f"Error stopping TTS: {e}")

    def set_continuous_voice_mode(self, enabled: bool):
        """Set continuous voice mode"""
        self.continuous_voice_mode = enabled
        logger.debug(f"Continuous voice mode: {'enabled' if enabled else 'disabled'}")

    def update_settings(self, settings: dict):
        """Update voice settings"""
        self.voice_settings.update(settings)
        logger.debug(f"Updated voice settings: {settings}")

    def get_settings(self) -> dict:
        """Get current voice settings"""
        return self.voice_settings.copy()

    def get_silence_threshold(self) -> float:
        """Get silence threshold for audio level detection"""
        return self.voice_settings.get("silence_threshold", 0.005)

    def is_continuous_voice_mode(self) -> bool:
        """Check if continuous voice mode is enabled"""
        return self.continuous_voice_mode

    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.recording_service:
                self.recording_service.cleanup()
            if self.tts_service:
                self.tts_service.cleanup()
            logger.info("Voice service cleanup completed")
        except Exception as e:
            logger.error(f"Error during voice service cleanup: {e}")

    # Signal handlers
    def _on_recording_started(self):
        """Handle recording started"""
        self.is_recording = True
        self.recording_started.emit()

    def _on_recording_stopped(self):
        """Handle recording stopped"""
        self.is_recording = False
        self.recording_stopped.emit()

    def _on_recording_error(self, error: str):
        """Handle recording error"""
        self.is_recording = False
        self.recording_error.emit(error)

    def _on_recording_auto_stopped(self):
        """Handle automatic recording stop"""
        print(f"[VOICE SERVICE] 🔇 Recording auto-stopped signal received")
        logger.debug("Recording auto-stopped signal received")
        self.is_recording = False

        # Process the recorded audio with STT
        if not self.recording_service:
            print(f"[VOICE SERVICE] ⚠️ Recording service not available")
            logger.warning("Recording service not available")
            return
            
        if not self.stt_service:
            print(f"[VOICE SERVICE] ⚠️ STT service not available")
            logger.warning("STT service not available")
            return
            
        try:
            # When auto-stopped, the file is already saved by the recording service
            # Get the audio file path directly instead of calling stop_recording() again
            audio_file_path = getattr(self.recording_service, 'audio_file', None)
            speech_detected = getattr(self.recording_service, 'speech_detected', False)
            
            print(f"[VOICE SERVICE] 📁 Audio file path: {audio_file_path}")
            print(f"[VOICE SERVICE] 🎤 Speech detected: {speech_detected}")
            
            if audio_file_path and speech_detected:
                print(f"[VOICE SERVICE] 🎤 Processing auto-stopped recording with STT: {audio_file_path}")
                logger.info(f"Processing recorded audio with STT: {audio_file_path}", print_to_terminal=True)
                self.stt_service.process_audio_file(audio_file_path)
            elif audio_file_path:
                print(f"[VOICE SERVICE] 🔇 Audio file saved but no speech detected: {audio_file_path}")
                logger.debug("No speech detected in recording")
            else:
                # Fallback: try stop_recording() if audio_file is not set
                print(f"[VOICE SERVICE] ⚠️ Audio file not found, trying stop_recording() fallback")
                result = self.recording_service.stop_recording()
                if result and result[0]:
                    audio_file_path, speech_detected = result
                    if speech_detected:
                        print(f"[VOICE SERVICE] 🎤 Processing recording with STT (fallback): {audio_file_path}")
                        logger.info(f"Processing recorded audio with STT (fallback): {audio_file_path}", print_to_terminal=True)
                        self.stt_service.process_audio_file(audio_file_path)
                    else:
                        print(f"[VOICE SERVICE] 🔇 No speech detected in recording (fallback)")
                        logger.debug("No speech detected in recording")
                else:
                    print(f"[VOICE SERVICE] ❌ stop_recording() returned no result")
                    logger.warning("stop_recording() returned no result")
        except Exception as e:
            print(f"[VOICE SERVICE] ❌ Error processing recorded audio: {e}")
            logger.error(f"Error processing recorded audio: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            print(f"[VOICE SERVICE] Traceback: {traceback.format_exc()}")

    def _on_stt_text_received(self, text: str):
        """Handle STT text received"""
        try:
            print(f"\n🎤 VOICE SERVICE: STT result received: '{text}'\n")
            logger.info(f"STT result received in voice service: '{text}'", print_to_terminal=True)
            self.is_processing_voice = False
            self.voice_processing_finished.emit()

            cleaned_text = text.strip()
            if cleaned_text and len(cleaned_text) >= 2:
                print(f"\n✅ VOICE INPUT PROCESSED: '{cleaned_text}'\n")
                logger.info(f"Voice input received: '{cleaned_text}'", print_to_terminal=True)
                self.voice_input_received.emit(cleaned_text)
            else:
                print(f"[VOICE INFO] STT result was empty or too short: '{text}'")
                logger.info("STT result was empty or too short", print_to_terminal=True)
                
        except Exception as e:
            print(f"[VOICE ERROR] Error in _on_stt_text_received: {e}")
            logger.error(f"Error in _on_stt_text_received: {e}")

    def _on_stt_error(self, error: str):
        """Handle STT error"""
        self.is_processing_voice = False
        self.voice_processing_finished.emit()
        self.voice_input_error.emit(error)

    def _on_tts_started(self):
        """Handle TTS started"""
        self.is_playing_tts = True
        self.tts_started.emit()

    def _on_tts_finished(self):
        """Handle TTS finished"""
        self.is_playing_tts = False
        self.tts_finished.emit()

    def _on_tts_error(self, error: str):
        """Handle TTS error"""
        self.is_playing_tts = False
        self.tts_error.emit(error)

    def _on_audio_level_changed(self, audio_level: float):
        """Handle audio level changes"""
        self.audio_level_changed.emit(audio_level) 
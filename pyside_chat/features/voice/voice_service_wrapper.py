"""
Voice Service Wrapper

Provides the same interface as VoiceService but uses the process manager
for running voice services in a separate process.
"""

from typing import Dict, Any, Optional
from PySide6.QtCore import QObject, Signal

from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.features.voice.orchestrator import VoiceProcessManager as VoiceProcessManager

logger = CustomLogger.get_logger(__name__)


class VoiceServiceWrapper(QObject):
    """Wrapper for voice services that runs in a separate process"""
    
    # Signals (same as VoiceService)
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
    audio_level_changed = Signal(float)  # Audio level for EQ visualization
    
    def __init__(self, use_separate_process: bool = True):
        super().__init__()
        self.use_separate_process = use_separate_process
        self.process_manager = None
        self.direct_service = None
        self._cached_state = {
            "is_recording": False,
            "is_processing_voice": False,
            "is_playing_tts": False
        }
        
        if use_separate_process:
            self._init_process_manager()
        else:
            self._init_direct_service()
    
    def _init_process_manager(self):
        """Initialize the process manager"""
        try:
            from pyside_chat.features.voice.orchestrator import create_voice_process_manager
            self.process_manager = create_voice_process_manager()
            
            # Connect signals from process manager with QueuedConnection for thread safety
            from PySide6.QtCore import Qt
            self.process_manager.voice_input_received.connect(self.voice_input_received.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.voice_input_error.connect(self.voice_input_error.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.tts_started.connect(self.tts_started.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.tts_finished.connect(self.tts_finished.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.tts_error.connect(self.tts_error.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.recording_started.connect(self.recording_started.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.recording_stopped.connect(self.recording_stopped.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.recording_error.connect(self.recording_error.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.voice_processing_started.connect(self.voice_processing_started.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.voice_processing_finished.connect(self.voice_processing_finished.emit, Qt.ConnectionType.QueuedConnection)
            self.process_manager.state_updated.connect(self._update_cached_state_from_signal, Qt.ConnectionType.QueuedConnection)
            
            logger.info("[ID:0225] Voice service wrapper initialized with process manager")
            
        except Exception as e:
            logger.error(f"[ID:0224] Failed to initialize process manager: {e}")
            logger.info("[ID:0223] Falling back to direct voice service")
            self._init_direct_service()
    
    def _init_direct_service(self):
        """Initialize direct voice service (fallback)"""
        try:
            from .voice_service import VoiceService
            self.direct_service = VoiceService()
            
            # Connect signals from direct service with QueuedConnection for thread safety
            from PySide6.QtCore import Qt
            self.direct_service.voice_input_received.connect(self.voice_input_received.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.voice_input_error.connect(self.voice_input_error.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.tts_started.connect(self.tts_started.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.tts_finished.connect(self.tts_finished.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.tts_error.connect(self.tts_error.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.recording_started.connect(self.recording_started.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.recording_stopped.connect(self.recording_stopped.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.recording_error.connect(self.recording_error.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.voice_processing_started.connect(self.voice_processing_started.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.voice_processing_finished.connect(self.voice_processing_finished.emit, Qt.ConnectionType.QueuedConnection)
            self.direct_service.audio_level_changed.connect(self.audio_level_changed.emit, Qt.ConnectionType.QueuedConnection)
            
            logger.info("[ID:0222] Voice service wrapper initialized with direct service")
            
        except Exception as e:
            logger.error(f"[ID:0221] Failed to initialize direct voice service: {e}")
            # Don't raise the exception, just log it and continue without voice service
            self.direct_service = None
    
    def start_voice_input(self):
        """Start voice recording and convert to text"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("start_voice_input")
        elif self.direct_service:
            self.direct_service.start_voice_input()
        else:
            logger.error("[ID:0220] No voice service available")
    
    def stop_voice_input(self):
        """Stop voice recording and process the audio"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("stop_voice_input")
        elif self.direct_service:
            self.direct_service.stop_voice_input()
        else:
            logger.error("[ID:0219] No voice service available")
    
    def speak_text(self, text: str):
        """Convert text to speech and play it"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("speak_text", text)
        elif self.direct_service:
            self.direct_service.speak_text(text)
        else:
            logger.error("[ID:0218] No voice service available")
    
    def speak_text_streaming(self, text: str):
        """Convert text to speech using streaming synthesis"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("speak_text_streaming", text)
        elif self.direct_service:
            self.direct_service.speak_text_streaming(text)
        else:
            logger.error("[ID:0217] No voice service available")
    
    def speak_text_non_streaming(self, text: str):
        """Convert text to speech using non-streaming synthesis"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("speak_text_non_streaming", text)
        elif self.direct_service:
            self.direct_service.speak_text_non_streaming(text)
        else:
            logger.error("[ID:0216] No voice service available")
    
    def stop_tts(self):
        """Stop current TTS playback"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("stop_tts")
        elif self.direct_service:
            self.direct_service.stop_tts()
        else:
            logger.error("[ID:0215] No voice service available")
    
    def is_voice_available(self) -> bool:
        """Check if voice functionality is available"""
        if self.use_separate_process and self.process_manager:
            return self.process_manager.is_process_running()
        elif self.direct_service:
            return self.direct_service.is_voice_available()
        else:
            return False
    
    def update_settings(self, settings: dict):
        """Update voice service settings"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("update_settings", settings)
        elif self.direct_service:
            self.direct_service.update_settings(settings)
        else:
            logger.error("[ID:0214] No voice service available")
    
    def get_recording_timeout(self) -> float:
        """Get current recording timeout in seconds"""
        if self.direct_service:
            return self.direct_service.get_recording_timeout()
        return 10.0  # Default fallback
    
    def set_recording_timeout(self, timeout: float):
        """Set recording timeout in seconds"""
        if self.direct_service:
            self.direct_service.set_recording_timeout(timeout)
    
    def get_silence_duration(self) -> float:
        """Get current silence duration in seconds"""
        if self.direct_service:
            return self.direct_service.get_silence_duration()
        return 3.0  # Default fallback
    
    def set_silence_duration(self, duration: float):
        """Set silence duration in seconds"""
        if self.direct_service:
            self.direct_service.set_silence_duration(duration)
    
    def get_silence_threshold(self) -> float:
        """Get current silence threshold (0-1)"""
        if self.direct_service:
            return self.direct_service.get_silence_threshold()
        return 0.005  # Default fallback
    
    def set_silence_threshold(self, threshold: float):
        """Set silence threshold (0-1)"""
        if self.direct_service:
            self.direct_service.set_silence_threshold(threshold)
    
    def set_audio_gate_enabled(self, enabled: bool):
        """Enable or disable audio gate detection"""
        if self.direct_service:
            self.direct_service.set_audio_gate_enabled(enabled)
    
    def get_current_audio_level(self) -> float:
        """Get current audio level for debugging"""
        if self.direct_service:
            return self.direct_service.get_current_audio_level()
        return 0.0  # Default fallback
    
    def set_continuous_voice_mode(self, enabled: bool):
        """Enable or disable continuous voice mode"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("set_continuous_voice_mode", enabled)
        elif self.direct_service:
            self.direct_service.set_continuous_voice_mode(enabled)
        else:
            logger.error("[ID:0213] No voice service available")
    
    def is_continuous_voice_mode(self) -> bool:
        """Check if continuous voice mode is enabled"""
        if self.direct_service:
            return self.direct_service.is_continuous_voice_mode()
        return False  # Default fallback
    
    def cleanup_on_exit(self):
        """Clean up resources on application exit"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.stop_voice_process()
        elif self.direct_service:
            self.direct_service.cleanup_on_exit()
    
    def get_audio_folder_path(self) -> str:
        """Get the path to the audio folder"""
        if self.direct_service:
            return self.direct_service.get_audio_folder_path()
        return "User_history/audio"  # Default fallback
    
    def list_audio_files(self) -> list:
        """List all audio files in the audio folder"""
        if self.direct_service:
            return self.direct_service.list_audio_files()
        return []
    
    def cleanup_old_audio_files(self, max_files: int = 100, max_age_days: int = 7):
        """Clean up old audio files to prevent folder from getting too large"""
        if self.direct_service:
            self.direct_service.cleanup_old_audio_files(max_files, max_age_days)
    
    def cleanup_all_audio_files(self):
        """Clean up all audio files"""
        if self.direct_service:
            self.direct_service.cleanup_all_audio_files()
    
    def get_process_info(self) -> Dict[str, Any]:
        """Get information about the voice process"""
        if self.use_separate_process and self.process_manager:
            return self.process_manager.get_process_info()
        return {"status": "direct_service"}
    
    def test_connection(self) -> bool:
        """Test connection to voice process"""
        if self.use_separate_process and self.process_manager:
            return self.process_manager.send_command("test_connection")
        return True  # Direct service is always available if initialized
    
    def _update_cached_state(self):
        """Update cached state from process manager"""
        if self.use_separate_process and self.process_manager:
            self.process_manager.send_command("get_state")
            # Note: The state will be updated via signal handling
    
    def _update_cached_state_from_signal(self, state: dict):
        """Update cached state from signal"""
        self._cached_state.update(state)
    
    @property
    def is_recording(self) -> bool:
        """Check if currently recording"""
        if self.direct_service:
            return self.direct_service.is_recording
        return self._cached_state.get("is_recording", False)
    
    @property
    def is_processing_voice(self) -> bool:
        """Check if currently processing voice input"""
        if self.direct_service:
            return self.direct_service.is_processing_voice
        return self._cached_state.get("is_processing_voice", False)
    
    @property
    def is_playing_tts(self) -> bool:
        """Check if TTS is currently playing"""
        if self.direct_service:
            return self.direct_service.is_playing_tts
        return self._cached_state.get("is_playing_tts", False)
    
    @property
    def recording_service(self):
        """Get the recording service (only available in direct mode)"""
        if self.direct_service:
            return self.direct_service.recording_service
        return None 
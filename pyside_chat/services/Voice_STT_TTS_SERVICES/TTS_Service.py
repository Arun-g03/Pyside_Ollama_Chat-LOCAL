import os
import subprocess
import platform
from PySide6.QtCore import QObject, Signal, QTimer
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class TTSService(QObject):
    """Text-to-Speech service for converting text to speech"""
    # Signals
    tts_started = Signal()
    tts_finished = Signal()
    tts_error = Signal(str)

    def __init__(self):
        super().__init__()
        self.available = self._check_availability()
        self.media_player = None
        self.audio_output = None
        self.current_audio_file = None
        self.current_voice = "en"
        self.current_api = "Google TTS"

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

    def speak_text(self, text: str):
        try:
            logger.debug(f"Converting text to speech: {text[:50]}...")
            self.tts_started.emit()
            self._speak_with_gtts(text)
        except Exception as e:
            logger.error(f"TTS conversion failed: {e}")
            self.tts_error.emit(f"TTS conversion failed: {str(e)}")

    def _speak_with_gtts(self, text: str):
        try:
            from gtts import gTTS
            import playsound
            audio_folder = os.path.join(os.getcwd(), "User_history", "audio")
            os.makedirs(audio_folder, exist_ok=True)
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_output_{timestamp}.mp3"
            audio_file_path = os.path.join(audio_folder, filename)
            tts = gTTS(text=text, lang=self.current_voice, slow=False)
            tts.save(audio_file_path)
            playsound.playsound(audio_file_path, block=False)
            QTimer.singleShot(5000, lambda: self._cleanup_audio_file(audio_file_path))
            QTimer.singleShot(1000, self.tts_finished.emit)
        except ImportError:
            logger.error("gTTS or playsound not available, falling back to eSpeak")
            self._speak_with_espeak(text)
        except Exception as e:
            logger.error(f"Google TTS failed: {e}")
            self._speak_with_espeak(text)

    def _speak_with_espeak(self, text: str):
        try:
            if platform.system() == "Windows":
                cmd = ["espeak", text]
            else:
                cmd = ["espeak", text]
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
            self.tts_finished.emit()
        except Exception as e:
            logger.error(f"eSpeak failed: {e}")
            self.tts_finished.emit()

    def _cleanup_audio_file(self, file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to cleanup audio file {file_path}: {e}")

    def _simulate_tts_finished(self):
        self.tts_finished.emit()

    def stop_playback(self):
        if self.media_player:
            self.media_player.stop()
        self.tts_finished.emit()

    def update_api(self, api_name: str):
        logger.debug(f"TTS API updated to: {api_name}")
        # TODO: Implement API switching logic

    def update_voice(self, voice_name: str):
        logger.debug(f"TTS voice updated to: {voice_name}")
        self.current_voice = voice_name

    def update_speed(self, speed: float):
        logger.debug(f"TTS speed updated to: {speed}")
        # TODO: Implement speed adjustment logic

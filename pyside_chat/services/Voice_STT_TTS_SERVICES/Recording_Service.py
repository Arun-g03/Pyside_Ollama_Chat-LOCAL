import os
import threading
import time
import wave
import pyaudio
from typing import Optional
from PySide6.QtCore import QObject, Signal
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class RecordingService(QObject):
    """Audio recording service for capturing voice input"""
    # Signals
    recording_started = Signal()
    recording_stopped = Signal()
    recording_error = Signal(str)
    audio_level_changed = Signal(float)  # Emitted when audio level changes
    recording_auto_stopped = Signal()    # Emitted when recording stops due to silence detection

    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.recording_thread = None
        self.audio_file = None
        self.audio = None
        self.frames = []
        self.stream = None
        self.speech_detected = False  # Track if speech was detected
        self.silence_threshold = 0.005  # Balanced threshold for good sensitivity
        self.silence_duration = 2.0
        self.silence_timer = None
        self.last_audio_level = 0.0
        try:
            self.audio = pyaudio.PyAudio()
            self.available = self._check_availability()
        except Exception as e:
            logger.error(f"Failed to initialize PyAudio: {e}")
            self.available = False

    def __del__(self):
        try:
            self.cleanup()
        except:
            pass

    def _check_availability(self) -> bool:
        try:
            test_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            test_stream.close()
            return True
        except Exception as e:
            logger.error(f"Recording service not available: {e}")
            return False

    def is_available(self) -> bool:
        return self.available

    def start_recording(self):
        if self.is_recording:
            logger.warning("Recording already in progress")
            return
        try:
            self.is_recording = True
            self.frames = []
            self.speech_detected = False  # Reset at start
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            self.recording_started.emit()
            logger.debug("Audio recording started")
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to start recording: {e}")
            self.recording_error.emit(f"Failed to start recording: {str(e)}")

    def _record_audio(self):
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            logger.debug("Recording audio with audio gate...")
            speech_detection_threshold = max(0.001, self.silence_threshold * 0.5)
            speech_started = False
            silence_start_time = None
            while self.is_recording:
                try:
                    data = self.stream.read(1024, exception_on_overflow=False)
                    self.frames.append(data)
                    audio_level = self._calculate_audio_level(data)
                    self.last_audio_level = audio_level
                    try:
                        self.audio_level_changed.emit(audio_level)
                    except Exception:
                        pass
                    if not speech_started:
                        if audio_level > speech_detection_threshold:
                            speech_started = True
                            self.speech_detected = True
                            silence_start_time = None
                    else:
                        if audio_level > self.silence_threshold:
                            silence_start_time = None
                        else:
                            if silence_start_time is None:
                                silence_start_time = time.time()
                            elif time.time() - silence_start_time >= self.silence_duration:
                                logger.debug("Silence timeout reached after speech, stopping recording automatically")
                                try:
                                    self.recording_auto_stopped.emit()
                                except Exception:
                                    pass
                                break
                except Exception as e:
                    logger.error(f"Error reading audio data: {e}")
                    break
        except Exception as e:
            logger.error(f"Recording thread error: {e}")
            self.recording_error.emit(f"Recording error: {str(e)}")
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()

    def _calculate_audio_level(self, audio_data: bytes) -> float:
        try:
            import struct
            import math
            samples = struct.unpack(f'{len(audio_data)//2}h', audio_data)
            if samples:
                rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))
                normalized_rms = rms / 32768.0
                return normalized_rms
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating audio level: {e}")
            return 0.0

    def audio_level_to_db(self, audio_level: float) -> float:
        try:
            import math
            if audio_level > 0:
                db = 20 * math.log10(audio_level)
                return max(-60, db)
            return -60.0
        except Exception as e:
            logger.error(f"Error converting to dB: {e}")
            return -60.0

    def get_current_audio_level(self) -> float:
        return self.last_audio_level

    def set_audio_gate_enabled(self, enabled: bool):
        if enabled:
            self.silence_threshold = 0.005
        else:
            self.silence_threshold = 0.0
        logger.debug(f"Audio gate {'enabled' if enabled else 'disabled'}")

    def cleanup(self):
        try:
            if self.audio:
                self.audio.terminate()
                self.audio = None
            logger.debug("PyAudio resources cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up PyAudio: {e}")

    def stop_recording(self) -> Optional[tuple]:
        if not self.is_recording and not self.frames:
            logger.warning("No recording in progress")
            return None
        try:
            if self.is_recording:
                self.is_recording = False
                if self.recording_thread and self.recording_thread.is_alive():
                    self.recording_thread.join(timeout=2.0)
            self.recording_stopped.emit()
            if not self.frames:
                logger.warning("No audio frames recorded")
                return None
            if not self.speech_detected:
                logger.info("No speech detected, not saving audio file.")
                return (None, False)
            audio_folder = os.path.join(os.getcwd(), "User_history", "audio")
            os.makedirs(audio_folder, exist_ok=True)
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_input_{timestamp}.wav"
            audio_file_path = os.path.join(audio_folder, filename)
            with wave.open(audio_file_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(16000)
                wf.writeframes(b''.join(self.frames))
            self.audio_file = audio_file_path
            logger.debug(f"Audio saved to: {self.audio_file}")
            return (self.audio_file, self.speech_detected)
        except Exception as e:
            if self.is_recording:
                self.is_recording = False
            logger.error(f"Failed to stop recording: {e}")
            self.recording_error.emit(f"Failed to stop recording: {str(e)}")
            return None

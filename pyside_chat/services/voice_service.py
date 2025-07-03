"""
Voice Service Module

Handles voice input/output functionality including:
- Speech-to-Text (STT) for user voice input
- Text-to-Speech (TTS) for AI responses
- Voice recording and playback
"""

import os
import tempfile
import threading
import time
import wave
import pyaudio
import speech_recognition as sr
from typing import Optional, Callable
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import subprocess
import platform
import json

from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class VoiceService(QObject):
    """Main voice service that orchestrates STT and TTS functionality"""
    
    # Signals
    voice_input_received = Signal(str)  # Emitted when voice is converted to text
    voice_input_error = Signal(str)     # Emitted when voice input fails
    tts_started = Signal()              # Emitted when TTS starts
    tts_finished = Signal()             # Emitted when TTS finishes
    tts_error = Signal(str)             # Emitted when TTS fails
    recording_started = Signal()        # Emitted when recording starts
    recording_stopped = Signal()        # Emitted when recording stops
    recording_error = Signal(str)       # Emitted when recording fails
    
    def __init__(self):
        super().__init__()
        self.stt_service = STTService()
        self.tts_service = TTSService()
        self.recording_service = RecordingService()
        
        # Connect signals
        self.stt_service.text_received.connect(self.voice_input_received.emit)
        self.stt_service.error_occurred.connect(self.voice_input_error.emit)
        self.tts_service.tts_started.connect(self.tts_started.emit)
        self.tts_service.tts_finished.connect(self.tts_finished.emit)
        self.tts_service.tts_error.connect(self.tts_error.emit)
        self.recording_service.recording_started.connect(self.recording_started.emit)
        self.recording_service.recording_stopped.connect(self.recording_stopped.emit)
        self.recording_service.recording_error.connect(self.recording_error.emit)
        
        # State tracking
        self.is_recording = False
        self.is_playing_tts = False
        
        # Recording settings
        self.recording_timeout = 10.0  # Default 10 seconds (fallback)
        self.silence_threshold = 0.01  # Audio level threshold for silence detection
        self.silence_duration = 2.0    # Seconds of silence before stopping
        self.recording_timer = QTimer()
        self.recording_timer.setSingleShot(True)
        self.recording_timer.timeout.connect(self._on_recording_timeout)
        
        # Clean up all audio files on startup (since they're only for STT processing)
        QTimer.singleShot(1000, lambda: self.cleanup_all_audio_files())
    
    def __del__(self):
        """Cleanup when voice service is destroyed"""
        try:
            self.cleanup_all_audio_files()
            if hasattr(self, 'recording_service'):
                self.recording_service.cleanup()
        except:
            pass  # Ignore errors during cleanup
        
    def start_voice_input(self):
        """Start voice recording and convert to text"""
        if self.is_recording:
            logger.warning("Voice recording already in progress")
            return
            
        try:
            self.is_recording = True
            
            # Update recording service with audio gate settings
            self.recording_service.silence_threshold = self.silence_threshold
            self.recording_service.silence_duration = self.silence_duration
            
            self.recording_service.start_recording()
            
            # Start fallback recording timeout timer (in case audio gate fails)
            timeout_ms = int(self.recording_timeout * 1000)
            self.recording_timer.start(timeout_ms)
            
            logger.debug(f"Voice input started with audio gate (silence: {self.silence_duration}s, threshold: {self.silence_threshold})")
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to start voice input: {e}")
            self.voice_input_error.emit(f"Failed to start voice input: {str(e)}")
    
    def stop_voice_input(self):
        """Stop voice recording and process the audio"""
        if not self.is_recording:
            logger.warning("No voice recording in progress")
            return
            
        try:
            # Stop the timeout timer
            self.recording_timer.stop()
            
            audio_file = self.recording_service.stop_recording()
            self.is_recording = False
            
            if audio_file and os.path.exists(audio_file):
                # Convert audio to text
                self.stt_service.convert_audio_to_text(audio_file)
            else:
                logger.warning("No audio file generated")
                self.voice_input_error.emit("No audio recorded")
                
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to stop voice input: {e}")
            self.voice_input_error.emit(f"Failed to process voice input: {str(e)}")
    
    def _on_recording_timeout(self):
        """Handle recording timeout - automatically stop recording"""
        if self.is_recording:
            logger.debug("Recording timeout reached, stopping automatically")
            self.stop_voice_input()
    
    def speak_text(self, text: str):
        """Convert text to speech and play it"""
        if self.is_playing_tts:
            logger.warning("TTS already in progress")
            return
            
        try:
            self.is_playing_tts = True
            self.tts_service.speak_text(text)
            logger.debug(f"TTS started for text: {text[:50]}...")
        except Exception as e:
            self.is_playing_tts = False
            logger.error(f"Failed to start TTS: {e}")
            self.tts_error.emit(f"Failed to start TTS: {str(e)}")
    
    def stop_tts(self):
        """Stop current TTS playback"""
        self.tts_service.stop_playback()
        self.is_playing_tts = False
    
    def is_voice_available(self) -> bool:
        """Check if voice functionality is available"""
        return (self.stt_service.is_available() and 
                self.tts_service.is_available() and 
                self.recording_service.is_available())
    
    def update_settings(self, settings: dict):
        """Update voice service settings"""
        logger.debug(f"Updating voice service settings: {settings}")
        
        # Update STT service settings
        if "stt_api" in settings:
            self.stt_service.update_api(settings["stt_api"])
            
        # Update TTS service settings
        if "tts_api" in settings:
            self.tts_service.update_api(settings["tts_api"])
            
        if "tts_voice" in settings:
            self.tts_service.update_voice(settings["tts_voice"])
            
        if "voice_speed" in settings:
            self.tts_service.update_speed(settings["voice_speed"])
            
        # Update recording settings
        if "recording_timeout" in settings:
            self.recording_timeout = settings["recording_timeout"]
            logger.debug(f"Recording timeout updated to {self.recording_timeout}s")
            
        if "silence_duration" in settings:
            self.silence_duration = settings["silence_duration"]
            logger.debug(f"Silence duration updated to {self.silence_duration}s")
            
        if "silence_threshold" in settings:
            self.silence_threshold = settings["silence_threshold"]
            logger.debug(f"Silence threshold updated to {self.silence_threshold}")
    
    def get_recording_timeout(self) -> float:
        """Get current recording timeout in seconds"""
        return self.recording_timeout
    
    def set_recording_timeout(self, timeout: float):
        """Set recording timeout in seconds"""
        self.recording_timeout = max(1.0, min(60.0, timeout))  # Clamp between 1-60 seconds
        logger.debug(f"Recording timeout set to {self.recording_timeout}s")
    
    def get_silence_duration(self) -> float:
        """Get current silence duration in seconds"""
        return self.silence_duration
    
    def set_silence_duration(self, duration: float):
        """Set silence duration in seconds"""
        self.silence_duration = max(0.5, min(10.0, duration))  # Clamp between 0.5-10 seconds
        logger.debug(f"Silence duration set to {self.silence_duration}s")
    
    def get_silence_threshold(self) -> float:
        """Get current silence threshold (0-1)"""
        return self.silence_threshold
    
    def set_silence_threshold(self, threshold: float):
        """Set silence threshold (0-1)"""
        self.silence_threshold = max(0.001, min(0.1, threshold))  # Clamp between 0.001-0.1
        logger.debug(f"Silence threshold set to {self.silence_threshold}")
    
    def set_audio_gate_enabled(self, enabled: bool):
        """Enable or disable audio gate detection"""
        self.recording_service.set_audio_gate_enabled(enabled)
        logger.debug(f"Audio gate {'enabled' if enabled else 'disabled'} for voice service")
    
    def get_current_audio_level(self) -> float:
        """Get current audio level for debugging"""
        return self.recording_service.get_current_audio_level()
    
    def cleanup_on_exit(self):
        """Clean up audio files on application exit"""
        logger.info("Cleaning up audio files on application exit")
        self.cleanup_all_audio_files()
        
        # Clean up recording service
        if hasattr(self, 'recording_service'):
            self.recording_service.cleanup()
    
    def get_audio_folder_path(self) -> str:
        """Get the path to the audio folder"""
        return os.path.join(os.getcwd(), "User_history", "audio")
    
    def list_audio_files(self) -> list:
        """List all audio files in the audio folder"""
        audio_folder = self.get_audio_folder_path()
        if not os.path.exists(audio_folder):
            return []
        
        audio_files = []
        for filename in os.listdir(audio_folder):
            if filename.endswith(('.wav', '.mp3')):
                file_path = os.path.join(audio_folder, filename)
                file_info = {
                    'filename': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                }
                audio_files.append(file_info)
        
        # Sort by modification time (newest first)
        audio_files.sort(key=lambda x: x['modified'], reverse=True)
        return audio_files
    
    def cleanup_old_audio_files(self, max_files: int = 100, max_age_days: int = 7):
        """Clean up old audio files to prevent folder from getting too large"""
        audio_files = self.list_audio_files()
        
        if len(audio_files) <= max_files:
            return
        
        # Calculate cutoff time for age-based cleanup
        import time
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
        
        files_to_delete = []
        
        # Mark files for deletion based on age
        for file_info in audio_files:
            if file_info['modified'] < cutoff_time:
                files_to_delete.append(file_info)
        
        # If we still have too many files, delete the oldest ones
        if len(audio_files) - len(files_to_delete) > max_files:
            remaining_files = [f for f in audio_files if f not in files_to_delete]
            files_to_delete.extend(remaining_files[max_files:])
        
        # Delete the marked files
        for file_info in files_to_delete:
            try:
                os.remove(file_info['path'])
                logger.debug(f"Deleted old audio file: {file_info['filename']}")
            except Exception as e:
                logger.error(f"Failed to delete audio file {file_info['filename']}: {e}")
        
        if files_to_delete:
            logger.info(f"Cleaned up {len(files_to_delete)} old audio files")
    
    def cleanup_all_audio_files(self):
        """Clean up all audio files (since they're only for STT processing)"""
        audio_files = self.list_audio_files()
        
        if not audio_files:
            return
        
        deleted_count = 0
        for file_info in audio_files:
            try:
                os.remove(file_info['path'])
                deleted_count += 1
                logger.debug(f"Deleted audio file: {file_info['filename']}")
            except Exception as e:
                logger.error(f"Failed to delete audio file {file_info['filename']}: {e}")
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} audio files on startup")


class STTService(QObject):
    """Speech-to-Text service for converting voice to text"""
    
    # Signals
    text_received = Signal(str)  # Emitted when text is successfully converted
    error_occurred = Signal(str) # Emitted when conversion fails
    
    def __init__(self):
        super().__init__()
        self.current_api = "Google Speech Recognition"
        self.vosk_model = None
        self.recognizer = sr.Recognizer()
        self.available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Check if STT service is available"""
        try:
            # Check if required packages are available
            import speech_recognition
            import pyaudio
            
            # Try to initialize Vosk model
            try:
                from vosk import Model
                model_path = os.path.join(os.getcwd(), "models", "vosk-model-small-en-us-0.15")
                if os.path.exists(model_path):
                    self.vosk_model = Model(model_path)
                    logger.debug("Vosk model loaded successfully")
                else:
                    logger.warning("Vosk model not found, offline STT will not be available")
            except ImportError:
                logger.warning("Vosk not available, offline STT will not be available")
            except Exception as e:
                logger.warning(f"Failed to load Vosk model: {e}")
                
            return True
        except ImportError as e:
            logger.error(f"STT dependencies not available: {e}")
            return False
        except Exception as e:
            logger.error(f"STT service not available: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if STT service is available"""
        return self.available
    
    def convert_audio_to_text(self, audio_file: str):
        """Convert audio file to text"""
        try:
            logger.debug(f"Converting audio file to text using {self.current_api}: {audio_file}")
            
            if self.current_api == "Google Speech Recognition":
                self._convert_with_google(audio_file)
            elif self.current_api == "Vosk (Offline)":
                self._convert_with_vosk(audio_file)
            else:
                # Fallback to Google
                self._convert_with_google(audio_file)
                
        except Exception as e:
            logger.error(f"STT conversion failed: {e}")
            self.error_occurred.emit(f"STT conversion failed: {str(e)}")
    
    def _convert_with_google(self, audio_file: str):
        """Convert audio using Google Speech Recognition"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            logger.debug(f"Google STT result: {text}")
            self.text_received.emit(text)
            
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
            self.error_occurred.emit("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            logger.error(f"Google Speech Recognition request failed: {e}")
            # Fallback to Vosk if available
            if self.vosk_model:
                logger.info("Falling back to Vosk for offline recognition")
                self._convert_with_vosk(audio_file)
            else:
                self.error_occurred.emit(f"Speech recognition failed: {str(e)}")
        except Exception as e:
            logger.error(f"Google STT failed: {e}")
            self.error_occurred.emit(f"Speech recognition failed: {str(e)}")
    
    def _convert_with_vosk(self, audio_file: str):
        """Convert audio using Vosk (offline)"""
        try:
            if not self.vosk_model:
                raise Exception("Vosk model not available")
                
            from vosk import KaldiRecognizer
            
            # Open the audio file
            wf = wave.open(audio_file, "rb")
            
            # Create recognizer
            rec = KaldiRecognizer(self.vosk_model, wf.getframerate())
            rec.SetWords(True)
            
            # Process audio
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get('text'):
                        results.append(result['text'])
            
            # Get final result
            final_result = json.loads(rec.FinalResult())
            if final_result.get('text'):
                results.append(final_result['text'])
            
            wf.close()
            
            # Combine all results
            text = ' '.join(results).strip()
            
            if text:
                logger.debug(f"Vosk STT result: {text}")
                self.text_received.emit(text)
            else:
                logger.warning("Vosk could not understand audio")
                self.error_occurred.emit("Could not understand audio. Please try again.")
                
        except Exception as e:
            logger.error(f"Vosk STT failed: {e}")
            self.error_occurred.emit(f"Offline speech recognition failed: {str(e)}")
    
    def update_api(self, api_name: str):
        """Update the STT API being used"""
        logger.debug(f"STT API updated to: {api_name}")
        self.current_api = api_name


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
        """Check if TTS service is available"""
        try:
            # TODO: Implement actual availability check based on chosen TTS provider
            # For now, assume it's available
            return True
        except Exception as e:
            logger.error(f"TTS service not available: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if TTS service is available"""
        return self.available
    
    def speak_text(self, text: str):
        """Convert text to speech and play it"""
        try:
            logger.debug(f"Converting text to speech: {text[:50]}...")
            self.tts_started.emit()
            
            # Use Google TTS
            self._speak_with_gtts(text)
            
        except Exception as e:
            logger.error(f"TTS conversion failed: {e}")
            self.tts_error.emit(f"TTS conversion failed: {str(e)}")
    
    def _speak_with_gtts(self, text: str):
        """Use Google TTS to convert text to speech"""
        try:
            from gtts import gTTS
            import playsound
            
            # Create audio folder if it doesn't exist
            audio_folder = os.path.join(os.getcwd(), "User_history", "audio")
            os.makedirs(audio_folder, exist_ok=True)
            
            # Generate timestamped filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_output_{timestamp}.mp3"
            audio_file_path = os.path.join(audio_folder, filename)
            
            # Convert text to speech with selected voice
            tts = gTTS(text=text, lang=self.current_voice, slow=False)
            tts.save(audio_file_path)
            
            # Play the audio
            playsound.playsound(audio_file_path, block=False)
            
            # Clean up the file after a delay
            QTimer.singleShot(5000, lambda: self._cleanup_audio_file(audio_file_path))
            
            # Emit finished signal after a short delay
            QTimer.singleShot(1000, self.tts_finished.emit)
            
        except ImportError:
            logger.error("gTTS or playsound not available, falling back to eSpeak")
            self._speak_with_espeak(text)
        except Exception as e:
            logger.error(f"Google TTS failed: {e}")
            self._speak_with_espeak(text)
    
    def _speak_with_espeak(self, text: str):
        """Use eSpeak as fallback TTS"""
        try:
            # Use eSpeak command line tool
            if platform.system() == "Windows":
                cmd = ["espeak", text]
            else:
                cmd = ["espeak", text]
            
            # Run eSpeak in a separate process
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for completion
            process.wait()
            
            self.tts_finished.emit()
            
        except Exception as e:
            logger.error(f"eSpeak failed: {e}")
            self.tts_finished.emit()
    
    def _cleanup_audio_file(self, file_path: str):
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to cleanup audio file {file_path}: {e}")
    
    def _simulate_tts_finished(self):
        """Simulate TTS completion (placeholder)"""
        self.tts_finished.emit()
    
    def stop_playback(self):
        """Stop current TTS playback"""
        if self.media_player:
            self.media_player.stop()
        self.tts_finished.emit()
    
    def update_api(self, api_name: str):
        """Update the TTS API being used"""
        logger.debug(f"TTS API updated to: {api_name}")
        # TODO: Implement API switching logic
    
    def update_voice(self, voice_name: str):
        """Update the TTS voice being used"""
        logger.debug(f"TTS voice updated to: {voice_name}")
        self.current_voice = voice_name
    
    def update_speed(self, speed: float):
        """Update the TTS playback speed"""
        logger.debug(f"TTS speed updated to: {speed}")
        # TODO: Implement speed adjustment logic


class RecordingService(QObject):
    """Audio recording service for capturing voice input"""
    
    # Signals
    recording_started = Signal()
    recording_stopped = Signal()
    recording_error = Signal(str)
    audio_level_changed = Signal(float)  # Emitted when audio level changes
    
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.recording_thread = None
        self.audio_file = None
        self.audio = None
        self.frames = []
        self.stream = None
        
        # Audio gate settings
        self.silence_threshold = 0.005  # Balanced threshold for good sensitivity
        self.silence_duration = 2.0
        self.silence_timer = None
        self.last_audio_level = 0.0
        
        # Initialize PyAudio and check availability
        try:
            self.audio = pyaudio.PyAudio()
            self.available = self._check_availability()
        except Exception as e:
            logger.error(f"Failed to initialize PyAudio: {e}")
            self.available = False
    
    def __del__(self):
        """Cleanup when recording service is destroyed"""
        try:
            self.cleanup()
        except:
            pass  # Ignore errors during cleanup
        
    def _check_availability(self) -> bool:
        """Check if recording service is available"""
        try:
            # Test if PyAudio can access microphone
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
        """Check if recording service is available"""
        return self.available
    
    def start_recording(self):
        """Start audio recording"""
        if self.is_recording:
            logger.warning("Recording already in progress")
            return
            
        try:
            self.is_recording = True
            self.frames = []
            
            # Start recording in a separate thread
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            
            self.recording_started.emit()
            logger.debug("Audio recording started")
            
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to start recording: {e}")
            self.recording_error.emit(f"Failed to start recording: {str(e)}")
    
    def _record_audio(self):
        """Record audio in a separate thread with audio gate detection"""
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024
            )
            
            logger.debug("Recording audio with audio gate...")
            
            # Track silence duration manually since QTimer can't be used in thread
            silence_start_time = None
            
            while self.is_recording:
                try:
                    data = self.stream.read(1024, exception_on_overflow=False)
                    self.frames.append(data)
                    
                    # Check audio level for silence detection
                    audio_level = self._calculate_audio_level(data)
                    self.last_audio_level = audio_level
                    
                    # Emit audio level for UI updates
                    try:
                        self.audio_level_changed.emit(audio_level)
                    except Exception as e:
                        # Ignore signal emission errors from non-main thread
                        pass
                    
                    if audio_level > self.silence_threshold:
                        # Audio detected, reset silence tracking
                        silence_start_time = None
                    else:
                        # Silence detected, start tracking silence duration
                        if silence_start_time is None:
                            silence_start_time = time.time()
                        elif time.time() - silence_start_time >= self.silence_duration:
                            # Silence duration reached, stop recording
                            logger.debug("Silence timeout reached, stopping recording automatically")
                            self.is_recording = False
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
        """Calculate the RMS (Root Mean Square) audio level"""
        try:
            import struct
            import math
            
            # Convert bytes to 16-bit integers
            samples = struct.unpack(f'{len(audio_data)//2}h', audio_data)
            
            # Calculate RMS
            if samples:
                rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))
                # Normalize to 0-1 range (16-bit audio has range -32768 to 32767)
                normalized_rms = rms / 32768.0
                

                    
                return normalized_rms
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating audio level: {e}")
            return 0.0
    
    def audio_level_to_db(self, audio_level: float) -> float:
        """Convert normalized audio level to dB"""
        try:
            import math
            if audio_level > 0:
                # Convert to dB (reference: 1.0 = 0 dB)
                db = 20 * math.log10(audio_level)
                return max(-60, db)  # Clamp to -60 dB minimum
            return -60.0
        except Exception as e:
            logger.error(f"Error converting to dB: {e}")
            return -60.0
    
    def get_current_audio_level(self) -> float:
        """Get the current audio level (for debugging)"""
        return self.last_audio_level
    

    
    def set_audio_gate_enabled(self, enabled: bool):
        """Enable or disable audio gate detection"""
        if enabled:
            self.silence_threshold = 0.005  # Restore normal threshold
        else:
            self.silence_threshold = 0.0    # Disable by setting threshold to 0
        logger.debug(f"Audio gate {'enabled' if enabled else 'disabled'}")
    
    def cleanup(self):
        """Clean up PyAudio resources"""
        try:
            if self.audio:
                self.audio.terminate()
                self.audio = None
            logger.debug("PyAudio resources cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up PyAudio: {e}")
    
    def stop_recording(self) -> Optional[str]:
        """Stop audio recording and return the audio file path"""
        if not self.is_recording:
            logger.warning("No recording in progress")
            return None
            
        try:
            self.is_recording = False
            
            # Wait for recording thread to finish
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=2.0)
            
            self.recording_stopped.emit()
            
            if not self.frames:
                logger.warning("No audio frames recorded")
                return None
            
            # Create audio folder if it doesn't exist
            audio_folder = os.path.join(os.getcwd(), "User_history", "audio")
            os.makedirs(audio_folder, exist_ok=True)
            
            # Generate timestamped filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_input_{timestamp}.wav"
            audio_file_path = os.path.join(audio_folder, filename)
            
            # Save audio to WAV file
            with wave.open(audio_file_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(16000)
                wf.writeframes(b''.join(self.frames))
            
            self.audio_file = audio_file_path
            logger.debug(f"Audio saved to: {self.audio_file}")
            
            return self.audio_file
            
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to stop recording: {e}")
            self.recording_error.emit(f"Failed to stop recording: {str(e)}")
            return None 
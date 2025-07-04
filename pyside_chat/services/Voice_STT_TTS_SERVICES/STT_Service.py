import os
import wave
import json
import speech_recognition as sr
from PySide6.QtCore import QObject, Signal
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

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
        try:
            import speech_recognition
            import pyaudio
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
        return self.available

    def convert_audio_to_text(self, audio_file: str):
        try:
            logger.debug(f"Converting audio file to text using {self.current_api}: {audio_file}")
            if self.current_api == "Google Speech Recognition":
                self._convert_with_google(audio_file)
            elif self.current_api == "Vosk (Offline)":
                self._convert_with_vosk(audio_file)
            else:
                self._convert_with_google(audio_file)
        except Exception as e:
            logger.error(f"STT conversion failed: {e}")
            self.error_occurred.emit(f"STT conversion failed: {str(e)}")

    def _convert_with_google(self, audio_file: str):
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio)
            logger.debug(f"Google STT result: {text}")
            self.text_received.emit(text)
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
            self.error_occurred.emit("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            logger.error(f"Google Speech Recognition request failed: {e}")
            if self.vosk_model:
                logger.info("Falling back to Vosk for offline recognition")
                self._convert_with_vosk(audio_file)
            else:
                self.error_occurred.emit(f"Speech recognition failed: {str(e)}")
        except Exception as e:
            logger.error(f"Google STT failed: {e}")
            self.error_occurred.emit(f"Speech recognition failed: {str(e)}")

    def _convert_with_vosk(self, audio_file: str):
        try:
            if not self.vosk_model:
                raise Exception("Vosk model not available")
            from vosk import KaldiRecognizer
            wf = wave.open(audio_file, "rb")
            rec = KaldiRecognizer(self.vosk_model, wf.getframerate())
            rec.SetWords(True)
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get('text'):
                        results.append(result['text'])
            final_result = json.loads(rec.FinalResult())
            if final_result.get('text'):
                results.append(final_result['text'])
            wf.close()
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
        logger.debug(f"STT API updated to: {api_name}")
        self.current_api = api_name

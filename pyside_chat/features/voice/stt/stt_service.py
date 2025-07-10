import os
import wave
import json
from PySide6.QtCore import QObject, Signal
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class STTService(QObject):
    """Speech-to-Text service for converting voice to text"""
    # Signals
    text_received = Signal(str)  # Emitted when text is successfully converted
    error_occurred = Signal(str) # Emitted when conversion fails

    def __init__(self):
        super().__init__()
        self.current_api = "Vosk"
        self.vosk_model = None
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        try:
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
                self._convert_with_vosk(audio_file)
        except Exception as e:
            logger.error(f"STT conversion failed: {e}")
            self.error_occurred.emit(f"STT conversion failed: {str(e)}")

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
                logger.debug(f"Vosk STT result: {text}", print_to_terminal=True)
                self.text_received.emit(text)
            else:
                logger.warning("Vosk could not understand audio", print_to_terminal=True)
                self.error_occurred.emit("Could not understand audio. Please try again.")
        except Exception as e:
            print(f"\n❌ STT ERROR: {e}\n")
            logger.error(f"Vosk STT failed: {e}", print_to_terminal=True)
            self.error_occurred.emit(f"Offline speech recognition failed: {str(e)}")

    def update_api(self, api_name: str):
        logger.debug(f"STT API updated to: {api_name}")
        self.current_api = api_name

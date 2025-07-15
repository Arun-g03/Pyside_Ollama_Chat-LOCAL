# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *

"""
StreamingAudioWorker - split from coqui_tts.py
"""
import numpy as np
from typing import List, Optional

logger = CustomLogger.get_logger(__name__)


class StreamingAudioWorker(QObject):
    """Worker for streaming audio generation in a separate thread"""
    audio_chunk_ready = Signal(object)  # Emit audio chunk (numpy array)
    progress_updated = Signal(int)  # Progress percentage
    streaming_finished = Signal()  # Signal when generation is complete
    streaming_error = Signal(str)  # Signal when error occurs

    def __init__(self, text: str, tts_service):
        super().__init__()
        self.text = text
        self.tts_service = tts_service
        self.is_running = True
        logger.debug(
            f"StreamingAudioWorker initialized with text: {text[:50]}...")

    def run(self):
        try:
            logger.debug("Starting streaming audio generation")
            sentences = self._split_text_into_sentences(self.text)
            total_sentences = len(sentences)
            logger.debug(f"Split text into {total_sentences} sentences")

            for i, sentence in enumerate(sentences):
                if not self.is_running:
                    logger.debug("Worker stopped, breaking generation loop")
                    break

                logger.debug(
                    f"Generating audio for sentence {i+1}/{total_sentences}: {sentence[:30]}...")
                audio_chunk = self._generate_audio_chunk(sentence)

                if audio_chunk is not None:
                    logger.debug(
                        f"Generated audio chunk: shape={audio_chunk.shape}, dtype={audio_chunk.dtype}, max={np.max(audio_chunk)}, min={np.min(audio_chunk)}")
                    self.audio_chunk_ready.emit(audio_chunk)
                    progress = int((i + 1) / total_sentences * 100)
                    self.progress_updated.emit(progress)
                    logger.debug(
                        f"Emitted audio chunk {i+1}/{total_sentences} (progress: {progress}%)")
                else:
                    logger.warning(
                        f"Failed to generate audio for sentence {i+1}: {sentence[:30]}...")

                time.sleep(0.1)

            if self.is_running:
                logger.debug(
                    "Streaming audio generation completed successfully")
                self.streaming_finished.emit()
            else:
                logger.debug("Streaming audio generation stopped by user")

        except Exception as e:
            logger.error(f"Error in streaming audio generation: {e}")
            import traceback
            logger.error(
                f"Streaming audio generation error traceback: {traceback.format_exc()}")
            self.streaming_error.emit(
                f"Streaming audio generation failed: {str(e)}")

    def _split_text_into_sentences(self, text: str) -> List[str]:
        import re
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            sentences = [text]
        max_chars = 200
        split_sentences = []
        for sentence in sentences:
            if len(sentence) > max_chars:
                parts = re.split(r'[,;:]', sentence)
                for part in parts:
                    if part.strip():
                        split_sentences.append(part.strip())
            else:
                split_sentences.append(sentence)
        logger.debug(f"Split text into {len(split_sentences)} sentences")
        return split_sentences

    def _generate_audio_chunk(self, text: str) -> Optional[np.ndarray]:
        try:
            if not text.strip():
                logger.debug("Empty text, skipping audio generation")
                return None

            logger.debug(f"Generating audio for text: {text[:50]}...")

            if self.tts_service.available_voices and self.tts_service.current_voice:
                logger.debug(
                    f"Generating audio with voice: {self.tts_service.current_voice}")
                audio = self.tts_service.tts_model.tts(
                    text=text,
                    speaker=self.tts_service.current_voice
                )
            else:
                logger.debug("Generating audio with single-speaker model")
                audio = self.tts_service.tts_model.tts(text=text)

            if isinstance(audio, list):
                audio = np.array(audio)
                logger.debug(
                    f"Converted list audio to numpy array: shape={audio.shape}")

            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
                logger.debug("Converted audio to float32")

            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio)) * 0.7
                logger.debug("Normalized audio")

            if self.tts_service.speech_speed != 1.0:
                logger.debug(
                    f"Adjusting audio speed to {self.tts_service.speech_speed}")
                audio = self._adjust_audio_speed(audio)

            logger.debug(
                f"Generated audio chunk: shape={audio.shape}, max={np.max(audio)}, min={np.min(audio)}")
            return audio

        except Exception as e:
            logger.error(f"Failed to generate audio chunk: {e}")
            import traceback
            logger.error(
                f"Audio generation error traceback: {traceback.format_exc()}")
            return None

    def _adjust_audio_speed(self, audio: np.ndarray) -> np.ndarray:
        try:
            from scipy import signal
            if self.tts_service.speech_speed > 1.0:
                new_length = int(len(audio) / self.tts_service.speech_speed)
                audio = signal.resample(audio, new_length)
                logger.debug(
                    f"Sped up audio: {len(audio)} -> {new_length} samples")
            elif self.tts_service.speech_speed < 1.0:
                new_length = int(len(audio) / self.tts_service.speech_speed)
                audio = signal.resample(audio, new_length)
                logger.debug(
                    f"Slowed down audio: {len(audio)} -> {new_length} samples")
            return audio
        except ImportError:
            logger.warning("scipy not available, skipping speed adjustment")
            return audio
        except Exception as e:
            logger.error(f"Failed to adjust audio speed: {e}")
            return audio

    def stop(self):
        logger.debug("Stopping streaming audio worker")
        self.is_running = False

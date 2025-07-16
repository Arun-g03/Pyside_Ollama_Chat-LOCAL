"""
Consolidated Streaming Audio

Combines streaming audio player and worker functionality into a single file
for simplified TTS streaming operations.
"""

from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.audio_imports import *
import numpy as np
import threading
import re
from typing import List, Optional

logger = CustomLogger.get_logger(__name__)


class StreamingAudioPlayer(QThread):
    """Thread for streaming audio playback"""
    audio_chunk_ready = Signal(bytes)
    playback_finished = Signal()
    playback_error = Signal(str)
    audio_level_changed = Signal(float)
    eq_bars_changed = Signal(list)
    player_started = Signal()

    def __init__(self, sample_rate=22050, channels=1, chunk_size=512):
        super().__init__()
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_queue = []
        self.is_playing = False
        self.should_stop = False
        self.volume = 0.5
        self.current_audio_level = 0.0
        self.audio_level_buffer = []
        self.pyaudio = None
        self.stream = None
        self._cleaned_up = False

    def __del__(self):
        if not self._cleaned_up:
            logger.debug("StreamingAudioPlayer destructor called - cleaning up")
            self.cleanup()

    def run(self):
        """Main playback loop"""
        try:
            logger.debug("Starting streaming audio player")

            # Initialize PyAudio
            if not self.pyaudio:
                self.pyaudio = pyaudio.PyAudio()

            # Open audio stream
            self.stream = self.pyaudio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.chunk_size
            )

            self.is_playing = True
            self.player_started.emit()

            # Main playback loop
            while self.is_playing and not self.should_stop:
                try:
                    if self.audio_queue:
                        audio_data = self.audio_queue.pop(0)
                        if audio_data is not None:
                            processed_audio = self._process_audio_chunk(audio_data)
                            self.stream.write(processed_audio.tobytes())
                        else:
                            break
                    else:
                        time.sleep(0.01)
                except Exception as e:
                    logger.error(f"Error in audio playback loop: {e}")
                    self.playback_error.emit(f"Audio playback error: {str(e)}")
                    break

            self.is_playing = False
            self.playback_finished.emit()

        except Exception as e:
            logger.error(f"Streaming audio playback error: {e}")
            self.playback_error.emit(str(e))
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()

    def _process_audio_chunk(self, audio_chunk: np.ndarray) -> np.ndarray:
        """Process audio chunk with volume and EQ calculation"""
        try:
            if audio_chunk is None or len(audio_chunk) == 0:
                return np.array([], dtype=np.float32)

            # Convert to float32 if needed
            if audio_chunk.dtype != np.float32:
                audio_chunk = audio_chunk.astype(np.float32)

            # Normalize audio
            if np.max(np.abs(audio_chunk)) > 0:
                audio_chunk = audio_chunk / np.max(np.abs(audio_chunk)) * 0.8

            # Apply volume
            audio_chunk = audio_chunk * self.volume
            audio_chunk = np.clip(audio_chunk, -1.0, 1.0)

            # Calculate EQ bars
            eq_bars = self._calculate_eq_bars(audio_chunk)
            try:
                self.eq_bars_changed.emit(eq_bars)
            except Exception:
                pass

            # Calculate audio level
            rms_level = np.sqrt(np.mean(audio_chunk**2))
            peak_level = np.max(np.abs(audio_chunk))
            combined_level = (rms_level * 0.4 + peak_level * 0.6)
            amplified_level = combined_level * 4.0

            self.current_audio_level = amplified_level
            self.audio_level_buffer.append(amplified_level)

            if len(self.audio_level_buffer) > 5:
                self.audio_level_buffer.pop(0)

            if self.audio_level_buffer:
                avg_level = sum(self.audio_level_buffer) / len(self.audio_level_buffer)
                smoothed_level = avg_level * 0.8 + amplified_level * 0.2
                try:
                    self.audio_level_changed.emit(smoothed_level)
                except Exception:
                    pass

            return audio_chunk

        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            return np.array([], dtype=np.float32)

    def _calculate_eq_bars(self, chunk, num_bars=24):
        """Calculate EQ bars for visualization"""
        try:
            fft = np.fft.rfft(chunk, n=2048)
            mag = np.abs(fft)
            freqs = np.fft.rfftfreq(2048, 1/self.sample_rate)
            band_edges = np.logspace(np.log10(20), np.log10(self.sample_rate/2), num_bars+1)
            
            bar_vals = []
            for i in range(num_bars):
                idx = np.where((freqs >= band_edges[i]) & (freqs < band_edges[i+1]))[0]
                if len(idx) > 0:
                    energy = float(np.sqrt(np.mean(mag[idx]**2)))
                    bar_vals.append(energy)
                else:
                    bar_vals.append(0.0)
            
            max_val = max(bar_vals) or 1.0
            bar_vals = [0.1 + 0.9 * (v / max_val) for v in bar_vals]
            return bar_vals
        except Exception as e:
            logger.error(f"Error calculating EQ bars: {e}")
            return [0.0] * num_bars

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))

    def add_audio_chunk(self, audio_chunk: np.ndarray):
        if self.is_playing:
            self.audio_queue.append(audio_chunk)

    def end_stream(self):
        self.audio_queue.append(None)

    def stop_playback(self):
        self.should_stop = True
        self.is_playing = False
        self.audio_queue.clear()

    def cleanup(self):
        try:
            self.stop_playback()
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.pyaudio:
                self.pyaudio.terminate()
            self._cleaned_up = True
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")


class StreamingAudioWorker(QObject):
    """Worker for streaming audio generation"""
    audio_chunk_ready = Signal(object)
    progress_updated = Signal(int)
    streaming_finished = Signal()
    streaming_error = Signal(str)

    def __init__(self, text: str, tts_service):
        super().__init__()
        self.text = text
        self.tts_service = tts_service
        self.is_running = True

    def run(self):
        try:
            logger.debug("Starting streaming audio generation")
            sentences = self._split_text_into_sentences(self.text)
            total_sentences = len(sentences)

            for i, sentence in enumerate(sentences):
                if not self.is_running:
                    break

                audio_chunk = self._generate_audio_chunk(sentence)
                if audio_chunk is not None:
                    self.audio_chunk_ready.emit(audio_chunk)
                    progress = int((i + 1) / total_sentences * 100)
                    self.progress_updated.emit(progress)

                time.sleep(0.1)

            if self.is_running:
                self.streaming_finished.emit()

        except Exception as e:
            logger.error(f"Error in streaming audio generation: {e}")
            self.streaming_error.emit(f"Streaming audio generation failed: {str(e)}")

    def _split_text_into_sentences(self, text: str) -> List[str]:
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
        return split_sentences

    def _generate_audio_chunk(self, text: str) -> Optional[np.ndarray]:
        try:
            if not text.strip():
                return None

            if self.tts_service.available_voices and self.tts_service.current_voice:
                audio = self.tts_service.tts_model.tts(
                    text=text,
                    speaker=self.tts_service.current_voice
                )
            else:
                audio = self.tts_service.tts_model.tts(text=text)

            if isinstance(audio, list):
                audio = np.array(audio)

            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)

            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio)) * 0.7

            if self.tts_service.speech_speed != 1.0:
                audio = self._adjust_audio_speed(audio)

            return audio

        except Exception as e:
            logger.error(f"Failed to generate audio chunk: {e}")
            return None

    def _adjust_audio_speed(self, audio: np.ndarray) -> np.ndarray:
        try:
            from scipy import signal
            if self.tts_service.speech_speed != 1.0:
                new_length = int(len(audio) / self.tts_service.speech_speed)
                audio = signal.resample(audio, new_length)
            return audio
        except ImportError:
            logger.warning("scipy not available, skipping speed adjustment")
            return audio
        except Exception as e:
            logger.error(f"Failed to adjust audio speed: {e}")
            return audio

    def stop(self):
        self.is_running = False 
"""
Coqui TTS Service Module

Provides advanced Text-to-Speech functionality using Coqui TTS library.
Features include:
- Multiple voice models and speakers
- Emotion control and voice cloning
- Local processing (no internet required)
- High-quality audio output
- Streaming synthesis for real-time playback
"""

import os
import tempfile
import threading
import time
import json
import numpy as np
import io
import wave
from typing import List, Dict, Optional, Tuple, Generator
from PySide6.QtCore import QObject, Signal, QTimer, QThread
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import pyaudio

from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class StreamingAudioPlayer(QThread):
    """Thread for streaming audio playback"""
    
    audio_chunk_ready = Signal(bytes)
    playback_finished = Signal()
    playback_error = Signal(str)
    audio_level_changed = Signal(float)  # Emit audio level for EQ visualization
    
    def __init__(self, sample_rate=22050, channels=1, chunk_size=512):
        super().__init__()
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_queue = []
        self.is_playing = False
        self.should_stop = False
        self.volume = 0.5  # Volume control (0.0 to 1.0)
        self.last_audio_level_time = 0  # For throttling audio level emissions
        
        # PyAudio setup
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        
    def run(self):
        """Main playback loop"""
        try:
            self.stream = self.pyaudio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.chunk_size
            )
            
            self.is_playing = True
            
            while self.is_playing and not self.should_stop:
                if self.audio_queue:
                    audio_data = self.audio_queue.pop(0)
                    if audio_data is not None:  # None signals end of stream
                        # Process audio data before playback
                        processed_audio = self._process_audio_chunk(audio_data)
                        self.stream.write(processed_audio.tobytes())
                    else:
                        break
                else:
                    time.sleep(0.01)  # Small delay to prevent busy waiting
            
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
        """Process audio chunk for better quality"""
        try:
            # Ensure audio is float32 and in the correct range
            if audio_chunk.dtype != np.float32:
                audio_chunk = audio_chunk.astype(np.float32)
            
            # Normalize audio to prevent clipping
            if np.max(np.abs(audio_chunk)) > 0:
                audio_chunk = audio_chunk / np.max(np.abs(audio_chunk)) * 0.8
            
            # Apply volume control
            audio_chunk = audio_chunk * self.volume
            
            # Ensure values are in valid range
            audio_chunk = np.clip(audio_chunk, -1.0, 1.0)
            
            # Calculate audio level for EQ visualization with more granular updates
            # Process smaller chunks for more frequent analysis
            chunk_size = len(audio_chunk)
            segment_size = max(1, chunk_size // 16)  # Split into 16 smaller segments for much more frequent updates
            
            print(f"[TTS DEBUG] Processing chunk size: {chunk_size}, segment size: {segment_size}")
            
            for i in range(0, chunk_size, segment_size):
                segment = audio_chunk[i:i + segment_size]
                if len(segment) > 0:
                    # Calculate multiple audio level metrics for better wave analysis
                    rms_level = np.sqrt(np.mean(segment**2))  # RMS level
                    peak_level = np.max(np.abs(segment))  # Peak level
                    # Combine RMS and peak for more complete wave representation
                    combined_level = (rms_level * 0.7 + peak_level * 0.3)
                    
                    # Amplify the audio level for better EQ visualization
                    # Use much smaller amplification to get reasonable values
                    amplified_level = combined_level * 2.0  # Reduced amplification
                    
                    #print(f"[TTS DEBUG] Segment {i//segment_size}: RMS={rms_level:.4f}, Peak={peak_level:.4f}, Combined={combined_level:.4f}, Amplified={amplified_level:.4f}")
                    
                    # Emit audio level for EQ visualization
                    self.audio_level_changed.emit(amplified_level)
                    
                    # Throttle updates to prevent overwhelming the UI
                    current_time = time.time()
                    if current_time - self.last_audio_level_time >= 0.01:  # 100 FPS for TTS
                        self.last_audio_level_time = current_time
                    else:
                        # Small delay to prevent overwhelming
                        time.sleep(0.001)
            
            return audio_chunk
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            return audio_chunk
    
    def set_volume(self, volume: float):
        """Set playback volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
    
    def add_audio_chunk(self, audio_chunk: np.ndarray):
        """Add audio chunk to playback queue"""
        if self.is_playing:
            self.audio_queue.append(audio_chunk)
    
    def end_stream(self):
        """Signal end of audio stream"""
        if self.is_playing:
            self.audio_queue.append(None)
    
    def stop_playback(self):
        """Stop playback immediately"""
        self.should_stop = True
        self.is_playing = False
        if self.stream:
            self.stream.stop_stream()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_playback()
        if self.pyaudio:
            self.pyaudio.terminate()


class CoquiTTSService(QObject):
    """Advanced TTS service using Coqui TTS library with streaming support"""
    
    # Signals
    tts_started = Signal()
    tts_finished = Signal()
    tts_error = Signal(str)
    model_loaded = Signal(str)
    voices_loaded = Signal(list)
    streaming_progress = Signal(int)  # Progress percentage for streaming
    audio_level_changed = Signal(float)  # Audio level for EQ visualization
    
    def __init__(self):
        super().__init__()
        self.available = False
        self.tts_model = None
        self.current_model = None
        self.available_voices = []
        self.current_voice = None
        self.speech_speed = 1.0
        self.audio_output = None
        self.media_player = None
        self.current_audio_file = None
        
        # Streaming support
        self.streaming_player = None
        self.is_streaming = False
        self.streaming_thread = None
        
        # Initialize the service
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize the Coqui TTS service"""
        try:
            from TTS.api import TTS
            self.available = True
            logger.info("Coqui TTS service initialized successfully")
            self._load_default_model()
        except ImportError as e:
            logger.error(f"Coqui TTS not available: {e}")
            self.available = False
        except Exception as e:
            logger.error(f"Failed to initialize Coqui TTS: {e}")
            self.available = False
    
    def _load_default_model(self):
        """Load the default TTS model"""
        try:
            from TTS.api import TTS
            
            # Try to load a default model
            default_models = [
                "tts_models/en/ljspeech/tacotron2-DDC",
                "tts_models/en/ljspeech/glow-tts",
                "tts_models/en/vctk/vits"
            ]
            
            for model_name in default_models:
                try:
                    self.tts_model = TTS(model_name=model_name)
                    self.current_model = model_name
                    logger.info(f"Loaded Coqui TTS model: {model_name}")
                    self.model_loaded.emit(model_name)
                    self._load_available_voices()
                    return
                except Exception as e:
                    logger.warning(f"Failed to load model {model_name}: {e}")
                    continue
            
            logger.error("No Coqui TTS models could be loaded")
            self.available = False
            
        except Exception as e:
            logger.error(f"Failed to load default model: {e}")
            self.available = False
    
    def _load_available_voices(self):
        """Load available voices for the current model"""
        try:
            if self.tts_model and hasattr(self.tts_model, 'list_voices'):
                self.available_voices = self.tts_model.list_voices()
                if self.available_voices:
                    self.current_voice = self.available_voices[0]
                    logger.info(f"Loaded {len(self.available_voices)} voices")
                    self.voices_loaded.emit(self.available_voices)
                else:
                    logger.warning("No voices available for current model")
            else:
                logger.info("Current model doesn't support multiple voices")
        except Exception as e:
            logger.error(f"Failed to load voices: {e}")
    
    def is_available(self) -> bool:
        """Check if Coqui TTS is available"""
        return self.available and self.tts_model is not None
    
    def _get_tts_model_cache_dirs(self):
        import os, sys
        cache_dirs = []
        # 1. Environment variable (TTS_HOME)
        tts_home = os.environ.get('TTS_HOME')
        if tts_home:
            cache_dirs.append(tts_home)
        # 2. Windows default
        if sys.platform == 'win32':
            local_appdata = os.environ.get('LOCALAPPDATA')
            if local_appdata:
                cache_dirs.append(os.path.join(local_appdata, 'tts'))
        # 3. macOS default
        if sys.platform == 'darwin':
            cache_dirs.append(os.path.expanduser('~/Library/Application Support/tts'))
        # 4. Linux default
        cache_dirs.append(os.path.expanduser('~/.local/share/tts'))
        cache_dirs.append(os.path.expanduser('~/.cache/tts'))
        # 5. Fallback
        cache_dirs.append(os.path.expanduser('~/tts_models'))
        return cache_dirs

    def _model_name_to_folder(self, model_name: str) -> str:
        return model_name.replace('/', '--')

    def _is_model_fully_downloaded(self, model_name: str) -> bool:
        import os
        folder = self._model_name_to_folder(model_name)
        for base_dir in self._get_tts_model_cache_dirs():
            model_dir = os.path.join(base_dir, folder)
            config_path = os.path.join(model_dir, "config.json")
            has_weights = False
            if os.path.exists(model_dir):
                for f in os.listdir(model_dir):
                    if f.endswith(".pth"):
                        has_weights = True
                        break
            if os.path.exists(config_path) and has_weights:
                return True
        return False

    def get_downloaded_models(self) -> list:
        import os
        downloaded = set()
        for base_dir in self._get_tts_model_cache_dirs():
            if os.path.exists(base_dir):
                for item in os.listdir(base_dir):
                    item_path = os.path.join(base_dir, item)
                    if os.path.isdir(item_path):
                        config_path = os.path.join(item_path, "config.json")
                        has_weights = any(f.endswith(".pth") for f in os.listdir(item_path))
                        if os.path.exists(config_path) and has_weights:
                            # Convert folder name back to model name for UI
                            downloaded.add(item.replace('--', '/'))
        return list(downloaded)

    def is_model_downloaded(self, model_name: str) -> bool:
        return self._is_model_fully_downloaded(model_name)

    def get_available_voices(self) -> list:
        # After loading a model, list available speakers (if multi-speaker)
        if self.tts_model and hasattr(self.tts_model, 'list_voices'):
            try:
                return self.tts_model.list_voices()
            except Exception:
                return []
        return []

    def download_model(self, model_name: str) -> bool:
        # Use TTS API to download model, robust to already-downloaded
        try:
            from TTS.api import TTS
            folder = self._model_name_to_folder(model_name)
            # Check if already downloaded
            if self._is_model_fully_downloaded(model_name):
                logger.info(f"Model {model_name} already downloaded.")
                return True
            logger.info(f"Downloading Coqui TTS model: {model_name}")
            TTS(model_name=model_name)
            logger.info(f"Successfully downloaded model: {model_name}")
            return self._is_model_fully_downloaded(model_name)
        except Exception as e:
            logger.error(f"Failed to download model {model_name}: {e}")
            return False
    
    def set_voice(self, voice_name: str) -> bool:
        """Set the current voice"""
        if voice_name in self.available_voices:
            self.current_voice = voice_name
            logger.info(f"Set Coqui TTS voice to: {voice_name}")
            return True
        else:
            logger.warning(f"Voice {voice_name} not available")
            return False
    
    def set_speed(self, speed: float):
        """Set speech speed (0.5 to 2.0)"""
        self.speech_speed = max(0.5, min(2.0, speed))
        logger.info(f"Set Coqui TTS speed to: {self.speech_speed}x")
    
    def set_streaming_volume(self, volume: float):
        """Set streaming audio volume (0.0 to 1.0)"""
        if self.streaming_player:
            self.streaming_player.set_volume(volume)
        logger.debug(f"Streaming volume set to: {volume}")
    
    def speak_text(self, text: str, use_streaming: bool = True):
        """Convert text to speech using Coqui TTS with optional streaming"""
        if not self.is_available():
            logger.error("Coqui TTS not available")
            self.tts_error.emit("Coqui TTS not available")
            return
        
        try:
            logger.debug(f"Converting text to speech with Coqui TTS: {text[:50]}...")
            self.tts_started.emit()
            
            if use_streaming:
                self._speak_text_streaming(text)
            else:
                # Use the original non-streaming method
                audio_file = self._generate_audio(text)
                if audio_file and os.path.exists(audio_file):
                    self._play_audio(audio_file, text)
                else:
                    logger.error("Failed to generate audio file")
                    self.tts_error.emit("Failed to generate audio")
                    
        except Exception as e:
            logger.error(f"Coqui TTS conversion failed: {e}")
            self.tts_error.emit(f"Coqui TTS conversion failed: {str(e)}")
    
    def _speak_text_streaming(self, text: str):
        """Convert text to speech using streaming synthesis"""
        try:
            # Stop any existing playback
            self.stop_playback()
            
            # Initialize streaming player
            self.streaming_player = StreamingAudioPlayer()
            self.streaming_player.playback_finished.connect(self._on_streaming_finished)
            self.streaming_player.playback_error.connect(self._on_streaming_error)
            self.streaming_player.audio_level_changed.connect(self.audio_level_changed.emit)
            
            # Set volume to a reasonable level (0.5 = 50%)
            self.streaming_player.set_volume(0.5)
            
            # Start streaming in a separate thread
            self.streaming_thread = threading.Thread(
                target=self._generate_and_stream_audio,
                args=(text,),
                daemon=True
            )
            self.streaming_thread.start()
            
            # Start the audio player
            self.streaming_player.start()
            self.is_streaming = True
            
            logger.debug("Started streaming TTS synthesis")
            
        except Exception as e:
            logger.error(f"Failed to start streaming TTS: {e}")
            self.tts_error.emit(f"Failed to start streaming TTS: {str(e)}")
    
    def _generate_and_stream_audio(self, text: str):
        """Generate audio in chunks and stream to player"""
        try:
            # Split text into sentences for chunked processing
            sentences = self._split_text_into_sentences(text)
            total_sentences = len(sentences)
            
            for i, sentence in enumerate(sentences):
                if not self.is_streaming:
                    break
                
                # Generate audio for this sentence
                audio_chunk = self._generate_audio_chunk(sentence)
                if audio_chunk is not None:
                    # Add to player queue
                    self.streaming_player.add_audio_chunk(audio_chunk)
                    
                    # Update progress
                    progress = int((i + 1) / total_sentences * 100)
                    self.streaming_progress.emit(progress)
                
                # Small delay between sentences for smoother streaming
                time.sleep(0.1)
            
            # Signal end of stream
            if self.is_streaming:
                self.streaming_player.end_stream()
                
        except Exception as e:
            logger.error(f"Error in streaming audio generation: {e}")
            self.tts_error.emit(f"Streaming audio generation failed: {str(e)}")
    
    def _split_text_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for chunked processing"""
        import re
        
        # Simple sentence splitting - can be improved with NLP libraries
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # If no sentences found, treat the whole text as one sentence
        if not sentences:
            sentences = [text]
        
        # Limit sentence length to prevent very long chunks
        max_chars = 200
        split_sentences = []
        for sentence in sentences:
            if len(sentence) > max_chars:
                # Split long sentences by commas or natural breaks
                parts = re.split(r'[,;:]', sentence)
                for part in parts:
                    if part.strip():
                        split_sentences.append(part.strip())
            else:
                split_sentences.append(sentence)
        
        return split_sentences
    
    def _generate_audio_chunk(self, text: str) -> Optional[np.ndarray]:
        """Generate audio chunk for a piece of text"""
        try:
            if not text.strip():
                return None
            
            # Generate audio using TTS model
            if self.available_voices and self.current_voice:
                # Multi-speaker model - use the selected voice
                logger.debug(f"Generating audio with voice: {self.current_voice}")
                audio = self.tts_model.tts(
                    text=text,
                    speaker=self.current_voice
                )
            else:
                # Single-speaker model
                logger.debug("Generating audio with single-speaker model")
                audio = self.tts_model.tts(text=text)
            
            # Convert to numpy array if needed
            if isinstance(audio, list):
                audio = np.array(audio)
            
            # Ensure audio is float32
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            
            # Normalize audio to prevent clipping
            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio)) * 0.7  # Reduce volume to 70%
            
            # Apply speed adjustment if needed
            if self.speech_speed != 1.0:
                audio = self._adjust_audio_speed(audio)
            
            return audio
            
        except Exception as e:
            logger.error(f"Failed to generate audio chunk: {e}")
            return None
    
    def _adjust_audio_speed(self, audio: np.ndarray) -> np.ndarray:
        """Adjust audio speed using simple resampling"""
        try:
            from scipy import signal
            
            # Simple speed adjustment using resampling
            if self.speech_speed > 1.0:
                # Speed up: downsample
                new_length = int(len(audio) / self.speech_speed)
                audio = signal.resample(audio, new_length)
            elif self.speech_speed < 1.0:
                # Slow down: upsample
                new_length = int(len(audio) / self.speech_speed)
                audio = signal.resample(audio, new_length)
            
            return audio
            
        except ImportError:
            logger.warning("scipy not available, skipping speed adjustment")
            return audio
        except Exception as e:
            logger.error(f"Failed to adjust audio speed: {e}")
            return audio
    
    def _on_streaming_finished(self):
        """Handle streaming playback finished"""
        self.is_streaming = False
        self.tts_finished.emit()
        logger.debug("Streaming TTS playback finished")
    
    def _on_streaming_error(self, error: str):
        """Handle streaming playback error"""
        self.is_streaming = False
        self.tts_error.emit(f"Streaming playback error: {error}")
        logger.error(f"Streaming TTS error: {error}")
    
    def stop_playback(self):
        """Stop current TTS playback (both streaming and non-streaming)"""
        # Stop streaming playback
        if self.is_streaming and self.streaming_player:
            self.is_streaming = False
            self.streaming_player.stop_playback()
            if self.streaming_player.isRunning():
                self.streaming_player.quit()
                self.streaming_player.wait()
        
        # Stop non-streaming playback
        if self.media_player:
            self.media_player.stop()
        
        self.tts_finished.emit()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_playback()
        
        if self.streaming_player:
            self.streaming_player.cleanup()
            self.streaming_player = None

    def get_model_info(self, model_name: str) -> Dict[str, str]:
        """Get information about a specific model without downloading it"""
        info = {
            "name": model_name,
            "downloaded": self.is_model_downloaded(model_name),
            "size": self.get_model_download_size(model_name),
            "type": "unknown"
        }
        
        # Determine model type based on name
        if "vits" in model_name.lower():
            info["type"] = "VITS"
            if "vctk" in model_name.lower():
                info["description"] = "Multi-speaker VITS model with high quality"
            else:
                info["description"] = "Single-speaker VITS model with good quality"
        elif "tacotron" in model_name.lower():
            info["type"] = "Tacotron2"
            info["description"] = "Classic TTS model with good quality"
        elif "glow" in model_name.lower():
            info["type"] = "Glow-TTS"
            info["description"] = "Fast and efficient TTS model"
        elif "fast_pitch" in model_name.lower():
            info["type"] = "FastPitch"
            info["description"] = "Fast pitch-controlled TTS model"
        elif "speedy_speech" in model_name.lower():
            info["type"] = "SpeedySpeech"
            info["description"] = "Very fast TTS model"
        elif "your_tts" in model_name.lower():
            info["type"] = "YourTTS"
            info["description"] = "Advanced multi-speaker model with voice cloning"
        elif "xtts" in model_name.lower():
            info["type"] = "XTTS"
            info["description"] = "Advanced multi-language model with voice cloning"
        else:
            info["type"] = "Unknown"
            info["description"] = "TTS model"
        
        return info
    
    def get_model_download_size(self, model_name: str) -> str:
        """Get estimated download size for a model"""
        # More accurate size estimates based on model types
        if "vits" in model_name.lower():
            if "vctk" in model_name.lower():
                return "~150-200 MB"  # Multi-speaker VITS models are larger
            else:
                return "~50-100 MB"
        elif "tacotron" in model_name.lower():
            return "~200-300 MB"
        elif "glow" in model_name.lower():
            return "~100-150 MB"
        elif "fast_pitch" in model_name.lower():
            return "~80-120 MB"
        elif "speedy_speech" in model_name.lower():
            return "~60-100 MB"
        elif "your_tts" in model_name.lower():
            return "~200-300 MB"
        elif "xtts" in model_name.lower():
            return "~500-800 MB"  # XTTS models are very large
        elif "coqui_studio" in model_name.lower():
            return "~100-200 MB"
        else:
            return "~50-200 MB"
    
    def get_comprehensive_model_list(self) -> List[str]:
        """Get a comprehensive list of available models for download"""
        # This is a curated list of popular and well-maintained models
        comprehensive_models = [
            # Single-speaker models (good quality, smaller size)
            "tts_models/en/ljspeech/tacotron2-DDC",
            "tts_models/en/ljspeech/glow-tts",
            "tts_models/en/ljspeech/fast_pitch",
            "tts_models/en/ljspeech/speedy_speech",
            
            # Multi-speaker models (more voices, larger size)
            "tts_models/en/vctk/vits",
            "tts_models/en/vctk/tacotron2-DDC",
            "tts_models/en/vctk/glow-tts",
            
            # Advanced models (best quality, largest size)
            "tts_models/en/ljspeech/your_tts",
            "tts_models/en/ljspeech/xtts_v2",
            
            # Coqui Studio models (if available)
            "tts_models/en/ljspeech/coqui_studio",
            "tts_models/en/ljspeech/coqui_studio_tts",
            "tts_models/en/ljspeech/coqui_studio_tts_v2",
            
            # Additional models for variety
            "tts_models/en/ljspeech/tacotron2-DDC_ph",
            "tts_models/en/ljspeech/glow-tts_ph",
            "tts_models/en/ljspeech/fast_pitch_ph",
            "tts_models/en/ljspeech/speedy_speech_ph"
        ]
        
        return comprehensive_models
    
    def get_current_model_info(self) -> Dict[str, str]:
        """Get information about the current loaded model"""
        if not self.current_model:
            return {}
        
        return {
            "model": self.current_model,
            "voice": self.current_voice or "default",
            "speed": str(self.speech_speed),
            "voices_available": str(len(self.available_voices))
        }

    def get_available_models(self) -> list:
        """
        Return a list of all models: downloaded first, then a curated list of popular downloadable models.
        """
        # Curated list of popular models (add more as needed)
        curated_models = [
            "tts_models/en/ljspeech/tacotron2-DDC",
            "tts_models/en/ljspeech/glow-tts",
            "tts_models/en/vctk/vits",
            "tts_models/en/ljspeech/fast_pitch",
            "tts_models/en/ljspeech/speedy_speech",
            "tts_models/en/ljspeech/your_tts",
            "tts_models/en/ljspeech/xtts_v2",
        ]
        downloaded = self.get_downloaded_models()
        # Add curated models not already downloaded
        all_models = list(downloaded)
        for model in curated_models:
            if model not in all_models:
                all_models.append(model)
        return all_models 

    def load_model(self, model_name: str) -> bool:
        """
        Load a specific TTS model and update available voices.
        """
        try:
            # Skip vocoder models
            if model_name.startswith("vocoder_models/"):
                print(f"[DEBUG] Skipping vocoder model: {model_name}")
                return False
            from TTS.api import TTS
            print(f"[DEBUG] Loading model: {model_name}")
            self.tts_model = TTS(model_name=model_name)
            self.current_model = model_name
            # Always try to get voices
            if hasattr(self.tts_model, 'list_voices'):
                self.available_voices = self.tts_model.list_voices()
                print(f"[DEBUG] Voices for model {model_name}: {self.available_voices}")
            else:
                self.available_voices = []
                print(f"[DEBUG] Model {model_name} has no list_voices method.")

            # Fallback: try to load speakers_file from config if available_voices is empty
            if not self.available_voices and self.current_model:
                config = self.get_model_config(self.current_model)
                speakers_file = config.get('speakers_file') if config else None
                if speakers_file and os.path.exists(speakers_file):
                    try:
                        with open(speakers_file, 'r', encoding='utf-8') as f:
                            speakers = json.load(f)
                            if isinstance(speakers, dict):
                                self.available_voices = list(speakers.keys())
                            elif isinstance(speakers, list):
                                self.available_voices = speakers
                            print(f"[DEBUG] Loaded speakers from speakers_file: {self.available_voices}")
                    except Exception as e:
                        print(f"[DEBUG] Failed to load speakers_file: {e}")

            # Set default voice for multi-speaker models
            if self.available_voices:
                self.current_voice = self.available_voices[0]
                print(f"[DEBUG] Set default voice to: {self.current_voice}")
                self.voices_loaded.emit(self.available_voices)
            else:
                self.current_voice = None
                print(f"[DEBUG] No voices available, using single-speaker mode")

            print(f"[DEBUG] Speaker count for model {model_name}: {len(self.available_voices)}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            print(f"[DEBUG] Exception loading model {model_name}: {e}")
            self.tts_model = None
            self.available_voices = []
            return False

    def is_multi_speaker(self) -> bool:
        # 1. Check available_voices
        print(f"[DEBUG] Checking if model {self.current_model} is multi-speaker...")
        if hasattr(self, 'available_voices') and self.available_voices:
            print(f"[DEBUG] available_voices: {self.available_voices}")
            if len(self.available_voices) > 1:
                print(f"[DEBUG] Model {self.current_model} is multi-speaker (voices > 1)")
                return True
            # If only one, check config for speakers/num_speakers
            if self.current_model:
                config = self.get_model_config(self.current_model)
                print(f"[DEBUG] Model config for {self.current_model}: {config}")
                if config:
                    if 'speakers' in config and isinstance(config['speakers'], list) and len(config['speakers']) > 1:
                        print(f"[DEBUG] Model {self.current_model} is multi-speaker (config speakers > 1)")
                        return True
                    if config.get('num_speakers', 1) > 1:
                        print(f"[DEBUG] Model {self.current_model} is multi-speaker (config num_speakers > 1)")
                        return True
        # 2. Fallback: check config directly
        if self.current_model:
            config = self.get_model_config(self.current_model)
            print(f"[DEBUG] Model config for {self.current_model}: {config}")
            if config:
                if 'speakers' in config and isinstance(config['speakers'], list) and len(config['speakers']) > 1:
                    print(f"[DEBUG] Model {self.current_model} is multi-speaker (config speakers > 1, fallback)")
                    return True
                if config.get('num_speakers', 1) > 1:
                    print(f"[DEBUG] Model {self.current_model} is multi-speaker (config num_speakers > 1, fallback)")
                    return True
        print(f"[DEBUG] Model {self.current_model} is single-speaker.")
        return False

    def get_model_config(self, model_name: str):
        # Find config.json for the model
        folder = self._model_name_to_folder(model_name)
        for base_dir in self._get_tts_model_cache_dirs():
            model_dir = os.path.join(base_dir, folder)
            config_path = os.path.join(model_dir, "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    return None
        return None

    def _generate_audio(self, text: str) -> Optional[str]:
        """Generate audio file from text (for non-streaming mode)"""
        try:
            # Create temporary file
            temp_dir = os.path.join(os.getcwd(), "User_history", "audio")
            os.makedirs(temp_dir, exist_ok=True)
            
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coqui_tts_{timestamp}.wav"
            audio_file_path = os.path.join(temp_dir, filename)
            
            # Generate audio
            if self.available_voices and self.current_voice:
                # Multi-speaker model - use the selected voice
                logger.debug(f"Generating audio file with voice: {self.current_voice}")
                self.tts_model.tts_to_file(
                    text=text,
                    speaker=self.current_voice,
                    file_path=audio_file_path
                )
            else:
                # Single-speaker model
                logger.debug("Generating audio file with single-speaker model")
                self.tts_model.tts_to_file(
                    text=text,
                    file_path=audio_file_path
                )
            
            logger.debug(f"Generated Coqui TTS audio: {audio_file_path}")
            return audio_file_path
            
        except Exception as e:
            logger.error(f"Failed to generate Coqui TTS audio: {e}")
            return None
    
    def _play_audio(self, audio_file: str, text: str):
        """Play the generated audio file (for non-streaming mode)"""
        try:
            # Initialize media player if needed
            if not self.media_player:
                self.media_player = QMediaPlayer()
                self.audio_output = QAudioOutput()
                self.media_player.setAudioOutput(self.audio_output)
                self.media_player.mediaStatusChanged.connect(self._on_media_status_changed)
            
            # Set up audio output
            self.audio_output.setVolume(50)
            
            # Play the audio
            self.current_audio_file = audio_file
            self.media_player.setSource(QUrl.fromLocalFile(audio_file))
            self.media_player.play()
            
            # Calculate estimated duration for cleanup
            word_count = len(text.split())
            base_duration_per_word = 0.24 / self.speech_speed
            estimated_duration = max(0.5, word_count * base_duration_per_word)
            
            # Set up cleanup timer
            QTimer.singleShot(int(estimated_duration * 1000) + 3000, 
                            lambda: self._cleanup_audio_file(audio_file))
            
            logger.debug(f"Started Coqui TTS playback, estimated duration: {estimated_duration:.1f}s")
            
        except Exception as e:
            logger.error(f"Failed to play Coqui TTS audio: {e}")
            self.tts_error.emit(f"Failed to play audio: {str(e)}")
    
    def _on_media_status_changed(self, status):
        """Handle media player status changes"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.tts_finished.emit()
            self.current_audio_file = None
        elif status == QMediaPlayer.MediaStatus.InvalidMedia:
            logger.error("Invalid media file")
            self.tts_error.emit("Invalid audio file")
    
    def _cleanup_audio_file(self, file_path: str):
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up audio file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to cleanup audio file {file_path}: {e}")
    
    def refresh_model_list(self) -> List[str]:
        """Refresh the list of available models"""
        # Clear any cached model information
        downloaded_models = self.get_downloaded_models()
        available_models = self.get_comprehensive_model_list()
        
        # Combine and deduplicate
        all_models = []
        seen_models = set()
        
        # Add downloaded models first
        for model in downloaded_models:
            if model not in seen_models:
                all_models.append(model)
                seen_models.add(model)
        
        # Add available models
        for model in available_models:
            if model not in seen_models:
                all_models.append(model)
                seen_models.add(model)
        
        return all_models[:15]  # Limit to first 15 for better UX 
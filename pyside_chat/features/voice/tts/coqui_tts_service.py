# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *

from pyside_chat.core.shared_imports.audio_imports import *

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

import numpy as np
import io
import wave
from typing import List, Dict, Optional, Tuple, Generator

logger = CustomLogger.get_logger(__name__)


def safe_disconnect(signal, slot=None, logger=logger):
    try:
        if signal is not None and hasattr(signal, 'disconnect'):
            try:
                if slot is not None:
                    signal.disconnect(slot)
                    logger.debug(f"[SAFE DISCONNECT] Disconnected {slot} from {signal}")
                else:
                    signal.disconnect()
                    logger.debug(f"[SAFE DISCONNECT] Disconnected all slots from {signal}")
            except Exception as e:
                logger.debug(f"[SAFE DISCONNECT] Could not disconnect {slot} from {signal}: {e}")
        else:
            logger.debug(f"[SAFE DISCONNECT] Signal {signal} is None or has no disconnect method, skipping")
    except Exception as e:
        logger.error(f"[SAFE DISCONNECT] Exception during disconnect: {e}")


class CoquiTTSService(QObject):
    """Advanced TTS service using Coqui TTS library with streaming support
    
    Always use CoquiTTSService.get_instance() to access the singleton instance.
    Do NOT instantiate directly.
    """
    
    # Singleton instance
    _instance = None
    _initialized = False
    
    @staticmethod
    def get_instance():
        """Get the singleton instance of CoquiTTSService"""
        if CoquiTTSService._instance is None:
            CoquiTTSService._instance = CoquiTTSService()
        return CoquiTTSService._instance
    
    # Signals
    tts_started = Signal()
    tts_finished = Signal()
    tts_error = Signal(str)
    model_loaded = Signal(str)
    voices_loaded = Signal(list)
    streaming_progress = Signal(int)  # Progress percentage for streaming
    audio_level_changed = Signal(float)  # Audio level for EQ visualization
    eq_bars_changed = Signal(list)  # NEW: Emit EQ bar array for visualization
    
    def __new__(cls):
        """Singleton pattern to prevent multiple model loading"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the Coqui TTS service (singleton)"""
        if self._initialized:
            return
            
        super().__init__()
        self._initialized = True
        
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
        self._cleaned_up = False
        
        # Model caching
        self._loaded_models = {}  # Cache for loaded models
        self._model_loading_lock = threading.Lock()  # Thread safety for model loading
        
        # Initialize the service
        self._initialize_service()
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        if not self._cleaned_up:
            logger.debug("CoquiTTSService destructor called - cleaning up")
            self.cleanup()
    
    def _initialize_service(self):
        """Initialize the Coqui TTS service"""
        try:
            from TTS.api import TTS
            self.available = True
            logger.info("Coqui TTS service initialized successfully")
            
            # Check if this is a new instance or cached
            if hasattr(self, '_loaded_models') and self._loaded_models:
                logger.info(f"Using cached Coqui TTS service with {len(self._loaded_models)} cached models")
            else:
                logger.info("Initializing new Coqui TTS service instance")
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
            # Try to load a default model
            default_models = [
                "tts_models/en/ljspeech/tacotron2-DDC",
                "tts_models/en/ljspeech/glow-tts",
                "tts_models/en/vctk/vits"
            ]
            
            for model_name in default_models:
                try:
                    # Use the new load_model method which includes caching
                    if self.load_model(model_name):
                        logger.info(f"Loaded Coqui TTS model: {model_name}")
                        self.model_loaded.emit(model_name)
                        return
                except Exception as e:
                    logger.warning(f"Failed to load model {model_name}: {e}")
                    continue
            
            logger.error("No Coqui TTS models could be loaded")
            self.available = False
            # Emit error signal to notify other components
            self.tts_error.emit("No TTS models available. Voice features will be disabled.")
            
        except Exception as e:
            logger.error(f"Failed to load default model: {e}")
            self.available = False
            # Emit error signal to notify other components
            self.tts_error.emit(f"TTS initialization failed: {str(e)}")
    
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
    
    def is_initialized(self) -> bool:
        """Check if Coqui TTS service is properly initialized"""
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
        downloaded = set()
        cache_dirs = self._get_tts_model_cache_dirs()
        logger.info(f"[CoquiTTS] Checking model cache directories: {cache_dirs}")
        for base_dir in cache_dirs:
            if os.path.exists(base_dir):
                for item in os.listdir(base_dir):
                    item_path = os.path.join(base_dir, item)
                    if os.path.isdir(item_path):
                        config_path = os.path.join(item_path, "config.json")
                        has_weights = any(f.endswith(".pth") for f in os.listdir(item_path))
                        if os.path.exists(config_path) and has_weights:
                            model_name = item.replace('--', '/')
                            logger.info(f"[CoquiTTS] Found downloaded model: {model_name} in {item_path}")
                            downloaded.add(model_name)
        logger.info(f"[CoquiTTS] Downloaded models: {list(downloaded)}", print_to_terminal=True)
        return list(downloaded)

    def is_model_downloaded(self, model_name: str) -> bool:
        return self._is_model_fully_downloaded(model_name)
    
    def is_model_loaded(self, model_name: str) -> bool:
        """Check if a model is currently loaded in memory"""
        try:
            with self._model_loading_lock:
                return (model_name == self.current_model and self.tts_model is not None) or model_name in self._loaded_models
        except Exception as e:
            logger.error(f"Error checking if model is loaded: {e}")
            return False

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
        """Set the voice for TTS synthesis"""
        try:
            if not voice_name or voice_name.strip() == "":
                logger.warning("Empty voice name provided, using default")
                voice_name = "ED"  # Default voice for VCTK model
            
            if voice_name == "No speakers available":
                logger.warning("Invalid voice name 'No speakers available', using default")
                voice_name = "ED"  # Default voice for VCTK model
            
            logger.debug(f"Setting voice to: {voice_name}")
            self.current_voice = voice_name
            
            # Check if voice is available in current model
            if hasattr(self, 'available_voices') and self.available_voices:
                if voice_name not in self.available_voices:
                    logger.warning(f"Voice {voice_name} not available, using first available voice")
                    self.current_voice = self.available_voices[0] if self.available_voices else "ED"
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
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
        """Convert text to speech and play it"""
        log_thread_info("TTS speak_text called", logger)
        if not text.strip():
            logger.warning("Empty text provided to speak_text")
            return
        
        # Check if TTS is available
        if not self.is_available():
            logger.warning("TTS not available, skipping speech synthesis")
            self.tts_error.emit("TTS not available - voice features disabled")
            return
        
        # Prevent multiple simultaneous TTS operations
        if hasattr(self, '_tts_in_progress') and self._tts_in_progress:
            logger.warning("TTS already in progress, skipping new request")
            return
        
        self._tts_in_progress = True
        
        try:
            logger.debug(f"Converting text to speech with Coqui TTS: {text[:50]}...")
            
            if use_streaming:
                self._speak_text_streaming(text)
            else:
                self._generate_and_play_audio(text)
                
        except Exception as e:
            logger.error(f"Error in speak_text: {e}")
            self.tts_error.emit(str(e))
            self._tts_in_progress = False
        finally:
            # Reset the flag after a short delay to allow for cleanup

            QTimer.singleShot(100, lambda: setattr(self, '_tts_in_progress', False))
    
    def _generate_and_play_audio(self, text: str):
        """Generate audio from text and play it (non-streaming mode)"""
        try:
            audio_file = self._generate_audio(text)
            if audio_file:
                self._play_audio(audio_file, text)
            else:
                logger.error("Failed to generate audio for playback.")
                self.tts_error.emit("Failed to generate audio for playback.")
        except Exception as e:
            logger.error(f"Error in _generate_and_play_audio: {e}")
            self.tts_error.emit(f"Error in _generate_and_play_audio: {str(e)}")


    def _ensure_cleanup_before_start(self):
        """Ensure proper cleanup before starting new streaming TTS"""
        try:
            # Stop any existing streaming
            if self.is_streaming:
                logger.debug("Stopping existing streaming before starting new one")
                self.stop_playback()
                
            # Wait a moment for cleanup to complete

            QTimer.singleShot(100, lambda: None)  # Small delay to ensure cleanup
            
            # Reset streaming state
            self.is_streaming = False
            self.streaming_player = None
            self.streaming_worker = None
            self.streaming_thread = None
            
            logger.debug("Cleanup before start completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup before start: {e}")
            # Reset state even on error
            self.is_streaming = False
            self.streaming_player = None
            self.streaming_worker = None
            self.streaming_thread = None
    
    def _speak_text_streaming(self, text: str):
        """Convert text to speech using streaming synthesis"""
        log_thread_info("TTS streaming started", logger)
        try:
            self._ensure_cleanup_before_start()
            
            # Initialize streaming player
            self.streaming_player = StreamingAudioPlayer()
            
            # Connect signals BEFORE starting the thread
            self.streaming_player.playback_finished.connect(self._on_streaming_finished)
            self.streaming_player.playback_error.connect(self._on_streaming_error)
            self.streaming_player.player_started.connect(self._on_player_started)
            
            # Use QueuedConnection for thread safety - connect to our signal, not directly to emit

                lambda level: self.audio_level_changed.emit(level), 
                Qt.ConnectionType.QueuedConnection
            )
            
            # NEW: Connect eq_bars_changed
            self.streaming_player.eq_bars_changed.connect(
                lambda bars: self.eq_bars_changed.emit(bars),
                Qt.ConnectionType.QueuedConnection
            )
            
            # Set volume to a reasonable level (0.5 = 50%)
            self.streaming_player.set_volume(0.5)
            
            # Start streaming in a separate QThread instead of threading.Thread

            self.streaming_thread = QThread()
            self.streaming_worker = StreamingAudioWorker(text, self)
            self.streaming_worker.moveToThread(self.streaming_thread)
            
            # Connect signals with QueuedConnection for thread safety
            self.streaming_worker.audio_chunk_ready.connect(
                self.streaming_player.add_audio_chunk, 
                Qt.ConnectionType.QueuedConnection
            )
            self.streaming_worker.progress_updated.connect(
                lambda progress: self.streaming_progress.emit(progress), 
                Qt.ConnectionType.QueuedConnection
            )
            self.streaming_worker.streaming_finished.connect(
                self._on_streaming_generation_finished, 
                Qt.ConnectionType.QueuedConnection
            )
            self.streaming_worker.streaming_error.connect(
                self._on_streaming_generation_error, 
                Qt.ConnectionType.QueuedConnection
            )
            
            # Connect thread started signal
            self.streaming_thread.started.connect(self.streaming_worker.run)
            
            # Start the threads
            if not self.streaming_thread.isRunning():
                self.streaming_thread.start()
            if not self.streaming_player.isRunning():
                self.streaming_player.start()
            self.is_streaming = True
            
            logger.debug("Started streaming TTS synthesis")
            
        except Exception as e:
            logger.error(f"Failed to start streaming TTS: {e}")
            import traceback
            logger.error(f"Streaming TTS error traceback: {traceback.format_exc()}")
            self.tts_error.emit(f"Failed to start streaming TTS: {str(e)}")
    
    def _on_streaming_generation_finished(self):
        """Handle streaming generation finished"""
        if self.is_streaming and self.streaming_player:
            self.streaming_player.end_stream()
    
    def _on_streaming_generation_error(self, error: str):
        """Handle streaming generation error"""
        self.is_streaming = False
        self.tts_error.emit(f"Streaming generation error: {error}")
        logger.error(f"Streaming TTS generation error: {error}")
    
    def _on_player_started(self):
        """Handle streaming player started signal"""
        logger.debug("Streaming audio player started successfully")
    
    def _on_streaming_finished(self):
        """Handle streaming playback finished"""
        try:
            logger.debug("[VOICE] Streaming TTS playback finished - starting cleanup")
            # Defensive: Only clean up if not already cleaned
            if getattr(self, '_cleaned_up', False):
                logger.debug("[VOICE] Already cleaned up, skipping.")
                return
            self._cleaned_up = True
            # Ensure proper cleanup of streaming player
            if hasattr(self, 'streaming_player') and self.streaming_player:
                try:
                    logger.debug("[VOICE] Disconnecting streaming_player signals")
                    safe_disconnect(self.streaming_player.playback_finished)
                    logger.debug("[VOICE] Disconnected playback_finished signal")
                    safe_disconnect(self.streaming_player.playback_error)
                    logger.debug("[VOICE] Disconnected playback_error signal")
                    safe_disconnect(self.streaming_player.audio_level_changed)
                    logger.debug("[VOICE] Disconnected audio_level_changed signal")
                    safe_disconnect(self.streaming_player.player_started)
                    logger.debug("[VOICE] Disconnected player_started signal")
                    self.streaming_player.stop_playback()
                    if self.streaming_player.isRunning():
                        self.streaming_player.quit()
                        if not self.streaming_player.wait(500):  # 500ms timeout
                            logger.warning("[VOICE] Streaming player cleanup timeout in finished callback")
                            self.streaming_player.terminate()
                            self.streaming_player.wait(200)  # Additional 200ms timeout
                except Exception as e:
                    logger.error(f"[VOICE] Error cleaning up streaming player in finished callback: {e}")
            # Clean up streaming worker and thread
            if hasattr(self, 'streaming_worker') and self.streaming_worker:
                try:
                    logger.debug("[VOICE] Disconnecting streaming_worker signals")
                    safe_disconnect(self.streaming_worker.audio_chunk_ready)
                    logger.debug("[VOICE] Disconnected audio_chunk_ready signal")
                    safe_disconnect(self.streaming_worker.progress_updated)
                    logger.debug("[VOICE] Disconnected progress_updated signal")
                    safe_disconnect(self.streaming_worker.streaming_finished)
                    logger.debug("[VOICE] Disconnected streaming_finished signal")
                    safe_disconnect(self.streaming_worker.streaming_error)
                    logger.debug("[VOICE] Disconnected streaming_error signal")
                except Exception as e:
                    logger.error(f"[VOICE] Error cleaning up streaming worker in finished callback: {e}")
            if hasattr(self, 'streaming_thread') and self.streaming_thread:
                try:
                    if self.streaming_thread.isRunning():
                        logger.debug("[VOICE] Stopping streaming thread")
                        self.streaming_thread.quit()
                        if not self.streaming_thread.wait(1000):  # 1 second timeout
                            logger.warning("[VOICE] Streaming thread quit timeout, forcing termination")
                            self.streaming_thread.terminate()
                            if not self.streaming_thread.wait(500):  # Additional timeout
                                logger.error("[VOICE] Streaming thread termination failed")
                        else:
                            logger.debug("[VOICE] Streaming thread stopped successfully")
                    self.streaming_thread.deleteLater()
                except Exception as e:
                    logger.error(f"[VOICE] Error cleaning up streaming thread: {e}")
            # Reset streaming state
            self.is_streaming = False
            self.streaming_player = None
            self.streaming_worker = None
            self.streaming_thread = None
            # Reset TTS in progress flag to allow new TTS requests
            if hasattr(self, '_tts_in_progress'):
                self._tts_in_progress = False
                logger.debug("[VOICE] TTS in progress flag reset")
            logger.debug("[VOICE] Emitting tts_finished after cleanup")
            self.tts_finished.emit()
        except Exception as e:
            logger.error(f"[VOICE] Error in streaming finished callback: {e}")
        finally:
            self._tts_in_progress = False
            self.tts_finished.emit()
    
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
            
            # Stop the streaming worker
            if hasattr(self, 'streaming_worker'):
                safe_disconnect(self.streaming_worker.audio_chunk_ready)
                safe_disconnect(self.streaming_worker.progress_updated)
                safe_disconnect(self.streaming_worker.streaming_finished)
                safe_disconnect(self.streaming_worker.streaming_error)
                self.streaming_worker.stop()
            
            # Disconnect streaming worker signals
            # These are now handled by safe_disconnect in _on_streaming_finished
            
            # Stop the streaming player with timeout
            try:
                # Disconnect player signals
                safe_disconnect(self.streaming_player.playback_finished)
                safe_disconnect(self.streaming_player.playback_error)
                safe_disconnect(self.streaming_player.audio_level_changed)
                safe_disconnect(self.streaming_player.player_started)
                
                self.streaming_player.stop_playback()
                if self.streaming_player.isRunning():
                    self.streaming_player.quit()
                    if not self.streaming_player.wait(1000):  # 1 second timeout
                        logger.warning("Streaming player quit timeout, forcing termination")
                        self.streaming_player.terminate()
                        self.streaming_player.wait(500)  # Additional 500ms timeout
            except Exception as e:
                logger.error(f"Error stopping streaming player: {e}")
            
            # Stop the streaming thread with timeout
            if hasattr(self, 'streaming_thread') and self.streaming_thread.isRunning():
                try:
                    logger.debug("Stopping streaming thread in stop_playback")
                    self.streaming_thread.quit()
                    if not self.streaming_thread.wait(1000):  # 1 second timeout
                        logger.warning("Streaming thread quit timeout, forcing termination")
                        self.streaming_thread.terminate()
                        if not self.streaming_thread.wait(500):  # Additional 500ms timeout
                            logger.error("Streaming thread termination failed in stop_playback")
                        else:
                            logger.debug("Streaming thread terminated successfully")
                    else:
                        logger.debug("Streaming thread stopped successfully")
                    self.streaming_thread.deleteLater()
                except Exception as e:
                    logger.error(f"Error stopping streaming thread: {e}")
            
            # Clear references
            self.streaming_player = None
            self.streaming_worker = None
            self.streaming_thread = None
        
        # Stop non-streaming playback
        if self.media_player:
            self.media_player.stop()
        
        # Only emit tts_finished if we're not already in a streaming finished callback
        # This prevents double emissions
        if not hasattr(self, '_emitting_finished'):
            self._emitting_finished = True
            self.tts_finished.emit()
            # Reset the flag after a short delay

            QTimer.singleShot(100, lambda: setattr(self, '_emitting_finished', False))
    
    def cleanup(self):
        """Clean up resources"""
        if self._cleaned_up:
            logger.debug("CoquiTTSService already cleaned up")
            return
            
        self.stop_playback()
        
        if self.streaming_player:
            self.streaming_player.cleanup()
            self.streaming_player = None
            
        # Clear model cache to free memory
        self.clear_model_cache()
        self._cleaned_up = True
    
    def clear_model_cache(self):
        """Clear the model cache to free memory"""
        try:
            with self._model_loading_lock:
                self._loaded_models.clear()
                logger.debug("Model cache cleared")
        except Exception as e:
            logger.error(f"Error clearing model cache: {e}")
    
    def get_cache_info(self) -> dict:
        """Get information about the model cache"""
        try:
            with self._model_loading_lock:
                return {
                    'cached_models': list(self._loaded_models.keys()),
                    'cache_size': len(self._loaded_models),
                    'current_model': self.current_model
                }
        except Exception as e:
            logger.error(f"Error getting cache info: {e}")
            return {}

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
        all_models = list(downloaded)
        for model in curated_models:
            if model not in all_models:
                all_models.append(model)
        logger.info(f"[CoquiTTS] Final available model list: {all_models}")
        return all_models

    def load_model(self, model_name: str) -> bool:
        """
        Load a specific TTS model and update available voices.
        Uses caching to prevent duplicate loading.
        """
        try:
            # Skip vocoder models
            if model_name.startswith("vocoder_models/"):
                logger.debug(f"Skipping vocoder model: {model_name}")
                return False
                
            # Check if model is already loaded
            with self._model_loading_lock:
                if model_name == self.current_model and self.tts_model is not None:
                    logger.debug(f"Model {model_name} already loaded, skipping")
                    return True
                    
                # Check cache for previously loaded models
                if model_name in self._loaded_models:
                    logger.debug(f"Loading model {model_name} from cache")
                    cached_data = self._loaded_models[model_name]
                    self.tts_model = cached_data['model']
                    self.current_model = model_name
                    self.available_voices = cached_data['voices']
                    self.current_voice = cached_data.get('current_voice', self.available_voices[0] if self.available_voices else None)
                    logger.debug(f"Model {model_name} loaded from cache with {len(self.available_voices)} voices")
                    return True
                
                # Load new model
                from TTS.api import TTS
                logger.debug(f"Loading new model: {model_name}")
                self.tts_model = TTS(model_name=model_name)
                self.current_model = model_name
                
                # Always try to get voices
                if hasattr(self.tts_model, 'list_voices'):
                    self.available_voices = self.tts_model.list_voices()
                    logger.debug(f"Voices for model {model_name}: {self.available_voices}")
                else:
                    self.available_voices = []
                    logger.debug(f"Model {model_name} has no list_voices method.")

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
                                logger.debug(f"Loaded speakers from speakers_file: {self.available_voices}")
                        except Exception as e:
                            logger.debug(f"Failed to load speakers_file: {e}")

                # Set default voice for multi-speaker models
                if self.available_voices:
                    self.current_voice = self.available_voices[0]
                    logger.debug(f"Set default voice to: {self.current_voice}")
                    self.voices_loaded.emit(self.available_voices)
                else:
                    self.current_voice = None
                    logger.debug(f"No voices available, using single-speaker mode")

                # Cache the loaded model
                self._loaded_models[model_name] = {
                    'model': self.tts_model,
                    'voices': self.available_voices,
                    'current_voice': self.current_voice
                }
                
                logger.debug(f"Speaker count for model {model_name}: {len(self.available_voices)}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
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
# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.audio_imports import *

"""
StreamingAudioPlayer - split from coqui_tts.py
"""
import numpy as np
import threading

logger = CustomLogger.get_logger(__name__)

class StreamingAudioPlayer(QThread):
    """Thread for streaming audio playback"""
    audio_chunk_ready = Signal(bytes)
    playback_finished = Signal()
    playback_error = Signal(str)
    audio_level_changed = Signal(float)  # Emit audio level for EQ visualization
    eq_bars_changed = Signal(list)  # NEW: Emit EQ bar array for visualization
    player_started = Signal()  # Signal when player starts successfully

    def __init__(self, sample_rate=22050, channels=1, chunk_size=512):
        super().__init__()
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_queue = []
        self.is_playing = False
        self.should_stop = False
        self.volume = 0.5  # Volume control (0.0 to 1.0)
        self.current_audio_level = 0.0
        self.audio_level_buffer = []  # Buffer for averaging audio levels
        self.last_audio_level_emit_time = 0  # Track when we last emitted audio level
        self.pyaudio = None
        self.stream = None
        self._cleaned_up = False
        
        logger.debug(f"StreamingAudioPlayer initialized with sample_rate={sample_rate}, channels={channels}, chunk_size={chunk_size}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        if not self._cleaned_up:
            logger.debug("StreamingAudioPlayer destructor called - cleaning up")
            self.cleanup()

    def run(self):
        """Main playback loop with comprehensive error handling"""
        try:
            logger.debug("Starting streaming audio player run method")
            
            # Initialize PyAudio with error handling
            if not self.pyaudio:
                try:
                    logger.debug("Initializing PyAudio")
                    self.pyaudio = pyaudio.PyAudio()
                    
                    # List available audio devices for debugging
                    try:
                        device_count = self.pyaudio.get_device_count()
                        logger.debug(f"Found {device_count} audio devices")
                        for i in range(device_count):
                            try:
                                device_info = self.pyaudio.get_device_info_by_index(i)
                                logger.debug(f"Device {i}: {device_info['name']} (max outputs: {device_info.get('maxOutputChannels', 0)})")
                            except Exception as e:
                                logger.warning(f"Could not get info for device {i}: {e}")
                    except Exception as e:
                        logger.warning(f"Could not enumerate audio devices: {e}")
                except Exception as e:
                    logger.error(f"Failed to initialize PyAudio: {e}")
                    self.playback_error.emit(f"PyAudio initialization failed: {str(e)}")
                    return
            
            # Get default output device with error handling
            try:
                default_device = self.pyaudio.get_default_output_device_info()
                logger.debug(f"Using default output device: {default_device['name']}")
            except Exception as e:
                logger.warning(f"Could not get default output device: {e}")
            
            # Open audio stream with error handling
            try:
                logger.debug("Opening audio stream")
                self.stream = self.pyaudio.open(
                    format=pyaudio.paFloat32,
                    channels=self.channels,
                    rate=self.sample_rate,
                    output=True,
                    frames_per_buffer=self.chunk_size
                )
                logger.debug("Audio stream opened successfully")
            except Exception as e:
                logger.error(f"Failed to open audio stream: {e}")
                self.playback_error.emit(f"Audio stream initialization failed: {str(e)}")
                return
            
            self.is_playing = True
            logger.debug("Starting audio playback loop")
            
            # Emit started signal with error handling
            try:
                self.player_started.emit()
            except Exception as e:
                logger.error(f"Error emitting player started signal: {e}")
            
            # Main playback loop with error handling
            while self.is_playing and not self.should_stop:
                try:
                    if self.audio_queue:
                        audio_data = self.audio_queue.pop(0)
                        if audio_data is not None:  # None signals end of stream
                            logger.debug(f"Processing audio chunk of size {len(audio_data)}")
                            processed_audio = self._process_audio_chunk(audio_data)
                            logger.debug(f"Writing {len(processed_audio.tobytes())} bytes to audio stream")
                            self.stream.write(processed_audio.tobytes())
                        else:
                            logger.debug("Received end-of-stream signal")
                            break
                    else:
                        time.sleep(0.01)  # Small delay to prevent busy waiting
                except Exception as e:
                    logger.error(f"Error in audio playback loop: {e}")
                    self.playback_error.emit(f"Audio playback error: {str(e)}")
                    break
            
            logger.debug("Audio playback loop finished")
            self.is_playing = False
            
            # Emit finished signal with error handling
            try:
                self.playback_finished.emit()
            except Exception as e:
                logger.error(f"Error emitting playback finished signal: {e}")
            
        except Exception as e:
            logger.error(f"Streaming audio playback error: {e}")
            import traceback
            logger.error(f"Audio playback error traceback: {traceback.format_exc()}")
            try:
                self.playback_error.emit(str(e))
            except Exception as emit_error:
                logger.error(f"Error emitting playback error signal: {emit_error}")
        finally:
            # Always clean up audio stream
            logger.debug("Cleaning up audio stream")
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    logger.debug("Audio stream closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing audio stream: {e}")

    def _process_audio_chunk(self, audio_chunk: np.ndarray) -> np.ndarray:
        """Process audio chunk with comprehensive error handling"""
        try:
            logger.debug(f"Processing audio chunk: shape={audio_chunk.shape}, dtype={audio_chunk.dtype}")
            
            # Validate input
            if audio_chunk is None or len(audio_chunk) == 0:
                logger.warning("Empty audio chunk received")
                return np.array([], dtype=np.float32)
            
            # Convert to float32 if needed
            if audio_chunk.dtype != np.float32:
                try:
                    audio_chunk = audio_chunk.astype(np.float32)
                    logger.debug("Converted audio chunk to float32")
                except Exception as e:
                    logger.error(f"Error converting audio chunk to float32: {e}")
                    return np.array([], dtype=np.float32)
                
            # Normalize audio if it has content
            if np.max(np.abs(audio_chunk)) > 0:
                try:
                    audio_chunk = audio_chunk / np.max(np.abs(audio_chunk)) * 0.8
                    logger.debug("Normalized audio chunk")
                except Exception as e:
                    logger.error(f"Error normalizing audio chunk: {e}")
                
            # Apply volume
            try:
                audio_chunk = audio_chunk * self.volume
                audio_chunk = np.clip(audio_chunk, -1.0, 1.0)
            except Exception as e:
                logger.error(f"Error applying volume to audio chunk: {e}")
            
            # Calculate EQ bars with error handling
            try:
                # --- FFT-based EQ bar calculation ---
                def calculate_eq_bars(chunk, num_bars=24, sample_rate=22050):
                    try:
                        fft = np.fft.rfft(chunk, n=2048)
                        mag = np.abs(fft)
                        freqs = np.fft.rfftfreq(2048, 1/sample_rate)
                        # Logarithmic bands
                        band_edges = np.logspace(np.log10(20), np.log10(sample_rate/2), num_bars+1)
                        bar_vals = []
                        for i in range(num_bars):
                            idx = np.where((freqs >= band_edges[i]) & (freqs < band_edges[i+1]))[0]
                            if len(idx) > 0:
                                energy = float(np.sqrt(np.mean(mag[idx]**2)))
                                bar_vals.append(energy)
                            else:
                                bar_vals.append(0.0)
                        # Normalize
                        max_val = max(bar_vals) or 1.0
                        bar_vals = [0.1 + 0.9 * (v / max_val) for v in bar_vals]
                        return bar_vals
                    except Exception as e:
                        logger.error(f"Error calculating EQ bars: {e}")
                        return [0.0] * num_bars
                
                eq_bars = calculate_eq_bars(audio_chunk, num_bars=24, sample_rate=self.sample_rate)
                
                # Emit EQ bars with error handling
                try:
                    self.eq_bars_changed.emit(eq_bars)
                except Exception as e:
                    logger.error(f"Error emitting EQ bars: {e}")
                    
            except Exception as e:
                logger.error(f"Error in EQ bar calculation: {e}")

            # Calculate audio level with error handling
            try:
                # (Keep the old audio level logic for backward compatibility)
                rms_level = np.sqrt(np.mean(audio_chunk**2))
                peak_level = np.max(np.abs(audio_chunk))
                combined_level = (rms_level * 0.4 + peak_level * 0.6)
                amplified_level = combined_level * 4.0
                
                if len(audio_chunk) > 0:
                    try:
                        fft = np.fft.rfft(audio_chunk)
                        magnitude = np.abs(fft)
                        low_freq_energy = np.mean(magnitude[:len(magnitude)//4])
                        mid_freq_energy = np.mean(magnitude[len(magnitude)//4:len(magnitude)//2])
                        high_freq_energy = np.mean(magnitude[len(magnitude)//2:])
                        freq_enhancement = (low_freq_energy * 0.3 + mid_freq_energy * 0.4 + high_freq_energy * 0.3) / np.max(magnitude) if np.max(magnitude) > 0 else 1.0
                        amplified_level *= (1.0 + freq_enhancement * 0.5)
                    except Exception as e:
                        logger.error(f"Error calculating frequency enhancement: {e}")
                        
                amplified_level = max(amplified_level, 0.05)
                self.current_audio_level = amplified_level
                self.audio_level_buffer.append(amplified_level)
                
                if len(self.audio_level_buffer) > 5:
                    self.audio_level_buffer.pop(0)
                    
                if self.audio_level_buffer:
                    avg_level = sum(self.audio_level_buffer) / len(self.audio_level_buffer)
                    smoothed_level = avg_level * 0.8 + amplified_level * 0.2
                    
                    # Emit audio level with error handling
                    try:
                        self.audio_level_changed.emit(smoothed_level)
                        logger.debug(f"Emitted audio level: {smoothed_level:.4f} (raw: {amplified_level:.4f})")
                    except Exception as e:
                        logger.error(f"Error emitting audio level: {e}")
                        
                logger.debug(f"Audio chunk processed: max={np.max(audio_chunk)}, min={np.min(audio_chunk)}, level={amplified_level:.4f}")
                
            except Exception as e:
                logger.error(f"Error calculating audio level: {e}")
                
            return audio_chunk
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            import traceback
            logger.error(f"Audio chunk processing error traceback: {traceback.format_exc()}")
            # Return empty array as fallback
            return np.array([], dtype=np.float32)

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
        logger.debug(f"Volume set to {self.volume}")

    def add_audio_chunk(self, audio_chunk: np.ndarray):
        """Add audio chunk to queue with error handling"""
        try:
            if self.is_playing:
                logger.debug(f"Adding audio chunk to queue (queue size: {len(self.audio_queue)})")
                self.audio_queue.append(audio_chunk)
            else:
                logger.warning("Audio player not playing, ignoring audio chunk")
        except Exception as e:
            logger.error(f"Error adding audio chunk to queue: {e}")

    def end_stream(self):
        """End audio stream with error handling"""
        try:
            logger.debug("Ending audio stream")
            self.audio_queue.append(None)  # Signal end of stream
        except Exception as e:
            logger.error(f"Error ending audio stream: {e}")

    def stop_playback(self):
        """Stop audio playback with comprehensive error handling"""
        try:
            logger.debug("Stopping audio playback")
            
            # Set stop flag
            self.should_stop = True
            self.is_playing = False
            
            # Clear audio queue
            try:
                self.audio_queue.clear()
            except Exception as e:
                logger.error(f"Error clearing audio queue: {e}")
            
            # Stop audio stream if it exists
            if self.stream:
                try:
                    self.stream.stop_stream()
                    logger.debug("Audio stream stopped")
                except Exception as e:
                    logger.error(f"Error stopping audio stream: {e}")
                    
        except Exception as e:
            logger.error(f"Error in stop_playback: {e}")
            import traceback
            logger.error(f"Stop playback error traceback: {traceback.format_exc()}")

    def cleanup(self):
        """Comprehensive cleanup with error handling"""
        try:
            logger.debug("Cleaning up streaming audio player")
            
            # Stop playback first
            try:
                self.stop_playback()
            except Exception as e:
                logger.error(f"Error stopping playback during cleanup: {e}")
            
            # Clean up audio stream
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    logger.debug("Audio stream closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing audio stream during cleanup: {e}")
            
            # Clean up PyAudio
            if self.pyaudio:
                try:
                    # Use a separate thread for PyAudio termination to avoid blocking
                    def terminate_pyaudio():
                        try:
                            self.pyaudio.terminate()
                            logger.debug("PyAudio terminated successfully")
                        except Exception as e:
                            logger.error(f"Error terminating PyAudio: {e}")
                    
                    # Start termination in background thread
                    import threading
                    term_thread = threading.Thread(target=terminate_pyaudio, name="terminate_pyaudio")
                    term_thread.daemon = True
                    # Check if thread is already running (safety check)
                    if not term_thread.is_alive():
                        term_thread.start()
                    
                except Exception as e:
                    logger.error(f"Error setting up PyAudio termination: {e}")
            
            # Clear state
            try:
                self.audio_queue.clear()
                self.audio_level_buffer.clear()
                self.current_audio_level = 0.0
                self._cleaned_up = True
            except Exception as e:
                logger.error(f"Error clearing state during cleanup: {e}")
                
            logger.debug("Streaming audio player cleanup completed")
            
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
            import traceback
            logger.error(f"Cleanup error traceback: {traceback.format_exc()}") 
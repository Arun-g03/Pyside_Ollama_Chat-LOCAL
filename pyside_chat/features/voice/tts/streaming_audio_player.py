"""
StreamingAudioPlayer - split from coqui_tts.py
"""
import time
import numpy as np
import threading
from PySide6.QtCore import QThread, Signal
import pyaudio
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class StreamingAudioPlayer(QThread):
    """Thread for streaming audio playback"""
    audio_chunk_ready = Signal(bytes)
    playback_finished = Signal()
    playback_error = Signal(str)
    audio_level_changed = Signal(float)  # Emit audio level for EQ visualization
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
        """Main playback loop"""
        try:
            logger.debug("Starting streaming audio player run method")
            
            # Initialize PyAudio
            if not self.pyaudio:
                logger.debug("Initializing PyAudio")
                self.pyaudio = pyaudio.PyAudio()
                
                # List available audio devices for debugging
                try:
                    device_count = self.pyaudio.get_device_count()
                    logger.debug(f"Found {device_count} audio devices")
                    for i in range(device_count):
                        device_info = self.pyaudio.get_device_info_by_index(i)
                        logger.debug(f"Device {i}: {device_info['name']} (max outputs: {device_info.get('maxOutputChannels', 0)})")
                except Exception as e:
                    logger.warning(f"Could not enumerate audio devices: {e}")
            
            # Get default output device
            try:
                default_device = self.pyaudio.get_default_output_device_info()
                logger.debug(f"Using default output device: {default_device['name']}")
            except Exception as e:
                logger.warning(f"Could not get default output device: {e}")
            
            # Open audio stream
            logger.debug("Opening audio stream")
            self.stream = self.pyaudio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                output=True,
                frames_per_buffer=self.chunk_size
            )
            logger.debug("Audio stream opened successfully")
            
            self.is_playing = True
            logger.debug("Starting audio playback loop")
            
            # Emit started signal
            self.player_started.emit()
            
            while self.is_playing and not self.should_stop:
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
            
            logger.debug("Audio playback loop finished")
            self.is_playing = False
            self.playback_finished.emit()
            
        except Exception as e:
            logger.error(f"Streaming audio playback error: {e}")
            import traceback
            logger.error(f"Audio playback error traceback: {traceback.format_exc()}")
            self.playback_error.emit(str(e))
        finally:
            logger.debug("Cleaning up audio stream")
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                    logger.debug("Audio stream closed successfully")
                except Exception as e:
                    logger.warning(f"Error closing audio stream: {e}")

    def _process_audio_chunk(self, audio_chunk: np.ndarray) -> np.ndarray:
        try:
            logger.debug(f"Processing audio chunk: shape={audio_chunk.shape}, dtype={audio_chunk.dtype}")
            
            if audio_chunk.dtype != np.float32:
                audio_chunk = audio_chunk.astype(np.float32)
                logger.debug("Converted audio chunk to float32")
                
            if np.max(np.abs(audio_chunk)) > 0:
                audio_chunk = audio_chunk / np.max(np.abs(audio_chunk)) * 0.8
                logger.debug("Normalized audio chunk")
                
            audio_chunk = audio_chunk * self.volume
            audio_chunk = np.clip(audio_chunk, -1.0, 1.0)
            
            rms_level = np.sqrt(np.mean(audio_chunk**2))
            peak_level = np.max(np.abs(audio_chunk))
            combined_level = (rms_level * 0.7 + peak_level * 0.3)
            amplified_level = combined_level * 2.0
            self.current_audio_level = amplified_level
            self.audio_level_buffer.append(amplified_level)
            
            if len(self.audio_level_buffer) > 5:
                self.audio_level_buffer.pop(0)
                
            if self.audio_level_buffer:
                avg_level = sum(self.audio_level_buffer) / len(self.audio_level_buffer)
                self.audio_level_changed.emit(avg_level)
                
            logger.debug(f"Audio chunk processed: max={np.max(audio_chunk)}, min={np.min(audio_chunk)}")
            return audio_chunk
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            import traceback
            logger.error(f"Audio chunk processing error traceback: {traceback.format_exc()}")
            return audio_chunk

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
        logger.debug(f"Volume set to {self.volume}")

    def add_audio_chunk(self, audio_chunk: np.ndarray):
        if self.is_playing:
            logger.debug(f"Adding audio chunk to queue (queue size: {len(self.audio_queue)})")
            self.audio_queue.append(audio_chunk)
        else:
            logger.warning("Cannot add audio chunk - player not playing")

    def end_stream(self):
        if self.is_playing:
            logger.debug("Ending audio stream")
            self.audio_queue.append(None)

    def stop_playback(self):
        logger.debug("Stopping audio playback")
        self.should_stop = True
        self.is_playing = False
        if self.stream:
            try:
                self.stream.stop_stream()
                logger.debug("Audio stream stopped")
            except Exception as e:
                logger.warning(f"Error stopping audio stream: {e}")

    def cleanup(self):
        logger.debug("Cleaning up streaming audio player")
        
        if self._cleaned_up:
            logger.debug("Streaming audio player already cleaned up")
            return
            
        self.stop_playback()
        
        # Wait for the thread to finish before cleaning up PyAudio
        if self.isRunning():
            logger.debug("Waiting for streaming audio player thread to finish")
            self.quit()
            if not self.wait(2000):  # 2 second timeout
                logger.warning("Streaming audio player thread quit timeout, forcing termination")
                self.terminate()
                if not self.wait(1000):  # Additional 1 second timeout
                    logger.error("Streaming audio player thread termination failed")
                else:
                    logger.debug("Streaming audio player thread terminated successfully")
            else:
                logger.debug("Streaming audio player thread stopped successfully")
        
        if self.pyaudio:
            try:
                def terminate_pyaudio():
                    try:
                        logger.debug("Terminating PyAudio")
                        self.pyaudio.terminate()
                        logger.debug("PyAudio terminated successfully")
                    except Exception as e:
                        logger.warning(f"Error terminating pyaudio: {e}")
                thread = threading.Thread(target=terminate_pyaudio)
                thread.daemon = True
                thread.start()
                thread.join(timeout=1.0)
                if thread.is_alive():
                    logger.warning("pyaudio.terminate() timed out, continuing cleanup")
            except Exception as e:
                logger.error(f"Error during pyaudio cleanup: {e}")
        
        self._cleaned_up = True 
"""
QThread-based workers for long-running, persistent tasks.

These workers are designed for tasks that need:
- Continuous operation
- Signal/slot communication
- Persistent thread lifecycle
- Complex state management
"""

from PySide6.QtCore import QObject, Signal, QThread, Qt
import requests
import json
import time
import traceback
from typing import Dict, List, Any, Optional
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class StreamingWorker(QObject):
    """
    Base streaming worker for long-running operations with signal/slot communication.
    
    Use this for:
    - Real-time data streaming
    - Continuous monitoring
    - Persistent background tasks
    """
    
    # Signals for communication with main thread
    chunk_received = Signal(str)  # Emitted when new data chunk arrives
    progress_updated = Signal(str)  # Emitted for progress updates
    finished = Signal()  # Emitted when task completes
    error = Signal(str)  # Emitted when error occurs
    status_changed = Signal(str)  # Emitted for status changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._should_stop = False
        self._start_time = None
        self._request_count = 0
        self._thread_id = None
        
        logger.debug(f"[ID:TH001] StreamingWorker created - ID: {id(self)}")
    
    def _log_thread_info(self, action: str):
        """Log thread information for debugging"""
        current_thread = QThread.currentThread()
        thread_name = current_thread.objectName() or 'unnamed'
        thread_id = id(current_thread)
        logger.debug(f"[ID:TH002] StreamingWorker {action} - Thread: {thread_name} (ID: {thread_id})")
    
    def start_streaming(self, **kwargs):
        """
        Start the streaming operation.
        
        Override this method in subclasses to implement specific streaming logic.
        """
        try:
            self._log_thread_info("start_streaming")
            self._running = True
            self._should_stop = False
            self._start_time = time.time()
            self._request_count += 1
            
            self.status_changed.emit("Starting streaming operation...")
            logger.debug(f"[ID:TH003] Streaming started with kwargs: {kwargs}")
            
            # Subclasses should override this method
            self._stream_operation(**kwargs)
            
        except Exception as e:
            error_msg = f"Streaming error: {str(e)}"
            logger.error(f"[ID:TH004] {error_msg}")
            logger.error(f"[ID:TH005] Streaming error traceback: {traceback.format_exc()}")
            self.error.emit(error_msg)
        finally:
            self._running = False
            self._start_time = None
            self._log_thread_info("start_streaming finished")
            self.finished.emit()
    
    def _stream_operation(self, **kwargs):
        """
        Override this method in subclasses to implement specific streaming logic.
        """
        raise NotImplementedError("Subclasses must implement _stream_operation")
    
    def stop(self):
        """Stop the streaming operation safely."""
        try:
            self._log_thread_info("stop requested")
            logger.debug(f"[ID:TH006] Streaming stop requested - Running: {self._running}")
            
            self._running = False
            self._should_stop = True
            self.status_changed.emit("Stopping streaming operation...")
            
            # Give the worker a moment to finish naturally
            if self._running:
                logger.debug("[ID:TH007] Waiting for streaming to finish naturally...")
                time.sleep(0.1)
            
            logger.debug("[ID:TH008] Streaming stop completed")
            
        except Exception as e:
            logger.error(f"[ID:TH009] Error stopping streaming: {e}")
            logger.error(f"[ID:TH010] Streaming stop traceback: {traceback.format_exc()}")
    
    def is_running(self):
        """Check if the streaming operation is currently running."""
        return self._running
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the streaming operation."""
        duration = time.time() - self._start_time if self._start_time else 0
        return {
            'running': self._running,
            'request_count': self._request_count,
            'duration': duration,
            'thread_id': self._thread_id
        }


class ChatStreamingWorker(StreamingWorker):
    """
    Worker for streaming chat responses from Ollama.
    
    This is a long-running operation that needs:
    - Continuous streaming of response chunks
    - Signal/slot communication for UI updates
    - Persistent thread lifecycle
    """
    
    def _stream_operation(self, messages: List[Dict], model: str, temperature: float,
                         ollama_url: str, max_tokens: int, top_p: float,
                         frequency_penalty: float, presence_penalty: float):
        """
        Stream chat response from Ollama.
        """
        try:
            logger.debug(f"[ID:TH011] Chat streaming started - Model: {model}")
            logger.debug(f"[ID:TH011A] Messages count: {len(messages)}")
            logger.debug(f"[ID:TH011B] First message: {messages[0] if messages else 'No messages'}")
            self.progress_updated.emit("Connecting to Ollama...")
            
            # Prepare request data
            base_url = ollama_url.replace('/api', '') if ollama_url.endswith('/api') else ollama_url
            url = f"{base_url}/api/chat"
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "stream": True
            }
            
            logger.debug(f"[ID:TH012] Making streaming request to: {url}")
            logger.debug(f"[ID:TH012A] Request data: {data}")
            
            # Test connection first with more detailed error handling
            try:
                logger.debug(f"[ID:TH012B] Testing Ollama connection to: {base_url}/api/tags")
                test_response = requests.get(f"{base_url}/api/tags", timeout=15)
                logger.debug(f"[ID:TH012C] Test response status: {test_response.status_code}")
                if test_response.status_code != 200:
                    raise requests.exceptions.RequestException(
                        f"Ollama not responding properly: {test_response.status_code}")
                
                # Check if models are available
                try:
                    models_data = test_response.json()
                    models = models_data.get('models', [])
                    if not models:
                        logger.warning("[ID:TH013A] No models found in Ollama response")
                        self.progress_updated.emit("Warning: No models found in Ollama")
                    else:
                        logger.debug(f"[ID:TH013B] Found {len(models)} models in Ollama")
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"[ID:TH013C] Could not parse models response: {e}")
                
                logger.debug(f"[ID:TH013] Ollama connection test successful")
                self.progress_updated.emit("Connection successful, sending request...")
                
            except requests.exceptions.ConnectionError as e:
                error_msg = "Cannot connect to Ollama. Please make sure Ollama is running on localhost:11434"
                logger.error(f"[ID:TH014] Ollama connection test failed: {e}")
                self.error.emit(error_msg)
                return
            except requests.exceptions.Timeout as e:
                error_msg = "Ollama connection timed out. The service might be busy or overloaded."
                logger.error(f"[ID:TH014A] Ollama connection timeout: {e}")
                self.error.emit(error_msg)
                return
            except Exception as e:
                error_msg = f"Ollama connection failed: {str(e)}"
                logger.error(f"[ID:TH015] Ollama connection error: {e}")
                self.error.emit(error_msg)
                return
            
            # Make streaming request
            logger.debug(f"[ID:TH015A] Starting streaming POST request to: {url}")
            self.progress_updated.emit("Sending request to Ollama...")
            with requests.post(url, json=data, stream=True, timeout=30) as response:
                logger.debug(f"[ID:TH016] Stream response received - Status: {response.status_code}")
                logger.debug(f"[ID:TH016A] Response headers: {dict(response.headers)}")
                
                if response.status_code != 200:
                    error_msg = f"Ollama returned error status: {response.status_code}"
                    logger.error(f"[ID:TH016C] {error_msg}")
                    self.error.emit(error_msg)
                    return
                
                self.progress_updated.emit("Receiving response from Ollama...")
                
                chunk_count = 0
                start_time = time.time()
                timeout_seconds = 15  # Reduced from 60 to 15 seconds for local connections
                
                # Send initial progress message for model loading
                self.progress_updated.emit(f"Model '{model}' is loading, please wait...")
                
                logger.debug(f"[ID:TH016B] Starting to iterate through response lines")
                for line in response.iter_lines(decode_unicode=True):
                    if self._should_stop:
                        logger.debug("[ID:TH017] Chat streaming stop requested")
                        break
                    
                    # Check for timeout - only for first chunk to allow for model loading
                    if chunk_count == 0 and (time.time() - start_time) > timeout_seconds:
                        error_msg = f"Timeout waiting for first response from Ollama after {timeout_seconds} seconds. The model '{model}' might be loading or Ollama might be busy. Try again in a moment."
                        logger.error(f"[ID:TH018] {error_msg}")
                        self.error.emit(error_msg)
                        return
                    
                    if line:
                        logger.debug(f"[ID:TH018A] Processing line: {line[:100]}...")
                        try:
                            chunk = json.loads(line)
                            logger.debug(f"[ID:TH018B] Parsed chunk: {chunk}")
                            content = chunk.get("message", {}).get("content", "")
                            logger.debug(f"[ID:TH018C] Extracted content: {content[:50]}...")
                            
                            if content:
                                chunk_count += 1
                                logger.debug(f"[ID:TH019] Emitting chunk {chunk_count}: {content[:50]}...")
                                self.chunk_received.emit(content)
                                
                                # Update progress on first chunk
                                if chunk_count == 1:
                                    self.progress_updated.emit("Model loaded, receiving response...")
                                
                                # Update progress every 10 chunks
                                if chunk_count % 10 == 0:
                                    self.progress_updated.emit(f"Received {chunk_count} chunks...")
                            else:
                                logger.debug(f"[ID:TH019A] Empty content in chunk: {chunk}")
                                    
                        except json.JSONDecodeError as e:
                            logger.warning(f"[ID:TH020] JSON decode error: {e}")
                            logger.warning(f"[ID:TH020A] Problematic line: {line}")
                            continue
                        except Exception as e:
                            logger.error(f"[ID:TH021] Error processing chunk: {e}")
                            logger.error(f"[ID:TH021A] Problematic line: {line}")
                            continue
                    else:
                        logger.debug(f"[ID:TH021B] Empty line received")
                
                logger.debug(f"[ID:TH022] Chat streaming completed - Total chunks: {chunk_count}")
                self.progress_updated.emit(f"Completed - {chunk_count} chunks received")
                
        except requests.exceptions.Timeout as e:
            error_msg = "Request timed out. Please try again."
            logger.error(f"[ID:TH023] Chat streaming timeout: {e}")
            self.error.emit(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(f"[ID:TH024] Chat streaming request error: {e}")
            self.error.emit(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"[ID:TH025] Chat streaming unexpected error: {e}")
            logger.error(f"[ID:TH026] Chat streaming traceback: {traceback.format_exc()}")
            self.error.emit(error_msg)


class AudioStreamingWorker(StreamingWorker):
    """
    Worker for streaming audio processing.
    
    This is a long-running operation that needs:
    - Continuous audio stream processing
    - Real-time audio chunk handling
    - Signal/slot communication for audio updates
    """
    
    audio_chunk_received = Signal(bytes)  # Emitted when audio chunk is processed
    audio_level_updated = Signal(float)  # Emitted for audio level updates
    
    def _stream_operation(self, audio_source: str, sample_rate: int = 16000, 
                         chunk_size: int = 1024):
        """
        Stream audio processing.
        """
        try:
            logger.debug(f"[ID:TH027] Audio streaming started - Source: {audio_source}")
            self.progress_updated.emit("Starting audio processing...")
            
            # Audio processing logic would go here
            # This is a placeholder for actual audio streaming implementation
            
            # Simulate audio processing
            import time
            for i in range(100):  # Simulate 100 audio chunks
                if self._should_stop:
                    break
                
                # Simulate audio chunk processing
                time.sleep(0.1)  # Simulate processing time
                
                # Emit audio level (simulated)
                import random
                audio_level = random.uniform(0.0, 1.0)
                self.audio_level_updated.emit(audio_level)
                
                # Emit progress every 10 chunks
                if i % 10 == 0:
                    self.progress_updated.emit(f"Processed {i} audio chunks...")
            
            logger.debug("[ID:TH028] Audio streaming completed")
            self.progress_updated.emit("Audio processing completed")
            
        except Exception as e:
            error_msg = f"Audio streaming error: {str(e)}"
            logger.error(f"[ID:TH029] {error_msg}")
            logger.error(f"[ID:TH030] Audio streaming traceback: {traceback.format_exc()}")
            self.error.emit(error_msg)


class MonitoringWorker(StreamingWorker):
    """
    Worker for continuous monitoring tasks.
    
    This is a long-running operation that needs:
    - Continuous monitoring of system resources
    - Periodic status updates
    - Signal/slot communication for monitoring updates
    """
    
    resource_updated = Signal(dict)  # Emitted when resource usage changes
    alert_triggered = Signal(str)  # Emitted when alert condition is met
    
    def _stream_operation(self, monitor_interval: float = 1.0, 
                         alert_threshold: float = 0.8):
        """
        Monitor system resources continuously.
        """
        try:
            logger.debug(f"[ID:TH031] Monitoring started - Interval: {monitor_interval}s")
            self.progress_updated.emit("Starting system monitoring...")
            
            import psutil
            import time
            
            while self._running and not self._should_stop:
                try:
                    # Get system resource usage
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    resource_data = {
                        'cpu_percent': cpu_percent,
                        'memory_percent': memory.percent,
                        'disk_percent': disk.percent,
                        'timestamp': time.time()
                    }
                    
                    # Emit resource update
                    self.resource_updated.emit(resource_data)
                    
                    # Check for alerts
                    if cpu_percent > (alert_threshold * 100):
                        self.alert_triggered.emit(f"High CPU usage: {cpu_percent:.1f}%")
                    
                    if memory.percent > (alert_threshold * 100):
                        self.alert_triggered.emit(f"High memory usage: {memory.percent:.1f}%")
                    
                    # Update progress periodically
                    if int(time.time()) % 10 == 0:  # Every 10 seconds
                        self.progress_updated.emit(
                            f"Monitoring - CPU: {cpu_percent:.1f}%, "
                            f"Memory: {memory.percent:.1f}%"
                        )
                    
                    time.sleep(monitor_interval)
                    
                except Exception as e:
                    logger.error(f"[ID:TH032] Monitoring iteration error: {e}")
                    time.sleep(monitor_interval)
                    continue
            
            logger.debug("[ID:TH033] Monitoring completed")
            self.progress_updated.emit("System monitoring stopped")
            
        except Exception as e:
            error_msg = f"Monitoring error: {str(e)}"
            logger.error(f"[ID:TH034] {error_msg}")
            logger.error(f"[ID:TH035] Monitoring traceback: {traceback.format_exc()}")
            self.error.emit(error_msg) 
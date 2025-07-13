"""
QThread-based workers for long-running, persistent tasks.

These workers are designed for tasks that need:
- Continuous operation
- Signal/slot communication
- Persistent thread lifecycle
- Complex state management
- Reusable configuration for persistent thread pools
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
    - Reusable workers for thread pools
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
        self._configuration = {}
        
        logger.debug(f"[ID:TH001] StreamingWorker created - ID: {id(self)}")
    
    def _log_thread_info(self, action: str):
        """Log thread information for debugging"""
        current_thread = QThread.currentThread()
        thread_name = current_thread.objectName() or 'unnamed'
        thread_id = id(current_thread)
        logger.debug(f"[ID:TH002] StreamingWorker {action} - Thread: {thread_name} (ID: {thread_id})")
    
    def configure_streaming(self, **kwargs):
        """
        Configure the worker for streaming operations.
        
        Args:
            **kwargs: Configuration parameters for streaming
        """
        try:
            self._configuration.update(kwargs)
            logger.debug(f"[ID:TH003] StreamingWorker configured with: {list(kwargs.keys())}")
        except Exception as e:
            logger.error(f"[ID:TH004] Error configuring streaming worker: {e}")
    
    def reset_state(self):
        """Reset worker state for reuse in persistent thread pool."""
        try:
            self._running = False
            self._should_stop = False
            self._start_time = None
            self._request_count = 0
            self._configuration = {}
            
            logger.debug("[ID:TH005] StreamingWorker state reset")
        except Exception as e:
            logger.error(f"[ID:TH006] Error resetting streaming worker state: {e}")
    
    def is_running(self) -> bool:
        """Check if the worker is currently running."""
        return self._running
    
    def start_streaming(self):
        """Start the streaming operation."""
        try:
            self._log_thread_info("starting streaming")
            self._running = True
            self._should_stop = False
            self._start_time = time.time()
            self._request_count = 0
            
            # Start the actual streaming operation
            self._stream_operation()
            
        except Exception as e:
            logger.error(f"[ID:TH007] Error starting streaming: {e}")
            self.error.emit(f"Failed to start streaming: {str(e)}")
    
    def stop(self):
        """Stop the streaming operation."""
        try:
            self._log_thread_info("stopping streaming")
            self._should_stop = True
            self._running = False
            
        except Exception as e:
            logger.error(f"[ID:TH008] Error stopping streaming: {e}")
    
    def _stream_operation(self):
        """
        Implement the actual streaming operation.
        
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _stream_operation")


class ChatStreamingWorker(StreamingWorker):
    """
    Worker for streaming chat responses from Ollama.
    
    This is a long-running operation that needs:
    - Continuous streaming of chat responses
    - Signal/slot communication for chunks
    - Persistent thread lifecycle
    - Reusable configuration for thread pools
    """
    
    def configure_streaming(self, context_messages: List[Dict], model: str, temperature: float, config_manager):
        """
        Configure the worker for chat streaming.
        
        Args:
            context_messages: List of conversation messages
            model: Model name to use
            temperature: Temperature setting
            config_manager: Configuration manager
        """
        try:
            super().configure_streaming(
                context_messages=context_messages,
                model=model,
                temperature=temperature,
                config_manager=config_manager
            )
            
            # Store configuration for streaming
            self._configuration.update({
                'context_messages': context_messages,
                'model': model,
                'temperature': temperature,
                'config_manager': config_manager
            })
            
            logger.debug(f"[ID:TH009] ChatStreamingWorker configured for model: {model}")
            
        except Exception as e:
            logger.error(f"[ID:TH010] Error configuring chat streaming worker: {e}")
    
    def _stream_operation(self):
        """Stream chat responses from Ollama."""
        try:
            self._log_thread_info("starting chat streaming")
            
            # Get configuration
            context_messages = self._configuration.get('context_messages', [])
            model = self._configuration.get('model', 'llama2')
            temperature = self._configuration.get('temperature', 0.7)
            config_manager = self._configuration.get('config_manager')
            
            if not config_manager:
                raise ValueError("Configuration manager is required for chat streaming")
            
            # Prepare request data
            request_data = {
                "model": model,
                "messages": context_messages,
                "stream": True,
                "options": {
                    "temperature": temperature,
                    "num_predict": config_manager.get_max_tokens(),
                    "top_p": config_manager.get_top_p(),
                    "frequency_penalty": config_manager.get_frequency_penalty(),
                    "presence_penalty": config_manager.get_presence_penalty()
                }
            }
            
            # Get Ollama URL
            ollama_url = config_manager.get_ollama_url()
            stream_url = f"{ollama_url}/api/chat"
            
            logger.debug(f"[ID:TH011] Starting chat streaming to: {stream_url}")
            self.progress_updated.emit("Starting chat streaming...")
            
            # Make streaming request
            response = requests.post(
                stream_url,
                json=request_data,
                stream=True,
                timeout=30
            )
            
            if response.status_code != 200:
                error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                logger.error(f"[ID:TH012] {error_msg}")
                self.error.emit(error_msg)
                return
            
            # Process streaming response
            chunk_count = 0
            for line in response.iter_lines():
                if self._should_stop:
                    logger.debug("[ID:TH013] Chat streaming stopped by user")
                    break
                
                if line:
                    try:
                        # Parse JSON response
                        data = json.loads(line.decode('utf-8'))
                        
                        if 'message' in data:
                            content = data['message'].get('content', '')
                            if content:
                                chunk_count += 1
                                self.chunk_received.emit(content)
                                
                                # Update progress periodically
                                if chunk_count % 10 == 0:
                                    self.progress_updated.emit(f"Received {chunk_count} chunks...")
                        
                        # Check for done signal
                        if data.get('done', False):
                            logger.debug(f"[ID:TH014] Chat streaming completed - Total chunks: {chunk_count}")
                            break
                            
                    except json.JSONDecodeError as e:
                        logger.warning(f"[ID:TH015] JSON decode error: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"[ID:TH016] Error processing streaming chunk: {e}")
                        self.error.emit(f"Error processing chunk: {str(e)}")
                        break
            
            self.progress_updated.emit(f"Chat streaming completed - {chunk_count} chunks")
            logger.debug(f"[ID:TH017] Chat streaming finished - Total chunks: {chunk_count}")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during chat streaming: {str(e)}"
            logger.error(f"[ID:TH018] {error_msg}")
            self.error.emit(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error during chat streaming: {str(e)}"
            logger.error(f"[ID:TH019] {error_msg}")
            logger.error(f"[ID:TH020] Chat streaming error traceback: {traceback.format_exc()}")
            self.error.emit(error_msg)
        finally:
            self._running = False
            self.finished.emit()


class AudioStreamingWorker(StreamingWorker):
    """
    Worker for streaming audio processing.
    
    This is a long-running operation that needs:
    - Continuous audio processing
    - Signal/slot communication for audio chunks
    - Persistent thread lifecycle
    - Reusable configuration for thread pools
    """
    
    def configure_audio_streaming(self, audio_source: str, sample_rate: int = 16000, chunk_size: int = 1024):
        """
        Configure the worker for audio streaming.
        
        Args:
            audio_source: Source of audio data
            sample_rate: Audio sample rate
            chunk_size: Size of audio chunks
        """
        try:
            super().configure_streaming(
                audio_source=audio_source,
                sample_rate=sample_rate,
                chunk_size=chunk_size
            )
            
            # Store configuration for audio streaming
            self._configuration.update({
                'audio_source': audio_source,
                'sample_rate': sample_rate,
                'chunk_size': chunk_size
            })
            
            logger.debug(f"[ID:TH021] AudioStreamingWorker configured for source: {audio_source}")
            
        except Exception as e:
            logger.error(f"[ID:TH022] Error configuring audio streaming worker: {e}")
    
    def start_audio_streaming(self):
        """Start audio streaming operation."""
        try:
            self._log_thread_info("starting audio streaming")
            self._running = True
            self._should_stop = False
            self._start_time = time.time()
            
            # Start the actual audio streaming operation
            self._stream_operation()
            
        except Exception as e:
            logger.error(f"[ID:TH023] Error starting audio streaming: {e}")
            self.error.emit(f"Failed to start audio streaming: {str(e)}")
    
    def _stream_operation(self, audio_source: str, sample_rate: int = 16000, 
                         chunk_size: int = 1024):
        """
        Stream audio processing.
        
        Args:
            audio_source: Source of audio data
            sample_rate: Audio sample rate
            chunk_size: Size of audio chunks
        """
        try:
            self._log_thread_info("starting audio streaming operation")
            
            # Get configuration
            audio_source = self._configuration.get('audio_source', audio_source)
            sample_rate = self._configuration.get('sample_rate', sample_rate)
            chunk_size = self._configuration.get('chunk_size', chunk_size)
            
            logger.debug(f"[ID:TH024] Audio streaming from: {audio_source}")
            self.progress_updated.emit("Starting audio streaming...")
            
            # Simulate audio processing (replace with actual implementation)
            chunk_count = 0
            while self._running and not self._should_stop:
                try:
                    # Simulate audio chunk processing
                    time.sleep(0.1)  # Simulate processing time
                    chunk_count += 1
                    
                    # Emit simulated audio chunk
                    simulated_chunk = f"audio_chunk_{chunk_count}"
                    self.chunk_received.emit(simulated_chunk)
                    
                    # Update progress periodically
                    if chunk_count % 10 == 0:
                        self.progress_updated.emit(f"Processed {chunk_count} audio chunks...")
                    
                    # Simulate completion after some chunks
                    if chunk_count >= 100:
                        break
                        
                except Exception as e:
                    logger.error(f"[ID:TH025] Error processing audio chunk: {e}")
                    self.error.emit(f"Error processing audio chunk: {str(e)}")
                    break
            
            self.progress_updated.emit(f"Audio streaming completed - {chunk_count} chunks")
            logger.debug(f"[ID:TH026] Audio streaming finished - Total chunks: {chunk_count}")
            
        except Exception as e:
            error_msg = f"Unexpected error during audio streaming: {str(e)}"
            logger.error(f"[ID:TH027] {error_msg}")
            logger.error(f"[ID:TH028] Audio streaming error traceback: {traceback.format_exc()}")
            self.error.emit(error_msg)
        finally:
            self._running = False
            self.finished.emit()


class MonitoringWorker(StreamingWorker):
    """
    Worker for continuous monitoring tasks.
    
    This is a long-running operation that needs:
    - Continuous monitoring of system resources
    - Periodic status updates
    - Signal/slot communication for monitoring updates
    - Reusable configuration for thread pools
    """
    
    resource_updated = Signal(dict)  # Emitted when resource usage changes
    alert_triggered = Signal(str)  # Emitted when alert condition is met
    
    def configure_monitoring(self, monitor_interval: float = 1.0, alert_threshold: float = 0.8):
        """
        Configure the worker for monitoring.
        
        Args:
            monitor_interval: Interval between monitoring checks
            alert_threshold: Threshold for triggering alerts
        """
        try:
            super().configure_streaming(
                monitor_interval=monitor_interval,
                alert_threshold=alert_threshold
            )
            
            # Store configuration for monitoring
            self._configuration.update({
                'monitor_interval': monitor_interval,
                'alert_threshold': alert_threshold
            })
            
            logger.debug(f"[ID:TH029] MonitoringWorker configured - interval: {monitor_interval}s")
            
        except Exception as e:
            logger.error(f"[ID:TH030] Error configuring monitoring worker: {e}")
    
    def start_monitoring(self):
        """Start monitoring operation."""
        try:
            self._log_thread_info("starting monitoring")
            self._running = True
            self._should_stop = False
            self._start_time = time.time()
            
            # Start the actual monitoring operation
            self._stream_operation()
            
        except Exception as e:
            logger.error(f"[ID:TH031] Error starting monitoring: {e}")
            self.error.emit(f"Failed to start monitoring: {str(e)}")
    
    def _stream_operation(self, monitor_interval: float = 1.0, 
                         alert_threshold: float = 0.8):
        """
        Monitor system resources continuously.
        
        Args:
            monitor_interval: Interval between monitoring checks
            alert_threshold: Threshold for triggering alerts
        """
        try:
            logger.debug(f"[ID:TH032] Monitoring started - Interval: {monitor_interval}s")
            self.progress_updated.emit("Starting system monitoring...")
            
            # Get configuration
            monitor_interval = self._configuration.get('monitor_interval', monitor_interval)
            alert_threshold = self._configuration.get('alert_threshold', alert_threshold)
            
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
                    logger.error(f"[ID:TH033] Monitoring iteration error: {e}")
                    time.sleep(monitor_interval)
                    continue
            
            logger.debug("[ID:TH034] Monitoring completed")
            self.progress_updated.emit("System monitoring stopped")
            
        except Exception as e:
            error_msg = f"Unexpected error during monitoring: {str(e)}"
            logger.error(f"[ID:TH035] {error_msg}")
            logger.error(f"[ID:TH036] Monitoring error traceback: {traceback.format_exc()}")
            self.error.emit(error_msg)
        finally:
            self._running = False
            self.finished.emit() 
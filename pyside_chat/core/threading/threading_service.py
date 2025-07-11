"""
Threading Service - Integrates QThread/QRunnable architecture with existing chat system.

This service provides:
- Backward compatibility with existing Worker class
- Integration of new QThread and QRunnable components
- Unified interface for all threading operations
- Migration path from old to new architecture
"""

from PySide6.QtCore import QObject, Signal, QThread, Qt
import time
import traceback
from typing import Dict, List, Any, Optional, Callable
from pyside_chat.core.logging.logger import CustomLogger

# Import new threading components
from .qthread_workers import ChatStreamingWorker, AudioStreamingWorker, MonitoringWorker
from .qrunnable_tasks import MessageProcessingTask, FileProcessingTask, DataProcessingTask
from .thread_pool_manager import get_global_thread_pool_manager
from .thread_monitor import get_global_thread_monitor

logger = CustomLogger.get_logger(__name__)


class ThreadingService(QObject):
    """
    Service that manages all threading operations in the chat application.
    
    This service provides:
    - Unified interface for QThread and QRunnable operations
    - Backward compatibility with existing Worker class
    - Integration with existing event system
    - Monitoring and debugging capabilities
    """
    
    # Signals for backward compatibility
    worker_chunk_received = Signal(str)  # For streaming chunks
    worker_progress_updated = Signal(str)  # For progress updates
    worker_finished = Signal()  # For completion
    worker_error = Signal(str)  # For errors
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize threading managers
        self.thread_pool_manager = get_global_thread_pool_manager()
        self.thread_monitor = get_global_thread_monitor()
        
        # QThread workers for long-running tasks
        self.chat_streaming_worker = None
        self.chat_streaming_thread = None
        self.audio_streaming_worker = None
        self.audio_streaming_thread = None
        self.monitoring_worker = None
        self.monitoring_thread = None
        
        # QRunnable tasks tracking
        self.active_tasks = {}
        
        # Backward compatibility
        self.legacy_worker = None
        self.legacy_thread = None
        
        logger.debug("[ID:TS001] ThreadingService initialized")
    
    def start_chat_streaming(self, messages: List[Dict], model: str, temperature: float,
                            ollama_url: str, max_tokens: int, top_p: float,
                            frequency_penalty: float, presence_penalty: float) -> bool:
        """
        Start chat streaming using QThread (long-running, persistent task).
        
        Args:
            messages: List of conversation messages
            model: Model name to use
            temperature: Temperature setting
            ollama_url: Ollama server URL
            max_tokens: Maximum tokens to generate
            top_p: Top-p sampling parameter
            frequency_penalty: Frequency penalty parameter
            presence_penalty: Presence penalty parameter
            
        Returns:
            bool: True if streaming started successfully
        """
        try:
            logger.debug(f"[ID:TS002] Starting chat streaming for model: {model}")
            
            # Clean up any existing streaming
            self.stop_chat_streaming()
            
            # Create QThread worker for streaming
            self.chat_streaming_worker = ChatStreamingWorker()
            self.chat_streaming_thread = QThread()
            self.chat_streaming_thread.setObjectName(f"ChatStreamingThread_{id(self.chat_streaming_thread)}")
            
            # Register thread for monitoring
            self.thread_monitor.register_thread(
                self.chat_streaming_thread, 
                thread_type="chat_streaming",
                metadata={'model': model, 'temperature': temperature}
            )
            
            # Move worker to thread
            self.chat_streaming_worker.moveToThread(self.chat_streaming_thread)
            
            # Connect signals with QueuedConnection for thread safety
            self.chat_streaming_worker.chunk_received.connect(
                self._on_chat_chunk_received, Qt.ConnectionType.QueuedConnection
            )
            self.chat_streaming_worker.progress_updated.connect(
                self._on_chat_progress_updated, Qt.ConnectionType.QueuedConnection
            )
            self.chat_streaming_worker.finished.connect(
                self._on_chat_streaming_finished, Qt.ConnectionType.QueuedConnection
            )
            self.chat_streaming_worker.error.connect(
                self._on_chat_streaming_error, Qt.ConnectionType.QueuedConnection
            )
            
            # Connect thread signals
            self.chat_streaming_thread.started.connect(
                lambda: self.chat_streaming_worker.start_streaming(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    ollama_url=ollama_url,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )
            )
            
            self.chat_streaming_thread.finished.connect(
                lambda: self.thread_monitor.unregister_thread(self.chat_streaming_thread.objectName())
            )
            
            # Start the thread
            self.chat_streaming_thread.start()
            
            logger.debug(f"[ID:TS003] Chat streaming thread started: {self.chat_streaming_thread.objectName()}")
            return True
            
        except Exception as e:
            logger.error(f"[ID:TS004] Error starting chat streaming: {e}")
            logger.error(f"[ID:TS005] Chat streaming error traceback: {traceback.format_exc()}")
            return False
    
    def stop_chat_streaming(self):
        """Stop chat streaming safely."""
        try:
            if self.chat_streaming_worker and self.chat_streaming_worker.is_running():
                logger.debug("[ID:TS006] Stopping chat streaming")
                self.chat_streaming_worker.stop()
            
            if self.chat_streaming_thread and self.chat_streaming_thread.isRunning():
                self.chat_streaming_thread.quit()
                if not self.chat_streaming_thread.wait(5000):  # 5 second timeout
                    logger.warning("[ID:TS007] Chat streaming thread did not quit within timeout")
                    self.chat_streaming_thread.terminate()
                    self.chat_streaming_thread.wait(2000)
                
                self.chat_streaming_thread.deleteLater()
                self.chat_streaming_thread = None
                self.chat_streaming_worker = None
                
                logger.debug("[ID:TS008] Chat streaming stopped")
            
        except Exception as e:
            logger.error(f"[ID:TS009] Error stopping chat streaming: {e}")
    
    def process_message_spell_check(self, message: str) -> str:
        """
        Process message spell check using QRunnable (short-lived, fire-and-forget task).
        
        Args:
            message: Message to spell check
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TS010] Processing message spell check: {message[:50]}...")
            
            # Create QRunnable task for spell checking
            spell_check_task = MessageProcessingTask(
                message=message,
                task_type="spell_check"
            )
            spell_check_task.result_ready.connect(self.on_message_processed)
            spell_check_task.error_occurred.connect(self.on_message_processing_error)
            
            # Start task using thread pool manager
            task_id = self.thread_pool_manager.start_task(spell_check_task)
            self.active_tasks[task_id] = {
                'type': 'spell_check',
                'message': message,
                'start_time': time.time()
            }
            
            logger.debug(f"[ID:TS011] Spell check task started: {task_id}")
            return task_id
            
        except Exception as e:
            logger.error(f"[ID:TS012] Error starting spell check task: {e}")
            return ""
    
    def process_message_formatting(self, message: str) -> str:
        """
        Process message formatting using QRunnable.
        
        Args:
            message: Message to format
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TS013] Processing message formatting: {message[:50]}...")
            
            # Create QRunnable task for formatting
            formatting_task = MessageProcessingTask(
                message=message,
                task_type="formatting"
            )
            formatting_task.result_ready.connect(self.on_message_processed)
            formatting_task.error_occurred.connect(self.on_message_processing_error)
            
            # Start task using thread pool manager
            task_id = self.thread_pool_manager.start_task(formatting_task)
            self.active_tasks[task_id] = {
                'type': 'formatting',
                'message': message,
                'start_time': time.time()
            }
            
            logger.debug(f"[ID:TS014] Formatting task started: {task_id}")
            return task_id
            
        except Exception as e:
            logger.error(f"[ID:TS015] Error starting formatting task: {e}")
            return ""
    
    def process_file_operation(self, file_path: str, operation: str, **kwargs) -> str:
        """
        Process file operation using QRunnable.
        
        Args:
            file_path: Path to the file
            operation: Operation to perform (read, write, process)
            **kwargs: Additional arguments for the operation
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TS016] Processing file operation: {operation} on {file_path}")
            
            # Create QRunnable task for file operation
            file_task = FileProcessingTask(
                file_path=file_path,
                operation=operation,
                **kwargs
            )
            file_task.result_ready.connect(self.on_file_processed)
            file_task.error_occurred.connect(self.on_file_processing_error)
            
            # Start task using thread pool manager
            task_id = self.thread_pool_manager.start_task(file_task)
            self.active_tasks[task_id] = {
                'type': 'file_operation',
                'file_path': file_path,
                'operation': operation,
                'start_time': time.time()
            }
            
            logger.debug(f"[ID:TS017] File operation task started: {task_id}")
            return task_id
            
        except Exception as e:
            logger.error(f"[ID:TS018] Error starting file operation task: {e}")
            return ""
    
    # Backward compatibility methods
    
    def create_legacy_worker(self, context_messages, chosen_model, temperature):
        """
        Create legacy worker for backward compatibility.
        
        This method provides the same interface as the old Worker class
        but uses the new QThread architecture internally.
        """
        try:
            logger.debug(f"[ID:TS019] Creating legacy worker for model: {chosen_model}")
            
            # Clean up any existing legacy worker
            self.cleanup_legacy_worker()
            
            # Create QThread worker for streaming
            self.legacy_worker = ChatStreamingWorker()
            self.legacy_thread = QThread()
            self.legacy_thread.setObjectName(f"LegacyWorkerThread_{id(self.legacy_thread)}")
            
            # Register thread for monitoring
            self.thread_monitor.register_thread(
                self.legacy_thread, 
                thread_type="legacy_worker",
                metadata={'model': chosen_model, 'temperature': temperature}
            )
            
            # Move worker to thread
            self.legacy_worker.moveToThread(self.legacy_thread)
            
            # Connect signals for backward compatibility
            self.legacy_worker.chunk_received.connect(
                self.worker_chunk_received, Qt.ConnectionType.QueuedConnection
            )
            self.legacy_worker.progress_updated.connect(
                self.worker_progress_updated, Qt.ConnectionType.QueuedConnection
            )
            self.legacy_worker.finished.connect(
                self.worker_finished, Qt.ConnectionType.QueuedConnection
            )
            self.legacy_worker.error.connect(
                self.worker_error, Qt.ConnectionType.QueuedConnection
            )
            
            # Connect thread signals
            config_manager = self.service_manager.config_manager if hasattr(self, 'service_manager') else None
            if config_manager:
                self.legacy_thread.started.connect(
                    lambda: self._start_legacy_worker_stream(context_messages, chosen_model, temperature, config_manager)
                )
            
            self.legacy_thread.finished.connect(self._on_legacy_worker_thread_finished)
            
            # Start the thread
            self.legacy_thread.start()
            
            logger.debug(f"[ID:TS020] Legacy worker thread started: {self.legacy_thread.objectName()}")
            
        except Exception as e:
            logger.error(f"[ID:TS021] Error creating legacy worker: {e}")
            logger.error(f"[ID:TS022] Legacy worker creation traceback: {traceback.format_exc()}")
    
    def _start_legacy_worker_stream(self, context_messages, chosen_model, temperature, config_manager):
        """Start the legacy worker stream."""
        try:
            logger.debug(f"[ID:TS023] Starting legacy worker stream")
            
            if self.legacy_worker:
                self.legacy_worker.start_streaming(
                    messages=context_messages,
                    model=chosen_model,
                    temperature=temperature,
                    ollama_url=config_manager.get_ollama_url(),
                    max_tokens=config_manager.get_max_tokens(),
                    top_p=config_manager.get_top_p(),
                    frequency_penalty=config_manager.get_frequency_penalty(),
                    presence_penalty=config_manager.get_presence_penalty()
                )
            
        except Exception as e:
            logger.error(f"[ID:TS024] Error starting legacy worker stream: {e}")
    
    def cleanup_legacy_worker(self):
        """Clean up legacy worker safely."""
        try:
            if self.legacy_worker and self.legacy_worker.is_running():
                logger.debug("[ID:TS025] Stopping legacy worker")
                self.legacy_worker.stop()
            
            if self.legacy_thread and self.legacy_thread.isRunning():
                self.legacy_thread.quit()
                if not self.legacy_thread.wait(5000):  # 5 second timeout
                    logger.warning("[ID:TS026] Legacy worker thread did not quit within timeout")
                    self.legacy_thread.terminate()
                    self.legacy_thread.wait(2000)
                
                self.legacy_thread.deleteLater()
                self.legacy_thread = None
                self.legacy_worker = None
                
                logger.debug("[ID:TS027] Legacy worker stopped")
            
        except Exception as e:
            logger.error(f"[ID:TS028] Error cleaning up legacy worker: {e}")
    
    def _on_legacy_worker_thread_finished(self):
        """Handle legacy worker thread finished."""
        try:
            logger.debug("[ID:TS029] Legacy worker thread finished")
            
            # Clean up thread reference
            if self.legacy_thread:
                try:
                    self.thread_monitor.unregister_thread(self.legacy_thread.objectName())
                    self.legacy_thread.deleteLater()
                    logger.debug("[ID:TS030] Legacy worker thread marked for deletion")
                except Exception as e:
                    logger.error(f"[ID:TS031] Error deleting legacy worker thread: {e}")
                finally:
                    self.legacy_thread = None
                    self.legacy_worker = None
            else:
                logger.debug("[ID:TS032] No legacy worker thread to clean up")
                
        except Exception as e:
            logger.error(f"[ID:TS033] Error handling legacy worker thread finished: {e}")
    
    # Signal handlers for QThread workers
    
    def _on_chat_chunk_received(self, chunk: str):
        """Handle chat chunk received from streaming worker."""
        try:
            logger.debug(f"[ID:TS034] Received chat chunk: {chunk[:50]}...")
            logger.debug(f"[ID:TS034A] Chunk length: {len(chunk)}")
            # Emit signal for backward compatibility
            self.worker_chunk_received.emit(chunk)
            logger.debug(f"[ID:TS034B] Emitted worker_chunk_received signal")
            
        except Exception as e:
            logger.error(f"[ID:TS035] Error handling chat chunk: {e}")
    
    def _on_chat_progress_updated(self, progress: str):
        """Handle chat progress update from streaming worker."""
        try:
            logger.debug(f"[ID:TS036] Chat progress: {progress}")
            # Emit signal for backward compatibility
            self.worker_progress_updated.emit(progress)
            logger.debug(f"[ID:TS036A] Emitted worker_progress_updated signal")
            
        except Exception as e:
            logger.error(f"[ID:TS037] Error handling chat progress: {e}")
    
    def _on_chat_streaming_finished(self):
        """Handle chat streaming finished."""
        try:
            logger.debug("[ID:TS038] Chat streaming finished")
            # Emit signal for backward compatibility
            self.worker_finished.emit()
            logger.debug(f"[ID:TS038A] Emitted worker_finished signal")
            
        except Exception as e:
            logger.error(f"[ID:TS039] Error handling chat streaming finished: {e}")
    
    def _on_chat_streaming_error(self, error: str):
        """Handle chat streaming error."""
        try:
            logger.error(f"[ID:TS040] Chat streaming error: {error}")
            # Emit signal for backward compatibility
            self.worker_error.emit(error)
            logger.debug(f"[ID:TS040A] Emitted worker_error signal")
            
        except Exception as e:
            logger.error(f"[ID:TS041] Error handling chat streaming error: {e}")
    
    # Callback methods for QRunnable tasks (invoked via QMetaObject.invokeMethod)
    
    def on_message_processed(self, task_type: str, result: Dict[str, Any]):
        """Handle message processing completion."""
        try:
            logger.debug(f"[ID:TS042] Message processing completed: {task_type}")
            
            if task_type == "spell_check":
                if result.get('has_corrections', False):
                    logger.info(f"[ID:TS043] Spell check found corrections: {result['corrections']}")
                else:
                    logger.debug("[ID:TS044] Spell check completed - no corrections needed")
                    
            elif task_type == "formatting":
                if result.get('changes_made', False):
                    logger.info(f"[ID:TS045] Formatting applied: {result['formatted']}")
                else:
                    logger.debug("[ID:TS046] Formatting completed - no changes needed")
            
            # Handle the result (e.g., update UI, apply corrections)
            # This can be overridden by subclasses or connected to signals
            
        except Exception as e:
            logger.error(f"[ID:TS047] Error handling message processing result: {e}")
    
    def on_message_processing_error(self, task_type: str, error_message: str):
        """Handle message processing error."""
        try:
            logger.error(f"[ID:TS048] Message processing error ({task_type}): {error_message}")
            # Handle the error (e.g., show error message to user)
            # This can be overridden by subclasses or connected to signals
            
        except Exception as e:
            logger.error(f"[ID:TS049] Error handling message processing error: {e}")
    
    def on_file_processed(self, operation: str, file_path: str, result: Dict[str, Any]):
        """Handle file processing completion."""
        try:
            logger.debug(f"[ID:TS050] File processing completed: {operation} on {file_path}")
            
            if 'error' in result:
                logger.error(f"[ID:TS051] File processing error: {result['error']}")
            else:
                logger.info(f"[ID:TS052] File processing successful: {result}")
            
            # Handle the result (e.g., update UI, load file content)
            # This can be overridden by subclasses or connected to signals
            
        except Exception as e:
            logger.error(f"[ID:TS053] Error handling file processing result: {e}")
    
    def on_file_processing_error(self, operation: str, file_path: str, error_message: str):
        """Handle file processing error."""
        try:
            logger.error(f"[ID:TS054] File processing error ({operation} on {file_path}): {error_message}")
            # Handle the error (e.g., show error message to user)
            # This can be overridden by subclasses or connected to signals
            
        except Exception as e:
            logger.error(f"[ID:TS055] Error handling file processing error: {e}")
    
    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return {
                'qthread_workers': {
                    'chat_streaming': {
                        'active': self.chat_streaming_worker is not None,
                        'running': self.chat_streaming_worker.is_running() if self.chat_streaming_worker else False,
                        'thread_name': self.chat_streaming_thread.objectName() if self.chat_streaming_thread else None
                    },
                    'legacy_worker': {
                        'active': self.legacy_worker is not None,
                        'running': self.legacy_worker.is_running() if self.legacy_worker else False,
                        'thread_name': self.legacy_thread.objectName() if self.legacy_thread else None
                    }
                },
                'qrunnable_tasks': {
                    'active_tasks': len(self.active_tasks),
                    'pool_status': self.thread_pool_manager.get_pool_status()
                },
                'monitoring': {
                    'thread_monitor_stats': self.thread_monitor.stats,
                    'resource_usage': self.thread_monitor.get_resource_usage()
                }
            }
            
        except Exception as e:
            logger.error(f"[ID:TS056] Error getting threading status: {e}")
            return {}
    
    def cleanup(self):
        """Clean up all threading resources."""
        try:
            logger.debug("[ID:TS057] Cleaning up ThreadingService")
            
            # Stop QThread workers
            self.stop_chat_streaming()
            self.cleanup_legacy_worker()
            
            # Wait for QRunnable tasks to complete
            self.thread_pool_manager.wait_for_all_tasks(timeout=10.0)
            
            # Clean up active tasks
            self.active_tasks.clear()
            
            logger.debug("[ID:TS058] ThreadingService cleanup complete")
            
        except Exception as e:
            logger.error(f"[ID:TS059] Error during ThreadingService cleanup: {e}")


# Global threading service instance
_global_threading_service: Optional[ThreadingService] = None


def get_global_threading_service() -> ThreadingService:
    """
    Get the global threading service instance.
    
    Returns:
        ThreadingService: Global threading service
    """
    global _global_threading_service
    
    if _global_threading_service is None:
        _global_threading_service = ThreadingService()
        logger.debug("[ID:TS060] Created global ThreadingService")
    
    return _global_threading_service


def shutdown_global_threading_service():
    """Shutdown the global threading service."""
    global _global_threading_service
    
    if _global_threading_service:
        _global_threading_service.cleanup()
        _global_threading_service = None
        logger.debug("[ID:TS061] Shutdown global ThreadingService") 
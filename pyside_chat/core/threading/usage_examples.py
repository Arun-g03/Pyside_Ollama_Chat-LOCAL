"""
Usage examples for QThread vs QRunnable in the chat application.

This file demonstrates the clear distinction between:
- QThread: For long-running, persistent tasks with signal/slot communication
- QRunnable: For short-lived, fire-and-forget tasks using thread pool
"""

from PySide6.QtCore import QThread, Qt, QMetaObject, Q_ARG
from PySide6.QtWidgets import QApplication
import time
import traceback
from typing import Dict, List, Any

from .qthread_workers import ChatStreamingWorker, AudioStreamingWorker
from .qrunnable_tasks import MessageProcessingTask, FileProcessingTask
from .thread_pool_manager import get_global_thread_pool_manager
from .thread_monitor import get_global_thread_monitor
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ChatApplicationExample:
    """
    Example class showing how to use QThread and QRunnable in a chat application.
    
    This demonstrates the clear distinction between:
    - QThread: For streaming chat responses (long-running, persistent)
    - QRunnable: For message processing (short-lived, fire-and-forget)
    """
    
    def __init__(self):
        self.thread_pool_manager = get_global_thread_pool_manager()
        self.thread_monitor = get_global_thread_monitor()
        
        # QThread workers for long-running tasks
        self.chat_streaming_worker = None
        self.chat_streaming_thread = None
        self.audio_streaming_worker = None
        self.audio_streaming_thread = None
        
        # QRunnable tasks for short-lived operations
        self.active_tasks = {}
        
        logger.debug("[ID:EX001] ChatApplicationExample initialized")
    
    def start_chat_streaming(self, messages: List[Dict], model: str, temperature: float,
                            ollama_url: str, max_tokens: int, top_p: float,
                            frequency_penalty: float, presence_penalty: float):
        """
        Start chat streaming using QThread (long-running, persistent task).
        
        This is a QThread use case because:
        - It's a long-running operation (streaming responses)
        - It needs continuous signal/slot communication
        - It has complex state management
        - It needs to be cancellable
        """
        try:
            logger.debug(f"[ID:EX002] Starting chat streaming for model: {model}")
            
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
            
            logger.debug(f"[ID:EX003] Chat streaming thread started: {self.chat_streaming_thread.objectName()}")
            
        except Exception as e:
            logger.error(f"[ID:EX004] Error starting chat streaming: {e}")
            logger.error(f"[ID:EX005] Chat streaming error traceback: {traceback.format_exc()}")
    
    def stop_chat_streaming(self):
        """Stop chat streaming safely."""
        try:
            if self.chat_streaming_worker and self.chat_streaming_worker.is_running():
                logger.debug("[ID:EX006] Stopping chat streaming")
                self.chat_streaming_worker.stop()
            
            if self.chat_streaming_thread and self.chat_streaming_thread.isRunning():
                self.chat_streaming_thread.quit()
                if not self.chat_streaming_thread.wait(5000):  # 5 second timeout
                    logger.warning("[ID:EX007] Chat streaming thread did not quit within timeout")
                    self.chat_streaming_thread.terminate()
                    self.chat_streaming_thread.wait(2000)
                
                self.chat_streaming_thread.deleteLater()
                self.chat_streaming_thread = None
                self.chat_streaming_worker = None
                
                logger.debug("[ID:EX008] Chat streaming stopped")
            
        except Exception as e:
            logger.error(f"[ID:EX009] Error stopping chat streaming: {e}")
    
    def process_message_spell_check(self, message: str):
        """
        Process message spell check using QRunnable (short-lived, fire-and-forget task).
        
        This is a QRunnable use case because:
        - It's a short-lived operation
        - It doesn't need continuous communication
        - It's a one-time processing task
        - It can be queued and executed by thread pool
        """
        try:
            logger.debug(f"[ID:EX010] Processing message spell check: {message[:50]}...")
            
            # Create QRunnable task for spell checking
            spell_check_task = MessageProcessingTask(
                message=message,
                callback=self,
                task_type="spell_check"
            )
            
            # Start task using thread pool manager
            task_id = self.thread_pool_manager.start_task(spell_check_task)
            self.active_tasks[task_id] = {
                'type': 'spell_check',
                'message': message,
                'start_time': time.time()
            }
            
            logger.debug(f"[ID:EX011] Spell check task started: {task_id}")
            
        except Exception as e:
            logger.error(f"[ID:EX012] Error starting spell check task: {e}")
    
    def process_message_formatting(self, message: str):
        """
        Process message formatting using QRunnable.
        """
        try:
            logger.debug(f"[ID:EX013] Processing message formatting: {message[:50]}...")
            
            # Create QRunnable task for formatting
            formatting_task = MessageProcessingTask(
                message=message,
                callback=self,
                task_type="formatting"
            )
            
            # Start task using thread pool manager
            task_id = self.thread_pool_manager.start_task(formatting_task)
            self.active_tasks[task_id] = {
                'type': 'formatting',
                'message': message,
                'start_time': time.time()
            }
            
            logger.debug(f"[ID:EX014] Formatting task started: {task_id}")
            
        except Exception as e:
            logger.error(f"[ID:EX015] Error starting formatting task: {e}")
    
    def process_file_operation(self, file_path: str, operation: str, **kwargs):
        """
        Process file operation using QRunnable.
        """
        try:
            logger.debug(f"[ID:EX016] Processing file operation: {operation} on {file_path}")
            
            # Create QRunnable task for file operation
            file_task = FileProcessingTask(
                file_path=file_path,
                operation=operation,
                callback=self,
                **kwargs
            )
            
            # Start task using thread pool manager
            task_id = self.thread_pool_manager.start_task(file_task)
            self.active_tasks[task_id] = {
                'type': 'file_operation',
                'file_path': file_path,
                'operation': operation,
                'start_time': time.time()
            }
            
            logger.debug(f"[ID:EX017] File operation task started: {task_id}")
            
        except Exception as e:
            logger.error(f"[ID:EX018] Error starting file operation task: {e}")
    
    # Signal handlers for QThread workers
    
    def _on_chat_chunk_received(self, chunk: str):
        """Handle chat chunk received from streaming worker."""
        try:
            logger.debug(f"[ID:EX019] Received chat chunk: {chunk[:50]}...")
            # Handle the chunk (e.g., update UI, accumulate response)
            
        except Exception as e:
            logger.error(f"[ID:EX020] Error handling chat chunk: {e}")
    
    def _on_chat_progress_updated(self, progress: str):
        """Handle chat progress update from streaming worker."""
        try:
            logger.debug(f"[ID:EX021] Chat progress: {progress}")
            # Update progress in UI
            
        except Exception as e:
            logger.error(f"[ID:EX022] Error handling chat progress: {e}")
    
    def _on_chat_streaming_finished(self):
        """Handle chat streaming finished."""
        try:
            logger.debug("[ID:EX023] Chat streaming finished")
            # Handle streaming completion
            
        except Exception as e:
            logger.error(f"[ID:EX024] Error handling chat streaming finished: {e}")
    
    def _on_chat_streaming_error(self, error: str):
        """Handle chat streaming error."""
        try:
            logger.error(f"[ID:EX025] Chat streaming error: {error}")
            # Handle streaming error
            
        except Exception as e:
            logger.error(f"[ID:EX026] Error handling chat streaming error: {e}")
    
    # Callback methods for QRunnable tasks (invoked via QMetaObject.invokeMethod)
    
    def on_message_processed(self, task_type: str, result: Dict[str, Any]):
        """Handle message processing completion."""
        try:
            logger.debug(f"[ID:EX027] Message processing completed: {task_type}")
            
            if task_type == "spell_check":
                if result.get('has_corrections', False):
                    logger.info(f"[ID:EX028] Spell check found corrections: {result['corrections']}")
                else:
                    logger.debug("[ID:EX029] Spell check completed - no corrections needed")
                    
            elif task_type == "formatting":
                if result.get('changes_made', False):
                    logger.info(f"[ID:EX030] Formatting applied: {result['formatted']}")
                else:
                    logger.debug("[ID:EX031] Formatting completed - no changes needed")
            
            # Handle the result (e.g., update UI, apply corrections)
            
        except Exception as e:
            logger.error(f"[ID:EX032] Error handling message processing result: {e}")
    
    def on_message_processing_error(self, task_type: str, error_message: str):
        """Handle message processing error."""
        try:
            logger.error(f"[ID:EX033] Message processing error ({task_type}): {error_message}")
            # Handle the error (e.g., show error message to user)
            
        except Exception as e:
            logger.error(f"[ID:EX034] Error handling message processing error: {e}")
    
    def on_file_processed(self, operation: str, file_path: str, result: Dict[str, Any]):
        """Handle file processing completion."""
        try:
            logger.debug(f"[ID:EX035] File processing completed: {operation} on {file_path}")
            
            if 'error' in result:
                logger.error(f"[ID:EX036] File processing error: {result['error']}")
            else:
                logger.info(f"[ID:EX037] File processing successful: {result}")
            
            # Handle the result (e.g., update UI, load file content)
            
        except Exception as e:
            logger.error(f"[ID:EX038] Error handling file processing result: {e}")
    
    def on_file_processing_error(self, operation: str, file_path: str, error_message: str):
        """Handle file processing error."""
        try:
            logger.error(f"[ID:EX039] File processing error ({operation} on {file_path}): {error_message}")
            # Handle the error (e.g., show error message to user)
            
        except Exception as e:
            logger.error(f"[ID:EX040] Error handling file processing error: {e}")
    
    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return {
                'qthread_workers': {
                    'chat_streaming': {
                        'active': self.chat_streaming_worker is not None,
                        'running': self.chat_streaming_worker.is_running() if self.chat_streaming_worker else False,
                        'thread_name': self.chat_streaming_thread.objectName() if self.chat_streaming_thread else None
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
            logger.error(f"[ID:EX041] Error getting threading status: {e}")
            return {}
    
    def cleanup(self):
        """Clean up all threading resources."""
        try:
            logger.debug("[ID:EX042] Cleaning up ChatApplicationExample")
            
            # Stop QThread workers
            self.stop_chat_streaming()
            
            # Wait for QRunnable tasks to complete
            self.thread_pool_manager.wait_for_all_tasks(timeout=10.0)
            
            # Clean up active tasks
            self.active_tasks.clear()
            
            logger.debug("[ID:EX043] ChatApplicationExample cleanup complete")
            
        except Exception as e:
            logger.error(f"[ID:EX044] Error during cleanup: {e}")


# Example usage demonstration
def demonstrate_threading_usage():
    """
    Demonstrate the usage of QThread vs QRunnable in a chat application.
    
    This function shows:
    1. How to use QThread for streaming operations
    2. How to use QRunnable for processing tasks
    3. The clear distinction between the two approaches
    """
    
    # Create application instance
    app = ChatApplicationExample()
    
    # Example 1: QThread for streaming chat (long-running, persistent)
    print("=== QThread Example: Chat Streaming ===")
    print("Use QThread for:")
    print("- Long-running operations (streaming)")
    print("- Continuous signal/slot communication")
    print("- Complex state management")
    print("- Cancellable operations")
    
    # Simulate starting chat streaming
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    app.start_chat_streaming(
        messages=messages,
        model="llama2",
        temperature=0.7,
        ollama_url="http://localhost:11434",
        max_tokens=1000,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    # Example 2: QRunnable for message processing (short-lived, fire-and-forget)
    print("\n=== QRunnable Example: Message Processing ===")
    print("Use QRunnable for:")
    print("- Short-lived operations")
    print("- One-time processing tasks")
    print("- Batch operations")
    print("- Fire-and-forget tasks")
    
    # Simulate message processing tasks
    test_messages = [
        "Hello, how are you doing today?",
        "I'm having a great day!",
        "The weather is beautiful outside."
    ]
    
    for message in test_messages:
        # Process spell check
        app.process_message_spell_check(message)
        
        # Process formatting
        app.process_message_formatting(message)
    
    # Example 3: QRunnable for file operations
    print("\n=== QRunnable Example: File Operations ===")
    
    # Simulate file operations
    app.process_file_operation("test_file.txt", "read")
    app.process_file_operation("output.json", "write", content='{"test": "data"}')
    
    # Show threading status
    print("\n=== Threading Status ===")
    status = app.get_threading_status()
    print(f"QThread workers: {status['qthread_workers']}")
    print(f"QRunnable tasks: {status['qrunnable_tasks']}")
    print(f"Monitoring: {status['monitoring']}")
    
    # Cleanup
    app.cleanup()
    
    print("\n=== Demonstration Complete ===")
    print("Key takeaways:")
    print("1. Use QThread for persistent, communication-heavy tasks")
    print("2. Use QRunnable for short-lived, independent tasks")
    print("3. QThread has higher overhead but better for complex operations")
    print("4. QRunnable is more efficient for simple, quick tasks")
    print("5. Both approaches can coexist in the same application")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_threading_usage() 
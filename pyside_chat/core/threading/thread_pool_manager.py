"""
Thread pool manager for handling QRunnable tasks efficiently.

This manager provides:
- Centralized thread pool management
- Task queuing and execution
- Resource monitoring
- Error handling and recovery
"""

from PySide6.QtCore import QThreadPool, QObject, Signal, QTimer
import time
import traceback
from typing import Dict, List, Any, Optional, Callable
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ThreadPoolManager(QObject):
    """
    Manager for handling QRunnable tasks with proper resource management.
    
    This manager provides:
    - Global thread pool management
    - Task queuing and execution
    - Resource monitoring
    - Error handling and recovery
    """
    
    # Signals for monitoring
    task_started = Signal(str)  # task_id
    task_completed = Signal(str)  # task_id
    task_failed = Signal(str, str)  # task_id, error_message
    pool_status_updated = Signal(dict)  # pool statistics
    
    def __init__(self, max_threads: int = 4, parent=None):
        super().__init__(parent)
        self.max_threads = max_threads
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(max_threads)
        
        # Task tracking
        self.active_tasks: Dict[str, Dict] = {}
        self.completed_tasks: List[Dict] = []
        self.failed_tasks: List[Dict] = []
        
        # Queue management
        self.max_queue_size = 50  # Maximum number of tasks in queue
        self.task_queue: List[Dict] = []
        
        # Statistics
        self.stats = {
            'total_tasks': 0,
            'active_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'queued_tasks': 0,
            'pool_utilization': 0.0
        }
        
        # Setup monitoring timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self._update_pool_status)
        self.monitor_timer.start(1000)  # Update every second
        
        logger.debug(f"[ID:TP001] ThreadPoolManager created - Max threads: {max_threads}")
    
    def start_task(self, task, task_id: Optional[str] = None) -> str:
        """
        Start a QRunnable task.
        
        Args:
            task: QRunnable task to execute
            task_id: Optional task identifier
            
        Returns:
            str: Task ID for tracking
        """
        try:
            if task_id is None:
                task_id = f"task_{int(time.time() * 1000)}"
            
            # Check queue size limit
            if len(self.active_tasks) >= self.max_queue_size:
                logger.warning(f"[ID:TP011] Queue full ({len(self.active_tasks)} tasks), rejecting task: {task_id}")
                return task_id
            
            # Track task
            task_info = {
                'id': task_id,
                'start_time': time.time(),
                'status': 'queued',
                'task_type': type(task).__name__
            }
            
            self.active_tasks[task_id] = task_info
            self.stats['total_tasks'] += 1
            self.stats['active_tasks'] += 1
            self.stats['queued_tasks'] = len(self.active_tasks)
            
            logger.debug(f"[ID:TP002] Starting task: {task_id} ({task_info['task_type']})")
            
            # Start the task
            self.thread_pool.start(task)
            
            # Emit signal
            self.task_started.emit(task_id)
            
            return task_id
            
        except Exception as e:
            error_msg = f"Error starting task: {str(e)}"
            logger.error(f"[ID:TP003] {error_msg}")
            logger.error(f"[ID:TP004] Task start traceback: {traceback.format_exc()}")
            
            # Update statistics
            self.stats['failed_tasks'] += 1
            self.stats['active_tasks'] -= 1
            
            # Track failed task
            failed_task = {
                'id': task_id or 'unknown',
                'error': error_msg,
                'timestamp': time.time()
            }
            self.failed_tasks.append(failed_task)
            
            # Emit signal
            self.task_failed.emit(task_id or 'unknown', error_msg)
            
            return task_id or 'unknown'
    
    def wait_for_task(self, task_id: str, timeout: float = 30.0) -> bool:
        """
        Wait for a specific task to complete.
        
        Args:
            task_id: Task identifier
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if task completed, False if timeout
        """
        try:
            start_time = time.time()
            
            while task_id in self.active_tasks:
                if time.time() - start_time > timeout:
                    logger.warning(f"[ID:TP005] Timeout waiting for task: {task_id}")
                    return False
                
                time.sleep(0.1)  # Small delay to avoid busy waiting
            
            logger.debug(f"[ID:TP006] Task completed: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"[ID:TP007] Error waiting for task {task_id}: {e}")
            return False
    
    def wait_for_all_tasks(self, timeout: float = 60.0) -> bool:
        """
        Wait for all active tasks to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if all tasks completed, False if timeout
        """
        try:
            start_time = time.time()
            
            while self.active_tasks:
                if time.time() - start_time > timeout:
                    logger.warning(f"[ID:TP008] Timeout waiting for {len(self.active_tasks)} tasks")
                    return False
                
                time.sleep(0.1)  # Small delay to avoid busy waiting
            
            logger.debug("[ID:TP009] All tasks completed")
            return True
            
        except Exception as e:
            logger.error(f"[ID:TP010] Error waiting for all tasks: {e}")
            return False
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a specific task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            bool: True if task was cancelled, False if not found
        """
        try:
            if task_id in self.active_tasks:
                task_info = self.active_tasks[task_id]
                task_info['status'] = 'cancelled'
                task_info['end_time'] = time.time()
                
                # Move to completed tasks
                self.completed_tasks.append(task_info)
                del self.active_tasks[task_id]
                
                # Update statistics
                self.stats['active_tasks'] -= 1
                self.stats['completed_tasks'] += 1
                
                logger.debug(f"[ID:TP011] Task cancelled: {task_id}")
                self.task_completed.emit(task_id)
                
                return True
            else:
                logger.warning(f"[ID:TP012] Task not found for cancellation: {task_id}")
                return False
                
        except Exception as e:
            logger.error(f"[ID:TP013] Error cancelling task {task_id}: {e}")
            return False
    
    def cancel_all_tasks(self) -> int:
        """
        Cancel all active tasks.
        
        Returns:
            int: Number of tasks cancelled
        """
        try:
            cancelled_count = 0
            
            for task_id in list(self.active_tasks.keys()):
                if self.cancel_task(task_id):
                    cancelled_count += 1
            
            logger.debug(f"[ID:TP014] Cancelled {cancelled_count} tasks")
            return cancelled_count
            
        except Exception as e:
            logger.error(f"[ID:TP015] Error cancelling all tasks: {e}")
            return 0
    
    def get_pool_status(self) -> Dict[str, Any]:
        """
        Get current thread pool status.
        
        Returns:
            dict: Pool status information
        """
        try:
            active_count = self.thread_pool.activeThreadCount()
            max_count = self.thread_pool.maxThreadCount()
            
            return {
                'active_threads': active_count,
                'max_threads': max_count,
                'utilization': (active_count / max_count) * 100 if max_count > 0 else 0,
                'active_tasks': len(self.active_tasks),
                'completed_tasks': len(self.completed_tasks),
                'failed_tasks': len(self.failed_tasks),
                'total_tasks': self.stats['total_tasks']
            }
            
        except Exception as e:
            logger.error(f"[ID:TP016] Error getting pool status: {e}")
            return {}
    
    def get_task_info(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            dict: Task information or None if not found
        """
        try:
            # Check active tasks
            if task_id in self.active_tasks:
                task_info = self.active_tasks[task_id].copy()
                if 'start_time' in task_info:
                    task_info['duration'] = time.time() - task_info['start_time']
                return task_info
            
            # Check completed tasks
            for task in self.completed_tasks:
                if task['id'] == task_id:
                    return task.copy()
            
            # Check failed tasks
            for task in self.failed_tasks:
                if task['id'] == task_id:
                    return task.copy()
            
            return None
            
        except Exception as e:
            logger.error(f"[ID:TP017] Error getting task info for {task_id}: {e}")
            return None
    
    def cleanup_old_tasks(self, max_age_hours: float = 24.0):
        """
        Clean up old completed and failed tasks.
        
        Args:
            max_age_hours: Maximum age in hours for tasks to keep
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            # Clean up completed tasks
            self.completed_tasks = [
                task for task in self.completed_tasks
                if current_time - task.get('end_time', task.get('start_time', 0)) < max_age_seconds
            ]
            
            # Clean up failed tasks
            self.failed_tasks = [
                task for task in self.failed_tasks
                if current_time - task.get('timestamp', 0) < max_age_seconds
            ]
            
            logger.debug(f"[ID:TP018] Cleaned up old tasks (max age: {max_age_hours}h)")
            
        except Exception as e:
            logger.error(f"[ID:TP019] Error cleaning up old tasks: {e}")
    
    def _update_pool_status(self):
        """Update pool status and emit signals."""
        try:
            # Update statistics
            self.stats['active_tasks'] = len(self.active_tasks)
            self.stats['completed_tasks'] = len(self.completed_tasks)
            self.stats['failed_tasks'] = len(self.failed_tasks)
            self.stats['queued_tasks'] = len(self.active_tasks)
            
            # Calculate pool utilization
            active_count = self.thread_pool.activeThreadCount()
            max_count = self.thread_pool.maxThreadCount()
            self.stats['pool_utilization'] = (active_count / max_count) * 100 if max_count > 0 else 0
            
            # Emit status update
            self.pool_status_updated.emit(self.get_pool_status())
            
        except Exception as e:
            logger.error(f"[ID:TP020] Error updating pool status: {e}")
    
    def on_task_completed(self, task_id: str):
        """
        Handle task completion.
        
        Args:
            task_id: Task identifier
        """
        try:
            if task_id in self.active_tasks:
                task_info = self.active_tasks[task_id]
                task_info['status'] = 'completed'
                task_info['end_time'] = time.time()
                
                # Move to completed tasks
                self.completed_tasks.append(task_info)
                del self.active_tasks[task_id]
                
                # Update statistics
                self.stats['active_tasks'] -= 1
                self.stats['completed_tasks'] += 1
                self.stats['queued_tasks'] = len(self.active_tasks)
                
                logger.debug(f"[ID:TP021] Task completed: {task_id}")
                self.task_completed.emit(task_id)
            
        except Exception as e:
            logger.error(f"[ID:TP022] Error handling task completion for {task_id}: {e}")
    
    def on_task_failed(self, task_id: str, error_message: str):
        """
        Handle task failure.
        
        Args:
            task_id: Task identifier
            error_message: Error message
        """
        try:
            if task_id in self.active_tasks:
                task_info = self.active_tasks[task_id]
                task_info['status'] = 'failed'
                task_info['end_time'] = time.time()
                task_info['error'] = error_message
                
                # Move to failed tasks
                self.failed_tasks.append(task_info)
                del self.active_tasks[task_id]
                
                # Update statistics
                self.stats['active_tasks'] -= 1
                self.stats['failed_tasks'] += 1
                self.stats['queued_tasks'] = len(self.active_tasks)
                
                logger.error(f"[ID:TP023] Task failed: {task_id} - {error_message}")
                self.task_failed.emit(task_id, error_message)
            
        except Exception as e:
            logger.error(f"[ID:TP024] Error handling task failure for {task_id}: {e}")
    
    def shutdown(self):
        """Shutdown the thread pool manager."""
        try:
            logger.debug("[ID:TP025] Shutting down ThreadPoolManager")
            
            # Stop monitoring timer
            if self.monitor_timer:
                self.monitor_timer.stop()
            
            # Cancel all active tasks
            self.cancel_all_tasks()
            
            # Wait for remaining tasks
            self.wait_for_all_tasks(timeout=5.0)
            
            # Clean up old tasks
            self.cleanup_old_tasks(max_age_hours=1.0)
            
            logger.debug("[ID:TP026] ThreadPoolManager shutdown complete")
            
        except Exception as e:
            logger.error(f"[ID:TP027] Error during ThreadPoolManager shutdown: {e}")


# Global thread pool manager instance
_global_thread_pool_manager: Optional[ThreadPoolManager] = None


def get_global_thread_pool_manager() -> ThreadPoolManager:
    """
    Get the global thread pool manager instance.
    
    Returns:
        ThreadPoolManager: Global thread pool manager
    """
    global _global_thread_pool_manager
    
    if _global_thread_pool_manager is None:
        _global_thread_pool_manager = ThreadPoolManager(max_threads=4)
        logger.debug("[ID:TP028] Created global ThreadPoolManager")
    
    return _global_thread_pool_manager


def shutdown_global_thread_pool_manager():
    """Shutdown the global thread pool manager."""
    global _global_thread_pool_manager
    
    if _global_thread_pool_manager:
        _global_thread_pool_manager.shutdown()
        _global_thread_pool_manager = None
        logger.debug("[ID:TP029] Shutdown global ThreadPoolManager") 
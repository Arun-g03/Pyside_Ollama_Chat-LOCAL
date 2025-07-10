"""
Threading module for PySide6 chat application.

This module provides clear distinction between QThread and QRunnable usage:
- QThread: For long-running, persistent tasks with signal/slot communication
- QRunnable: For short-lived, fire-and-forget tasks using thread pool
"""

from .qthread_workers import (
    StreamingWorker,
    ChatStreamingWorker,
    AudioStreamingWorker,
    MonitoringWorker
)

from .qrunnable_tasks import (
    MessageProcessingTask,
    FileProcessingTask,
    DataProcessingTask,
    CalculationTask
)

from .thread_pool_manager import ThreadPoolManager, get_global_thread_pool_manager
from .thread_monitor import ThreadMonitor, get_global_thread_monitor
from .threading_service import ThreadingService, get_global_threading_service

__all__ = [
    # QThread Workers
    'StreamingWorker',
    'ChatStreamingWorker', 
    'AudioStreamingWorker',
    'MonitoringWorker',
    
    # QRunnable Tasks
    'MessageProcessingTask',
    'FileProcessingTask',
    'DataProcessingTask',
    'CalculationTask',
    
    # Managers
    'ThreadPoolManager',
    'ThreadMonitor',
    'ThreadingService',
    
    # Global instances
    'get_global_thread_pool_manager',
    'get_global_thread_monitor',
    'get_global_threading_service'
] 
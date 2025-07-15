"""
Threading module for PySide6 chat application.

This module provides clear distinction between QThread and QRunnable usage:
- QThread: For long-running, persistent tasks with signal/slot communication
- QRunnable: For short-lived, fire-and-forget tasks using thread pool
- PersistentThreadPool: For managing reusable threads throughout app lifecycle
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
from .persistent_thread_pool import PersistentThreadPool, get_global_persistent_thread_pool
from .thread_calculator import (
    ThreadCalculator,
    ThreadRecommendations,
    thread_calculator,
    get_thread_recommendations,
    get_pool_thread_count,
    analyze_system
)

# Global instances for shutdown
_global_threading_service = None
_global_persistent_thread_pool = None


def shutdown_global_threading_service():
    """Shutdown the global threading service."""
    global _global_threading_service
    if _global_threading_service:
        try:
            _global_threading_service.cleanup()
            _global_threading_service = None
        except Exception as e:
            from pyside_chat.core.logging.logger import CustomLogger
            logger = CustomLogger.get_logger(__name__)
            logger.error(f"Error shutting down global threading service: {e}")


def shutdown_global_persistent_thread_pool():
    """Shutdown the global persistent thread pool."""
    global _global_persistent_thread_pool
    if _global_persistent_thread_pool:
        try:
            _global_persistent_thread_pool.shutdown()
            _global_persistent_thread_pool = None
        except Exception as e:
            from pyside_chat.core.logging.logger import CustomLogger
            logger = CustomLogger.get_logger(__name__)
            logger.error(
                f"Error shutting down global persistent thread pool: {e}")


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
    'PersistentThreadPool',

    # Thread Calculator
    'ThreadCalculator',
    'ThreadRecommendations',
    'thread_calculator',
    'get_thread_recommendations',
    'get_pool_thread_count',
    'analyze_system',

    # Global instances
    'get_global_thread_pool_manager',
    'get_global_thread_monitor',
    'get_global_threading_service',
    'get_global_persistent_thread_pool',

    # Shutdown functions
    'shutdown_global_threading_service',
    'shutdown_global_persistent_thread_pool'
]

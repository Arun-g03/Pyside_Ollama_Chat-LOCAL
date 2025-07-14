# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *    
from pyside_chat.core.shared_imports.pyside_imports import *


"""
Persistent Thread Pool - Manages long-running threads that stay alive throughout app lifecycle.

This module provides:
- Persistent thread pools for different types of operations
- Thread reuse to avoid creation/destruction overhead
- Better resource management for long-running tasks
- Unified interface for persistent threading operations
"""

logger = CustomLogger.get_logger(__name__)


class PersistentThreadPool(QObject):
    """
    Manages persistent threads that stay alive throughout the application lifecycle.
    
    This pool provides:
    - Thread reuse to avoid creation/destruction overhead
    - Better resource management for long-running tasks
    - Unified interface for persistent threading operations
    """
    
    # Signals for pool management
    thread_available = Signal(str)  # thread_type
    thread_busy = Signal(str)  # thread_type
    pool_status_changed = Signal(dict)  # pool status update
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Thread pools for different types of operations
        self.chat_streaming_pool: List[QThread] = []
        self.audio_streaming_pool: List[QThread] = []
        self.monitoring_pool: List[QThread] = []
        self.voice_processing_pool: List[QThread] = []
        
        # Pool configuration
        self.pool_config = {
            'chat_streaming': {
                'size': 2,  # Keep 2 chat streaming threads ready
                'max_wait_time': 30.0,  # Max time to wait for available thread
                'idle_timeout': 300.0,  # Time before idle thread is cleaned up
                'worker_class': None  # Will be set when needed
            },
            'audio_streaming': {
                'size': 1,  # Keep 1 audio streaming thread ready
                'max_wait_time': 10.0,
                'idle_timeout': 180.0,
                'worker_class': None
            },
            'monitoring': {
                'size': 1,  # Keep 1 monitoring thread ready
                'max_wait_time': 5.0,
                'idle_timeout': 600.0,  # Longer timeout for monitoring
                'worker_class': None
            },
            'voice_processing': {
                'size': 1,  # Keep 1 voice processing thread ready
                'max_wait_time': 15.0,
                'idle_timeout': 240.0,
                'worker_class': None
            }
        }
        
        # Thread tracking
        self.active_threads: Dict[str, Dict] = {}
        self.idle_threads: Dict[str, List[QThread]] = {
            'chat_streaming': [],
            'audio_streaming': [],
            'monitoring': [],
            'voice_processing': []
        }
        
        # Thread lifecycle management
        self.thread_locks: Dict[str, Lock] = {
            'chat_streaming': Lock(),
            'audio_streaming': Lock(),
            'monitoring': Lock(),
            'voice_processing': Lock()
        }
        
        # Cleanup timer for idle threads
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self._cleanup_idle_threads)
        self.cleanup_timer.start(60000)  # Check every minute
        
        logger.debug("[ID:PTP001] PersistentThreadPool initialized")
    
    def initialize_pool(self, thread_type: str, worker_class: type, **kwargs):
        """
        Initialize a thread pool with the specified worker class.
        
        Args:
            thread_type: Type of thread pool to initialize
            worker_class: Worker class to use for this pool
            **kwargs: Additional configuration for the pool
        """
        try:
            if thread_type not in self.pool_config:
                logger.error(f"[ID:PTP002] Unknown thread type: {thread_type}")
                return False
            
            # Update pool configuration
            self.pool_config[thread_type]['worker_class'] = worker_class
            self.pool_config[thread_type].update(kwargs)
            
            # Pre-populate the pool with idle threads
            pool_size = self.pool_config[thread_type]['size']
            logger.debug(f"[ID:PTP003] Initializing {thread_type} pool with {pool_size} threads")
            
            for i in range(pool_size):
                thread = self._create_idle_thread(thread_type, worker_class)
                if thread:
                    self.idle_threads[thread_type].append(thread)
            
            logger.debug(f"[ID:PTP004] {thread_type} pool initialized with {len(self.idle_threads[thread_type])} idle threads")
            return True
            
        except Exception as e:
            logger.error(f"[ID:PTP005] Error initializing {thread_type} pool: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def get_thread(self, thread_type: str, timeout: Optional[float] = None) -> Optional[QThread]:
        """
        Get an available thread from the pool.
        
        Args:
            thread_type: Type of thread to get
            timeout: Maximum time to wait for available thread
            
        Returns:
            QThread: Available thread or None if timeout
        """
        try:
            if thread_type not in self.pool_config:
                logger.error(f"[ID:PTP006] Unknown thread type: {thread_type}")
                return None
            
            lock = self.thread_locks[thread_type]
            max_wait_time = timeout or self.pool_config[thread_type]['max_wait_time']
            
            with lock:
                # Check if we have idle threads available
                if self.idle_threads[thread_type]:
                    thread = self.idle_threads[thread_type].pop(0)
                    self.active_threads[thread.objectName()] = {
                        'type': thread_type,
                        'start_time': time.time(),
                        'status': 'active'
                    }
                    logger.debug(f"[ID:PTP007] Retrieved {thread_type} thread: {thread.objectName()}")
                    self.thread_busy.emit(thread_type)
                    return thread
                
                # No idle threads, create a new one if we haven't reached max
                max_size = self.pool_config[thread_type]['size']
                current_active = len([t for t in self.active_threads.values() if t['type'] == thread_type])
                
                if current_active < max_size:
                    worker_class = self.pool_config[thread_type]['worker_class']
                    if worker_class:
                        thread = self._create_active_thread(thread_type, worker_class)
                        if thread:
                            logger.debug(f"[ID:PTP008] Created new {thread_type} thread: {thread.objectName()}")
                            self.thread_busy.emit(thread_type)
                            return thread
                
                # Wait for a thread to become available
                logger.debug(f"[ID:PTP009] Waiting for {thread_type} thread (timeout: {max_wait_time}s)")
                start_time = time.time()
                
                while time.time() - start_time < max_wait_time:
                    time.sleep(0.1)
                    if self.idle_threads[thread_type]:
                        thread = self.idle_threads[thread_type].pop(0)
                        self.active_threads[thread.objectName()] = {
                            'type': thread_type,
                            'start_time': time.time(),
                            'status': 'active'
                        }
                        logger.debug(f"[ID:PTP010] Retrieved {thread_type} thread after wait: {thread.objectName()}")
                        self.thread_busy.emit(thread_type)
                        return thread
                
                logger.warning(f"[ID:PTP011] Timeout waiting for {thread_type} thread")
                return None
                
        except Exception as e:
            logger.error(f"[ID:PTP012] Error getting {thread_type} thread: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def return_thread(self, thread: QThread):
        """
        Return a thread to the pool for reuse.
        
        Args:
            thread: Thread to return to the pool
        """
        try:
            thread_name = thread.objectName()
            if thread_name not in self.active_threads:
                logger.warning(f"[ID:PTP013] Thread {thread_name} not found in active threads")
                return
            
            thread_info = self.active_threads[thread_name]
            thread_type = thread_info['type']
            
            # Reset thread state
            if hasattr(thread, 'worker') and thread.worker:
                thread.worker.reset_state()
            
            # Move to idle pool
            with self.thread_locks[thread_type]:
                self.idle_threads[thread_type].append(thread)
                del self.active_threads[thread_name]
            
            logger.debug(f"[ID:PTP014] Returned {thread_type} thread to pool: {thread_name}")
            self.thread_available.emit(thread_type)
            
        except Exception as e:
            logger.error(f"[ID:PTP015] Error returning thread {thread.objectName()}: {e}")
            logger.error(traceback.format_exc())
    
    def _create_idle_thread(self, thread_type: str, worker_class: type) -> Optional[QThread]:
        """Create an idle thread for the pool."""
        try:
            thread = QThread()
            thread.setObjectName(f"{thread_type.capitalize()}Thread_{id(thread)}")
            
            # Create worker but don't start it yet
            worker = worker_class()
            worker.moveToThread(thread)
            
            # Store worker reference for later use
            thread.worker = worker
            
            # Register thread for monitoring
            from .thread_monitor import get_global_thread_monitor
            thread_monitor = get_global_thread_monitor()
            thread_monitor.register_thread(thread, thread_type, {'status': 'idle'})
            
            logger.debug(f"[ID:PTP016] Created idle {thread_type} thread: {thread.objectName()}")
            return thread
            
        except Exception as e:
            logger.error(f"[ID:PTP017] Error creating idle {thread_type} thread: {e}")
            return None
    
    def _create_active_thread(self, thread_type: str, worker_class: type) -> Optional[QThread]:
        """Create an active thread for immediate use."""
        try:
            thread = QThread()
            thread.setObjectName(f"{thread_type.capitalize()}Thread_{id(thread)}")
            
            # Create and start worker
            worker = worker_class()
            worker.moveToThread(thread)
            
            # Store worker reference
            thread.worker = worker
            
            # Start the thread
            thread.start()
            
            # Register thread for monitoring
            from .thread_monitor import get_global_thread_monitor
            thread_monitor = get_global_thread_monitor()
            thread_monitor.register_thread(thread, thread_type, {'status': 'active'})
            
            logger.debug(f"[ID:PTP018] Created active {thread_type} thread: {thread.objectName()}")
            return thread
            
        except Exception as e:
            logger.error(f"[ID:PTP019] Error creating active {thread_type} thread: {e}")
            return None
    
    def _cleanup_idle_threads(self):
        """Clean up idle threads that have exceeded their timeout."""
        try:
            current_time = time.time()
            
            for thread_type, idle_threads in self.idle_threads.items():
                if not idle_threads:
                    continue
                
                timeout = self.pool_config[thread_type]['idle_timeout']
                min_size = self.pool_config[thread_type]['size']
                
                # Keep at least min_size threads, clean up excess
                if len(idle_threads) > min_size:
                    threads_to_remove = len(idle_threads) - min_size
                    
                    for _ in range(threads_to_remove):
                        if idle_threads:
                            thread = idle_threads.pop(0)
                            logger.debug(f"[ID:PTP020] Cleaning up idle {thread_type} thread: {thread.objectName()}")
                            
                            # Stop and clean up thread
                            if thread.isRunning():
                                thread.quit()
                                thread.wait(5000)  # 5 second timeout
                            
                            thread.deleteLater()
            
        except Exception as e:
            logger.error(f"[ID:PTP021] Error cleaning up idle threads: {e}")
    
    def get_pool_status(self) -> Dict[str, Any]:
        """Get status of all thread pools."""
        try:
            status = {}
            
            for thread_type in self.pool_config.keys():
                idle_count = len(self.idle_threads[thread_type])
                active_count = len([t for t in self.active_threads.values() if t['type'] == thread_type])
                
                status[thread_type] = {
                    'idle_threads': idle_count,
                    'active_threads': active_count,
                    'total_threads': idle_count + active_count,
                    'max_size': self.pool_config[thread_type]['size']
                }
            
            return status
            
        except Exception as e:
            logger.error(f"[ID:PTP022] Error getting pool status: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown all thread pools."""
        try:
            logger.debug("[ID:PTP023] Shutting down PersistentThreadPool")
            
            # Stop cleanup timer
            self.cleanup_timer.stop()
            
            # Clean up all threads
            for thread_type, idle_threads in self.idle_threads.items():
                for thread in idle_threads:
                    if thread.isRunning():
                        thread.quit()
                        thread.wait(5000)
                    thread.deleteLater()
                idle_threads.clear()
            
            # Clean up active threads
            for thread_name, thread_info in self.active_threads.items():
                # Find the actual thread object
                for thread_type, idle_threads in self.idle_threads.items():
                    for thread in idle_threads:
                        if thread.objectName() == thread_name:
                            if thread.isRunning():
                                thread.quit()
                                thread.wait(5000)
                            thread.deleteLater()
                            break
            
            self.active_threads.clear()
            
            logger.debug("[ID:PTP024] PersistentThreadPool shutdown complete")
            
        except Exception as e:
            logger.error(f"[ID:PTP025] Error during PersistentThreadPool shutdown: {e}")


# Global persistent thread pool instance
_global_persistent_thread_pool: Optional[PersistentThreadPool] = None


def get_global_persistent_thread_pool() -> PersistentThreadPool:
    """Get the global persistent thread pool instance."""
    global _global_persistent_thread_pool
    
    if _global_persistent_thread_pool is None:
        _global_persistent_thread_pool = PersistentThreadPool()
        logger.debug("[ID:PTP026] Created global PersistentThreadPool")
    
    return _global_persistent_thread_pool


def shutdown_global_persistent_thread_pool():
    """Shutdown the global persistent thread pool."""
    global _global_persistent_thread_pool
    
    if _global_persistent_thread_pool:
        _global_persistent_thread_pool.shutdown()
        _global_persistent_thread_pool = None
        logger.debug("[ID:PTP027] Shutdown global PersistentThreadPool") 
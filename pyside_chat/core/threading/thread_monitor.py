"""
Thread monitor for tracking and debugging QThread and QRunnable usage.

This monitor provides:
- Thread lifecycle tracking
- Performance monitoring
- Resource usage analysis
- Debug information for threading issues
"""

from PySide6.QtCore import QObject, Signal, QThread, QTimer
import time
import traceback
from typing import Dict, List, Any, Optional
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ThreadMonitor(QObject):
    """
    Monitor for tracking QThread and QRunnable usage across the application.
    
    This monitor provides:
    - Thread lifecycle tracking
    - Performance monitoring
    - Resource usage analysis
    - Debug information for threading issues
    """
    
    # Signals for monitoring
    thread_registered = Signal(str)  # thread_name
    thread_started = Signal(str)  # thread_name
    thread_finished = Signal(str)  # thread_name
    thread_error = Signal(str, str)  # thread_name, error_message
    resource_usage_updated = Signal(dict)  # resource usage statistics
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Thread tracking
        self.active_threads: Dict[str, Dict] = {}
        self.thread_history: List[Dict] = []
        self.thread_errors: List[Dict] = []
        
        # Statistics
        self.stats = {
            'total_threads': 0,
            'active_threads': 0,
            'completed_threads': 0,
            'failed_threads': 0,
            'total_runtime': 0.0,
            'average_runtime': 0.0
        }
        
        # Setup monitoring timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self._update_monitoring)
        self.monitor_timer.start(2000)  # Update every 2 seconds
        
        logger.debug(f"[ID:TM001] ThreadMonitor created - ID: {id(self)}")
    
    def register_thread(self, thread: QThread, thread_type: str = "unknown", 
                       metadata: Optional[Dict] = None):
        """
        Register a thread for monitoring.
        
        Args:
            thread: QThread instance to monitor
            thread_type: Type of thread (e.g., "streaming", "processing")
            metadata: Additional metadata about the thread
        """
        try:
            thread_id = id(thread)
            thread_name = thread.objectName() or f"{thread_type}_{thread_id}"
            
            thread_info = {
                'id': thread_id,
                'name': thread_name,
                'type': thread_type,
                'start_time': time.time(),
                'status': 'registered',
                'is_running': thread.isRunning(),
                'priority': thread.priority(),
                'stack_size': thread.stackSize(),
                'metadata': metadata or {},
                'error_count': 0,
                'last_error': None
            }
            
            self.active_threads[thread_name] = thread_info
            
            # Connect to thread signals
            thread.started.connect(lambda: self._on_thread_started(thread_name))
            thread.finished.connect(lambda: self._on_thread_finished(thread_name))
            
            # Update statistics
            self.stats['total_threads'] += 1
            self.stats['active_threads'] += 1
            
            logger.debug(f"[ID:TM002] Registered thread: {thread_name} (ID: {thread_id})")
            self.thread_registered.emit(thread_name)
            
        except Exception as e:
            logger.error(f"[ID:TM003] Error registering thread: {e}")
            logger.error(f"[ID:TM004] Thread registration error traceback: {traceback.format_exc()}")
    
    def unregister_thread(self, thread_name: str):
        """
        Unregister a thread from monitoring.
        
        Args:
            thread_name: Name of the thread to unregister
        """
        try:
            if thread_name in self.active_threads:
                thread_info = self.active_threads[thread_name]
                thread_info['end_time'] = time.time()
                thread_info['duration'] = thread_info['end_time'] - thread_info['start_time']
                thread_info['status'] = 'unregistered'
                
                # Move to history
                self.thread_history.append(thread_info)
                del self.active_threads[thread_name]
                
                # Update statistics
                self.stats['active_threads'] -= 1
                self.stats['completed_threads'] += 1
                self.stats['total_runtime'] += thread_info['duration']
                
                if self.stats['completed_threads'] > 0:
                    self.stats['average_runtime'] = self.stats['total_runtime'] / self.stats['completed_threads']
                
                logger.debug(f"[ID:TM005] Unregistered thread: {thread_name}")
                
        except Exception as e:
            logger.error(f"[ID:TM006] Error unregistering thread {thread_name}: {e}")
    
    def record_thread_error(self, thread_name: str, error_message: str, 
                           error_type: str = "unknown"):
        """
        Record an error for a specific thread.
        
        Args:
            thread_name: Name of the thread
            error_message: Error message
            error_type: Type of error
        """
        try:
            error_info = {
                'thread_name': thread_name,
                'error_message': error_message,
                'error_type': error_type,
                'timestamp': time.time(),
                'traceback': traceback.format_exc()
            }
            
            self.thread_errors.append(error_info)
            
            # Update thread info if it exists
            if thread_name in self.active_threads:
                self.active_threads[thread_name]['error_count'] += 1
                self.active_threads[thread_name]['last_error'] = error_message
            
            # Update statistics
            self.stats['failed_threads'] += 1
            
            logger.error(f"[ID:TM007] Thread error recorded: {thread_name} - {error_message}")
            self.thread_error.emit(thread_name, error_message)
            
        except Exception as e:
            logger.error(f"[ID:TM008] Error recording thread error: {e}")
    
    def get_thread_info(self, thread_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific thread.
        
        Args:
            thread_name: Name of the thread
            
        Returns:
            dict: Thread information or None if not found
        """
        try:
            # Check active threads
            if thread_name in self.active_threads:
                thread_info = self.active_threads[thread_name].copy()
                if 'start_time' in thread_info:
                    thread_info['current_duration'] = time.time() - thread_info['start_time']
                return thread_info
            
            # Check thread history
            for thread in self.thread_history:
                if thread['name'] == thread_name:
                    return thread.copy()
            
            return None
            
        except Exception as e:
            logger.error(f"[ID:TM009] Error getting thread info for {thread_name}: {e}")
            return None
    
    def get_all_threads_info(self) -> Dict[str, Any]:
        """
        Get information about all threads.
        
        Returns:
            dict: Information about all threads
        """
        try:
            return {
                'active_threads': self.active_threads.copy(),
                'thread_history': self.thread_history.copy(),
                'thread_errors': self.thread_errors.copy(),
                'statistics': self.stats.copy()
            }
            
        except Exception as e:
            logger.error(f"[ID:TM010] Error getting all threads info: {e}")
            return {}
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage statistics.
        
        Returns:
            dict: Resource usage information
        """
        try:
            import psutil
            
            # Get system resource usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Calculate thread-specific metrics
            total_threads = len(self.active_threads)
            total_runtime = sum(
                time.time() - thread['start_time'] 
                for thread in self.active_threads.values() 
                if 'start_time' in thread
            )
            
            return {
                'system_cpu_percent': cpu_percent,
                'system_memory_percent': memory.percent,
                'active_threads': total_threads,
                'total_thread_runtime': total_runtime,
                'average_thread_runtime': total_runtime / total_threads if total_threads > 0 else 0,
                'thread_utilization': (total_threads / 10) * 100,  # Assuming max 10 threads
                'error_rate': len(self.thread_errors) / max(self.stats['total_threads'], 1) * 100
            }
            
        except Exception as e:
            logger.error(f"[ID:TM011] Error getting resource usage: {e}")
            return {}
    
    def cleanup_old_history(self, max_age_hours: float = 24.0):
        """
        Clean up old thread history.
        
        Args:
            max_age_hours: Maximum age in hours for history to keep
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            # Clean up thread history
            self.thread_history = [
                thread for thread in self.thread_history
                if current_time - thread.get('end_time', thread.get('start_time', 0)) < max_age_seconds
            ]
            
            # Clean up thread errors
            self.thread_errors = [
                error for error in self.thread_errors
                if current_time - error.get('timestamp', 0) < max_age_seconds
            ]
            
            logger.debug(f"[ID:TM012] Cleaned up old thread history (max age: {max_age_hours}h)")
            
        except Exception as e:
            logger.error(f"[ID:TM013] Error cleaning up old history: {e}")
    
    def _on_thread_started(self, thread_name: str):
        """Handle thread started event."""
        try:
            if thread_name in self.active_threads:
                self.active_threads[thread_name]['status'] = 'running'
                self.active_threads[thread_name]['start_time'] = time.time()
                
                logger.debug(f"[ID:TM014] Thread started: {thread_name}")
                self.thread_started.emit(thread_name)
            
        except Exception as e:
            logger.error(f"[ID:TM015] Error handling thread started for {thread_name}: {e}")
    
    def _on_thread_finished(self, thread_name: str):
        """Handle thread finished event."""
        try:
            if thread_name in self.active_threads:
                thread_info = self.active_threads[thread_name]
                thread_info['status'] = 'finished'
                thread_info['end_time'] = time.time()
                thread_info['duration'] = thread_info['end_time'] - thread_info['start_time']
                
                # Move to history
                self.thread_history.append(thread_info)
                del self.active_threads[thread_name]
                
                # Update statistics
                self.stats['active_threads'] -= 1
                self.stats['completed_threads'] += 1
                self.stats['total_runtime'] += thread_info['duration']
                
                if self.stats['completed_threads'] > 0:
                    self.stats['average_runtime'] = self.stats['total_runtime'] / self.stats['completed_threads']
                
                logger.debug(f"[ID:TM016] Thread finished: {thread_name} (Duration: {thread_info['duration']:.2f}s)")
                self.thread_finished.emit(thread_name)
            
        except Exception as e:
            logger.error(f"[ID:TM017] Error handling thread finished for {thread_name}: {e}")
    
    def _update_monitoring(self):
        """Update monitoring information and emit signals."""
        try:
            # Update resource usage
            resource_usage = self.get_resource_usage()
            self.resource_usage_updated.emit(resource_usage)
            
            # Log monitoring information periodically
            if len(self.active_threads) > 0:
                logger.debug(f"[ID:TM018] Monitoring update - Active threads: {len(self.active_threads)}")
            
        except Exception as e:
            logger.error(f"[ID:TM019] Error updating monitoring: {e}")
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive threading report.
        
        Returns:
            dict: Comprehensive threading report
        """
        try:
            # Calculate additional statistics
            total_errors = len(self.thread_errors)
            error_rate = (total_errors / max(self.stats['total_threads'], 1)) * 100
            
            # Get thread type distribution
            thread_types = {}
            for thread in self.active_threads.values():
                thread_type = thread.get('type', 'unknown')
                thread_types[thread_type] = thread_types.get(thread_type, 0) + 1
            
            # Get recent errors
            recent_errors = [
                error for error in self.thread_errors
                if time.time() - error.get('timestamp', 0) < 3600  # Last hour
            ]
            
            return {
                'summary': {
                    'total_threads': self.stats['total_threads'],
                    'active_threads': self.stats['active_threads'],
                    'completed_threads': self.stats['completed_threads'],
                    'failed_threads': self.stats['failed_threads'],
                    'total_runtime': self.stats['total_runtime'],
                    'average_runtime': self.stats['average_runtime'],
                    'error_rate': error_rate
                },
                'thread_types': thread_types,
                'recent_errors': recent_errors,
                'resource_usage': self.get_resource_usage(),
                'active_threads': list(self.active_threads.keys()),
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"[ID:TM020] Error generating report: {e}")
            return {}
    
    def shutdown(self):
        """Shutdown the thread monitor."""
        try:
            logger.debug("[ID:TM021] Shutting down ThreadMonitor")
            
            # Stop monitoring timer
            if self.monitor_timer:
                self.monitor_timer.stop()
            
            # Generate final report
            final_report = self.generate_report()
            logger.info(f"[ID:TM022] Final thread monitor report: {final_report}")
            
            # Clean up old history
            self.cleanup_old_history(max_age_hours=1.0)
            
            logger.debug("[ID:TM023] ThreadMonitor shutdown complete")
            
        except Exception as e:
            logger.error(f"[ID:TM024] Error during ThreadMonitor shutdown: {e}")


# Global thread monitor instance
_global_thread_monitor: Optional[ThreadMonitor] = None


def get_global_thread_monitor() -> ThreadMonitor:
    """
    Get the global thread monitor instance.
    
    Returns:
        ThreadMonitor: Global thread monitor
    """
    global _global_thread_monitor
    
    if _global_thread_monitor is None:
        _global_thread_monitor = ThreadMonitor()
        logger.debug("[ID:TM025] Created global ThreadMonitor")
    
    return _global_thread_monitor


def shutdown_global_thread_monitor():
    """Shutdown the global thread monitor."""
    global _global_thread_monitor
    
    if _global_thread_monitor:
        _global_thread_monitor.shutdown()
        _global_thread_monitor = None
        logger.debug("[ID:TM026] Shutdown global ThreadMonitor") 
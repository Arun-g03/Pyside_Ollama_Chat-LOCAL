"""
Logging Helpers Module

This module provides centralized logging utilities to standardize log formats
and reduce code duplication throughout the application.
"""

import logging
import traceback
import threading
import time
from typing import Optional, Dict, List
from PySide6.QtCore import QThread, QObject, Signal
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class LoggingHelpers:
    """Centralized logging helper methods for consistent logging across the application"""
    
    @staticmethod
    def log_exception_with_context(operation: str, exception: Exception, context: Dict = None):
        """Log an exception with context information"""
        context_str = f" - Context: {context}" if context else ""
        logger.error(f"[ID:0900] Exception in {operation}: {str(exception)}{context_str}")
        logger.error(f"[ID:0901] Exception traceback: {traceback.format_exc()}")
    
    @staticmethod
    def log_warning_with_context(message: str, context: Dict = None):
        """Log a warning with context information"""
        context_str = f" - Context: {context}" if context else ""
        logger.warning(f"[ID:0902] {message}{context_str}")
    
    @staticmethod
    def log_info_with_context(message: str, context: Dict = None):
        """Log an info message with context information"""
        context_str = f" - Context: {context}" if context else ""
        logger.info(f"[ID:0903] {message}{context_str}")
    
    @staticmethod
    def log_debug(message: str):
        """Log a debug message"""
        logger.debug(f"[ID:0904] {message}")
    
    @staticmethod
    def log_error(message: str):
        """Log an error message"""
        logger.error(f"[ID:0905] {message}")
    
    @staticmethod
    def log_network_request(url: str, method: str, status_code: int = None, error: Exception = None):
        """Log network request information"""
        if error:
            logger.error(f"[ID:0906] Network request failed - {method} {url}: {str(error)}")
        elif status_code:
            logger.info(f"[ID:0907] Network request - {method} {url}: {status_code}")
        else:
            logger.debug(f"[ID:0908] Network request - {method} {url}")
    
    @staticmethod
    def log_file_operation(operation: str, filepath: str, success: bool, error: Exception = None):
        """Log file operation information"""
        if success:
            logger.debug(f"[ID:0909] File operation successful - {operation}: {filepath}")
        else:
            logger.error(f"[ID:0910] File operation failed - {operation}: {filepath} - {str(error)}")
    
    @staticmethod
    def log_audio_operation(operation: str, success: bool, error: Exception = None, details: str = ""):
        """Log audio operation information"""
        if success:
            logger.debug(f"[ID:0911] Audio operation successful - {operation}{' - ' + details if details else ''}")
        else:
            logger.error(f"[ID:0912] Audio operation failed - {operation} - {str(error)}")
    
    @staticmethod
    def log_memory_operation(operation: str, memory_type: str, success: bool, error: Exception = None):
        """Log memory operation information"""
        if success:
            logger.debug(f"[ID:0913] Memory operation successful - {operation} ({memory_type})")
        else:
            logger.error(f"[ID:0914] Memory operation failed - {operation} ({memory_type}) - {str(error)}")
    
    @staticmethod
    def log_ui_operation(component: str, operation: str, success: bool, error: Exception = None):
        """Log UI operation information"""
        if success:
            logger.debug(f"[ID:0915] UI operation successful - {component}.{operation}")
        else:
            logger.error(f"[ID:0916] UI operation failed - {component}.{operation} - {str(error)}")
    
    @staticmethod
    def log_performance_metric(operation: str, duration: float, context: str = ""):
        """Log performance metric"""
        context_str = f" - Context: {context}" if context else ""
        logger.debug(f"[ID:0917] Performance - {operation}: {duration:.3f}s{context_str}")
    
    @staticmethod
    def log_json_parsing_error(error: Exception, json_str: str):
        """Log JSON parsing error"""
        logger.error(f"[ID:0918] JSON parsing error: {str(error)}")
        logger.error(f"[ID:0919] JSON content: {json_str[:200]}...")
    
    @staticmethod
    def log_json_parsing_success(json_str: str):
        """Log successful JSON parsing"""
        logger.debug(f"[ID:0920] JSON parsing successful: {json_str[:100]}...")
    
    @staticmethod
    def log_critical_error(component: str, error: Exception, recovery_action: str):
        """Log a critical error with recovery action"""
        logger.critical(f"[ID:0921] Critical error in {component}: {str(error)}")
        logger.critical(f"[ID:0922] Recovery action: {recovery_action}")
    
    # Memory service specific logging methods
    @staticmethod
    def log_fact_extraction_start(query: str):
        """Log fact extraction start"""
        logger.debug(f"[ID:0923] Fact extraction started for query: {query[:100]}...")
    
    @staticmethod
    def log_fact_extraction_end(facts_count: int):
        """Log fact extraction end"""
        logger.debug(f"[ID:0924] Fact extraction completed - {facts_count} facts extracted")
    
    @staticmethod
    def log_fact_extraction_result(facts: List[Dict]):
        """Log fact extraction result"""
        logger.debug(f"[ID:0925] Fact extraction result: {len(facts)} facts")
    
    @staticmethod
    def log_fact_processing(fact_type: str, fact_count: int):
        """Log fact processing"""
        logger.debug(f"[ID:0926] Processing {fact_count} {fact_type} facts")
    
    @staticmethod
    def log_fact_storage_start(fact_type: str, fact_count: int):
        """Log fact storage start"""
        logger.debug(f"[ID:0927] Storing {fact_count} {fact_type} facts")
    
    @staticmethod
    def log_fact_storage_end(fact_type: str, stored_count: int):
        """Log fact storage end"""
        logger.debug(f"[ID:0928] Stored {stored_count} {fact_type} facts")
    
    @staticmethod
    def log_fact_storage_summary(total_facts: int, stored_facts: int):
        """Log fact storage summary"""
        logger.info(f"[ID:0929] Fact storage summary: {stored_facts}/{total_facts} facts stored")
    
    @staticmethod
    def log_fact_skipped(reason: str, fact_type: str = "unknown"):
        """Log skipped fact"""
        logger.debug(f"[ID:0930] Fact skipped ({fact_type}): {reason}")
    
    @staticmethod
    def log_memory_result(query: str, memory_count: int):
        """Log memory search result"""
        logger.debug(f"[ID:0931] Memory search for '{query[:50]}...' returned {memory_count} results")
    
    @staticmethod
    def log_memory_ltm_status(ltm_count: int, stm_count: int):
        """Log memory status"""
        logger.debug(f"[ID:0932] Memory status - LTM: {ltm_count}, STM: {stm_count}")
    
    @staticmethod
    def log_llm_call(model: str, prompt_length: int):
        """Log LLM call"""
        logger.debug(f"[ID:0933] LLM call - Model: {model}, Prompt length: {prompt_length}")
    
    @staticmethod
    def log_llm_response(model: str, response_length: int):
        """Log LLM response"""
        logger.debug(f"[ID:0934] LLM response - Model: {model}, Response length: {response_length}")
    
    @staticmethod
    def log_json_extraction(json_data: Dict):
        """Log JSON extraction"""
        logger.debug(f"[ID:0935] JSON extraction successful: {len(json_data)} fields")
    
    @staticmethod
    def log_message_sent(message_length: int):
        """Log message sent"""
        logger.debug(f"[ID:0936] Message sent - Length: {message_length}")
    
    @staticmethod
    def log_message_sent_end(message_length: int, response_length: int):
        """Log message sent end"""
        logger.debug(f"[ID:0937] Message exchange completed - Sent: {message_length}, Received: {response_length}")
    
    @staticmethod
    def log_conversation_detection(conversation_type: str):
        """Log conversation detection"""
        logger.debug(f"[ID:0938] Conversation detected: {conversation_type}")
    
    @staticmethod
    def log_service_initialization(service_name: str, success: bool, error: Exception = None):
        """Log service initialization"""
        if success:
            logger.info(f"[ID:0939] Service initialized successfully: {service_name}")
        else:
            error_msg = f" - Error: {str(error)}" if error else ""
            logger.error(f"[ID:0940] Service initialization failed: {service_name}{error_msg}")


class ThreadMonitor(QObject):
    """Monitor for tracking QThread lifecycle and debugging thread issues"""
    
    thread_started = Signal(str)  # thread_name
    thread_finished = Signal(str)  # thread_name
    thread_error = Signal(str, str)  # thread_name, error_message
    
    def __init__(self):
        super().__init__()
        self.active_threads: Dict[str, Dict] = {}
        self.thread_history: List[Dict] = []
        self._monitor_id = id(self)
        
        logger.debug(f"[ID:0800] ThreadMonitor created - ID: {self._monitor_id}")
    
    def register_thread(self, thread: QThread, thread_type: str = "unknown"):
        """Register a thread for monitoring"""
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
                'stack_size': thread.stackSize()
            }
            
            self.active_threads[thread_name] = thread_info
            
            # Connect to thread signals
            thread.started.connect(lambda: self._on_thread_started(thread_name))
            thread.finished.connect(lambda: self._on_thread_finished(thread_name))
            
            logger.debug(f"[ID:0801] Registered thread: {thread_name} (ID: {thread_id})")
            self.thread_started.emit(thread_name)
            
        except Exception as e:
            logger.error(f"[ID:0802] Error registering thread: {e}")
            logger.error(f"[ID:0803] Thread registration error traceback: {traceback.format_exc()}")
    
    def unregister_thread(self, thread_name: str):
        """Unregister a thread from monitoring"""
        try:
            if thread_name in self.active_threads:
                thread_info = self.active_threads[thread_name]
                thread_info['end_time'] = time.time()
                thread_info['duration'] = thread_info['end_time'] - thread_info['start_time']
                thread_info['status'] = 'unregistered'
                
                # Move to history
                self.thread_history.append(thread_info)
                del self.active_threads[thread_name]
                
                logger.debug(f"[ID:0804] Unregistered thread: {thread_name} (Duration: {thread_info['duration']:.2f}s)")
                self.thread_finished.emit(thread_name)
                
        except Exception as e:
            logger.error(f"[ID:0805] Error unregistering thread {thread_name}: {e}")
            logger.error(f"[ID:0806] Thread unregistration error traceback: {traceback.format_exc()}")
    
    def _on_thread_started(self, thread_name: str):
        """Handle thread started signal"""
        try:
            if thread_name in self.active_threads:
                self.active_threads[thread_name]['status'] = 'running'
                self.active_threads[thread_name]['actual_start_time'] = time.time()
                
                logger.debug(f"[ID:0807] Thread started: {thread_name}")
                
        except Exception as e:
            logger.error(f"[ID:0808] Error handling thread started for {thread_name}: {e}")
    
    def _on_thread_finished(self, thread_name: str):
        """Handle thread finished signal"""
        try:
            if thread_name in self.active_threads:
                thread_info = self.active_threads[thread_name]
                thread_info['status'] = 'finished'
                thread_info['end_time'] = time.time()
                thread_info['duration'] = thread_info['end_time'] - thread_info['start_time']
                
                logger.debug(f"[ID:0809] Thread finished: {thread_name} (Duration: {thread_info['duration']:.2f}s)")
                
        except Exception as e:
            logger.error(f"[ID:0810] Error handling thread finished for {thread_name}: {e}")
    
    def get_thread_info(self, thread_name: str) -> Optional[Dict]:
        """Get information about a specific thread"""
        return self.active_threads.get(thread_name)
    
    def get_all_threads(self) -> Dict[str, Dict]:
        """Get information about all active threads"""
        return self.active_threads.copy()
    
    def get_thread_history(self) -> List[Dict]:
        """Get history of completed threads"""
        return self.thread_history.copy()
    
    def get_thread_stats(self) -> Dict:
        """Get statistics about thread usage"""
        try:
            active_count = len(self.active_threads)
            history_count = len(self.thread_history)
            
            # Calculate average duration for completed threads
            completed_threads = [t for t in self.thread_history if 'duration' in t]
            avg_duration = 0.0
            if completed_threads:
                avg_duration = sum(t['duration'] for t in completed_threads) / len(completed_threads)
            
            # Count by thread type
            type_counts = {}
            for thread_info in self.active_threads.values():
                thread_type = thread_info['type']
                type_counts[thread_type] = type_counts.get(thread_type, 0) + 1
            
            stats = {
                'active_threads': active_count,
                'completed_threads': history_count,
                'average_duration': avg_duration,
                'thread_types': type_counts,
                'monitor_id': self._monitor_id
            }
            
            logger.debug(f"[ID:0811] Thread stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"[ID:0812] Error getting thread stats: {e}")
            logger.error(f"[ID:0813] Thread stats error traceback: {traceback.format_exc()}")
            return {
                'active_threads': 0,
                'completed_threads': 0,
                'average_duration': 0.0,
                'thread_types': {},
                'error': str(e)
            }
    
    def cleanup(self):
        """Clean up the thread monitor"""
        try:
            logger.debug(f"[ID:0814] Cleaning up ThreadMonitor - ID: {self._monitor_id}")
            
            # Log final stats
            stats = self.get_thread_stats()
            logger.debug(f"[ID:0815] Final thread stats: {stats}")
            
            # Clear active threads
            self.active_threads.clear()
            self.thread_history.clear()
            
            logger.debug("[ID:0816] ThreadMonitor cleanup completed")
            
        except Exception as e:
            logger.error(f"[ID:0817] Error cleaning up ThreadMonitor: {e}")
            logger.error(f"[ID:0818] ThreadMonitor cleanup error traceback: {traceback.format_exc()}")


class ThreadSafeLogger:
    """Thread-safe logging utilities"""
    
    @staticmethod
    def log_thread_context(message: str, thread: Optional[QThread] = None):
        """Log a message with thread context information"""
        try:
            current_thread = QThread.currentThread()
            thread_name = current_thread.objectName() or 'unnamed'
            thread_id = id(current_thread)
            
            if thread:
                target_thread_name = thread.objectName() or 'unnamed'
                target_thread_id = id(thread)
                logger.debug(f"[ID:0819] {message} - Current: {thread_name} (ID: {thread_id}), Target: {target_thread_name} (ID: {target_thread_id})")
            else:
                logger.debug(f"[ID:0820] {message} - Thread: {thread_name} (ID: {thread_id})")
                
        except Exception as e:
            logger.error(f"[ID:0821] Error logging thread context: {e}")
    
    @staticmethod
    def log_thread_safety_check(operation: str, current_thread: QThread, target_thread: QThread):
        """Log thread safety check"""
        try:
            current_name = current_thread.objectName() or 'unnamed'
            target_name = target_thread.objectName() or 'unnamed'
            
            if current_thread == target_thread:
                logger.debug(f"[ID:0822] Thread-safe operation: {operation} - Same thread: {current_name}")
            else:
                logger.warning(f"[ID:0823] Cross-thread operation: {operation} - Current: {current_name}, Target: {target_name}")
                
        except Exception as e:
            logger.error(f"[ID:0824] Error logging thread safety check: {e}")
    
    @staticmethod
    def log_thread_operation(operation: str, thread_name: str, details: str = ""):
        """Log thread operation"""
        try:
            details_str = f" - {details}" if details else ""
            logger.debug(f"[ID:0825] Thread operation: {operation} on {thread_name}{details_str}")
            
        except Exception as e:
            logger.error(f"[ID:0826] Error logging thread operation: {e}")


def get_thread_monitor() -> ThreadMonitor:
    """Get the global thread monitor instance"""
    if not hasattr(get_thread_monitor, '_instance'):
        get_thread_monitor._instance = ThreadMonitor()
    return get_thread_monitor._instance


def cleanup_thread_monitor():
    """Clean up the global thread monitor"""
    if hasattr(get_thread_monitor, '_instance'):
        get_thread_monitor._instance.cleanup()
        get_thread_monitor._instance = None

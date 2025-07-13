"""
Threading Integration - Bridges new QThread/QRunnable architecture with existing event system.

This module provides:
- Integration with existing EventBus
- Modern QThread/QRunnable architecture
- Unified interface for all threading operations
"""

from PySide6.QtCore import QObject, Signal
from typing import Dict, List, Any, Optional
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.threading import get_global_threading_service

logger = CustomLogger.get_logger(__name__)


class ThreadingIntegration(QObject):
    """
    Integration layer that bridges the new threading architecture with existing event system.
    
    This class provides:
    - Integration with new ThreadingService
    - Unified interface for all threading operations
    - Modern QThread/QRunnable architecture
    """
    
    # Signals for integration with existing system
    chunk_received = Signal(str)  # For streaming chunks
    progress_updated = Signal(str)  # For progress updates
    finished = Signal()  # For completion
    error = Signal(str)  # For errors
    
    def __init__(self, event_handler):
        super().__init__()
        self.event_handler = event_handler
        self.threading_service = get_global_threading_service()
        
        # Connect threading service signals to integration signals
        self.threading_service.chunk_received.connect(self.chunk_received)
        self.threading_service.progress_updated.connect(self.progress_updated)
        self.threading_service.finished.connect(self.finished)
        self.threading_service.error.connect(self.error)
        
        logger.debug("[ID:TI001] ThreadingIntegration initialized")
    
    def start_chat_streaming(self, context_messages: List[Dict], chosen_model: str, temperature: float, config_manager) -> bool:
        """
        Start chat streaming using the new QThread architecture.
        
        Args:
            context_messages: List of conversation messages
            chosen_model: Model name to use
            temperature: Temperature setting
            config_manager: Configuration manager
            
        Returns:
            bool: True if streaming started successfully
        """
        try:
            logger.debug(f"[ID:TI002] Starting chat streaming for model: {chosen_model}")
            return self.threading_service.start_chat_streaming(context_messages, chosen_model, temperature, config_manager)
            
        except Exception as e:
            logger.error(f"[ID:TI003] Error starting chat streaming: {e}")
            return False
    
    def stop_chat_streaming(self):
        """Stop chat streaming safely."""
        try:
            logger.debug("[ID:TI004] Stopping chat streaming")
            self.threading_service.stop_chat_streaming()
            
        except Exception as e:
            logger.error(f"[ID:TI005] Error stopping chat streaming: {e}")
    
    def process_message_spell_check(self, message: str, callback) -> str:
        """
        Process message spell check using QRunnable.
        
        Args:
            message: Message to spell check
            callback: Callback function for results
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TI006] Processing message spell check: {message[:50]}...")
            return self.threading_service.process_message(message, "spell_check", callback)
            
        except Exception as e:
            logger.error(f"[ID:TI007] Error processing message spell check: {e}")
            return ""
    
    def process_message_formatting(self, message: str, callback) -> str:
        """
        Process message formatting using QRunnable.
        
        Args:
            message: Message to format
            callback: Callback function for results
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TI008] Processing message formatting: {message[:50]}...")
            return self.threading_service.process_message(message, "formatting", callback)
            
        except Exception as e:
            logger.error(f"[ID:TI009] Error processing message formatting: {e}")
            return ""
    
    def process_file_operation(self, file_path: str, operation: str, **kwargs) -> str:
        """
        Process file operation using QRunnable.
        
        Args:
            file_path: Path to the file
            operation: Operation to perform
            **kwargs: Additional arguments
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TI010] Processing file operation: {operation} on {file_path}")
            return self.threading_service.process_file_operation(file_path, operation, **kwargs)
            
        except Exception as e:
            logger.error(f"[ID:TI011] Error processing file operation: {e}")
            return ""
    
    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return self.threading_service.get_threading_status()
            
        except Exception as e:
            logger.error(f"[ID:TI012] Error getting threading status: {e}")
            return {}


class EventBusThreadingBridge:
    """
    Bridge class that integrates new threading architecture with existing EventBus.
    
    This class provides:
    - Drop-in replacement for existing Worker usage
    - Integration with current EventBus methods
    - Modern QThread/QRunnable architecture
    """
    
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.threading_integration = ThreadingIntegration(event_handler)
        
        # Connect integration signals to Event Bus methods
        self.threading_integration.chunk_received.connect(self._on_chunk_received)
        self.threading_integration.progress_updated.connect(self._on_progress_updated)
        self.threading_integration.finished.connect(self._on_finished)
        self.threading_integration.error.connect(self._on_error)
        
        logger.debug("[ID:TB001] EventBusThreadingBridge initialized")
    
    def _on_chunk_received(self, chunk: str):
        """Handle chunk received from streaming."""
        try:
            logger.debug(f"[ID:TB002] Received chunk: {chunk[:50]}...")
            
            # Call existing Event Bus method
            if hasattr(self.event_handler, '_on_worker_chunk'):
                self.event_handler._on_worker_chunk(chunk)
            
        except Exception as e:
            logger.error(f"[ID:TB003] Error handling chunk: {e}")
    
    def _on_progress_updated(self, progress: str):
        """Handle progress update from streaming."""
        try:
            logger.debug(f"[ID:TB004] Progress update: {progress}")
            
            # Call existing Event Bus method
            if hasattr(self.event_handler, '_on_worker_progress'):
                self.event_handler._on_worker_progress(progress)
            
        except Exception as e:
            logger.error(f"[ID:TB005] Error handling progress: {e}")
    
    def _on_finished(self):
        """Handle streaming finished."""
        try:
            logger.debug("[ID:TB006] Streaming finished")
            
            # Call existing Event Bus method
            if hasattr(self.event_handler, '_on_worker_finished'):
                self.event_handler._on_worker_finished()
            
        except Exception as e:
            logger.error(f"[ID:TB007] Error handling finished: {e}")
    
    def _on_error(self, error_message: str):
        """Handle streaming error."""
        try:
            logger.error(f"[ID:TB008] Streaming error: {error_message}")
            
            # Call existing Event Bus method
            if hasattr(self.event_handler, '_on_worker_error'):
                self.event_handler._on_worker_error(error_message)
            
        except Exception as e:
            logger.error(f"[ID:TB009] Error handling error: {e}")
    
    def start_chat_streaming(self, context_messages: List[Dict], chosen_model: str, temperature: float, config_manager) -> bool:
        """
        Start chat streaming via bridge.
        
        Args:
            context_messages: List of conversation messages
            chosen_model: Model name to use
            temperature: Temperature setting
            config_manager: Configuration manager
            
        Returns:
            bool: True if streaming started successfully
        """
        try:
            logger.debug(f"[ID:TB010] Starting chat streaming via bridge - Model: {chosen_model}")
            return self.threading_integration.start_chat_streaming(context_messages, chosen_model, temperature, config_manager)
            
        except Exception as e:
            logger.error(f"[ID:TB011] Error starting chat streaming via bridge: {e}")
            return False
    
    def stop_chat_streaming(self):
        """Stop chat streaming safely."""
        try:
            logger.debug("[ID:TB012] Stopping chat streaming via bridge")
            self.threading_integration.stop_chat_streaming()
            
        except Exception as e:
            logger.error(f"[ID:TB013] Error stopping chat streaming via bridge: {e}")
    
    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return self.threading_integration.get_threading_status()
            
        except Exception as e:
            logger.error(f"[ID:TB014] Error getting threading status via bridge: {e}")
            return {} 
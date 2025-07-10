"""
Threading Integration - Bridges new QThread/QRunnable architecture with existing event system.

This module provides:
- Integration with existing EventHandler
- Backward compatibility with current Worker usage
- Migration path from old to new threading architecture
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
    - Backward compatibility with existing EventHandler
    - Integration with new ThreadingService
    - Migration path from old Worker to new architecture
    - Unified interface for all threading operations
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
        self.threading_service.worker_chunk_received.connect(self.chunk_received)
        self.threading_service.worker_progress_updated.connect(self.progress_updated)
        self.threading_service.worker_finished.connect(self.finished)
        self.threading_service.worker_error.connect(self.error)
        
        logger.debug("[ID:TI001] ThreadingIntegration initialized")
    
    def start_chat_streaming(self, context_messages: List[Dict], chosen_model: str, temperature: float) -> bool:
        """
        Start chat streaming using the new QThread architecture.
        
        Args:
            context_messages: List of conversation messages
            chosen_model: Model name to use
            temperature: Temperature setting
            
        Returns:
            bool: True if streaming started successfully
        """
        try:
            logger.debug(f"[ID:TI002] Starting chat streaming with new architecture - Model: {chosen_model}")
            
            # Get configuration from service manager
            config_manager = self.event_handler.service_manager.config_manager
            
            # Start streaming using threading service
            success = self.threading_service.start_chat_streaming(
                messages=context_messages,
                model=chosen_model,
                temperature=temperature,
                ollama_url=config_manager.get_ollama_url(),
                max_tokens=config_manager.get_max_tokens(),
                top_p=config_manager.get_top_p(),
                frequency_penalty=config_manager.get_frequency_penalty(),
                presence_penalty=config_manager.get_presence_penalty()
            )
            
            if success:
                logger.debug("[ID:TI003] Chat streaming started successfully with new architecture")
            else:
                logger.error("[ID:TI004] Failed to start chat streaming with new architecture")
            
            return success
            
        except Exception as e:
            logger.error(f"[ID:TI005] Error starting chat streaming: {e}")
            return False
    
    def stop_chat_streaming(self):
        """Stop chat streaming safely."""
        try:
            logger.debug("[ID:TI006] Stopping chat streaming")
            self.threading_service.stop_chat_streaming()
            
        except Exception as e:
            logger.error(f"[ID:TI007] Error stopping chat streaming: {e}")
    
    def process_message_spell_check(self, message: str) -> str:
        """
        Process message spell check using QRunnable.
        
        Args:
            message: Message to spell check
            
        Returns:
            str: Task ID for tracking
        """
        try:
            logger.debug(f"[ID:TI008] Processing message spell check: {message[:50]}...")
            task_id = self.threading_service.process_message_spell_check(message)
            return task_id
            
        except Exception as e:
            logger.error(f"[ID:TI009] Error processing message spell check: {e}")
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
            logger.debug(f"[ID:TI010] Processing message formatting: {message[:50]}...")
            task_id = self.threading_service.process_message_formatting(message)
            return task_id
            
        except Exception as e:
            logger.error(f"[ID:TI011] Error processing message formatting: {e}")
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
            logger.debug(f"[ID:TI012] Processing file operation: {operation} on {file_path}")
            task_id = self.threading_service.process_file_operation(file_path, operation, **kwargs)
            return task_id
            
        except Exception as e:
            logger.error(f"[ID:TI013] Error processing file operation: {e}")
            return ""
    
    def create_legacy_worker(self, context_messages: List[Dict], chosen_model: str, temperature: float):
        """
        Create legacy worker for backward compatibility.
        
        This method provides the same interface as the old Worker class
        but uses the new QThread architecture internally.
        """
        try:
            logger.debug(f"[ID:TI014] Creating legacy worker for model: {chosen_model}")
            self.threading_service.create_legacy_worker(context_messages, chosen_model, temperature)
            
        except Exception as e:
            logger.error(f"[ID:TI015] Error creating legacy worker: {e}")
    
    def cleanup_legacy_worker(self):
        """Clean up legacy worker safely."""
        try:
            logger.debug("[ID:TI016] Cleaning up legacy worker")
            self.threading_service.cleanup_legacy_worker()
            
        except Exception as e:
            logger.error(f"[ID:TI017] Error cleaning up legacy worker: {e}")
    
    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return self.threading_service.get_threading_status()
            
        except Exception as e:
            logger.error(f"[ID:TI018] Error getting threading status: {e}")
            return {}
    
    def cleanup(self):
        """Clean up all threading resources."""
        try:
            logger.debug("[ID:TI019] Cleaning up ThreadingIntegration")
            self.threading_service.cleanup()
            
        except Exception as e:
            logger.error(f"[ID:TI020] Error during ThreadingIntegration cleanup: {e}")


class EventHandlerThreadingBridge:
    """
    Bridge class that integrates new threading architecture with existing EventHandler.
    
    This class provides:
    - Drop-in replacement for existing Worker usage
    - Backward compatibility with current EventHandler methods
    - Migration path from old to new threading architecture
    """
    
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.threading_integration = ThreadingIntegration(event_handler)
        
        # Connect integration signals to event handler methods
        self.threading_integration.chunk_received.connect(self._on_chunk_received)
        self.threading_integration.progress_updated.connect(self._on_progress_updated)
        self.threading_integration.finished.connect(self._on_finished)
        self.threading_integration.error.connect(self._on_error)
        
        logger.debug("[ID:TB001] EventHandlerThreadingBridge initialized")
    
    def _on_chunk_received(self, chunk: str):
        """Handle chunk received from streaming."""
        try:
            logger.debug(f"[ID:TB002] Received chunk: {chunk[:50]}...")
            
            # Call existing event handler method
            if hasattr(self.event_handler, '_on_worker_chunk'):
                self.event_handler._on_worker_chunk(chunk)
            
        except Exception as e:
            logger.error(f"[ID:TB003] Error handling chunk: {e}")
    
    def _on_progress_updated(self, progress: str):
        """Handle progress update from streaming."""
        try:
            logger.debug(f"[ID:TB004] Progress update: {progress}")
            
            # Call existing event handler method
            if hasattr(self.event_handler, '_on_worker_progress'):
                self.event_handler._on_worker_progress(progress)
            
        except Exception as e:
            logger.error(f"[ID:TB005] Error handling progress: {e}")
    
    def _on_finished(self):
        """Handle streaming finished."""
        try:
            logger.debug("[ID:TB006] Streaming finished")
            
            # Call existing event handler method
            if hasattr(self.event_handler, '_on_worker_finished'):
                self.event_handler._on_worker_finished()
            
        except Exception as e:
            logger.error(f"[ID:TB007] Error handling finished: {e}")
    
    def _on_error(self, error: str):
        """Handle streaming error."""
        try:
            logger.error(f"[ID:TB008] Streaming error: {error}")
            
            # Call existing event handler method
            if hasattr(self.event_handler, '_on_worker_detailed_error'):
                self.event_handler._on_worker_detailed_error(error)
            
        except Exception as e:
            logger.error(f"[ID:TB009] Error handling error: {e}")
    
    def start_chat_streaming(self, context_messages: List[Dict], chosen_model: str, temperature: float) -> bool:
        """
        Start chat streaming using new architecture.
        
        Args:
            context_messages: List of conversation messages
            chosen_model: Model name to use
            temperature: Temperature setting
            
        Returns:
            bool: True if streaming started successfully
        """
        try:
            logger.debug(f"[ID:TB010] Starting chat streaming via bridge - Model: {chosen_model}")
            return self.threading_integration.start_chat_streaming(context_messages, chosen_model, temperature)
            
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
    
    def create_legacy_worker(self, context_messages: List[Dict], chosen_model: str, temperature: float):
        """
        Create legacy worker for backward compatibility.
        """
        try:
            logger.debug(f"[ID:TB014] Creating legacy worker via bridge - Model: {chosen_model}")
            self.threading_integration.create_legacy_worker(context_messages, chosen_model, temperature)
            
        except Exception as e:
            logger.error(f"[ID:TB015] Error creating legacy worker via bridge: {e}")
    
    def cleanup_legacy_worker(self):
        """Clean up legacy worker safely."""
        try:
            logger.debug("[ID:TB016] Cleaning up legacy worker via bridge")
            self.threading_integration.cleanup_legacy_worker()
            
        except Exception as e:
            logger.error(f"[ID:TB017] Error cleaning up legacy worker via bridge: {e}")
    
    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return self.threading_integration.get_threading_status()
            
        except Exception as e:
            logger.error(f"[ID:TB018] Error getting threading status via bridge: {e}")
            return {}
    
    def cleanup(self):
        """Clean up all threading resources."""
        try:
            logger.debug("[ID:TB019] Cleaning up EventHandlerThreadingBridge")
            self.threading_integration.cleanup()
            
        except Exception as e:
            logger.error(f"[ID:TB020] Error during EventHandlerThreadingBridge cleanup: {e}")


# Global integration instance
_global_threading_integration: Optional[ThreadingIntegration] = None


def get_global_threading_integration(event_handler=None) -> ThreadingIntegration:
    """
    Get the global threading integration instance.
    
    Args:
        event_handler: EventHandler instance (required for first call)
        
    Returns:
        ThreadingIntegration: Global threading integration
    """
    global _global_threading_integration
    
    if _global_threading_integration is None and event_handler is not None:
        _global_threading_integration = ThreadingIntegration(event_handler)
        logger.debug("[ID:TI021] Created global ThreadingIntegration")
    
    return _global_threading_integration


def shutdown_global_threading_integration():
    """Shutdown the global threading integration."""
    global _global_threading_integration
    
    if _global_threading_integration:
        _global_threading_integration.cleanup()
        _global_threading_integration = None
        logger.debug("[ID:TI022] Shutdown global ThreadingIntegration") 
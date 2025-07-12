"""
Voice Service Manager

Manages voice service initialization and provides a singleton pattern
to prevent multiple initializations and reduce resource usage.
"""

import threading
from typing import Optional, Dict, Any
from PySide6.QtCore import QObject, Signal

from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class VoiceServiceManager(QObject):
    """Singleton manager for voice service initialization and management"""
    
    # Signals
    voice_service_ready = Signal()  # Emitted when voice service is ready
    voice_service_error = Signal(str)  # Emitted when voice service fails to initialize
    voice_service_initializing = Signal()  # Emitted when initialization starts
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the voice service manager (singleton)"""
        if hasattr(self, '_initialized'):
            return
            
        super().__init__()
        self._initialized = True
        
        # Voice service instance
        self._voice_service = None
        self._voice_service_initialized = False
        self._initialization_in_progress = False
        self._initialization_error = None
        
        # Settings cache
        self._cached_settings = {}
        
        # Callbacks for when service becomes ready
        self._ready_callbacks = []
        
        logger.info("Voice Service Manager initialized")
    
    def get_voice_service(self, force_reinitialize: bool = False) -> Optional[Any]:
        """
        Get the voice service instance, initializing if necessary
        
        Args:
            force_reinitialize: Force reinitialization even if already initialized
            
        Returns:
            Voice service instance or None if initialization failed
        """
        if force_reinitialize:
            self._reset_voice_service()
        
        if not self._voice_service_initialized and not self._initialization_in_progress:
            self._initialize_voice_service()
        
        return self._voice_service
    
    def _initialize_voice_service(self):
        """Initialize the voice service"""
        if self._initialization_in_progress:
            logger.debug("Voice service initialization already in progress")
            return
            
        self._initialization_in_progress = True
        self._initialization_error = None
        self.voice_service_initializing.emit()
        
        logger.info("Starting voice service initialization", print_to_terminal=True)
        
        try:
            # Try to get voice service from service manager first
            voice_service = self._try_get_from_service_manager()
            
            if not voice_service:
                # Fallback to direct initialization
                logger.info("Trying direct voice service initialization", print_to_terminal=True)
                voice_service = self._try_direct_initialization()
            
            if voice_service:
                self._voice_service = voice_service
                self._voice_service_initialized = True
                self._initialization_error = None
                
                # Log the type of voice service being used
                service_type = type(voice_service).__name__
                logger.info(f"Voice service type: {service_type}", print_to_terminal=True)
                
                # Apply cached settings if any
                if self._cached_settings:
                    try:
                        voice_service.update_settings(self._cached_settings)
                        logger.debug(f"Applied cached settings to voice service")
                    except Exception as e:
                        logger.warning(f"Failed to apply cached settings: {e}")
                
                # Check if the voice service is actually ready before emitting signal
                if hasattr(voice_service, 'is_voice_available') and voice_service.is_voice_available():
                    logger.info("Voice service is ready, emitting ready signal", print_to_terminal=True)
                    self.voice_service_ready.emit()
                else:
                    logger.info("Voice service initialized but not ready yet, waiting for ready signal", print_to_terminal=True)
                    # The voice service will emit its own ready signal when it becomes ready
                    if hasattr(voice_service, 'voice_service_ready'):
                        voice_service.voice_service_ready.connect(self._on_voice_service_ready)
                
                # Call any registered callbacks
                for callback in self._ready_callbacks:
                    try:
                        callback(voice_service)
                    except Exception as e:
                        logger.error(f"Error in voice service ready callback: {e}")
                self._ready_callbacks.clear()
                
            else:
                raise Exception("Failed to initialize voice service - no service available")
                
        except Exception as e:
            self._initialization_error = str(e)
            logger.error(f"Voice service initialization failed: {e}", print_to_terminal=True)
            self.voice_service_error.emit(str(e))
            
        finally:
            self._initialization_in_progress = False
    
    def _on_voice_service_ready(self):
        """Handle voice service ready signal from the actual service"""
        logger.info("Voice service ready signal received from service", print_to_terminal=True)
        self.voice_service_ready.emit()
    
    def _try_get_from_service_manager(self):
        """Try to get voice service from service manager"""
        try:
            # Try to get service manager from the main application
            from pyside_chat.app.service_manager import ServiceManager
            service_manager = ServiceManager.get_instance()
            
            if hasattr(service_manager, 'get_voice_service'):
                voice_service = service_manager.get_voice_service()
                if voice_service:
                    logger.info("Voice service obtained from service manager")
                    return voice_service
                    
        except Exception as e:
            logger.debug(f"Could not get voice service from service manager: {e}")
        
        return None
    
    def _try_direct_initialization(self):
        """Try direct voice service initialization (always use direct service, skip wrapper)"""
        try:
            # Always use direct voice service for now
            logger.info("Trying direct VoiceService initialization (skipping wrapper)", print_to_terminal=True)
            from pyside_chat.features.voice.voice_service import VoiceService
            voice_service = VoiceService()
            logger.info("Direct voice service initialized successfully", print_to_terminal=True)
            return voice_service
        except Exception as e2:
            logger.error(f"Direct voice service initialization failed: {e2}", print_to_terminal=True)
            return None
    
    def _reset_voice_service(self):
        """Reset the voice service (for reinitialization)"""
        logger.info("Resetting voice service")
        
        if self._voice_service:
            try:
                # Cleanup existing service
                if hasattr(self._voice_service, 'cleanup_on_exit'):
                    self._voice_service.cleanup_on_exit()
            except Exception as e:
                logger.warning(f"Error during voice service cleanup: {e}")
        
        self._voice_service = None
        self._voice_service_initialized = False
        self._initialization_in_progress = False
        self._initialization_error = None
    
    def update_settings(self, settings: Dict[str, Any]):
        """
        Update voice service settings
        
        Args:
            settings: Dictionary of settings to apply
        """
        self._cached_settings.update(settings)
        
        if self._voice_service and self._voice_service_initialized:
            try:
                self._voice_service.update_settings(settings)
                logger.debug(f"Updated voice service settings: {settings}")
            except Exception as e:
                logger.error(f"Failed to update voice service settings: {e}")
        else:
            logger.debug(f"Cached settings for later application: {settings}")
    
    def get_settings(self) -> Dict[str, Any]:
        """Get current voice service settings"""
        if self._voice_service and self._voice_service_initialized:
            try:
                return self._voice_service.voice_settings.copy()
            except Exception as e:
                logger.error(f"Failed to get voice service settings: {e}")
        
        return self._cached_settings.copy()
    
    def is_ready(self) -> bool:
        """Check if voice service is ready"""
        ready = self._voice_service_initialized and self._voice_service is not None
        logger.debug(f"Voice service ready check: initialized={self._voice_service_initialized}, service={self._voice_service is not None}, ready={ready}")
        return ready
    
    def is_initializing(self) -> bool:
        """Check if voice service is currently initializing"""
        return self._initialization_in_progress
    
    def get_last_error(self) -> Optional[str]:
        """Get the last initialization error"""
        return self._initialization_error
    
    def register_ready_callback(self, callback):
        """
        Register a callback to be called when voice service becomes ready
        
        Args:
            callback: Function to call with voice service as argument
        """
        if self.is_ready():
            # Service is already ready, call immediately
            try:
                callback(self._voice_service)
            except Exception as e:
                logger.error(f"Error in immediate ready callback: {e}")
        else:
            # Service not ready, register for later
            self._ready_callbacks.append(callback)
    
    def force_reinitialize(self):
        """Force reinitialization of the voice service"""
        logger.info("Forcing voice service reinitialization")
        self._reset_voice_service()
        self._initialize_voice_service()
    
    def cleanup(self):
        """Cleanup the voice service manager"""
        logger.info("Cleaning up voice service manager")
        
        if self._voice_service:
            try:
                if hasattr(self._voice_service, 'cleanup_on_exit'):
                    self._voice_service.cleanup_on_exit()
            except Exception as e:
                logger.error(f"Error during voice service cleanup: {e}")
        
        self._voice_service = None
        self._voice_service_initialized = False
        self._initialization_in_progress = False
        self._cached_settings.clear()
        self._ready_callbacks.clear()


# Global instance
_voice_service_manager = None

def get_voice_service_manager() -> VoiceServiceManager:
    """Get the global voice service manager instance"""
    global _voice_service_manager
    if _voice_service_manager is None:
        _voice_service_manager = VoiceServiceManager()
    return _voice_service_manager 
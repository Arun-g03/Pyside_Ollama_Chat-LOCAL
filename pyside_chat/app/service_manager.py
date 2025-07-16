"""
Service Manager - Handles initialization and management of all application services
"""

from pyside_chat.core.shared_imports.shared_imports import *


from pyside_chat.features.ollama.ollama_service import OllamaService
from pyside_chat.features.chat.conversation_service import ConversationService
from pyside_chat.features.chat.enhancers.enhancement_service import EnhancementService
from pyside_chat.features.memory.memory_service import MemoryService
from pyside_chat.features.chat.summarization.summarization_service import SummarizationService
from pyside_chat.features.personality.models.personality_model import PersonalityModel
from pyside_chat.core.models.conversation_metadata import ConversationManager
from pyside_chat.config.config_manager import ConfigManager
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ServiceManager:
    """Manages all application services and their initialization"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_manager: ConfigManager = None):
        """Initialize the service manager (singleton)"""
        if hasattr(self, '_initialized'):
            return

        self._initialized = True

        if config_manager is None:
            logger.warning("ServiceManager initialized without config_manager")
            return

        self.config_manager = config_manager
        self.ollama_service: Optional[OllamaService] = None
        self.conversation_service: Optional[ConversationService] = None
        self.enhancement_service: Optional[EnhancementService] = None
        self.memory_service: Optional[MemoryService] = None
        self.summarization_service: Optional[SummarizationService] = None
        self.personality_service: Optional[PersonalityModel] = None
        self.conversation_manager: Optional[ConversationManager] = None
        self.memory_enabled: bool = False
        self.session_variables: dict = {}

        # Voice service (singleton)
        self.voice_service = None

        self._initialize_services()

    @classmethod
    def get_instance(cls) -> 'ServiceManager':
        """Get the global service manager instance"""
        if cls._instance is None:
            raise RuntimeError(
                "ServiceManager not initialized. Call ServiceManager(config_manager) first.")
        return cls._instance

    def _initialize_services(self):
        """Initialize all application services"""
        try:
            # Initialize core services
            self.ollama_service = OllamaService(
                self.config_manager.get_ollama_url())
            self.conversation_service = ConversationService(
                self.config_manager.get_history_directory()
            )
            self.enhancement_service = EnhancementService(self.ollama_service)
            self.summarization_service = SummarizationService(
                self.ollama_service)

            # Initialize memory service based on configuration
            self.memory_enabled = self.config_manager.get(
                "memory_enabled", True)
            if self.memory_enabled:
                self.memory_service = MemoryService(
                    max_context_messages=self.config_manager.get_max_context_messages()
                )
                self.conversation_service.set_memory_service(
                    self.memory_service)
            else:
                self.memory_service = None
                self.conversation_service.set_memory_service(None)

            # Initialize personality service with error handling
            try:
                self.personality_service = PersonalityModel(config_manager=self.config_manager)
                logger.info(
                    "[ID:0095] Personality service initialized successfully")
            except Exception as e:
                logger.error(
                    f"[ID:0096] Error initializing personality service: {e}")
                self.personality_service = None

            # Initialize conversation manager
            self.conversation_manager = ConversationManager(
                self.config_manager.get_history_directory()
            )

            # Connect conversation service with conversation manager for unified saving
            self.conversation_service.set_conversation_manager(
                self.conversation_manager)

            # Initialize voice service (singleton)
            try:
                from pyside_chat.features.voice.voice_service import VoiceService
                self.voice_service = VoiceService.get_instance()
                logger.info(
                    "[ID:0097] Voice service initialized successfully")
            except Exception as e:
                logger.error(
                    f"[ID:0098] Error initializing voice service: {e}")
                self.voice_service = None

            # Initialize session variables
            self.session_variables = {
                'history': self.config_manager.is_history_enabled(),
                'wordwrap': self.config_manager.is_wordwrap_enabled(),
                'json_format': self.config_manager.is_json_format_enabled(),
                'verbose': self.config_manager.is_verbose_enabled(),
                'think': self.config_manager.is_think_enabled()
            }

            logger.info("[ID:0094] All services initialized successfully")

        except Exception as e:
            logger.error(f"[ID:0093] Error initializing services: {e}")
            raise

    def reinitialize_services(self):
        """Reinitialize services (used when configuration changes)"""
        logger.info("[ID:0092] Reinitializing services...")
        self._initialize_services()

    def get_ollama_service(self) -> OllamaService:
        """Get the Ollama service instance"""
        return self.ollama_service

    def get_conversation_service(self) -> ConversationService:
        """Get the conversation service instance"""
        return self.conversation_service

    def get_enhancement_service(self) -> EnhancementService:
        """Get the enhancement service instance"""
        return self.enhancement_service

    def get_memory_service(self) -> Optional[MemoryService]:
        """Get the memory service instance (may be None if disabled)"""
        return self.memory_service

    def get_summarization_service(self) -> SummarizationService:
        """Get the summarization service instance"""
        return self.summarization_service

    def get_conversation_manager(self) -> ConversationManager:
        """Get the conversation manager instance"""
        return self.conversation_manager

    def get_personality_service(self) -> PersonalityModel:
        """Get the personality service instance"""
        return self.personality_service

    def get_voice_service(self):
        """Get the voice service instance"""
        return self.voice_service

    def is_voice_service_initialized(self) -> bool:
        """Check if voice service has been initialized"""
        if self.voice_service:
            return self.voice_service.is_voice_available()
        return False

    def is_memory_enabled(self) -> bool:
        """Check if memory is enabled"""
        return self.memory_enabled

    def get_config_manager(self) -> ConfigManager:
        """Get the config manager"""
        return self.config_manager

    def get_session_variables(self) -> dict:
        """Get session variables"""
        return self.session_variables.copy()

    def cleanup(self):
        """Clean up services on application shutdown"""
        try:
            if self.ollama_service:
                # Any cleanup needed for Ollama service
                pass

            if self.memory_service:
                # Any cleanup needed for memory service
                pass

            # Clean up voice service
            if self.voice_service:
                try:
                    self.voice_service.cleanup()
                    logger.info(
                        "[ID:0091A] Voice service cleaned up successfully")
                except Exception as e:
                    logger.error(
                        f"[ID:0091B] Error cleaning up voice service: {e}")

            logger.info("[ID:0091] Services cleaned up successfully")

        except Exception as e:
            logger.error(f"[ID:0090] Error during service cleanup: {e}")

    def _initialize_voice_service(self):
        """Initialize voice service only when needed"""
        logger.debug("[ID:0102] Initializing voice service")
        return self.get_voice_service()

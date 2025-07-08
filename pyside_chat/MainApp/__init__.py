"""
MainApp Package - Refactored main application components
"""

from .ollama_chat import OllamaChat
from .service_manager import ServiceManager
from .ui_manager import UIManager
from .event_handler import EventHandler
from .app_lifecycle import AppLifecycleManager

__all__ = [
    'OllamaChat',
    'ServiceManager', 
    'UIManager',
    'EventHandler',
    'AppLifecycleManager'
]

__version__ = "1.0.0"
__author__ = "Ollama Chat Team"
__description__ = "Refactored main application components for better modularity" 
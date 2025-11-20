"""
UI Components Package
Contains all user interface components for the PySide Chat application.
"""

# Main UI tabs
from .chat_tab import ChatTab
from .memory_tab import MemoryTab
from .model_tab import ModelTab
from .personality_tab import PersonalityTab

# UI widgets and utilities
from .spellchecker_widget import SpellCheckerTextEdit

# Subpackages
from . import styles
from . import Widgets

__all__ = [
    'ChatTab',
    'MemoryTab',
    'ModelTab',
    'PersonalityTab',
    'SpellCheckerTextEdit',
    'styles',
    'Widgets'
]
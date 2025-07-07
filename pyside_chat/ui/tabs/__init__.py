"""
Tabs Module - UI tab components for the PySide6 chat application

This module contains all the tab widgets used in the main application:
- ChatTab: Main chat interface with voice support and EQ visualizer
- MemoryTab: Memory management and LLM memory settings
- ModelTab: Model management, pulling, removing, and updating models
- PersonalityTab: Personality selection and management
"""

from .chat_tab.chat_tab import ChatTab
from .memory_tab import MemoryTab
from .model_tab import ModelTab
from .personality_tab import PersonalityTab

__all__ = [
    'ChatTab',
    'MemoryTab', 
    'ModelTab',
    'PersonalityTab'
]

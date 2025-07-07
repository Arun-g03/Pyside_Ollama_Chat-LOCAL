"""
Chat Tab Module - Modular components for the main chat interface

This module contains all the components used in the chat tab:
- ChatTab: Main chat interface orchestrator
- ChatDisplay: Message display and editing functionality
- VoiceControls: Voice mode, TTS, and audio level handling
- EQVisualizer: Audio visualization components
- InputControls: Message input, send/cancel buttons, settings
- StreamingHandler: Message streaming and response handling
"""

from .chat_tab import ChatTab
from .chat_display import ChatDisplay
from .voice_controls import VoiceControls
from .eq_visualizer import EQVisualizer
from .input_controls import InputControls

__all__ = [
    'ChatTab',
    'ChatDisplay',
    'VoiceControls', 
    'EQVisualizer',
    'InputControls'
] 
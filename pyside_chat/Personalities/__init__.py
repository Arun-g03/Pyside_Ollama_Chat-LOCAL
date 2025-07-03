"""
Personalities Package

This package provides a comprehensive personality management system for AI chat applications.
It includes data models, services, utilities, and a main interface for managing AI personalities.

The package is organized into:
- models/: Data classes and types for personality definitions
- services/: Business logic for personality management
- utils/: Utility functions for formatting and processing
"""

# Import the main classes for easy access
from .personality_model import PersonalityModel
from .models import (
    PersonalityType, PersonalityTraits, PersonalityConfig, 
    PersonalityMetadata, PersonalityPrompt, PersonalityPronouns
)
from .services.personality_service import PersonalityService
from .services.personality_loader import PersonalityLoader
from .utils.personality_formatter import PersonalityFormatter

# For backward compatibility, also import the original model
try:
    from .personality_model import PersonalityModel as OriginalPersonalityModel
except ImportError:
    # If the original file doesn't exist, use the refactored version
    OriginalPersonalityModel = PersonalityModel

__all__ = [
    # Main interface
    'PersonalityModel',
    'OriginalPersonalityModel',
    
    # Data models
    'PersonalityType',
    'PersonalityTraits',
    'PersonalityConfig',
    'PersonalityMetadata',
    'PersonalityPrompt',
    'PersonalityPronouns',
    
    # Services
    'PersonalityService',
    'PersonalityLoader',
    
    # Utils
    'PersonalityFormatter'
]

# Version information
__version__ = "2.0.0"
__author__ = "AI Chat Application Team"
__description__ = "Comprehensive personality management system for AI chat applications" 
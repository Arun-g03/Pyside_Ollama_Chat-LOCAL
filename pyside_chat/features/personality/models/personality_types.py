"""
Personality Types - Data models for personality system

This module contains the core data classes and enums used to define
personality characteristics, configuration, and metadata.
"""

from typing import List
from dataclasses import dataclass
from enum import Enum


class PersonalityType(Enum):
    """Enumeration of available personality types"""
    ASSISTANT = "assistant"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    EDUCATOR = "educator"
    ANALYST = "analyst"
    STORYTELLER = "storyteller"
    CUSTOM = "custom"


@dataclass
class PersonalityTraits:
    """Data class for personality traits"""
    name: str
    description: str
    tone: str
    style: str
    expertise: List[str]
    conversation_style: str
    response_length: str  # "concise", "detailed", "verbose"
    formality_level: str  # "casual", "semi-formal", "formal"
    humor_level: str  # "none", "subtle", "moderate", "high"
    emoji_usage: bool
    code_formatting: bool
    examples_usage: bool
    questions_usage: bool


@dataclass
class PersonalityConfig:
    """Data class for personality-specific configuration"""
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    use_prompt_templates: bool = True  # Whether to use user/context prompt templates


@dataclass
class PersonalityMetadata:
    """Data class for personality metadata"""
    created_date: str = ""
    last_modified: str = ""
    version: str = "1.0"
    author: str = ""
    category: str = "general"
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class PersonalityPrompt:
    """Data class for personality prompt templates"""
    system_prompt: str
    user_prompt_template: str
    context_prompt: str
    examples: List[str]
    constraints: List[str]

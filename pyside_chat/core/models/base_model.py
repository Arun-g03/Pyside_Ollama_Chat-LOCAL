"""
Base model for all data models in the application.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseModel(ABC):
    """Base class for all models in the application."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model from dictionary."""
        pass

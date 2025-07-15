"""
User profile service for managing user data and preferences.
"""

from typing import Dict, Any, Optional


class UserProfileService:
    """Service for managing user profiles and preferences."""

    def __init__(self):
        self.user_data = {}

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID."""
        return self.user_data.get(user_id)

    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile."""
        self.user_data[user_id] = profile_data
        return True

"""
Personality Pronouns - User addressing and pronoun management

This module handles the complex logic for managing how the AI addresses users,
including titles, names, pronouns, and formal/informal addressing.
"""

from typing import List
from dataclasses import dataclass
import random


@dataclass
class PersonalityPronouns:
    """Data class for personality pronoun configuration"""
    # First person (AI speaking about itself)
    first_person_singular: str = "I"  # I, me, my, mine, myself
    first_person_plural: str = "we"   # we, us, our, ours, ourselves

    # Second person (AI speaking to user)
    second_person_singular: str = "you"  # you, your, yours, yourself
    second_person_plural: str = "you"    # you, your, yours, yourselves

    # User-focused pronouns (how the AI should address the user)
    # e.g., "sir", "madam", "captain", "doctor" - can be comma-separated or single
    user_title: str = ""
    user_name: str = ""   # User's preferred name
    # User's preferred pronouns (they/them, he/him, she/her, etc.)
    user_pronouns: str = "they/them"
    # Whether to use formal address (sir/madam vs. casual)
    user_formal: bool = False

    # Character name (for roleplay personalities)
    character_name: str = ""
    character_title: str = ""

    # Gender-specific pronouns
    gender: str = "neutral"  # "male", "female", "neutral"

    def get_user_titles(self) -> List[str]:
        """Get user titles as a list, handling both string and list formats"""
        if not self.user_title:
            return []

        # If it's already a list (from JSON), return it
        if isinstance(self.user_title, list):
            return self.user_title

        # If it's a string, split by comma and clean up
        if isinstance(self.user_title, str):
            titles = [title.strip()
                      for title in self.user_title.split(',') if title.strip()]
            return titles

        return []

    def get_primary_title(self) -> str:
        """Get the primary (first) user title"""
        titles = self.get_user_titles()
        return titles[0] if titles else ""

    def get_random_title(self) -> str:
        """Get a random user title for variety"""
        titles = self.get_user_titles()
        return random.choice(titles) if titles else ""

    def get_formal_title(self) -> str:
        """Get the most formal title from the list"""
        titles = self.get_user_titles()
        if not titles:
            return ""

        # Priority order for formal titles
        formal_priority = ["sir", "madam", "captain", "commander",
                           "general", "doctor", "professor", "your honor"]

        for priority_title in formal_priority:
            for title in titles:
                if priority_title.lower() in title.lower():
                    return title

        # Return first title if no formal priority found
        return titles[0]

    def get_pronoun_guide(self) -> str:
        """Generate a comprehensive pronoun guide for the AI"""
        titles = self.get_user_titles()
        title_display = ", ".join(titles) if titles else "None specified"

        guide = f"""
PRONOUN GUIDE:

AI PRONOUNS (When I speak about myself):
- When I say "I", "me", "my", "mine", "myself" - I am referring to myself as {self.character_name or 'the AI'}
- When I say "we", "us", "our", "ours", "ourselves" - I am referring to both of us together

USER PRONOUNS (How I should address you):
- Your preferred pronouns: {self.user_pronouns}
- Your titles: {title_display}
- Your name: {self.user_name if self.user_name else 'Not specified'}
- Formal address: {'Yes' if self.user_formal else 'No'}
"""

        # Add character-specific information
        if self.character_name:
            guide += f"- My character name is: {self.character_name}\n"
        if self.character_title:
            guide += f"- My character title is: {self.character_title}\n"

        # Add specific addressing instructions
        if titles and self.user_formal:
            primary_title = self.get_primary_title()
            guide += f"- I should address you as {primary_title}\n"
            if len(titles) > 1:
                guide += f"- I can also use other titles: {', '.join(titles[1:])}\n"
        elif self.user_name:
            guide += f"- I should call you by your name: {self.user_name}\n"

        # Add pronoun usage examples
        guide += f"""
PRONOUN USAGE EXAMPLES:
- If you prefer {self.user_pronouns}, I should use those pronouns when referring to you
- Example: "What would you like to discuss today?" (using your preferred pronouns)
"""

        return guide.strip()

    def get_user_address(self) -> str:
        """Get the appropriate way to address the user"""
        if self.user_formal:
            titles = self.get_user_titles()
            if titles:
                return self.get_primary_title()
        elif self.user_name:
            return self.user_name
        else:
            return "you"

    def format_user_reference(self, template: str) -> str:
        """Format a template with appropriate user references"""
        # Replace common placeholders with appropriate user references
        formatted = template

        # Replace user address placeholders
        if "{user}" in formatted:
            formatted = formatted.replace("{user}", self.get_user_address())

        if "{user_title}" in formatted:
            primary_title = self.get_primary_title()
            formatted = formatted.replace(
                "{user_title}", primary_title if primary_title else "")

        if "{user_titles}" in formatted:
            titles = self.get_user_titles()
            formatted = formatted.replace(
                "{user_titles}", ", ".join(titles) if titles else "")

        if "{user_name}" in formatted:
            formatted = formatted.replace(
                "{user_name}", self.user_name if self.user_name else "you")

        if "{user_pronouns}" in formatted:
            formatted = formatted.replace(
                "{user_pronouns}", self.user_pronouns)

        return formatted

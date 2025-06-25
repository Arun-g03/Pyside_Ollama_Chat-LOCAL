import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

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
    user_title: str = ""  # e.g., "sir", "madam", "captain", "doctor" - can be comma-separated or single
    user_name: str = ""   # User's preferred name
    user_pronouns: str = "they/them"  # User's preferred pronouns (they/them, he/him, she/her, etc.)
    user_formal: bool = False  # Whether to use formal address (sir/madam vs. casual)
    
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
            titles = [title.strip() for title in self.user_title.split(',') if title.strip()]
            return titles
        
        return []
    
    def get_primary_title(self) -> str:
        """Get the primary (first) user title"""
        titles = self.get_user_titles()
        return titles[0] if titles else ""
    
    def get_random_title(self) -> str:
        """Get a random user title for variety"""
        import random
        titles = self.get_user_titles()
        return random.choice(titles) if titles else ""
    
    def get_formal_title(self) -> str:
        """Get the most formal title from the list"""
        titles = self.get_user_titles()
        if not titles:
            return ""
        
        # Priority order for formal titles
        formal_priority = ["sir", "madam", "captain", "commander", "general", "doctor", "professor", "your honor"]
        
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
            formatted = formatted.replace("{user_title}", primary_title if primary_title else "")
        
        if "{user_titles}" in formatted:
            titles = self.get_user_titles()
            formatted = formatted.replace("{user_titles}", ", ".join(titles) if titles else "")
        
        if "{user_name}" in formatted:
            formatted = formatted.replace("{user_name}", self.user_name if self.user_name else "you")
        
        if "{user_pronouns}" in formatted:
            formatted = formatted.replace("{user_pronouns}", self.user_pronouns)
        
        return formatted

class PersonalityModel:
    """Main class for managing AI personalities"""
    
    def __init__(self, personalities_dir: str = "personalities"):
        self.personalities_dir = personalities_dir
        self.personalities: Dict[str, Dict[str, Any]] = {}
        self.current_personality: Optional[str] = None
        self.custom_personalities: Dict[str, Dict[str, Any]] = {}
        
        # Create personalities directory if it doesn't exist
        if not os.path.exists(personalities_dir):
            os.makedirs(personalities_dir)
        
        # Initialize default personalities
        self._initialize_default_personalities()
        self._load_custom_personalities()
    
    def _initialize_default_personalities(self):
        """Initialize the default personality set by loading from JSON files recursively"""
        self.personalities = {}
        
        # Recursively load all JSON files from the personalities directory and subdirectories
        for filepath in self._find_personality_files(self.personalities_dir):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    personality_data = json.load(f)
                    # Extract personality name from file path, preserving folder structure
                    personality_name = self._extract_personality_name(filepath)
                    self.personalities[personality_name] = personality_data
            except Exception as e:
                print(f"Error loading personality {filepath}: {e}")
    
    def _find_personality_files(self, directory: str) -> List[str]:
        """Recursively find all personality JSON files in the given directory and subdirectories"""
        personality_files = []
        
        if not os.path.exists(directory):
            return personality_files
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    personality_files.append(filepath)
        
        return personality_files
    
    def _extract_personality_name(self, filepath: str) -> str:
        """Extract personality name from file path, preserving folder structure for uniqueness"""
        # Get the relative path from the personalities directory
        rel_path = os.path.relpath(filepath, self.personalities_dir)
        
        # Remove the .json extension
        name_without_ext = os.path.splitext(rel_path)[0]
        
        # Replace path separators with dots to create a unique name
        # This allows personalities in subfolders to have the same base name
        # e.g., "professional/assistant.json" becomes "professional.assistant"
        personality_name = name_without_ext.replace(os.sep, '.')
        
        return personality_name
    
    def _load_custom_personalities(self):
        """Load custom personalities from JSON files (now handled in _initialize_default_personalities)"""
        # All personalities are now loaded from JSON files in _initialize_default_personalities
        # This method is kept for backward compatibility but is no longer needed
        pass
    
    def get_available_personalities(self) -> List[str]:
        """Get list of all available personality names"""
        return sorted(list(self.personalities.keys()))
    
    def get_personality(self, name: str) -> Optional[Dict[str, Any]]:
        """Get personality by name"""
        return self.personalities.get(name)
    
    def set_current_personality(self, name: str) -> bool:
        """Set the current active personality"""
        if name in self.personalities:
            self.current_personality = name
            return True
        return False
    
    def get_current_personality(self) -> Optional[Dict[str, Any]]:
        """Get the current active personality"""
        if self.current_personality:
            return self.get_personality(self.current_personality)
        return None
    
    def create_custom_personality(self, name: str, traits: PersonalityTraits, prompt: PersonalityPrompt, 
                                 config: PersonalityConfig = None, metadata: PersonalityMetadata = None) -> bool:
        """Create a new custom personality"""
        try:
            # Set default config and metadata if not provided
            if config is None:
                config = PersonalityConfig()
            if metadata is None:
                metadata = PersonalityMetadata()
                metadata.created_date = datetime.now().isoformat()
                metadata.last_modified = datetime.now().isoformat()
            
            personality_data = {
                "traits": asdict(traits),
                "prompt": asdict(prompt),
                "config": asdict(config),
                "metadata": asdict(metadata)
            }
            
            # Handle nested folder structure in the name
            # If name contains dots, treat them as folder separators
            if '.' in name:
                # Split by dots to get folder path and filename
                parts = name.split('.')
                folder_path = os.path.join(self.personalities_dir, *parts[:-1])
                filename = f"{parts[-1]}.json"
                
                # Create folder structure if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)
                filepath = os.path.join(folder_path, filename)
            else:
                # Simple case - save in root personalities directory
                filepath = os.path.join(self.personalities_dir, f"{name}.json")
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(personality_data, f, indent=2, ensure_ascii=False)
            
            # Add to personalities
            self.personalities[name] = personality_data
            return True
        except Exception as e:
            print(f"Error creating personality {name}: {e}")
            return False
    
    def delete_custom_personality(self, name: str) -> bool:
        """Delete a custom personality"""
        if name in self.personalities:
            try:
                # Find the actual file path for this personality
                filepath = self._find_personality_file_by_name(name)
                if filepath and os.path.exists(filepath):
                    os.remove(filepath)
                
                # Remove from memory
                del self.personalities[name]
                return True
            except Exception as e:
                print(f"Error deleting personality {name}: {e}")
                return False
        return False
    
    def _find_personality_file_by_name(self, personality_name: str) -> Optional[str]:
        """Find the actual file path for a personality by its name"""
        # Convert personality name back to file path
        if '.' in personality_name:
            # Handle nested structure
            parts = personality_name.split('.')
            filename = f"{parts[-1]}.json"
            folder_path = os.path.join(self.personalities_dir, *parts[:-1])
            filepath = os.path.join(folder_path, filename)
        else:
            # Simple case - look in root directory
            filepath = os.path.join(self.personalities_dir, f"{personality_name}.json")
        
        return filepath if os.path.exists(filepath) else None
    
    def refresh_personalities(self) -> bool:
        """Refresh personalities from disk, reloading all JSON files"""
        try:
            # Store current personality to restore it after refresh
            current_personality = self.current_personality
            
            # Reinitialize personalities
            self._initialize_default_personalities()
            
            # Restore current personality if it still exists
            if current_personality and current_personality in self.personalities:
                self.current_personality = current_personality
            elif self.personalities:
                # Set to first available personality if current one no longer exists
                self.current_personality = list(self.personalities.keys())[0]
            
            return True
        except Exception as e:
            print(f"Error refreshing personalities: {e}")
            return False
    
    def format_prompt_with_personality(self, user_input: str, context: str = "") -> str:
        """Format a prompt using the current personality's prompt templates"""
        current_personality = self.get_current_personality()
        if not current_personality:
            # Default to assistant personality if available, otherwise use first available
            if "assistant" in self.personalities:
                current_personality = self.personalities["assistant"]
            elif self.personalities:
                # Use the first available personality
                first_personality_name = list(self.personalities.keys())[0]
                current_personality = self.personalities[first_personality_name]
            else:
                # No personalities available, return user input as-is
                return user_input
        
        prompt_data = current_personality.get("prompt", {})
        config_data = current_personality.get("config", {})
        pronouns_data = prompt_data.get("pronouns", {})
        
        # Create pronouns object for user reference formatting
        pronouns = PersonalityPronouns(**pronouns_data) if pronouns_data else PersonalityPronouns()
        
        # Check if prompt templates should be used
        use_templates = config_data.get("use_prompt_templates", True)
        
        if not use_templates:
            # Return user input directly if templates are disabled
            return user_input
        
        if context:
            # Use context prompt template if available
            context_template = prompt_data.get("context_prompt", "{user_input}")
            # Format template with user references
            formatted_template = pronouns.format_user_reference(context_template)
            return formatted_template.format(
                context=context,
                user_input=user_input
            )
        else:
            # Use user prompt template if available
            user_template = prompt_data.get("user_prompt_template", "{user_input}")
            # Format template with user references
            formatted_template = pronouns.format_user_reference(user_template)
            return formatted_template.format(user_input=user_input)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current personality"""
        current_personality = self.get_current_personality()
        if current_personality:
            return current_personality["prompt"]["system_prompt"]
        
        # Fallback to assistant personality if available, otherwise use first available
        if "assistant" in self.personalities:
            return self.personalities["assistant"]["prompt"]["system_prompt"]
        elif self.personalities:
            # Use the first available personality
            first_personality_name = list(self.personalities.keys())[0]
            return self.personalities[first_personality_name]["prompt"]["system_prompt"]
        else:
            # No personalities available, return empty string
            return ""
    
    def get_personality_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a personality"""
        personality = self.get_personality(name)
        if personality:
            traits = personality["traits"]
            return {
                "name": traits["name"],
                "description": traits["description"],
                "tone": traits["tone"],
                "style": traits["style"],
                "expertise": traits["expertise"],
                "conversation_style": traits["conversation_style"],
                "response_length": traits["response_length"],
                "formality_level": traits["formality_level"],
                "humor_level": traits["humor_level"],
                "emoji_usage": traits["emoji_usage"],
                "code_formatting": traits["code_formatting"],
                "examples_usage": traits["examples_usage"],
                "questions_usage": traits["questions_usage"]
            }
        return None

    def get_personality_config(self, name: str = None) -> Optional[PersonalityConfig]:
        """Get configuration for a personality"""
        if name is None:
            name = self.current_personality
        
        personality = self.get_personality(name)
        if personality and "config" in personality:
            config_data = personality["config"]
            return PersonalityConfig(**config_data)
        return None

    def update_personality_metadata(self, name: str, **kwargs) -> bool:
        """Update metadata for a personality"""
        personality = self.get_personality(name)
        if not personality:
            return False
        
        # Get current metadata or create new
        metadata_data = personality.get("metadata", {})
        metadata = PersonalityMetadata(**metadata_data)
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
        
        # Update last modified
        metadata.last_modified = datetime.now().isoformat()
        
        # Save back to personality
        personality["metadata"] = asdict(metadata)
        
        # Save to file
        try:
            filepath = self._find_personality_file_by_name(name)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(personality, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error updating personality metadata {name}: {e}")
            return False

    def build_comprehensive_system_prompt(self) -> str:
        """Build a comprehensive system prompt with pronoun guidance"""
        current_personality = self.get_current_personality()
        if not current_personality:
            return ""
        
        traits = current_personality.get('traits', {})
        prompt_data = current_personality.get('prompt', {})
        pronouns_data = prompt_data.get('pronouns', {})
        
        # Create pronouns object
        pronouns = PersonalityPronouns(**pronouns_data) if pronouns_data else PersonalityPronouns()
        
        # Build comprehensive prompt
        comprehensive_prompt = []
        
        # 1. Main system prompt
        main_prompt = prompt_data.get('system_prompt', '')
        if main_prompt:
            # Format the main prompt with user references if any placeholders exist
            main_prompt = pronouns.format_user_reference(main_prompt)
            comprehensive_prompt.append(main_prompt)
        
        # 2. Add comprehensive pronoun guide
        pronoun_guide = pronouns.get_pronoun_guide()
        if pronoun_guide:
            comprehensive_prompt.append("\n\n" + pronoun_guide)
        
        # 3. Add personality traits
        if traits:
            comprehensive_prompt.append("\n\nPERSONALITY TRAITS:")
            comprehensive_prompt.append(f"• Name: {traits.get('name', 'Unknown')}")
            comprehensive_prompt.append(f"• Tone: {traits.get('tone', 'Unknown')}")
            comprehensive_prompt.append(f"• Style: {traits.get('style', 'Unknown')}")
            comprehensive_prompt.append(f"• Conversation Style: {traits.get('conversation_style', 'Unknown')}")
            comprehensive_prompt.append(f"• Response Length: {traits.get('response_length', 'Unknown')}")
            comprehensive_prompt.append(f"• Formality Level: {traits.get('formality_level', 'Unknown')}")
            comprehensive_prompt.append(f"• Humor Level: {traits.get('humor_level', 'Unknown')}")
            
            # Add expertise areas
            expertise = traits.get('expertise', [])
            if expertise:
                comprehensive_prompt.append(f"• Expertise: {', '.join(expertise)}")
            
            # Add feature flags
            features = []
            if traits.get('emoji_usage', False):
                features.append("Use emojis")
            if traits.get('code_formatting', False):
                features.append("Format code properly")
            if traits.get('examples_usage', False):
                features.append("Provide examples when helpful")
            if traits.get('questions_usage', False):
                features.append("Ask questions when appropriate")
            
            if features:
                comprehensive_prompt.append(f"• Features: {', '.join(features)}")
        
        # 4. Add examples if available
        examples = prompt_data.get('examples', [])
        if examples:
            comprehensive_prompt.append("\n\nEXAMPLE RESPONSES:")
            for i, example in enumerate(examples, 1):
                # Format examples with user references
                formatted_example = pronouns.format_user_reference(example)
                comprehensive_prompt.append(f"{i}. {formatted_example}")
        
        # 5. Add constraints
        constraints = prompt_data.get('constraints', [])
        if constraints:
            comprehensive_prompt.append("\n\nCONSTRAINTS:")
            for constraint in constraints:
                # Format constraints with user references
                formatted_constraint = pronouns.format_user_reference(constraint)
                comprehensive_prompt.append(f"• {formatted_constraint}")
        
        return "\n".join(comprehensive_prompt)

# Example usage and testing
if __name__ == "__main__":
    # Create personality model instance
    pm = PersonalityModel()
    
    # List available personalities
    print("Available personalities:")
    for personality in pm.get_available_personalities():
        print(f"- {personality}")
    
    # Test setting and getting current personality
    pm.set_current_personality("creative")
    current = pm.get_current_personality()
    print(f"\nCurrent personality: {current['traits']['name']}")
    
    # Test prompt formatting
    formatted_prompt = pm.format_prompt_with_personality("Write a story about a robot")
    print(f"\nFormatted prompt:\n{formatted_prompt}")
    
    # Test creating a custom personality
    custom_traits = PersonalityTraits(
        name="Code Mentor",
        description="A programming mentor that helps with coding challenges",
        tone="encouraging and educational",
        style="practical and hands-on",
        expertise=["programming", "debugging", "software design"],
        conversation_style="mentoring",
        response_length="detailed",
        formality_level="semi-formal",
        humor_level="subtle",
        emoji_usage=False,
        code_formatting=True,
        examples_usage=True,
        questions_usage=True
    )
    
    custom_prompt = PersonalityPrompt(
        system_prompt="You are a code mentor - an experienced programmer who helps students and developers improve their coding skills through guidance, examples, and best practices.",
        user_prompt_template="Coding Question: {user_input}\nMentor:",
        context_prompt="Previous coding session:\n{context}\n\nNew question: {user_input}",
        examples=[
            "Let me walk you through this step by step.",
            "Here's how we can approach this problem..."
        ],
        constraints=[
            "Always provide educational explanations",
            "Include code examples when helpful",
            "Encourage good programming practices"
        ]
    )
    
    success = pm.create_custom_personality("code_mentor", custom_traits, custom_prompt)
    print(f"\nCustom personality created: {success}")

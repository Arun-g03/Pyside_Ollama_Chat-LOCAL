"""
Personality Formatter - Prompt formatting utilities

This module handles formatting prompts with personality-specific templates
and building comprehensive system prompts.
"""

from typing import Dict, Any, Optional, List

from ..models import PersonalityPronouns


class PersonalityFormatter:
    """Handles formatting prompts and building system prompts with personality data"""
    
    @staticmethod
    def format_prompt_with_personality(personality_data: Dict[str, Any], user_input: str, context: str = "") -> str:
        """Format a prompt using the personality's prompt templates"""
        if not personality_data:
            return user_input
        
        prompt_data = personality_data.get("prompt", {})
        config_data = personality_data.get("config", {})
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
    
    @staticmethod
    def build_comprehensive_system_prompt(personality_data: Dict[str, Any]) -> str:
        """Build a comprehensive system prompt with pronoun guidance"""
        if not personality_data:
            return ""
        
        traits = personality_data.get('traits', {})
        prompt_data = personality_data.get('prompt', {})
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
    
    @staticmethod
    def get_system_prompt(personality_data: Dict[str, Any]) -> str:
        """Get the system prompt for a personality"""
        if personality_data:
            return personality_data.get("prompt", {}).get("system_prompt", "")
        return ""
    
    @staticmethod
    def get_personality_info(personality_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get detailed information about a personality"""
        if not personality_data:
            return None
            
        traits = personality_data.get("traits", {})
        if not traits:
            return None
            
        return {
            "name": traits.get("name", ""),
            "description": traits.get("description", ""),
            "tone": traits.get("tone", ""),
            "style": traits.get("style", ""),
            "expertise": traits.get("expertise", []),
            "conversation_style": traits.get("conversation_style", ""),
            "response_length": traits.get("response_length", ""),
            "formality_level": traits.get("formality_level", ""),
            "humor_level": traits.get("humor_level", ""),
            "emoji_usage": traits.get("emoji_usage", False),
            "code_formatting": traits.get("code_formatting", False),
            "examples_usage": traits.get("examples_usage", False),
            "questions_usage": traits.get("questions_usage", False)
        }
    
    @staticmethod
    def validate_personality_data(personality_data: Dict[str, Any]) -> List[str]:
        """Validate personality data and return list of errors"""
        errors = []
        
        # Check required sections
        required_sections = ["traits", "prompt"]
        for section in required_sections:
            if section not in personality_data:
                errors.append(f"Missing required section: {section}")
        
        if not errors:
            traits = personality_data.get("traits", {})
            prompt = personality_data.get("prompt", {})
            
            # Validate traits
            required_traits = ["name", "description", "tone", "style", "expertise", 
                             "conversation_style", "response_length", "formality_level", 
                             "humor_level"]
            for trait in required_traits:
                if trait not in traits:
                    errors.append(f"Missing required trait: {trait}")
            
            # Validate prompt
            required_prompt_fields = ["system_prompt", "user_prompt_template", "context_prompt"]
            for field in required_prompt_fields:
                if field not in prompt:
                    errors.append(f"Missing required prompt field: {field}")
        
        return errors
    
    @staticmethod
    def format_personality_summary(personality_data: Dict[str, Any]) -> str:
        """Format a brief summary of a personality"""
        if not personality_data:
            return "No personality data available"
        
        traits = personality_data.get("traits", {})
        metadata = personality_data.get("metadata", {})
        
        summary_parts = []
        
        # Basic info
        name = traits.get("name", "Unknown")
        description = traits.get("description", "No description")
        summary_parts.append(f"**{name}**")
        summary_parts.append(description)
        
        # Style info
        tone = traits.get("tone", "")
        style = traits.get("style", "")
        if tone or style:
            style_info = []
            if tone:
                style_info.append(f"Tone: {tone}")
            if style:
                style_info.append(f"Style: {style}")
            summary_parts.append(" | ".join(style_info))
        
        # Expertise
        expertise = traits.get("expertise", [])
        if expertise:
            summary_parts.append(f"Expertise: {', '.join(expertise)}")
        
        # Metadata
        category = metadata.get("category", "")
        if category:
            summary_parts.append(f"Category: {category}")
        
        return "\n".join(summary_parts)
    
    @staticmethod
    def create_personality_template(name: str, description: str = "") -> Dict[str, Any]:
        """Create a template personality data structure"""
        from ..models import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
        
        traits = PersonalityTraits(
            name=name,
            description=description or f"A {name} personality",
            tone="friendly",
            style="helpful",
            expertise=["general"],
            conversation_style="conversational",
            response_length="detailed",
            formality_level="semi-formal",
            humor_level="subtle",
            emoji_usage=False,
            code_formatting=True,
            examples_usage=True,
            questions_usage=True
        )
        
        prompt = PersonalityPrompt(
            system_prompt=f"You are a {name} - {description or 'a helpful AI assistant'}.",
            user_prompt_template="{user_input}",
            context_prompt="Context: {context}\n\nUser: {user_input}",
            examples=[],
            constraints=[]
        )
        
        config = PersonalityConfig()
        metadata = PersonalityMetadata(
            category="custom",
            tags=[name.lower()]
        )
        
        return {
            "traits": traits.__dict__,
            "prompt": prompt.__dict__,
            "config": config.__dict__,
            "metadata": metadata.__dict__
        } 
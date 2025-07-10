"""
Personality Loader - File operations for personality management

This module handles loading and saving personality data from/to JSON files,
including recursive directory scanning and file path management.
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from datetime import datetime

from ..models import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class PersonalityLoader:
    """Handles loading and saving personality data from/to files"""
    
    def __init__(self, personalities_dir: str = "pyside_chat/Personalities/personality_Profiles"):
        self.personalities_dir = personalities_dir
        
        # Create personalities directory if it doesn't exist
        if not os.path.exists(personalities_dir):
            os.makedirs(personalities_dir)
        
        # Create Custom folder for custom personalities
        custom_dir = os.path.join(personalities_dir, "Custom")
        if not os.path.exists(custom_dir):
            os.makedirs(custom_dir)
    
    def find_personality_files(self, directory: str = None) -> List[str]:
        """Recursively find all personality JSON files in the given directory and subdirectories"""
        if directory is None:
            directory = self.personalities_dir
            
        personality_files = []
        
        if not os.path.exists(directory):
            return personality_files
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    personality_files.append(filepath)
        
        return personality_files
    
    def extract_personality_name(self, filepath: str) -> str:
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
    
    def load_personality_from_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load a single personality from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                personality_data = json.load(f)
                return personality_data
        except Exception as e:
            logger.debug(f"Error loading personality {filepath}: {e}",print_to_terminal=True)
            return None
    
    def load_all_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Load all personalities from JSON files recursively"""
        personalities = {}
        
        for filepath in self.find_personality_files():
            personality_data = self.load_personality_from_file(filepath)
            if personality_data:
                personality_name = self.extract_personality_name(filepath)
                personalities[personality_name] = personality_data
        
        return personalities
    
    def save_personality_to_file(self, name: str, personality_data: Dict[str, Any]) -> bool:
        """Save a personality to a JSON file"""
        try:
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
            
            return True
        except Exception as e:
            logger.debug(f"Error saving personality {name}: {e}",print_to_terminal=True)
            return False
    
    def find_personality_file_by_name(self, personality_name: str) -> Optional[str]:
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
    
    def delete_personality_file(self, name: str) -> bool:
        """Delete a personality file"""
        try:
            filepath = self.find_personality_file_by_name(name)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            logger.debug(f"Error deleting personality {name}: {e}",print_to_terminal=True)
            return False
    
    def create_personality_data(self, traits: PersonalityTraits, prompt: PersonalityPrompt, 
                               config: PersonalityConfig = None, metadata: PersonalityMetadata = None) -> Dict[str, Any]:
        """Create personality data dictionary from component objects"""
        # Set default config and metadata if not provided
        if config is None:
            config = PersonalityConfig()
        if metadata is None:
            metadata = PersonalityMetadata()
        
        personality_data = {
            "traits": asdict(traits),
            "prompt": asdict(prompt),
            "config": asdict(config),
            "metadata": asdict(metadata)
        }
        
        return personality_data
    
    def validate_personality_file(self, filepath: str) -> List[str]:
        """Validate a personality file and return list of errors"""
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                personality_data = json.load(f)
            
            # Use the formatter to validate the data
            from ..utils.personality_formatter import PersonalityFormatter
            errors = PersonalityFormatter.validate_personality_data(personality_data)
            
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {e}")
        except Exception as e:
            errors.append(f"Error reading file: {e}")
        
        return errors
    
    def backup_personality(self, name: str, backup_dir: str = None) -> bool:
        """Create a backup of a personality file"""
        try:
            filepath = self.find_personality_file_by_name(name)
            if not filepath or not os.path.exists(filepath):
                return False
            
            # Create backup directory if not provided
            if backup_dir is None:
                backup_dir = os.path.join(self.personalities_dir, "backups")
            
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Create backup filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{name}_{timestamp}.json"
            backup_filepath = os.path.join(backup_dir, backup_filename)
            
            # Copy the file
            import shutil
            shutil.copy2(filepath, backup_filepath)
            
            return True
        except Exception as e:
            logger.debug(f"Error backing up personality {name}: {e}",print_to_terminal=True)
            return False
    
    def restore_personality_from_backup(self, backup_filepath: str) -> bool:
        """Restore a personality from a backup file"""
        try:
            # Validate the backup file
            errors = self.validate_personality_file(backup_filepath)
            if errors:
                logger.debug(f"Backup file validation errors: {errors}",print_to_terminal=True)
                return False
            
            # Extract personality name from backup filename
            backup_filename = os.path.basename(backup_filepath)
            # Remove timestamp and extension
            name_with_timestamp = os.path.splitext(backup_filename)[0]
            # Extract original name (everything before the last underscore)
            name_parts = name_with_timestamp.rsplit('_', 1)
            if len(name_parts) < 2:
                logger.debug("Invalid backup filename format",print_to_terminal=True)
                return False
            
            original_name = name_parts[0]
            
            # Save to the main personalities directory
            with open(backup_filepath, 'r', encoding='utf-8') as f:
                personality_data = json.load(f)
            
            return self.save_personality_to_file(original_name, personality_data)
            
        except Exception as e:
            logger.debug(f"Error restoring personality from backup: {e}",print_to_terminal=True)
            return False
    
    def get_personality_file_info(self, filepath: str) -> Dict[str, Any]:
        """Get information about a personality file"""
        info = {
            "filepath": filepath,
            "exists": False,
            "size": 0,
            "last_modified": None,
            "errors": []
        }
        
        if os.path.exists(filepath):
            info["exists"] = True
            info["size"] = os.path.getsize(filepath)
            info["last_modified"] = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            
            # Validate the file
            info["errors"] = self.validate_personality_file(filepath)
        
        return info
    
    def list_backup_files(self, backup_dir: str = None) -> List[str]:
        """List all backup files"""
        if backup_dir is None:
            backup_dir = os.path.join(self.personalities_dir, "backups")
        
        backup_files = []
        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                if filename.endswith('.json'):
                    backup_files.append(os.path.join(backup_dir, filename))
        
        return sorted(backup_files, reverse=True)  # Most recent first 
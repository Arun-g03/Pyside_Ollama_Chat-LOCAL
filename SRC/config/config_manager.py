import json
import os
from typing import Dict, Any, Optional
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class ConfigManager:
    """Manages application configuration settings"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default if not exists"""
        default_config = {
            "default_model": "llama2",
            "default_temperature": 0.7,
            "default_personality": "assistant",
            "auto_save_enabled": True,
            "spellcheck_enabled": True,
            "window_size": {
                "width": 1200,
                "height": 800
            },
            "chat_settings": {
                "max_tokens": 2048,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self.merge_configs(default_config, loaded_config)
            except Exception as e:
                logger.debug(f"Error loading config: {e}, using defaults",print_to_terminal=True)
                return default_config
        else:
            # Create default config file
            self.save_config(default_config)
            return default_config
    
    def merge_configs(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with defaults, ensuring all keys exist"""
        merged = default.copy()
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.debug(f"Error saving config: {e}",print_to_terminal=True)
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Set a configuration value"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated config
        return self.save_config()
    
    def get_default_model(self) -> str:
        """Get the default model name"""
        return self.get("default_model", "llama2")
    
    def set_default_model(self, model_name: str) -> bool:
        """Set the default model name"""
        return self.set("default_model", model_name)
    
    def get_default_temperature(self) -> float:
        """Get the default temperature"""
        return self.get("default_temperature", 0.7)
    
    def set_default_temperature(self, temperature: float) -> bool:
        """Set the default temperature"""
        return self.set("default_temperature", temperature)
    
    def get_default_personality(self) -> str:
        """Get the default personality"""
        return self.get("default_personality", "assistant")
    
    def set_default_personality(self, personality: str) -> bool:
        """Set the default personality"""
        return self.set("default_personality", personality)
    
    def get_window_size(self) -> tuple:
        """Get the default window size"""
        size = self.get("window_size", {"width": 1200, "height": 800})
        return (size.get("width", 1200), size.get("height", 800))
    
    def set_window_size(self, width: int, height: int) -> bool:
        """Set the default window size"""
        return self.set("window_size", {"width": width, "height": height})
    
    def get_chat_settings(self) -> Dict[str, Any]:
        """Get chat settings"""
        return self.get("chat_settings", {
            "max_tokens": 2048,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        })
    
    def is_auto_save_enabled(self) -> bool:
        """Check if auto-save is enabled"""
        return self.get("auto_save_enabled", True)
    
    def set_auto_save_enabled(self, enabled: bool) -> bool:
        """Set auto-save enabled/disabled"""
        return self.set("auto_save_enabled", enabled)
    
    def is_spellcheck_enabled(self) -> bool:
        """Check if spellcheck is enabled"""
        return self.get("spellcheck_enabled", True)
    
    def set_spellcheck_enabled(self, enabled: bool) -> bool:
        """Set spellcheck enabled/disabled"""
        return self.set("spellcheck_enabled", enabled)
    
    def get_ollama_url(self) -> str:
        """Get the Ollama API URL"""
        return self.get("ollama_url", "http://127.0.0.1:11434/api")
    
    
    def set_ollama_url(self, url: str) -> bool:
        """Set the Ollama API URL"""
        return self.set("ollama_url", url)
    
    def get_history_directory(self) -> str:
        """Get the chat history directory"""
        return self.get("history_directory", "User_history/Chat_history")
    
    def set_history_directory(self, directory: str) -> bool:
        """Set the chat history directory"""
        return self.set("history_directory", directory)
    
    def is_enhancement_enabled(self) -> bool:
        """Check if response enhancement is enabled"""
        return self.get("enhancement_enabled", True)
    
    def set_enhancement_enabled(self, enabled: bool) -> bool:
        """Set response enhancement enabled/disabled"""
        return self.set("enhancement_enabled", enabled)
    
    def is_history_enabled(self) -> bool:
        """Check if history is enabled"""
        return self.get("history_enabled", True)
    
    def set_history_enabled(self, enabled: bool) -> bool:
        """Set history enabled/disabled"""
        return self.set("history_enabled", enabled)
    
    def is_wordwrap_enabled(self) -> bool:
        """Check if wordwrap is enabled"""
        return self.get("wordwrap_enabled", True)
    
    def set_wordwrap_enabled(self, enabled: bool) -> bool:
        """Set wordwrap enabled/disabled"""
        return self.set("wordwrap_enabled", enabled)
    
    def is_json_format_enabled(self) -> bool:
        """Check if JSON format is enabled"""
        return self.get("json_format_enabled", False)
    
    def set_json_format_enabled(self, enabled: bool) -> bool:
        """Set JSON format enabled/disabled"""
        return self.set("json_format_enabled", enabled)
    
    def is_verbose_enabled(self) -> bool:
        """Check if verbose is enabled"""
        return self.get("verbose_enabled", False)
    
    def set_verbose_enabled(self, enabled: bool) -> bool:
        """Set verbose enabled/disabled"""
        return self.set("verbose_enabled", enabled)
    
    def is_think_enabled(self) -> bool:
        """Check if think mode is enabled"""
        return self.get("think_enabled", False)
    
    def set_think_enabled(self, enabled: bool) -> bool:
        """Set think mode enabled/disabled"""
        return self.set("think_enabled", enabled)
    
    def get_max_tokens(self):
        return self.config.get('chat_settings', {}).get('max_tokens', 2048)
    
    def get_top_p(self):
        return self.config.get('chat_settings', {}).get('top_p', 0.9)
    
    def get_frequency_penalty(self):
        return self.config.get('chat_settings', {}).get('frequency_penalty', 0.0)
    
    def get_presence_penalty(self):
        """Get the presence penalty setting"""
        return self.get("chat_settings.presence_penalty", 0.0)
    
    def get_max_context_messages(self) -> int:
        """Get the maximum number of context messages for memory management"""
        return self.get("max_context_messages", 20)
    
    def set_max_context_messages(self, max_messages: int) -> bool:
        """Set the maximum number of context messages for memory management"""
        return self.set("max_context_messages", max_messages) 
"""
Persistent Thread Configuration

This module provides configuration settings for persistent thread pools,
allowing easy adjustment of pool sizes, timeouts, and other parameters.
"""

from typing import Dict, Any

# Default configuration for persistent thread pools
DEFAULT_PERSISTENT_THREAD_CONFIG = {
    'chat_streaming': {
        'size': 2,  # Number of threads to keep in pool
        # Max time to wait for available thread (seconds)
        'max_wait_time': 30.0,
        # Time before idle thread is cleaned up (seconds)
        'idle_timeout': 300.0,
        'description': 'Chat response streaming threads'
    },
    'audio_streaming': {
        'size': 1,
        'max_wait_time': 10.0,
        'idle_timeout': 180.0,
        'description': 'Audio processing streaming threads'
    },
    'monitoring': {
        'size': 1,
        'max_wait_time': 5.0,
        'idle_timeout': 600.0,  # Longer timeout for monitoring
        'description': 'System monitoring threads'
    },
    'voice_processing': {
        'size': 1,
        'max_wait_time': 15.0,
        'idle_timeout': 240.0,
        'description': 'Voice processing threads'
    },
    'file_processing': {
        'size': 2,
        'max_wait_time': 20.0,
        'idle_timeout': 120.0,
        'description': 'File processing threads'
    },
    'data_processing': {
        'size': 3,
        'max_wait_time': 25.0,
        'idle_timeout': 180.0,
        'description': 'Data processing threads'
    }
}

# Performance-optimized configuration for high-load scenarios
HIGH_PERFORMANCE_CONFIG = {
    'chat_streaming': {
        'size': 4,  # More threads for concurrent chat sessions
        'max_wait_time': 15.0,
        'idle_timeout': 180.0,
        'description': 'High-performance chat streaming threads'
    },
    'audio_streaming': {
        'size': 2,
        'max_wait_time': 5.0,
        'idle_timeout': 120.0,
        'description': 'High-performance audio streaming threads'
    },
    'monitoring': {
        'size': 2,
        'max_wait_time': 3.0,
        'idle_timeout': 300.0,
        'description': 'High-performance monitoring threads'
    },
    'voice_processing': {
        'size': 2,
        'max_wait_time': 10.0,
        'idle_timeout': 120.0,
        'description': 'High-performance voice processing threads'
    },
    'file_processing': {
        'size': 4,
        'max_wait_time': 10.0,
        'idle_timeout': 60.0,
        'description': 'High-performance file processing threads'
    },
    'data_processing': {
        'size': 6,
        'max_wait_time': 15.0,
        'idle_timeout': 120.0,
        'description': 'High-performance data processing threads'
    }
}

# Resource-conservative configuration for low-resource systems
LOW_RESOURCE_CONFIG = {
    'chat_streaming': {
        'size': 1,  # Single thread to conserve resources
        'max_wait_time': 60.0,  # Longer wait time
        'idle_timeout': 600.0,  # Longer idle timeout
        'description': 'Low-resource chat streaming thread'
    },
    'audio_streaming': {
        'size': 1,
        'max_wait_time': 30.0,
        'idle_timeout': 300.0,
        'description': 'Low-resource audio streaming thread'
    },
    'monitoring': {
        'size': 1,
        'max_wait_time': 10.0,
        'idle_timeout': 900.0,  # Very long idle timeout
        'description': 'Low-resource monitoring thread'
    },
    'voice_processing': {
        'size': 1,
        'max_wait_time': 45.0,
        'idle_timeout': 360.0,
        'description': 'Low-resource voice processing thread'
    },
    'file_processing': {
        'size': 1,
        'max_wait_time': 40.0,
        'idle_timeout': 240.0,
        'description': 'Low-resource file processing thread'
    },
    'data_processing': {
        'size': 1,
        'max_wait_time': 50.0,
        'idle_timeout': 300.0,
        'description': 'Low-resource data processing thread'
    }
}

# Development configuration with more debugging
DEVELOPMENT_CONFIG = {
    'chat_streaming': {
        'size': 1,  # Single thread for easier debugging
        'max_wait_time': 10.0,
        'idle_timeout': 120.0,
        'description': 'Development chat streaming thread'
    },
    'audio_streaming': {
        'size': 1,
        'max_wait_time': 5.0,
        'idle_timeout': 60.0,
        'description': 'Development audio streaming thread'
    },
    'monitoring': {
        'size': 1,
        'max_wait_time': 3.0,
        'idle_timeout': 180.0,
        'description': 'Development monitoring thread'
    },
    'voice_processing': {
        'size': 1,
        'max_wait_time': 8.0,
        'idle_timeout': 90.0,
        'description': 'Development voice processing thread'
    },
    'file_processing': {
        'size': 1,
        'max_wait_time': 15.0,
        'idle_timeout': 60.0,
        'description': 'Development file processing thread'
    },
    'data_processing': {
        'size': 1,
        'max_wait_time': 20.0,
        'idle_timeout': 90.0,
        'description': 'Development data processing thread'
    }
}


def get_persistent_thread_config(config_type: str = 'default') -> Dict[str, Any]:
    """
    Get persistent thread configuration based on type.

    Args:
        config_type: Type of configuration ('default', 'high_performance', 'low_resource', 'development')

    Returns:
        dict: Configuration for persistent thread pools
    """
    configs = {
        'default': DEFAULT_PERSISTENT_THREAD_CONFIG,
        'high_performance': HIGH_PERFORMANCE_CONFIG,
        'low_resource': LOW_RESOURCE_CONFIG,
        'development': DEVELOPMENT_CONFIG
    }

    return configs.get(config_type, DEFAULT_PERSISTENT_THREAD_CONFIG)


def validate_persistent_thread_config(config: Dict[str, Any]) -> bool:
    """
    Validate persistent thread configuration.

    Args:
        config: Configuration to validate

    Returns:
        bool: True if configuration is valid
    """
    try:
        required_keys = ['size', 'max_wait_time', 'idle_timeout']

        for thread_type, thread_config in config.items():
            # Check required keys
            for key in required_keys:
                if key not in thread_config:
                    print(
                        f"Missing required key '{key}' in {thread_type} configuration")
                    return False

            # Validate values
            if thread_config['size'] < 1:
                print(f"Invalid size for {thread_type}: must be >= 1")
                return False

            if thread_config['max_wait_time'] < 0:
                print(f"Invalid max_wait_time for {thread_type}: must be >= 0")
                return False

            if thread_config['idle_timeout'] < 0:
                print(f"Invalid idle_timeout for {thread_type}: must be >= 0")
                return False

        return True

    except Exception as e:
        print(f"Error validating persistent thread config: {e}")
        return False


def get_config_summary(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of the persistent thread configuration.

    Args:
        config: Configuration to summarize

    Returns:
        dict: Summary of configuration
    """
    try:
        total_threads = sum(thread_config['size']
                            for thread_config in config.values())
        total_max_wait = sum(thread_config['max_wait_time']
                             for thread_config in config.values())

        return {
            'total_threads': total_threads,
            'thread_types': len(config),
            'total_max_wait_time': total_max_wait,
            'thread_details': {
                thread_type: {
                    'size': thread_config['size'],
                    'description': thread_config.get('description', 'No description')
                }
                for thread_type, thread_config in config.items()
            }
        }

    except Exception as e:
        print(f"Error generating config summary: {e}")
        return {}


# Example usage and testing
if __name__ == "__main__":
    # Test different configurations
    configs = ['default', 'high_performance', 'low_resource', 'development']

    for config_type in configs:
        config = get_persistent_thread_config(config_type)
        print(f"\n=== {config_type.upper()} CONFIGURATION ===")

        if validate_persistent_thread_config(config):
            summary = get_config_summary(config)
            print(f"Total threads: {summary['total_threads']}")
            print(f"Thread types: {summary['thread_types']}")
            print("Thread details:")
            for thread_type, details in summary['thread_details'].items():
                print(
                    f"  {thread_type}: {details['size']} threads - {details['description']}")
        else:
            print("Configuration validation failed!")

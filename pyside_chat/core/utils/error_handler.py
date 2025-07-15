# Shared imports


"""
Error Handler Module

Provides comprehensive error handling utilities including decorators,
context managers, and helper functions for consistent error handling
across the application.
"""

import functools
import traceback
from typing import Callable, Any, Optional, Dict, Type, Union
from contextlib import contextmanager
from pyside_chat.utils.Logging.logging_helpers import LoggingHelpers
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ErrorHandler:
    """Centralized error handling utilities"""

    @staticmethod
    def safe_execute(func: Callable, *args, default_return: Any = None,
                     error_msg: str = "Operation failed", **kwargs) -> Any:
        """
        Safely execute a function with comprehensive error handling

        Args:
            func: Function to execute
            *args: Function arguments
            default_return: Value to return on error
            error_msg: Custom error message
            **kwargs: Function keyword arguments

        Returns:
            Function result or default_return on error
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            LoggingHelpers.log_exception_with_context(
                error_msg, e,
                {"function": func.__name__, "args": args, "kwargs": kwargs}
            )
            return default_return

    @staticmethod
    def retry_on_failure(func: Callable, max_attempts: int = 3,
                         delay_seconds: float = 1.0,
                         exceptions: tuple = (Exception,)) -> Callable:
        """
        Decorator to retry a function on failure

        Args:
            func: Function to retry
            max_attempts: Maximum number of retry attempts
            delay_seconds: Delay between retries
            exceptions: Tuple of exceptions to catch

        Returns:
            Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    LoggingHelpers.log_warning_with_context(
                        f"Attempt {attempt + 1} failed",
                        {"function": func.__name__,
                            "attempt": attempt + 1, "error": str(e)}
                    )

                    if attempt < max_attempts - 1:
                        time.sleep(delay_seconds)

            # All attempts failed
            LoggingHelpers.log_exception_with_context(
                f"All {max_attempts} attempts failed", last_exception,
                {"function": func.__name__, "max_attempts": max_attempts}
            )
            raise last_exception

        return wrapper

    @staticmethod
    def handle_network_errors(func: Callable) -> Callable:
        """
        Decorator to handle network-related errors specifically

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                LoggingHelpers.log_network_request(
                    "unknown", "unknown", error=e
                )
                raise
            except TimeoutError as e:
                LoggingHelpers.log_network_request(
                    "unknown", "unknown", error=e
                )
                raise
            except Exception as e:
                LoggingHelpers.log_exception_with_context(
                    "network_operation", e,
                    {"function": func.__name__, "args": args, "kwargs": kwargs}
                )
                raise

        return wrapper

    @staticmethod
    def handle_file_operations(func: Callable) -> Callable:
        """
        Decorator to handle file operation errors

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                LoggingHelpers.log_file_operation(
                    "unknown", "unknown", False, e
                )
                raise
            except PermissionError as e:
                LoggingHelpers.log_file_operation(
                    "unknown", "unknown", False, e
                )
                raise
            except Exception as e:
                LoggingHelpers.log_exception_with_context(
                    "file_operation", e,
                    {"function": func.__name__, "args": args, "kwargs": kwargs}
                )
                raise

        return wrapper

    @staticmethod
    def handle_audio_operations(func: Callable) -> Callable:
        """
        Decorator to handle audio operation errors

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                LoggingHelpers.log_audio_operation(
                    func.__name__, False, e
                )
                raise

        return wrapper

    @staticmethod
    def handle_memory_operations(func: Callable) -> Callable:
        """
        Decorator to handle memory operation errors

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                LoggingHelpers.log_memory_operation(
                    func.__name__, "unknown", False, e
                )
                raise

        return wrapper

    @staticmethod
    def handle_ui_operations(func: Callable) -> Callable:
        """
        Decorator to handle UI operation errors

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                LoggingHelpers.log_ui_operation(
                    "unknown", func.__name__, False, e
                )
                raise

        return wrapper


@contextmanager
def error_context(operation: str, context: Optional[Dict[str, Any]] = None):
    """
    Context manager for error handling with automatic logging

    Args:
        operation: Name of the operation being performed
        context: Additional context information
    """
    context = context or {}
    start_time = time.time()

    try:
        yield
        duration = (time.time() - start_time) * 1000
        LoggingHelpers.log_performance_metric(
            operation, duration, str(context))
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        LoggingHelpers.log_exception_with_context(operation, e, context)
        LoggingHelpers.log_performance_metric(
            f"{operation}_failed", duration, str(context))
        raise


@contextmanager
def network_error_context(url: str, method: str):
    """
    Context manager for network operations with error handling

    Args:
        url: URL being accessed
        method: HTTP method being used
    """
    try:
        LoggingHelpers.log_network_request(url, method)
        yield
    except Exception as e:
        LoggingHelpers.log_network_request(url, method, error=e)
        raise


@contextmanager
def file_operation_context(operation: str, filepath: str):
    """
    Context manager for file operations with error handling

    Args:
        operation: File operation being performed
        filepath: Path to the file
    """
    try:
        yield
        LoggingHelpers.log_file_operation(operation, filepath, True)
    except Exception as e:
        LoggingHelpers.log_file_operation(operation, filepath, False, e)
        raise


@contextmanager
def audio_operation_context(operation: str):
    """
    Context manager for audio operations with error handling

    Args:
        operation: Audio operation being performed
    """
    try:
        yield
        LoggingHelpers.log_audio_operation(operation, True)
    except Exception as e:
        LoggingHelpers.log_audio_operation(operation, False, e)
        raise


@contextmanager
def memory_operation_context(operation: str, memory_type: str):
    """
    Context manager for memory operations with error handling

    Args:
        operation: Memory operation being performed
        memory_type: Type of memory being operated on
    """
    try:
        yield
        LoggingHelpers.log_memory_operation(operation, memory_type, True)
    except Exception as e:
        LoggingHelpers.log_memory_operation(operation, memory_type, False, e)
        raise


@contextmanager
def ui_operation_context(component: str, operation: str):
    """
    Context manager for UI operations with error handling

    Args:
        component: UI component being operated on
        operation: UI operation being performed
    """
    try:
        yield
        LoggingHelpers.log_ui_operation(component, operation, True)
    except Exception as e:
        LoggingHelpers.log_ui_operation(component, operation, False, e)
        raise


def safe_json_parse(json_str: str, default: Any = None) -> Any:
    """
    Safely parse JSON string with error handling

    Args:
        json_str: JSON string to parse
        default: Default value to return on error

    Returns:
        Parsed JSON object or default value
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        LoggingHelpers.log_json_parsing_error(e, json_str)
        return default
    except Exception as e:
        LoggingHelpers.log_exception_with_context(
            "json_parse", e, {"json_str": json_str})
        return default


def safe_file_read(filepath: str, encoding: str = 'utf-8', default: Any = None) -> Any:
    """
    Safely read a file with error handling

    Args:
        filepath: Path to the file
        encoding: File encoding
        default: Default value to return on error

    Returns:
        File contents or default value
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        LoggingHelpers.log_file_operation("read", filepath, False, e)
        return default


def safe_file_write(filepath: str, content: str, encoding: str = 'utf-8') -> bool:
    """
    Safely write to a file with error handling

    Args:
        filepath: Path to the file
        content: Content to write
        encoding: File encoding

    Returns:
        True if successful, False otherwise
    """
    try:
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        LoggingHelpers.log_file_operation("write", filepath, True)
        return True
    except Exception as e:
        LoggingHelpers.log_file_operation("write", filepath, False, e)
        return False


def safe_network_request(url: str, method: str = "GET", **kwargs) -> Optional[Any]:
    """
    Safely make a network request with error handling

    Args:
        url: URL to request
        method: HTTP method
        **kwargs: Additional request parameters

    Returns:
        Response object or None on error
    """
    try:
        import requests
        response = requests.request(method, url, **kwargs)
        LoggingHelpers.log_network_request(url, method, response.status_code)
        return response
    except Exception as e:
        LoggingHelpers.log_network_request(url, method, error=e)
        return None


def validate_input(data: Any, expected_type: Type, field_name: str = "input") -> bool:
    """
    Validate input data with error handling

    Args:
        data: Data to validate
        expected_type: Expected type
        field_name: Name of the field for error messages

    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(data, expected_type):
            LoggingHelpers.log_warning_with_context(
                f"Invalid {field_name} type",
                {"expected": expected_type,
                    "actual": type(data), "value": data}
            )
            return False
        return True
    except Exception as e:
        LoggingHelpers.log_exception_with_context(
            "input_validation", e, {"field_name": field_name})
        return False


def cleanup_resources(resources: list) -> None:
    """
    Safely cleanup a list of resources

    Args:
        resources: List of resources to cleanup
    """
    for resource in resources:
        try:
            if hasattr(resource, 'close'):
                resource.close()
            elif hasattr(resource, 'cleanup'):
                resource.cleanup()
            elif hasattr(resource, '__del__'):
                del resource
        except Exception as e:
            LoggingHelpers.log_exception_with_context(
                "resource_cleanup", e, {"resource": str(resource)})


def handle_critical_error(error: Exception, component: str, recovery_action: str) -> None:
    """
    Handle critical errors that may require application restart

    Args:
        error: The critical error
        component: Component where the error occurred
        recovery_action: Action to take for recovery
    """
    LoggingHelpers.log_critical_error(component, error, recovery_action)

    # Additional critical error handling could go here
    # For example, saving state, notifying user, etc.

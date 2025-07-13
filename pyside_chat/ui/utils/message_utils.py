"""
Message Box Utilities - Replace QMessageBox with copy-enabled dialogs
"""

import traceback
from typing import Optional
from PySide6.QtWidgets import QMessageBox

from pyside_chat.ui.dialogs.error_dialog import show_error_dialog, ErrorDialog
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

def show_error(title: str, message: str, details: str = "", traceback_str: str = "", parent=None):
    """Show an error dialog with copy functionality"""
    return show_error_dialog(title, message, details, traceback_str, parent)

def show_warning(title: str, message: str, details: str = "", parent=None):
    """Show a warning dialog with copy functionality"""
    # For warnings, we'll use a simple dialog without detailed traceback
    dialog = ErrorDialog(title, message, details, parent)
    dialog.setIcon(QMessageBox.Icon.Warning)
    dialog.exec()
    return dialog

def show_critical_error(title: str, message: str, exception: Optional[Exception] = None, parent=None):
    """Show a critical error dialog with copy functionality and exception details"""
    details = ""
    traceback_str = ""
    
    if exception:
        details = str(exception)
        traceback_str = traceback.format_exc()
    
    return show_error_dialog(title, message, details, traceback_str, parent)

def show_operation_error(operation: str, error: Exception, parent=None):
    """Show an operation error with copy functionality"""
    return show_critical_error(
        title=f"{operation} Error",
        message=f"Failed to {operation.lower()}",
        exception=error,
        parent=parent
    )

def show_connection_error(service: str, error: Exception, parent=None):
    """Show a connection error with copy functionality"""
    return show_critical_error(
        title=f"{service} Connection Error",
        message=f"Failed to connect to {service}",
        exception=error,
        parent=parent
    )

def show_file_error(operation: str, file_path: str, error: Exception, parent=None):
    """Show a file operation error with copy functionality"""
    details = f"File: {file_path}\nError: {str(error)}"
    return show_error_dialog(
        title=f"File {operation} Error",
        message=f"Failed to {operation.lower()} file",
        details=details,
        traceback=traceback.format_exc(),
        parent=parent
    )

def show_validation_error(field: str, message: str, parent=None):
    """Show a validation error with copy functionality"""
    return show_error_dialog(
        title="Validation Error",
        message=f"Invalid {field}",
        details=message,
        parent=parent
    ) 
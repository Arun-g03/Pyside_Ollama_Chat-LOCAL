from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
"""
Threading utilities for safe signal connections and UI updates.
"""

import threading
from typing import Any, Callable, Optional

logger = CustomLogger.get_logger(__name__)


def is_main_thread() -> bool:
    """Check if current thread is the main (GUI) thread."""
    return QThread.currentThread() == QApplication.instance().thread()


def safe_ui_update(target: QObject, method: str, *args, **kwargs):
    """
    Safely update UI from any thread.

    Args:
        target: The QObject to call the method on
        method: The method name to call
        *args: Arguments to pass to the method
        **kwargs: Keyword arguments to pass to the method
    """
    try:
        if is_main_thread():
            # We're already in the main thread, call directly
            getattr(target, method)(*args, **kwargs)
        else:
            # We're in a worker thread, use QueuedConnection
            QMetaObject.invokeMethod(
                target,
                method,
                Qt.ConnectionType.QueuedConnection,
                *[Q_ARG(type(arg), arg) for arg in args]
            )
    except Exception as e:
        logger.error(f"Error in safe_ui_update: {e}")


def safe_ui_update_with_callback(target: QObject, method: str, callback: Optional[Callable] = None, *args, **kwargs):
    """
    Safely update UI from any thread with optional callback.

    Args:
        target: The QObject to call the method on
        method: The method name to call
        callback: Optional callback to execute after UI update
        *args: Arguments to pass to the method
        **kwargs: Keyword arguments to pass to the method
    """
    try:
        if is_main_thread():
            # We're already in the main thread, call directly
            result = getattr(target, method)(*args, **kwargs)
            if callback:
                callback()
            return result
        else:
            # We're in a worker thread, schedule for main thread
            def ui_update_with_callback():
                try:
                    result = getattr(target, method)(*args, **kwargs)
                    if callback:
                        callback()
                    return result
                except Exception as e:
                    logger.error(f"Error in UI update callback: {e}")

            QTimer.singleShot(0, ui_update_with_callback)
    except Exception as e:
        logger.error(f"Error in safe_ui_update_with_callback: {e}")


def safe_button_update(button: QObject, enabled: bool = None, visible: bool = None, text: str = None):
    """
    Safely update button properties from any thread.

    Args:
        button: The button to update
        enabled: Optional enabled state
        visible: Optional visible state  
        text: Optional text to set
    """
    try:
        if is_main_thread():
            # Direct update in main thread
            if enabled is not None:
                button.setEnabled(enabled)
            if visible is not None:
                button.setVisible(visible)
            if text is not None:
                button.setText(text)
            button.update()
        else:
            # Schedule update for main thread
            def update_button():
                try:
                    if enabled is not None:
                        button.setEnabled(enabled)
                    if visible is not None:
                        button.setVisible(visible)
                    if text is not None:
                        button.setText(text)
                    button.update()
                except Exception as e:
                    logger.error(f"Error updating button: {e}")

            QTimer.singleShot(0, update_button)
    except Exception as e:
        logger.error(f"Error in safe_button_update: {e}")


def safe_widget_update(widget: QObject, method: str, *args, **kwargs):
    """
    Safely update any widget from any thread.

    Args:
        widget: The widget to update
        method: The method name to call
        *args: Arguments to pass to the method
        **kwargs: Keyword arguments to pass to the method
    """
    try:
        if is_main_thread():
            # Direct update in main thread
            getattr(widget, method)(*args, **kwargs)
        else:
            # Schedule update for main thread
            def update_widget():
                try:
                    getattr(widget, method)(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error updating widget: {e}")

            QTimer.singleShot(0, update_widget)
    except Exception as e:
        logger.error(f"Error in safe_widget_update: {e}")


def safe_process_events_alternative():
    """
    Alternative to processEvents() that's safer for background threads.
    This schedules a small delay to allow the event loop to process pending events.
    """
    try:
        if is_main_thread():
            # In main thread, use a minimal timer to process events
            QTimer.singleShot(1, lambda: None)
        else:
            # In background thread, schedule a callback in main thread
            QTimer.singleShot(1, lambda: None)
    except Exception as e:
        logger.error(f"Error in safe_process_events_alternative: {e}")


def safe_force_update(widget: QObject):
    """
    Safely force a widget update without using processEvents.

    Args:
        widget: The widget to update
    """
    try:
        if is_main_thread():
            # Direct update in main thread
            widget.update()
            widget.repaint()
        else:
            # Schedule update for main thread
            def force_update():
                try:
                    widget.update()
                    widget.repaint()
                except Exception as e:
                    logger.error(f"Error forcing widget update: {e}")

            QTimer.singleShot(0, force_update)
    except Exception as e:
        logger.error(f"Error in safe_force_update: {e}")


def safe_connect_signal(signal, slot, connection_type=Qt.ConnectionType.QueuedConnection):
    """
    Safely connect a signal to a slot with proper connection type.

    Args:
        signal: The signal to connect
        slot: The slot to connect to
        connection_type: The connection type (default: QueuedConnection for thread safety)
    """
    try:
        signal.connect(slot, connection_type)
    except Exception as e:
        logger.error(f"Error connecting signal: {e}")


def safe_signal_connect(signal, slot, connection_type=Qt.ConnectionType.QueuedConnection):
    """
    Alias for safe_connect_signal for backward compatibility.

    Args:
        signal: The signal to connect
        slot: The slot to connect to
        connection_type: The connection type (default: QueuedConnection for thread safety)
    """
    return safe_connect_signal(signal, slot, connection_type)


def safe_signal_disconnect(signal, slot=None):
    """
    Alias for safe_disconnect for backward compatibility.

    Args:
        signal: The signal to disconnect
        slot: The slot to disconnect from (optional)
    """
    return safe_disconnect(signal, slot)


def safe_disconnect_signal(signal, slot):
    """
    Safely disconnect a signal from a slot.

    Args:
        signal: The signal to disconnect
        slot: The slot to disconnect from
    """
    try:
        signal.disconnect(slot)
    except Exception as e:
        logger.error(f"Error disconnecting signal: {e}")


def create_thread_safe_callback(callback: Callable, *args, **kwargs):
    """
    Create a thread-safe callback that ensures execution in the main thread.

    Args:
        callback: The callback function to execute
        *args: Arguments to pass to the callback
        **kwargs: Keyword arguments to pass to the callback

    Returns:
        A thread-safe callback function
    """
    def thread_safe_callback():
        try:
            if is_main_thread():
                callback(*args, **kwargs)
            else:
                QTimer.singleShot(0, lambda: callback(*args, **kwargs))
        except Exception as e:
            logger.error(f"Error in thread-safe callback: {e}")

    return thread_safe_callback


class ThreadSafeCallback:
    """
    A thread-safe callback wrapper that ensures callbacks are executed in the main thread.
    """

    def __init__(self, callback: Callable, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        """Execute the callback in a thread-safe manner."""
        try:
            if is_main_thread():
                self.callback(*self.args, **self.kwargs)
            else:
                QTimer.singleShot(0, lambda: self.callback(
                    *self.args, **self.kwargs))
        except Exception as e:
            logger.error(f"Error in ThreadSafeCallback: {e}")


def ensure_main_thread(func: Callable) -> Callable:
    """
    Decorator to ensure a function runs in the main thread.

    Args:
        func: The function to wrap

    Returns:
        A thread-safe version of the function
    """
    def wrapper(*args, **kwargs):
        if is_main_thread():
            return func(*args, **kwargs)
        else:
            # Schedule for main thread
            QTimer.singleShot(0, lambda: func(*args, **kwargs))

    return wrapper


def log_thread_info(operation: str, logger_instance=None):
    """
    Log thread information for debugging.

    Args:
        operation: Description of the operation being performed
        logger_instance: Optional logger instance to use
    """
    try:
        current_thread = QThread.currentThread()
        if current_thread is None:
            thread_name = "Unknown"
        else:
            thread_name = current_thread.objectName() or "Unknown"
        is_main = is_main_thread()

        log_func = logger_instance or logger
        log_func.debug(
            f"[THREAD] {operation} - Thread: {thread_name}, Main: {is_main}")
    except Exception as e:
        (logger_instance or logger).error(f"Error logging thread info: {e}")


def safe_log_thread_info(operation: str):
    """
    Safely log thread information for debugging.

    Args:
        operation: Description of the operation being performed
    """
    try:
        current_thread = QThread.currentThread()
        main_thread = QApplication.instance().thread() if QApplication.instance() else None

        logger.debug(f"Thread info for {operation}:")
        if current_thread is None:
            logger.debug("  Current thread: None")
        else:
            logger.debug(
                f"  Current thread: {current_thread.objectName() or 'unnamed'}")
        if main_thread is None:
            logger.debug("  Main thread: None")
        else:
            logger.debug(
                f"  Main thread: {main_thread.objectName() or 'unnamed'}")
        logger.debug(f"  Is main thread: {is_main_thread()}")
    except Exception as e:
        logger.error(f"Error logging thread info: {e}")


def safe_disconnect(signal, slot=None):
    """
    Safely disconnect a signal from a slot.

    Args:
        signal: The signal to disconnect
        slot: The slot to disconnect from (optional)
    """
    try:
        if slot:
            signal.disconnect(slot)
        else:
            signal.disconnect()
    except Exception as e:
        logger.error(f"Error disconnecting signal: {e}")


def safe_emit_signal(signal, *args):
    """
    Safely emit a signal from any thread.

    Args:
        signal: The signal to emit
        *args: Arguments to pass to the signal
    """
    try:
        if is_main_thread():
            # Direct emission in main thread
            signal.emit(*args)
        else:
            # Schedule emission for main thread
            QTimer.singleShot(0, lambda: signal.emit(*args))
    except Exception as e:
        logger.error(f"Error emitting signal: {e}")


def safe_set_property(widget: QObject, property_name: str, value: Any):
    """
    Safely set a widget property from any thread.

    Args:
        widget: The widget to update
        property_name: The property name to set
        value: The value to set
    """
    try:
        if is_main_thread():
            # Direct property set in main thread
            widget.setProperty(property_name, value)
        else:
            # Schedule property set for main thread
            def set_property():
                try:
                    widget.setProperty(property_name, value)
                except Exception as e:
                    logger.error(
                        f"Error setting property {property_name}: {e}")

            QTimer.singleShot(0, set_property)
    except Exception as e:
        logger.error(f"Error in safe_set_property: {e}")


def safe_call_method(widget: QObject, method_name: str, *args, **kwargs):
    """
    Safely call a widget method from any thread.

    Args:
        widget: The widget to call the method on
        method_name: The method name to call
        *args: Arguments to pass to the method
        **kwargs: Keyword arguments to pass to the method
    """
    try:
        if is_main_thread():
            # Direct method call in main thread
            method = getattr(widget, method_name)
            return method(*args, **kwargs)
        else:
            # Schedule method call for main thread
            def call_method():
                try:
                    method = getattr(widget, method_name)
                    return method(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error calling method {method_name}: {e}")

            QTimer.singleShot(0, call_method)
    except Exception as e:
        logger.error(f"Error in safe_call_method: {e}")


def safe_show_widget(widget: QObject):
    """
    Safely show a widget from any thread.

    Args:
        widget: The widget to show
    """
    safe_widget_update(widget, "show")


def safe_hide_widget(widget: QObject):
    """
    Safely hide a widget from any thread.

    Args:
        widget: The widget to hide
    """
    safe_widget_update(widget, "hide")


def safe_enable_widget(widget: QObject, enabled: bool = True):
    """
    Safely enable/disable a widget from any thread.

    Args:
        widget: The widget to enable/disable
        enabled: Whether to enable the widget
    """
    safe_widget_update(widget, "setEnabled", enabled)


def safe_set_text(widget: QObject, text: str):
    """
    Safely set text on a widget from any thread.

    Args:
        widget: The widget to update
        text: The text to set
    """
    safe_widget_update(widget, "setText", text)


def safe_set_style(widget: QObject, style: str):
    """
    Safely set style sheet on a widget from any thread.

    Args:
        widget: The widget to update
        style: The style sheet to set
    """
    safe_widget_update(widget, "setStyleSheet", style)

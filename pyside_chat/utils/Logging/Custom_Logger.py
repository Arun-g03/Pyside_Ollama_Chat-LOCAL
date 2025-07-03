import logging
import os
import re

LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s"
LOG_LEVEL = logging.DEBUG

# Ensure the Logs directory exists at the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
LOGS_DIR = os.path.join(PROJECT_ROOT, "Logs")
os.makedirs(LOGS_DIR, exist_ok=True)
CENTRAL_LOG_FILE = os.path.join(LOGS_DIR, "pychat.log")

_warned_about_default = False

def _sanitize_filename(name):
    return "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)

def strip_emojis(text):
    # Remove all emoji characters from the text
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002700-\U000027BF"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

class PrintOnLogMixin:
    def _print(self, msg):
        print(strip_emojis(msg))
    def info(self, msg, *args, print_to_terminal=False, **kwargs):
        clean_msg = strip_emojis(msg % args if args else msg)
        super().info(clean_msg, **kwargs)
        if print_to_terminal:
            self._print(clean_msg)
    def debug(self, msg, *args, print_to_terminal=False, **kwargs):
        clean_msg = strip_emojis(msg % args if args else msg)
        super().debug(clean_msg, **kwargs)
        if print_to_terminal:
            self._print(clean_msg)
    def warning(self, msg, *args, print_to_terminal=False, **kwargs):
        clean_msg = strip_emojis(msg % args if args else msg)
        super().warning(clean_msg, **kwargs)
        if print_to_terminal:
            self._print(clean_msg)
    def error(self, msg, *args, print_to_terminal=False, **kwargs):
        clean_msg = strip_emojis(msg % args if args else msg)
        super().error(clean_msg, **kwargs)
        if print_to_terminal:
            self._print(clean_msg)
    def critical(self, msg, *args, print_to_terminal=False, **kwargs):
        clean_msg = strip_emojis(msg % args if args else msg)
        super().critical(clean_msg, **kwargs)
        if print_to_terminal:
            self._print(clean_msg)

class CustomLogger(logging.Logger):
    """
    Custom Logging class for the PyChat project.
    
    This class provides enhanced logging functionality with file output and
    optional terminal printing. For complete setup and usage instructions,
    refer to: DOCUMENTATION/Logging Commands.md
    
    Args:
        name (str): The name of the logger.
        level (int): The level of the logger.
    """
    _instance = None
    _loggers = {}
    _cleared_files = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def _clear_log_file(cls, filepath):
        if filepath not in cls._cleared_files and os.path.exists(filepath):
            with open(filepath, 'w'):
                pass  # Truncate the file
            cls._cleared_files.add(filepath)

    @classmethod
    def get_logger(cls, name: str = None):
        global _warned_about_default
        if not name:
            name = "PyChat"
            if not _warned_about_default:
                print("[CustomLogger WARNING] No logger name specified. Using default 'PyChat' logger. Specify a module name for module-specific logging.")
                _warned_about_default = True
        if name in cls._loggers:
            return cls._loggers[name]
        logger = logging.getLogger(name)
        if not logger.handlers:
            formatter = logging.Formatter(LOG_FORMAT)
            # No StreamHandler by default
            # If using the default name, log to pychat.log; otherwise, log to module-specific file only
            if name == "PyChat":
                cls._clear_log_file(CENTRAL_LOG_FILE)
                file_handler = logging.FileHandler(CENTRAL_LOG_FILE)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            else:
                module_log_file = os.path.join(LOGS_DIR, f"{_sanitize_filename(name)}.log")
                cls._clear_log_file(module_log_file)
                file_handler = logging.FileHandler(module_log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            logger.setLevel(LOG_LEVEL)
            logger.propagate = False
        # Wrap logger with print-on-log mixin for per-message print_to_terminal support
        class PrintLogger(PrintOnLogMixin, type(logger)):
            pass
        logger.__class__ = PrintLogger
        cls._loggers[name] = logger
        return logger

    def info(self, msg, *args, **kwargs):
        clean_msg = self._filter_non_ascii(str(msg))
        super().info(clean_msg, *args, **kwargs)
    def debug(self, msg, *args, **kwargs):
        clean_msg = self._filter_non_ascii(str(msg))
        super().debug(clean_msg, *args, **kwargs)
    def warning(self, msg, *args, **kwargs):
        clean_msg = self._filter_non_ascii(str(msg))
        super().warning(clean_msg, *args, **kwargs)
    def error(self, msg, *args, **kwargs):
        clean_msg = self._filter_non_ascii(str(msg))
        super().error(clean_msg, *args, **kwargs)
    def _filter_non_ascii(self, s):
        return re.sub(r'[^\x00-\x7F]+', '', s)

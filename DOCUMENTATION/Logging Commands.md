# Logging Setup Instructions

To use the custom logger in any file, follow these steps:

1. **Import the logger:**

    ```python
    from SRC.utils.Logging.Custom_Logger import CustomLogger
    ```

2. **Create a logger instance (usually at the top of your file):**

    **Using the module name (recommended):**
    ```python
    logger = CustomLogger.get_logger(__name__)
    ```

    **Using a custom name:**
    ```python
    logger = CustomLogger.get_logger("A Custom name")
    ```

3. **Use the logger in your code:**

    ```python
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    ```

4. **To also print a log message to the terminal, use the `print_to_terminal` keyword:**

    By default, writing logs to the terminal is disabled to avoid clutter. Remember to add the parameter at the end if needed.

    **This will write the logs to the terminal:**
    ```python
    logger.info("This will go to the log file and terminal", print_to_terminal=True)
    logger.debug("Debug message", print_to_terminal=True)
    ```

    **This will NOT write to the terminal:**
    ```python
    logger.info("This will go to the log file ONLY", print_to_terminal=False)
    logger.debug("Debug message")
    ```

---

- All logs will be written to `/Logs/<module_name>.log` (where `<module_name>` is the name you pass to `get_logger`).
- If you pass no name, the default logger name (`PyChat`), logs will go to `/Logs/pychat.log`.
- The `/Logs` directory is created automatically if it does not exist.
- Emojis are automatically stripped from all log messages for compatibility.

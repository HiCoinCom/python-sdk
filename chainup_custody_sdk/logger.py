"""
ChainUp Custody SDK Logging

Provides a unified logging system for the SDK.
Uses Python's built-in logging module with customizable configuration.
"""
import logging
import sys
from typing import Optional


# SDK logger name
SDK_LOGGER_NAME = "chainup_custody"

# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEBUG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - "
    "[%(filename)s:%(lineno)d] - %(message)s"
)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for the SDK.
    
    Args:
        name: Logger name suffix (appended to SDK_LOGGER_NAME)
    
    Returns:
        Logger instance
    
    Example:
        logger = get_logger("waas")  # Returns logger named "chainup_custody.waas"
    """
    if name:
        return logging.getLogger(f"{SDK_LOGGER_NAME}.{name}")
    return logging.getLogger(SDK_LOGGER_NAME)


def configure_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
    debug: bool = False
) -> None:
    """
    Configure SDK logging.
    
    Args:
        level: Logging level (default: INFO)
        format_string: Custom log format string
        handler: Custom log handler
        debug: Enable debug mode with detailed format
    
    Example:
        # Enable debug logging
        configure_logging(level=logging.DEBUG, debug=True)
        
        # Use custom handler
        file_handler = logging.FileHandler("sdk.log")
        configure_logging(handler=file_handler)
    """
    logger = logging.getLogger(SDK_LOGGER_NAME)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create handler
    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
    
    # Set format
    if format_string is None:
        format_string = DEBUG_FORMAT if debug else DEFAULT_FORMAT
    
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    
    logger.addHandler(handler)


def enable_debug_logging() -> None:
    """
    Enable debug logging with detailed output.
    
    Shortcut for configure_logging(level=logging.DEBUG, debug=True)
    """
    configure_logging(level=logging.DEBUG, debug=True)


def disable_logging() -> None:
    """
    Disable SDK logging.
    
    Sets log level to CRITICAL+1 to suppress all logs.
    """
    logger = logging.getLogger(SDK_LOGGER_NAME)
    logger.setLevel(logging.CRITICAL + 1)


class LoggerMixin:
    """
    Mixin class that provides logging functionality.
    
    Classes that inherit from this mixin get a `_logger` property
    that returns a properly named logger.
    
    Example:
        class MyApi(LoggerMixin):
            def do_something(self):
                self._logger.info("Doing something")
    """
    
    @property
    def _logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


# Null handler for library use (prevents "No handler found" warnings)
logging.getLogger(SDK_LOGGER_NAME).addHandler(logging.NullHandler())

"""Logging Utility for Dragonsweepyr"""

import logging


def setup_logger(
    name: str = "dragonsweepyr",
    level: int = logging.DEBUG,
    log_format: str = "%(asctime)s | %(levelname)-7s | %(lineno)-4d | %(message)s",
) -> logging.Logger:
    """
    Set up a logger with the specified name and level.

    Args:
        name: Name of the logger.
        level: Logging level (e.g., logging.DEBUG, logging.INFO).
        log_format: Format string for log messages.

    Returns:
        Configured logger instance.
    """
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(level)

    # Remove existing handlers to avoid duplicates
    for handler in logger_instance.handlers[:]:
        logger_instance.removeHandler(handler)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger_instance.addHandler(ch)

    return logger_instance

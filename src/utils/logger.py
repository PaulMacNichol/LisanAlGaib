# src/utils/logger.py

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger with a consistent format and StreamHandler.

    Args:
        name (str): The name of the logger, typically __name__.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set base level (adjust as needed)

    # Only add handlers if there are none already attached to avoid duplicates.
    if not logger.handlers:
        # Create a console handler that outputs to stdout.
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

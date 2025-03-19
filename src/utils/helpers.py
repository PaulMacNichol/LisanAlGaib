# src/utils/helpers.py

import re
from urllib.parse import urlparse


def format_time(seconds: int) -> str:
    """
    Converts a time in seconds to a human-readable string in HH:MM:SS or MM:SS format.

    Args:
        seconds (int): The number of seconds.

    Returns:
        str: The formatted time string.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def is_valid_url(url: str) -> bool:
    """
    Checks whether a given string is a valid URL.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)


def sanitize_text(text: str) -> str:
    """
    Sanitizes input text by removing control characters and trimming whitespace.

    Args:
        text (str): The input text.

    Returns:
        str: The sanitized text.
    """
    # Remove any control characters (non-printable) and trim the text.
    sanitized = re.sub(r'[\x00-\x1F\x7F]', '', text).strip()
    return sanitized

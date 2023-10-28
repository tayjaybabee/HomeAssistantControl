from urllib.parse import urlparse
from typing import List


def format_time(hours: int, minutes: int, seconds: int) -> str:
    """Format time as a human-readable string."""
    time_strings = []
    if hours:
        time_strings.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        time_strings.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds or not time_strings:
        time_strings.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return f"The cache was last refreshed {', '.join(time_strings)} ago."


def get_headers(token):
    return {
            'Authorization': f'Bearer {token}',
            'content-type':  'application/json',
            }


def is_valid_url(url: str) -> bool:
    """
    Validate if the given string is a valid URL.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Usage Examples:
        >>> is_valid_url('https://www.example.com')
        True

        >>> is_valid_url('invalid.url')
        False
    """

    try:
        result = urlparse(url)
        # Ensure scheme (http, https) and network location are present
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def validate_and_transform_url(url: str) -> str:
    """
    Validate and transform the given URL.

    Args:
        url (str): The URL to validate and transform.

    Returns:
        str: The validated and transformed URL.
    """
    if not isinstance(url, str):
        raise TypeError('"url" must be a string!')

    if not url.startswith('http://'):
        url = f'http://{url}'

    # Assuming is_valid_url is defined elsewhere or is imported
    if not is_valid_url(url):
        raise ValueError('"url" must be a valid URL!')

    return url

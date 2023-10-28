from home_assistant_control.utils import get_headers
from requests import get, RequestException

BASE_ENDPOINT = '/api/'


def make_request(url: str, token: str):
    """Make an HTTP request and handle potential errors.

    Args:
        url (str): The URL to send the request to.
        token (str): The authorization token.

    Returns:
        Response: The HTTP response.

    Raises:
        RequestException: If there's a network-related error.
    """
    headers = get_headers(token)
    res = get(url, headers=headers)
    res.raise_for_status()  # This will raise HTTPError for bad responses (4xx and 5xx)
    return res


def validate_token(url, token) -> bool:
    """Validate the token by making a request to the base API endpoint.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        res = make_request(f'{url}{BASE_ENDPOINT}', token)
        return res.status_code == 200
    except RequestException:
        return False


def validate_and_return_token(url, token):
    if not validate_token(url, token):
        raise ValueError('Invalid token!')
    return token

class APIError(Exception):
    """
    A generic error for API issues.

    Attributes:
        message (str): A descriptive error message.

    Usage example:
        >>> raise APIError("An unknown API error occurred.")
        Traceback (most recent call last):
        ...
        APIError: An unknown API error occurred.
    """

    def __init__(self, message: str):
        super().__init__(message)


class AuthenticationError(APIError):
    """
    A generic error for authentication issues.

    Usage example:
        >>> raise AuthenticationError("Authentication failed.")
        Traceback (most recent call last):
        ...
        AuthenticationError: Authentication failed.
    """
    pass


class InvalidTokenError(AuthenticationError):
    """
    An error raised when an invalid token is provided.

    Attributes:
        token (str): The invalid token that caused the error.

    Usage example:
        >>> raise InvalidTokenError("The token provided is invalid.", "InvalidToken")
        Traceback (most recent call last):
        ...
        InvalidTokenError: The token provided is invalid.
    """

    def __init__(self, message: str, token: str):
        super().__init__(message)
        self.token = token

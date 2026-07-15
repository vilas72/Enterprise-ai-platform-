"""
Enterprise Confluence exceptions.
"""

from __future__ import annotations


class ConfluenceError(Exception):
    """
    Base Confluence exception.
    """


class ConfluenceAuthenticationError(ConfluenceError):
    """
    Authentication failed.
    """


class ConfluenceAuthorizationError(ConfluenceError):
    """
    Authorization failed.
    """


class ConfluenceNotFoundError(ConfluenceError):
    """
    Resource not found.
    """


class ConfluenceConflictError(ConfluenceError):
    """
    Resource conflict.
    """


class ConfluenceValidationError(ConfluenceError):
    """
    Validation failed.
    """


class ConfluenceRateLimitError(ConfluenceError):
    """
    API rate limit exceeded.
    """


class ConfluenceServerError(ConfluenceError):
    """
    Atlassian server error.
    """


class ConfluenceRequestError(ConfluenceError):
    """
    Generic request failure.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
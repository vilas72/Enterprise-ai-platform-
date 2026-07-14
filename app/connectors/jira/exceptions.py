from __future__ import annotations


class JiraError(Exception):
    """
    Base exception for all Jira connector errors.
    """


class JiraAuthenticationError(JiraError):
    """
    Authentication with Jira failed.
    """


class JiraAuthorizationError(JiraError):
    """
    Authorization to access the Jira resource was denied.
    """


class JiraNotFoundError(JiraError):
    """
    Requested Jira resource was not found.
    """


class JiraConflictError(JiraError):
    """
    The requested operation conflicts with the current state
    of the Jira resource.
    """


class JiraValidationError(JiraError):
    """
    Jira rejected the request because of validation errors.
    """


class JiraRateLimitError(JiraError):
    """
    Jira Cloud rate limit exceeded.
    """


class JiraServerError(JiraError):
    """
    Jira returned an internal server error.
    """


class JiraRequestError(JiraError):
    """
    Unexpected Jira request failure.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
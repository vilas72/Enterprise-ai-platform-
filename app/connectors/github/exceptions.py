from __future__ import annotations


class GitHubError(Exception):
    """
    Base exception for all GitHub connector errors.
    """


class GitHubAuthenticationError(GitHubError):
    """
    Authentication with GitHub failed.
    """


class GitHubAuthorizationError(GitHubError):
    """
    The caller is not authorized to perform the requested operation.
    """


class GitHubNotFoundError(GitHubError):
    """
    The requested GitHub resource does not exist.
    """


class GitHubRateLimitError(GitHubError):
    """
    GitHub API rate limit exceeded.
    """


class GitHubValidationError(GitHubError):
    """
    GitHub rejected the supplied request because of validation errors.
    """


class GitHubConflictError(GitHubError):
    """
    The request conflicts with the current state of the resource.
    """


class GitHubServerError(GitHubError):
    """
    GitHub returned an internal server error.
    """


class GitHubRequestError(GitHubError):
    """
    Unexpected GitHub request failure.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
from __future__ import annotations

from typing import Any

import httpx
import logging

from httpx import HTTPStatusError
from .exceptions import (
    GitHubAuthenticationError,
    GitHubAuthorizationError,
    GitHubNotFoundError,
    GitHubRateLimitError,
    GitHubValidationError,
    GitHubConflictError,
    GitHubServerError,
    GitHubRequestError,
)

logger = logging.getLogger(__name__)

class GitHubClient:
    """
    Async GitHub REST client.

    This client is responsible only for HTTP communication with
    the GitHub REST API.

    Business operations belong in GitHubConnector.
    """

    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        *,
        base_url: str = "https://api.github.com",
        token: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        cleaned_token = token.strip()
        if cleaned_token:
            headers["Authorization"] = f"Bearer {cleaned_token}"
        logger.info("GitHub Token Present: %s", bool(cleaned_token))
        logger.info("GitHub Token Length: %d", len(cleaned_token))
        
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
        )

    async def close(self) -> None:
        """
        Close HTTP resources.
        """

        await self._client.aclose()

    async def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        """
        Execute a GET request.
        """

        response = await self._client.get(
            url,
            params=params,
        )

        self._raise_for_status(response)

        return response.json()

    async def post(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a POST request.
        """

        response = await self._client.post(
            url,
            json=json,
        )

        self._raise_for_status(response)

        if response.status_code == 204:
            return {}

        if not response.content:
            return {}

        return response.json()
    
    async def patch(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a PATCH request.
        """

        response = await self._client.patch(
            url,
            json=json,
        )

        self._raise_for_status(response)

        if response.status_code == 204:
            return {}

        if not response.content:
            return {}

        return response.json()

    async def delete(
        self,
        url: str,
    ) -> None:
        """
        Execute a DELETE request.
        """

        response = await self._client.delete(url)

        self._raise_for_status(response)
        
    async def put(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a PUT request.
        """

        response = await self._client.put(
            url,
            json=json,
        )

        self._raise_for_status(response)

        return response.json()
    
    def _raise_for_status(
        self,
        response: httpx.Response,
    ) -> None:
        """
        Translate HTTP errors into GitHub domain exceptions.
        """

        try:
            response.raise_for_status()

        except HTTPStatusError as exc:

            status = exc.response.status_code

            if status == 401:
                raise GitHubAuthenticationError(
                    "GitHub authentication failed."
                ) from exc

            if status == 403:
                raise GitHubAuthorizationError(
                    "GitHub authorization failed."
                ) from exc

            if status == 404:
                raise GitHubNotFoundError(
                    "GitHub resource not found."
                ) from exc

            if status == 409:
                raise GitHubConflictError(
                    "GitHub resource conflict."
                ) from exc

            if status == 422:
                raise GitHubValidationError(
                    "GitHub validation failed."
                ) from exc

            if status == 429:
                raise GitHubRateLimitError(
                    "GitHub API rate limit exceeded."
                ) from exc

            if status >= 500:
                raise GitHubServerError(
                    "GitHub server error."
                ) from exc

            raise GitHubRequestError(
                "GitHub request failed.",
                status_code=status,
            ) from exc
"""
Enterprise Confluence REST client.

This client is responsible only for HTTP communication with the
Confluence REST API.

Business operations belong in ConfluenceConnector.
"""

from __future__ import annotations

from typing import Any

import httpx
from httpx import HTTPStatusError

from .exceptions import (
    ConfluenceAuthenticationError,
    ConfluenceAuthorizationError,
    ConfluenceConflictError,
    ConfluenceNotFoundError,
    ConfluenceRateLimitError,
    ConfluenceRequestError,
    ConfluenceServerError,
    ConfluenceValidationError,
)


class ConfluenceClient:
    """
    Async Confluence REST client.
    """

    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        *,
        base_url: str,
        token: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:

        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    async def close(
        self,
    ) -> None:
        """
        Release HTTP resources.
        """

        await self._client.aclose()

    # ==========================================================
    # HTTP
    # ==========================================================

    async def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

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

    async def put(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        response = await self._client.put(
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

        response = await self._client.delete(url)

        self._raise_for_status(response)

    # ==========================================================
    # Error Translation
    # ==========================================================

    def _raise_for_status(
        self,
        response: httpx.Response,
    ) -> None:
        """
        Translate HTTP errors into Confluence domain exceptions.
        """

        try:

            response.raise_for_status()

        except HTTPStatusError as exc:

            status = exc.response.status_code

            if status == 401:
                raise ConfluenceAuthenticationError(
                    "Confluence authentication failed."
                ) from exc

            if status == 403:
                raise ConfluenceAuthorizationError(
                    "Confluence authorization failed."
                ) from exc

            if status == 404:
                raise ConfluenceNotFoundError(
                    "Confluence resource not found."
                ) from exc

            if status == 409:
                raise ConfluenceConflictError(
                    "Confluence resource conflict."
                ) from exc

            if status == 422:
                raise ConfluenceValidationError(
                    "Confluence validation failed."
                ) from exc

            if status == 429:
                raise ConfluenceRateLimitError(
                    "Confluence API rate limit exceeded."
                ) from exc

            if status >= 500:
                raise ConfluenceServerError(
                    "Confluence server error."
                ) from exc

            raise ConfluenceRequestError(
                "Confluence request failed.",
                status_code=status,
            ) from exc
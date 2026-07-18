from __future__ import annotations

import base64
from typing import Any

from fastapi import logger
import httpx

from app.connectors.jira.exceptions import (
    JiraAuthenticationError,
    JiraAuthorizationError,
    JiraConflictError,
    JiraNotFoundError,
    JiraRateLimitError,
    JiraRequestError,
    JiraServerError,
    JiraValidationError,
)


class JiraClient:
    """
    Async Jira REST client.

    This client is responsible only for HTTP communication with
    the Jira REST API.

    Business logic belongs in JiraConnector.
    """

    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        *,
        base_url: str,
        email: str,
        api_token: str,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        credentials = f"{email}:{api_token}".encode("utf-8")
        authorization = base64.b64encode(credentials).decode("utf-8")

        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers={
                "Authorization": f"Basic {authorization}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    async def close(self) -> None:
        """
        Release HTTP resources.
        """

        await self._client.aclose()

    async def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        response = await self._client.get(
            url,
            params=params,
        )

        self._raise_for_status(response)

        if not response.content:
            return {}

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

    async def delete(
        self,
        url: str,
    ) -> None:
        response = await self._client.delete(url)

        self._raise_for_status(response)

    def _raise_for_status(
        self,
        response: httpx.Response,
    ) -> None:
        """
        Translate HTTP errors into Jira connector exceptions.
        """

        try:
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:

            status = exc.response.status_code

            if status == 401:
                raise JiraAuthenticationError(
                    "Jira authentication failed."
                ) from exc

            if status == 403:
                raise JiraAuthorizationError(
                    "Jira authorization failed."
                ) from exc

            if status == 404:
                raise JiraNotFoundError(
                    "Jira resource not found."
                ) from exc

            if status == 409:
                raise JiraConflictError(
                    "Jira resource conflict."
                ) from exc

            if status == 422:
                raise JiraValidationError(
                    "Jira validation failed."
                ) from exc

            if status == 429:
                raise JiraRateLimitError(
                    "Jira API rate limit exceeded."
                ) from exc

            if status >= 500:
                raise JiraServerError(
                    "Jira server error."
                ) from exc

            logger.logger.error(
                "Jira request failed with status %s: %s",
                status,
                response.text,
            )

            raise JiraRequestError(
                f"Jira request failed: {response.text}"
            ) from exc
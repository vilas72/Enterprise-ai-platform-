from __future__ import annotations

from functools import lru_cache

from app.connectors.github.github_client import GitHubClient
from app.connectors.github.github_connector import GitHubConnector
from app.core.config import Settings, get_settings


@lru_cache(maxsize=1)
def get_github_client() -> GitHubClient:
    """
    Returns the singleton GitHub client.
    """

    settings: Settings = get_settings()

    return GitHubClient(
        token=settings.github.token,
        base_url=settings.github.base_url,
        timeout=settings.github.timeout,
    )


@lru_cache(maxsize=1)
def get_github_connector() -> GitHubConnector:
    """
    Returns the singleton GitHub connector.
    """

    return GitHubConnector(
        client=get_github_client(),
    )
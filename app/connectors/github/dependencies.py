from __future__ import annotations

import os
from functools import lru_cache

from app.connectors.github.github_client import GitHubClient
from app.connectors.github.github_connector import GitHubConnector
from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_github_client() -> GitHubClient:
    """
    Returns the singleton GitHub client.
    """

    settings = get_settings()
    base_url = os.getenv("GITHUB_BASE_URL") or "https://api.github.com"
    timeout_value = os.getenv("GITHUB_TIMEOUT")
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_API_TOKEN") or ""

    if timeout_value is not None:
        try:
            timeout = float(timeout_value)
        except ValueError:
            timeout = GitHubClient.DEFAULT_TIMEOUT
    else:
        timeout = GitHubClient.DEFAULT_TIMEOUT

    if hasattr(settings, "github"):
        github_settings = getattr(settings, "github")
        base_url = getattr(github_settings, "base_url", base_url) or base_url
        timeout = getattr(github_settings, "timeout", timeout)
        token = getattr(github_settings, "token", token) or token

    return GitHubClient(
        token=token,
        base_url=base_url,
        timeout=timeout,
    )


@lru_cache(maxsize=1)
def get_github_connector() -> GitHubConnector:
    """
    Returns the singleton GitHub connector.
    """

    return GitHubConnector(
        client=get_github_client(),
    )
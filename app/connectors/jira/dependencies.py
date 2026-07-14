from __future__ import annotations

from functools import lru_cache

from app.connectors.jira.jira_client import JiraClient
from app.connectors.jira.jira_connector import JiraConnector
from app.core.config import Settings, get_settings


@lru_cache(maxsize=1)
def get_jira_client() -> JiraClient:
    """
    Returns the singleton Jira client.
    """

    settings: Settings = get_settings()

    return JiraClient(
        base_url=settings.jira.base_url,
        email=settings.jira.email,
        api_token=settings.jira.api_token,
        timeout=settings.jira.timeout,
    )


@lru_cache(maxsize=1)
def get_jira_connector() -> JiraConnector:
    """
    Returns the singleton Jira connector.
    """

    return JiraConnector(
        client=get_jira_client(),
    )                                                                                   
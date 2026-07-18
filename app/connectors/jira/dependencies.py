from __future__ import annotations

import os
from functools import lru_cache

from app.connectors.jira.jira_client import JiraClient
from app.connectors.jira.jira_connector import JiraConnector
from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_jira_client() -> JiraClient:
    """
    Returns the singleton Jira client.
    """

    settings = get_settings()
    base_url = os.getenv("JIRA_BASE_URL") or "https://vilasrajage7289.atlassian.net/"
    email = os.getenv("JIRA_EMAIL") or ""
    api_token = os.getenv("JIRA_API_TOKEN") or ""
    timeout_value = os.getenv("JIRA_TIMEOUT")

    if timeout_value is not None:
        try:
            timeout = float(timeout_value)
        except ValueError:
            timeout = JiraClient.DEFAULT_TIMEOUT
    else:
        timeout = JiraClient.DEFAULT_TIMEOUT

    if hasattr(settings, "jira"):
        jira_settings = getattr(settings, "jira")
        base_url = getattr(jira_settings, "base_url", base_url) or base_url
        email = getattr(jira_settings, "email", email) or email
        api_token = getattr(jira_settings, "api_token", api_token) or api_token
        timeout = getattr(jira_settings, "timeout", timeout)

    return JiraClient(
        base_url=base_url,
        email=email,
        api_token=api_token,
        timeout=timeout,
    )


@lru_cache(maxsize=1)
def get_jira_connector() -> JiraConnector:
    """
    Returns the singleton Jira connector.
    """

    return JiraConnector(
        client=get_jira_client(),
    )                                                                                   
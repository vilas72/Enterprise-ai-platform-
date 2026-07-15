"""
Dependency registration for the Enterprise Confluence Connector.
"""

from __future__ import annotations

from functools import lru_cache

from app.core.config import settings

from .client import ConfluenceClient
from .connector import ConfluenceConnector


@lru_cache
def get_confluence_client() -> ConfluenceClient:
    """
    Create a singleton Confluence REST client.
    """

    return ConfluenceClient(
        base_url=settings.confluence_base_url,
        token=settings.confluence_token,
    )


@lru_cache
def get_confluence_connector() -> ConfluenceConnector:
    """
    Create the Enterprise Confluence connector.
    """

    return ConfluenceConnector(
        client=get_confluence_client(),
    )
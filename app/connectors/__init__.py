"""Connectors package for enterprise knowledge source integrations."""

from app.connectors.base_connector import KnowledgeConnector, ConnectorConfig
from app.connectors.filesystem_connector import FileSystemConnector, FileSystemConfig
from app.connectors.web_scraper_connector import WebScraperConnector, WebScraperConfig
from app.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
    DatabaseDialect,
    QueryConfig,
)
from app.connectors.connector_registry import (
    KnowledgeConnectorRegistry,
    ConnectorNotFoundError,
    ConnectorAlreadyRegisteredError,
)

__all__ = [
    "KnowledgeConnector",
    "ConnectorConfig",
    "FileSystemConnector",
    "FileSystemConfig",
    "WebScraperConnector",
    "WebScraperConfig",
    "DatabaseConnector",
    "DatabaseConfig",
    "DatabaseDialect",
    "QueryConfig",
    "KnowledgeConnectorRegistry",
    "ConnectorNotFoundError",
    "ConnectorAlreadyRegisteredError",
]

"""Knowledge connector registry for managing and discovering connectors."""

from __future__ import annotations

from typing import Callable, Type

from app.connectors.base_connector import KnowledgeConnector
from app.document.document import Document


class ConnectorNotFoundError(Exception):
    """Raised when a connector type is not registered."""
    pass


class ConnectorAlreadyRegisteredError(Exception):
    """Raised when attempting to register a connector ID that already exists."""
    pass


class KnowledgeConnectorRegistry:
    """
    Central registry for discovering and instantiating knowledge connectors.

    Supports:
    - Registration of connector types by ID
    - Creating connector instances from config
    - Bulk ingestion: fetch from all registered connectors and return Documents
    - Discovery: list registered connector IDs

    Usage:
        registry = KnowledgeConnectorRegistry()
        registry.register("filesystem", FileSystemConnector)
        registry.register("web_scraper", WebScraperConnector)
        registry.register("database", DatabaseConnector)

        # Fetch from a single connector
        config = FileSystemConfig(root_path="/data/docs")
        async with registry.create("filesystem", config) as connector:
            documents = await connector.fetch()

        # Fetch from all registered connectors at once
        configs = {
            "filesystem": FileSystemConfig(...),
            "database": DatabaseConfig(...),
        }
        all_docs = await registry.fetch_all(configs)
    """

    def __init__(self):
        self._registry: dict[str, Type[KnowledgeConnector]] = {}

    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------

    def register(
        self,
        connector_id: str,
        connector_class: Type[KnowledgeConnector],
        *,
        overwrite: bool = False,
    ) -> None:
        """
        Register a connector class under the given ID.

        Args:
            connector_id: Unique identifier string (e.g. "filesystem")
            connector_class: Class (not instance) implementing KnowledgeConnector
            overwrite: If True, silently replace an existing registration

        Raises:
            ConnectorAlreadyRegisteredError: If ID is taken and overwrite=False
        """
        if connector_id in self._registry and not overwrite:
            raise ConnectorAlreadyRegisteredError(
                f"Connector '{connector_id}' is already registered. "
                "Pass overwrite=True to replace it."
            )
        self._registry[connector_id] = connector_class

    def unregister(self, connector_id: str) -> None:
        """
        Remove a connector from the registry.

        Raises:
            ConnectorNotFoundError: If the connector ID is not registered
        """
        if connector_id not in self._registry:
            raise ConnectorNotFoundError(
                f"Connector '{connector_id}' is not registered."
            )
        del self._registry[connector_id]

    # -------------------------------------------------------------------------
    # Discovery
    # -------------------------------------------------------------------------

    def list_connectors(self) -> list[str]:
        """Return a sorted list of all registered connector IDs."""
        return sorted(self._registry.keys())

    def is_registered(self, connector_id: str) -> bool:
        """Return True if the given connector ID is registered."""
        return connector_id in self._registry

    def get_class(self, connector_id: str) -> Type[KnowledgeConnector]:
        """
        Return the class registered under the given ID.

        Raises:
            ConnectorNotFoundError: If the ID is not registered
        """
        if connector_id not in self._registry:
            raise ConnectorNotFoundError(
                f"Connector '{connector_id}' is not registered. "
                f"Available: {self.list_connectors()}"
            )
        return self._registry[connector_id]

    # -------------------------------------------------------------------------
    # Instantiation
    # -------------------------------------------------------------------------

    def create(self, connector_id: str, config) -> KnowledgeConnector:
        """
        Instantiate a connector by ID with the provided config.

        Args:
            connector_id: Registered connector identifier
            config: Configuration object matching the connector's constructor

        Returns:
            A new KnowledgeConnector instance (not yet connected)

        Raises:
            ConnectorNotFoundError: If the ID is not registered
        """
        connector_class = self.get_class(connector_id)
        return connector_class(config)

    # -------------------------------------------------------------------------
    # Bulk operations
    # -------------------------------------------------------------------------

    async def fetch_all(
        self,
        connector_configs: dict[str, object],
        *,
        stop_on_error: bool = False,
    ) -> list[Document]:
        """
        Fetch documents from all connectors whose ID appears in connector_configs.

        Connectors are invoked sequentially. Errors are collected rather than
        raised (unless stop_on_error=True), so a single failing connector does
        not block the others.

        Args:
            connector_configs: Maps connector_id → config object
            stop_on_error: If True, re-raise the first error encountered

        Returns:
            Aggregated list of Document objects from all connectors
        """
        all_documents: list[Document] = []
        errors: list[tuple[str, Exception]] = []

        for connector_id, config in connector_configs.items():
            try:
                connector = self.create(connector_id, config)
                async with connector:
                    documents = await connector.fetch()
                all_documents.extend(documents)
            except Exception as exc:
                if stop_on_error:
                    raise
                errors.append((connector_id, exc))

        # Surface errors as a warning-level summary (non-fatal by default)
        if errors:
            error_summary = "; ".join(
                f"{cid}: {type(e).__name__}({e})"
                for cid, e in errors
            )
            import warnings
            warnings.warn(
                f"KnowledgeConnectorRegistry.fetch_all encountered errors: {error_summary}",
                RuntimeWarning,
                stacklevel=2,
            )

        return all_documents

    # -------------------------------------------------------------------------
    # Dunder
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._registry)

    def __repr__(self) -> str:
        return (
            f"KnowledgeConnectorRegistry("
            f"connectors={self.list_connectors()})"
        )

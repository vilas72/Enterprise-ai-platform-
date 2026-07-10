"""Knowledge connector abstractions for enterprise data source integration."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.document.document import Document


class ConnectorConfig(ABC):
    """Base configuration for knowledge connectors."""
    pass


class KnowledgeConnector(ABC):
    """
    Abstract base class for all knowledge source connectors.

    Each connector is responsible for:
    - Connecting to a data source
    - Extracting documents
    - Normalizing them to Document format
    """

    @property
    @abstractmethod
    def connector_id(self) -> str:
        """Unique identifier for this connector type."""
        ...

    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to the data source."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Release any resources held by this connector."""
        ...

    @abstractmethod
    async def fetch(self) -> list[Document]:
        """
        Fetch all available documents from the data source.

        Returns:
            List of normalized Document objects
        """
        ...

    async def __aenter__(self) -> "KnowledgeConnector":
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.disconnect()

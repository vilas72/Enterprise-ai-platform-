"""Unit tests for KnowledgeConnectorRegistry."""

import warnings
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from app.connectors.base_connector import KnowledgeConnector
from app.connectors.connector_registry import (
    KnowledgeConnectorRegistry,
    ConnectorNotFoundError,
    ConnectorAlreadyRegisteredError,
)
from app.connectors.filesystem_connector import FileSystemConnector, FileSystemConfig
from app.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
    DatabaseDialect,
    QueryConfig,
)
from app.document.document import Document


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------

class MockConnector(KnowledgeConnector):
    """Minimal connector for testing."""

    CONNECTOR_ID = "mock"

    def __init__(self, config=None):
        self.config = config
        self._connected = False

    @property
    def connector_id(self) -> str:
        return self.CONNECTOR_ID

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False

    async def fetch(self) -> list[Document]:
        return [
            Document(
                id="mock-1",
                name="Mock Document",
                text="This is a mock document.",
                metadata={"source": "mock"},
            )
        ]


class FailingConnector(KnowledgeConnector):
    """Connector that always fails on fetch."""

    def __init__(self, config=None):
        pass

    @property
    def connector_id(self) -> str:
        return "failing"

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def fetch(self) -> list[Document]:
        raise RuntimeError("Simulated fetch failure")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRegistration:
    """Test connector registration and discovery."""

    def test_register_connector(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        assert registry.is_registered("mock")

    def test_register_duplicate_raises(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        with pytest.raises(ConnectorAlreadyRegisteredError, match="already registered"):
            registry.register("mock", MockConnector)

    def test_register_duplicate_with_overwrite(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        registry.register("mock", MockConnector, overwrite=True)
        assert registry.is_registered("mock")

    def test_unregister_connector(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        registry.unregister("mock")
        assert not registry.is_registered("mock")

    def test_unregister_nonexistent_raises(self):
        registry = KnowledgeConnectorRegistry()
        with pytest.raises(ConnectorNotFoundError):
            registry.unregister("nonexistent")

    def test_list_connectors_sorted(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("zebra", MockConnector)
        registry.register("apple", MockConnector)
        registry.register("mango", MockConnector)
        assert registry.list_connectors() == ["apple", "mango", "zebra"]

    def test_list_connectors_empty(self):
        registry = KnowledgeConnectorRegistry()
        assert registry.list_connectors() == []

    def test_is_registered_false_for_unknown(self):
        registry = KnowledgeConnectorRegistry()
        assert not registry.is_registered("unknown")

    def test_len(self):
        registry = KnowledgeConnectorRegistry()
        assert len(registry) == 0
        registry.register("mock", MockConnector)
        assert len(registry) == 1

    def test_get_class(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        assert registry.get_class("mock") is MockConnector

    def test_get_class_nonexistent_raises(self):
        registry = KnowledgeConnectorRegistry()
        with pytest.raises(ConnectorNotFoundError, match="not registered"):
            registry.get_class("nonexistent")

    def test_repr(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        assert "mock" in repr(registry)


class TestCreate:
    """Test connector instantiation."""

    def test_create_returns_connector_instance(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        config = object()
        connector = registry.create("mock", config)
        assert isinstance(connector, MockConnector)
        assert connector.config is config

    def test_create_nonexistent_raises(self):
        registry = KnowledgeConnectorRegistry()
        with pytest.raises(ConnectorNotFoundError):
            registry.create("nonexistent", None)

    def test_create_multiple_independent_instances(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        c1 = registry.create("mock", "config-a")
        c2 = registry.create("mock", "config-b")
        assert c1 is not c2
        assert c1.config == "config-a"
        assert c2.config == "config-b"


class TestFetchAll:
    """Test bulk fetch across multiple connectors."""

    @pytest.mark.asyncio
    async def test_fetch_all_aggregates_documents(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)

        configs = {
            "mock": None,
        }
        documents = await registry.fetch_all(configs)

        assert len(documents) == 1
        assert documents[0].id == "mock-1"

    @pytest.mark.asyncio
    async def test_fetch_all_multiple_connectors(self):
        class MockConnectorA(MockConnector):
            CONNECTOR_ID = "mock_a"
            async def fetch(self):
                return [Document(id="a-1", name="A Doc", text="Doc A", metadata={})]

        class MockConnectorB(MockConnector):
            CONNECTOR_ID = "mock_b"
            async def fetch(self):
                return [
                    Document(id="b-1", name="B Doc 1", text="Doc B1", metadata={}),
                    Document(id="b-2", name="B Doc 2", text="Doc B2", metadata={}),
                ]

        registry = KnowledgeConnectorRegistry()
        registry.register("mock_a", MockConnectorA)
        registry.register("mock_b", MockConnectorB)

        documents = await registry.fetch_all({
            "mock_a": None,
            "mock_b": None,
        })

        assert len(documents) == 3
        ids = {d.id for d in documents}
        assert ids == {"a-1", "b-1", "b-2"}

    @pytest.mark.asyncio
    async def test_fetch_all_skips_errors_by_default(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("mock", MockConnector)
        registry.register("failing", FailingConnector)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            documents = await registry.fetch_all({
                "mock": None,
                "failing": None,
            })

        # Should still return the mock docs
        assert len(documents) == 1
        assert documents[0].id == "mock-1"

        # Should have emitted a warning about the failure
        assert len(caught) == 1
        assert "failing" in str(caught[0].message)

    @pytest.mark.asyncio
    async def test_fetch_all_stop_on_error(self):
        registry = KnowledgeConnectorRegistry()
        registry.register("failing", FailingConnector)

        with pytest.raises(RuntimeError, match="Simulated fetch failure"):
            await registry.fetch_all({"failing": None}, stop_on_error=True)

    @pytest.mark.asyncio
    async def test_fetch_all_empty_configs(self):
        registry = KnowledgeConnectorRegistry()
        documents = await registry.fetch_all({})
        assert documents == []

    @pytest.mark.asyncio
    async def test_fetch_all_with_real_filesystem_connector(self, tmp_path: Path):
        (tmp_path / "knowledge.txt").write_text("Enterprise AI knowledge base content.")

        registry = KnowledgeConnectorRegistry()
        registry.register("filesystem", FileSystemConnector)

        config = FileSystemConfig(root_path=str(tmp_path))
        documents = await registry.fetch_all({"filesystem": config})

        assert len(documents) == 1
        assert "Enterprise AI knowledge base content" in documents[0].text

    @pytest.mark.asyncio
    async def test_fetch_all_with_real_database_connector(self, tmp_path: Path):
        import sqlite3
        db_path = str(tmp_path / "test.db")
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE docs (id INTEGER PRIMARY KEY, text TEXT)")
        conn.execute("INSERT INTO docs VALUES (1, 'Registry integration test.')")
        conn.commit()
        conn.close()

        registry = KnowledgeConnectorRegistry()
        registry.register("database", DatabaseConnector)

        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=db_path,
            queries=[
                QueryConfig(
                    sql="SELECT id, text FROM docs",
                    text_columns=["text"],
                    id_column="id",
                    label="docs",
                )
            ],
        )
        documents = await registry.fetch_all({"database": config})

        assert len(documents) == 1
        assert "Registry integration test" in documents[0].text

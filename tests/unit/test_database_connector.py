"""Unit tests for DatabaseConnector."""

import sqlite3
import pytest
from pathlib import Path

from app.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
    DatabaseDialect,
    QueryConfig,
)


@pytest.fixture
def sqlite_db(tmp_path: Path) -> str:
    """Create a temporary SQLite database with sample data."""
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Articles table
    cursor.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT,
            category TEXT
        )
    """)
    cursor.executemany(
        "INSERT INTO articles (title, content, author, category) VALUES (?, ?, ?, ?)",
        [
            ("Python Basics", "Python is a high-level programming language.", "Alice", "programming"),
            ("FastAPI Guide", "FastAPI is a modern web framework for Python.", "Bob", "web"),
            ("Machine Learning", "ML is a subset of artificial intelligence.", "Carol", "ai"),
        ],
    )

    # Products table
    cursor.execute("""
        CREATE TABLE products (
            sku TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL
        )
    """)
    cursor.executemany(
        "INSERT INTO products (sku, name, description, price) VALUES (?, ?, ?, ?)",
        [
            ("SKU-001", "Widget Pro", "A professional grade widget.", 29.99),
            ("SKU-002", "Gadget Plus", "Next generation gadget.", 49.99),
        ],
    )

    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def basic_config(sqlite_db: str) -> DatabaseConfig:
    """Basic config querying the articles table."""
    return DatabaseConfig(
        dialect=DatabaseDialect.SQLITE,
        connection_string=sqlite_db,
        queries=[
            QueryConfig(
                sql="SELECT id, title, content, author, category FROM articles",
                text_columns=["title", "content"],
                id_column="id",
                metadata_columns=["author", "category"],
                label="articles",
            )
        ],
    )


class TestDatabaseConnectorConnect:
    """Test connection lifecycle."""

    @pytest.mark.asyncio
    async def test_connect_sqlite(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[],
        )
        connector = DatabaseConnector(config)
        await connector.connect()
        assert connector._connection is not None
        await connector.disconnect()

    @pytest.mark.asyncio
    async def test_disconnect_closes_connection(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[],
        )
        connector = DatabaseConnector(config)
        await connector.connect()
        await connector.disconnect()
        assert connector._connection is None

    @pytest.mark.asyncio
    async def test_fetch_without_connect_raises(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[],
        )
        connector = DatabaseConnector(config)
        with pytest.raises(RuntimeError, match="not connected"):
            await connector.fetch()

    def test_connector_id(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[],
        )
        connector = DatabaseConnector(config)
        assert connector.connector_id == "database"

    @pytest.mark.asyncio
    async def test_context_manager(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[],
        )
        async with DatabaseConnector(config) as connector:
            assert connector._connection is not None
        assert connector._connection is None


class TestDatabaseConnectorFetch:
    """Test document fetching."""

    @pytest.mark.asyncio
    async def test_fetch_returns_one_document_per_row(self, basic_config: DatabaseConfig):
        async with DatabaseConnector(basic_config) as connector:
            documents = await connector.fetch()

        assert len(documents) == 3

    @pytest.mark.asyncio
    async def test_fetch_document_text_from_text_columns(self, basic_config: DatabaseConfig):
        async with DatabaseConnector(basic_config) as connector:
            documents = await connector.fetch()

        doc = next(d for d in documents if "Python" in d.text)
        assert "Python Basics" in doc.text
        assert "Python is a high-level programming language." in doc.text

    @pytest.mark.asyncio
    async def test_fetch_document_id_from_id_column(self, basic_config: DatabaseConfig):
        async with DatabaseConnector(basic_config) as connector:
            documents = await connector.fetch()

        # IDs should be the row's integer primary key as string
        ids = {d.id for d in documents}
        assert "1" in ids
        assert "2" in ids
        assert "3" in ids

    @pytest.mark.asyncio
    async def test_fetch_metadata_columns(self, basic_config: DatabaseConfig):
        async with DatabaseConnector(basic_config) as connector:
            documents = await connector.fetch()

        doc = next(d for d in documents if d.id == "1")
        assert doc.metadata["author"] == "Alice"
        assert doc.metadata["category"] == "programming"
        assert doc.metadata["source"] == "database"
        assert doc.metadata["dialect"] == "sqlite"
        assert doc.metadata["label"] == "articles"

    @pytest.mark.asyncio
    async def test_fetch_document_name_is_first_text_column(self, basic_config: DatabaseConfig):
        async with DatabaseConnector(basic_config) as connector:
            documents = await connector.fetch()

        doc = next(d for d in documents if d.id == "1")
        assert doc.name == "Python Basics"

    @pytest.mark.asyncio
    async def test_fetch_multiple_queries(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[
                QueryConfig(
                    sql="SELECT id, title, content FROM articles",
                    text_columns=["title", "content"],
                    id_column="id",
                    label="articles",
                ),
                QueryConfig(
                    sql="SELECT sku, name, description FROM products",
                    text_columns=["name", "description"],
                    id_column="sku",
                    label="products",
                ),
            ],
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()

        assert len(documents) == 5  # 3 articles + 2 products
        labels = {d.metadata["label"] for d in documents}
        assert labels == {"articles", "products"}

    @pytest.mark.asyncio
    async def test_fetch_all_columns_when_no_text_columns(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[
                QueryConfig(
                    sql="SELECT id, title, content FROM articles WHERE id = 1",
                    text_columns=[],  # No specific columns — use all
                    label="articles",
                )
            ],
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()

        assert len(documents) == 1
        # All columns should appear as "key: value" pairs
        assert "title: Python Basics" in documents[0].text
        assert "content:" in documents[0].text

    @pytest.mark.asyncio
    async def test_fetch_auto_generated_id_when_no_id_column(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[
                QueryConfig(
                    sql="SELECT title, content FROM articles",
                    text_columns=["title", "content"],
                    id_column=None,  # No ID column
                    label="articles",
                )
            ],
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()

        # IDs should be generated and stable
        assert len(documents) == 3
        assert all(len(d.id) == 16 for d in documents)

        # Same query should produce same IDs
        async with DatabaseConnector(config) as connector:
            documents2 = await connector.fetch()

        ids_first = {d.id for d in documents}
        ids_second = {d.id for d in documents2}
        assert ids_first == ids_second

    @pytest.mark.asyncio
    async def test_fetch_respects_max_rows(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[
                QueryConfig(
                    sql="SELECT id, title, content FROM articles",
                    text_columns=["title", "content"],
                    id_column="id",
                    label="articles",
                )
            ],
            max_rows_per_query=2,
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()

        assert len(documents) == 2

    @pytest.mark.asyncio
    async def test_fetch_empty_result_returns_empty_list(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[
                QueryConfig(
                    sql="SELECT id, title, content FROM articles WHERE 1=0",
                    text_columns=["title", "content"],
                    id_column="id",
                    label="articles",
                )
            ],
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()

        assert documents == []

    @pytest.mark.asyncio
    async def test_fetch_with_sql_filtering(self, sqlite_db: str):
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string=sqlite_db,
            queries=[
                QueryConfig(
                    sql="SELECT id, title, content FROM articles WHERE category = 'ai'",
                    text_columns=["title", "content"],
                    id_column="id",
                    label="articles",
                )
            ],
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()

        assert len(documents) == 1
        assert "Machine Learning" in documents[0].text

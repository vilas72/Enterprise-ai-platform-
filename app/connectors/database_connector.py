"""Database knowledge connector for ingesting data from SQL databases."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.connectors.base_connector import KnowledgeConnector
from app.document.document import Document


class DatabaseDialect(str, Enum):
    """Supported database dialects."""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"


@dataclass
class QueryConfig:
    """
    Configuration for a single query to execute.

    Attributes:
        sql: SQL SELECT statement to execute
        text_columns: Column names whose values form the document text
                      (joined with newlines). If empty, all columns are used.
        id_column: Column that provides a stable document ID.
                   If None, a hash of the row data is used.
        metadata_columns: Additional columns to store in document metadata
        label: Human-readable label for this query (used as document source)
    """

    sql: str
    text_columns: list[str] = field(default_factory=list)
    id_column: str | None = None
    metadata_columns: list[str] = field(default_factory=list)
    label: str = "database"


@dataclass
class DatabaseConfig:
    """
    Configuration for the DatabaseConnector.

    Attributes:
        dialect: Database type (sqlite, postgresql, mysql)
        connection_string: Full DSN / connection string.
                           For SQLite: path to the .db file.
                           For PostgreSQL: postgresql://user:pass@host/db
                           For MySQL: mysql+pymysql://user:pass@host/db
        queries: One or more QueryConfig objects to execute
        max_rows_per_query: Safety cap per query (default 10 000)
    """

    dialect: DatabaseDialect
    connection_string: str
    queries: list[QueryConfig]
    max_rows_per_query: int = 10_000


class DatabaseConnector(KnowledgeConnector):
    """
    Executes SQL queries and converts result rows into Document objects.

    Each row in the result set becomes one Document.
    Text is assembled from designated text columns (or all columns if none
    are specified), and extra columns can be stored as metadata.

    Supports SQLite (built-in), PostgreSQL (psycopg2/asyncpg), and
    MySQL (pymysql). The underlying driver is selected automatically based
    on the configured dialect.

    Usage:
        config = DatabaseConfig(
            dialect=DatabaseDialect.SQLITE,
            connection_string="/data/knowledge.db",
            queries=[
                QueryConfig(
                    sql="SELECT id, title, content FROM articles",
                    text_columns=["title", "content"],
                    id_column="id",
                    metadata_columns=["title"],
                    label="articles",
                )
            ],
        )
        async with DatabaseConnector(config) as connector:
            documents = await connector.fetch()
    """

    CONNECTOR_ID = "database"

    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._connection = None

    @property
    def connector_id(self) -> str:
        return self.CONNECTOR_ID

    async def connect(self) -> None:
        """Open a connection to the database."""
        self._connection = self._open_connection()

    async def disconnect(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None

    async def fetch(self) -> list[Document]:
        """
        Execute all configured queries and return Documents.

        Each row becomes one Document; text is built from text_columns
        (or all columns when text_columns is empty).

        Returns:
            List of Document objects, one per result row across all queries
        """
        if self._connection is None:
            raise RuntimeError(
                "DatabaseConnector is not connected. "
                "Use 'async with' or call connect() first."
            )

        documents: list[Document] = []

        for query_config in self._config.queries:
            rows = self._execute_query(query_config)
            for row in rows:
                document = self._row_to_document(row, query_config)
                if document is not None:
                    documents.append(document)

        return documents

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _open_connection(self):
        """Open and return a database connection based on the dialect."""
        dialect = self._config.dialect
        dsn = self._config.connection_string

        if dialect == DatabaseDialect.SQLITE:
            return self._connect_sqlite(dsn)
        elif dialect == DatabaseDialect.POSTGRESQL:
            return self._connect_postgresql(dsn)
        elif dialect == DatabaseDialect.MYSQL:
            return self._connect_mysql(dsn)
        else:
            raise ValueError(f"Unsupported dialect: {dialect}")

    @staticmethod
    def _connect_sqlite(path: str):
        """Connect to SQLite (built-in, no extra dependencies)."""
        import sqlite3
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _connect_postgresql(dsn: str):
        """Connect to PostgreSQL using psycopg2."""
        try:
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(dsn)
            return conn
        except ImportError:
            raise RuntimeError(
                "psycopg2 is required for PostgreSQL support. "
                "Install it with: pip install psycopg2-binary"
            )

    @staticmethod
    def _connect_mysql(dsn: str):
        """Connect to MySQL using pymysql."""
        try:
            import pymysql
            import pymysql.cursors
            # Parse DSN: mysql+pymysql://user:pass@host/db
            clean_dsn = dsn.replace("mysql+pymysql://", "")
            userinfo, hostdb = clean_dsn.split("@", 1)
            user, password = userinfo.split(":", 1)
            host_port, database = hostdb.split("/", 1)
            host = host_port.split(":")[0]
            port = int(host_port.split(":")[1]) if ":" in host_port else 3306
            conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor,
            )
            return conn
        except ImportError:
            raise RuntimeError(
                "pymysql is required for MySQL support. "
                "Install it with: pip install pymysql"
            )

    def _execute_query(
        self,
        query_config: QueryConfig,
    ) -> list[dict[str, Any]]:
        """Execute a query and return rows as a list of dicts."""
        cursor = self._connection.cursor()
        try:
            cursor.execute(query_config.sql)
            raw_rows = cursor.fetchmany(self._config.max_rows_per_query)
            # Normalize to list of dicts
            return [self._normalize_row(row) for row in raw_rows]
        finally:
            cursor.close()

    @staticmethod
    def _normalize_row(row) -> dict[str, Any]:
        """Convert a database row to a plain dict."""
        if isinstance(row, dict):
            return row
        # sqlite3.Row, psycopg2.RealDictRow, etc.
        try:
            return dict(row)
        except (TypeError, ValueError):
            return {}

    def _row_to_document(
        self,
        row: dict[str, Any],
        query_config: QueryConfig,
    ) -> Document | None:
        """Convert a single database row to a Document."""
        if not row:
            return None

        # Build document text
        if query_config.text_columns:
            text_parts = [
                str(row[col])
                for col in query_config.text_columns
                if col in row and row[col] is not None
            ]
        else:
            # Use all column values
            text_parts = [
                f"{col}: {val}"
                for col, val in row.items()
                if val is not None
            ]

        text = "\n".join(text_parts).strip()
        if not text:
            return None

        # Stable document ID
        if query_config.id_column and query_config.id_column in row:
            doc_id = str(row[query_config.id_column])
        else:
            doc_id = self._make_row_id(row)

        # Build metadata
        metadata: dict[str, str] = {
            "source": "database",
            "dialect": self._config.dialect.value,
            "label": query_config.label,
        }
        for col in query_config.metadata_columns:
            if col in row and row[col] is not None:
                metadata[col] = str(row[col])

        # Use the first text column value (or id) as document name
        name = (
            str(row.get(query_config.text_columns[0], doc_id))
            if query_config.text_columns
            else doc_id
        )

        return Document(
            id=doc_id,
            name=name[:200],  # Truncate long names
            text=text,
            metadata=metadata,
        )

    @staticmethod
    def _make_row_id(row: dict[str, Any]) -> str:
        """Generate a stable ID from the row's content."""
        serialized = json.dumps(row, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()[:16]

"""Unit tests for FileSystemConnector."""

import os
import pytest
from pathlib import Path

from app.connectors.filesystem_connector import FileSystemConnector, FileSystemConfig


@pytest.fixture
def temp_knowledge_base(tmp_path: Path) -> Path:
    """Create a temporary directory structure with sample files."""
    # Root level files
    (tmp_path / "readme.txt").write_text("Welcome to the knowledge base.")
    (tmp_path / "overview.md").write_text("# Overview\nThis is an overview document.")
    (tmp_path / "data.csv").write_text("name,age\nAlice,30\nBob,25")

    # Subdirectory
    subdir = tmp_path / "technical"
    subdir.mkdir()
    (subdir / "api_guide.txt").write_text("API Guide: use /api/v1 endpoints.")
    (subdir / "deployment.md").write_text("# Deployment\nUse Docker.")

    # Nested subdirectory
    nested = subdir / "advanced"
    nested.mkdir()
    (nested / "performance.txt").write_text("Performance tuning tips here.")

    # Files that should be excluded
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n")  # unsupported extension
    (tmp_path / ".hidden.txt").write_text("hidden file")  # excluded by pattern

    return tmp_path


class TestFileSystemConnectorConnect:
    """Test connector validation on connect."""

    @pytest.mark.asyncio
    async def test_connect_valid_path(self, temp_knowledge_base: Path):
        config = FileSystemConfig(root_path=str(temp_knowledge_base))
        connector = FileSystemConnector(config)
        await connector.connect()  # Should not raise

    @pytest.mark.asyncio
    async def test_connect_nonexistent_path(self, tmp_path: Path):
        config = FileSystemConfig(root_path=str(tmp_path / "does_not_exist"))
        connector = FileSystemConnector(config)
        with pytest.raises(FileNotFoundError, match="does not exist"):
            await connector.connect()

    @pytest.mark.asyncio
    async def test_connect_file_path_raises(self, tmp_path: Path):
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")
        config = FileSystemConfig(root_path=str(file_path))
        connector = FileSystemConnector(config)
        with pytest.raises(NotADirectoryError, match="not a directory"):
            await connector.connect()


class TestFileSystemConnectorFetch:
    """Test document fetching."""

    @pytest.mark.asyncio
    async def test_fetch_returns_documents(self, temp_knowledge_base: Path):
        config = FileSystemConfig(root_path=str(temp_knowledge_base))
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        assert len(documents) > 0
        assert all(doc.text.strip() for doc in documents)

    @pytest.mark.asyncio
    async def test_fetch_document_fields(self, temp_knowledge_base: Path):
        config = FileSystemConfig(
            root_path=str(temp_knowledge_base),
            extensions={".txt"},
            recursive=False,
        )
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        doc = next(d for d in documents if "readme" in d.name.lower())
        assert doc.id is not None
        assert doc.name == "readme.txt"
        assert "Welcome" in doc.text
        assert doc.metadata["source"] == "filesystem"
        assert doc.metadata["extension"] == ".txt"
        assert "path" in doc.metadata

    @pytest.mark.asyncio
    async def test_fetch_recursive_finds_nested_files(self, temp_knowledge_base: Path):
        config = FileSystemConfig(
            root_path=str(temp_knowledge_base),
            recursive=True,
        )
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        names = [d.name for d in documents]
        assert "performance.txt" in names

    @pytest.mark.asyncio
    async def test_fetch_non_recursive_skips_subdirs(self, temp_knowledge_base: Path):
        config = FileSystemConfig(
            root_path=str(temp_knowledge_base),
            recursive=False,
        )
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        names = [d.name for d in documents]
        assert "performance.txt" not in names
        assert "api_guide.txt" not in names

    @pytest.mark.asyncio
    async def test_fetch_extension_filter(self, temp_knowledge_base: Path):
        config = FileSystemConfig(
            root_path=str(temp_knowledge_base),
            extensions={".md"},
        )
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        assert all(d.name.endswith(".md") for d in documents)
        assert len(documents) >= 2

    @pytest.mark.asyncio
    async def test_fetch_skips_unsupported_extensions(self, temp_knowledge_base: Path):
        config = FileSystemConfig(root_path=str(temp_knowledge_base))
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        names = [d.name for d in documents]
        assert "image.png" not in names

    @pytest.mark.asyncio
    async def test_fetch_exclude_pattern(self, temp_knowledge_base: Path):
        config = FileSystemConfig(
            root_path=str(temp_knowledge_base),
            exclude_patterns=[".hidden*"],
        )
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        names = [d.name for d in documents]
        assert ".hidden.txt" not in names

    @pytest.mark.asyncio
    async def test_fetch_max_file_size_skips_large_files(self, tmp_path: Path):
        # Create a file larger than the limit
        large_file = tmp_path / "large.txt"
        large_file.write_text("x" * 200)

        config = FileSystemConfig(
            root_path=str(tmp_path),
            max_file_size_bytes=100,  # 100 bytes limit
        )
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        names = [d.name for d in documents]
        assert "large.txt" not in names

    @pytest.mark.asyncio
    async def test_fetch_empty_directory(self, tmp_path: Path):
        config = FileSystemConfig(root_path=str(tmp_path))
        async with FileSystemConnector(config) as connector:
            documents = await connector.fetch()

        assert documents == []

    @pytest.mark.asyncio
    async def test_fetch_stable_document_ids(self, temp_knowledge_base: Path):
        """Same file always produces the same document ID."""
        config = FileSystemConfig(root_path=str(temp_knowledge_base))
        async with FileSystemConnector(config) as connector:
            docs_first = await connector.fetch()

        async with FileSystemConnector(config) as connector:
            docs_second = await connector.fetch()

        ids_first = {d.id for d in docs_first}
        ids_second = {d.id for d in docs_second}
        assert ids_first == ids_second

    @pytest.mark.asyncio
    async def test_connector_id(self, temp_knowledge_base: Path):
        config = FileSystemConfig(root_path=str(temp_knowledge_base))
        connector = FileSystemConnector(config)
        assert connector.connector_id == "filesystem"

"""Tests for Session 6 — ConnectorIngestionPipeline."""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from app.connectors.connector_registry import KnowledgeConnectorRegistry
from app.connectors.filesystem_connector import FileSystemConnector, FileSystemConfig
from app.document.document import Document
from app.document.ingestion_service import IngestionService
from app.rag.connector_ingestion_pipeline import (
    ConnectorIngestionPipeline,
    IngestionPipelineConfig,
)
from app.search.hybrid_search import HybridSearch
from app.search.search_result import SearchResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_pipeline(
    registry=None,
    ingestion_service=None,
    hybrid_search=None,
):
    registry = registry or KnowledgeConnectorRegistry()
    ingestion_service = ingestion_service or MagicMock(spec=IngestionService)
    if hybrid_search is None:
        hybrid_search = MagicMock(spec=HybridSearch)
        hybrid_search.search = AsyncMock(return_value=[])
    return ConnectorIngestionPipeline(
        registry=registry,
        ingestion_service=ingestion_service,
        hybrid_search=hybrid_search,
    )


def sample_doc(doc_id: str, source: str = "filesystem") -> Document:
    return Document(
        id=doc_id,
        name=f"Doc {doc_id}",
        text=f"Content for document {doc_id}.",
        metadata={"source": source},
    )


def sample_search_result(doc_id: str) -> SearchResult:
    return SearchResult(
        document_id=doc_id,
        text="Some result",
        score=0.9,
        source="vector",
        metadata={},
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestConnectorIngestionPipelineRun:

    async def test_run_returns_result(self):
        pipeline = make_pipeline()
        config = IngestionPipelineConfig(provider="openai")
        result = await pipeline.run(query="test", config=config)
        assert result.results == []
        assert result.documents_ingested == 0
        assert result.chunks_indexed == 0

    async def test_run_searches_and_returns_results(self):
        mock_search = MagicMock(spec=HybridSearch)
        sr = sample_search_result("doc1")
        mock_search.search = AsyncMock(return_value=[sr])

        pipeline = make_pipeline(hybrid_search=mock_search)
        config = IngestionPipelineConfig(provider="openai")
        result = await pipeline.run(query="test query", config=config)

        assert len(result.results) == 1
        assert result.results[0].document_id == "doc1"

    async def test_run_calls_search_with_correct_params(self):
        mock_search = MagicMock(spec=HybridSearch)
        mock_search.search = AsyncMock(return_value=[])

        pipeline = make_pipeline(hybrid_search=mock_search)
        config = IngestionPipelineConfig(
            provider="openai",
            model="text-embedding-3-small",
            top_k=10,
            enable_reranking=False,
        )
        await pipeline.run(query="my query", config=config)

        mock_search.search.assert_called_once_with(
            query="my query",
            provider="openai",
            model="text-embedding-3-small",
            top_k=10,
            enable_reranking=False,
        )

    async def test_run_with_connectors_ingests_documents(self, tmp_path: Path):
        # Create files to ingest
        (tmp_path / "doc1.txt").write_text("Document one content.")
        (tmp_path / "doc2.txt").write_text("Document two content.")

        registry = KnowledgeConnectorRegistry()
        registry.register("filesystem", FileSystemConnector)

        mock_ingestion = MagicMock(spec=IngestionService)
        mock_ingestion.ingest_document = MagicMock(return_value=3)  # 3 chunks each

        mock_search = MagicMock(spec=HybridSearch)
        mock_search.search = AsyncMock(return_value=[])

        pipeline = ConnectorIngestionPipeline(
            registry=registry,
            ingestion_service=mock_ingestion,
            hybrid_search=mock_search,
        )

        config = IngestionPipelineConfig(
            provider="openai",
            connector_configs={
                "filesystem": FileSystemConfig(root_path=str(tmp_path)),
            },
        )
        result = await pipeline.run(query="document content", config=config)

        assert result.documents_ingested == 2
        assert result.chunks_indexed == 6  # 2 docs × 3 chunks
        assert "filesystem" in result.connectors_used
        assert mock_ingestion.ingest_document.call_count == 2


@pytest.mark.asyncio
class TestConnectorIngestionPipelineIngestOnly:

    async def test_ingest_only_returns_no_search_results(self, tmp_path: Path):
        (tmp_path / "file.txt").write_text("content")
        registry = KnowledgeConnectorRegistry()
        registry.register("filesystem", FileSystemConnector)
        mock_ingestion = MagicMock(spec=IngestionService)
        mock_ingestion.ingest_document = MagicMock(return_value=1)

        pipeline = ConnectorIngestionPipeline(
            registry=registry,
            ingestion_service=mock_ingestion,
            hybrid_search=MagicMock(spec=HybridSearch),
        )

        config = IngestionPipelineConfig(
            provider="openai",
            connector_configs={
                "filesystem": FileSystemConfig(root_path=str(tmp_path)),
            },
        )
        result = await pipeline.ingest_only(config)

        assert result.results == []
        assert result.documents_ingested == 1
        assert result.chunks_indexed == 1

    async def test_ingest_only_empty_connectors_returns_zeros(self):
        pipeline = make_pipeline()
        config = IngestionPipelineConfig(provider="openai")
        result = await pipeline.ingest_only(config)
        assert result.results == []
        assert result.documents_ingested == 0
        assert result.chunks_indexed == 0


@pytest.mark.asyncio
class TestConnectorIngestionPipelineSearchOnly:

    async def test_search_only_does_not_call_ingestion(self):
        mock_ingestion = MagicMock(spec=IngestionService)
        mock_search = MagicMock(spec=HybridSearch)
        mock_search.search = AsyncMock(return_value=[sample_search_result("x")])

        pipeline = ConnectorIngestionPipeline(
            registry=KnowledgeConnectorRegistry(),
            ingestion_service=mock_ingestion,
            hybrid_search=mock_search,
        )

        config = IngestionPipelineConfig(
            provider="openai",
            connector_configs={"filesystem": object()},  # Ignored in search_only
        )
        result = await pipeline.search_only(query="hello", config=config)

        assert len(result.results) == 1
        assert result.documents_ingested == 0
        assert result.chunks_indexed == 0
        mock_ingestion.ingest_document.assert_not_called()

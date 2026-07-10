"""
Connector-aware ingestion pipeline.

Orchestrates: KnowledgeConnectors → Documents → Chunks → VectorStore → Search
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.connectors.connector_registry import KnowledgeConnectorRegistry
from app.document.ingestion_service import IngestionService
from app.search.hybrid_search import HybridSearch
from app.search.search_result import SearchResult


@dataclass
class IngestionPipelineConfig:
    """
    Configuration for a connector ingestion + search pipeline run.

    Attributes:
        provider: Embedding provider for ingestion and search
        model: Embedding model name
        connector_configs: Maps connector_id → config object.
                           If empty, skips ingestion (queries existing index).
        top_k: Number of search results to return
        enable_reranking: Apply reranking to search results
    """

    provider: str
    model: str | None = None
    connector_configs: dict[str, object] = field(default_factory=dict)
    top_k: int = 5
    enable_reranking: bool = True


@dataclass
class IngestionPipelineResult:
    """
    Result of a pipeline run.

    Attributes:
        results: Ranked search results (empty when ingest_only=True)
        documents_ingested: Total Document objects fetched from connectors
        chunks_indexed: Total chunks written to the vector store
        connectors_used: Connector IDs that contributed documents
    """

    results: list[SearchResult]
    documents_ingested: int
    chunks_indexed: int
    connectors_used: list[str]


class ConnectorIngestionPipeline:
    """
    End-to-end pipeline that connects knowledge sources to the search index.

    Stages:
    1. **Fetch** — pull Documents from all configured KnowledgeConnectors
    2. **Ingest** — chunk, embed, and store in the vector store
    3. **Search** — hybrid + reranking search over the now-updated index

    The ingestion stage is skipped when no connector_configs are provided,
    allowing the pipeline to serve as a pure search interface over a
    pre-indexed corpus.

    Usage:
        pipeline = ConnectorIngestionPipeline(
            registry=registry,
            ingestion_service=ingestion_service,
            hybrid_search=hybrid_search,
        )

        # Full run: ingest + search
        result = await pipeline.run(
            query="how to deploy the platform",
            config=IngestionPipelineConfig(
                provider="openai",
                connector_configs={
                    "filesystem": FileSystemConfig(root_path="/docs"),
                    "database": DatabaseConfig(...),
                },
            ),
        )

        # Ingest only (pre-indexing, no query)
        result = await pipeline.ingest_only(config)
    """

    def __init__(
        self,
        registry: KnowledgeConnectorRegistry,
        ingestion_service: IngestionService,
        hybrid_search: HybridSearch,
    ):
        self._registry = registry
        self._ingestion_service = ingestion_service
        self._hybrid_search = hybrid_search

    async def run(
        self,
        query: str,
        config: IngestionPipelineConfig,
    ) -> IngestionPipelineResult:
        """
        Ingest from configured connectors, then search.

        Args:
            query: User search query
            config: Pipeline configuration

        Returns:
            IngestionPipelineResult with results and ingestion statistics
        """
        chunks_indexed = 0
        documents_ingested = 0
        connectors_used: list[str] = []

        if config.connector_configs:
            chunks_indexed, documents_ingested, connectors_used = (
                await self._ingest(config)
            )

        results = await self._hybrid_search.search(
            query=query,
            provider=config.provider,
            model=config.model,
            top_k=config.top_k,
            enable_reranking=config.enable_reranking,
        )

        return IngestionPipelineResult(
            results=results,
            documents_ingested=documents_ingested,
            chunks_indexed=chunks_indexed,
            connectors_used=connectors_used,
        )

    async def ingest_only(
        self,
        config: IngestionPipelineConfig,
    ) -> IngestionPipelineResult:
        """
        Run only the ingest stage (useful for pre-indexing jobs).

        Args:
            config: Pipeline configuration

        Returns:
            IngestionPipelineResult with ingestion statistics, empty results
        """
        chunks_indexed = 0
        documents_ingested = 0
        connectors_used: list[str] = []

        if config.connector_configs:
            chunks_indexed, documents_ingested, connectors_used = (
                await self._ingest(config)
            )

        return IngestionPipelineResult(
            results=[],
            documents_ingested=documents_ingested,
            chunks_indexed=chunks_indexed,
            connectors_used=connectors_used,
        )

    async def search_only(
        self,
        query: str,
        config: IngestionPipelineConfig,
    ) -> IngestionPipelineResult:
        """
        Search without ingestion (pure retrieval over existing index).

        Args:
            query: User search query
            config: Pipeline configuration (connector_configs ignored)

        Returns:
            IngestionPipelineResult with results, zero ingestion stats
        """
        results = await self._hybrid_search.search(
            query=query,
            provider=config.provider,
            model=config.model,
            top_k=config.top_k,
            enable_reranking=config.enable_reranking,
        )

        return IngestionPipelineResult(
            results=results,
            documents_ingested=0,
            chunks_indexed=0,
            connectors_used=[],
        )

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    async def _ingest(
        self,
        config: IngestionPipelineConfig,
    ) -> tuple[int, int, list[str]]:
        """
        Fetch from connectors and ingest all documents.

        Returns:
            (chunks_indexed, documents_fetched, connectors_used)
        """
        documents = await self._registry.fetch_all(config.connector_configs)

        total_chunks = 0
        for document in documents:
            chunks = self._ingestion_service.ingest_document(
                document=document,
                provider=config.provider,
                model=config.model,
            )
            total_chunks += chunks

        # Derive connector list from document metadata
        connectors_used = sorted(
            {doc.metadata.get("source", "unknown") for doc in documents}
        )

        return total_chunks, len(documents), connectors_used

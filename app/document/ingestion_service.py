from importlib.resources import path

from app.document.chunker import DocumentChunker
from app.document.loader_factory import LoaderFactory
from app.document.loaders.document_loader import DocumentLoader
from app.vectorstore.vector_service import VectorService


class IngestionService:
    """
    Enterprise Document Ingestion Service.

    Responsibilities
    ----------------
    1. Detect document type.
    2. Load the document.
    3. Chunk the document.
    4. Generate embeddings.
    5. Store chunks in the vector store.
    """

    def __init__(
        self,
        chunker: DocumentChunker,
        vector_service: VectorService,
    ):
        self._chunker = chunker
        self._vector_service = vector_service

    def ingest(
        self,
        path: str,
        provider: str | None = None,
        model: str | None = None,
        
    ) -> int:
        """
        Ingest a document into the vector store.

        Args:
            path:
                File path.

            provider:
                Embedding provider.
                (OpenAI, Gemini, Azure OpenAI...)

            model:
                Optional embedding model.

        Returns
        -------
        Number of indexed chunks.
        """

        #
        # Step 1
        # Select the appropriate loader.
        #

        loader = LoaderFactory.create(path)

        #
        # Step 2
        # Load document.
        #

        document = loader.load(path)

        #
        # Step 3
        # Chunk document.
        #

        chunks = self._chunker.chunk(document)

        #
        # Step 4
        # Index every chunk.
        #

        for chunk in chunks:

            self._vector_service.index(
                document_id=chunk.id,
                text=chunk.text,
                metadata={
                    **chunk.metadata,
                    "document_id": chunk.document_id,
                    "chunk_number": str(chunk.chunk_number),
                    "document_name": document.name,
                },
                provider=provider,
                model=model,
            )
            
            self._keyword_search.add_document(
                {
                    "document_id": chunk.id,
                    "text": chunk.text,
                    "metadata": chunk.metadata,
                }
            )

        #
        # Step 5
        # Return indexed chunk count.
        #

        return len(chunks)
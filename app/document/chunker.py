from app.document.document import Document
from app.document.document_chunk import DocumentChunk
from app.document.paragraph_splitter import ParagraphSplitter
from app.document.sentence_splitter import SentenceSplitter

class DocumentChunker:
    """
    Enterprise Document Chunker.

    Current Strategy
    ----------------
    Character-based chunking with overlap.

    Future Enhancements
    -------------------
    - Paragraph-aware chunking
    - Sentence-aware chunking
    - Token-aware chunking
    - Semantic chunking
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero."
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative."
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:
        """
        Split document into paragraph-aware chunks.
        """

        paragraphs = ParagraphSplitter.split(
            document.text,
        )

        if not paragraphs:
            return []

        chunks: list[DocumentChunk] = []

        current_chunk = ""
        chunk_number = 1

        for paragraph in paragraphs:

            sentences = SentenceSplitter.split(
                paragraph,
            )

            for sentence in sentences:

                candidate = (
                    sentence
                    if not current_chunk
                    else current_chunk + " " + sentence
                )

                #
                # Fits into current chunk
                #

                if len(candidate) <= self.chunk_size:

                    current_chunk = candidate

                    continue

                #
                # Save current chunk
                #

                chunks.append(
                    DocumentChunk(
                        id=f"{document.id}_{chunk_number}",
                        document_id=document.id,
                        chunk_number=chunk_number,
                        text=current_chunk,
                        metadata={
                            **document.metadata,
                            "document_name": document.name,
                        },
                    )
                )

                chunk_number += 1

                current_chunk = sentence

        #
        # Enrich metadata.
        #

        total_chunks = len(chunks)

        for chunk in chunks:

            chunk.metadata["chunk_number"] = str(
                chunk.chunk_number
            )

            chunk.metadata["total_chunks"] = str(
                total_chunks
            )

        return chunks
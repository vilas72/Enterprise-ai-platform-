from app.document.document import Document
from app.document.document_chunk import DocumentChunk


class DocumentChunker:
    """
    Splits documents into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        chunks: list[DocumentChunk] = []

        start = 0
        chunk_number = 1

        while start < len(document.text):

            end = min(
                start + self.chunk_size,
                len(document.text),
            )

            chunk_text = document.text[start:end]

            chunks.append(
                DocumentChunk(
                    id=f"{document.id}_{chunk_number}",
                    document_id=document.id,
                    chunk_number=chunk_number,
                    text=chunk_text,
                    metadata=document.metadata.copy(),
                )
            )

            start += self.chunk_size - self.overlap
            chunk_number += 1

        return chunks 
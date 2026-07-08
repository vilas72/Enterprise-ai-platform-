"""Logic for splitting documents into chunks."""

from __future__ import annotations

from typing import Iterable
from app.rag.chunk import Chunk


class Chunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, document_id: str, metadata: dict[str, str] | None = None) -> list[Chunk]:
        chunks: list[Chunk] = []
        start = 0
        metadata = metadata or {}

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end]
            chunks.append(
                Chunk(
                    id=f"{document_id}-{len(chunks)}",
                    text=chunk_text,
                    metadata=metadata,
                )
            )
            start = max(end - self.overlap, end)

        return chunks

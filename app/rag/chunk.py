"""Defines a document chunk for retrieval."""

from dataclasses import dataclass
from typing import Mapping, Any


@dataclass
class Chunk:
    id: str
    text: str
    metadata: Mapping[str, Any]
    embedding: list[float] | None = None

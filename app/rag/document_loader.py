"""Loads documents for RAG processing."""

from pathlib import Path
from typing import Iterable


class DocumentLoader:
    def load_from_file(self, file_path: str) -> str:
        path = Path(file_path)
        return path.read_text(encoding="utf-8")

    def load_from_files(self, file_paths: Iterable[str]) -> list[str]:
        return [self.load_from_file(path) for path in file_paths]

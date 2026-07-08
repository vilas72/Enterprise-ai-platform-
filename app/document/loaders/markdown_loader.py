from pathlib import Path

from app.document.document import Document
from app.document.loaders.base_loader import BaseLoader


class MarkdownLoader(BaseLoader):
    """
    Loads Markdown files.
    """

    def load(self, path: str) -> Document:
        file = Path(path)
        text = file.read_text(encoding="utf-8")

        return self._build_document(
            str(file),
            text,
            extension=".md",
            document_type="markdown",
        )

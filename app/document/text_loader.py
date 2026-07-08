from pathlib import Path
from unittest import loader

from app.document.document import Document
from app.document.document_loader import DocumentLoader


class TextLoader(DocumentLoader):
    """
    Loads plain text documents.
    """

    def load(
        self,
        path: str,
    ) -> Document:

        file = Path(path)

        return Document(
            id=file.stem,
            name=file.name,
            text=file.read_text(
                encoding="utf-8",
            ),
            metadata={
                "type": "txt",
            },
        )
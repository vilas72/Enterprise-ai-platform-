from pathlib import Path

from app.document.document import Document
from app.document.loaders.document_loader import DocumentLoader


class BaseLoader(DocumentLoader):
    """
    Shared helper logic for simple file-based document loaders.
    """

    def _build_document(
        self,
        path: str,
        text: str,
        *,
        extension: str,
        document_type: str,
    ) -> Document:
        file = Path(path)

        return Document(
            id=file.stem,
            name=file.name,
            text=text,
            metadata={
                "type": document_type,
                "extension": extension,
            },
        )

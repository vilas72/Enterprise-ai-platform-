from pathlib import Path

from app.document.document import Document
from app.document.loaders.document_loader import DocumentLoader


class TextLoader(DocumentLoader):
    """
    Loads plain text files.
    """

    def load(
        self,
        path: str,
    ) -> Document:

        file = Path(path)
        raw_bytes = file.read_bytes()

        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = raw_bytes.decode("utf-16")
            except UnicodeDecodeError:
                text = raw_bytes.decode("utf-8", errors="replace")

        return Document(
            id=file.stem,
            name=file.name,
            text=text,
            metadata={
                "type": "text",
                "extension": file.suffix.lower() or ".txt",
            },
        )
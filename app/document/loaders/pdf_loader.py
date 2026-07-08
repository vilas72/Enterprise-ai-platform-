from pathlib import Path

from pypdf import PdfReader

from app.document.document import Document
from app.document.loaders.document_loader import DocumentLoader


class PdfLoader(DocumentLoader):
    """
    Loads PDF documents.

    Responsibilities
    ----------------
    - Read PDF
    - Extract text
    - Build Document model
    """

    def load(
        self,
        path: str,
    ) -> Document:
        """
        Load a PDF document.
        """

        file = Path(path)

        reader = PdfReader(file)

        pages: list[str] = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        document_text = "\n\n".join(pages)

        return Document(
            id=file.stem,
            name=file.name,
            text=document_text,
            metadata={
                "type": "pdf",
                "extension": ".pdf",
                "pages": str(len(reader.pages)),
            },
        )
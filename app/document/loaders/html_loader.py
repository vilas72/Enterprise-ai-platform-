from pathlib import Path

from bs4 import BeautifulSoup

from app.document.document import Document
from app.document.loaders.document_loader import DocumentLoader


class HtmlLoader(DocumentLoader):
    """
    Loads HTML documents.

    Extracts readable text while removing HTML tags,
    scripts and styles.
    """

    def load(
        self,
        path: str,
    ) -> Document:

        file = Path(path)

        html = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        #
        # Remove unwanted elements.
        #

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True,
        )

        return Document(
            id=file.stem,
            name=file.name,
            text=text,
            metadata={
                "document_type": "html",
                "extension": ".html",
                "source": file.name,
            },
        )
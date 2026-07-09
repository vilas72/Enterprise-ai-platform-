from pathlib import Path

from app.document.loaders.document_loader import DocumentLoader
from app.document.loaders.text_loader import TextLoader
from app.document.loaders.pdf_loader import PdfLoader
from app.document.loaders.docx_loader import DocxLoader
from app.document.loaders.markdown_loader import MarkdownLoader
from app.document.loaders.csv_loader import CsvLoader
from app.document.loaders.html_loader import HtmlLoader


class LoaderFactory:

    _loaders = {
        ".txt": TextLoader,
        ".pdf": PdfLoader,
        ".docx": DocxLoader,
        ".md": MarkdownLoader,
        ".csv": CsvLoader,
        ".html": HtmlLoader,
        "htm": HtmlLoader,
    }

    @classmethod
    def create(
        cls,
        file_path: str,
    ) -> DocumentLoader:

        extension = Path(file_path).suffix.lower()

        print("Extension:", extension)

        loader = cls._loaders.get(extension)

        print("Loader:", loader)

        if loader is None:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loader()
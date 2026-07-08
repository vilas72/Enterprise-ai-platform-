from pathlib import Path

from app.document.loaders.document_loader import DocumentLoader
from app.document.loaders.text_loader import TextLoader
from app.document.loaders.pdf_loader import PdfLoader


class LoaderFactory:

    _loaders = {
        ".txt": TextLoader,
        ".pdf": PdfLoader,
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
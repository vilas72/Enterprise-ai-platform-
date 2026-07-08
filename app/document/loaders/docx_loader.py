from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET

from app.document.document import Document
from app.document.loaders.base_loader import BaseLoader


class DocxLoader(BaseLoader):
    """
    Loads Microsoft Word DOCX files.
    """

    def load(self, path: str) -> Document:
        file = Path(path)

        with zipfile.ZipFile(file) as archive:
            document_xml = archive.read("word/document.xml")

        root = ET.fromstring(document_xml)
        namespace = {
            "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        }

        paragraphs: list[str] = []
        for paragraph in root.findall(".//w:p", namespace):
            texts = [
                node.text or ""
                for node in paragraph.findall(".//w:t", namespace)
            ]
            if texts:
                paragraphs.append("".join(texts))

        text = "\n".join(paragraphs)

        return self._build_document(
            str(file),
            text,
            extension=".docx",
            document_type="docx",
        )

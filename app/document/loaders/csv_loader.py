import csv
from pathlib import Path

from app.document.document import Document
from app.document.loaders.document_loader import DocumentLoader


class CsvLoader(DocumentLoader):
    """
    Loads CSV documents.

    Each row is converted into a readable sentence so that
    embeddings capture the meaning of each record.
    """

    def load(
        self,
        path: str,
    ) -> Document:

        file = Path(path)

        rows = []

        with open(
            file,
            newline="",
            encoding="utf-8",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for index, row in enumerate(reader, start=1):

                values = []

                for key, value in row.items():

                    if value is None:
                        continue

                    value = value.strip()

                    if value:

                        values.append(
                            f"{key}: {value}"
                        )

                if values:

                    rows.append(
                        f"Row {index}\n" +
                        "\n".join(values)
                    )

        document_text = "\n\n--------------------\n\n".join(rows)

        return Document(
            id=file.stem,
            name=file.name,
            text=document_text,
            metadata={
                "document_type": "csv",
                "extension": ".csv",
                "rows": str(len(rows)),
                "source": file.name,
            },
        )
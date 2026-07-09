import re


class ParagraphSplitter:
    """
    Splits text into paragraphs.

    Empty paragraphs are ignored.
    """

    @staticmethod
    def split(
        text: str,
    ) -> list[str]:

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            paragraph.strip()
            for paragraph in paragraphs
            if paragraph.strip()
        ]
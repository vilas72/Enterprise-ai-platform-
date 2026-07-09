import re


class SentenceSplitter:
    """
    Splits a paragraph into sentences.

    Future enhancements:
    - NLP-based splitting (spaCy)
    - Language detection
    """

    SENTENCE_PATTERN = re.compile(
        r'(?<=[.!?])\s+'
    )

    @classmethod
    def split(
        cls,
        paragraph: str,
    ) -> list[str]:

        if not paragraph.strip():
            return []

        return [
            sentence.strip()
            for sentence in cls.SENTENCE_PATTERN.split(paragraph)
            if sentence.strip()
        ]
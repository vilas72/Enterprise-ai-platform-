from abc import ABC, abstractmethod

from app.document.document import Document


class DocumentLoader(ABC):
    """
    Base class for all document loaders.
    """

    @abstractmethod
    def load(
        self,
        path: str,
    ) -> Document:
        """
        Load a document.
        """
        pass
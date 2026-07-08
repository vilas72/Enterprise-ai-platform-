from app.vectorstore.similarity import Similarity
from app.vectorstore.vector_document import VectorDocument
from app.vectorstore.vector_search_result import VectorSearchResult
from app.vectorstore.vector_store import VectorStore


class InMemoryVectorStore(VectorStore):
    """
    Simple in-memory vector store.

    Intended for development and testing.
    """

    def __init__(self):

        self._documents: dict[str, VectorDocument] = {}

    def index(
        self,
        document: VectorDocument,
    ) -> None:

        self._documents[document.id] = document

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:

        results: list[VectorSearchResult] = []

        for document in self._documents.values():

            score = Similarity.cosine_similarity(
                embedding,
                document.embedding,
            )

            results.append(
                VectorSearchResult(
                    document=document,
                    score=score,
                )
            )

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:top_k]

    def delete(
        self,
        document_id: str,
    ) -> None:

        self._documents.pop(
            document_id,
            None,
        )

    def clear(
        self,
    ) -> None:

        self._documents.clear()

    def count(
        self,
    ) -> int:

        return len(self._documents)
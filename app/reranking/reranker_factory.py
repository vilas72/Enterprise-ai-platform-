from __future__ import annotations

from collections.abc import Callable

from app.reranking.noop_reranker import NoOpReranker
from app.reranking.reranker import Reranker


class RerankerFactory:
    """
    Factory responsible for creating reranker instances.

    The registry-based design allows new rerankers to be added
    without modifying the factory implementation.
    """

    def __init__(self) -> None:

        self._registry: dict[
            str,
            Callable[[], Reranker],
        ] = {
            "noop": NoOpReranker,
        }

    def register(
        self,
        name: str,
        factory: Callable[[], Reranker],
    ) -> None:
        """
        Register a reranker implementation.
        """

        self._registry[name] = factory

    def create(
        self,
        reranker_type: str = "noop",
    ) -> Reranker:
        """
        Create a reranker instance.
        """

        try:
            return self._registry[reranker_type]()

        except KeyError as exc:

            supported = ", ".join(
                sorted(self._registry)
            )

            raise ValueError(
                f"Unsupported reranker "
                f"'{reranker_type}'. "
                f"Supported: {supported}"
            ) from exc
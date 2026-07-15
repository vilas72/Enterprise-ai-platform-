"""Knowledge runtime exceptions."""


class KnowledgeRuntimeError(Exception):
    """Base Knowledge Runtime exception."""


class KnowledgeSearchError(KnowledgeRuntimeError):
    """Raised when enterprise knowledge search fails."""


class KnowledgeRetrievalError(KnowledgeRuntimeError):
    """Raised when retrieval pipeline execution fails."""


class KnowledgeGenerationError(KnowledgeRuntimeError):
    """Raised when AI answer generation fails."""

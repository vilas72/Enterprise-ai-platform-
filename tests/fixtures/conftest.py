"""Test fixtures for pytest."""

import pytest
from app.conversation.in_memory_store import InMemoryConversationStore
from app.conversation.session import ConversationSession
from app.domain.models.chat_message import ChatMessage
from app.search.keyword_search import KeywordSearch
from app.vectorstore.in_memory_vector_store import InMemoryVectorStore
from app.vectorstore.vector_service import VectorService
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.embedding_factory import EmbeddingFactory
from app.rag.retrieved_document import RetrievedDocument


@pytest.fixture
def sample_conversation_session() -> ConversationSession:
    """Create a sample conversation session."""
    session = ConversationSession()
    session.add_message(
        ChatMessage(
            conversation_id=session.session_id,
            role="user",
            content="What is Python?",
        )
    )
    session.add_message(
        ChatMessage(
            conversation_id=session.session_id,
            role="assistant",
            content="Python is a programming language.",
        )
    )
    return session


@pytest.fixture
def conversation_store() -> InMemoryConversationStore:
    """Create an in-memory conversation store."""
    return InMemoryConversationStore()


@pytest.fixture
def vector_service() -> VectorService:
    """Create a vector service with in-memory store."""
    store = InMemoryVectorStore()
    embedding_factory = EmbeddingFactory()
    embedding_service = EmbeddingService(embedding_factory=embedding_factory)
    return VectorService(
        embedding_service=embedding_service, vector_store=store
    )


@pytest.fixture
def keyword_search() -> KeywordSearch:
    """Create a keyword search instance."""
    search = KeywordSearch()
    # Index sample documents
    documents = [
        {"id": "1", "text": "Python is a programming language"},
        {"id": "2", "text": "JavaScript is used for web development"},
        {"id": "3", "text": "Database management systems store data"},
    ]
    search.index(documents)
    return search


@pytest.fixture
def sample_retrieved_documents() -> list[RetrievedDocument]:
    """Create sample retrieved documents."""
    return [
        RetrievedDocument(
            id="doc1",
            text="Python is a high-level programming language.",
            score=0.95,
            metadata={"source": "wiki", "category": "programming"},
        ),
        RetrievedDocument(
            id="doc2",
            text="Python supports multiple programming paradigms.",
            score=0.87,
            metadata={"source": "docs", "category": "programming"},
        ),
        RetrievedDocument(
            id="doc3",
            text="Python has a large standard library.",
            score=0.72,
            metadata={"source": "tutorial", "category": "libraries"},
        ),
    ]

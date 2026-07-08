from app.bootstrap.provider_bootstrap import register_providers
from app.providers.provider_factory import ProviderFactory
from app.services.ai_service import AIService
from app.conversation.conversation_manager import ConversationManager
from app.conversation.in_memory_store import InMemoryConversationStore

from app.prompt.file_prompt_repository import FilePromptRepository
from app.prompt.prompt_service import PromptService

from app.tracking.in_memory_usage_tracker import InMemoryUsageTracker

from app.conversation.conversation_memory_manager import ConversationMemoryManager

from app.embeddings.embedding_factory import EmbeddingFactory
from app.embeddings.embedding_service import EmbeddingService

from app.vectorstore.in_memory_vector_store import InMemoryVectorStore
from app.vectorstore.vector_service import VectorService

from app.rag.rag_service import RagService

from app.document.chunker import DocumentChunker
from app.document.ingestion_service import IngestionService
from app.document.text_loader import TextLoader


# Register providers once when this module is imported
register_providers()

_provider_factory = ProviderFactory()
_ai_service = AIService(_provider_factory, usage_tracker=InMemoryUsageTracker(), prompt_service=PromptService(repository=FilePromptRepository()))   

usage_tracker = InMemoryUsageTracker()


#
# Conversation Services
#

conversation_store = InMemoryConversationStore()

conversation_manager = ConversationManager(
    conversation_store=conversation_store,
    memory_manager=ConversationMemoryManager,    
)

embedding_factory = EmbeddingFactory()
embedding_service = EmbeddingService(
    embedding_factory=embedding_factory
)


prompt_repository = FilePromptRepository()

prompt_service = PromptService(
    repository=prompt_repository,
)

_vector_store = InMemoryVectorStore()

_vector_service = VectorService(
    embedding_service=embedding_service,
    vector_store=_vector_store,
)

_rag_service = RagService(
    vector_service=_vector_service,
    ai_service=_ai_service,
)   

_document_loader = TextLoader()
_document_chunker  = DocumentChunker()
_ingestion_service = IngestionService(
    loader=_document_loader,
    chunker=_document_chunker ,
    vector_service=_vector_service,
)

def get_ai_service() -> AIService:
    """
    FastAPI dependency that returns the singleton AIService.
    """
    return _ai_service

def get_conversation_manager() -> ConversationManager:
    """
    Returns the singleton ConversationManager.
    """
    return conversation_manager

def get_usage_tracker() -> InMemoryUsageTracker:
    return usage_tracker

def get_prompt_service() -> PromptService:
    """
    Returns the singleton PromptService.
    """
    return prompt_service

def get_embedding_service() -> EmbeddingService:
    return embedding_service

def get_vector_service() -> VectorService:
    return _vector_service

def get_rag_service() -> RagService:
    return _rag_service

def get_ingestion_service() -> IngestionService:
    return _ingestion_service
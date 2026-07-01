from app.bootstrap.provider_bootstrap import register_providers
from app.providers.provider_factory import ProviderFactory
from app.services.ai_service import AIService
from app.conversation.conversation_manager import ConversationManager
from app.conversation.in_memory_store import InMemoryConversationStore

# Register providers once when this module is imported
register_providers()

_provider_factory = ProviderFactory()
_ai_service = AIService(_provider_factory)

#
# Conversation Services
#

conversation_store = InMemoryConversationStore()

conversation_manager = ConversationManager(
    conversation_store=conversation_store,
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
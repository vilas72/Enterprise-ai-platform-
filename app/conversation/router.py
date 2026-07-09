from fastapi import APIRouter, HTTPException

from app.conversation.conversation_message import ConversationMessage
from app.conversation.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])
service = ConversationService()


@router.post("", status_code=201)
def create_conversation(conversation_id: str | None = None) -> dict[str, object]:
    conversation_id = conversation_id or "default"
    conversation = service.create(conversation_id)
    return {"conversation_id": conversation.id, "messages": conversation.messages}


@router.get("/{conversation_id}")
def get_conversation(conversation_id: str) -> dict[str, object]:
    conversation = service.get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"conversation_id": conversation.id, "messages": conversation.messages}


@router.post("/{conversation_id}/messages")
def add_message(conversation_id: str, message: ConversationMessage) -> dict[str, object]:
    conversation = service.add_message(conversation_id, message)
    return {"conversation_id": conversation.id, "messages": conversation.messages}

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.chat_message_api import ChatMessageApi
from app.api.schemas.conversation.chat_request import ChatRequest
from app.api.schemas.conversation.chat_response import ChatResponse
from app.api.schemas.conversation.conversation_response import (
    ConversationResponse,
)
from app.api.schemas.conversation.create_session_response import (
    CreateSessionResponse,
)
from app.conversation.conversation_manager import ConversationManager
from app.dependencies.service_dependencies import (
    get_ai_service,
    get_conversation_manager,
)
from app.domain.generate_request import GenerateRequest
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation"],
)


@router.post(
    "",
    response_model=CreateSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_session(
    conversation_manager: ConversationManager = Depends(
        get_conversation_manager
    ),
):

    conversation = await conversation_manager.create_session()

    return CreateSessionResponse(
        session_id=conversation.conversation_id,
    )


@router.get(
    "/{session_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    session_id: str,
    conversation_manager: ConversationManager = Depends(
        get_conversation_manager
    ),
):

    conversation = await conversation_manager.get_session(session_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return ConversationResponse(
        session_id=conversation.conversation_id,
        messages=[
            ChatMessageApi(
                role=message.role.value,
                content=message.content,
            )
            for message in conversation.messages
        ],
    )


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    session_id: str,
    conversation_manager: ConversationManager = Depends(
        get_conversation_manager
    ),
):

    conversation = await conversation_manager.get_session(session_id)
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    await conversation_manager.delete_session(session_id)


@router.post(
    "/{session_id}/chat",
    response_model=ChatResponse,
)
async def chat(
    session_id: str,
    request: ChatRequest,
    conversation_manager: ConversationManager = Depends(
        get_conversation_manager
    ),
    ai_service: AIService = Depends(
        get_ai_service
    ),
):

    conversation = await conversation_manager.get_session(session_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    #
    # Add user message
    #

    await conversation_manager.add_user_message(
        conversation,
        request.message,
    )

    #
    # Build AI request
    #

    generate_request = GenerateRequest(
        provider=request.provider,
        model=request.model,
        messages=[
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in conversation.messages
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    #
    # Call AI
    #

    response = ai_service.generate(generate_request)

    #
    # Save assistant response
    #

    await conversation_manager.add_assistant_message(
        conversation,
        response.response,
    )

    return ChatResponse(
        session_id=conversation.conversation_id,
        provider=response.provider,
        model=response.model,
        response=response.response,
    )
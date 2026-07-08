from fastapi import APIRouter, Depends

from app.api.schemas.rag.rag_request_api import RagRequestApi
from app.api.schemas.rag.rag_response_api import RagResponseApi

from app.dependencies.service_dependencies import (
    get_rag_service,
)

from app.mappers.rag_mapper import RagMapper

from app.rag.rag_service import RagService

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/ask",
    response_model=RagResponseApi,
)
def ask(
    request: RagRequestApi,
    rag_service: RagService = Depends(
        get_rag_service,
    ),
):

    response = rag_service.ask(
        RagMapper.to_domain(request),
    )

    return RagMapper.to_api(
        response,
    )
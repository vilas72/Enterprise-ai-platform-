from fastapi import APIRouter, Depends

from app.api.schemas.vector.index_request import IndexRequest
from app.api.schemas.vector.index_response import IndexResponse
from app.api.schemas.vector.search_request import SearchRequest
from app.api.schemas.vector.search_response import SearchResponse
from app.api.schemas.vector.search_result import SearchResult

from app.dependencies.service_dependencies import get_vector_service

from app.vectorstore.vector_service import VectorService

router = APIRouter(
    prefix="/vectors",
    tags=["Vector Store"],
)

@router.post(
    "",
    response_model=IndexResponse,
)
def index_document(
    request: IndexRequest,
    vector_service: VectorService = Depends(
        get_vector_service,
    ),
):

    document_id = vector_service.index(
        document_id=request.document_id,
        text=request.text,
        metadata=request.metadata,
        provider=request.provider,
        model=request.model,
    )

    return IndexResponse(
        document_id=document_id,
        message="Document indexed successfully.",
    )

@router.post(
    "/search",
    response_model=SearchResponse,
)
def search(
    request: SearchRequest,
    vector_service: VectorService = Depends(
        get_vector_service,
    ),
):

    results = vector_service.search(
        query=request.query,
        top_k=request.top_k,
        provider=request.provider,
        model=request.model,
    )

    return SearchResponse(
        total=len(results),
        results=[
            SearchResult(
                document_id=result.document.id,
                text=result.document.text,
                metadata=result.document.metadata,
                score=result.score,
            )
            for result in results
        ],
    )

@router.delete(
    "/{document_id}",
)
def delete(
    document_id: str,
    vector_service: VectorService = Depends(
        get_vector_service,
    ),
):

    vector_service.delete(document_id)

    return {
        "message": "Document deleted successfully.",
    }

@router.delete(
    "",
)
def clear(
    vector_service: VectorService = Depends(
        get_vector_service,
    ),
):

    vector_service.clear()

    return {
        "message": "Vector store cleared successfully.",
    }
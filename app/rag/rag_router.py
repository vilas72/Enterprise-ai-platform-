from fastapi import APIRouter, Depends

from app.dependencies.service_dependencies import get_vector_service, get_embedding_service
from app.rag.rag_request import RAGRequest
from app.rag.rag_response import RAGResponse
from app.rag.rag_service import RAGService
from app.vectorstore.vector_service import VectorService
from app.embeddings.embedding_service import EmbeddingService

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "",
    response_model=RAGResponse,
)
def run_rag(
    request: RAGRequest,
    vector_service: VectorService = Depends(get_vector_service),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> RAGResponse:
    service = RAGService(
        vector_service=vector_service,
        embedding_service=embedding_service,
    )

    return service.retrieve_and_generate(request)

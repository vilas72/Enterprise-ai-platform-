from fastapi import APIRouter, Depends

from app.api.schemas.embedding.embedding_request_api import (
    EmbeddingRequestApi,
)
from app.api.schemas.embedding.embedding_response_api import (
    EmbeddingResponseApi,
)
from app.dependencies.service_dependencies import (
    get_embedding_service,
)
from app.embeddings.embedding_service import (
    EmbeddingService,
)
from app.mappers.embedding_mapper import (
    EmbeddingMapper,
)

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"],
)


@router.post(
    "",
    response_model=EmbeddingResponseApi,
)
def generate_embedding(
    request: EmbeddingRequestApi,
    embedding_service: EmbeddingService = Depends(
        get_embedding_service,
    ),
):

    domain_request = EmbeddingMapper.to_domain(
        request,
    )

    response = embedding_service.generate(
        domain_request,
    )

    return EmbeddingMapper.to_api(
        response,
    )
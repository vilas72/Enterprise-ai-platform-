from app.api.schemas.rag.rag_request_api import RagRequestApi
from app.api.schemas.rag.rag_response_api import RagResponseApi
from app.api.schemas.rag.source_api import SourceApi

from app.rag.rag_request import RagRequest
from app.rag.rag_response import RagResponse


class RagMapper:

    @staticmethod
    def to_domain(
        request: RagRequestApi,
    ) -> RagRequest:

        return RagRequest(
            question=request.question,
            provider=request.provider,
            model=request.model,
            top_k=request.top_k,
        )

    @staticmethod
    def to_api(
        response: RagResponse,
    ) -> RagResponseApi:

        return RagResponseApi(
            answer=response.answer,
            sources=[
                SourceApi(
                    id=source.id,
                    text=source.text,
                    score=source.score,
                    metadata=source.metadata,
                )
                for source in response.sources
            ],
        )
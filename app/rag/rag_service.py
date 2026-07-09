from app.domain.generate_request import GenerateRequest
from app.domain.models.chat_message import ChatMessage

from app.rag.context_builder import ContextBuilder
from app.rag.rag_request import RagRequest
from app.rag.rag_response import RagResponse
from app.rag.retrieved_document import RetrievedDocument

from app.services.ai_service import AIService
from app.vectorstore.vector_service import VectorService


class RagService:
    """
    Retrieval Augmented Generation (RAG) Service.

    Workflow

    User Question
            │
            ▼
    Vector Search
            │
            ▼
    Retrieved Documents
            │
            ▼
    Context Builder
            │
            ▼
    Generate Prompt
            │
            ▼
    AI Service
            │
            ▼
    Final Answer
    """

    def __init__(
        self,
        vector_service: VectorService,
        ai_service: AIService,
    ):
        self._vector_service = vector_service
        self._ai_service = ai_service

    def ask(
        self,
        request: RagRequest,
    ) -> RagResponse:
        """
        Execute a RAG query.
        """

        #
        # Step 1
        # Retrieve relevant documents
        #

        search_results = self._hybrid_search.search(
            query=request.question,
            provider=request.provider,
            model=request.model,
            top_k=request.top_k,
        )

        #
        # Step 2
        # Convert results
        #

        documents: list[RetrievedDocument] = []

        for result in search_results:

            documents.append(
                RetrievedDocument(
                    id=result.document.id,
                    text=result.document.text,
                    score=result.score,
                    metadata=result.document.metadata,
                )
            )

        #
        # Step 3
        # No context found
        #

        if not documents:

            return RagResponse(
                answer="I couldn't find any relevant information in the knowledge base.",
                sources=[],
            )

        #
        # Step 4
        # Build Context
        #

        context = ContextBuilder.build(documents)

        #
        # Step 5
        # Build Prompt
        #

        prompt = f"""
You are an Enterprise AI Assistant.

Answer ONLY using the supplied context.

If the answer is not present in the context,
reply exactly:

"I couldn't find that information in the knowledge base."

======================
CONTEXT
======================

{context}

======================
QUESTION
======================

{request.question}
"""

        #
        # Step 6
        # Build GenerateRequest
        #

        generate_request = GenerateRequest(
            provider=request.provider,
            model=None,
            temperature=0.2,
            max_tokens=50,          # <----- IMPORTANT
            messages=[
                ChatMessage(
                    role="user",
                    content=prompt,
                )
            ],
        )

       
        #
        # Step 7
        # Ask LLM
        #

        response = self._ai_service.generate(
            generate_request,
        )

        #
        # Step 8
        # Return
        #

        return RagResponse(
            answer=response.response,
            sources=documents,
        )
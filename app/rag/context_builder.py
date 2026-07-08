from app.rag.retrieved_document import RetrievedDocument


class ContextBuilder:
    """
    Builds the context supplied to the LLM
    from retrieved documents.
    """

    @staticmethod
    def build(
        documents: list[RetrievedDocument],
    ) -> str:
        """
        Build a formatted context.
        """

        if not documents:
            return "No relevant context found."

        context_parts: list[str] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            context_parts.append(
                f"""
Document {index}

Score:
{document.score:.4f}

Content:
{document.text[:1000]}
""".strip()
            )

        return "\n\n------------------------\n\n".join(
            context_parts
        )
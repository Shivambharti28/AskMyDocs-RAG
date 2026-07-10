import logfire

from app.services.retrieval.qdrant_service import search
from app.services.retrieval.prompt_builder import build_prompt
from app.services.retrieval.llm_service import generate_answer
from app.services.retrieval.post_processing import deduplicate_chunks

def ask(question: str) -> dict:
    """
    Complete Enterprise RAG pipeline.

    Flow:
        User Question
              ↓
        Vector Search (Qdrant)
              ↓
        Prompt Builder
              ↓
        Gemini
              ↓
        Final Answer

    Returns:
        {
            "answer": str,
            "sources": list
        }
    """

    with logfire.span(
        "🚀 Enterprise RAG Pipeline",
        question=question,
    ):

        try:

            logfire.info(
                "Searching knowledge base",
                question=question,
            )

            # retrieved_chunks = search(question)
            retrieved_chunks = search(
                query=question,
                limit=5,
            )

            retrieved_chunks = deduplicate_chunks(
                retrieved_chunks
            )

            logfire.info(
                "Retrieval completed",
                retrieved_chunks=len(retrieved_chunks),
            )

            if not retrieved_chunks:
                logfire.warning(
                    "No relevant documents found."
                )

                return {
                    "answer": (
                        "I couldn't find any relevant information "
                        "in the knowledge base."
                    ),
                    "sources": [],
                }

            logfire.info("Building prompt")

            prompt = build_prompt(
                question=question,
                retrieved_chunks=retrieved_chunks,
            )

            logfire.info("Generating answer")

            answer = generate_answer(prompt)

            logfire.info(
                "Pipeline completed successfully",
                answer_length=len(answer),
            )

            return {
                "answer": answer,
                "sources": retrieved_chunks,
            }

        except Exception as e:

            logfire.error(
                "RAG Pipeline Failed",
                error=str(e),
            )

            return {
                "answer": (
                    "An unexpected error occurred while "
                    "processing your request."
                ),
                "sources": [],
            }
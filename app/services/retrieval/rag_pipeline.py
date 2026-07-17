import logfire
import traceback
from app.services.retrieval.prompt_builder import build_prompt
from app.services.retrieval.llm_service import generate_answer
from app.services.retrieval.post_processing import (deduplicate_chunks,merge_adjacent_chunks,)
from app.services.retrieval.hybrid_search import hybrid_search
from app.services.retrieval.reranker import rerank_chunks
from app.services.retrieval.context_compression import compress_chunks


def ask(
    question: str,
    source: str | None = None,
    page: int | None = None,
):

    with logfire.span("🚀 Enterprise RAG Pipeline",question=question):
        try:

            logfire.info(
                "Searching knowledge base",
                question=question,
            )

            retrieved_chunks = hybrid_search(
                query=question,
                limit=5,
                source=source,
                page=page,
            )

            if not retrieved_chunks:
                logfire.warning("No relevant documents found.")

                return {
                    "answer": (
                        "I couldn't find any relevant information "
                        "in the knowledge base."
                    ),
                    "sources": [],
                }

            retrieved_chunks = deduplicate_chunks(
                retrieved_chunks
            )
            retrieved_chunks = merge_adjacent_chunks(
                retrieved_chunks
            )
            retrieved_chunks = rerank_chunks(
                question=question,
                chunks=retrieved_chunks,
                top_k=5,
            )
            logfire.info("Compressing retrieved context")

            retrieved_chunks = compress_chunks(
                question=question,
                chunks=retrieved_chunks,
            )

            logfire.info("Context compression completed",chunks=len(retrieved_chunks),)
            logfire.info("Retrieval completed",retrieved_chunks=len(retrieved_chunks),)
            logfire.info("Building prompt")
            prompt = build_prompt(
                question=question,
                retrieved_chunks=retrieved_chunks,
            )
            logfire.info("Generating answer")
            answer = generate_answer(
                prompt
            )
            logfire.info("Pipeline completed successfully",answer_length=len(answer))
            return {
                "answer": answer,
                "sources": retrieved_chunks,
            }

        except Exception as e:

            traceback.print_exc()

            logfire.error("RAG Pipeline Failed",error=str(e),)
            return {
                "answer": (
                    "An unexpected error occurred while "
                    "processing your request."
                ),
                "sources": [],
            }
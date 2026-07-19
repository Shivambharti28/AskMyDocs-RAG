import logfire
import traceback
from app.services.retrieval.prompt_builder import build_prompt
from app.services.retrieval.llm_service import generate_answer
from app.services.retrieval.post_processing import (deduplicate_chunks,merge_adjacent_chunks,)
from app.services.retrieval.hybrid_search import hybrid_search
from app.services.retrieval.reranker import rerank_chunks
from app.services.retrieval.context_compression import compress_chunks
from app.services.conversation.memory import ConversationMemory
from app.services.retrieval.confidence import calculate_confidence

conversation_memory = ConversationMemory()


def ask(question: str,source: str | None = None,page: int | None = None,):

    with logfire.span("🚀 Enterprise RAG Pipeline",question=question):
        try:

            logfire.info(
                "Searching knowledge base",
                question=question,
            )

            retrieved_chunks = hybrid_search(
                query=question,
                conversation_history=conversation_memory.get_history(),
                limit = 5,
                source=source,
                page=page,
            )

            if not retrieved_chunks:
                logfire.warning("No relevant documents found.")

                return {
                    "answer": (
                        "I couldn't find this information in the provided documents."
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

            confidence = calculate_confidence(retrieved_chunks)

            print("\n===== CONFIDENCE =====")
            print(f"Level   : {confidence['level']}")
            print(f"Score   : {confidence['score']}%")
            print(f"Top     : {confidence['top_score']}")
            print(f"Average : {confidence['average_score']}")
            print("======================\n")

            logfire.info("Context compression completed",chunks=len(retrieved_chunks),)
            logfire.info("Retrieval completed",retrieved_chunks=len(retrieved_chunks),)
            logfire.info("Building prompt")
            prompt = build_prompt(
                question=question,
                retrieved_chunks=retrieved_chunks,
                conversation_history=conversation_memory.get_history(),
            )
            logfire.info("Generating answer")
            answer = generate_answer(prompt)
            conversation_memory.add_user_message(question)
            conversation_memory.add_assistant_message(answer)
            print("\n===== Conversation History =====")
            for message in conversation_memory.get_history():
                print(f"{message['role'].upper()}: "
                      f"{message['content']}"
                )
            logfire.info("Pipeline completed successfully",answer_length=len(answer))
            return {
                "answer": answer,
                "sources": retrieved_chunks,
                "confidence": confidence,
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
import traceback
import time
import logfire

from app.services.conversation.memory import ConversationMemory
from app.services.retrieval.confidence import calculate_confidence
from app.services.retrieval.context_compression import compress_chunks
from app.services.retrieval.hybrid_search import hybrid_search
from app.services.retrieval.llm_service import generate_answer
from app.services.retrieval.post_processing import (deduplicate_chunks,merge_adjacent_chunks)
from app.services.retrieval.prompt_builder import build_prompt
from app.services.retrieval.reranker import rerank_chunks
from app.services.retrieval.query_rewriter import rewrite_query

MIN_RERANK_SCORE = 0.0
conversation_memory = ConversationMemory()

def empty_response(timings: dict):
    return {
        "answer": (
            "I couldn't find this information in the provided documents."
        ),
        "sources": [],
        "confidence": {
            "level": "LOW",
            "score": 0,
            "top_score": 0,
            "average_score": 0,
        },
        "timings": timings,
    }

def build_retrieval_debug(chunks):

    retrieval_debug = []

    for rank, chunk in enumerate(chunks, start=1):
        retrieval_debug.append(
            {
                "rank": rank,
                "page": chunk.get("page"),
                "source": chunk.get("source"),
                "vector_score": chunk.get("score"),
                "bm25_score": chunk.get("bm25_score"),
                "rrf_score": chunk.get("rrf_score"),
                "rerank_score": chunk.get("rerank_score"),
            }
        )

    return retrieval_debug

def ask(
    question: str,
    source: str | None = None,
    page: int | None = None,
    verbose: bool = True,
):

    with logfire.span("🚀 Enterprise RAG Pipeline", question=question):
        try:
            pipeline_start = time.perf_counter()
            timings = {}

            logfire.info(
                "Searching knowledge base",
                question=question,
            )
            start = time.perf_counter()

            rewritten_question = rewrite_query(
                question,
                conversation_memory.get_history(),
                verbose=verbose,
            )

            retrieved_chunks = hybrid_search(
                query=rewritten_question,
                conversation_history=conversation_memory.get_history(),
                limit=5,
                source=source,
                page=page,
                verbose=verbose,
            )
            timings["Hybrid Search"] = time.perf_counter() - start

            if verbose:
                print("\n===== AFTER HYBRID SEARCH =====")
                for c in retrieved_chunks:
                    print(
                        f"Page={c['page']}",
                        f"score={c.get('score')}",
                        f"bm25={c.get('bm25_score')}",
                        f"rrf={c.get('rrf_score')}",
                        f"rerank={c.get('rerank_score')}",
                    )



            if not retrieved_chunks:
                timings["Total"] = time.perf_counter() - pipeline_start
                logfire.warning("No relevant documents found.")

                return empty_response(timings)

            start = time.perf_counter()

            retrieved_chunks = deduplicate_chunks(retrieved_chunks)
            retrieved_chunks = merge_adjacent_chunks(retrieved_chunks)

            timings["Post Processing"] = time.perf_counter() - start

            start = time.perf_counter()

            retrieved_chunks = rerank_chunks(
                question=rewritten_question,
                chunks=retrieved_chunks,
                top_k=5,
            )

            timings["Reranking"] = time.perf_counter() - start

            # Remove chunks that are not relevant enough
            

            retrieved_chunks = [
                chunk
                for chunk in retrieved_chunks
                if chunk.get("rerank_score", float("-inf")) >= MIN_RERANK_SCORE
            ]

            if not retrieved_chunks:
                timings["Total"] = time.perf_counter() - pipeline_start


                logfire.warning("No relevant chunks after reranking.")

                return empty_response(timings)
            
            if verbose:
                print("\n===== AFTER RERANK =====")
                for c in retrieved_chunks:
                    print(
                        f"Page={c['page']}",
                        f"score={c.get('score')}",
                        f"bm25={c.get('bm25_score')}",
                        f"rrf={c.get('rrf_score')}",
                        f"rerank={c.get('rerank_score')}",
                    )
            logfire.info("Compressing retrieved context")

            start = time.perf_counter()

            retrieved_chunks = compress_chunks(
                question=rewritten_question,
                chunks=retrieved_chunks,
                verbose=verbose,
            )

            timings["Compression"] = time.perf_counter() - start

            if verbose:
                print("\n===== AFTER COMPRESSION =====")
                for c in retrieved_chunks:
                    print(
                        f"Page={c['page']}",
                        f"score={c.get('score')}",
                        f"bm25={c.get('bm25_score')}",
                        f"rrf={c.get('rrf_score')}",
                        f"rerank={c.get('rerank_score')}",
                    )
            retrieval_debug = build_retrieval_debug(retrieved_chunks)

            if verbose:
                print("\n===== RETRIEVAL DEBUG =====")
                for row in retrieval_debug:
                    print(row)
    
            confidence = calculate_confidence(retrieved_chunks)

            if verbose:
                print("\n===== CONFIDENCE =====")
                print(f"Level   : {confidence['level']}")
                print(f"Score   : {confidence['score']}%")
                print(f"Top     : {confidence['top_score']}")
                print(f"Average : {confidence['average_score']}")
                print("======================\n")

            logfire.info(
                "Context compression completed",
                chunks=len(retrieved_chunks),
            )
            logfire.info(
                "Retrieval completed",
                retrieved_chunks=len(retrieved_chunks),
            )
            logfire.info("Building prompt")

            start = time.perf_counter()

            prompt = build_prompt(
                question=rewritten_question,
                retrieved_chunks=retrieved_chunks,
                conversation_history=conversation_memory.get_history(),
            )

            timings["Prompt Building"] = time.perf_counter() - start

            logfire.info("Generating answer")
            start = time.perf_counter()
            answer = generate_answer(prompt)
            timings["LLM Generation"] = time.perf_counter() - start
            start = time.perf_counter()
            conversation_memory.add_user_message(question)
            conversation_memory.add_assistant_message(answer)
            timings["Memory Update"] = time.perf_counter() - start

            if verbose:
                print("\n===== Conversation History =====")
                for message in conversation_memory.get_history():
                    print(f"{message['role'].upper()}: " f"{message['content']}")
            logfire.info("Pipeline completed successfully", answer_length=len(answer))

            timings["Total"] = time.perf_counter() - pipeline_start

            return {
                "answer": answer,
                "sources": retrieved_chunks,
                "confidence": confidence,
                "retrieval_debug": retrieval_debug,
                "timings": timings,
            }

        except Exception as e:

            traceback.print_exc()

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
                "confidence": {
                    "level": "LOW",
                    "score": 0,
                    "top_score": 0,
                    "average_score": 0,
                },
            }

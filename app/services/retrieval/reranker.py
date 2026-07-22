import math
from sentence_transformers import CrossEncoder


reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_chunks(
    question: str,
    chunks: list[dict],
    top_k: int = 5,
):

    if not chunks:
        return []

    pairs = [(question, chunk["text"]) for chunk in chunks]

    scores = reranker.predict(pairs)

    for chunk, score in zip(chunks, scores):
        raw_score = float(score)
        chunk["rerank_score"] = raw_score
        chunk["score"] = 1 / (1 + math.exp(-raw_score))

    chunks = sorted(
        chunks,
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    return chunks[:top_k]

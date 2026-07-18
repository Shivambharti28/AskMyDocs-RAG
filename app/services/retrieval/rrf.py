def reciprocal_rank_fusion(dense_results,bm25_results,k=60,):

    fused_scores = {}

    # Dense search contribution
    for rank, chunk in enumerate(dense_results, start=1):

        key = (
            chunk["document_id"],
            chunk["chunk_id"],
        )

        if key not in fused_scores:
            fused_scores[key] = {
                "chunk": chunk,
                "score": 0,
            }

        fused_scores[key]["score"] += 1 / (k + rank)

    # BM25 contribution
    for rank, chunk in enumerate(bm25_results, start=1):

        key = (chunk["document_id"],chunk["chunk_id"],)

        if key not in fused_scores:
            fused_scores[key] = {
                "chunk": chunk,
                "score": 0,
            }

        fused_scores[key]["score"] += 1 / (k + rank)

    # Sort by fused score
    ranked = sorted(
        fused_scores.values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    # Return only chunks
    results = []

    for item in ranked:

        chunk = item["chunk"].copy()

        # Store the RRF score
        chunk["rrf_score"] = item["score"]

        results.append(chunk)

    return results
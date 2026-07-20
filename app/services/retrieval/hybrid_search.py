from app.services.retrieval.bm25_service import search_bm25
from app.services.retrieval.multi_query import generate_multi_queries
from app.services.retrieval.qdrant_service import search
from app.services.retrieval.query_expansion import expand_query
from app.services.retrieval.query_rewriter import rewrite_query
from app.services.retrieval.rrf import reciprocal_rank_fusion


def hybrid_search(
    query,
    conversation_history,
    limit=5,
    source=None,
    page=None,
    verbose=True,
):

    # expanded_queries = expand_query(query)
    query = rewrite_query(
        query,
        conversation_history,
        verbose=verbose,
    )

    expanded_queries = expand_query(
        query,
        verbose=verbose,
    )

    multi_queries = generate_multi_queries(
        query,
        verbose=verbose,
    )
    queries = expanded_queries + multi_queries
    # queries = [query]

    # Remove duplicates while preserving order
    seen = set()
    unique_queries = []

    for q in queries:
        key = q.lower().strip()

        if key not in seen:
            seen.add(key)
            unique_queries.append(q)

    # Optional: Limit total searches
    queries = unique_queries[:3]

    if verbose:
        print("\n===== FINAL SEARCH QUERIES =====")
        for q in queries:
            print(q)

    all_dense_results = []
    all_bm25_results = []

    for q in queries:
        if verbose:
            print(f"\nSearching for: {q}")

        dense_results = search(
            query=q,
            limit=limit,
            source=source,
            page=page,
            verbose=verbose,
        )

        bm25_results = search_bm25(
            query=q,
            limit=limit,
            source=source,
            page=page,
            verbose=verbose,
        )

        all_dense_results.extend(dense_results)
        all_bm25_results.extend(bm25_results)

    fused_results = reciprocal_rank_fusion(
        all_dense_results,
        all_bm25_results,
    )

    return fused_results

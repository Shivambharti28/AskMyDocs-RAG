from app.services.retrieval.qdrant_service import search
from app.services.retrieval.bm25_service import search_bm25
from app.services.retrieval.rrf import reciprocal_rank_fusion


def hybrid_search(
    query: str,
    limit: int = 5,
    source: str | None = None,
    page: int | None = None,
):

    dense_results = search(
        query=query,
        limit=limit,
        source=source,
        page=page,
    )

    bm25_results = search_bm25(
        query=query,
        limit=limit,
        source=source,
        page=page,
    )

    return reciprocal_rank_fusion(
        dense_results,
        bm25_results,
    )
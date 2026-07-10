# import logfire

# from qdrant_client import QdrantClient

# from app.config import settings
# from app.services.retrieval.embeddings import embed_query


# client = QdrantClient(
#     url=settings.QDRANT_URL,
#     api_key=settings.QDRANT_API_KEY,
# )

# def search_by_vector(query_vector: list[float], limit: int = 5):
#     response = client.query_points(
#         collection_name=settings.QDRANT_COLLECTION,
#         query=query_vector,
#         limit=limit,
#         with_payload=True,
#     )

#     results = []

#     for point in response.points:
#         results.append({
#             "score": point.score,
#             "text": point.payload.get("text"),
#             "source": point.payload.get("source"),
#             "page": point.payload.get("page"),
#             "section": point.payload.get("section"),
#             "chunk_id": point.payload.get("chunk_id"),
#             "document_id": point.payload.get("document_id"),
#         })

#     return results

# def search(query: str, limit: int = 5):
#     query_vector = embed_query(query)

#     return search_by_vector(
#         query_vector=query_vector,
#         limit=limit,
#     )

# def search_with_filter(
#     query: str,
#     filter_condition,
#     limit: int = 5,
# ):
#     query_vector = embed_query(query)

#     response = client.query_points(
#         collection_name=settings.QDRANT_COLLECTION,
#         query=query_vector,
#         query_filter=filter_condition,
#         limit=limit,
#         with_payload=True,
#     )

#     return response

# from app.config import settings

# print(settings.QDRANT_URL)
# print(settings.QDRANT_COLLECTION)

import logfire

from qdrant_client import QdrantClient

from app.config import settings
from app.services.retrieval.embeddings import embed_query


client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

# Minimum similarity score required
MIN_SCORE = 0.70


def search_by_vector(query_vector: list[float], limit: int = 5):
    response = client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=query_vector,
        limit=limit,
        with_payload=True,
    )

    results = []

    for point in response.points:

        # Skip weak matches
        if point.score < MIN_SCORE:
            continue

        results.append({
            "score": point.score,
            "text": point.payload.get("text"),
            "source": point.payload.get("source"),
            "page": point.payload.get("page"),
            "section": point.payload.get("section"),
            "chunk_id": point.payload.get("chunk_id"),
            "document_id": point.payload.get("document_id"),
        })

    logfire.info(
        f"Retrieved {len(results)} chunks above threshold ({MIN_SCORE})"
    )

    return results


def search(query: str, limit: int = 5):
    query_vector = embed_query(query)

    return search_by_vector(
        query_vector=query_vector,
        limit=limit,
    )


def search_with_filter(
    query: str,
    filter_condition,
    limit: int = 5,
):
    query_vector = embed_query(query)

    response = client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=query_vector,
        query_filter=filter_condition,
        limit=limit,
        with_payload=True,
    )

    return response


print(settings.QDRANT_URL)
print(settings.QDRANT_COLLECTION)
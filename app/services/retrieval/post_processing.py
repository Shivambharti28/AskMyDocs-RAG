import logfire


def deduplicate_chunks(
    chunks: list[dict],
) -> list[dict]:
    """
    Remove duplicate retrieved chunks.

    Duplicate means same document + same chunk_id.

    Keeps the highest scored occurrence.
    """

    with logfire.span(
        "Post Processing - Deduplicate Chunks"
    ):

        seen = set()
        unique_chunks = []

        for chunk in chunks:

            key = (
                chunk.get("document_id"),
                chunk.get("chunk_id"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique_chunks.append(chunk)

        logfire.info(
            "Deduplication completed",
            before=len(chunks),
            after=len(unique_chunks),
        )

        return unique_chunks
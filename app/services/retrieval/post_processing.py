import logfire

def deduplicate_chunks(chunks: list[dict],) -> list[dict]:

    with logfire.span("Post Processing - Deduplicate Chunks"):
        
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

        logfire.info("Deduplication completed",before=len(chunks),after=len(unique_chunks),)

        return unique_chunks

def merge_adjacent_chunks(chunks: list[dict]) -> list[dict]:

    with logfire.span("Post Processing - Merge Adjacent Chunks"):

        if not chunks:
            return []

        # Sort first
        chunks = sorted(
            chunks,
            key=lambda c: (
                c["document_id"],
                c["page"],
                c["chunk_id"],
            ),
        )

        merged = []
        current = chunks[0].copy()
        current = chunks[0].copy()

        # Initially, start and end are the same chunk
        current["end_chunk_id"] = current["chunk_id"]

        for chunk in chunks[1:]:
            same_document = (chunk["document_id"] == current["document_id"])
            same_page = (chunk["page"] == current["page"])
            adjacent = (chunk["chunk_id"] == current["chunk_id"] + 1)

            if same_document and same_page and adjacent:
                current["text"] += "\n\n" + chunk["text"]
                current["score"] = max(current["score"],chunk["score"],)
                current["end_chunk_id"] = chunk["chunk_id"]

            else:
                merged.append(current)
                current = chunk.copy()
                current["end_chunk_id"] = current["chunk_id"]

        merged.append(current)

        logfire.info("Merge completed",before=len(chunks),after=len(merged),)
        return merged
import os
import json

from rank_bm25 import BM25Okapi

PROCESSED_DATA_DIR = "processed_data"

bm25 = None
documents = []


def build_bm25_index():
    global bm25, documents
    documents = []
    corpus = []
    for root, _, files in os.walk(PROCESSED_DATA_DIR):
        for file in files:
            if not file.endswith(".json"):
                continue
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for chunk in data["chunks"]:
                chunk["source"] = data["filename"]
                chunk["document_id"] = data["document_id"]
                documents.append(chunk)
                corpus.append(
                    chunk["text"].split()
                )

    bm25 = BM25Okapi(corpus)

    print(f"BM25 built with {len(documents)} chunks.")

def search_bm25(query: str,limit: int = 5,source: str | None = None,page: int | None = None,):

    global bm25

    if bm25 is None:
        build_bm25_index()

    scores = bm25.get_scores(query.split())

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    results = []

    for chunk, score in ranked:

        # Filter by source
        if source is not None and chunk["source"] != source:
            continue

        # Filter by page
        if page is not None and chunk["page"] != page:
            continue

        chunk = chunk.copy()
        chunk["score"] = float(score)

        results.append(chunk)

        if len(results) == limit:
            break

    return results
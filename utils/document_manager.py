import os
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.config import settings
from app.services.retrieval.bm25_service import refresh_bm25_index
from utils.document_registry import load_documents, save_documents


UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed_data")

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)


def delete_uploaded_file(source: str):
    """
    Delete original uploaded file.
    """
    file_path = UPLOAD_DIR / source

    if file_path.exists():
        file_path.unlink()


def delete_processed_json(source: str):
    """
    Delete processed JSON metadata.
    """
    json_path = PROCESSED_DIR / "general" / f"{source}.json"

    if json_path.exists():
        json_path.unlink()


def delete_from_registry(source: str):
    """
    Remove document from documents.json.
    """
    documents = load_documents()

    documents = [
        doc
        for doc in documents
        if doc["source"] != source
    ]

    save_documents(documents)


def delete_from_qdrant(source: str):
    """
    Delete all vectors belonging to a document.
    """
    qdrant_client.delete(
        collection_name=settings.QDRANT_COLLECTION,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="source",
                        match=models.MatchValue(value=source),
                    )
                ]
            )
        ),
    )


def rebuild_bm25():
    """
    Rebuild BM25 index after deletion.
    """
    refresh_bm25_index(verbose=True)


def delete_document(source: str):
    """
    Delete a document from the entire system.
    """

    delete_uploaded_file(source)

    delete_processed_json(source)

    delete_from_registry(source)

    delete_from_qdrant(source)

    rebuild_bm25()
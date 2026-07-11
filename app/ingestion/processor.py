import os
import sys
import uuid
import json
import logfire
import traceback
from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.config import settings
from app.services.retrieval.embeddings import embed_texts, get_embedding_dim
from app.ingestion.loaders.pdf import parse_pdf
from app.ingestion.loaders.html import parse_html
from app.ingestion.loaders.text import parse_text
from app.ingestion.loaders.office import parse_office
from app.ingestion.chunking.splitter import chunk_text

logfire.configure(service_name="enterprise-ingestion-service")

PROCESSED_DATA_DIR = "processed_data"

# Initiaize Qdrant Client
qdrant_client = QdrantClient(
    url = settings.QDRANT_URL,
    api_key = settings.QDRANT_API_KEY,
    timeout = 120,
)

from app.config import settings

print("QDRANT_URL =", settings.QDRANT_URL)
print("QDRANT_COLLECTION =", settings.QDRANT_COLLECTION)

def save_processed_locally(data: dict, source_type: str, filename: str) -> str:
    """
    Save parsed chunk metadata as JSON in processed_data/<source_type>/.
    """
    folder = os.path.join(PROCESSED_DATA_DIR, source_type)
    os.makedirs(folder, exist_ok= True)
    dest = os.path.join(folder, f"{filename}.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return dest


def processed_file(file_path: str, filename: str, source_type: str):
    """
    Parse -> Chunk -> Save Locally -> Embed -> Index in Qdrant,
    """
    with logfire.span("Processing File", file = filename, source = source_type):
        try:
            # 1. Extract text based on file extension
            ext = filename.lower().rsplit(".",1)[-1]
            if ext == "pdf":
                full_text = parse_pdf(file_path)
            elif ext in ("html", "htm"):
                full_text = parse_html(file_path)
            elif ext == "txt":
                full_text = parse_text(file_path)
            elif ext in ("docx", "pptx",):
                full_text = parse_office(file_path)
            else:
                logfire.warning(f"Skipping unsupported file type: {filename}")
                return

            if not full_text:
                logfire.warning(f"No content extracted from {filename} - skipping.")
                return
            
            # 2. Chunk text
            chunks = chunk_text(full_text)
            if not chunks:
                return
            
            # 3. Save processed metadata locally
            document_id = str(uuid.uuid4())

            processed_data = {
                "document_id": document_id,
                "filename": filename,
                "source_type": source_type,
                "total_chunks": len(chunks),
                "chunks": chunks,
            }
            
            local_path = save_processed_locally(processed_data, source_type, filename)
            logfire.info(f"Saved processed data -> {local_path}")

            # 4. Embedding and Indexing
            with logfire.span("Vectorizing & Indexing"):
                document_id = str(uuid.uuid4())
                texts = [chunk["text"] for chunk in chunks]
                embeddings = embed_texts(texts)
                # embeddings = embed_texts(chunks)
                points = []
                # for chunk_id, (chunk, vector) in enumerate(zip(chunks, embeddings), start=1):
                for chunk, vector in zip(chunks, embeddings):
                    points.append(
                        models.PointStruct(
                            id=str(uuid.uuid4()),
                            vector=vector,
                         
                            payload={
                                "document_id": document_id,
                                "chunk_id": chunk["chunk_id"],
                                "page": chunk["page"],
                                "section": chunk["section"],
                                "text": chunk["text"],
                                "source": filename,
                                "source_type": source_type,
                                "chunk_length": len(chunk["text"]),
                            }
                        )
                    )
                UPSERT_BATCH_SIZE = 50
                for batch_number, i in enumerate(range(0, len(points), UPSERT_BATCH_SIZE), start=1):
                    batch = points[i:i + UPSERT_BATCH_SIZE]
                    with logfire.span(
                        "Qdrant Upload",
                        batch=batch_number,
                        points=len(batch),
                    ):
                        qdrant_client.upsert(
                            collection_name=settings.QDRANT_COLLECTION,
                            points=batch,
                            wait=True,
                        )

                logfire.info(
                    "Indexing complete",
                    filename=filename,
                    document_id=document_id,
                    chunks=len(points),
                )

        except Exception as e:
            logfire.error(f"Failed to process {filename}: {e}")
            traceback.print_exc()


def process_directory(dir_path: str, source_type: str):
    """
    Process every file in a directory.
    """
    with logfire.span("Scanning Directory", path = dir_path, source = source_type):
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        logfire.info(f"Found {len(files)} files in {dir_path}.")
        for filename in files:
            processed_file(os.path.join(dir_path, filename), filename, source_type)


def run_universal_ingestion(base_dir: str, explicit_source_type: str = None, wipe: bool = False):
    """
    Scan base_dir. map sub-folders to source types, and ingest all documents.
    Pass --wipe to drop and recreate the Qdrant collection before ingestion.
    """
    with logfire.span("Universal Ingestion Started", base_directory = base_dir):
        # Recreate collection - dimension resolved at runtime after embedding model probe
        if not qdrant_client.collection_exists(settings.QDRANT_COLLECTION):
            dim = get_embedding_dim()
            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(
                    size = dim,
                    distance=models.Distance.COSINE,
                ),
            )
            logfire.info(
                f"Created collection '{settings.QDRANT_COLLECTION}'"
                f"({dim}-dim, Cosine)."
            )

        subdirs = [
            d for d in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, d))
        ]

        if not subdirs:
            if explicit_source_type:
                source_type = explicit_source_type
            else:
                base_name = os.path.basename(os.path.normpath(base_dir)).lower()
                source_type = (
                    "true" if "true" in base_name
                    else "noisy" if "noisy" in base_name
                    else "general"
                )
            logfire.info(f"No sub-folders found - processing '{base_dir}' as '{source_type}'.")
            process_directory(base_dir, source_type)
        else:
            for subdir in subdirs:
                source_type = (
                    "true" if "true" in subdir.lower()
                    else "noisy" if "noisy" in subdir.lower()
                    else subdir
                )
                process_directory(os.path.join(base_dir, subdir), source_type)
                


if __name__ == "__main__":
    # Usage:
    #   python -m app.ingestion.processor DATA --wipe
    #   python -m app.ingestion.processor DATA/true_data true
    wipe_requested = "--wipe" in sys.argv
    clean_args = [a for a in sys.argv if a != "--wipe"]

    target_dir = clean_args[1] if len(clean_args) > 1 else "DATA"
    explicit_type = clean_args[2] if len(clean_args) > 2 else None


    if not os.path.exists(target_dir):
        print(f"Error: path '{target_dir}' does not exist.")
        sys.exit(1)

    run_universal_ingestion(target_dir, explicit_source_type=explicit_type, wipe=wipe_requested)
    logfire.info("Ingestion job completed.")


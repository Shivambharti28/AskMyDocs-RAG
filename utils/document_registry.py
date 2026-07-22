import json
from pathlib import Path
from datetime import datetime

# Project paths
DATA_DIR = Path("DATA")
DOCUMENTS_FILE = DATA_DIR / "documents.json"


def load_documents():
    DATA_DIR.mkdir(exist_ok=True)

    if not DOCUMENTS_FILE.exists():
        with open(DOCUMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []

    try:
        with open(DOCUMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_documents(documents):
    DATA_DIR.mkdir(exist_ok=True)

    with open(DOCUMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=4)


def register_document(source, file_type, pages, chunks):

    documents = load_documents()

    # Remove existing entry if the same document already exists
    documents = [
        doc for doc in documents
        if doc["source"] != source
    ]

    new_document = {
        "source": source,
        "type": file_type,
        "pages": pages,
        "chunks": chunks,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    documents.append(new_document)
    save_documents(documents)


def get_document(source):
    documents = load_documents()

    for document in documents:
        if document["source"] == source:
            return document

    return None


def document_exists(source):

    documents = load_documents()
    return any(doc["source"] == source for doc in documents)
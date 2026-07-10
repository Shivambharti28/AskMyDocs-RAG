from typing import List
import re
import nltk
import logfire

from nltk.tokenize import sent_tokenize
from langchain_text_splitters import RecursiveCharacterTextSplitter

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def split_into_sections(text: str) -> List[str]:
    with logfire.span("📑 Structure Splitter"):
        sections = re.split(r"\n\s*\n", text)
        sections = [s.strip() for s in sections if s.strip()]

        logfire.info(
            "Structure split complete",
            total_sections=len(sections)
        )
        return sections


def semantic_group(sentences: List[str], max_chars: int = 1500) -> List[str]:
    with logfire.span(
        "🧠 Semantic Grouping",
        total_sentences=len(sentences)
    ):
        chunks = []
        current = ""
        for sentence in sentences:
            if len(current) + len(sentence) <= max_chars:
                current += sentence + " "
            else:
                chunks.append(current.strip())
                current = sentence + " "
        if current.strip():
            chunks.append(current.strip())

        logfire.info(
            "Semantic grouping complete",
            semantic_chunks=len(chunks)
        )
        return chunks


# def chunk_text(text: str) -> List[str]:
def chunk_text(documents: List[dict]) -> List[dict]:
    with logfire.span(
        "✂️ Hybrid Chunking",
        documents=len(documents)
    ):
        if not documents:
            logfire.warning("Received empty document list")
            return []
        final_chunks = []
        chunk_counter = 1
        for document in documents:
            page = document["page"]
            # section_name = document["section"]
            section_name = document.get("section", f"Page {page}")
            text = document["text"]
            if not text.strip():
                continue
            sections = split_into_sections(text)
            for section_number, section_text in enumerate(sections, start=1):
                with logfire.span(
                    "📄 Processing Section",
                    page=page,
                    section=section_number,
                    length=len(section_text)
                ):
                    sentences = sent_tokenize(section_text)
                    logfire.info(
                        "Sentence tokenization",
                        sentences=len(sentences)
                    )
                    semantic_chunks = semantic_group(sentences)
                    for chunk_number, chunk_text in enumerate(semantic_chunks, start=1):
                        with logfire.span(
                            "🔹 Processing Chunk",
                            chunk=chunk_number,
                            chars=len(chunk_text)
                        ):
                            if len(chunk_text) <= 1500:
                            # final_chunks.append(chunk)
                                final_chunks.append(
                                    {
                                        "chunk_id": chunk_counter,
                                        "page": page,
                                        "section": section_name,
                                        "text": chunk_text,
                                    }
                                )
                                chunk_counter += 1
                                logfire.info(
                                    "Chunk accepted",
                                    size=len(chunk_text)
                                )
                            else:
                                recursive_chunks = recursive_splitter.split_text(chunk_text)
                                # final_chunks.extend(recursive_chunks)
                                for recursive_chunk in recursive_chunks:
                                    final_chunks.append(
                                        {
                                            "chunk_id": chunk_counter,
                                            "page": page,
                                            "section": section_name,
                                            "text": recursive_chunk,
                                        }
                                    )
                                    chunk_counter += 1
                                logfire.info(
                                    "Recursive split applied",
                                    original_size=len(chunk_text),
                                    generated=len(recursive_chunks)
                                )
        final_chunks = [
            chunk
            for chunk in final_chunks
            if chunk["text"].strip()
        ]
        logfire.info(
            "✅ Hybrid chunking complete",
            total_chunks=len(final_chunks),
            average_size=(
                sum(len(chunk["text"]) for chunk in final_chunks)
                // len(final_chunks)
                if final_chunks
                else 0
            ),
        )
    return final_chunks
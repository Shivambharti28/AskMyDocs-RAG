# Week 2 Submission
# AskMyDocs – Production RAG System

## Project Overview

During Week 2, the Retrieval-Augmented Generation (RAG) system was significantly enhanced by improving the retrieval pipeline, introducing metadata-aware search, implementing retrieval post-processing, building a production-ready API, and adding an automatic LLM fallback mechanism.

The objective of these improvements was to increase retrieval accuracy, reduce redundant context, improve answer quality, and make the overall system more reliable for production use.

---

# Features Implemented

## 1. FastAPI Backend

Built a REST API using FastAPI.

Implemented:

- POST `/ask`
- Health endpoint
- Request and Response Pydantic models
- Automatic Swagger documentation

The API now allows external applications to query the RAG system programmatically.

---

## 2. Streamlit User Interface

Developed a simple web interface using Streamlit.

Features include:

- Ask questions interactively
- Display generated answers
- Display retrieved document sources
- Show page numbers
- Show retrieval scores

This provides an easy-to-use interface for testing the RAG system.

---

## 3. Retrieval Post Processing

Created a dedicated `post_processing.py` module to improve retrieval quality before sending context to the LLM.

Implemented:

### Similarity Threshold

Introduced a minimum similarity score.

Low-confidence chunks are discarded before prompt generation.

Benefits:

- Removes irrelevant context
- Reduces hallucinations
- Improves answer quality

---

### Chunk Deduplication

Implemented duplicate removal based on:

- document_id
- chunk_id

Benefits:

- Prevents repeated context
- Reduces prompt size
- Improves retrieval efficiency

---

### Merge Adjacent Chunks

Implemented intelligent chunk merging.

Chunks are merged when:

- Same document
- Same page
- Consecutive chunk IDs

Example:

Before:

Page 8

Chunk 15

Chunk 16

Chunk 17

After:

Page 8

Chunk 15–17

Benefits:

- Better context
- More complete paragraphs
- Improved LLM understanding

---

### Chunk Range Tracking

Added

- chunk_id
- end_chunk_id

to merged chunks.

Benefits:

- Easier debugging
- Better traceability
- Future document highlighting support

---

## 4. Metadata Filtering

Implemented metadata-aware retrieval.

Supported filters:

- Source document
- Page number

Examples:

Search only:

- Motivation_Psychology_Notes.pdf

or

- Page 5

Benefits:

- More targeted retrieval
- Faster search
- Useful for multi-document collections

---

## 5. Payload Indexing

Created:

create_indexes.py

Implemented payload indexes in Qdrant.

Indexed fields:

- source
- page

Benefits:

- Enables metadata filtering
- Faster filtering performance
- Required by Qdrant

---

## 6. Improved Retrieval Pipeline

Current retrieval flow:

User Question

↓

Query Embedding

↓

Vector Search (Qdrant)

↓

Similarity Threshold

↓

Deduplicate Chunks

↓

Merge Adjacent Chunks

↓

Metadata Filtering

↓

Prompt Builder

↓

Gemini

↓

Groq (Fallback)

↓

Final Answer

---

## 7. Gemini → Groq Automatic Fallback

Implemented automatic fallback mechanism.

Primary LLM:

- Gemini 2.5 Flash

Fallback LLM:

- Groq (Llama)

When Gemini quota is exceeded:

429 RESOURCE_EXHAUSTED

↓

Automatically switches to Groq

↓

Returns answer

Benefits:

- Higher reliability
- Better uptime
- Production-ready architecture

---

## 8. Improved Logging

Integrated Logfire throughout the retrieval pipeline.

Added tracing for:

- Retrieval
- Deduplication
- Merge
- Prompt generation
- LLM invocation
- Fallback handling

Benefits:

- Easier debugging
- Better observability
- Production monitoring

---

# Technologies Used

- Python
- FastAPI
- Streamlit
- LangChain
- Google Gemini
- Groq
- Qdrant Vector Database
- Logfire
- Pydantic
- NLTK

---

# Current Project Architecture

```
                    User Question
                           │
                           ▼
                  Query Embedding
                           │
                           ▼
                  Qdrant Vector Search
                           │
                           ▼
                Retrieval Post Processing
        ┌─────────────────────────────────────┐
        │ Similarity Threshold                │
        │ Deduplicate Chunks                  │
        │ Merge Adjacent Chunks               │
        │ Metadata Filtering                  │
        └─────────────────────────────────────┘
                           │
                           ▼
                    Prompt Builder
                           │
                           ▼
                 Gemini 2.5 Flash
                           │
             Quota exceeded?
                  │
          Yes ────┘
                  ▼
              Groq Fallback
                  │
                  ▼
          Answer + Citations
```

---

# Learning Outcomes

During Week 2, I learned:

- Building REST APIs using FastAPI
- Developing Streamlit interfaces
- Improving retrieval quality through post-processing
- Implementing metadata-aware vector search
- Creating payload indexes in Qdrant
- Designing production-grade retrieval pipelines
- Implementing automatic LLM fallback mechanisms
- Using Logfire for observability and debugging

---

# Future Improvements

Planned improvements include:

- Hybrid Search (Dense + BM25)
- Cross-Encoder Re-ranking
- Multi-Query Retrieval
- Query Rewriting
- Parent-Child Retrieval
- Conversation Memory
- Streaming Responses
- Docker Deployment
- RAGAS Evaluation
- Multi-document Collections
- OCR Support
- Multi-modal RAG

---

# Conclusion

Week 2 focused on transforming the initial RAG prototype into a more production-ready system. Significant improvements were made to retrieval quality, API development, metadata filtering, observability, and fault tolerance through automatic LLM fallback. These enhancements make the system more accurate, reliable, scalable, and easier to maintain.
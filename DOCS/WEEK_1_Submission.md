# Week 1 Submission – AskMyDocs RAG Project

## Student Information

**Project:** AskMyDocs – Retrieval-Augmented Generation (RAG) System

**Week:** 1

---

# Overview

During Week 1, I focused on understanding the core building blocks required to develop a Retrieval-Augmented Generation (RAG) application.

Instead of building the complete application immediately, I implemented and tested each major component independently to understand how they work together.

The project currently uses:

- LangChain
- Google Gemini 2.5 Flash
- Gemini Embeddings
- ChromaDB
- Python
- python-dotenv

---

# Work Completed

## 1. Project Setup

- Configured Python virtual environment.
- Installed all required dependencies using `uv`.
- Configured API keys using `.env`.
- Verified LangChain and LangGraph installation.
- Successfully tested:
  - Google Gemini
  - Groq LLM

---

## 2. Document Loaders

Implemented and tested different document loading techniques.

Completed:

- TextLoader
- WebBaseLoader
- DirectoryLoader
- PyPDFLoader
- Manual Document creation

Learned:

- LangChain `Document` structure
- Metadata handling
- Loading documents from different sources

---

## 3. Text Splitters

Implemented multiple chunking strategies.

Studied:

- RecursiveCharacterTextSplitter
- CharacterTextSplitter
- TokenTextSplitter
- MarkdownHeaderTextSplitter
- Language-specific splitters

Implemented experiments for:

- Recursive chunking
- Chunk size comparison
- Chunk overlap analysis

Key Learning:

- How chunk size affects retrieval quality.
- Why chunk overlap preserves context.
- Importance of semantic chunking in RAG.

---

## 4. Embeddings

Implemented semantic embeddings using Google Gemini.

Completed:

- Single text embedding
- Batch embeddings
- Cosine similarity calculation
- Basic semantic search

Key Learning:

- Difference between queries and document embeddings.
- How embeddings represent semantic meaning.
- Similarity search using cosine similarity.

---

## 5. Vector Stores

Implemented ChromaDB vector database.

Completed:

- Creating vector store
- Similarity search
- Similarity search with scores
- Metadata filtering

Key Learning:

- Storing embeddings
- Retrieving relevant documents
- Using metadata for filtered retrieval

---

## 6. Basic RAG Pipeline

Implemented a complete Retrieval-Augmented Generation workflow.

Pipeline:

Knowledge Base

↓

Chunking

↓

Gemini Embeddings

↓

ChromaDB

↓

Retriever

↓

Gemini 2.5 Flash

↓

Generated Answer

Implemented:

- Basic RAG
- Prompt template
- Retriever
- Gemini integration
- Response generation

---

## 7. Prompt Engineering

Improved prompts to:

- Generate complete sentences
- Reduce short one-word answers
- Restrict answers to retrieved context
- Return "I don't know" when evidence is unavailable

---

## 8. Cost Optimization Experiments

Implemented basic production concepts including:

- Model routing
- Semantic caching
- Token budgeting

Purpose:

- Understand techniques used to reduce LLM inference cost.

---

## 9. Documentation

Prepared:

- README.md
- Design Document

Both describe the project architecture, workflow, and future enhancements.

---

# Technologies Used

- Python 3.13
- LangChain
- LangChain Community
- Google Gemini
- Gemini Embeddings
- ChromaDB
- LangGraph
- python-dotenv
- NumPy

---

# Folder Structure

```
project/
│
├── document_loaders.py
├── text_splitters.py
├── embeddings_deep.py
├── vector_stores.py
├── rag_pipeline.py
├── cost_optimization.py
├── design_doc.md
├── README.md
├── pyproject.toml
└── .env
```

---

# Key Learnings

Throughout this week, I learned:

- How LangChain represents documents.
- Different document loading strategies.
- Importance of chunking.
- Embeddings and semantic similarity.
- Vector databases and similarity search.
- Retrieval-Augmented Generation workflow.
- Prompt engineering basics.
- Metadata filtering.
- Basic production optimization techniques.

---

# Challenges Faced

- Migrating tutorial code from OpenAI to Google Gemini.
- Understanding embedding APIs.
- Configuring LangChain with Gemini.
- Understanding chunk overlap and chunk size.
- Debugging package compatibility issues.

---

# Current Status

Completed:

- Environment setup
- Document loading
- Chunking
- Embeddings
- Vector database
- Basic RAG pipeline
- Prompt engineering
- Cost optimization experiments
- Project documentation

The current implementation demonstrates the core concepts required for building a Retrieval-Augmented Generation system.

---

# Planned Work for Week 2

- PDF-based RAG
- Streamlit interface
- Upload custom documents
- Source citations
- Hybrid Search (BM25 + Dense Retrieval)
- Multi-document comparison
- RAG evaluation
- Docker deployment

---

# Conclusion

Week 1 established the foundational components of a Retrieval-Augmented Generation system. I now understand how documents are loaded, chunked, embedded, stored in a vector database, retrieved, and used by an LLM to generate grounded responses.

This foundation will be extended in the coming weeks to build a complete production-style AskMyDocs application.
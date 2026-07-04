# Design Document – Building RAG Pipelines

## Project Overview

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using LangChain, Google Gemini, and ChromaDB.

The goal is to allow an LLM to answer questions using only information retrieved from a knowledge base instead of relying solely on its pretrained knowledge. This reduces hallucinations and produces grounded, context-aware responses.

---

# Objectives

- Learn the complete RAG workflow.
- Store documents as embeddings in a vector database.
- Retrieve the most relevant chunks for a user query.
- Generate answers using Gemini.
- Demonstrate different RAG patterns:
  - Basic RAG
  - RAG with source attribution
  - RAG with fallback responses
  - Structured output using Pydantic
  - Reusable Document Q&A system

---

# Architecture

```
                Knowledge Base
                     │
                     ▼
           Text Splitter (Chunking)
                     │
                     ▼
      Google Gemini Embeddings
                     │
                     ▼
              Chroma Vector Store
                     │
                     ▼
                Retriever
                     │
                     ▼
          Relevant Document Chunks
                     │
                     ▼
              Prompt Template
                     │
                     ▼
      Gemini 2.5 Flash Language Model
                     │
                     ▼
             Generated Response
```

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| LLM | Gemini 2.5 Flash |
| Embeddings | Gemini Embedding 2 |
| Framework | LangChain |
| Vector Database | ChromaDB |
| Prompting | ChatPromptTemplate |
| Output Parser | StrOutputParser |
| Structured Output | Pydantic |

---

# System Components

## 1. Knowledge Base

A sample knowledge base containing information about LangChain is used.

Currently, the knowledge base is stored as a Python string.

Future enhancement:

- PDF documents
- Research papers
- Documentation websites

---

## 2. Document Chunking

The knowledge base is divided into smaller chunks using:

- RecursiveCharacterTextSplitter

Configuration:

- Chunk Size: 500 characters
- Chunk Overlap: 50 characters

Purpose:

- Preserve context
- Improve retrieval quality
- Reduce token usage

---

## 3. Embeddings

Each chunk is converted into a dense vector using:

GoogleGenerativeAIEmbeddings

Model:

```
models/gemini-embedding-2
```

Purpose:

Convert text into semantic vectors for similarity search.

---

## 4. Vector Database

Embeddings are stored inside ChromaDB.

Responsibilities:

- Store vectors
- Perform similarity search
- Return the most relevant chunks

---

## 5. Retriever

The retriever performs similarity search on ChromaDB.

Current configuration:

```
Top K = 2 or 3
Search Type = Similarity
```

Output:

Relevant document chunks.

---

## 6. Prompt Template

The retrieved context and user question are combined into a prompt.

The prompt instructs Gemini to:

- Use only retrieved context.
- Avoid hallucinations.
- Respond with complete sentences.
- Return "I don't know" if evidence is missing.

---

## 7. Language Model

The project uses:

Gemini 2.5 Flash

Responsibilities:

- Read retrieved context.
- Generate natural language responses.
- Follow prompt instructions.

---

## 8. Output Parser

StrOutputParser converts the LLM response into plain text.

---

# RAG Variants Implemented

## Basic RAG

Features:

- Retrieval
- Generation
- Context-aware answering

---

## RAG with Sources

Additional capability:

- Includes document source information.

Benefit:

Improves transparency.

---

## RAG with Fallback

If relevant information is unavailable:

```
I don't have information about that in my knowledge base.
```

Purpose:

Reduce hallucinations.

---

## Structured RAG

Uses:

- Pydantic
- Structured Output

Returns:

- Answer
- Confidence
- Sources
- Follow-up question

---

## Document Q&A

Encapsulates the complete RAG workflow into a reusable class.

Responsibilities:

- Chunk document
- Create vector store
- Retrieve context
- Generate answers

---

# Design Decisions

## Why Gemini?

- High-quality responses
- Fast inference
- Native embedding support
- Easy integration with LangChain

---

## Why ChromaDB?

- Lightweight
- Easy setup
- No external server
- Suitable for learning projects

---

## Why RecursiveCharacterTextSplitter?

Advantages:

- Preserves paragraph boundaries.
- Avoids splitting words unnecessarily.
- Produces semantically meaningful chunks.

---

## Why Chunk Overlap?

Overlap preserves information across chunk boundaries.

Without overlap:

```
Chunk 1:
Machine learning is...

Chunk 2:
...used for image recognition.
```

Important context may be lost.

With overlap:

```
Chunk 1:
Machine learning is used...

Chunk 2:
...is used for image recognition.
```

---

# Limitations

Current limitations:

- Hardcoded knowledge base
- No PDF ingestion
- No page citations
- No metadata filtering
- Similarity search only
- Single document
- No evaluation framework

---

# Future Enhancements

Planned improvements:

- PDF upload support
- PyMuPDF integration
- Page-level citations
- Hybrid Search (BM25 + Dense Retrieval)
- Metadata filtering
- Multi-document comparison
- Streamlit interface
- RAGAS evaluation
- Docker deployment
- Production logging
- Unit tests

---

# Project Workflow

```
Knowledge Base
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
Vector Store
      │
      ▼
Retriever
      │
      ▼
Prompt
      │
      ▼
Gemini
      │
      ▼
Generated Answer
```

---

# Conclusion

This project demonstrates the core concepts of Retrieval-Augmented Generation using LangChain, Gemini, and ChromaDB.

It serves as a foundation for building production-grade AI applications capable of answering questions from domain-specific knowledge while minimizing hallucinations through retrieval-based grounding.
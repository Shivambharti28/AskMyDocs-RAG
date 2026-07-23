# ADR-001: Use Qdrant Cloud as the Vector Database

## Status

Accepted

---

## Context

The AskMyBook application requires a vector database to store document embeddings and perform fast semantic similarity search over uploaded PDF documents.

The solution should:

- Store high-dimensional embeddings (3072-dimensional Gemini embeddings)
- Support metadata filtering
- Be scalable
- Provide low-latency retrieval
- Integrate easily with Python

---

## Decision

We chose **Qdrant Cloud** as the vector database.

---

## Alternatives Considered

### ChromaDB

Pros
- Easy to set up
- Good for local development

Cons
- Limited scalability
- Not ideal for production deployments

---

### Weaviate

Pros
- Rich feature set
- Graph capabilities

Cons
- More complex to configure
- Heavier infrastructure requirements

---

### pgvector

Pros
- Works inside PostgreSQL
- Good for existing SQL ecosystems

Cons
- Additional tuning required
- Not optimized specifically for vector search

---

## Why Qdrant Cloud?

Qdrant Cloud provides:

- Managed cloud infrastructure
- High-performance ANN search
- Metadata filtering
- REST API
- Python SDK
- Production-ready deployment
- Easy integration with Streamlit applications

It also supports storing additional metadata such as:

- document name
- page number
- source file
- chunk identifiers

which simplifies citation generation.

---

## Consequences

### Advantages

- Fully managed cloud service
- Persistent storage
- Scalable architecture
- Fast semantic retrieval
- Easy deployment

### Disadvantages

- Requires internet connectivity
- Dependent on cloud service availability
- Free tier storage limitations

---

## Outcome

Qdrant Cloud met all project requirements while providing a production-ready vector storage solution suitable for enterprise Retrieval-Augmented Generation systems.
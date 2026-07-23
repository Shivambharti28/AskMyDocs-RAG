# ADR-002: Use Hybrid Retrieval (BM25 + Dense Retrieval + RRF)

## Status

Accepted

---

## Context

A Retrieval-Augmented Generation (RAG) system depends on retrieving the most relevant document chunks before generating an answer.

Relying only on dense embeddings may miss exact keyword matches, while lexical retrieval alone cannot understand semantic similarity.

The retrieval pipeline should balance both approaches.

---

## Decision

Implement a hybrid retrieval pipeline consisting of:

- BM25 lexical search
- Dense vector search using Gemini embeddings
- Reciprocal Rank Fusion (RRF)
- Cross-Encoder reranking
- Context compression

---

## Alternatives Considered

### BM25 Only

Pros

- Excellent keyword matching
- Fast

Cons

- Cannot understand semantic similarity
- Misses paraphrased queries

---

### Dense Retrieval Only

Pros

- Understands semantic meaning
- Handles synonyms

Cons

- Can miss exact terminology
- Embedding similarity is not always sufficient

---

## Why Hybrid Retrieval?

The hybrid approach combines the strengths of both retrieval methods.

The implemented pipeline performs:

1. Query rewriting
2. Query expansion
3. Multi-query generation
4. BM25 retrieval
5. Dense vector retrieval
6. Reciprocal Rank Fusion
7. Duplicate removal
8. Adjacent chunk merging
9. Cross-Encoder reranking
10. Context compression

This significantly improves retrieval quality compared to a single retrieval strategy.

---

## Consequences

### Advantages

- Better recall
- Better precision
- Handles synonyms
- Preserves exact keyword matches
- More robust retrieval

### Disadvantages

- Increased implementation complexity
- Additional latency
- More LLM calls during retrieval

---

## Outcome

The hybrid retrieval pipeline consistently retrieves more relevant context and forms the foundation of the AskMyBook RAG system.
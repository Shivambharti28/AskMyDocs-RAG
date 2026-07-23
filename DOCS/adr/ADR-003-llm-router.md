# ADR-003: Use an LLM Router Instead of a Single Language Model

## Status

Accepted

---

## Context

The application requires a language model for several tasks:

- Query rewriting
- Query expansion
- Multi-query generation
- Context compression
- Final answer generation

Different tasks have different cost and latency requirements.

Using a single large model for every stage increases both cost and response time.

---

## Decision

Implement an LLM Router capable of selecting different models depending on the task.

Current configuration:

- Gemini models
- Groq-hosted models

The router allows selecting either a lower-cost model for retrieval-related tasks or a higher-quality model for answer generation.

---

## Alternatives Considered

### Single Gemini Model

Pros

- Simple implementation

Cons

- Higher cost for lightweight tasks
- Less flexibility

---

### Single OpenAI Model

Pros

- High quality

Cons

- Increased API cost
- Vendor dependency

---

## Why an LLM Router?

Different pipeline stages have different computational requirements.

Examples:

Query rewriting

- Small model

Query expansion

- Small model

Context compression

- Medium model

Final answer generation

- High-quality model

Using an LLM router allows selecting the appropriate model for each task while balancing cost, latency, and answer quality.

The design also makes future model replacements straightforward.

---

## Consequences

### Advantages

- Lower operational cost
- Faster response times
- Easy experimentation
- Reduced vendor lock-in
- Flexible architecture

### Disadvantages

- Slightly more complex implementation
- Additional routing logic

---

## Outcome

The LLM Router provides a flexible and extensible architecture that supports multiple providers while improving efficiency and reducing inference costs.
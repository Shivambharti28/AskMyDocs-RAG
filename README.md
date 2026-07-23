# 📚 AskMyBook – Enterprise RAG System

AskMyBook is an **Enterprise Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask natural language questions about their content.

The system combines **Hybrid Retrieval**, **Query Rewriting**, **Query Expansion**, **Multi-Query Retrieval**, **Reciprocal Rank Fusion (RRF)**, **Cross-Encoder Reranking**, and **Context Compression** to provide accurate, citation-backed answers.

Built as part of a GenAI engineering project to demonstrate production-style Retrieval-Augmented Generation systems.

---

# 🚀 Features

### 📄 Intelligent Document Processing

- PDF text extraction (PyPDF + PDFPlumber fallback)
- Structural chunking
- Semantic chunking
- Metadata extraction
- Automatic ingestion pipeline

---

### 🔍 Enterprise Retrieval Pipeline

- Query Rewriting
- Query Expansion
- Multi-Query Generation
- Hybrid Search
  - BM25
  - Dense Vector Search
- Reciprocal Rank Fusion (RRF)
- Duplicate Removal
- Adjacent Chunk Merging
- Cross-Encoder Reranking
- Context Compression
- Confidence Scoring

---

### 🤖 LLM Pipeline

- Gemini Embeddings
- Gemini LLM
- Groq LLM Support
- Automatic LLM Routing
- Conversation Memory
- Prompt Engineering

---

### 📑 Answer Generation

- Context-aware responses
- Source citations
- Page references
- Guardrails ("I don't know" when evidence is insufficient)

---

### 💻 User Interface

- Streamlit Web App
- PDF Upload
- Interactive Chat Interface
- Conversation History
- Retrieval Debug Panel
- Source Viewer

---

# 🏗️ System Architecture

```
                    Upload PDF
                         │
                         ▼
                 PDF Parsing
                         │
                         ▼
          Structural + Semantic Chunking
                         │
                         ▼
                  Gemini Embeddings
                         │
                         ▼
                  Qdrant Cloud
                         │
                         ▼
                  User Question
                         │
                         ▼
                 Query Rewriting
                         │
                         ▼
                 Query Expansion
                         │
                         ▼
              Multi Query Generation
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
   BM25 Retrieval                 Dense Retrieval
        └──────────────┬───────────────┘
                       ▼
          Reciprocal Rank Fusion (RRF)
                       ▼
            Duplicate Removal
                       ▼
          Adjacent Chunk Merging
                       ▼
         Cross Encoder Reranking
                       ▼
            Context Compression
                       ▼
             Prompt Construction
                       ▼
            Gemini / Groq Router
                       ▼
               Final Response
                       ▼
         Answer + Source Citations
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.13 |
| UI | Streamlit |
| LLM | Google Gemini, Groq |
| Embeddings | Gemini Embedding 2 |
| Vector Database | Qdrant Cloud |
| Lexical Search | BM25 |
| Retrieval | Hybrid Retrieval |
| Fusion | Reciprocal Rank Fusion |
| Reranker | Cross Encoder |
| PDF Parsing | PyPDF, PDFPlumber |
| Chunking | Structural + Semantic |
| Environment | python-dotenv |

---

# 📂 Project Structure

```
AskMyBook/
│
├── app/
│   ├── ingestion/
│   ├── services/
│   │   ├── retrieval/
│   │   ├── llm/
│   │   ├── embeddings/
│   │   └── vector_store/
│   ├── prompts/
│   └── utils/
│
├── uploads/
├── processed_data/
├── docs/
│   └── adr/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── design_doc.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AskMyBook.git

cd AskMyBook
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Mac/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_KEY

GROQ_API_KEY=YOUR_KEY

QDRANT_URL=YOUR_URL

QDRANT_API_KEY=YOUR_KEY
```

---

# ▶️ Running the Application

```bash
streamlit run streamlit_app.py
```

---

# 📖 How It Works

1. Upload a PDF.
2. The document is parsed and chunked.
3. Chunks are embedded using Gemini Embeddings.
4. Embeddings are stored in Qdrant Cloud.
5. User asks a question.
6. The system rewrites and expands the query.
7. BM25 and Dense Retrieval execute in parallel.
8. Results are fused using Reciprocal Rank Fusion.
9. Chunks are reranked and compressed.
10. The selected context is passed to the LLM.
11. The system returns an answer with citations.

---

# 🛡️ Guardrails

The system includes several guardrails:

- Refuses to hallucinate when evidence is weak.
- Returns "I don't know" when sufficient context is unavailable.
- Answers only from uploaded documents.
- Uses retrieved evidence for every response.

---

# 📊 Current Capabilities

- PDF Question Answering
- Hybrid Retrieval
- Query Rewriting
- Query Expansion
- Multi Query Retrieval
- Reciprocal Rank Fusion
- Cross Encoder Reranking
- Context Compression
- Conversation Memory
- Confidence Scoring
- Source Citations

---

# 🔮 Future Improvements

- Multi-document comparison
- Metadata filtering
- OCR for scanned PDFs
- Image understanding
- Table extraction
- RAGAS evaluation
- Docker deployment
- Authentication
- Streaming responses
- REST API

---

# 📈 Evaluation

The system will be evaluated using:

- Correctness
- Citation Precision
- Completeness

using a benchmark of 20+ manually curated questions.

---

# 📚 Architecture Decision Records (ADRs)

The project includes ADRs documenting important architectural decisions:

- ADR-001: Choosing Qdrant Cloud
- ADR-002: Hybrid Retrieval Pipeline
- ADR-003: LLM Routing Strategy

---

# 📸 Screenshots

> Add screenshots of:

- Home Page
- PDF Upload
- Chat Interface
- Retrieval Debug
- Source Citations

---

# 👨‍💻 Author

**Shivam Bharti**

Enterprise Retrieval-Augmented Generation (RAG) Project

Built using Python, Streamlit, Gemini, Qdrant Cloud, and modern Retrieval Engineering techniques.

** Video Link **
https://drive.google.com/file/d/1r8bLVqjQWBoknZ3elLPrJUic75JtbIPf/view?usp=sharing
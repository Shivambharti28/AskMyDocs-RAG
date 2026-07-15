# 📚 AskMyDocs – Production RAG System

A production-ready Retrieval-Augmented Generation (RAG) system that allows users to ask natural language questions over their own documents and receive accurate, citation-backed answers powered by Large Language Models.

The system performs semantic retrieval using vector embeddings, retrieves the most relevant document chunks from Qdrant, builds a grounded prompt, and generates responses using Google's Gemini models.

---

# ✨ Features

- 📄 Multi-document ingestion
- 🧩 Hybrid document chunking
- 🔍 Semantic vector search
- 📚 Citation-backed answers
- 🤖 Gemini/Groq LLM integration
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- ☁️ Qdrant Cloud vector database
- 📊 Logfire observability
- 🔄 Modular production architecture
- 🚀 REST API support

---

# 🏗️ Architecture

```
                User Question
                      │
                      ▼
              FastAPI / Streamlit
                      │
                      ▼
              Query Embedding
          (Gemini Embeddings)
                      │
                      ▼
            Semantic Search
             (Qdrant Cloud)
                      │
                      ▼
          Retrieved Document Chunks
                      │
                      ▼
             Prompt Builder
                      │
                      ▼
           Gemini 2.5 Flash Lite
                      │
                      ▼
            Final Grounded Answer
                      │
                      ▼
         Sources + Page Citations
```

---

# 📂 Project Structure

```
AskMyDocs-RAG/

│
├── app/
│   ├── ingestion/
│   │   ├── loaders/
│   │   ├── chunking/
│   │   └── processor.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── qdrant_service.py
│   │   ├── post_processing.py
│   │   ├── prompt_builder.py
│   │   ├── llm_service.py
│   │   └── rag_pipeline.py
│   │
│   ├── ui/
│   │   └── streamlit_app.py
│   │
│   ├── api.py
│   ├── config.py
│   └── tests...
│
├── DATA/
├── .env
├── requirements.txt
└── README.md
```

---

# 🚀 Tech Stack

### LLM

- Google Gemini 2.5 Flash Lite

### Embeddings

- Gemini Embedding 2

### Vector Database

- Qdrant Cloud

### Backend

- FastAPI

### Frontend

- Streamlit

### Logging

- Logfire

### Language

- Python 3.13+

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/AskMyDocs-RAG.git

cd AskMyDocs-RAG
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY

QDRANT_CLUSTER_ENDPOINT=https://your-cluster.cloud.qdrant.io

QDRANT_API_KEY=YOUR_QDRANT_KEY

GROQ_API_KEY=YOUR_GROQ_KEY
```

---

# 📥 Document Ingestion

Place your files inside

```
DATA/
```

Run

```bash
python -m app.ingestion.processor DATA
```

The pipeline will

- Parse documents
- Chunk documents
- Generate embeddings
- Upload vectors to Qdrant

---

# ▶️ Run FastAPI

```bash
uvicorn app.api:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# 🎨 Run Streamlit

```bash
streamlit run app/ui/streamlit_app.py
```

---

# 🔍 Example Query

```
What is motivation?
```

Example response

```
Motivation is an internal psychological process that directs
behavior toward goals and energizes action.

Source:
Motivation_Psychology_Notes.pdf
Page 3
```

---

# 🌐 API

### POST

```
/ask
```

Request

```json
{
    "question": "What is motivation?"
}
```

Response

```json
{
  "answer": "...",
  "sources": [
    {
      "source": "Motivation_Psychology_Notes.pdf",
      "page": 3,
      "score": 0.76
    }
  ]
}
```

---

# 🔄 RAG Pipeline

```
User Question
        │
        ▼
Generate Query Embedding
        │
        ▼
Semantic Search (Qdrant)
        │
        ▼
Post Processing
    ├── Similarity Threshold
    ├── Deduplication
        │
        ▼
Prompt Builder
        │
        ▼
Gemini LLM
        │
        ▼
Answer + Sources
```

---

# 📊 Current Retrieval Features

✅ Semantic Retrieval

✅ Similarity Threshold Filtering

✅ Duplicate Chunk Removal

✅ Source Attribution

✅ Page-Level Citations

---

# 📈 Future Improvements

- Hybrid Search (BM25 + Dense Retrieval)
- Cross Encoder Re-ranking
- Metadata Filtering
- Query Expansion
- Parent-Child Retrieval
- Multi-Query Retrieval
- Context Compression
- OCR Support
- Image Retrieval
- Streaming Responses
- Authentication
- Docker Deployment
- CI/CD Pipeline

---

# 🧪 Testing

Retrieval

```bash
python -m app.test_retrieval
```

Prompt Builder

```bash
python -m app.test_prompt
```

LLM

```bash
python -m app.test_llm
```

Complete Pipeline

```bash
python -m app.test_rag
```

---

# 📸 Screenshots

You can add screenshots here.

- Streamlit Interface
- Swagger UI
- Logfire Dashboard
- Qdrant Cloud

---

# 👨‍💻 Author

**Shivam Bharti**

AI/ML Engineer | Python | RAG | LLM Applications

---

# 📄 License

This project is released under the MIT License.
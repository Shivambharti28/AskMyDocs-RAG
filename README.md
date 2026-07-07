# 📚 AskMyDocs - Production RAG System 

A **Retrieval-Augmented Generation (RAG)** application built using **LangChain**, **Google Gemini**, and **ChromaDB**. This project allows users to upload documents and ask natural language questions. Instead of relying only on the LLM's knowledge, the system retrieves relevant document chunks and generates accurate, context-aware answers.

----

## 🚀 Features 

* 📄 Load PDF and text documents
* ✂️ Intelligent document chunking
* 🔍 Semantic search using embeddings
* 🗂️ ChromaDB vector database
* 🤖 Google Gemini as the LLM
* 💬 Context-aware question answering
* 📚 Source document retrieval
* ⚡ Modular and production-ready architecture

---

## 🏗️ Project Architecture

```
                +----------------------+
                |     User Uploads     |
                |   PDF / TXT Files    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Document Loader      |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Text Splitter        |
                | (Chunking)           |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Embedding Model      |
                | Gemini Embeddings    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Chroma Vector Store  |
                +----------+-----------+
                           |
                    User Question
                           |
                           v
                +----------------------+
                | Similarity Search    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Retrieved Chunks     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Gemini LLM           |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Final Answer         |
                +----------------------+
```

---

## 🛠️ Tech Stack

* Python 3.11+
* LangChain
* Google Gemini
* ChromaDB
* LangChain Community
* python-dotenv

---

## 📂 Project Structure

```
AskMyDocs/
│
├── vector_store/          # Chroma database
├── loaders.py             # Document loading
├── vector_store.py        # ChromaDB operations
├── main.py                # Entry point
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/AskMyDocs.git
cd AskMyDocs
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=your_google_api_key
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🔄 RAG Workflow

1. Load documents.
2. Split documents into smaller chunks.
3. Generate vector embeddings.
4. Store embeddings in ChromaDB.
5. Receive a user query.
6. Perform similarity search.
7. Retrieve the most relevant chunks.
8. Send retrieved context to Gemini.
9. Generate a grounded answer.

---

## 📌 Example Query

**Question**

```
What is Retrieval-Augmented Generation?
```

**Output**

```
Retrieval-Augmented Generation (RAG) combines information retrieval
with a Large Language Model by retrieving relevant document chunks
and using them as context before generating the final answer.
```

----


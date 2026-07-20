import os
import shutil
from pathlib import Path
import streamlit as st
from app.ingestion.processor import run_universal_ingestion

# run_universal_ingestion(
#     base_dir="uploads",
#     wipe=True,
# )

st.set_page_config(
    page_title="Enterprise Document Assistant",
    page_icon="📚",
    layout="wide",
)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("📚 Enterprise RAG")

    st.divider()

    st.subheader("📄 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "docx", "pptx", "txt", "html"],
        accept_multiple_files=True,
    )

    if st.button("📥 Save & Index Documents"):

        if not uploaded_files:
            st.warning("Please upload at least one document.")
        else:

            # Remove previous uploads
            if UPLOAD_DIR.exists():
                shutil.rmtree(UPLOAD_DIR)

            UPLOAD_DIR.mkdir(exist_ok=True)

            # Save uploaded files
            for uploaded_file in uploaded_files:
                file_path = UPLOAD_DIR / uploaded_file.name

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Index the uploaded documents
            with st.spinner("Indexing documents... Please wait."):
                run_universal_ingestion(
                    base_dir="uploads",
                    wipe=True,
                )

            st.success("✅ Documents indexed successfully!")

    st.divider()

    st.subheader("⚙️ Options")

    st.button("🗑️ Clear Chat")

    st.button("♻️ Clear Database")

# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 Enterprise Document Assistant")

st.write(
    "Upload your documents and ask questions about them."
)

st.divider()

question = st.text_input(
    "Ask a question"
)

if st.button("Ask"):
    st.info(f"You asked: {question}")

st.divider()

st.subheader("Answer")

st.empty()

st.divider()

st.subheader("Confidence")

st.empty()

st.divider()

st.subheader("Sources")

st.empty()
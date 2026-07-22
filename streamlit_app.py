import re
import json
import shutil
from pathlib import Path

import streamlit as st


from app.ingestion.processor import run_universal_ingestion
from app.services.retrieval.rag_pipeline import ask
from utils.document_registry import load_documents
from utils.document_manager import delete_document

st.set_page_config(
    page_title="Enterprise Document Assistant",
    page_icon="📚",
    layout="wide",
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR = Path("processed_data")


def get_pages_for_document(filename: str):
    """
    Returns all available page numbers for a document.
    """

    json_name = filename + ".json"

    json_path = PROCESSED_DIR / "general" / json_name

    if not json_path.exists():
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pages = sorted(
        {
            chunk["page"]
            for chunk in data["chunks"]
        }
    )

    return pages

def make_preview(text, max_chars=200):
    text = " ".join(text.split())

    if len(text) <= max_chars:
        return text

    preview = text[:max_chars]

    if "." in preview:
        return preview.rsplit(".", 1)[0] + "."

    return preview.rsplit(" ", 1)[0] + "..."

def highlight_query(text, query):

    words = [
        word
        for word in query.split()
        if len(word) > 2
    ]

    for word in words:

        text = re.sub(
            rf"(?i)\b({re.escape(word)})\b",
            r"**\1**",
            text,
        )

    return text

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("📚 Enterprise RAG")

    # -------------------------
    # Upload Documents
    # -------------------------
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

            # Index uploaded documents
            with st.spinner("Indexing documents... Please wait."):
                run_universal_ingestion(
                    base_dir="uploads",
                    wipe=True,
                )

            st.success("✅ Documents indexed successfully!")

    # -------------------------
    # Uploaded Documents
    # -------------------------
    st.divider()
    st.subheader("📚 Uploaded Documents")

    documents = load_documents()

    if not documents:
        st.info("No documents uploaded yet.")

    else:
        for doc in documents:

            with st.container():

                st.markdown(f"**📄 {doc['source']}**")
                st.caption(f"📑 {doc['type']}")
                st.caption(f"📄 {doc['pages']} Pages")
                st.caption(f"🧩 {doc['chunks']} Chunks")
                st.caption(f"🕒 {doc['uploaded_at']}")
                # if st.button("🗑 Delete", key=doc["source"]):
                #     st.success(f"Delete clicked for {doc['source']}")
                if st.button("🗑 Delete", key=doc["source"]):
                    with st.spinner("Deleting document..."):
                        delete_document(doc["source"])
                    st.success("Document deleted successfully!")
                    st.rerun()

                st.divider()

    # -------------------------
    # Search Scope
    # -------------------------
    st.divider()
    st.subheader("🔍 Search Scope")

    available_files = sorted(
        [
            f.name
            for f in UPLOAD_DIR.iterdir()
            if f.is_file()
        ]
    )

    selected_file = st.selectbox(
        "Search only in:",
        ["All Documents"] + available_files,
    )

    selected_page = None

    if selected_file != "All Documents":

        pages = get_pages_for_document(selected_file)

        page_options = ["All Pages"] + pages

        selected_page = st.selectbox(
            "Page",
            page_options,
        )

    # -------------------------
    # Options
    # -------------------------
    st.divider()
    st.subheader("⚙️ Options")

    if st.button("🗑️ Clear Chat"):

        if "result" in st.session_state:
            del st.session_state["result"]

        st.rerun()

# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 Enterprise Document Assistant")

st.write(
    "Upload your documents and ask questions about them."
)

st.divider()

question = st.text_input("Ask a question")

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Searching documents..."):

            result = ask(
                question=question,
                source=(
                    None
                    if selected_file == "All Documents"
                    else selected_file
                ),
                page = (
                    None
                    if selected_page in (None, "All Pages")
                    else selected_page
                ),
                verbose=True,
            )

        st.session_state["result"] = result

# -----------------------------
# Answer
# -----------------------------
st.divider()

st.subheader("Answer")

if "result" in st.session_state:
    st.write(st.session_state["result"]["answer"])

# -----------------------------
# Confidence
# -----------------------------
st.divider()

st.subheader("Confidence")

if "result" in st.session_state:

    confidence = st.session_state["result"]["confidence"]

    score = confidence.get("score", 0)

    progress = score / 100 if score > 1 else score

    st.progress(progress)

    st.write(f"Confidence Score: {score:.1f}%")
    st.write(f"Confidence Level: {confidence.get('level', 'Unknown')}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Confidence", f"{score:.2f}%")

    with col2:
        st.metric("Level", confidence.get("level", "Unknown"))

# -----------------------------
# Sources
# -----------------------------


st.divider()

if "result" in st.session_state:
    answer = st.session_state["result"]["answer"]
    sources = st.session_state["result"]["sources"]

    if sources:

        st.subheader("📚 Sources")

        cited_pages = {
            int(page)
            for page in re.findall(
                r"p\.\s*(\d+)",
                answer
            )
        }

        # -------------------------
        # Group by document
        # -------------------------
        grouped = {}

        for source in sources:

            filename = source.get("source", "Unknown")

            grouped.setdefault(filename, []).append(source)

        # -------------------------
        # Display documents
        # -------------------------

        for filename, doc_sources in grouped.items():

            filtered_sources = [
                s
                for s in doc_sources
                if len(s.get("text", "").strip()) >= 50
            ]

            unique_pages = len(
                {
                    s.get("page")
                    for s in filtered_sources
                }
            )
        
            # with st.container(border=True):
            
            #     st.markdown(f"## 📘 {filename}")
        
            #     st.caption(
            #         f"📑 Evidence from {unique_pages} page(s)"
            #     )
            st.markdown(f"## 📘 {filename}")
            st.caption(f"📑 Evidence from {unique_pages} page(s)")
        
            filtered_sources = sorted(
                filtered_sources,
                key=lambda x: (
                    x.get("page") not in cited_pages,
                    x.get("page") or 0,
                ),
            )

            # st.caption(
            #     f"📑 Evidence from {unique_pages} page(s)"
            # )

            filtered_sources = sorted(
                filtered_sources,
                key=lambda x: (
                    x.get("page") not in cited_pages,
                    x.get("page") or 0,
                ),
            )

            seen_pages = set()

            MAX_PASSAGES = 5
            if len(filtered_sources) > MAX_PASSAGES:

                st.info(
                    f"Showing first {MAX_PASSAGES} of "
                    f"{len(filtered_sources)} retrieved passages."
                )
            for source in filtered_sources[:MAX_PASSAGES]:

                page = source.get("page")

                # Remove duplicate pages
                if page in seen_pages:
                    continue

                seen_pages.add(page)

                full_text = source.get("text", "").strip()
                word_count = len(full_text.split())


                # if page in cited_pages:
                #     st.markdown(
                #         f"⭐ **Page {page} (Used in Answer)** • {word_count} words"
                #     )
                # else:
                #     st.markdown(
                #         f"📄 **Page {page}** • {word_count} words"
                #     )

                if page in cited_pages:
                    st.success("🟢 Referenced in Answer")
                    # st.markdown(
                    #     f"**📄 Page {page} • {word_count} words**"
                    # )
                else:
                    st.info("📚 Retrieved as Supporting Context")
                    st.markdown(
                        f"**📄 Page {page} • {word_count} words**"
                    )


                # Better preview
            
                preview = make_preview(full_text)
                preview = highlight_query(
                    preview,
                    question,
                )

                with st.container(border=True):
                    st.caption("Passage Preview")
                    st.markdown(f"> {preview}")

                with st.expander(
                    f"📖 View Full Passage (Page {page})"
                ):
                    # st.write(full_text)
                    st.code(full_text, language=None)

                st.divider()

    else:

        st.info(
            "No supporting passages were found."
        )


# streamlit run streamlit_app.py
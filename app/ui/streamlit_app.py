import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Enterprise RAG")
st.write("Ask questions about your documents.")

question = st.text_input(
    "Ask a question",
    placeholder="Example: What is motivation?"
)

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching documents..."):

        response = requests.post(
            API_URL,
            json={"question": question}
        )

    if response.status_code != 200:
        st.error("API Error")
        st.write(response.text)
        st.stop()

    data = response.json()

    st.divider()

    st.subheader("Answer")

    st.write(data["answer"])

    st.divider()

    st.subheader("Sources")

    for source in data["sources"]:

        with st.expander(
            f"{source['source']} | Page {source['page']}"
        ):
            st.write(f"Similarity Score: {source['score']:.4f}")
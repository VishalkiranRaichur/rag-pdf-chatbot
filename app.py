import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from src.chunker import chunk_text
from src.embedder import create_vector_store
from src.generator import generate_answer
from src.loader import load_pdf
from src.retriever import retrieve_relevant_chunks

load_dotenv()

st.set_page_config(page_title="PDF Chatbot", page_icon="📄")
st.title("📄 PDF Chatbot")
st.write("Upload a PDF and ask questions about its content.")

if not os.getenv("OPENAI_API_KEY"):
    st.error("Set OPENAI_API_KEY in your .env file before using the app.")
    st.stop()

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    if (
        "vector_store" not in st.session_state
        or st.session_state.get("file_name") != uploaded_file.name
    ):
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                text = load_pdf(tmp_path)
                chunks = chunk_text(text)
                st.session_state.vector_store = create_vector_store(chunks)
                st.session_state.file_name = uploaded_file.name
                st.session_state.num_chunks = len(chunks)
            finally:
                os.unlink(tmp_path)

        st.success(
            f"Ready! Indexed {st.session_state.num_chunks} chunks from "
            f"**{uploaded_file.name}**."
        )

    query = st.text_input("Ask a question about the PDF")

    if query:
        with st.spinner("Finding answer..."):
            relevant_chunks = retrieve_relevant_chunks(
                query, st.session_state.vector_store
            )
            answer = generate_answer(query, relevant_chunks)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("Source chunks used"):
            for i, chunk in enumerate(relevant_chunks, start=1):
                st.markdown(f"**Chunk {i}**")
                st.write(chunk)

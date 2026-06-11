import os
import tempfile
import traceback

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF Chatbot", page_icon="📄")

MAX_FILE_SIZE_MB = 15
LARGE_FILE_WARNING_MB = 5


def debug(msg: str) -> None:
    """Log to terminal and UI debug panel (main thread only)."""
    print(f"[DEBUG] {msg}", flush=True)
    if "debug_messages" not in st.session_state:
        st.session_state.debug_messages = []
    st.session_state.debug_messages.append(msg)


def show_debug_panel() -> None:
    messages = st.session_state.get("debug_messages", [])
    if messages:
        with st.expander("Debug log", expanded=False):
            for msg in messages:
                st.caption(msg)


# --- UI renders immediately; no heavy imports above this line ---
debug("App started — UI rendering")

st.title("📄 PDF Chatbot")
st.write("Upload a PDF and ask questions about its content.")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Set OPENAI_API_KEY in your .env file before using the app.")
    show_debug_panel()
    st.stop()

debug("OPENAI_API_KEY found")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    file_bytes = uploaded_file.getvalue()
    file_size_mb = len(file_bytes) / (1024 * 1024)
    debug(f"Uploaded file received: {uploaded_file.name} ({file_size_mb:.2f} MB)")

    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(
            f"PDF is too large ({file_size_mb:.1f} MB). "
            f"Maximum allowed size is {MAX_FILE_SIZE_MB} MB."
        )
        show_debug_panel()
        st.stop()

    if file_size_mb > LARGE_FILE_WARNING_MB:
        st.warning(
            f"Large PDF ({file_size_mb:.1f} MB). Processing may take a minute."
        )

    already_processed = st.session_state.get("file_name") == uploaded_file.name
    has_vector_store = "vector_store" in st.session_state
    needs_processing = not already_processed or not has_vector_store

    if needs_processing and st.session_state.get("processing_error"):
        st.session_state.pop("processing_error", None)

    if needs_processing:
        for key in ("vector_store", "file_name", "num_chunks"):
            st.session_state.pop(key, None)

        with st.spinner("Processing PDF..."):
            tmp_path = None
            try:
                debug("Creating temp file...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp_path = tmp.name
                    debug(f"Temp file created: {tmp_path}")

                    debug("Writing uploaded bytes to temp file...")
                    tmp.write(file_bytes)
                    debug(f"Temp file written ({len(file_bytes)} bytes)")

                debug("PDF extraction started...")
                from src.loader import load_pdf

                text = load_pdf(tmp_path)
                debug(f"PDF extraction completed: {len(text)} characters")

                debug("Chunking started...")
                from src.chunker import chunk_text

                chunks = chunk_text(text)
                debug(f"Chunking completed: {len(chunks)} chunks")

                debug("TF-IDF indexing started...")
                from src.embedder import create_vector_store

                vector_store = create_vector_store(chunks)
                debug("TF-IDF indexing completed")

                st.session_state.vector_store = vector_store
                st.session_state.file_name = uploaded_file.name
                st.session_state.num_chunks = len(chunks)
                st.session_state.pop("processing_error", None)
                st.rerun()

            except RuntimeError as e:
                st.error(str(e))
                debug(f"Processing error: {e}")
                st.session_state.processing_error = str(e)
                st.session_state.file_name = uploaded_file.name
            except Exception as e:
                msg = f"Failed to process PDF: {e}"
                st.error(msg)
                debug(traceback.format_exc())
                st.session_state.processing_error = msg
                st.session_state.file_name = uploaded_file.name
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    debug("Temp file deleted")

    elif st.session_state.get("processing_error"):
        st.error(st.session_state.processing_error)

    if "vector_store" in st.session_state:
        st.success(
            f"Ready! Indexed {st.session_state.num_chunks} chunks from "
            f"**{uploaded_file.name}**."
        )

        query = st.text_input("Ask a question about the PDF")

        if query:
            debug(f"Question received: {query[:80]}")
            with st.spinner("Finding answer..."):
                relevant_chunks = []
                answer = ""

                try:
                    debug("Retrieval started")
                    from src.retriever import retrieve_relevant_chunks

                    relevant_chunks = retrieve_relevant_chunks(
                        query, st.session_state.vector_store
                    )
                    debug(f"Retrieval completed: {len(relevant_chunks)} chunks")

                    debug("Generation started")
                    from src.generator import fallback_answer, generate_answer

                    try:
                        answer = generate_answer(query, relevant_chunks)
                        debug("Generation completed")
                    except Exception as e:
                        st.error(str(e))
                        debug(f"Generation failed: {e}")
                        answer = fallback_answer(query, relevant_chunks)
                        debug("Using fallback answer from retrieved chunks")

                    st.subheader("Answer")
                    st.write(answer)

                    with st.expander("Source chunks used"):
                        for i, chunk in enumerate(relevant_chunks, start=1):
                            st.markdown(f"**Chunk {i}**")
                            st.write(chunk)

                except Exception as e:
                    st.error(f"Failed to retrieve relevant chunks: {e}")
                    debug(traceback.format_exc())

show_debug_panel()

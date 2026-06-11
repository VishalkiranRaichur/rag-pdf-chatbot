from sklearn.feature_extraction.text import TfidfVectorizer


def create_vector_store(chunks: list[str]) -> dict:
    """
    Build a local TF-IDF index over text chunks.
    Returns vectorizer, sparse matrix, and original chunks.
    """
    if not chunks:
        raise ValueError("Cannot create vector store from an empty chunks list.")

    print(f"[DEBUG] TF-IDF indexing started for {len(chunks)} chunks", flush=True)

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(chunks)

    print(
        f"[DEBUG] TF-IDF indexing completed: {matrix.shape[0]} chunks, "
        f"{matrix.shape[1]} features",
        flush=True,
    )

    return {"vectorizer": vectorizer, "matrix": matrix, "chunks": chunks}

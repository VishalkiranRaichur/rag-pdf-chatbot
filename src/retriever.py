from sklearn.metrics.pairwise import cosine_similarity


def retrieve_relevant_chunks(query: str, vector_store: dict, k: int = 3) -> list[str]:
    """Find the k most relevant chunks for a query using TF-IDF cosine similarity."""
    print(f"[DEBUG] retrieval started for query: {query[:80]}", flush=True)

    vectorizer = vector_store["vectorizer"]
    matrix = vector_store["matrix"]
    chunks = vector_store["chunks"]

    k = min(k, len(chunks))
    print(f"[DEBUG] transforming query with TF-IDF vectorizer", flush=True)
    query_vector = vectorizer.transform([query])

    print(f"[DEBUG] computing cosine similarity across {len(chunks)} chunks", flush=True)
    scores = cosine_similarity(query_vector, matrix).flatten()
    top_indices = scores.argsort()[-k:][::-1]

    results = [chunks[i] for i in top_indices]
    print(f"[DEBUG] retrieval completed: {len(results)} chunks", flush=True)
    return results

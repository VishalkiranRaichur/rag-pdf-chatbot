import numpy as np

from src.embedder import get_embeddings


def retrieve_relevant_chunks(query: str, vector_store: dict, k: int = 3) -> list[str]:
    """Find the k most relevant chunks for a query using FAISS similarity search."""
    query_embedding = get_embeddings([query])[0]
    query_vector = np.array([query_embedding], dtype=np.float32)

    num_chunks = len(vector_store["chunks"])
    k = min(k, num_chunks)

    _, indices = vector_store["index"].search(query_vector, k)
    return [vector_store["chunks"][i] for i in indices[0]]

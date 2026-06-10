import os

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

EMBEDDING_MODEL = "text-embedding-3-small"


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Get OpenAI embeddings for a list of text strings."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def create_vector_store(chunks: list[str]) -> dict:
    """
    Embed chunks and store them in a local FAISS index.
    Returns a dict with the FAISS index and the original chunks.
    """
    embeddings = get_embeddings(chunks)
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    vectors = np.array(embeddings, dtype=np.float32)
    index.add(vectors)

    return {"index": index, "chunks": chunks}

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CHAT_MODEL = "gpt-4o-mini"
API_TIMEOUT_SECONDS = 20


def fallback_answer(query: str, relevant_chunks: list[str]) -> str:
    """Return a simple answer using retrieved chunks when OpenAI is unavailable."""
    if not relevant_chunks:
        return "No relevant information found in the document."

    context = "\n\n---\n\n".join(relevant_chunks)
    return (
        f"(OpenAI unavailable — showing retrieved excerpts for: \"{query}\")\n\n"
        f"{context}"
    )


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key, timeout=API_TIMEOUT_SECONDS)


def generate_answer(query: str, relevant_chunks: list[str]) -> str:
    """Generate an answer using retrieved chunks as context."""
    context = "\n\n".join(relevant_chunks)
    client = _get_client()

    print("[DEBUG] calling client.chat.completions.create...", flush=True)

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Answer the question using only "
                        "the provided context. If the answer is not in the context, "
                        "say you don't know."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
        )
    except Exception as e:
        raise RuntimeError(f"OpenAI chat completion failed: {e}") from e

    print("[DEBUG] client.chat.completions.create completed", flush=True)
    return response.choices[0].message.content

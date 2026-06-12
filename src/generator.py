import os

from dotenv import load_dotenv

load_dotenv()

CHAT_MODEL = "gpt-4o-mini"
API_TIMEOUT_SECONDS = 20


def fallback_answer(query: str, relevant_chunks: list[str]) -> str:
    """Return an instant answer using the top retrieved chunks."""
    if not relevant_chunks:
        return "No relevant information found in the document."

    context = "\n\n---\n\n".join(relevant_chunks)
    return (
        f"Top excerpts from the document for: \"{query}\"\n\n"
        f"{context}"
    )


def _get_client():
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key, timeout=API_TIMEOUT_SECONDS)


def generate_answer(query: str, relevant_chunks: list[str]) -> str:
    """Generate an answer using retrieved chunks as context."""
    print("[DEBUG] Entered generate_answer", flush=True)

    context = "\n\n".join(relevant_chunks)

    print("[DEBUG] Creating OpenAI client", flush=True)
    client = _get_client()
    print("[DEBUG] OpenAI client created", flush=True)

    print("[DEBUG] Calling OpenAI", flush=True)
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

    print("[DEBUG] OpenAI response received", flush=True)
    return response.choices[0].message.content

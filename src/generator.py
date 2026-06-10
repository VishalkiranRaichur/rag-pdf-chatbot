import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CHAT_MODEL = "gpt-4o-mini"


def generate_answer(query: str, relevant_chunks: list[str]) -> str:
    """Generate an answer using retrieved chunks as context."""
    context = "\n\n".join(relevant_chunks)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    return response.choices[0].message.content

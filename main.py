import os

from dotenv import load_dotenv

from src.chunker import chunk_text
from src.embedder import create_vector_store
from src.generator import generate_answer
from src.loader import load_pdf
from src.retriever import retrieve_relevant_chunks

load_dotenv()


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Set OPENAI_API_KEY in your .env file.")
        return

    file_path = "data/sample.pdf"
    query = input("Ask a question about the PDF: ").strip()

    if not query:
        print("No question provided.")
        return

    print(f"Loading PDF from: {file_path}")
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks. Building vector store...")

    vector_store = create_vector_store(chunks)
    relevant_chunks = retrieve_relevant_chunks(query, vector_store)
    answer = generate_answer(query, relevant_chunks)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()

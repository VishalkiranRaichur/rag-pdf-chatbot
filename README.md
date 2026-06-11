# PDF Chatbot (RAG-Based Question Answering System)

## Overview

This project is a Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their contents. The application extracts text from PDFs, splits the content into chunks, retrieves the most relevant sections for a user query, and generates answers using OpenAI's language models.

## Features

* Upload PDF documents
* Automatic text extraction
* Intelligent text chunking
* TF-IDF based document retrieval
* OpenAI-powered answer generation
* Interactive Streamlit web interface
* Source chunk display for transparency

## Tech Stack

* Python
* Streamlit
* OpenAI API
* Scikit-learn
* PyMuPDF
* NumPy

## Project Structure

```text
rag-system/
│
├── app.py
├── requirements.txt
├── .env.example
│
├── src/
│   ├── loader.py
│   ├── chunker.py
│   ├── retriever.py
│   ├── generator.py
│   └── embedder.py
│
└── data/
```

## How It Works

1. User uploads a PDF.
2. Text is extracted using PyMuPDF.
3. The text is divided into manageable chunks.
4. TF-IDF indexing is created.
5. Relevant chunks are retrieved for each question.
6. OpenAI generates an answer using the retrieved context.
7. The answer is displayed along with supporting chunks.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd rag-system
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## Future Improvements

* Multi-PDF support
* Chat history
* Vector databases (FAISS, Pinecone, Chroma)
* Semantic search embeddings
* PDF summarization
* Citation highlighting

## Author

Vishalkiran Raichur

Data Science Student

San José State University

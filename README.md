# AI-Powered PDF Chatbot (RAG-Based Question Answering System)

An AI-powered PDF chatbot that allows users to upload PDF documents and ask natural language questions about their content. The system extracts text from uploaded PDFs, retrieves the most relevant sections using information retrieval techniques, and generates context-aware answers using OpenAI's GPT models.

---

## Why I Built This

While exploring Retrieval-Augmented Generation (RAG), I wanted to understand how modern AI systems combine document retrieval with Large Language Models to answer questions from custom data.

Instead of simply calling ChatGPT, I built an end-to-end pipeline that processes PDF documents, retrieves relevant information, and generates grounded responses based on the uploaded content.

This project helped me gain hands-on experience with:

* Retrieval-Augmented Generation (RAG)
* Document processing pipelines
* OpenAI API integration
* Information retrieval techniques
* Streamlit application development
* Debugging real-world software systems

---

## Features

* Upload PDF documents
* Extract text automatically from uploaded files
* Split large documents into manageable chunks
* TF-IDF based document retrieval
* OpenAI-powered answer generation
* Display source chunks used for answering
* Interactive Streamlit web interface
* Modular and extensible architecture

---

## System Architecture

```text
User Uploads PDF
         │
         ▼
  PDF Text Extraction
         │
         ▼
     Chunking
         │
         ▼
   TF-IDF Indexing
         │
         ▼
 User Question
         │
         ▼
 Retrieve Relevant Chunks
         │
         ▼
 OpenAI GPT-4o-mini
         │
         ▼
 Generated Answer
         │
         ▼
 Answer + Source Chunks
```

---

## Tech Stack

### Languages

* Python

### AI / Machine Learning

* OpenAI GPT-4o-mini
* TF-IDF Retrieval
* Scikit-learn

### Frameworks & Libraries

* Streamlit
* PyMuPDF
* NumPy
* python-dotenv

### Tools

* Git
* GitHub
* VS Code / Cursor

---

## Project Structure

```text
rag-pdf-chatbot/
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
└── assets/
```

---

## How It Works

### 1. PDF Upload

Users upload a PDF document through the Streamlit interface.

### 2. Text Extraction

The system extracts text from each page using PyMuPDF.

### 3. Chunking

The extracted text is divided into smaller chunks to improve retrieval efficiency.

### 4. Retrieval

TF-IDF vectorization is used to identify the most relevant chunks for a given question.

### 5. Answer Generation

The retrieved context is passed to OpenAI GPT-4o-mini, which generates an answer grounded in the document content.

### 6. Transparency

The source chunks used for answering are displayed alongside the response.

---

## Demo

### Upload PDF

*Add screenshot here*

### Example Output

Question:

> Summarize this project in 3 sentences.

Answer:

> The project aims to create an AI-based tool that generates dyslexia-friendly educational content by analyzing and simplifying text using Natural Language Processing techniques. It improves readability by addressing complex vocabulary, long sentences, and poor formatting while potentially incorporating text-to-speech functionality. The system promotes inclusive education and supports students with dyslexia as well as educators preparing accessible learning materials.

---

## Challenges & Lessons Learned

Building this project involved significantly more debugging than coding.

Some of the challenges I encountered included:

* Integrating and authenticating with OpenAI APIs
* Managing Streamlit reruns and session state
* Handling PDF processing edge cases
* Improving retrieval quality
* Resolving package and dependency conflicts
* Debugging Git and repository synchronization issues
* Understanding how retrieval and generation work together in a RAG pipeline

Working through these problems gave me valuable experience building and troubleshooting AI-powered applications.

---

## Future Improvements

* Replace TF-IDF retrieval with semantic embeddings
* Integrate FAISS or Pinecone for vector search
* Support multiple PDFs simultaneously
* Add conversational memory and chat history
* Highlight exact document citations
* Deploy using Docker and cloud infrastructure
* Add authentication and document management

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/rag-pdf-chatbot.git
cd rag-pdf-chatbot
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

---

## Author

**Vishalkiran Raichur**

Data Science Student at 
San José State University

Interested in:

* Artificial Intelligence
* Machine Learning
* NLP
* Quantitative Finance
* Software Engineering

---

## Key Takeaway

This project taught me how modern AI applications combine retrieval systems with large language models to answer questions using custom data rather than relying solely on model memory. It was my first complete end-to-end RAG application and provided valuable experience in building, debugging, and deploying AI-powered software.

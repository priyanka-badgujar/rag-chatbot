# RAG Chatbot

A small Streamlit-based retrieval-augmented generation (RAG) chatbot for asking questions over PDF documents.

## Overview

This project lets you upload a PDF, extract its text, split the text into chunks, build embeddings using OpenAI, and then answer user questions by retrieving relevant chunks and generating responses with a chat model.

## Features

- Upload a PDF document via Streamlit UI
- Extract text from PDF pages using `pdfplumber`
- Split text into chunks using `RecursiveCharacterTextSplitter`
- Generate OpenAI embeddings with `OpenAIEmbeddings`
- Store vectors in a FAISS index
- Use a chat model (`ChatOpenAI`) to answer questions from the document content

## Requirements

- Python 3.8+
- `streamlit`
- `pdfplumber`
- `langchain`
- `langchain-openai`
- `langchain-community`
- `langchain-core`
- `openai`
- `faiss-cpu`
- `tiktoken`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository.
2. Install dependencies.
3. Replace the placeholder OpenAI API key in `ragchatbot.py` with your actual key, or update the app to load it from an environment variable.

```python
OPENAI_API_KEY = "pb-xxxxxx"
```

## Run

Start the Streamlit app from the project root:

```bash
streamlit run ragchatbot.py
```

Then open the URL shown in the terminal.

## Usage

1. Upload a PDF file using the sidebar.
2. Enter a question in the text input field.
3. The app will retrieve relevant document chunks and generate an answer.

## Notes

- The current implementation stores embeddings in memory only, so re-uploading or restarting the app rebuilds the FAISS index.
- For production use, consider securing the OpenAI API key and avoiding hardcoded credentials in source code.

## Project Structure

- `ragchatbot.py` - main Streamlit application
- `requirements.txt` - Python dependencies
- `pyproject.toml` - project metadata and packaging

## License

This project does not include a license file. Add one if you want to specify reuse terms.

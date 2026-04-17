# RAG Chatbot Technical Documentation

## Project Overview
- Python-based Streamlit application for PDF Q&A using Retrieval-Augmented Generation (RAG).
- Ingests a PDF from user upload, extracts text, splits into chunks, computes embeddings, stores them in FAISS, and uses an LLM to answer user queries with contextual documents.

## Key Files
- `ragchatbot.py`: Main Streamlit application code.
- `pyproject.toml`: Project metadata and package config.
- `requirements.txt`: Dependencies.
- `src/chatbot`: Package impl (module skeleton).

## Dependencies
- streamlit: provides web UI components (file uploader, text input, output rendering, app state).

```python
import streamlit as st
st.header('My First Chatbot')
with st.sidebar:
    file = st.file_uploader('Upload a PDF file and start asking questions', type='pdf')
    user_question = st.text_input('Type your question here')
```

- pdfplumber: extracts page-level plain text from PDF files (supports fonts, line joins, and layout retention).

```python
import pdfplumber
with pdfplumber.open(file) as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text() + '\n'
```

- langchain_text_splitters: splits long text into overlapping chunks to preserve context while enabling vector retrieval.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', '. ', ' ', ''],
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_text(text)
```

- langchain_community: includes community-supported vector stores and utilities like FAISS wrappers for fast semantic search.

```python
from langchain_community.vectorstores import FAISS
vector_store = FAISS.from_texts(chunks, embeddings)
retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k': 4})
```

- langchain_openai: integrates OpenAI APIs for embeddings and chat models, with config helpers.

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
embeddings = OpenAIEmbeddings(model='text-embedding-3-small', openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=OPENAI_API_KEY, temperature=0.3, max_tokens=1000)
```

- langchain_core: core chain abstractions (prompts, runnables, parsers) and glue code for pipeline construction.

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
prompt = ChatPromptTemplate.from_messages([
    ('system', '...'),
    ('human', '{question}')
])
chain = ({'context': retriever, 'question': RunnablePassthrough()} | prompt | llm | StrOutputParser())
```

- openai: low-level OpenAI client enabling embedding and LLM requests.

```python
import openai
# implicit via langchain_openai wrappers; can also use openai directly for custom calls.
```

- faiss-cpu: FAISS vector index on CPU for fast similarity search in embeddings.

```python
# FAISS is used via langchain_community vector store.
```

- tiktoken: tokenizer for OpenAI models and token counting, ensures chunk sizes fit context windows.

```python
import tiktoken
# Use tokenization for awareness of model token limits when splitting text.
```

## Setup
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `streamlit run ragchatbot.py`

## `ragchatbot.py` workflow
1. User uploads a PDF.
2. PDF is opened with `pdfplumber`.
3. Text from all pages is concatenated.
4. `RecursiveCharacterTextSplitter` breaks text into overlapping chunks.
5. `OpenAIEmbeddings` computes vector representations for each chunk.
6. `FAISS.from_texts` creates a local vector index with these embeddings.
7. User enters question; retriever performs similarity search.
8. `ChatPromptTemplate` builds the prompt with system/human instructions.
9. `ChatOpenAI` generates answer using `gpt-4o-mini` (or configured model).
10. `RunnablePassthrough` + `StrOutputParser` connect retrieving pipeline to output UI.

## Design notes
- `chunk_size=1000`, `chunk_overlap=200` balances retrieval recall vs vector count.
- `search_type='mmr'` for diverse top results.
- The system prompt emphasizes factual, context-grounded answers and failure handling.

## Troubleshooting
- `ModuleNotFoundError`: Ensure venv is activated and `pip install -r requirements.txt` executed.
- Langchain paths: use `langchain_text_splitters` + `langchain_community`; not obsolete `langchain.text_splitter`.
- If OpenAI key missing, set env var `OPENAI_API_KEY` or direct assignment.

## Optional improvements
- Add `st.cache_data` to avoid recompute on repeated uploads.
- Support DOCX / PPTX input loaders.
- Add user login & session history.
- Add model selection UI and chunk feedback loop.

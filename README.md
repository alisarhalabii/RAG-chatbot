# RAG Chatbot

A production-style Retrieval-Augmented Generation (RAG) chatbot built to demonstrate the full engineering chain: data ingestion → vector search → LLM generation → REST API.

## What it does

1. Ingests documents from `data/raw/` and splits them into chunks
2. Embeds chunks using `all-MiniLM-L6-v2` (runs locally, no API key needed)
3. Stores embeddings in ChromaDB (vector database)
4. On query: embeds the question, retrieves the most relevant chunks, sends them as context to an LLM
5. Exposes a REST API via FastAPI

## Tech stack

- **Python 3.13** with src-layout and editable install
- **LangChain** — LCEL chain for retrieval and generation
- **ChromaDB** — local vector database
- **sentence-transformers** — local embeddings (all-MiniLM-L6-v2)
- **Ollama + llama3.2** — local LLM, no cloud required
- **FastAPI + uvicorn** — REST API with auto-generated Swagger docs

## Project structure
src/rag_chatbot/
├── config.py      # paths and model settings
├── ingest.py      # load → chunk → embed → store
├── retrieve.py    # query vector database
├── generate.py    # LangChain chain: retrieve → prompt → LLM
└── api.py         # FastAPI endpoints

## Getting started

Requirements: Python 3.11+, Ollama installed and running (https://ollama.com)

```bash
git clone https://github.com/alisarhalabii/RAG-chatbot.git
cd RAG-chatbot
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -e .
pip install sentence-transformers chromadb langchain langchain-ollama langchain-chroma fastapi uvicorn ollama

ollama pull llama3.2

# Place .txt files in data/raw/, then:
python -m rag_chatbot.ingest

uvicorn rag_chatbot.api:app --reload
```

Open http://localhost:8000/docs for interactive API documentation.

## API

### POST /chat

Request:
```json
{ "text": "What is RAG?" }
```

Response:
```json
{ "answer": "RAG stands for Retrieval-Augmented Generation..." }
```

### GET /health

```json
{ "status": "ok" }
```

## Roadmap

- [x] Local RAG pipeline with ChromaDB
- [x] LangChain LCEL chain
- [x] FastAPI REST API
- [ ] Azure OpenAI integration
- [ ] Terraform infrastructure as code
- [ ] CI/CD with GitHub Actions
- [ ] React/TypeScript frontend
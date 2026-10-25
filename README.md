# RAG Chatbot

A production-style Retrieval-Augmented Generation (RAG) chatbot with a real chat UI: data ingestion → vector search → LLM generation → REST API → Next.js frontend, deployed live.

**Live demo:** _add your deployed URL here once it's live_

## What it does

- Ingests documents from `data/raw/` and splits them into chunks
- Embeds chunks using `all-MiniLM-L6-v2` (runs locally, no API key needed)
- Stores embeddings in ChromaDB (vector database)
- On query: embeds the question, retrieves the most relevant chunks, sends them as context to an LLM, and returns the answer together with which source documents it used
- Exposes a REST API via FastAPI
- A Next.js chat UI talks to that API — the same interface you'd put on a portfolio

## Tech stack

**Backend**
- Python 3.11+, src-layout, editable install
- LangChain — retrieval + generation pipeline
- ChromaDB — local vector database
- sentence-transformers — local embeddings (`all-MiniLM-L6-v2`)
- **Groq** (cloud LLM, e.g. Llama 3.1) for the deployed version — free tier, no GPU needed. **Ollama** is still supported for fully offline local development.
- FastAPI + uvicorn — REST API with auto-generated Swagger docs

**Frontend**
- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- Plain `fetch` against the FastAPI backend — no extra state library needed for a chat this size

## Project structure

```
src/rag_chatbot/
├── config.py     # paths, model + provider settings (env-driven)
├── ingest.py     # load → chunk → embed → store
├── retrieve.py   # standalone CLI for querying the vector db directly
├── generate.py   # retrieval + prompt + LLM, returns answer + sources
└── api.py        # FastAPI endpoints (/chat, /health) with CORS

frontend/
├── app/          # Next.js App Router pages
├── components/   # ChatInput, MessageBubble, ThemeToggle, TypingIndicator
└── lib/          # API client + shared types
```

## Getting started (local development)

### Backend

Requirements: Python 3.11+. Optionally Ollama (https://ollama.com) if you want to run fully offline.

```bash
git clone https://github.com/alisarhalabii/RAG-chatbot.git
cd RAG-chatbot
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -e .

cp .env.example .env
# Edit .env:
#   - Get a free Groq API key at https://console.groq.com and set GROQ_API_KEY
#   - Or set LLM_PROVIDER=ollama to use a local model instead (run `ollama pull llama3.2` first)

# Place .txt files in data/raw/, then:
python -m rag_chatbot.ingest

uvicorn rag_chatbot.api:app --reload
```

Backend runs at http://localhost:8000 — interactive API docs at http://localhost:8000/docs.

### Frontend

Requirements: Node.js 18+.

```bash
cd frontend
npm install
cp .env.local.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:3000.

## API

### `POST /chat`

Request:
```json
{ "text": "What is RAG?" }
```

Response:
```json
{
  "answer": "RAG stands for Retrieval-Augmented Generation...",
  "sources": ["test.txt"]
}
```

### `GET /health`
```json
{ "status": "ok" }
```

## Deployment

**Backend → Render**
1. Push this repo to GitHub.
2. In Render: New → Blueprint → connect the repo (it picks up `render.yaml`).
3. Set the `GROQ_API_KEY` environment variable in the Render dashboard (get one free at https://console.groq.com).
4. After the first deploy, copy the Render URL (e.g. `https://rag-chatbot-api.onrender.com`) and update `ALLOWED_ORIGINS` to include your Vercel URL once you have it.

**Frontend → Vercel**
1. In Vercel: New Project → import the same GitHub repo → set the root directory to `frontend`.
2. Add an environment variable `NEXT_PUBLIC_API_URL` = your Render backend URL.
3. Deploy. Vercel gives you a live URL you can put straight on your portfolio.

Note: Render's free tier spins down after inactivity, so the first request after a while can take ~30-50 seconds to wake up. That's expected on a free plan, not a bug.

## Roadmap

- [x] Local RAG pipeline with ChromaDB
- [x] LangChain retrieval + generation pipeline
- [x] FastAPI REST API
- [x] Next.js chat UI
- [x] Live deployment (Vercel + Render)
- [ ] Streaming responses (token-by-token)
- [ ] File upload in the UI (ingest documents without touching the CLI)
- [ ] CI/CD with GitHub Actions
- [ ] Terraform infrastructure as code

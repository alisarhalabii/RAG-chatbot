from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_chatbot.config import ALLOWED_ORIGINS
from rag_chatbot.generate import build_chain

app = FastAPI(title="RAG Chatbot API")

# Let the frontend (local dev + the deployed Vercel app) call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chain = build_chain()


class Question(BaseModel):
    text: str


class Answer(BaseModel):
    answer: str
    sources: list[str]


@app.post("/chat", response_model=Answer)
def chat(question: Question):
    if not question.text.strip():
        raise HTTPException(status_code=400, detail="text cannot be empty")
    return chain(question.text)


@app.get("/health")
def health():
    return {"status": "ok"}

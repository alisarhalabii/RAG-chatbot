from fastapi import FastAPI
from pydantic import BaseModel
from rag_chatbot.generate import build_chain


app = FastAPI()
chain= build_chain()


class Question(BaseModel):
    text:str

@app.post("/chat")
def chat(question: Question):
    answer = chain.invoke(question.text)
    return {"answer": answer}

@app.get("/health")
def health():
    return{"status": "ok"}

  
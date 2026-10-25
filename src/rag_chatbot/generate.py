from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from rag_chatbot.config import (
    CHROMA_DIR,
    EMBEDDING_MODEL,
    LLM_PROVIDER,
    GROQ_API_KEY,
    GROQ_MODEL,
    OLLAMA_MODEL,
)


class LocalEmbeddings(Embeddings):
    """Wrapper som lar LangChain bruke sentence-transformers."""

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def get_llm():
    """Pick the LLM backend based on LLM_PROVIDER.

    - "groq": a free/cheap cloud API. Used in production so the chatbot works
      without anyone needing a local GPU or Ollama installed.
    - "ollama": a fully local model. Useful for offline development.
    """
    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq

        if not GROQ_API_KEY:
            raise RuntimeError(
                "LLM_PROVIDER is 'groq' but GROQ_API_KEY is not set. "
                "Get a free key at https://console.groq.com and add it to your .env file, "
                "or set LLM_PROVIDER=ollama to use a local model instead."
            )
        return ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.2)

    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=OLLAMA_MODEL)

    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER!r} (expected 'groq' or 'ollama')")


PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful assistant. Answer based only on the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:"""
)


def build_chain():
    """Builds a callable RAG pipeline: question (str) -> {"answer": str, "sources": [str]}.

    Returning the source filenames alongside the answer lets the UI show the
    user which documents the answer was grounded in.
    """
    embeddings = LocalEmbeddings()
    vectorstore = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
    collection_metadata={"hnsw:space": "cosine"},
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()
    answer_chain = PROMPT | llm | StrOutputParser()

    def answer_with_sources(question: str) -> dict:
        docs = retriever.invoke(question)
        answer = answer_chain.invoke({"context": format_docs(docs), "question": question})
        sources = sorted({doc.metadata.get("source", "unknown") for doc in docs})
        return {"answer": answer, "sources": sources}

    return answer_with_sources


if __name__ == "__main__":
    chain = build_chain()
    result = chain("What is RAG?")
    print(result["answer"])
    print("Sources:", result["sources"])

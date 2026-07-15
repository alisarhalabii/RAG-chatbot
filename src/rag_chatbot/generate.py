from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from rag_chatbot.config import CHROMA_DIR, EMBEDDING_MODEL


class LocalEmbeddings(Embeddings):
    """Wrapper som lar LangChain bruke sentence-transformers."""
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()


def build_chain():
    embeddings = LocalEmbeddings()
    vectorstore = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer based only on the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}

Answer:""")

    llm = ChatOllama(model="llama3.2")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


if __name__ == "__main__":
    chain = build_chain()
    answer = chain.invoke("What is RAG?")
    print(answer)
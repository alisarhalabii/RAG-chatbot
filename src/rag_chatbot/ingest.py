from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

from rag_chatbot.config import (
    RAW_DATA_DIR,
    CHROMA_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def load_documents(directory: Path) -> list[dict]:
    """read all .txt files in dir. return list with [text, source]"""
    documents= []
    for path in directory.glob("*txt"):
        text= path.read_text(encoding="utf-8")
        documents.append({"text": text, "source": path.name})

    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Splitting documents into smaller chunks"""
    splitting= RecursiveCharacterTextSplitter(
        chunk_size= CHUNK_SIZE,
        chunk_overlap= CHUNK_OVERLAP,
    )
    chunks = []
    for doc in documents:
        splits = splitting.split_text(doc["text"])
        for i, split in enumerate(splits):
            chunks.append({"text": split, "source": doc["source"], "chunk_id": i})
    return chunks

def embed_and_store(chunks: list[dict]) -> None:
    """Embedding chunks and storing in chroma"""
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection("documents")

    texts= [c["text"] for c in chunks]
    embeddings = model.encode(texts).tolist()
    ids= [f"{c['source']}-{c['chunk_id']}" for c in chunks] 
    metadatas= [{"source": c["source"]} for c in chunks]

    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)
    print(f"Saved {len(chunks)} chunks in Chroma")



if __name__ == "__main__":
    docs= load_documents(RAW_DATA_DIR)
    print(f"Read {len(docs)} documents")
    chunks= chunk_documents(docs)
    print(f"Chunking to {len(chunks)} chunks")
    embed_and_store(chunks)

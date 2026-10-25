from sentence_transformers import SentenceTransformer
import chromadb

from rag_chatbot.config import CHROMA_DIR, EMBEDDING_MODEL

def query(question: str, n_results: int= 3) -> list[dict]:
    """Find the n most relevant chunks for a users query"""
    model = SentenceTransformer(EMBEDDING_MODEL)
    client= chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
    "documents",
    metadata={"hnsw:space": "cosine"},
)

    question_embedding= model.encode(question).tolist()
    
    results= collection.query(
        query_embeddings=[question_embedding],
        n_results= n_results,
    )

    chunks= []
    for i, doc in enumerate(results["documents"][0]):
        chunks.append({
            "text":doc,
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i],
        })
    return chunks



if __name__ == "__main__":
    results= query("Can you explain what RAG is?")
    for r in results:
        print(f"[{r['source']} | distance: {r['distance']:.4f}]")
        print(r["text"])
        print()

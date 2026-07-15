import ollama
from rag_chatbot.retrieve import query


def generate(question: str) -> str:
    """Hent relevante chunks og generer svar med LLM."""
    chunks = query(question, n_results=3)

    context = "\n\n".join([c["text"] for c in chunks])

    prompt = f"""Du er en hjelpsom assistent. Bruk kun følgende kontekst for å svare.
Hvis svaret ikke finnes i konteksten, si at du ikke vet.

Kontekst:
{context}

Spørsmål: {question}

Svar:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    svar = generate("What is RAG?")
    print(svar)
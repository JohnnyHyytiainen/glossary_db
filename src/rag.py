# Kod: Engelska
# Kommentarer: Svenska
# Helper function som ska fungera som min context till min /ask endpoint

# Mina imports
import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import Any

# Hämtar API key via Pydantic settings
from src.config import settings

# Pathin variabel + koppla upp mot min skapade vector DB som innehåller hela databasen med glosor
# ===== 1) Databas setup ChromaDB =====
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection("glossary_terms")

# --- Embedding setup (SentenceTransformer) ---
# --- Laddar in exakt samma modell som används i embed_terms.py
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# ===== 2) AI setup (Grunden.ai via OpenAI kompatibelt API) =====
# base_url pekar om OpenAIklitenten mot Grunden.ai's server istället för OpenAI protokollet
# hur requests/responses ser ut är IDENTISKT med OpenAI
ai_client = OpenAI(
    api_key=settings.GRUNDEN_API_KEY,
    base_url="https://api.grunden.ai/v1",
)


# ===== Helper funktion för context hantering =====
def get_relevant_context(
    user_query: str, num_results: int = 5
) -> tuple[str, list[str]]:
    """Gets context and returns (context_string, list_of_sources)""" ""

    # Översätter users fråga till vektor innan fråga till ChromaDB skickas
    # normalize_embeddings=True för att matcha cosine matte
    query_vector = encoder.encode(user_query, normalize_embeddings=True).tolist()

    # 1) Fråga ChromaDB
    results = collection.query(query_embeddings=[query_vector], n_results=num_results)

    # 2) Hämta och packa upp min key+values bestående av en list med lists i sig.
    # 2) + hämta metadata för att hämta min SLUG
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 3) Sätt ihop listan till en lång str med simpel formattering för läsbarhet.
    # 3) Formatering för att underlätta för LLM och undvika framtida headaches
    context_string = "\n----\n".join(
        f"Term {i + 1}: {doc}" for i, doc in enumerate(documents)
    )

    # 4) Ta ut källorna(slugs) till user
    sources = [meta.get("slug") for meta in metadatas]

    return context_string, sources


# === Helper funktion för /search endpoint till mitt API ===
# === (Underlättar och söker i vektorDB och returnerar raw data för att kunna felsöka och se glosor DB tar fram)
def search_database(query: str, num_results: int = 5) -> list[dict[str, Any]]:
    """Searches the vector database and returns raw data.
    Used for troubleshooting and to see which words the database picks up.
    (/search)
    """
    # 1) Översätter frågan till matematisk vektor (Samma princip som för RAG)
    query_vector = encoder.encode(query, normalize_embeddings=True).tolist()

    # 2) Sök i vector DB(ChromaDB)
    results = collection.query(query_embeddings=[query_vector], n_results=num_results)

    # 3) Packa upp list bestående av nested lists som är nyckelns Value
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # 4) Zippa ihop all data
    formatted_results = []
    for docs, meta, dist in zip(documents, metadatas, distances):
        formatted_results.append(
            {
                "term": meta.get("term"),
                "slug": meta.get("slug"),
                "distance": round(dist, 4),  # Avrundar för formattering
                "sources": meta.get("sources") or [],
                "snippet": docs[:100] + "..",  # 100 första tecknen av glosan
            }
        )

    return formatted_results


# ===== Funktion för att generera RAG svar =====
def generate_rag_response(user_query: str) -> dict:
    """Main function for RAG: Get context and let LLM formulate an answer"""

    # 1) R (Retrieval), hämta faktan(user_query + slugs)
    # Hämtar kontext från ChromaDB
    context_text, source_slugs = get_relevant_context(user_query)

    # 2) A (Augmentation) - Injucera den hämtade kontexten i instruktionen, det är context_text
    # inbäddad i system_message som är augmenteringen
    system_message = f"""You are a pedagogical and highly skilled Data Engineering assistant.
    Answer the user's question using ONLY the context below. No hallucinations.
    Reply in the exact same language as the user's question.
    If the answer is not in the context, say so and suggest another search term.

    --- CONTEXT FROM DATABASE ---
    {context_text}"""

    # 3) G(Generation), skicka augmenterad kontext + fråga till LLM (GLM 5.1 via Grunden.ai)
    # OpenAI-format: Svaret sitter i choices[0].message.content
    response = ai_client.chat.completions.create(
        model="glm-5.1",
        messages=[
            {
                "role": "system",
                "content": system_message,
            },  # <-- instruktioner + kontext
            {"role": "user", "content": user_query},  # <-- bara frågan
        ],
    )

    # Returnera en dict med både AI svaret och sources
    return {"answer": response.choices[0].message.content, "sources": source_slugs}


# --- Testblock ---
# Allt under if __name__ == "__main__": körs BARA om jag kör just denna fil i terminalen.
if __name__ == "__main__":
    print("Testar RAG-motorn...\n")
    # Test prints. Ställa fråga som question består av
    test_question = "What does DRY mean?"

    print(f"Fråga: '{test_question}'")
    print(f"\n")
    svar = generate_rag_response(test_question)

    print("\n--- SVAR ---")
    print(svar)

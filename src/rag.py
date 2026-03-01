# Kod: Engelska
# Kommentarer: Svenska
# Helper function som ska fungera som min context till min /ask endpoint

# Mina imports
import os
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
from google import genai
from dotenv import load_dotenv
from typing import Any


# Ladda in .env variabel så Gemini hittar min API key
load_dotenv()

# Pathin variabel + koppla upp mot min skapade vector DB som innehåller hela databasen med glosor
# ===== 1) Databas setup ChromaDB =====
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection("glossary_terms")

# --- Embedding setup (SentenceTransformer) ---
# --- Laddar in exakt samma modell som används i embed_terms.py
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# ===== 2) AI setup (Gemini) =====
ai_client = genai.Client()

# ===== Helper funktion för context hantering =====
def get_relevant_context(user_query: str, num_results: int =5) -> tuple[str, list[str]]:
    """Gets context and returns (context_string, list_of_sources)"""""
    
    # Översätter users fråga till vektor innan fråga till ChromaDB skickas
    # normalize_embeddings=True för att matcha cosine matte
    query_vector = encoder.encode(user_query, normalize_embeddings=True).tolist()

    # 1) Fråga ChromaDB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=num_results
    )

    # 2) Hämta och packa upp min key+values bestående av en list med lists i sig.
    # 2) + hämta metadata för att hämta min SLUG
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 3) Sätt ihop listan till en lång str med simpel formattering för läsbarhet.
    # 3) Formatering för att underlätta för LLM och undvika framtida headaches
    context_string = "\n----\n".join(
        f"Term {i+1}: {doc}"
        for i, doc in enumerate(documents)
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
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=num_results
    )

    # 3) Packa upp list bestående av nested lists som är nyckelns Value
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # 4) Zippa ihop all data
    formatted_results = []
    for docs, meta, dist in zip(documents, metadatas, distances):
        formatted_results.append({
            "term": meta.get("term"),
            "slug": meta.get("slug"),
            "distance": round(dist, 4), # Avrundar för formattering
            "sources": meta.get("sources"),
            "snippet": docs[:100] + ".." # 100 första tecknen av glosan
        })

    return formatted_results


# ===== Funktion för att generera RAG svar =====
def generate_rag_response(user_query: str) -> dict:
    """Main function for RAG: Get context and let LLM formulate an answer"""
    
    # 1) R (Retrieval), hämta faktan(user_query + slugs)
    context_text, source_slugs = get_relevant_context(user_query)

    # 2) A(Augmented), bygg den super prompt och de regler som LLM ska använda sig av.
    prompt = f"""You are a pedagogical and highly skilled Data Engineering assistant.
    Your task is to accurately answer the user's question.
     
    CRITICAL RULES:
    1. NO HALLUCINATIONS: You must ONLY base your answer on the information provided in the context block below. Do not invent external information.
    2. LANGUAGE MATCHING (ABSOLUTE): You MUST reply in the exact language of the user's question. 
       - If user asks in English -> Reply in English. 
       - If user asks in Swedish -> Reply in Swedish.
    3. TRANSLATION PERMITTED: You are allowed to translate the context database into the user's language to fulfill Rule 2.
    4. FALLBACK: If the answer cannot be found in the context, reply in the user's language that you do not know based on the available information, and ask them to search for another term.

    --- CONTEXT FROM DATABASE ---
    {context_text}
    
    --- USER'S QUESTION ---
    {user_query}
    """

    # 3) G(Generation), Skicka vidare till google Gemini 2.5 Flash modellen
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    # Returnera en dict med både AI svaret och sources
    return {
        "answer": response.text,
        "sources": source_slugs
    }

# --- Testblock ---
# Allt under if __name__ == "__main__": körs BARA om jag kör just denna fil i terminalen.
if __name__ == "__main__":
    print("Testar RAG-motorn...\n")
    # Test prints. Ställa fråga som test_search.py hade problem med att svara på igår
    test_question = "Hur fungerar undantagshantering?"
    

    print(f"Fråga: '{test_question}'")
    print(f"\n")
    svar = generate_rag_response(test_question)

    print("\n--- SVAR ---")
    print(svar)
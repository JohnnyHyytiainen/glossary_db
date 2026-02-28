# Kod: Engelska
# Kommentarer: Svenska
# Helper function som ska fungera som min context till min /ask endpoint

# Mina imports
import os
import chromadb
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# Ladda in .env variabel så Gemini hittar min API key
load_dotenv()

# Pathin variabel + koppla upp mot min skapade vector DB som innehåller hela databasen med glosor
# ===== 1) Databas setup ChromaDB =====
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection("glossary_terms")

# ===== 2) AI setup (Gemini) =====
ai_client = genai.Client()

# ===== Helper funktion för context hantering =====
def get_relevant_context(user_query: str, num_results: int =5) -> str:
    """Retrieves the 3 closest relevant terms from ChromaDB for given question(/ask)"""

    # 1) Fråga ChromaDB
    results = collection.query(
        query_texts=[user_query],
        n_results=num_results
    )

    # 2) hämta och packa upp min key+values bestående av en list med lists i sig.
    documents = results["documents"][0]

    # 3) Sätt ihop listan till en lång str med simpel formattering för läsbarhet.
    # 3) Formatering för att underlätta för LLM och undvika framtida headaches
    context_string = "\n----\n".join(
        f"Term {i+1}: {doc}"
        for i, doc in enumerate(documents)
    )

    return context_string

# ===== Funktion för att generera RAG svar =====
def generate_rag_response(user_query: str) -> str:
    """Main function for RAG: Get context and let LLM formulate an answer"""
    
    # 1) R (Retrieval), hämta faktan(user_query)
    context = get_relevant_context(user_query)

    # 2) A(Augmented), bygg den super prompt och de regler som LLM ska använda sig av.
    prompt = f"""You are a pedagogical and highly skilled Data Engineering assistant.
    Your task is to accurately answer the user's question.
    
    CRITICAL RULES:
    1. NO HALLUCINATIONS: You must ONLY base your answer on the information provided in the context block below. Do not invent or add external information.
    2. LANGUAGE MATCHING: You MUST reply in the exact same language that the user used in their question. If the user asks in English, reply in English. If the user asks in Swedish, reply in Swedish.
    3. TRANSLATION PERMITTED: The provided context might be in English, but the user might ask in Swedish (e.g., "undantagshantering" vs "exception handling"). You are explicitly ALLOWED to translate the context information into the user's language to formulate your answer.
    4. FALLBACK: If the answer cannot be found in the context, reply in the user's language that you do not know based on the available information, and ask them to search for another term.
    
    --- CONTEXT FROM DATABASE ---
    {context}
    
    --- USER'S QUESTION ---
    {user_query}
    """

    # 3) G(Generation), Skicka vidare till google Gemini 2.5 Flash modellen
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

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
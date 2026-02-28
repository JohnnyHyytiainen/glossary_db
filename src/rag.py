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
    prompt = f"""Du är en pedagogisk och tekniskt kunnig Data Engineering-assistent.
    Din uppgift är att svara på användarens fråga.
    
    VIKTIG REGEL: Du får ENBART basera ditt svar på informationen i kontext-blocket nedan. 
    Om svaret inte finns i kontexten, svara vänligt på SAMMA SPRÅK som frågan att du inte vet och uppmana användaren att söka på en annan term.
    Hitta inte på egen information. Svara på samma språk som användarens fråga.

    SPRÅK REGEL: Om användaren använder sig av ENGELSKA ska du svara på ENGELSKA,
    om användaren använder sig av SVENSKA ska du svara på SVENSKA.
    
    --- KONTEXT FRÅN DATABASEN ---
    {context}
    
    --- ANVÄNDARENS FRÅGA ---
    {user_query}
    """

    # 3) G(Generation), Skicka vidare till google Gemini 2.5 Flash modellen
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

# --- Testblock ---
# Allt under if __name__ == "__main__": körs BARA om du kör just denna fil i terminalen.
if __name__ == "__main__":
    print("Testar RAG-motorn...\n")
    # Test prints. Ställa fråga som test_search.py hade problem med att svara på igår
    test_question = "How does exception handling work?"
    

    print(f"Fråga: '{test_question}'")
    print(f"\n")
    svar = generate_rag_response(test_question)

    print("\n--- SVAR ---")
    print(svar)
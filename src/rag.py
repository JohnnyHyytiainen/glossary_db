# Kod: Engelska
# Kommentarer: Svenska
# Helper function som ska fungera som min context till min /ask endpoint

# Mina imports
import chromadb
from pathlib import Path

# Pathin variabel + koppla upp mot min skapade vector DB som innehåller hela databasen med glosor
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection("glossary_terms")

def get_relevant_context(user_query: str, num_results: int =3) -> str:
    """Retrieves the 3 closest relevant terms from ChromaDB for given question(/ask)"""

    # 1) Fråga ChromaDB
    results = collection.query(
        query_texts=[user_query],
        n_results=num_results
    )

    # 2) hämta och packa upp min key+values bestående av en list med lists i sig.
    documents = results["documents"][0]

    # 3) Sätt ihop listan till en lång str med simpel formattering för läsbarhet
    # Formatering för att underlätta(?) för google-genai 
    
    # context_string = "\n--\n".join(documents)
    context_string = "\n----\n".join(
        f"Term {i+1}: {doc}"
        for i, doc in enumerate(documents)
    )

    return context_string
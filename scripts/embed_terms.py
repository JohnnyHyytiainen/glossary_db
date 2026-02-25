# Kod: Engelska
# Kommentarer: Svenska
# ETL: Extract terms från PostgreSQL db -> Transformera till vector embeddings -> Load in till ChromaDB(vector DB)

from sentence_transformers import SentenceTransformer
import chromadb
# Imports from mina moduler i src/
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database import SessionLocal
from src.models import Term

# 1) E i ETL - Funktion för att extrahera alla terms, categories och sources från PostgreSQL db 
def extract_terms():
    """Extract all terms from PostgreSQL DB"""
    db = SessionLocal()
    try:
        stmt = (
            select(Term)
            .options(
                selectinload(Term.categories), 
                selectinload(Term.sources)
            )
        )
        # .all() returnerar en python lista av Term objekt.
        # terms = [<Term slug='ci-cd'>, <Term slug='etl'>, ...]
        terms = db.scalars(stmt).all()
        # print för att verifiera
        print(f"Extracted: {len(terms)} from PostgreSQL DB")
        if terms:
            t = terms[0] # <-- Första elementet i listan.
            print(f"Example: {t.term} | {t.slug} | {t.definition[:50]}..") 
            # t.term --> det riktiga namnet  ("CI/CD")
            # t.slug --> URL-vänligt namn    ("ci-cd")  
            # t.definition[:50] --> slice, första 50 tecknen av strängen
        return terms
    finally:
        db.close() # <-- stäng dörren fint för att ej behöva oroa mig för memory leaks.

# 2) T i ETL - Funktion för att transformera varje term -> embedded vector
def transform_to_embeddings(terms: list[Term]) -> list[dict]:
    """
    Transform: Converts each term into an embedding vector.
    Combines term + definition into a single text string before embedding
    so the model has more context to work with.
    """
    print("Loading embedding model..")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded.")

    # Förbered lista att fylla.
    prepared = []
    for term in terms:
        # kombinera term + definition för att ge bättre kontext till min MiniLM modellen
        # Ex: "ETL: Extract Transform Load. A pipeline that... ...."
        text = f"{term.term}: {term.definition}"

        prepared.append({
            "id": term.slug,    # Unikt ID för ChromaDB
            "text": text,       # Råtext (sparas i ChromaDB)
            "metadata": {       # Extra info som går att filtrera på vid senare tillfälle
                "term": term.term,
                "slug": term.slug,
                "difficulty": term.difficulty.value if term.difficulty else "beginner",
                "categories": [c.name for c in term.categories],
            }
        })

    # Extrahera all test och skicka till modellen på en och samma gång.
    # Batch processing är mycket snabbare än att skicka en åt gången!
    texts = [p["text"] for p in prepared]
    print(f"Creating embeddings for {len(texts)} terms..")
    # Embeddings + progress bar för att ej drabbas av panik.
    embeddings = model.encode(texts, show_progress_bar=True)

    # Koppla ihop embedding vektor med rätt term.
    for i, item in enumerate(prepared):
        item["embedding"] = embeddings[i]

    # Print för att ha koll.
    print(f"Transform stage is done! {len(prepared)} ready for ChromaDB!")
    # returnera ifylld lista.
    return prepared


# 3) L i ETL - Funktion för att ladda in allting i min vector db(ChromaDB)
def load_into_chromadb(prepared: list[dict]) -> None:
    """
    Load: Save embeddings + the metadata in ChromaDB (persistent).
    PersistentClient saves directly to disc. Meaning data survives between runs.
    """




    

if __name__ == "__main__":
    terms = extract_terms()
    prepared = transform_to_embeddings(terms)

    # Verifiera första termen just in case!
    first = prepared[0]
    print(f"\nFirst term after transformation:")
    print(f"ID:             {first['id']}")             # ID
    print(f"Text:           {first['text'][:60]}")      # Råtext, första 60 chars
    print(f"Embedding:      {first['embedding'][:5]}")  # Mina första 5 värden av vektor
    print(f"Dimensions:     {len(first['embedding'])}") # SKA vara 384 EXAKT


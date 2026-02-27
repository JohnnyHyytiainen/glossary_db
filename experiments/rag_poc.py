# Kod: Engelska
# Kommentarer: Svenska
# Första experimentet med RAG proof of concept!
# ChromaDB + sentence transformers
# Experiment: ChromaDB + sentence-transformers proof of concept
# Frikopplat från FastAPI/PostgreSQL - bara för att känna på hur det funkar

import chromadb
from sentence_transformers import SentenceTransformer

# 1. LADDA EMBEDDING-MODELL
print("Laddar embedding-modell...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Modell laddad!")

# 2. SKAPA CHROMADB (in-memory, inget sparas till disk ännu)
client = chromadb.Client()
collection = client.create_collection("glossary_test")

# 3. NÅGRA TESTGLOSOR (manuellt, ingen PostgreSQL än)
test_terms = [
    {"id": "etl", "text": "ETL: Extract Transform Load. A pipeline that moves and transforms data between systems."},
    {"id": "pipeline", "text": "Pipeline: A series of data processing steps where output of one step is input to the next."},
    {"id": "schema", "text": "Schema: The structure that defines how data is organized in a database."},
    {"id": "normalization", "text": "Normalization: Organizing data to reduce redundancy and improve data integrity."},
    {"id": "api", "text": "API: Application Programming Interface. A way for applications to communicate with each other."},
]

# 4. LADDA IN I CHROMADB
print("\nLaddar in testglosor...")
collection.add(
    documents=[t["text"] for t in test_terms],
    ids=[t["id"] for t in test_terms]
)
print(f"{len(test_terms)} glosor inladdade!")

# 5. SÖK SEMANTISKT
queries = [
    "vad är ett api",                       # bör hitta API
    "Hur strukturerar jag någonting",       # bör hitta schema + normalization
    "what do i use to structure something", # bör hitta schema
]

print("\n--- SÖKRESULTAT ---")
for query in queries:
    results = collection.query(query_texts=[query], n_results=2)
    print(f"\nFråga: '{query}'")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        print(f"  → {doc[:60]}... (distance: {distance:.3f})")
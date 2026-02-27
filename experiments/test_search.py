# Kod: Engelska
# Kommentarer: Svenska
# Experiment: Testa semantisk sökning mot riktiga 308 terms i ChromaDB

import chromadb
from pathlib import Path

# Gör pathing skottsäker för chroma_db folder. Just in case pathing gremlins spökar..
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"

# Använd pathing variabel enbart för att undvika pathing huvudvärk(just in case)
# Persistent klient (Sparar alla filer lokalt i chroma_db mappen)
client = chromadb.PersistentClient(path=str(CHROMA_PATH))
# Hämtar den collection vid namn glossary_terms
# collection(name="my_collection", metadata={})
collection = client.get_collection("glossary_terms")

# Prints för att se att allting fungerar som Jag vill
# Returnerar hur många 'records'(antal terms(?)) i glossary_terms
print(f"Terms in ChromaDB: {collection.count()}")
print("-" * 50)

queries = [
    "hur funkar datainsamling",         # Förväntat: ETL, pipeline, ingestion
    "how does data collection work",    # Förväntat: ???
    "Vad är versionskontroll",          # Förväntat: git, commit, branch (högre värde)
    "what is version control",          # Förväntat: git, commit, branch (lägre värde)
    "databasstruktur och tabeller",     # Förväntat: schema, normalization, ddl (högre värde)
    "database structure and tables",    # Förväntat: schema, normalization, ddl (lägre värde)
    "how to handle errors in code",     # Förväntat: exception, try/except, debugging
    "container och virtualisering",     # Förväntat: docker, image, compose
]

# Loopar över min queries lista, en query i taget.
for query in queries:
    results = collection.query(
        query_texts=[query],
        n_results=3 # top 3 närmaste terms 
    )
    print(f"\nFråga: '{query}'")
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        print(f" --> {meta['term']:<30} (distance: {dist:.3f})")

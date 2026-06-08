# Vector-ETL & ChromaDB: Module Overview

***Skapat: 2026-02-25***

## Syfte med Modulen

Att bygga en frikopplad Data Engineering-pipeline (ETL) som flyttar och transformerar data från en traditionell relationsdatabas (PostgreSQL) till en semantisk vektordatabas (ChromaDB). Detta utgör grunden (Retrieval fasen) för applikationens RAG-arkitektur (Retrieval Augmented Generation)

## Kärnkoncept & Teori

### 1. Vector Embeddings (Semantisk Sökning)

Traditionella databaser (SQL) söker efter exakta bokstavsmatchningar (lexikal sökning). För att en AI ska förstå data måste texten översättas till matematik.
Genom att använda en Embedding-modell `all-MiniLM-L6-v2` omvandlas varje glosa till en array av 384 siffror (en 384-dimensionell vektor). Dessa siffror representerar ordets **betydelse**. Ord med liknande innebörd får vektorer som pekar åt nästan samma håll i en matematisk rymd.



### 2. Cosine Similarity (Mätning av avstånd)

När jag konfigurerade ChromaDB valde jag `metadata={"hnsw:space": "cosine"}`. Istället för att mäta det raka avståndet mellan två punkter (L2 / Euclidean distance), mäter Cosine Similarity **vinkeln** (riktningen) mellan två vektorer. Inom Natural Language Processing (NLP) är det här branschstandard, eftersom textens "längd" (magnitud) är mindre viktig än dess faktiska "riktning" (innebörd).


### 3. Idempotency (Skottsäkra västen för min Pipeline)

En pipeline måste vara **idempotent,** den ska kunna köras 1 gång eller 1000 gånger utan att systemet kraschar eller datan dupliceras. Genom att använda mig av `.upsert()` (Update or Insert) istället för `.add()` i laddningsfasen, garanteras det att pipelinen säkert kan köras varje gång en ny glosa läggs till i PostgreSQL.

---

## Arkitektur: Den 3 stegade Pipelinen

**Skriptet (`scripts/embed_terms.py`) är uppdelat i en klassisk ETL-struktur:**

* **Extract (E):** Jag öppnar en koppling till PostgreSQL via SQLAlchemy (`SessionLocal`). För att undvika N+1-problemet vid extraktionen används Eager Loading (`selectinload`) för att hämta alla `Terms`, `Categories` och `Sources` på ett minneseffektivt sätt.  

* **Transform (T):** Datan tvättas och kontextualiseras. Jag slår ihop `term` och `definition` till en enda sträng för att ge AI-modellen maximal kontext. Hela datasetet skickas sedan som en *Batch* in i SentenceTransformer-modellen, vilket är **extremt** mycket snabbare än att loopa och processa ett ord i taget.

* **Load (L):** De transformerade vektorerna, råtexten och metadatan (som ID och kategorier) laddas in i `ChromaDB`. Där jag använder en `PersistentClient` med en dynamisk `pathlib`-sökväg för att spara databasen säkert på hårddisken, detta för att undvika lokala pathing buggar som kan uppstå.

---

## ANN (Approximate Nearest Neighbor) 

* ANN är något jag redan har använt mig utav utan att veta om det och tänka på just det. Tittar jag i min `ChromaDB`-konfiguration:
```python
    collection = client.get_or_create_collection(
        name="glossary_terms",
        metadata={"hnsw:space": "cosine"} # <--- Här
    )
```
* Tittar jag på `metadata={"hnsw:space": "cosine"}` så ser jag att hnsw(Hierarchical Navigable Small World) redan är ett `ANN`-index. Jag konfigurerade redan ANN i Februari 2026 utan att ens veta om det.

* Exakt nearest neighbor i 384 dimensioner kräver att jag beräknas `cosine similarity` mot varje enstaka vektor i databasen. Vid ~500 glosor så spelar det ej någon roll. Vid 50 MILJONER glosor så är det här oanvändbart. `ANN` byter ut "den exakt närmaste" mot "någon som med mycket hög sannolikhet är bland de närmaste" och på så sätt vinner extrem hastighet på det. Det är t.ex det som Ewa för Qdrant pratade om när hon pratade om Token efficiency och skalbarhet.

* `Qdrant` VS `ChromaDB`: `ChromaDB` är rätt för tillfället. Snabb prototyp, lokalt och enkelt API. `Qdrant` är mer för produktion, distribuerad och ger ännu mer kontroll över `HNSW`-parametrar.
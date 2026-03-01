# Notes and documentation regarding project to further deepen my knowledge.

## Tuesday 17/02/2026
**Goals for today:**  
```text
- Docker container is up and running. (The house and blueprints for the structure) 
    - Done

- Server for database created in PgAdmin4.
    - Done

- Get python to talk with PostgreSQL via SQLAlchemy (ORM-Object Relational Mapping)

- config.py (Configuration file for quality of life)
    - Done

- database.py (ORM engine + session + base model + helper function for FastAPI)
    - Done

- models.py (Using Base from database.py to create my tables for DB)
    - Done
```
        
## Wednesday 18/02/2026
**Goals for today:**  
```text
During ERT infusion:
- Create "to-do-list" (revision) with alembic
    - Done

- Migration and config alembic (alembic/env.py)
    - Done

- Revision, migration, alembic theory
    - Done
```

## Thursday 19/02/2026
**Goals for today:** 
```text
- Theory to understand an objects lifecycle in SQLAlchemy(an objects THREE phases)
    - Done

- Seed my database by writing a python script and not using SQL
    - Done

- Started to fill in glossary terms with explanation prior to manually entering them in seed.py script before writing an automated script.
    - Done
```

## Saturday 21/02-2026
**Goals for today:**
```text
- Keep on translating glossary terms and continue writing seed script to fill my database.
    - Done

- Write a few more glossary classes to ingest into postgres db.
    - Done

- Start writing a basic ETL pipeline to clean up messy glossary data because I dont feel like writing it manually anymore.
    - Done

- Fill in definition for all terms in glossary csv.
    - Done

- Add pandas dependency to read in glossary_filled_clean.csv to load it all in to postgres db all at once.
    - Done
```

## Sunday 22/02-2026
**Goals for today:**
```text
- Add endpoints with FastAPI (main.py)
    - Done

- Theory and code review of `config.py` `database.py` `models.py` `extract.py` `seed.py` `seed_csv.py`
    - Done

- Add Pydantic schemas and classes.
    - Term schema Done.
    - 

- Add different endpoints, term/slug
    - Done

- Add endpoint for RANDOM terms
    - Done

- Added nested schemas in schemas.py(Category + source) to terms
    - Done

Agenda: 
Endpoints - FastAPI(Done)
Pydantic schemas, classes (Done)
Testing with httpx - (Done)
First API calls - (Done)
```
## Monday 23/02-2026
**Goals for today:**
```text
- Add health check endpoint in main.py script
    - Done

- Add testing for API(tests/test_api.py script) with functions and asserts(learn how to make it)
    - Done

- Add pagination (For/terms endpoint + add docs for further understanding)
    - Done
    - See quick_setup_commands.md for explanation
```
## Tuesday 24/02-2026
**Goals for today:**
```text
- Add Query params (Filter by category)
    - Done

- Add query params (filter by word)
    - Done
```

## Wednesday 25/02-2026
**Goals for today:**
**MUST DO 1) :  DONE**
```text
1) FIX double get_db, one in database.py and one in main.py.
    - ONLY USE ONE, PREF FROM DATABASE.PY, database.py should own both SessionLocal AND get_db()
Förklaring:
Just nu importerar jag SessionLocal från src.database och definierar get_db() lokalt i main.py.
Det funkar, men 'clean' är att database.py äger både SessionLocal och get_db().

1.1) I src/database.py: lägg tillbaka en riktig get_db() (generatorn) utanför kommentarer/docstrings.

1.2) I src/main.py: ta bort din lokala get_db() och importera den:
    - före: from src.database import SessionLocal
    - efter: from src.database import get_db (och om jag fortfarande behöver SessionLocal någonstans, importera båda)

DoD: inget endpoint-beteende ändras, Jag har bara flyttat DB-dörrvakten till rätt fil.

```
## Wednesday 25/02-2026
**MUST DO 2) :  DONE**
```text
2) FIX N+1 risk on /terms.

N+1-fix: selectinload på de queries som returnerar Terms
Min /terms, /terms/{slug}, /random returnerar TermResponse som innehåller categories och sources.
Om relationerna lazy-loadas blir det klassiskt N+1: en query för terms + extra queries när Pydantic läser term.categories och term.sources.

Fix:
Lägg på "eager loading" i select(Term):
import: from sqlalchemy.orm import selectinload

bygg stmt så här (idé):
    - select(Term).options(selectinload(Term.categories), selectinload(Term.sources))

Gör det i:
    - get_terms
    - get_term_by_slug
    - random_term
----------
/terms?limit=10 ska typiskt bli ~3 queries totalt:

2.1) terms
2.2) categories för alla hämtade terms (IN-lista via junction)
2.3) sources för alla hämtade terms (IN-lista via junction)

Det här är "N+1 ->  3" utan att jag ändrar API:t alls(?)
---
För att Verifiera snabbt att N+1 är borta (5–10 min):
- Sätt echo=True på din engine tillfälligt och slå /terms?limit=10.
- Räkna SQL-rader i terminaln: du ska se '1 + 2' queries, inte '1 + 20'
```
## Wednesday 25/02-2026
**MUST DO 3) :  DONE**
```TEXT
3) FIX Mini runbook/readme!
    - Done
```


## Wednesday 25/02-2026
**Goals for today:**
```text
- Prepare everything for RAG -> ChromaDB
    - Done

- Read up on vector DBs, Vector Embedding, Augmentation(prompt engineering), Generation(Gemini API(?))
    - Done

- First proof of concept for vector embeddings and tests /experiments/rag_poc.py
    - Done

- ETL to take data from Postgres DB, extract, transform, load data into vector DB(chromaDB) scripts/embed_terms.py
    - Done
```

## Friday 27/02-2026
**Goals for today:**
```text
- Nuke container, rebuild it all from scratch with bigger dataset och terms.
    - Done

- Rebuild everything from scratch after nuke. Build(Docker), migration(alembic), seed(script), embed/ingest(postgres -> vectors -> ChromaDB)
    - Done

- Test semantic search on my real terms in ChromaDB (experiments/test_search.py)
    - Done
```
## Saturday 28/02-2026
**Goals for today:**
```text
- Create helper function in src/rag.py for my FastAPI endpoint to call on when using /ask endpoint
    - Done

- Uv add google-genai + create new api key to use gemini-2.5-flash for project, uv add python-dotenv to avoid issues with .env file.
    - Done

- Formulate and add super prompt for Gemini to adhere to.
    - Done

- Add ai-engine layer in src/rag.py
    - Done

- Write new /ask endpoint in src/main.py to use helper function src/rag.py
    - Done
```

## Sunday 01/03-2025
**Goals for today:**
```text
- Fix embedding mismatch. Change retrieval to use the same SentenceTransformer at when querying to match with indexing (match src/rag.py with scripts/embed_terms.py)
    - Done

- Fix embedding mismatch in embed_terms.py to match with rag.py.
(embeddings = model.encode(texts, show_progress_bar=True) | to ->  embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True).tolist() )
    - Done

- Add a /search endpoint to my API.
    - Done

- Make /ask endpoint more user friendly and return sources in the output.
    -

- Add Gemini API key example to .env.example file
    - Done

- Add sources in AskResponse class in schemas.py
    - Done

- Add traceability to my /search and /ask endpoint
    - 
    
```
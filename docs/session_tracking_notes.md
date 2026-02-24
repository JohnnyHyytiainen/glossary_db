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
```text
MUST DO:
1) FIX double get_db, one in database.py and one in main.py.
    - ONLY USE ONE, PREF FROM DATABASE.PY, database.py should own both SessionLocal AND get_db()
Förklaring:
Just nu importerar jag SessionLocal från src.database och definierar get_db() lokalt i main.py.
Det funkar, men 'clean' är att database.py äger både SessionLocal och get_db().

Gör så här för minsta ändring:

I src/database.py: lägg tillbaka en riktig get_db() (generatorn) utanför kommentarer/docstrings.

I src/main.py: ta bort din lokala get_db() och importera den:

    - före: from src.database import SessionLocal
    - efter: from src.database import get_db (och om jag fortfarande behöver SessionLocal någonstans, importera båda)

DoD: inget endpoint-beteende ändras, Jag har bara flyttat DB-dörrvakten till rätt fil.
```
```text
2) FIX N+1 risk on /terms.

N+1-fix: selectinload på de queries som returnerar Terms
Min /terms, /terms/{slug}, /random returnerar TermResponse som innehåller categories och sources.
Om relationerna lazy-loadas blir det klassiskt N+1: en query för terms + extra queries när Pydantic läser term.categories och term.sources.

Fix:
Lägg på "eager loading" i select(Term):

import: from sqlalchemy.orm import selectinload

bygg stmt så här (idé):

select(Term).options(selectinload(Term.categories), selectinload(Term.sources))

Gör det i:
    - get_terms
    - get_term_by_slug
    - random_term
--- 

/terms?limit=10 ska typiskt bli ~3 queries totalt:

1) terms
2) categories för alla hämtade terms (IN-lista via junction)
3) sources för alla hämtade terms (IN-lista via junction)
--- 
Det här är "N+1 → 3" utan att jag ändrar API:t alls(?)
---
För att Verifiera snabbt att N+1 är borta (5–10 min):
- Sätt echo=True på din engine tillfälligt och slå /terms?limit=10.
- Räkna SQL-rader i terminaln: du ska se '1 + 2' queries, inte '1 + 20'
```
```TEXT
3) FIX Mini runbook/readme!
"Mini runbook" för imorgon:
1) Flytta get_db till database.py och importera i main.py
2) Lägg selectinload på de tre term-queries
3) Testa:

- /health

- /terms?limit=10

- /terms/{slug}

- /random

---

Efter den fixen ovanför(KRITISK!) är detta nästa steg:
1) README runbook(runbook + brief explanation för att ej skjuta på det!)
- Start DB(docker compose)
- Migrera (alembic)
- seed (csv script)
- Start API
- Exempelanrop (curl)
    - Mest ROI för tiden jag lägger trots pågående projekt.
```

```text
- Code review by me and Q/A forms made from LLM over all modules get deeper understanding for Mondays session and entire MvP v1.0 codebase
    -

- Prepare everything for RAG -> ChromaDB
    -

- Read up on vector DBs, Vector Embedding, Augmentation(prompt engineering), Generation(Gemini API(?))
    -
```
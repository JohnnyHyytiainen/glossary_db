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
    - 
Agenda: 
Endpoints - FastAPI(Done)
Pydantic schemas, classes (?)
Testing with httpx - (?)
First API calls - (?)
```

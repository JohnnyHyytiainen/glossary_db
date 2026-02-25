# Glossary DB (FastAPI + PostgreSQL)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=Pydantic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)  
![License](https://img.shields.io/badge/License-MIT-green)


A small backend API for a technical glossary. It stores normalized glossary data in PostgreSQL and exposes clean, nested JSON via FastAPI.

## Features (MVP v1.0)
- Normalized PostgreSQL schema (Terms, Categories, Sources + M:N association tables)
- FastAPI endpoints with Dependency Injection (DB session per request)
- Pydantic response models (nested JSON without leaking internal fields)
- `/health` endpoint for monitoring
- Pagination (`skip`/`limit`, hard cap at 100)
- Filtering via pushdown computation (`search`, `category`)
- Basic seed/ETL scripts for loading glossary data
- Unit tests with Pytest

## Tech Stack
- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy 2.x (ORM)
- Alembic (migrations)
- PostgreSQL (Docker)
- (Optional) Pandas for CSV ingest

---

## Quickstart

### Prerequisites
- Docker / Docker Desktop
- `uv` installed

### 1) Clone & configure env
```bash
git clone https://github.com/JohnnyHyytiainen/glossary_db.git
cd glossary_db
````

Create a local `.env` from the example:

```bash
cp .env.example .env
```

> The app reads configuration via `pydantic-settings`. Keep secrets in `.env` (never commit them).

### 2) Start PostgreSQL (Docker)

```bash
docker compose up -d

or: 

docker-compose up -d

docker compose ps
```

### 3) Install dependencies

```bash
uv sync
```

### 4) Run migrations (create tables)

```bash
uv run alembic upgrade head
```

### 5) Seed the database (ETL)

Choose one seeding method depending on your repo scripts:

```bash
# If you have a module-based seeder:
uv run python -m src.seed

# If you seed from CSV:
uv run python -m src.seed_csv
```

> If you see `ModuleNotFoundError: No module named 'src'`, run scripts as modules:
>
> **Do use:** `uv run python -m src.seed` 
>
> **Dont use:** `uv run src/seed.py`

### 6) Run the API

```bash
uv run uvicorn src.main:app --reload
```

Open:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## API Endpoints

### Health

* `GET /health`

### Terms

* `GET /terms?skip=0&limit=10`
* Filtering:

  * `GET /terms?category=python`
  * `GET /terms?search=etl`

Notes:

* `limit` is capped at 100.
* Responses include nested `categories` and `sources` (optimized to avoid N+1 queries).

### Term by slug

* `GET /terms/{term_slug}`

### Random term

* `GET /random`

---

## Tests

```bash
uv run pytest -v
```

## Dev tooling

```bash
uv run ruff check .
uv run black .
```

---

## Data Model (high level)

* `terms` (core entity)
* `categories`
* `sources`
* `term_categories` (M:N)
* `term_sources` (M:N)

---

## Troubleshooting

### Reset DB and re-seed

```bash
docker compose down -v
docker compose up -d
uv run alembic upgrade head
uv run python -m src.seed_csv
```

### Common issue: running scripts inside `src/`

Run scripts as modules (recommended):

```bash
uv run python -m src.seed_csv
```

---

## Next steps (planned)

* Mini RAG expansion:

  * ChromaDB (vector index)
  * Embeddings
  * Retrieval endpoint (`/search?q=...`)
  * Optional LLM integration (Gemini API)

See docs:

* `docs/mvp_v1_api.md`
* `docs/quick_setup_commands.md`



# Glossary DB (FastAPI + PostgreSQL)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=Pydantic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Grunden.ai](https://img.shields.io/badge/Grunden.ai-GLM_5.1-5C3EE8?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/AI%20RAG-ChromaDB-FF6F00?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green)

**A modern backend API for a technical glossary with 500+ terms across 11 Data Engineering categories. Stores normalized data in PostgreSQL, exposes clean JSON via FastAPI, features a built-in RAG engine for semantic search and AI-powered Q&A, and includes a Streamlit frontend for interactive demo.**

---

## Features (v1.4.x)

- **AI RAG Engine:** Ask questions in any language via Grunden.ai (GLM 5.1, OpenAI-compatible API). Responses are restricted to internal glossary data only - no hallucinations.

- **Explainable AI (XAI):** Every AI response includes a `sources` array with the exact glossary terms used to build the answer.

- **Streamlit Frontend:** Interactive UI with three views - AI assistant, semantic search, and term browser. Fully decoupled from the backend (communicates via HTTP only).

- **Semantic Search:** Vector embeddings (Sentence-Transformers `all-MiniLM-L6-v2`) and ChromaDB integration (`/search`).

- **Normalized DB Schema:** Terms, Categories, Sources + M:N association tables. N+1 queries eliminated via SQLAlchemy `selectinload`.

- **FastAPI Endpoints:** Dependency Injection, Pydantic response models, pagination, and filtering.

- **Robust ETL Pipelines:** Two-step ingestion - seed PostgreSQL from CSV (`seed_csv.py`), then build ChromaDB vectors (`embed_terms.py`).

---

## Tech Stack

- **Backend:** Python 3.12+, FastAPI, Uvicorn, Pydantic
- **Frontend:** Streamlit (modular `ui/` package)
- **Database:** PostgreSQL (Docker), SQLAlchemy 2.x, Alembic
- **AI & Vector DB:** ChromaDB, `all-MiniLM-L6-v2` (Sentence-Transformers), Grunden.ai API (GLM 5.1, OpenAI-compatible)
- **Tooling:** `uv`, Pytest, Ruff, Black

---

## Project Structure

```text
glossary_db/
├── data/                # Raw and cleaned CSV files for ingestion
├── docs/                # Architecture diagrams, module overviews, session notes
│   ├── diagrams/        # CDM / LDM / PDM (Mermaid + PNG)
│   └── modules/         # RAG flow, schema design, ORM theory, etc.
├── scripts/             # Vector ETL (embed_terms.py)
├── src/                 # FastAPI application (main.py, rag.py, models, schemas)
├── ui/                  # Streamlit frontend (modular package)
│   ├── __init__.py
│   ├── api.py           # All HTTP calls against FastAPI - single source of truth
│   ├── styles.py        # CSS
│   ├── ask_tab.py       # AI assistant tab
│   ├── search_tab.py    # Semantic search tab
│   └── browse_tab.py    # Term browser tab
├── tests/               # Pytest suite
├── streamlit_app.py     # Streamlit entry point (orchestration only)
├── .env.example         # Environment variable template
├── docker-compose.yml   # Local infrastructure (PostgreSQL)
└── README.md
```

---

## Dataset

- **500+ terms** across 11 categories
- **Categories:** Python, SQL, Data Engineering, Data Modeling, Data Platform Development, Data Visualization, Data Warehouse, AI Engineering, LLMOps, Machine Learning, Big Data Databricks

---

## Quickstart

### Prerequisites
- Docker / Docker Desktop
- `uv` installed
- Grunden.ai API key (for the `/ask` endpoint - [grunden.ai](https://grunden.ai))

### 1) Clone & configure env
```bash
git clone https://github.com/JohnnyHyytiainen/glossary_db.git
cd glossary_db
cp .env.example .env
```

Open `.env` and fill in your credentials:
```
GRUNDEN_API_KEY=sk-grunden-...
DB_USER=...
DB_PASSWORD=...
```

> Configuration is managed via `pydantic-settings`. Never commit `.env`.

### 2) Start PostgreSQL (Docker)
```bash
docker compose up -d
```

### 3) Install dependencies
```bash
uv sync
```

### 4) Run migrations and seed the database
```bash
# Create tables
uv run alembic upgrade head

# Seed PostgreSQL from CSV
uv run python -m src.seed_csv
```

### 5) Build the vector database (ChromaDB)
```bash
uv run python -m scripts.embed_terms
```

> **Rebuilding ChromaDB** after adding new terms:
> ```bash
> # Windows (PowerShell)
> Remove-Item -Recurse -Force chroma_db
> uv run python -m scripts.embed_terms
> ```

### 6) Run the API
```bash
uv run uvicorn src.main:app --reload
```

Swagger UI: **http://127.0.0.1:8000/docs**

### 7) Run the Streamlit frontend
```bash
# In a second terminal (keep the API running)
uv run streamlit run streamlit_app.py
```

Streamlit UI: **http://localhost:8501**

---

## API Endpoints

**AI & Semantic Search**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ask` | RAG engine. Accepts `{"query": "..."}`, returns pedagogical answer + `sources` array (GLM 5.1 via Grunden.ai). |
| `GET` | `/search?q=...&k=5` | Semantic search directly against ChromaDB. Returns top-k matches with cosine distances. |

**Glossary CRUD**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/terms` | Paginated list. Filters: `?category=`, `?search=`, `?skip=`, `?limit=` (max 100). |
| `GET` | `/terms/{slug}` | Single term by URL slug. |
| `GET` | `/random` | Random term. |
| `GET` | `/health` | API + database liveness check. |

> Responses include nested `categories` and `sources` - N+1 queries eliminated via `selectinload`.

---

## Documentation

Deep dives in `/docs`:

- **[Conceptual, Logical and Physical data models](docs/diagrams/)**
- **[RAG Flow Architecture](docs/modules/rag_flow_architecture.md)**
- **[Database Schema Design](docs/modules/database_schema_design.md)**
- **[Database Overview](docs/modules/database_overview.md)**
- **[Quick Setup Commands](docs/modules/quick_setup_commands.md)**

---

## Tests & Linting

```bash
uv run pytest -v
uv run ruff check .
uv run black .
```

---

## Data Model

```
terms           (core entity)
categories
sources
term_categories (M:N)
term_sources    (M:N)
```

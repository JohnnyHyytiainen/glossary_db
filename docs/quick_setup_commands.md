## Quick setup.

- Start the container
    - `docker-compose up -d`

- Check status on the container
    - `docker-compose ps`

- Close docker (save the data)
    - `docker-compose down`

- Make "todo" list with alembic (Revision)
    - `uv run alembic revision --autogenerate -m "Initial tables"`

- Build "the house" (Send script to database)
    - `uv run alembic upgrade head`

- Fill the database with data (seed it / seeding)
    - `uv run python -m src.seed`

    - `uv run src/seed.py`
    - You will probably encounter `ModuleNotFoundError: No module named 'src'` when running this command.
```text
The reason for ModuleNotFoundError: No module named 'src' is because of this:

When you run: uv run src/seed.py

What Python is thinking: "Okay, I'll start the file seed.py. Since it's in the src folder, I'll set src as my 'home directory' (root directory)."

What happens next: Python reads the line from src.database import... and thinks: "Okay, I'm looking for a folder called src inside my home directory."

The error: But the home directory is already src. Python is looking for src/src/database.py, which doesn't exist!
```
- The solution:
```text
The Solution: The Module Flag (-m)
The solution is to tell Python to run your file as a Module instead of a standalone script. Then Python will keep your current folder (glossary_db/) as your home directory.

Run this exact command in the terminal:

- uv run python -m src.seed

(Notice how you use a dot . instead of a slash / and skip the .py. This is Python's way of saying "Look in the src folder for the seed module".)
```

- **Run the API script:**
    - `uv run uvicorn src.main:app --reload`
    - (--reload means that the server restarts automatically as soon as i save a change in my code.)
    - Terminal should give `Uvicorn running on http://127:0.0.1:8000` if everything went smoothly

- **Run the API TEST script:**
    - `pytest tests/test_api.py -v`

- **Use pagination(sidindelning) URL:**
    - http://127.0.0.1:8000/terms?skip=NUMBER&limit=NUMBER MAX 100
    - http://127.0.0.1:8000/terms?skip=20&limit=85

- **Run experimental PoC script:**
    - `uv run python -m experiments.rag_poc`


- **Run embed_terms ETL pipeline(Postgres db -> VectorDB using Chromadb):**
    - `uv run python -m scripts.embed_terms`

## Terms for NUKE and rebuild (Bigger seed_csv.py file)

- `docker compose down -v`          -v is crucial in this scenario. This nukes the database's ENTIRE saved volume.
- `docker compose up -d`            Starts an entire new and blank databaste.
- `uv run alembic upgrade head`     Migrates and rebuilds all my tables once again.
- `rm -rf chroma_db/`               Removes the entire chroma_db folder containing my vector DB.
- `uv run python -m src.seed_csv`   Runs my seed_csv.py script and seeds my database again
- `uv run python -m scripts.embed_terms` Runs my embed_terms.py script and rebuilds my vector DB.
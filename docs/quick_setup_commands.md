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
    - Du stöter säkert på `ModuleNotFoundError: No module named 'src'` vid detta kommando.
```text
Anledningen för ModuleNotFoundError: No module named 'src' är pga detta:

När du kör: uv run src/seed.py

Vad Python tänker: "Okej, jag startar filen seed.py. Eftersom den ligger i mappen src, sätter jag src som min 'hemkatalog' (root directory)."

Vad som händer sen: Python läser raden from src.database import... och tänker: "Okej, jag letar efter en mapp som heter src inuti min hemkatalog."

Felet: Men hemkatalogen är ju redan src. Python letar alltså efter src/src/database.py, vilket inte finns!
```
- Lösningen:
```text
Lösningen: The Module Flag (-m)
Lösningen är att be Python köra din fil som en Modul istället för ett fristående skript. Då behåller Python din nuvarande mapp (glossary_db/) som hemkatalog.

Kör exakt detta kommando i terminalen:

- uv run python -m src.seed

(Märk hur du använder en punkt . istället för slash / och skippar .py. Detta är Pythons sätt att säga "Leta i mappen src efter modulen seed".)
```

- Run the API script
    - `uv run uvicorn src.main:app --reload`
    - (--reload means that the server restarts automatically as soon as i save a change in my code.)
    - Terminal should give `Uvicorn running on http://127:0.0.1:8000` if everything went smoothly
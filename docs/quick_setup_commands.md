## Quick setup.

- Starta the container
    - `docker-compose up -d`

- Check status on the container
    - `docker-compose ps`

- Close docker (save the data)
    - `docker-compose down`

- Make "todo" list with alembic (Revision)
    - `uv run alembic revision --autogenerate -m "Initial tables"`

- Build "the house" (Send script to database)
    - `uv run alembic upgrade head`
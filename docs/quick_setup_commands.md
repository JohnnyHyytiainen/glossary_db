## Quick setup.

- Starta the container
    - `docker-compose up -d`

- Check status on the container
    - `docker-compose ps`

- Make "todo" list with alembic (Revision)
    - `uv run alembic revision --autogenerate -m "Initial tables"`

- Build "the house" (Send script to database)
    - `uv run alembic upgrade head`
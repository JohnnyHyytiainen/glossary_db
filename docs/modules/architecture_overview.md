## Architecture overview (basic)

```text
1) Routing-lagret (FastAPI - main.py): Tar emot HTTP-anropet (t.ex. GET /terms). Det validerar att anropet är rimligt (t.ex att limit inte är 500) och agerar trafikpolis.

2) Access-lagret (Depends(get_db)): Öppnar en säker tunnel till din databas.

3) ORM-lagret (SQLAlchemy - models.py): Det här är min översättare. Jag skriver Python-kod (select(Term).offset()), och SQLAlchemy översätter detta till ren, optimerad SQL queries som PostgreSQL förstår.

4) Databas-lagret (PostgreSQL via Docker): Gör det tunga lyftet. Databasen filtrerar, sorterar och plockar fram exakt den data jag bad om, blixtsnabbt.

5) Serialiserings-lagret (Pydantic - schemas.py): Tar databas-objekten och tvättar dem till ren JSON som skickas tillbaka till användaren. Den klipper bort allt som inte finns definierat i min TermResponse.
```

## Module Overview: The Access Layer (FastAPI & Pydantic)

Denna modul hanterar applikationens "Ytterdörr". Den tar emot förfrågningar från webben, lånar en databassession, hämtar data via SQLAlchemy, och filtrerar den genom Pydantic innan den skickas tillbaka som snygg JSON till användaren.

### 1. `schemas.py` (Kontrakten & Filtren)

**Syfte:** Definierar exakt hur datan ska se ut när den lämnar API:et. Pydantic fungerar som en strikt tulltjänsteman som säkerställer att ingen oönskad eller felaktig data läcker ut till användaren.

* **`BaseModel`:** Grundklassen från Pydantic. Allt den ärver härifrån får automatisk datavalidering. Om jag säger att `id` är en `int`, kommer Pydantic att kasta ett fel om databasen försöker skicka en sträng.

* **`ConfigDict(from_attributes=True)` (The Magic Bridge):** Detta är den absolut viktigaste raden. Den säger åt Pydantic: *"Försök inte läsa detta som en vanlig Python dictionary. Läs det som ett SQLAlchemy-objekt och hämta attributen direkt (t.ex `obj.term` istället för `obj['term']`)"*

* **Nästlade Scheman (Nested JSON):** Genom att skapa sub scheman (`CategoryResponse`, `SourceResponse`) och lägga dem som listor i huvudschemat (`TermResponse`), tvingas  SQLAlchemy att automatiskt göra en `JOIN` och hämta relaterad data via junction-tabeller.

### 2. `main.py` (Växeln & Vägarna)

**Syfte:** Initierar webbservern och definierar  Endpoints (URL-vägar) som användare kan anropa.

* **Dependency Injection (`Depends(get_db)`):** Ett smart sätt att hantera resurser. Istället för att öppna en databaskoppling som ligger och drar minne permanent, lånar funktionen `get_db()` ut en session via `yield` när ett anrop kommer in, och stänger den via `finally` så fort anropet är klart. Detta för att undvika `memory leaks`.

* **Response Model (`response_model=...`):** Det är här `main.py` och `schemas.py` knyts ihop. Genom att skriva `@app.get(..., response_model=TermResponse)` säger jag åt FastAPI att ta den råa datan från databasen och skicka den genom Pydantic-filter innan den returneras.

* **Path Parameters (`/terms/{term_slug}`):** Gör URL:er dynamiska. Variabeln i måsvingarna plockas automatiskt upp av Python-funktionen.

* **Endpoint Priority (Viktig regel!!):** FastAPI läser filen uppifrån och ner. Specifika, hårdkodade vägar (som `/random`) måste alltid ligga **ovanför** dynamiska vägar (som `/{term_slug}`). Annars misstolkar servern ordet "random" som en dynamisk slug och returnerar 404.

---

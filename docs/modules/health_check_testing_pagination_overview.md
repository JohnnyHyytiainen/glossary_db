# Module overview for health checks, unit testing with TestClient, Pagination & Api limits

---

### Dagens Lärdomar: MvP Polering Del 1

**1. Health Checks (Livstecken & Övervakning)**

* **Vad jag gjorde:** Skapade en `/health` endpoint.

- Gemini förklaring:
* **Varför det är viktigt:** I en professionell miljö drivs applikationer av orkestreringsverktyg (som Kubernetes eller Docker). Dessa system är blinda och behöver en specifik URL att "pinga" med jämna mellanrum. Svarar den `200 OK` fortsätter trafiken flöda. Svarar den `503 Service Unavailable` startas containern automatiskt om.
* **Teknisk detalj:** Du nöjde mig inte med att bara returnera en statisk text. Jag tvingade fram ett databasanrop med `db.execute(text("SELECT 1"))`. Detta kallas en "Deep Health Check" – den bevisar att hela kedjan (API -> ORM -> Databas) är intakt.

**2. Unit Testing med TestClient (Skyddsnätet)**

* **Vad Jag gjorde:** Satte upp en testmiljö med `pytest` och FastAPI:s `TestClient`.

- Gemini förklaring:  
* **Varför det är viktigt:** Manuell testning via Swagger UI fungerar för MvP, men när kodbasen växer blir det ohållbart. Automatiserade tester är ditt skyddsnät. De garanterar att den kod du skriver imorgon inte råkar ta sönder den kod du skrev igår. Det är "Fail Fast"-principen i praktiken.
* **Teknisk detalj:** `TestClient` startar ingen riktig webbserver. Den skickar HTTP-anropen virtuellt, direkt in i applikationens arbetsminne (RAM). Detta gör testerna blixtsnabba. Du använde `assert` för att skapa strikta kontrakt – om svaret från API:et avviker det allra minsta från vårt antagande, avbryts processen och varnar oss.

**3. Pagination & API Limits (Skalbarhet & Minneshantering)**

* **Vad Jag gjorde:** Byggde om dina primära `/terms` endpoint till att använda sidindelning via *Query Parameters* (`?skip=X&limit=Y`).

- Gemini förklaring:  
* **Varför det är viktigt:** Ett API måste designas för att klara extrem tillväxt. Om databasen en dag innehåller två miljoner rader, skulle ett anrop utan `limit` orsaka en "Out of Memory"-krasch.  Paginering delar upp datan i hanterbara, säkra portioner.
* **Tekniska detaljer:**
* **Deterministisk sortering:** Du var tvungen att ta bort `order_by(func.random())`. Paginering kräver en förutsägbar ordning (t.ex. alfabetisk) för att fungera, annars riskerar man att missa glosor eller få dubbletter när man byter "sida".
* **Inbyggd Säkerhet:** Genom Pydantics validering `Query(default=10, le=100)` skapade du en sköld. Om en klient begär 500 glosor, avvisar FastAPI anropet innan det ens når databasen och svarar med `422 Unprocessable Entity` (ett fel orsakat av användaren, inte servern).
* **Tomma rymden:** Att be om en "sida" (offset) som inte har någon data returnerar inte ett fel, utan en ärlig, tom lista `[]`. Databasen gjorde exakt vad den blev tillsagd, det råkade bara vara tomt där.



---
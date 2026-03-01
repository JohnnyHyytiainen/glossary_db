# Theory and explanations to better understand the architecture, how the data flows and how RAG works.


```text
RAG (Retrieval-Augmented Generation) låter krångligt, men det handlar egentligen bara om att ge en LLM (Gemini) ett väldigt specifikt, öppet lexikon innan den får svara på frågor.

Istället för att Gemini gissar utifrån vad den läste på Reddit för tre år sedan, tvingar jag den att läsa min databas. Det kan delas in i olika faser.

Fas 1: Preppen (Vektor ETL) innan APIt ens kan svara på frågor måste jag bygga ChromaDB.
- Läs: Jag hämtar alla mina glosor ifrån PostgreSQL
- Transformera(Embeddings): Jag skickar texten genom en "embedding model" (t.ex Sentence-transformers(?)). Den förvandlar texten till en array av siffror(Vektor). Varje siffra representerar ordets BETYDELSE.
- Ladda: Jag sparar ner dessa värden(vektorer) i ChromaDB.

Fas 2: Anropet(Här kommer RAG "flödet" in).
- När allting är preppat skapar jag en ny endpoint, t.ex POST /ask.

- 1) Användaren frågar (FastAPI):
    - Användaren skickar: "Vad är skillnaden mellan primary key och foreign key?" till mitt API.

- 2) Retrieval(ChromaDB):
    - Mitt API översätter frågan till en vektor, frågar ChromaDB, "vilka 3 glosor ligger närmast användarens fråga rent matematiskt?" ChromaDB svarar fort med glosorna för PK och FK.

- 3) Augmentation(Prompt engineering):
    - Med Python bygger jag ihop en osynlig "super prompt/master prompt". Enkelt exempel är typ så här:
    - "Du är en AI-assistent. Svara på användarens fråga baserat enbart på följande kontext. Kontext: [Klistrar in definitionerna av PK och FK från ChromaDB]. Användarens fråga: Vad är skillnaden?"

- 4) Generation (Gemini API(?))
    - Super/master prompten skickas till Gemini via ett API-call. Eftersom att Gemini nu har facit i hand så genererar den ett svar som är baserat på MINA definitioner ifrån min databas.

- 5) Svar(User/användaren):
    - FastAPI skickar tillbaka geminis svar till användaren som JSON.
``` 


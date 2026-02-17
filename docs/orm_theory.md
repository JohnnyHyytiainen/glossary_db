## För att förstå koden som ska skrivas måste jag förstå tre koncept i SQLAlchemy (ORM):

1. **The Engine (Motorn)** (src/database.py)
- Motorn är den fysiska kopplingen till databasen.
- Den håller koll på "Connection Pool" (en hink med öppna linjer till databasen så jag slipper ringa upp varje gång).
- Du skapar motorn en gång när appen startar.

2. **The Session (Sessionen)** (src/database.py)
- Detta är min "arbetsyta".
- När jag vill göra något (spara en term, hämta en lista), öppnar jag en Session.
- Jag gör dina ändringar i sessionen (Python-objekt).
- Sen gör du Commit (spara till DB) eller Rollback (ångra allt).
    - När du är klar stänger du sessionen.
- Tumregel: En session per "request" (anrop).

3. **Declarative Base (Kartan/Grundplåten)** 
- Det är en Python-klass som alla mina databas-modeller (tabeller) kommer ärva ifrån.
- Om jag skapar class Term(Base): så vet SQLAlchemy automatiskt att "Aha, Term är en tabell, jag ska hålla koll på den".
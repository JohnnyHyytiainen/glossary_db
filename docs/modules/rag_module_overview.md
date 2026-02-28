# RAG: Module Overview (`rag.py`)

***Skapat: 2026-02-28***

## Syfte med Modulen
Att bygga kärnan i min AI-motor genom att implementera **Retrieval-Augmented Generation (RAG)**. Modulen agerar brygga mellan ChromaDB (vektordatabas) och Google Gemini (LLM)

## Arkitektur & Flöde (The R-A-G process)
1. **Retrieval (`get_relevant_context`):** Tar emot användarens fråga och gör en semantisk sökning (Cosine Similarity) i ChromaDB för att hämta de 5 mest relevanta glosorna.
2. **Augmentation (Super-prompten):** Paketerar de hämtade glosorna och användarens fråga in i en strikt regelstyrd prompt.
3. **Generation (`generate_rag_response`):** Skickar den paketerade prompten till `gemini-2.5-flash` som formulerar ett mänskligt och pedagogiskt svar baserat *exakt* på min data.

## Säkerhet & Skydd
* **Hallucination Guard:** Gemini är instruerad att svara "Jag vet inte" om informationen saknas i kontexten. Tester visar att detta fungerar till 100% **(exempelvis vägrade den svara på "ETL" när termen inte fanns i databasen)**

* **Language Matching:** En regel tvingar AI'n att svara på samma språk som användaren ställde frågan på, med tillåtelse att översätta den engelska kontexten i farten.

## Kända Begränsningar (MvP v1.0)
Det finns en identifierad begränsning när användare ställer frågor på svenska (tex. "Hur fungerar undantagshantering?")

**Orsaken:** Problemet ligger *inte* i LLM's förmåga att översätta, utan i **Retrieval-fasen**. Eftersom min text-embedding-modell (`all-MiniLM-L6-v2`) är tränad på engelska, och min databas består av engelska termer, kan inte ChromaDB mappa den matematiska vektorn för det svenska ordet "undantagshantering" mot det engelska ordet "exception handling". Resultatet blir att fel glosor hämtas, och LLM svarar korrekt att den "inte vet"

**Potentiella framtida lösningar (Out of scope för v1.0):**
1. Fortsätta använda systemet "as-is" och rekommendera engelska söktermer i dokumentationen.
2. Applicera ett översättningslager (API) på användarens fråga *innan* den skickas in i vektordatabasen.
3. Byta ut embedding-modellen mot en flerspråkig modell (multilingual embedding model)
# Theory: Google GenAI, Super-Prompts, and Context

## 1. Why do we need Super-Prompts?
A Large Language Model (LLM) like Gemini is basically an incredibly advanced guessing machine. If you ask it "What is .wal in Johnny's database?" it will guess, hallucinate, or give a generic answer based on its public training data.

A **Super-Prompt** is how you force the LLM to stop guessing and start reading. We build an invisible string of text (a wrapper) around the user's question:

> "You are a professional Data Engineering teacher.
> Your task is to answer the user's question, but you may ONLY use the information found in the Context block below. If the answer is not in the context, say you don't know.
> 
> CONTEXT:
> {Here we inject the results from our get_relevant_context() function}
> 
> USER QUESTION:
> {Here we paste what the user typed into the API}"

When Gemini receives this Super-Prompt, it transforms from a "knowledgeable but sloppy guesser" into a strict expert restricted to your exact course literature.

---

## 2. Prompt Engineering & "Lost in the Middle" (Svensk förklaring)

**Frågeställning:** Spelar ordningen på reglerna i min super-prompt någon roll?

**Svar:** Ja, ordningen spelar en enorm roll. Detta beror på ett fenomen som kallas **"Lost in the Middle"**

Large Language Models (LLMs) läser text uppifrån och ner. De har extremt lätt för att komma ihåg och lyda det som står allra först i texten, och det som står allra sist. Det som hamnar i mitten (vilket oftast är den stora mängden inskjuten kontext-data) får mindre "Attention" av modellens neurala nätverk.

**Branschstandard för att bygga en Super-prompt:**
* **Toppen (Persona & Huvudregler):** Definiera vem AI:n är (t.ex "Pedagogisk Data Engineering-assistent") och de absoluta, oföränderliga huvudreglerna (t.ex "Inga hallucinationer", "Språkregler")
* **Mitten (Faktan):** Databas-kontexten. Det gör inget om modellen tappar lite fokus här, för den ska enbart använda detta som ett uppslagsverk.
* **Botten (Uppgiften):** Användarens specifika fråga. Eftersom frågan ligger allra sist, är det den absolut färskaste "tanken" i AI'ns kontextfönster precis när den ska generera sitt svar.

**Tips för regler:** AI-modeller reagerar väldigt bra på formatering. Att skriva nyckelord med STORA BOKSTÄVER (exempelvis `ENBART`, `MÅSTE`) hjälper modellens Attention-mekanism att vikta dessa instruktioner högre.
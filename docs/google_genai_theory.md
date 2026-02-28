# Theory regarding google-genai, super-prompts and context

```text
A Large Language Model (LLM) like Gemini is basically an incredibly advanced guessing machine. If you ask it "What is .wal in Johnny's database?" it will guess, lie (hallucinate) or give a generic answer.

A super-prompt is how you force it to stop guessing. In Python, I need to build an invisible string of text that looks something like this:

"You are a professional Data Engineering teacher.
Your task is to answer the user's question, but you may ONLY use the information found in the Context block below. If the answer is not in the context, say you don't know.

CONTEXT:
{Here we paste our get_relevant_context() function into the three words}

USER QUESTION:
{Here we paste what the user typed into the API}"


And when Gemini receives this Super Prompt, it transforms from a "knowledgeable but sloppy guesser" to an "expert on your exact course literature."

```

## Theory surronding prompt engineering and rules explained in Swedish:

```text
Frågeställning: Spelar ordningen på reglerna i min super prompt någon roll? (src/rag.py)

Svar:

Ordningen spelar en enorm roll. Teorin bakom Prompt-strukturen (Lost in the Middle)

Large Language Models (LLMs) läser text uppifrån och ner, ungefär som människor gör, men de lider av ett välkänt problem som kallas "Lost in the Middle"
De har extremt lätt för att komma ihåg och lyda det som står allra först i texten, och det som står allra sist. Det som hamnar i mitten (ofta den stora mängden kontext-data) får lite mindre uppmärksamhet.


Att bygg Super-prompts som följer branschstandard (Enligt Gemini 3.1 pro):

Toppen (Vem du är & Vad som gäller): 
- Persona (Pedagogisk Data Engineering-assistent) och de absoluta, oföränderliga huvudreglerna (ENBART basera ditt svar på informationen..., SPRÅK REGEL).

Mitten (Faktan): 
- Databas-kontexten. Det gör inget om modellen "glömmer" lite här, för den ska bara använda det som ett uppslagsverk.

Botten (Uppgiften): 
- Användarens fråga. Eftersom frågan ligger allra sist, är det den absolut färskaste tanken i AI:ns "hjärna" precis när den ska börja spotta ur sig sitt svar.

Din SPRÅK REGEL är också jättebra formulerad. Även om du hade en liknande mening i stycket ovanför, skadar det absolut inte att vara övertydlig. AI-modeller älskar när man skriver med STORA BOKSTÄVER för viktiga sökord som ENGELSKA och SVENSKA.
```
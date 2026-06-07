## Rag reponse issues.
Problem: After changing API keys and what model i use for my RAG responses(from googles Gemini dev API to grunden.ai) I stumbled upon a few issues with my RAG answers.

- When asking a test query to try the RAG engine i got back these sources: `'sources': ['assignment', 'backup', 'pull', 'output', 'string']`.  
Chroma DB didnt find any terms related to 'undantagshantering' and it returned completely unrelated words, this is a documented with Swedish limitation when using this model: `all-MiniLM-L6-v2`. The model maps the Swedish query to the wrong spot in my vector space(?). But that does not really explain the absurd answer I got back. 

- The answer i got back was this:

```
Testar RAG-motorn...

Fråga: 'Hur fungerar undantagshantering?'

--- SVAR ---
{'answer': 'It looks like you just typed "prompt"! I can definitely help you with that, but I need a little more direction. \n\nWhat kind of prompt are you looking for? Here are a few ways I can help:\n\n**1. Writing Prompts (to spark a story)**\n*   *Example:* "Write a story about a clockmaker who discovers that one of their antique clocks can freeze time, but only for the person holding it."\n\n**2. Image Generation Prompts (for Midjourney, DALL-E, etc.)**\n*   *Example:* "A cozy, magical apothecary shop tucked away in a rainy cobblestone alley, glowing jars of luminescent potions on wooden shelves, hyper-detailed, cinematic lighting, Studio Ghibli style."\n\n**3. Productivity Prompts (to help you work or learn)**\n*   *Example:* "Act as an expert editor. Review the following text and suggest improvements for clarity, tone, and grammar."\n\n**4. Roleplay/Fun Prompts (to chat with an AI persona)**\n*   *Example:* "Act as a stoic Spartan warrior who has accidentally time-traveled to a modern-day shopping mall. Answer my questions from that perspective."\n\n**Tell me what you are trying to do!** Are you trying to write a story, generate an image, learn something new, or something else entirely?', 'sources': ['assignment', 'backup', 'pull', 'output', 'string']}
```

- While trying to figure out this issue and with a bit of guidance Im starting to understand that its confusing for the `GLM 5.1`-model I am now using. It gets confused around where in my super prompt `the A(augmented) in RAG(See line 106 in rag.py)`. As it is now I send the entire prompt as a single `user message`. That means: my Instructions + context + question, all in one.

- The model doesn't know where ONE ends and the other begins and got stuck on the word `prompt`, which is my named variable for my `super prompt` that contains all my rules on how it should act.

---

### The solution:
Split it up in `system(instructions + context)` and `user(the query(question))`. This is apparently how all modern chat models expects their structured prompts to look like. The change is only in my `generate_rag_response`-function.

- From this:
```python
def generate_rag_response(user_query: str) -> dict:
    """Main function for RAG: Get context and let LLM formulate an answer"""

    # 1) R (Retrieval), hämta faktan(user_query + slugs)
    context_text, source_slugs = get_relevant_context(user_query)

    # 2) A(Augmented), bygg den super prompt och de regler som LLM ska använda sig av.
    prompt = f"""You are a pedagogical and highly skilled Data Engineering assistant.
    Your task is to accurately answer the user's question.
     
    CRITICAL RULES:
    1. NO HALLUCINATIONS: You must ONLY base your answer on the information provided in the context block below. Do not invent external information.
    2. LANGUAGE MATCHING (ABSOLUTE): You MUST reply in the exact language of the user's question. 
       - If user asks in English -> Reply in English. 
       - If user asks in Swedish -> Reply in Swedish.
    3. TRANSLATION PERMITTED: You are allowed to translate the context database into the user's language to fulfill Rule 2.
    4. FALLBACK: If the answer cannot be found in the context, reply in the user's language that you do not know based on the available information, and ask them to search for another term.

    --- CONTEXT FROM DATABASE ---
    {context_text}
    
    --- USER'S QUESTION ---
    {user_query}
    """

    # 3) G(Generation), Skicka vidare till GLM 5.1 via Grunden.ai
    # OpenAI-format: Svaret sitter i choises[0].message.content
    # (choises är en lista, designat för när man ber om flera alternativ. Jag kör på [0])
    response = ai_client.chat.completions.create(
        model="glm-5.1", messages=[{"role": "user", "content": "prompt"}]
    )

    # Returnera en dict med både AI svaret och sources
    return {"answer": response.choices[0].message.content, "sources": source_slugs}
```
---
- To this:

```python
def generate_rag_response(user_query: str) -> dict:
    """Main function for RAG: Get context and let LLM formulate an answer"""

    # 1) R (Retrieval), hämta faktan(user_query + slugs)
    # Hämtar kontext från ChromaDB
    context_text, source_slugs = get_relevant_context(user_query)

    # 2) A (Augmentation) - Injucera den hämtade kontexten i instruktionen, det är context_text
    # inbäddad i system_message som är augmenteringen
    system_message = f"""You are a pedagogical and highly skilled Data Engineering assistant.
    Answer the user's question using ONLY the context below. No hallucinations.
    Reply in the exact same language as the user's question.
    If the answer is not in the context, say so and suggest another search term.

    --- CONTEXT FROM DATABASE ---
    {context_text}"""

    # 3) G(Generation), skicka augmenterad kontext + fråga till LLM (GLM 5.1 via Grunden.ai)
    # OpenAI-format: Svaret sitter i choices[0].message.content
    response = ai_client.chat.completions.create(
        model="glm-5.1",
        messages=[
            {
                "role": "system",
                "content": system_message,
            },  # <-- instruktioner + kontext
            {"role": "user", "content": user_query},  # <-- bara frågan
        ],
    )

    # Returnera en dict med både AI svaret och sources
    return {"answer": response.choices[0].message.content, "sources": source_slugs}
```

Now it works as intended. Reasoning to unserstand with conceptual breakdown below:

```
The Conceptual Point to understand.
Think of it this way: if you had a consultant helping you answer questions, and you gave them a reference book to look up - that's augmentation. It doesn't matter if you gave them the book in an envelope or a bag. The augmentation is the act of giving them the book, not the format it's delivered in.
{context_text} injected into system_message = you give the LLM the book. That's the A.
```
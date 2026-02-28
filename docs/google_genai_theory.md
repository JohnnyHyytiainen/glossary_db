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

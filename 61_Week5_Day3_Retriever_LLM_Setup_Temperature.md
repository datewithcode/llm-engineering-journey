# LLM Engineering – Week 5, Day 3 (Part 2)
## Setting Up the Retriever and the LLM, the Same-Encoder Rule, and Temperature (the lecturer's explanation)

> Personal study notes. Read file 60 (retriever and LLM objects) first.
> Concepts first; the code is at the end of each section for reference only.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. **Same encoder rule:** the encoder used to turn **questions** into vectors must be the **same** one used on Day 2 to turn **chunks** into vectors. Otherwise the lengths don't match (crash) and, more deeply, they'd be on **different meaning maps**.
2. **Two helpers:** the **retriever** (librarian) fetches the closest chunks; the **LLM** (expert) reads them and writes the answer. Your code (the secretary) carries things between them.
3. **The expert is swappable:** OpenAI, Claude or a local Llama all respond to the same "go" button (`invoke`), so nothing else changes.
4. **Temperature** controls how the next word is picked from the model's probabilities. **0 = always the most likely word** (steady answers). Higher = more variety; near 2 = odd.
5. Temperature is **not really "creativity"**: for creativity, use the **system prompt** and examples. And temperature 0 is **not a full guarantee** of identical answers.

---

## 1. The Same-Encoder Rule

### The concept
On Day 2, the encoder placed every chunk on a meaning map. Today the question must be placed on **that same map**, so it must use **the same encoder**.

### Two ways it goes wrong if you mix encoders
| Problem | What happens |
|---|---|
| **Different lengths** | Database built with OpenAI large (3,072 numbers per vector); question made with MiniLM (384). The comparison fails with "a nasty ugly stack trace about mismatch in dimensions." |
| **Different maps** (the deeper reason) | Every encoder draws its own map (Day 2's pictures looked completely different per encoder). Comparing points across two maps gives nonsense matches, even if the lengths happened to be equal. |

**Rule: same encoder for storing and for asking.**

### The lecturer's setup
He rebuilt the database with **all-MiniLM-L6-v2** (the original, weaker one) in case you stuck with it. If yours was built with an OpenAI encoder, use `OpenAIEmbeddings` here, or rebuild the database.

```python
# Reference code (from the notebook)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="vector_db", embedding_function=embeddings)
```

---

## 2. The Two Helpers

### The picture
- **Librarian = retriever.** Gets the question, places it on the same meaning map, brings back the closest chunks of text. **Does not answer.**
- **Expert = LLM.** Gets the question plus the librarian's pages, reads them, **writes the answer**. Sees only English, never the map or numbers.
- **Secretary = your code.** Carries the question to the librarian, the pages to the expert, the answer back to the customer.

```
Customer -> Secretary -> Librarian (fetch pages) -> Secretary -> Expert (write answer) -> Secretary -> Customer
```

### Swappable expert
LangChain lets you replace the expert (OpenAI, Anthropic, local Llama via Ollama) without changing anything else, because they all respond to the same `invoke` button. The lecturer: that's "the promise of LangChain," similar to LiteLLM but heavier (each provider is a separate package to install and import).

```python
# Reference code
retriever = vectorstore.as_retriever()              # wraps Chroma (+ its encoder) as a retriever
llm = ChatOpenAI(temperature=0, model_name=MODEL)   # MODEL = "gpt-4.1-nano"

# Swappable alternatives the lecturer showed:
# from langchain_ollama import ChatOllama
# from langchain_anthropic import ChatAnthropic
```

---

## 3. Temperature (the lecturer's own explanation)

*(File 41 has the ice cream shop picture as extra explanation; this section is what the lecturer actually says.)*

### What the model really outputs
It doesn't output one word. For the next token, it gives **every possible token a probability**:
```
Next word after "The CEO of Insurellm is ..."    (illustration, my numbers)
   "Avery"    80%
   "the"      12%
   "a"         6%
   "banana"    0.01%
   ... every token gets some chance
```

### What temperature does

| Temperature | How the next token is picked | Result |
|---|---|---|
| **0** | Always the **highest-probability** token | Most predictable, steady |
| **1** | **Sampled by probability**: a token with 10% chance is picked about 10% of the time; a 1% token about 1 in 100 times | More variety in wording |
| **near 2** (OpenAI's range is 0 to 2) | Unlikely tokens picked much more often | Can get "quite strange answers" |

### Correction 1: it isn't really "creativity"
People say "higher temperature = more creative." The lecturer: not wrong, but misleading. It just changes word choices, sometimes oddly.
- **Want creativity?** Say so in the **system prompt**, and give examples of what creative means to you.
- **Want a different answer?** Show the model its **previous answers** and ask for something different. More reliable than temperature.
- In short: **focus on prompting** for behaviour.

### Correction 2: temperature 0 is not a full guarantee
Even at 0, output isn't guaranteed to be identical, because:
- there are **random numbers** involved in running LLMs; setting a **random seed** fixes them (the course does this in **Weeks 6 to 8**, important for testing)
- labs **change their models**
- **parallel calculations** for performance can't always be guaranteed to run the same way

With temperature 0 **and** a random seed you're "pretty likely" to get the same answer, but nothing is fully guaranteed.

### Why RAG uses temperature 0
You want reliable, steady answers based on the retrieved facts. 0 is "quite common with RAG systems"; around **0.5 to 0.7** is also typical.

---

## How to Explain This to Someone

### If a non-technical person asks "What is temperature in AI?"
"When an AI writes, it ranks every possible next word by how likely it is. Temperature decides whether it always takes the top-ranked word (temperature 0, steady and predictable) or sometimes picks a less likely one (higher temperature, more varied wording). It's not really a creativity dial; if you want creative writing, it's better to ask for it in the instructions."

### If a technical person asks
"At inference the model outputs a probability distribution over the vocabulary for the next token. Temperature 0 is greedy decoding (argmax); temperature 1 samples from the distribution as-is; higher values flatten it so low-probability tokens appear more often (OpenAI allows 0 to 2). It affects lexical variety, not reasoning. Temperature 0 plus a fixed seed improves reproducibility but doesn't guarantee it, due to model updates and non-deterministic parallel computation. RAG typically uses 0 for consistency. Separately, the query must be embedded with the same model used to build the index, or you get dimension mismatches or meaningless similarity."

### The analogy
Librarian fetches, expert answers; temperature is how strictly the expert sticks to the most likely next word.

### The one-liner
"Embed questions with the same encoder as the index; use temperature 0 for steady RAG answers, and use prompting, not temperature, for creativity."

---

## Self-Check

1. Why must the question encoder match the database encoder? Give both reasons.
2. What error appears if dimensions don't match?
3. What does the librarian (retriever) do? What does it not do?
4. Why can you swap ChatOpenAI for ChatAnthropic without changing other code?
5. What does an LLM actually output for the next token?
6. What happens at temperature 0? At 1? Near 2?
7. If you want more creative answers, what should you change instead of temperature?
8. Give two reasons temperature 0 doesn't guarantee identical answers.
9. What temperature is common for RAG, and why?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| Same-encoder rule | Use the same embedding model for indexing and querying |
| Dimension mismatch | Error from comparing vectors of different lengths |
| `as_retriever()` | Turns a Chroma store into a retriever object |
| `ChatOpenAI` | LangChain's OpenAI chat model wrapper |
| `ChatOllama`, `ChatAnthropic` | Swappable alternatives (local Llama, Claude) |
| Temperature | Controls how the next token is chosen from probabilities |
| Greedy (temperature 0) | Always pick the most likely token |
| Sampling (temperature 1) | Pick tokens in proportion to their probability |
| Random seed | Fixes the random numbers so runs repeat more reliably |

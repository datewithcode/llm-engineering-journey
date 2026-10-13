# LLM Engineering – Week 5, Day 1 (Part 3)
## The Full RAG Flow: Must-Know Concepts (interview-ready)

> Personal study notes. This file is the condensed, interview-focused version of all of Week 5 Day 1.
> Files 52 (toy RAG) and 53 (vectors) hold the longer explanations. If short on time, read only this file.
> Companion: the animated "RAG, Step by Step" artifact (14 steps, Heathrow example) shows this flow moving.

---

## READ THIS FIRST (whole of Day 1 in 5 lines)

1. **RAG** = your code finds relevant text and **pastes it into the prompt** before calling the LLM. The LLM answers from what it just read.
2. The hard part is **choosing which text**. Matching exact words is brittle ("Who is Avery?" finds nothing).
3. Real RAG matches by **meaning**: an **embedding model** turns text into a **vector** (list of numbers). Similar meaning = nearby vectors.
4. Two phases: **ahead of time**, every document becomes a vector and is saved as a (text, vector) pair in a **vector store**. **At question time**, the question becomes a vector, the store returns the **text** of the nearest entries, and that text goes into the prompt.
5. **The LLM never sees vectors.** It understands language, not lists of numbers. Vectors are only for searching.

---

## 1. What RAG Is, and WHY

**The problem:** the LLM was trained on the internet. It has never seen your company's private files (Insurellm's employees, products, contracts).

**The fix:** before calling the LLM, your code fetches the relevant document and adds it to the prompt.

| Letter | Meaning | Who does it |
|---|---|---|
| **R**etrieval | Fetch the relevant text | Your code (with the vector store) |
| **A**ugmented | Add that text to the prompt | Your code |
| **G**eneration | Write the answer | The LLM |

The LLM is **not retrained**. It is the same model; the answer is right only because the fact was in the text it read.

**WHY not paste every document every time?** Too many tokens: slow, expensive, and may not fit in the context window (file 10). So you paste only the relevant pieces. The lecturer: RAG exists "to avoid having to put everything in the context."

**WHY not fine-tuning?** Fine-tuning = training the model further on your data. The lecture calls it the harder, older way. RAG is low cost, low barrier, and much quicker to market.

---

## 2. Knowledge Base

A **knowledge base** is just the collection of your documents (a "fancy term for a database"). In the course: the Insurellm share drive with folders `company`, `contracts`, `employees`, `products`.

---

## 3. Why Keyword Lookup Fails (the toy RAG, file 52)

The toy version looked for exact words: the question contains "lancaster", so it fetched Lancaster's file.

| Failure | Example | What happens |
|---|---|---|
| **Miss** | "Who is Avery?" | No key matches; nothing fetched |
| **Wrong match** | "Who is Alex Lancaster?" | Fetches Avery Lancaster's file for the wrong person |

Also fails on typos and different words for the same thing ("Heathrow" vs "London"). **Lesson: match meaning, not spelling.**

---

## 4. Two Kinds of LLM

| | Autoregressive LLM | Encoder / embedding model |
|---|---|---|
| Examples | GPT, Claude, Llama, Gemini | OpenAI text-embedding-3-large / -small, all-MiniLM-L6-v2, BERT |
| Output | Next token, repeated | One list of numbers for the whole input |
| Job in RAG | **Writes the answer** | **Finds the relevant text** |

---

## 5. Vector Embedding

- An embedding model turns text into a **list of numbers** (a **vector**) representing its **meaning**.
- Think of the numbers as **coordinates**: each text becomes a point on a "meaning map."
- **Close together = similar meaning.** "Ticket prices from New York to London" and "price of a flight from JFK to Heathrow" share almost no words but land close together.
- This is a **trained property**: the model was trained so similar meanings get similar numbers.
- Real vectors have **hundreds or thousands** of numbers.
- How "close" is measured: **cosine similarity** (the lecturer named it as a technicality for later). *(Extra, not from the lecture: it compares the direction two vectors point.)*

**Tokens vs vectors:** tokens are the **input** (text as ID numbers, a simple lookup). Vectors are the **output** (meaning, produced by the model).

---

## 6. Vector Data Store

A database holding **each piece of text together with its vector**.

```
| Text (pasted into prompts)              | Vector (used for searching) |
| Ticket prices to London: £450 return    | [8.5, 1.5]                  |
| Hotel rooms in Paris: €200 a night      | [6.0, 3.5]                  |
| Avery Lancaster is the CEO of Insurellm | [3.0, 6.0]                  |
```
*(Illustration only: 2 hand-picked numbers per vector so it can be drawn.)*

**WHY store both?** The vector is for **finding**. The text is what gets **pasted into the prompt**. The LLM can only use the text.

---

## 7. The Full Flow (the most likely interview question)

### Phase 1: ahead of time (runs once, not per question)

```
1. Your code reads every file in the knowledge base          (plain text)
2. Your code  →  embedding model : document text
3. Embedding model  →  your code : vector  [8.5, 1.5]
4. Repeat for every document
5. Your code  →  vector store    : save (text, vector) pairs
```

### Phase 2: every time a customer asks

```
 6. Customer  →  your code            : "What are ticket prices to Heathrow?"
 7. Your code  →  embedding model     : the question text   (the SAME embedding model as Phase 1)
 8. Embedding model  →  your code     : question vector [8.3, 2.3]
 9. Your code  →  vector store        : "which stored vectors are closest to [8.3, 2.3]?"
10. Vector store  →  your code        : the TEXT "Ticket prices to London: £450 return"
                                        (the vector stays behind; only English moves on)
11. Your code builds the prompt       : system prompt + retrieved text + question
12. Your code  →  LLM                 : that prompt (English only, no numbers)
13. LLM  →  your code                 : "Return tickets to London Heathrow are £450."
14. Your code  →  customer            : the answer
```

**Why the SAME embedding model in both phases?** So the question and the documents are placed on the same map. The lecturer: "we've already used that same encoder to turn all of the data ... into vectors as well."

**Note "Heathrow" appears in no document.** Keyword lookup would fetch nothing. Meaning lookup finds London because Heathrow is London's airport.

---

## 8. The Two Models Are Separate (confuses even pros)

- The **embedding model** is used only for the fuzzy search. It has "nothing to do with" the LLM.
- The **LLM never sees vectors.** It "wouldn't know what to do with a bunch of numbers." Its input must be language: the user's question plus the retrieved English text.
- The LLM doesn't even know an embedding model was used.

---

## 9. Testing Trap: Conversation History

"Who is Avery?" got answered correctly in the demo only because Avery's file was already in the **earlier chat history**. Retrieval had actually failed. **Always test retrieval in a fresh chat** (file 52, section 6b).

---

## 10. RAG Is Empirical

The lecturer calls RAG "one big hack": using encoder tricks to guess which context will be useful. There's "a whole zoo of hacks" to improve it, and it's a lot of **trial and error**. Coming next: LangChain, and a vector store called **Chroma**.

---

## Optional (fine to skip for interviews)

- king - man + woman = queen (word2vec): nice proof the numbers capture meaning; not needed for RAG (file 53, section 3b).
- BERT history, list-comprehension style, glob paths, the LLM positivity bias in synthetic data (file 52), the course roadmap.

---

## How to Explain This to Someone

### If a non-technical person asks "What is RAG?"
"An AI chatbot doesn't know your company's private documents. RAG is a way around that: before the AI answers, the system searches your documents for the parts most related to the question and hands them to the AI along with the question. The AI then answers using those pages. The clever part is that the search works by meaning, so 'flights to Heathrow' still finds the page about London ticket prices."

### If a technical person asks
"RAG has an indexing phase and a query phase. At indexing time, documents (or chunks) are embedded with an encoder model and stored as (text, vector) pairs in a vector store. At query time, the query is embedded with the same encoder, a nearest-neighbour search (typically cosine similarity) retrieves the closest entries, and their text is injected into the prompt of an autoregressive LLM, which generates the answer. The LLM only ever sees natural language; embeddings are purely for retrieval. It's cheaper and faster to ship than fine-tuning, and retrieval quality is tuned empirically."

### The analogy
A librarian with a meaning map: every book was pinned on the map ahead of time. Your question gets pinned too, the librarian pulls the books nearest your pin, and the expert reads those pages to answer you. The expert reads pages, never the map.

### The one-liner
"RAG embeds your documents and the question as vectors, retrieves the text closest in meaning, and pastes it into the LLM's prompt."

---

## Self-Check

1. What do R, A and G stand for, and who does each part?
2. Why not paste every document into every prompt?
3. Why is RAG often preferred to fine-tuning, per the lecture?
4. Give the two failure types of keyword lookup, with examples.
5. Name the two kinds of LLM and the job of each in RAG.
6. What is a vector embedding? What does "close together" mean?
7. What two things does the vector store keep for each entry, and why both?
8. Walk through Phase 1 and Phase 2 from memory, showing your code in every step.
9. Why must the same embedding model be used in both phases?
10. At step 10, what does the store return? What happens to the vector?
11. Why does the LLM never receive vectors?
12. Why can "Who is Avery?" seem to work in a chat even though retrieval failed?
13. What is cosine similarity (one line)?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| RAG | Retrieval Augmented Generation: fetch relevant text, add it to the prompt, let the LLM answer |
| Knowledge base | Your collection of documents |
| Embedding model / encoder | Model that turns text into a vector; used only for searching |
| Autoregressive LLM | The answer-writing model (GPT, Claude); predicts the next token |
| Vector / vector embedding | List of numbers representing the meaning of a text |
| Vector data store | Database of (text, vector) pairs |
| Indexing (Phase 1) | Embedding all documents and saving them, done ahead of time |
| Retrieval (Phase 2) | Embedding the question and fetching the nearest texts |
| Cosine similarity | The usual measure of how close two vectors are |
| Fuzzy lookup | Finding by meaning rather than exact spelling |
| Chroma | The vector store used in the next lectures |

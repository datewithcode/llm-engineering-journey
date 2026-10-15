# LLM Engineering – Week 5, Day 3 (Part 5)
## The RAG App in Action, and Its Rough Edges (RAG Is Whack-a-Mole)

> Personal study notes. Read file 63 (production modules, history fix, combined question) first.
> This closes Week 5 Day 3. Day 4 is about **evals**: measuring RAG properly.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. **The broken simple version:** "Who is Avery?" then "How much is her salary?" gave **Samantha Green's** salary. Two causes: no history sent to the LLM, and retrieval searched only "how much is her salary?" so it grabbed a random salary chunk.
2. **The new app** (`uv run app.py`): chat on the left, **retrieved context on the right** (5 chunks, with their source). Now "what is her salary?" correctly answers about Avery.
3. **Rough edge 1, chunks lose context:** asked who won the Innovator of the Year award, it answered "**Maxine**" but not "Maxine Thompson", because the chunk with the award didn't contain her full name (that was at the top of the document).
4. **Rough edge 2, the combined-question fix backfired:** after chatting about Avery, a **new-topic** question (the award) failed, because the combined search text was dominated by Avery.
5. **RAG is hit and miss, a bit like whack-a-mole:** fixing one problem can create another. Tomorrow: **evals**, a scientific way to measure and improve.

---

## 1. Why the Simple Version Broke

In the Day 3 notebook's five-line version (file 62):
```
User: Who is Avery?                -> good answer
User: How much is her salary?      -> "Samantha Green's current salary is ..."   (wrong person!)
```

| Cause | What went wrong |
|---|---|
| **No history to the LLM** | The LLM had no idea "her" meant Avery |
| **Retrieval used only the last message** | The search text was "How much is her salary?", so it fetched the first chunk with "salary" in it: Samantha Green's. A **red herring** answer |

These are exactly the two fixes in `answer.py` (file 63): send history (via `convert_to_messages`), and search on the **combined** user messages.

---

## 2. The New App: "Insurellm Expert Assistant"

Run: `cd implementation` then `uv run ingest.py`; then from `week5`, `uv run app.py`.

### The layout
| Left | Right |
|---|---|
| The **conversation** | The **retrieved context** for the latest answer |

On the right:
- **White text** = the chunk text **actually sent to the LLM**.
- **Orange text** = the **source** (metadata, which file it came from). Shown to you, **not** sent to the LLM.
- **5 chunks** appear, because **k = 5**.

This is the "show the documents it used" feature promised at the start of Day 3.

### It works with follow-ups now
```
User: Who is Avery?          -> correct answer; right panel shows Avery's chunks
User: And what is her salary? -> answers about Avery's salary; the salary is in one of the retrieved chunks
```
The LLM got the history (knows "her" = Avery) **and** the retrieval found Avery's salary chunk. "RAG with history with lookup."

---

## 3. Rough Edge 1: A Chunk Can Lose Crucial Context

### The test
Maxine Thompson's HR record says she won the **inaugural Innovator of the Year (IOTY) award in 2023**.
Question: "Who won the prestigious IOTY award?"

### What happened
- It answered "**Maxine**". Good, it found it.
- But **not "Maxine Thompson"**: her full name wasn't in the chunk.

### Why
Her **full name was at the top** of the HR document. The award was mentioned **in the middle**, in a different chunk that only said "Maxine". The chunk answered the question but lacked context from elsewhere in the document.

*(Connects to file 56: chunking cuts a document into pieces, and each piece only knows what's inside it.)*

**Lesson:** a chunk can contain the answer but miss crucial context from elsewhere in the same document. The result is "okay but not perfect."

---

## 4. Rough Edge 2: The Combined-Question Fix Created a New Problem

### The test (fresh conversation)
```
User: Who is Avery?                       -> good
User: And what did Avery do before?       -> good (senior product manager before Insurellm)
User: Who won the prestigious award?      -> doesn't know!
```

### Why
The combined-question fix (file 63) searches on **all the user's messages joined together**:
```
"Who is Avery? And what did Avery do before? Who won the prestigious award?"
```
That search text is **mostly about Avery**, so the retriever keeps fetching **Avery chunks**, not Maxine's award chunk. The right panel confirms it: still Avery.

### The trade-off
| Search on... | Good at | Bad at |
|---|---|---|
| Only the latest message | Topic changes | Follow-ups ("her salary") |
| All messages combined | Follow-ups | **Topic changes** (old topics drown the new one) |

There are many ways to fix this, "some better than others." The course works on problems like this over the next couple of days.

---

## 5. The Big Lesson: RAG Is Hit and Miss

- RAG can work **really well** (it found Maxine's award buried in a document).
- It can be **incomplete** (no full name).
- It can be **thrown off track** (topic change after Avery).
- It's **experimental and hacky**: you find a problem, fix it, find another. Like **whack-a-mole**. Sometimes **fixing one problem causes another** (the history fix caused the topic-change problem).
- Getting better = solving these puzzles one by one with different techniques.
- There's a **more scientific way** to do this: **evals** (tomorrow).

### The "conjuring trick"
It **looks like** an expert on your whole knowledge base. In reality, at any moment it only sees **a few chunks** pulled by vector similarity, pasted into the prompt. "It's a trick. It's a conjuring trick." It works really well, with rough edges.

---

## 6. Homework (the lecturer's mission)

1. `cd implementation` then `uv run ingest.py` (populate Chroma).
2. From `week5`: `uv run app.py`.
3. **Experiment and find the rough edges:**
   - Find great examples of deep expertise from information buried in documents.
   - Find cases where it **fails** on something clearly in the documents.
   - **Watch the chunks on the right** and understand **why** they were surfaced.
4. Keep a list of blind spots; the course will fix them starting tomorrow.

---

## 7. Recap and What's Next

**You can now:** generate text and code with frontier and open-source models, use tools, choose the right model, and **implement a RAG expert question-answering system**. The lecturer's "dark secret": it's actually quite easy.

**Next (Day 4):**
- The importance of **evaluations (evals)** to **measure** how effective a RAG system is.
- Experiment with **encoders** and **chunking strategies**, using metrics to see how much difference each change makes and to decide between solutions.

---

## How to Explain This to Someone

### If a non-technical person asks "Does your company chatbot always get it right?"
"No. It searches our documents for the few most relevant passages and answers from those, so it can miss things: a passage might mention 'Maxine' but not her surname, or if you've been talking about one person, it can keep pulling up that person's records when you switch topics. Each fix can create a new issue, so the next step is measuring it properly with tests."

### If a technical person asks
"The app surfaces the k=5 retrieved chunks with their sources alongside the chat, which makes failures easy to diagnose. We saw two classic issues: chunk context loss (the award chunk lacked the entity's full name, which lived in the document header) and query drift from concatenating all prior user turns, which helps follow-ups but hurts topic switches. RAG tuning is iterative and can regress, which is why you need an evaluation set and metrics before changing encoders, chunking or query construction."

### The analogy
Whack-a-mole: fix one problem and another pops up, so you need a scoreboard (evals) to know if you're actually winning.

### The one-liner
"RAG feels like an expert on everything but only ever sees a few chunks at a time, so it has rough edges you fix one by one, and need evals to measure."

---

## Self-Check

1. Why did "How much is her salary?" return Samantha Green's salary in the simple version? Give both causes.
2. What's shown on the right side of the new app? What's the difference between the white and orange text?
3. Why are there 5 chunks?
4. Why did it answer "Maxine" but not "Maxine Thompson"?
5. What general chunking problem does that show?
6. After talking about Avery, why couldn't it answer who won the award?
7. What's the trade-off between searching on the latest message vs all messages?
8. Why does the lecturer compare RAG to whack-a-mole?
9. Why is RAG a "conjuring trick"?
10. What will Day 4 introduce, and why is it needed?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| Red herring answer | A confident answer about the wrong thing, caused by fetching the wrong chunk |
| Retrieved context panel | The app's right side showing which chunks were used |
| Chunk context loss | A chunk has the answer but lacks key info (like a full name) from elsewhere in the document |
| Query drift | Combined search text dominated by earlier topics, missing the new one |
| Whack-a-mole | Fixing one problem, another appears |
| Evals (evaluations) | Tests and metrics that measure how well the RAG system works (Day 4) |
| IOTY | Innovator of the Year award (from Maxine Thompson's HR record) |

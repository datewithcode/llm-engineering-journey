# LLM Engineering – Week 5, Day 2 (Part 1)
## What Day 2 Covers, and LangChain: What It Is, the Good and the Bad

> Personal study notes. Read file 54 first (the full RAG flow). Today builds the real version of that flow.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. **Day 2 goal:** replace Day 1's toy keyword lookup with the real thing. By the end of the day: explain LangChain (good and bad), work with embedding models, **split documents into chunks, turn chunks into vectors, store them in a vector store called Chroma**.
2. **Recap of the flow:** the question becomes a vector (via an encoder / embedding model), the vector store finds similar stored information, and that information goes into the prompt for the LLM.
3. **LangChain** = an open-source Python library of ready-made parts for LLM jobs (loading files, splitting text, making vectors, storing and searching them, calling LLMs), plus a way to connect them into pipelines.
4. **Good:** much quicker to build assistants, RAG and summarization; robust tools out of the box; very common in enterprise (good resume material).
5. **Bad:** less needed than it used to be; heavyweight with a learning curve and its own terminology; starting to feel legacy next to lighter options like LiteLLM.

---

## 1. WHY Day 2 Exists

Day 1's toy RAG broke the question into words and looked each word up in a dictionary. That can miss important information ("Who is Avery?" found nothing).

The fix is a **fuzzy search by meaning**, using vectors (files 53 and 54). Day 2 is where that is actually built and where you first **look at vectors inside Chroma**.

---

## 2. Recap: the Flow (from the lecture)

```
1. Customer asks a question (it arrives at your code)
2. Your code sends the question to an encoder / embedding model
3. The embedding model returns a vector that represents the question's meaning
4. Your code asks the vector data store for the entries most similar to that vector
5. Your code puts that retrieved information into the prompt
6. Your code calls the LLM; the answer is based on that relevant context
```

The vector data store is "a database which is quick at finding similar information to the vector that you just passed in." Full step-by-step version: file 54, section 7.

---

## 3. What LangChain Is

### The picture that clicks: it's a library, like `requests`

To read a web page you don't write socket code by hand. You write `requests.get(url)` and a library has done the boring work.

**LangChain is the same kind of thing, for LLM jobs.** It is a Python library of **pre-written parts**:

| Job in a RAG app | Day 1 (by hand) | With LangChain |
|---|---|---|
| Read the files | a `glob` loop | a ready-made loader |
| Split documents into pieces | not needed in toy version | a ready-made splitter |
| Turn text into vectors | not needed in toy version | a ready-made embedding wrapper |
| Save and search vectors | a plain dict | a ready-made vector-store wrapper (Chroma) |
| Call the LLM | `openai.chat.completions.create(...)` | a ready-made chat model wrapper |

Think of **puzzle pieces**: each piece is one job, and you snap them together so one piece's output feeds the next. That snapping together is the "chain" in the name.

**What does NOT change:** the Day 1 flow. Your code is still the secretary, the embedding model is still a separate machine, and the LLM still only reads English. LangChain only saves you from writing every step by hand. You still write the Python that connects the pieces.

*(Extra explanation, not from the lecture: the table's "ready-made" function names are intentionally generic; the real names appear when the notebook is shown.)*

### Facts from the lecture
- Open-source framework, launched **October 2022** by **Harrison Chase**, who later formed a company around it.
- It is an **abstraction layer**: one way of working with many different models, plus tools to stitch steps into pipelines such as RAG.
- **Version 1.0 was released in October 2025**, a significant overhaul that repackaged much of LangChain. There is a "pre-1.0" and a "post-1.0", and the course uses 1.0. *(Extra, not from the lecture: this means older online tutorials may show code that no longer matches.)*

---

## 4. The Good and the Bad (a likely interview topic)

| | Point | What it means |
|---|---|---|
| Good | **Faster to market** | For assistants, RAG and summarization you glue together existing parts instead of building them |
| Good | **Robust tools out of the box** | Ready-made tools, quick to use |
| Good | **Enterprise adoption** | Took off in 2023; many company projects use it; good resume material; you will meet it often |
| Bad | **Less needed now** | In 2022-23 calling OpenAI, Anthropic and Gemini differed, so unifying them was valuable. Now all providers have **OpenAI-compatible endpoints**, so with the OpenAI Python library you only change the `base_url` (you did this in Week 4, file 51). Tools and prompt templates have also converged into common patterns |
| Bad | **Heavyweight** | Started lightweight, grew a lot: much terminology, many concepts, a real learning curve. It even has its own language (the transcript says "LCL", which I read as LCEL; that is my reading, not the lecture's) that "hasn't really taken off" |
| Bad | **Starting to feel legacy** | Leftovers like `HumanMessage` and `AIMessage` classes, which most people replaced with the plain **list of dicts** from OpenAI. Lighter layers such as **LiteLLM** (file 18) have a tiny learning curve |

The lecturer gave this candid view on purpose. You will form your own opinion this week: "the best of LangChain" (a RAG pipeline in a couple of lines) and "some of the rough edges" (terminology, extra concepts).

### The wider LangChain family
- **LangChain:** the framework in this lecture.
- **LangGraph:** connects agents in a dependency graph (covered in the lecturer's agent course, not here).
- **LangSmith:** an observability platform.
- Other offerings exist too, from the LangChain company.

---

## 5. WHY Learn It At All, If It Has Downsides?

Because the lecturer says it is common in enterprise and good resume material, you will run into it in real projects. Learning it also makes the RAG pipeline quick to build, so you can focus on the ideas (chunks, vectors, search). You do not need to love it to use it.

---

## How to Explain This to Someone

### If a non-technical person asks "What is LangChain?"
"It's a toolbox for building apps on top of AI models. Instead of writing every step yourself (loading documents, searching them, calling the AI), you snap together ready-made parts. It saves time, though it comes with its own vocabulary to learn, and simpler options exist now."

### If a technical person asks
"LangChain is an open-source orchestration and abstraction framework for LLM applications, launched in 2022. It provides loaders, splitters, embedding and vector-store integrations, tools, and model wrappers so you can compose pipelines like RAG quickly. Its value has shrunk since providers converged on OpenAI-compatible APIs and tool and prompt patterns standardised, and it has grown heavy in terminology and learning curve. Lighter layers like LiteLLM cover model switching alone. It remains widely used in enterprise, and v1.0 (Oct 2025) was a major repackaging."

### The analogy
`requests` for LLM jobs: a library of pre-written pieces you snap together, so you don't write the plumbing yourself.

### The one-liner
"LangChain is a Python library of ready-made parts for building LLM apps like RAG: fast to build with, but heavier and less necessary than it used to be."

---

## Self-Check

1. What are the three things you should be able to do by the end of Day 2?
2. Walk through the recap flow from memory, with your code in each step.
3. Why does the toy RAG from Day 1 need replacing?
4. What is LangChain, using the `requests` comparison?
5. Does LangChain change the Day 1 flow? What does it change?
6. Name three advantages and three disadvantages the lecturer gave.
7. Why is LangChain less needed than in 2022-23? (hint: `base_url`)
8. What changed in October 2025?
9. What do LangGraph and LangSmith do?
10. Why learn LangChain even with its downsides?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| LangChain | Open-source Python library of ready-made parts for LLM apps |
| Abstraction layer | A layer giving one common way to use many different models or services |
| Chain / pipeline | Steps joined so one's output feeds the next |
| Harrison Chase | Creator of LangChain (2022); founded a company around it |
| LangChain 1.0 | October 2025 overhaul; the version the course uses |
| OpenAI-compatible endpoint | A provider API that accepts OpenAI-style calls, so only the `base_url` changes |
| LiteLLM | A lightweight abstraction layer (file 18) |
| LangGraph | Connects agents in a dependency graph |
| LangSmith | LangChain's observability platform |
| Chroma | The vector store used in Day 2 |
| Chunk | A piece of a document, made before turning it into a vector (coming in the next videos) |

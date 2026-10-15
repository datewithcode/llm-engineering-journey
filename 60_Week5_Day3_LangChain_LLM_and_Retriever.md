# LLM Engineering – Week 5, Day 3 (Part 1)
## Completing RAG: LangChain's Two Building Blocks (LLM and Retriever) and `.invoke()`

> Personal study notes. Read file 54 (full RAG flow) and files 55 to 59 (Day 2) first.
> Visual companions: "RAG, Step by Step" (Day 1 flow) and "Vector Store, Step by Step" (Day 2) artifacts.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. **Day 2 built half of RAG** (documents to chunks to vectors to Chroma). **Day 3 completes it**: a LangChain RAG pipeline, an expert question answerer, and a **Gradio app that shows the answer and the source documents** it used.
2. LangChain gives two key objects: an **LLM** (wraps a chat model) and a **retriever** (wraps the **encoder + Chroma** together).
3. Both are used the same way: **`.invoke()`**. `retriever.invoke(question)` returns the **relevant chunks** (text); `llm.invoke(messages)` returns the **answer**.
4. Anything you can `.invoke()` is a **runnable** in LangChain. The word is used less in LangChain 1.0, but the idea is the same.
5. LangChain is **not required** for RAG. In Week 8 you'll build it manually, and it's only a few more lines.

---

## 1. Where We Are

| Day | What it did |
|---|---|
| Day 1 | The idea: small idea (paste context) and big idea (vectors) |
| Day 2 | **Phase 1, ahead of time:** documents, chunks (1000 chars, 200 overlap, recursive splitter), vectors (encoder), stored in Chroma |
| **Day 3** | **Phase 2, at question time:** question, retrieve, prompt, LLM, answer (+ show sources) |

### The big idea, one more time (the lecturer's recap)
```
1. Customer asks a question; it arrives at your code
2. A plain SQL/text search would miss important stuff
3. Your code uses an ENCODER (embedding model, not the usual autoregressive LLM)
   to turn the question into a vector
4. A vector database (indexed by the vectors of every chunk) quickly finds
   chunks whose vectors are close to the question's vector
5. Your code puts that relevant context in the prompt
6. The LLM answers
```

### Recap of choices (from Day 2, file 57)
- **Encoders:** OpenAI text-embedding-3-small / -large, Gemini embeddings ("great", not tried in the course), all-MiniLM-L6-v2.
- **Vector stores:** Chroma (used), FAISS, one transcribed as "Kudrin" (*I read it as Qdrant; my reading, not confirmed*), paid ones like Pinecone, and mainstream databases with vector support. Elasticsearch, for example, can **filter at the same time** as finding nearest vectors.
- Store choice = infrastructure (cost, support, performance). Encoder choice = the right kind of vectors for your problem (more on this tomorrow).

---

## 2. WHY LangChain for RAG (and why it isn't required)

- RAG was **one of the first places LangChain really shone**; building a RAG pipeline was so easy that LangChain became very popular. So it makes sense to learn it here.
- But it's **not essential**. Without LangChain it's "just a couple more lines of code." **Week 8** does it the manual way.
- Today's LangChain version: "just a couple of lines of code."

---

## 3. The Two Key Objects

### Object 1: the LLM
You met this in Week 2 (file 18): a LangChain wrapper around a chat model, so OpenAI, Anthropic or Llama can be swapped in and respond the same way.
```python
answer = llm.invoke(messages)    # English in, English answer out
```

### Object 2: the retriever (new)
A **retriever wraps two things together: the encoder and the vector store (Chroma)**. You ask it for documents similar to some text.
```python
docs = retriever.invoke("Who is Avery Lancaster?")
```
What happens inside that one call:
```
question text
   -> encoder turns it into a vector          (hidden inside the retriever)
   -> Chroma finds the nearest chunk vectors  (hidden inside the retriever)
   -> returns those chunks' TEXT (as LangChain Documents) to your code
```

**What you get back:** the relevant chunks' text, ready to paste into the prompt. **Not** vectors, and **not** an answer. The LLM writes the answer in the next step.

*(Extra, my note: the retriever returns LangChain `Document` objects, the same kind as file 56, with `page_content` and `metadata`. The notebook will show this.)*

### Why this matters
These two objects are exactly the two machines from Day 1 (file 54): the retriever does the **search** (encoder + store), the LLM does the **answering**. They are still separate; LangChain just gives each a simple handle.

---

## 4. `.invoke()` and "Runnables"

- Many LangChain objects respond to the **same method, `.invoke()`**: LLMs, retrievers, tools, and many more.
- In LangChain, something you can `.invoke()` is called a **runnable**.
- In the older version, "runnable" was very visible in code and conversation. In **LangChain 1.0** it's less surfaced as a term, but the objects still behave that way.
- Other common methods exist: **`stream`** (results piece by piece) and **`ainvoke`** (async invoke). The course won't use these today.

*(My Python picture:)* like many different Python objects all having a `.read()` method; you don't need to know what's inside, you just call `.read()`.

---

## How to Explain This to Someone

### If a non-technical person asks "How does the system find the right info and answer?"
"There are two helpers. The first, the retriever, searches the company's documents by meaning and pulls out the few passages most related to the question. The second, the language model, reads those passages plus the question and writes the answer. The tool we use, LangChain, gives each helper the same simple 'go' button."

### If a technical person asks
"In LangChain, a RAG pipeline combines a retriever and a chat model. The retriever encapsulates the embedding model and vector store (here Chroma) and returns the top matching chunks as Documents for a text query. The chat model wrapper abstracts the provider. Both implement the runnable interface (`invoke`, plus `stream` and `ainvoke`), which is what makes composition easy. LangChain is convenient but optional; a manual implementation is only marginally longer."

### The analogy
The retriever is the librarian who finds the right pages; the LLM is the expert who reads them and answers. Both start when you say "invoke."

### The one-liner
"A LangChain retriever wraps the encoder and vector store to fetch relevant chunks; the LLM wrapper writes the answer; both are called with `.invoke()`."

---

## Self-Check

1. What did Day 2 build, and what does Day 3 add?
2. What will the Gradio app show besides the answer?
3. What two things does a retriever wrap together?
4. What does `retriever.invoke(question)` return? What does it NOT return?
5. What does `llm.invoke(messages)` return?
6. What is a "runnable"? How has its visibility changed in LangChain 1.0?
7. Name two other runnable methods besides `invoke`.
8. Is LangChain required for RAG? Where will the course do it manually?
9. Which of the two objects does the encoder live inside?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| RAG pipeline | The full question-time flow: retrieve chunks, build prompt, call LLM, answer |
| LLM (LangChain object) | Wrapper around a chat model; swap providers easily |
| Retriever | LangChain object wrapping encoder + vector store; returns relevant chunks for a query |
| `.invoke()` | The common "run this" method on LangChain objects |
| Runnable | Any LangChain object you can `.invoke()` |
| `stream` | Get results piece by piece |
| `ainvoke` | Async version of `invoke` |
| Qdrant (my reading of "Kudrin") | Another vector store |

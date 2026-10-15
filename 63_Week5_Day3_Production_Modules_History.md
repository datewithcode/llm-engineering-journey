# LLM Engineering – Week 5, Day 3 (Part 4)
## From Notebook to Production Modules, Plus Two Fixes: Chat History and the "Combined Question"

> Personal study notes. Read file 62 (RAG in five lines) first.
> Concepts first; code sketches at the end of each section are for reference.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. Notebooks are for experimenting; for production, split the code into **Python modules**. The lecturer puts them in a package folder called **`implementation`**: **`ingest.py`** (Phase 1: build Chroma) and **`answer.py`** (Phase 2: answer questions). **`app.py`** is the Gradio UI.
2. `answer.py` exposes two functions: **`fetch_context(question)`** and **`answer_question(question, history)`**. Any implementation that provides these two can be swapped in, and the same UI keeps working.
3. **Fix 1, history:** the simple version ignored history, so "And what did she do before?" failed (LLMs are stateless). Now history is passed in, converted from OpenAI-style dicts to LangChain message objects with **`convert_to_messages`**.
4. **Fix 2, the combined question:** retrieval used only the latest message, so "what did she do before?" fetched nothing about Avery. Now retrieval searches on **everything the user has said so far, combined**.
5. Retrieval count **k = 5** chunks. The encoder name appears in **both** files: change it in both (same-encoder rule).

---

## 1. WHY Modules: Taking Off the Experimenter's Hat

- The notebook way is good for **experimenting**.
- For **production / engineering**, you put the code into **Python modules**: each file has one job, can be run on its own, and can be called by other code.

### The structure
```
week5/
├── app.py                 <- Gradio chat UI; calls answer.py
└── implementation/        <- a Python package (one swappable implementation)
    ├── ingest.py          <- Phase 1: knowledge base -> chunks -> vectors -> Chroma
    └── answer.py          <- Phase 2: fetch_context() and answer_question()
```

### What each file does

| File | Job | Matches |
|---|---|---|
| `ingest.py` | Read the knowledge base, split into chunks (RecursiveCharacterTextSplitter, 1000 / 200), make embeddings (MiniLM), delete old Chroma if present, build Chroma, print "413 vectors with 384 dimensions" | Day 2 notebook |
| `answer.py` | `fetch_context(question)` returns relevant chunks; `answer_question(question, history)` fetches context and answers | Day 3 notebook |
| `app.py` | Gradio UI that calls `answer.py` | Day 3 Gradio |

### WHY split this way
1. **Ingest runs on its own.** In a real data pipeline it could run automatically **whenever a new file arrives**, or on a schedule (the lecturer's example: a **cron job every hour**), keeping Chroma up to date.
2. **Swappable implementations.** Later this week the lecturer builds a **better** RAG, and he wants you to build your own too. Each implementation just has to provide `fetch_context` and `answer_question`; `app.py` keeps working unchanged. (Like a plug that fits the same socket.)

### Running it
```
cd week5/implementation
uv run ingest.py          # builds Chroma: "413 vectors with 384 dimensions"

cd ..                     # back to week5
uv run app.py             # launches the Gradio UI
```
(New terminal in Cursor: Ctrl + Shift + backtick, or View menu, Terminal.)

### Small details in `answer.py`
- **Encoder appears in two places** (`ingest.py` and `answer.py`). Change it in one, change it in both: the **same-encoder rule** (file 61).
- **k = 5:** number of chunks retrieved and put in the prompt (the default was 4).
- Paths to the database and knowledge base are built in a **platform-independent** way.
- Same system prompt, same vector store, retriever and LLM as the notebook.

```python
# Reference sketch of answer.py's shape (simplified)
RETRIEVAL_K = 5

def fetch_context(question):
    return retriever.invoke(question, k=RETRIEVAL_K)

def answer_question(question, history):
    ...  # see sections 2 and 3
```

---

## 2. Fix 1: Using the Chat History

### The problem
The simple `answer_question` (file 62) **ignored `history`**. So:
```
User: Who is Avery?
Bot:  Avery Lancaster is the CEO...
User: And what did she do before?
Bot:  ??? (doesn't know who "she" is)
```
LLMs are **stateless**: every call is a fresh start unless you send the conversation again. Same lesson as "My name is Ed. Who am I?" from Week 1 (file 09, illusion of memory).

### The fix
Send the whole conversation to the LLM every time: system message + all previous turns + the new question.

### The format wrinkle
- **Gradio** passes history as the **OpenAI-style list of dicts** (`{"role": "user", "content": ...}`).
- **LangChain** wants its own message objects: `SystemMessage`, `HumanMessage`, `AIMessage`.
- LangChain's **`convert_to_messages`** converts the dicts into LangChain message objects.

```python
# Reference sketch
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages

messages = [SystemMessage(content=system_prompt)]
messages += convert_to_messages(history)          # OpenAI dicts -> LangChain messages
messages.append(HumanMessage(content=question))
response = llm.invoke(messages)
```
Tip from the lecturer: add **print statements** to see the before (dicts) and after (LangChain objects).

---

## 3. Fix 2: The "Combined Question" for Retrieval

### The subtle problem
Fix 1 lets the **LLM** see the history. But the **retriever** was still searching using **only the latest message**:
```
User: Who is Avery?               -> retriever searches "Who is Avery?"            -> Avery's chunks. Good.
User: And what did she do before? -> retriever searches "what did she do before?"  -> nothing about Avery!
```
The LLM knows we mean Avery, but the context it receives is irrelevant, because the search text had no "Avery" in it.

### The lecturer's fix
When fetching context, don't search on just the latest message. **Combine everything the user has said so far** into one "combined question" and search on that.
```
combined question = "Who is Avery? And what did she do before?"
   -> retriever finds Avery's chunks again (including her earlier career)
```

### There's no single right answer
Options the lecturer lists:
- search on the **latest message only** (his old approach; fails on follow-ups)
- search on **all the user's messages combined** (his current approach)
- search on **each message separately** and gather all the results

"It really depends on the use case." Older LangChain did this behind the scenes; he likes that it's now **in our hands**.

### A better way exists
He hints there's an even better approach, to be revisited later in the week when looking at more advanced implementations. Puzzle: how could you search using the latest question **plus** just the useful bits of history?
*(Extra, not from the lecture: one common technique is asking an LLM to rewrite the follow-up as a standalone question, e.g. "What did Avery Lancaster do before Insurellm?", then searching on that. Wait for the lecture to confirm what he means.)*

```python
# Reference sketch (shape only)
def combined_question(question, history):
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question

def answer_question(question, history):
    docs = fetch_context(combined_question(question, history))   # search on everything said
    context = "\n\n".join(d.page_content for d in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)] + convert_to_messages(history) + [HumanMessage(content=question)]
    return llm.invoke(messages).content
```
*(Sketches reconstructed from the lecturer's description; the real file may differ in detail.)*

---

## 4. The Two Fixes Side by Side

| | Who it helps | Problem without it | Fix |
|---|---|---|---|
| **History to the LLM** | The **expert** (LLM) | Doesn't know who "she" is | Send all previous turns, converted with `convert_to_messages` |
| **Combined question** | The **librarian** (retriever) | Fetches irrelevant chunks for follow-ups | Search on everything the user has said, not just the last message |

You need **both**: the expert must remember the conversation, and the librarian must fetch the right pages for it.

---

## How to Explain This to Someone

### If a non-technical person asks "How did you make the chatbot production-ready?"
"I split it into two parts: one that reads and indexes the company's documents (it can rerun automatically when files change), and one that answers questions. I also made it remember the conversation, and made its search use the whole conversation, so follow-ups like 'what did she do before?' still find the right information."

### If a technical person asks
"I refactored the notebook into an `implementation` package: `ingest.py` builds the Chroma index (load, split 1000/200, embed with MiniLM, persist) and can run on file-change or cron triggers; `answer.py` exposes `fetch_context` and `answer_question`, so implementations are swappable behind the same Gradio `app.py`. Two fixes: pass conversation history to the LLM (OpenAI dicts converted via `convert_to_messages`), and build the retrieval query from all prior user turns so follow-ups retrieve relevant chunks. k is 5. Query rewriting is a likely next improvement."

### The analogy
The expert needs the conversation notes; the librarian needs the whole question, not just the last sentence.

### The one-liner
"Split ingest and answer into swappable modules, give the LLM the chat history, and search on the whole conversation so follow-up questions still retrieve the right chunks."

---

## Self-Check

1. Why move code from a notebook into modules?
2. What does `ingest.py` do? When might it run automatically?
3. What two functions does `answer.py` expose, and why does that make implementations swappable?
4. Which commands run ingest and the app, and from which folders?
5. Why must the encoder name match in both files?
6. What is k, and what value does `answer.py` use?
7. Why did "And what did she do before?" fail in the simple version?
8. What format does Gradio send history in, and what does `convert_to_messages` do?
9. Even with history sent to the LLM, why could retrieval still fail on a follow-up?
10. What is the "combined question"? Name two other ways to choose the search text.

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| Module | A Python file with a focused job |
| Package | A folder of modules (here `implementation`) |
| `ingest.py` | Builds the vector store (Phase 1) |
| `answer.py` | Answers questions (Phase 2): `fetch_context`, `answer_question` |
| `app.py` | Gradio UI calling `answer.py` |
| Swappable implementation | Any version providing the same two functions works with the same UI |
| Cron job | A scheduled task that runs automatically (e.g. every hour) |
| k | How many chunks the retriever returns (5 here) |
| Stateless | The LLM remembers nothing between calls |
| `convert_to_messages` | Converts OpenAI-style dicts into LangChain message objects |
| `AIMessage` | LangChain's object for an assistant reply |
| Combined question | All the user's messages joined, used as the search text |

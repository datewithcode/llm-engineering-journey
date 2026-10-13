# LLM Engineering – Week 5, Day 2 (Part 2)
## Part A: Loading Documents and Cutting Them into Chunks

> Personal study notes. Read file 54 (full RAG flow) and file 55 (LangChain) first.
> This lecture covers only Part A of the day2 notebook. Parts B (vectors in Chroma) and C (visualizing) come in later videos.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. A **chunk** is just a **slice of a long document**, like `document[0:1000]` in Python. Each chunk gets its own vector, so the search can find the one small piece that answers a question.
2. The whole Insurellm knowledge base is 76 files, about 300,000 characters, almost **64,000 tokens**. It would fit in a context window, but pasting it into every call is costly, and it stops fitting as data grows. **RAG is about scale.**
3. LangChain's loader turns each file into a **`Document`** with two parts: **`page_content`** (the text) and **`metadata`** (facts: `source`, `doc_type`).
4. **`RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`** cuts at natural breaks (blank lines first, then sentence ends). `chunk_size` = roughly how big each chunk is; `chunk_overlap` = how many characters neighbouring chunks share. Result: **76 documents to 413 chunks**.
5. Chunking is **trial and error**. How to judge which chunking works best comes later in the week.

---

## 0. Today's Plan (from the notebook)

| Part | What happens |
|---|---|
| **A** (this lecture) | Divide documents into **chunks** |
| B (later video) | Turn chunks into **vectors** and put them in **Chroma** (an open-source vector database) |
| C (later video) | **Visualize** the vectors |

---

## 1. What a Chunk Is

A chunk is a smaller piece of a long document. Nothing more.

```python
chunk_1 = document[0:1000]
chunk_2 = document[800:1800]
```

Cutting documents into pieces is called **chunking**. LangChain just provides ready-made code to do the cutting.

---

## 2. WHY Cut Documents into Chunks

### The everyday picture
A 300-page employee handbook. Someone asks: "How many sick days do I get?" The answer is one paragraph on page 87.
- **Whole handbook into the prompt:** slow, costly, mostly irrelevant.
- **Cut into small pieces first:** your code finds the one piece about sick days and pastes only that. Short, cheap, on-topic.
*(Handbook example is my illustration.)*

### The lecturer's reason (the vector side)
Each document holds many kinds of information (HR records, product details). A question usually concerns **just one part of one document**. One vector for a whole document is "much less likely" to match a specific question. So each **chunk** gets its own vector, at "just the right granularity" for questions to match.

**Remember:** one text = one vector. A whole document as one vector is a blurry average of everything in it. A chunk's vector is about one thing.

---

## 3. Measuring the Knowledge Base (and WHY RAG Is Still Needed)

```python
files = glob.glob("knowledge-base/**/*.md", recursive=True)
# read them all into one string: entire_knowledge_base

encoding = tiktoken.encoding_for_model("gpt-4.1-nano")
tokens = encoding.encode(entire_knowledge_base)
```

| Measure | Value |
|---|---|
| Files | 76 |
| Characters | about 300,000 |
| Tokens (via `tiktoken`, file 08) | almost 64,000 |

**The surprise:** 64,000 tokens fits in the context window of any major model. You *could* paste the whole thing in.

**Why not:**
1. **Cost on every call.** You pay per token (file 10). The lecturer: like "putting all of Hamlet in every single time."
2. **It doesn't scale.** At 10x or 100x the size, it no longer fits.

**RAG is about scale:** supporting massive knowledge bases while still getting high-quality answers. In **Week 8** the course builds a knowledge base of **400,000 documents**. Insurellm is "medium scale".

**Common mix-up:** this is about the size of the **prompt** on every call, not about training data.

---

## 4. Loading Files with LangChain: the `Document` Object

```python
folders = glob.glob("knowledge-base/*")        # company, contracts, employees, products

documents = []
for folder in folders:
    doc_type = os.path.basename(folder)        # folder name, e.g. "products"
    loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader,
                             loader_kwargs={'encoding': 'utf-8'})
    folder_docs = loader.load()                # read every file in the folder
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type    # our own label
        documents.append(doc)
```

**In plain words:** for each folder, load every markdown file, label each with its folder name, collect them all in a list. Not much more than Day 1, except each file becomes a LangChain **`Document`**.

- `DirectoryLoader` (from `langchain_community`) loads a whole directory.
- The `encoding` setting makes it work on PCs as well as Macs.

### A `Document` has two parts

| Field | Holds |
|---|---|
| `page_content` | The full text of the file |
| `metadata` | A dict of facts: `source` (the file path) and `doc_type` (the label our code added) |

Think of it as a dict with two keys: the text, and facts about the text.

**WHY metadata:** remembers where each text came from and what kind it is. The notebook later uses `doc_type` to colour the dots in the Part C plot. *(My inference from the notebook code: chunks keep this metadata, since the plot reads `doc_type` back from the vector store.)*

---

## 5. Splitting into Chunks: `RecursiveCharacterTextSplitter`

```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
# 76 documents -> 413 chunks
```

### The name, word by word
- **Text splitter:** cuts documents into chunks (LangChain has several, in `langchain_text_splitters`).
- **Character:** sizes are measured in characters.
- **Recursive:** sounds fancy, isn't (the lecturer's words).

### Dumb splitter vs recursive splitter

The simplest one, **`CharacterTextSplitter`**, just chops by character count, even mid-word:
```python
chunks = [document[i:i+1000] for i in range(0, len(document), 1000)]
```

The **recursive** one tries the **nicest break first** and falls back only if needed:
1. Blank lines between sections (a couple of empty lines)
2. A single blank line
3. Ends of sentences, and so on

"Recursive" just means: if a piece is still too big, apply the same trick to that piece. A list of fallbacks.

*(Extra, from my knowledge of the library, not the lecture: the real default order is blank line, new line, space, single character.)*

**WHY:** cuts land at natural breaks, so each chunk makes sense on its own.

### `chunk_size` and `chunk_overlap`

| Setting | Meaning |
|---|---|
| `chunk_size=1000` | Each chunk is roughly up to 1000 characters |
| `chunk_overlap=200` | The **last ~200 characters of one chunk are repeated at the start of the next** |

**WHY overlap:** so an answer isn't chopped in half at a cut. *(My example:)*
```
Without overlap:  chunk A ends "...Sick leave is"   chunk B starts "10 days per year..."
                  -> neither chunk holds the full answer
With overlap:     chunk A ends "...Sick leave is 10 days per year."
                  chunk B starts "Sick leave is 10 days per year. Managers..."
                  -> at least one chunk holds it whole
```
The lecturer: overlap makes it less likely we "chop an answer in half," so a question usually maps nicely to at least one chunk.

### Changing the size

| chunk_size | Chunks from the same 76 documents |
|---|---|
| 1000 | 413 |
| 800 | 532 |

Smaller chunks, more of them. The lecturer looked at `chunks[0]` (a piece of a product summary) and `chunks[100]` (a fragment starting "7. Business continuity") to show they are just fragments.

### It's trial and error
"There's no one rule to get chunking right." You experiment with strategies and see which works best. **How do you measure "works best"?** The lecturer says that is one of the most essential parts of a RAG workflow and will be covered later this week.

---

## 6. The Imports: LangChain Is Heavyweight

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

| Package | For |
|---|---|
| `langchain_openai` | OpenAI classes |
| `langchain_chroma` | The Chroma database |
| `langchain_huggingface` | Hugging Face classes |
| `langchain_community` | Community contributions, including document loaders |
| `langchain_text_splitters` | Splitting documents into chunks |

Each package is installed separately with its own dependencies, and importing them takes a while. Compare **LiteLLM**: one package, any LLM. This is the "heavyweight" point from file 55, seen in practice.

Other setup: `MODEL = "gpt-4.1-nano"` (cheap and fast) and `db_name = "vector_db"` (the vector database, used in Part B).

---

## How to Explain This to Someone

### If a non-technical person asks "What is chunking?"
"Before an AI system can search your documents, it cuts them into small pieces, like tearing a big manual into single pages. When someone asks a question, the system finds the one page that answers it and gives the AI only that page, instead of the whole manual. The pieces overlap slightly so no answer gets cut in half."

### If a technical person asks
"Chunking splits documents into retrieval units sized so each embedding represents a focused piece of content. In LangChain, documents are loaded as `Document` objects (page_content plus metadata) and split with a text splitter such as `RecursiveCharacterTextSplitter`, which prefers natural boundaries (paragraphs, then lines, then sentences) and takes `chunk_size` and `chunk_overlap`. Overlap reduces the chance an answer straddles a boundary. Chunk strategy is empirical and should be evaluated. Even when a corpus fits in context (here ~64k tokens), RAG is used for cost per call and to scale to much larger corpora."

### The analogy
Tearing a manual into overlapping pages so you can hand over just the right page.

### The one-liner
"Chunking cuts documents into small, slightly overlapping slices so each gets its own vector and retrieval can return just the relevant piece."

---

## Self-Check

1. What is a chunk, in Python terms?
2. Why does one vector per whole document match questions poorly?
3. The knowledge base is ~64,000 tokens and fits in a context window. Give two reasons to still use RAG.
4. Is the cost problem about training data or the prompt? Explain.
5. What are the two parts of a LangChain `Document`? What's in `metadata`, and who added `doc_type`?
6. What does `DirectoryLoader` do?
7. How does `RecursiveCharacterTextSplitter` differ from `CharacterTextSplitter`?
8. What does "recursive" mean here?
9. What do `chunk_size` and `chunk_overlap` do? Why overlap?
10. What happened to the chunk count when chunk_size went from 1000 to 800? Why?
11. Why does the import cell show LangChain is heavyweight?
12. How do you know which chunking strategy is best? (Hint: trial and error, measured later this week.)

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| Chunk | A small slice of a document; each gets its own vector |
| Chunking | Cutting documents into chunks |
| `tiktoken` | Library for counting tokens |
| `DirectoryLoader` | LangChain loader that reads every file in a folder |
| `TextLoader` | Loader used per file inside `DirectoryLoader` |
| `Document` | LangChain object with `page_content` and `metadata` |
| `page_content` | The text of a document or chunk |
| `metadata` | Dict of facts about the text (`source`, `doc_type`) |
| Text splitter | LangChain class that cuts documents into chunks |
| `CharacterTextSplitter` | Simplest splitter; cuts by character count only |
| `RecursiveCharacterTextSplitter` | Tries natural breaks first (blank lines, then sentences) |
| `chunk_size` | Roughly the max characters per chunk |
| `chunk_overlap` | Characters repeated between neighbouring chunks |
| `split_documents` | The method that turns a list of Documents into chunks |
| Chroma | Open-source vector database used in Part B |

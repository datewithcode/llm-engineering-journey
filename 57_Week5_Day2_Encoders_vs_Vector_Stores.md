# LLM Engineering – Week 5, Day 2 (Part 3)
## Encoders vs Vector Databases: Two Separate Jobs, and Which One to Care About

> Personal study notes. Read file 56 (chunking) first. This lecture sits between Part A and Part B of the day2 notebook.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. **Two separate things:** the **encoder** (embedding model) **makes** the vector. The **vector database** (e.g. Chroma) **stores** vectors and **finds the closest ones fast**. The database never creates vectors.
2. The code blurs this because you hand the encoder to Chroma in one line, so it *looks* like Chroma makes vectors. It doesn't.
3. For each chunk, the vector store keeps the **chunk text**, its **vector**, and its **metadata**.
4. **Spend your energy on the encoder.** Different embedding models perform very differently per use case, so you test them. That decides which chunks count as relevant.
5. **The database is an infrastructure choice** like any database: cost, performance, scaling, resiliency, backups, security. Mainstream databases (Postgres, MongoDB, Elasticsearch) now support vectors natively.

---

## 1. Recap of Part A (from the lecture)

Documents were loaded and split into chunks with the `RecursiveCharacterTextSplitter` (tries double empty lines, then single, then spaces), about 1000 characters each with 200-character overlap, to divide documents into fragments "likely to map to questions." Full detail: file 56.

---

## 2. The Key Idea: Who Makes the Vector vs Who Stores It

| | Encoder (embedding model) | Vector database (e.g. Chroma) |
|---|---|---|
| Job | **Makes** the vector: text in, numbers out | **Stores** vectors, **finds closest** ones fast |
| Is it an LLM? | Yes, the autoencoding kind (file 53) | No, it's a database |
| Creates vectors? | **Yes** | **No, never** |

*(My plain-Python sketch, not real code:)*
```python
vector = encoder("Avery Lancaster is the CEO")    # ENCODER makes the numbers
database.save(text, vector)                        # DATABASE keeps them
database.find_closest(question_vector)             # ...and searches them fast
```

**A vector database** is a database built for one kind of query: not SQL, but "which stored vector is **closest** to this one?" Quick vector-based retrieval is its whole point.

### Why people mix them up
In the notebook (Part B) both appear together:
```python
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")                 # the encoder
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, ...)   # the database
```
You pass the encoder into Chroma, so it looks like Chroma makes the vectors. Really, Chroma calls the encoder you gave it, then stores the result. The lecturer: the vector database "is where they get stored, but it's not where they're created."

### What the store holds per chunk
- the chunk's **text** (Chroma calls it the "document")
- its **vector**
- its **metadata** (`source`, `doc_type`)

The notebook's Part C reads all three back:
```python
result = collection.get(include=['embeddings', 'documents', 'metadatas'])
```
Same (text, vector) pair as Day 1 (file 54), plus metadata.

---

## 3. Popular Encoders (embedding models)

| Encoder | Notes from the lecture |
|---|---|
| **word2vec** | Where it began; word to vector; the king - man + woman = queen example (file 53). Historical, not used for this |
| **BERT** | Google's 2018 transformer encoder; powerful; still somewhat used |
| **text-embedding-3-small / -large** | OpenAI; the course will likely use both at some point |
| **Gemini Embedding 001** | Google's embedding model; very popular |
| **all-MiniLM-L6-v2** | Open source, in Hugging Face's **sentence-transformers** package; "very popular indeed," the one you'll meet most |

---

## 4. Popular Vector Stores

| Store | Notes from the lecture |
|---|---|
| **Chroma** | Open source, free, easy; used in this course |
| **FAISS** | Meta ("Facebook AI Similarity Search"). Very popular, but **not really a database**: in-memory vector search only |
| **Pinecone** and "Alleviate" | Paid, managed, more powerful, scale for enterprise. *(Transcript says "Alleviate"; I read it as Weaviate. That is my reading, not confirmed by the lecture.)* |
| **Postgres** (relational), **MongoDB** (NoSQL / document), **Elasticsearch** (search platform) | Mainstream databases that now support vectors natively |

**The trend:** pure vector databases like Pinecone are "less common in recent years," because mainstream databases support vectors natively, so there's less need for a separate one.

**Real-world scale:** at the lecturer's company (Nebula), Elasticsearch holds about **200 million vectors** and does filtered similarity search in **a couple of seconds**.

---

## 5. WHY the Encoder Matters More Than the Database

People often ask "which vector database is best?" The lecturer's answer: that's usually the wrong worry.

| Choice | What it affects | How to decide |
|---|---|---|
| **Encoder** | **Which chunks count as similar**, so which context the LLM gets, so answer quality | Test and experiment for your business problem (this week) |
| **Database** | Cost, performance, scale, resiliency, backups, security | A normal infrastructure trade-off; works with any encoder |

*(My picture:)* the encoder is the brain that decides what "similar" means; the database is the filing cabinet. A better cabinet doesn't make the brain smarter.

**Exceptions exist:** some high-end platforms offer special similarity searches or performance tricks (e.g. searching only certain regions of space), so there's "some overlap," but it's "relatively light most of the time."

---

## How to Explain This to Someone

### If a non-technical person asks "What's a vector database?"
"It's a database that stores pieces of text as lists of numbers that capture their meaning, and it's very fast at finding the pieces closest in meaning to a question. It doesn't create those numbers. A separate AI model does that. Choosing that model well matters much more than choosing the database."

### If a technical person asks
"In RAG, the embedding model (encoder) produces the vectors and the vector store persists them and serves nearest-neighbour queries. Frameworks like LangChain couple them (`Chroma.from_documents(..., embedding=...)`) but they're independent. Retrieval quality is driven mainly by the embedding model, which needs empirical evaluation per use case. Store choice (Chroma, FAISS, Pinecone, or native vector support in Postgres, MongoDB, Elasticsearch) is mostly an infrastructure decision about cost, latency, scale and operations."

### The analogy
The encoder is the brain that decides what "similar" means; the vector store is the fast filing cabinet.

### The one-liner
"The encoder makes the vectors and decides relevance; the vector database just stores and searches them, so pick the encoder carefully and the database like any other database."

---

## Self-Check

1. What does the encoder do? What does the vector database do?
2. Does Chroma create vectors? Why does the code make it look like it does?
3. What kind of query is a vector database built for?
4. What three things does the store keep for each chunk?
5. Name four encoders and who makes each.
6. Why is FAISS "not really a database"?
7. Why are pure vector databases like Pinecone less common recently?
8. Which choice deserves most of an AI engineer's energy, and why?
9. What factors decide the database choice?
10. What did the lecturer's company do with Elasticsearch?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| Encoder / embedding model | Model that turns text into a vector |
| Vector database / vector store | Database that stores vectors and quickly finds the closest ones |
| Vector-based retrieval | Fetching the stored items whose vectors are closest to a query vector |
| sentence-transformers | Hugging Face package of open-source encoders (includes all-MiniLM-L6-v2) |
| Gemini Embedding 001 | Google's embedding model |
| Chroma | Free, open-source vector store used in the course |
| FAISS | Meta's in-memory vector search library |
| Pinecone | Paid, managed vector database |
| Native vector support | Mainstream databases (Postgres, MongoDB, Elasticsearch) storing and searching vectors themselves |

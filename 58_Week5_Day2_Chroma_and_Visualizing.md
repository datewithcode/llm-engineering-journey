# LLM Engineering – Week 5, Day 2 (Part 4)
## Part B and C: Building the Chroma Vector Store, and Seeing the Vectors

> Personal study notes. Read file 56 (chunking) and file 57 (encoder vs vector database) first.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. One line builds the vector database: `Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="vector_db")`. For each of the 413 chunks, the **encoder** (all-MiniLM-L6-v2) makes the vector and **Chroma** stores text + vector + metadata.
2. It creates **one** database (a `vector_db` folder, with **SQLite** behind it): one entry per chunk, not one database per chunk.
3. Result: **413 vectors x 384 dimensions**. **413 comes from chunking**; **384 comes from the encoder** (Chroma accepts any size).
4. Humans can't see 384 dimensions, so **t-SNE** squashes them to 2D while keeping close things close. The **axes mean nothing**; only closeness matters.
5. The encoder saw **only the chunk text**, never the doc type, yet chunks **grouped by type** (employees together, etc.). Proof the vectors capture meaning.

---

## 1. Part B: Building the Vector Store

```python
# 1. Pick the encoder (makes the vectors)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. If an old database exists, wipe it so we start fresh
if os.path.exists(db_name):
    Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

# 3. Build: for every chunk, make its vector and store it
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
```

| Line | What it does |
|---|---|
| 1 | Names the encoder: free, open-source **all-MiniLM-L6-v2** from Hugging Face (a LangChain `HuggingFaceEmbeddings` object). Nothing runs yet |
| 2 | Housekeeping: if `vector_db` already exists, delete its contents. Lets you rerun the cell without duplicates |
| 3 | The real work. Loops over all 413 chunks: **encoder** makes each vector, **Chroma** stores chunk text + vector + metadata |

### What you pass to `Chroma.from_documents`

| Argument | What it is |
|---|---|
| `documents=chunks` | The 413 chunks from Part A |
| `embedding=embeddings` | The encoder |
| `persist_directory=db_name` | Folder to save the database in (`vector_db`) |

### The picture: ONE database, one entry per chunk
```
vector_db  (one database, SQLite behind it)
   ├── chunk 1 text   + vector (384 numbers) + metadata
   ├── chunk 2 text   + vector               + metadata
   ├── ...
   └── chunk 413 text + vector               + metadata
```

- **Chroma** is free and open source, with **SQLite** running behind it. It's created on your computer with no extra setup.
- The `vector_db` folder fills with SQLite files: "your very first vector data store."
- **Reminder (file 57):** you pass the encoder into Chroma, but they're separate. "It could be any embedding model we could pass in there."

### Hugging Face login note
You shouldn't need a Hugging Face login for this model. If you get a login error, add your `HF_TOKEN` (from Week 3) to `.env` and rerun `load_dotenv(override=True)`. You'll need it in Week 8 anyway.

---

## 2. Looking Inside: 413 x 384

```python
collection = vectorstore._collection
count = collection.count()
sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
dimensions = len(sample_embedding)
# "There are 413 vectors with 384 dimensions in the vector store"
```

- **Collection** is roughly Chroma's word for a **table** in a relational database. There's one collection here.

| Number | Comes from | Changes if you... |
|---|---|---|
| **413** | **Chunking** (the splitter) | change `chunk_size` (800 gave 532) |
| **384** | **The encoder** (all-MiniLM-L6-v2 always outputs 384 numbers) | change the encoder |

**Common mistake:** thinking 413 comes from the encoder. It doesn't; it's the chunk count. And 384 is not a Chroma feature: "Chroma can take vectors of any size."

---

## 3. Part C: Visualizing the Vectors

### WHY visualize
The lecturer is "a big believer" in visualizing data. It helps you:
- spot **outliers** and interesting or problematic **trends**
- build a real intuition for what "data represented by vectors" means

### The problem and the fix
We can't see 384 dimensions. Techniques like **PCA** and **t-SNE** (t-distributed stochastic neighbor embedding; you don't need to remember the name) project high-dimensional data down to 2D so that **things close in 2D are likely close in 384D**, and far apart stays far apart.

```python
# Prework: pull everything back out of Chroma
result = collection.get(include=['embeddings', 'documents', 'metadatas'])
vectors = np.array(result['embeddings'])
documents = result['documents']
doc_types = [m['doc_type'] for m in result['metadatas']]
# colour per type: products blue, employees green, contracts red, company orange

tsne = TSNE(n_components=2, random_state=42)   # squash to 2 dimensions
reduced_vectors = tsne.fit_transform(vectors)  # 413 x 384  ->  413 x 2
# then plot with plotly: one dot per chunk, hover shows type + first 100 chars of text
```

- `random_state=42` makes it give the same picture each run.
- The notebook also has a 3D version (`n_components=3`, `Scatter3d`).
- You may see a Hugging Face warning about threads. Ignore it; warnings with open-source software are common. Note them down in case something goes wrong later.

### How to read the plot
- **The x and y axes have no meaning.** It's just how the data is spread out.
- **Only closeness matters:** nearby dots = chunks with similar meaning.
- Hover over a dot to see its doc type and chunk text.

### The surprising result
The encoder was given **only the chunk text**. It was never told which chunks were employees, products, contracts or company. Yet:
- **employee chunks mostly cluster together**
- some company chunks that are employee-related sit near them
- a **stripe of product chunks** sits between sections of contracts
- contract chunks on similar topics (e.g. integration services) sit near each other

The colours (doc_type, from metadata) were added only for the picture. The **grouping came purely from meaning**. That's Day 1's "close together = similar meaning," on real data.

**Final reminder from the lecturer:** the vectors are **stored** in Chroma, but they were **made** by the Hugging Face all-MiniLM-L6-v2 model.

---

## How to Explain This to Someone

### If a non-technical person asks "What did you build?"
"I took a company's documents, cut them into 413 small pieces, and used an AI model to turn each piece into a list of 384 numbers that capture its meaning. I saved those in a small database. When I plotted them, pieces about similar things landed near each other on their own: all the employee records grouped together, for instance, even though the model was never told which was which."

### If a technical person asks
"Using LangChain, I embedded 413 chunks with all-MiniLM-L6-v2 (384-dim) via `HuggingFaceEmbeddings` and persisted them in a local Chroma store (SQLite-backed) with `Chroma.from_documents`. The collection holds text, embedding and metadata per chunk. I then pulled the embeddings back, reduced them to 2D/3D with t-SNE, and plotted them coloured by doc_type metadata. Clusters aligned with document type despite the encoder only seeing raw text, a quick sanity check that the embeddings separate content semantically."

### The analogy
413 index cards, each with a 384-number "meaning fingerprint," filed in one cabinet. Squash the fingerprints onto a flat map and similar cards end up as neighbours.

### The one-liner
"Each chunk became a 384-number vector stored in Chroma; flattening them to 2D shows similar content clustering by meaning alone."

---

## Self-Check

1. What three things do you pass to `Chroma.from_documents`?
2. Who makes the vectors and who stores them in that line?
3. Does it create one database or one per chunk?
4. What runs behind Chroma, and where is the database saved?
5. Why does the cell wipe an existing `vector_db` first?
6. What is a "collection"?
7. Where does 413 come from? Where does 384 come from?
8. What would change each number?
9. Why do we need t-SNE? What does it preserve?
10. What do the x and y axes mean on the t-SNE plot?
11. What does `random_state=42` do?
12. Why is it surprising that the chunks grouped by doc type?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| `HuggingFaceEmbeddings` | LangChain wrapper for a Hugging Face encoder |
| all-MiniLM-L6-v2 | Free open-source encoder; outputs 384-number vectors |
| `Chroma.from_documents` | Builds a Chroma store: embeds each chunk and saves it |
| `persist_directory` | Folder where the Chroma database is saved |
| `delete_collection` | Wipes an existing collection so you start fresh |
| SQLite | Small file-based database running behind Chroma |
| Collection | Chroma's equivalent of a table |
| Dimensions | How many numbers are in each vector (384 here) |
| t-SNE | Technique to squash high-dimensional vectors to 2D/3D, keeping neighbours close |
| PCA | Another dimension-reduction technique |
| `random_state` | Fixes randomness so results repeat |
| Outlier | A point far from where you'd expect it |

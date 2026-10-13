# LLM Engineering – Week 5, Day 2 (Part 5)
## 3D View, and Swapping Encoders: Proof That the Encoder Decides Quality

> Personal study notes. Read file 57 (encoder vs vector database) and file 58 (Chroma and t-SNE) first.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. t-SNE can squash vectors to **3D** (`n_components=3`). Messy at first, but you can **rotate and zoom** and see separation you miss in 2D.
2. The lecturer changed **only the encoder** and reran on the **same 413 chunks**: all-MiniLM-L6-v2 (**384** dims), OpenAI text-embedding-3-small (**1,536**), text-embedding-3-large (**3,072**).
3. **Each step up separated the document types more cleanly**; large gave four clean blobs in 3D. Same data, same Chroma, different encoder, completely different picture.
4. A large model is better mainly because it's a **more advanced transformer that captures meaning better**, not simply because it has more dimensions (they often go together).
5. **Next (Day 3):** build a full RAG pipeline with LangChain and a Gradio chatbot that shows the answer **and the source chunks** it used.

---

## 1. The 3D View

```python
tsne = TSNE(n_components=3, random_state=42)    # 3 instead of 2
reduced_vectors = tsne.fit_transform(vectors)
# plotted with go.Scatter3d: hover, rotate, zoom
```

- First impression: "a bit of a mess." 2D is easier to look at.
- But rotating and zooming shows groups that looked mixed in 2D are actually separate (e.g. one colour that seemed close to another is "distributed differently").
- **Proper use:** spot anomalies and mistakes in how documents are grouped, and get clues about whether a different encoder would do better. Also: fun, and builds intuition.
- Reminder: we're viewing vectors **as stored in Chroma**, but they were **made** by the encoder (all-MiniLM-L6-v2, from Hugging Face sentence-transformers).

---

## 2. The Experiment: Same Chunks, Three Encoders

Only one line changed each time:
```python
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")    # run 1
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")        # run 2
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")        # run 3
```
Each run wipes the old database and rebuilds it with the same 413 chunks (file 58).

| Encoder | Dimensions | Cost | What the plot showed |
|---|---|---|---|
| all-MiniLM-L6-v2 (Hugging Face) | 384 | Free, open source | Some grouping by type, fairly mixed |
| text-embedding-3-small (OpenAI) | 1,536 | Paid but "very, very cheap" | Much better separation: employees in one area, contracts in another, company in one strip, products elsewhere |
| text-embedding-3-large (OpenAI) | 3,072 | Paid | Even stronger separation; in 3D, "four blobs" cleanly separated |

**This is file 57's lesson made visible:** the encoder decides where points land, so it decides which chunks count as similar. Chroma didn't change at all.

### How to read the differences correctly
- **The picture rotating between runs means nothing.** The axes have no meaning; only how separated the groups are matters.
- **Some overlap is correct, not a mistake:**
  - Product chunks about **features** sit beside contract chunks about features, because contracts contain product information.
  - A couple of employee chunks sat with the company group: they are the parts of an employee record about the company as a whole (in the large-model plot, both contained the company name).
- Remember the colours come from metadata; the encoder never saw them (file 58).

---

## 3. Is "Bigger Vector" the Reason It's Better?

**Not exactly.** The lecturer warns against this tempting idea.

- What really matters: the large model is a **more advanced transformer, better at capturing the meaning** of text.
- More dimensions give it **more room ("degrees of freedom") to express** that meaning.
- So bigger models **often** produce bigger vectors, and the two are "somewhat related," but more dimensions alone is not the cause, and it doesn't have to be the case.

### The picture that makes it click *(my illustration)*
Two people describe a house:
- A: 50 words, "nice house, good house, big-ish, nice nice..."
- B: 20 words, "3-bed, near metro, south-facing, renovated 2024, quiet street."

B uses fewer words but describes it better, because B understands what matters. **Dimensions = how many words you're allowed. Quality = how well the model understands.**

---

## 4. The Lecturer's Homework

- **Experiment with different encoders:** other open-source ones, or Gemini's if you have an account. Look at the visualizations each time.
- Find points close together and **check their chunk text really is similar**.
- Build intuition for how different encoders represent information.

---

## 5. Day 2 Recap and What's Next

**After Day 2 you can explain** how RAG works: documents become chunks, chunks become vectors (via an encoder), vectors go into a vector store (Chroma, now running on your computer). The lecturer: vectors act like "the index into the data."

**Next time (Day 3):**
- Use LangChain to build a full RAG pipeline ("super easy").
- Deliver a RAG-based expert question answerer.
- A **Gradio** chatbot that shows not only answers but also **the documents (chunks) used** to answer: the relevant context surfaced by the pipeline.

Progress: the lecturer says you're **55% of the way** to being an LLM engineer.

---

## How to Explain This to Someone

### If a non-technical person asks "Does the choice of AI model for search matter?"
"A lot. We took the exact same 413 pieces of company text and let three different models place them on a map by meaning. The cheap free model mixed things up a bit; OpenAI's larger model neatly separated employee records, contracts, products and company info. Better understanding means the system finds the right pieces when someone asks a question."

### If a technical person asks
"Holding the chunks and vector store constant, I swapped embedding models: all-MiniLM-L6-v2 (384-d), text-embedding-3-small (1536-d) and text-embedding-3-large (3072-d). t-SNE projections showed progressively cleaner semantic separation by doc_type, with expected overlap where content genuinely overlaps (product features in contracts). Gains come mainly from a stronger encoder's representation quality; higher dimensionality gives capacity but isn't itself the cause. It's a cheap, visual sanity check before formal retrieval evaluation."

### The analogy
Same pile of index cards, three different librarians sorting them by topic. The expert librarian makes the cleanest piles.

### The one-liner
"Swapping only the encoder reshaped the whole vector space; a stronger encoder separates meaning better, which is why the encoder choice matters most."

---

## Self-Check

1. How do you make a 3D t-SNE plot? Why bother when 2D is easier?
2. What was the one thing changed between the three runs? What stayed the same?
3. Give the dimensions of each of the three encoders.
4. Describe how separation changed from run to run.
5. The plot rotated between runs. Does that matter? Why not?
6. Why do some product chunks sit near contract chunks? Is that a mistake?
7. Is the large model better because its vectors are longer? Explain.
8. What does this experiment prove about encoder vs vector store?
9. What will Day 3 build?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| `n_components=3` | Tells t-SNE to squash to 3D instead of 2D |
| `go.Scatter3d` | Plotly's 3D scatter plot (rotate and zoom) |
| `OpenAIEmbeddings` | LangChain wrapper for OpenAI's embedding models |
| text-embedding-3-small | OpenAI encoder, 1,536 dimensions, very cheap |
| text-embedding-3-large | OpenAI encoder, 3,072 dimensions, best separation here |
| Separation | How cleanly different kinds of content form their own groups |
| Degrees of freedom | Room to express meaning; more dimensions give more |
| Anomaly | A point grouped in a surprising place, worth checking |

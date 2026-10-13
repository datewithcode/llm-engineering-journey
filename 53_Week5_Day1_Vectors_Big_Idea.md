# LLM Engineering – Week 5, Day 1 (Part 2)
## The Big Idea Behind RAG: Vectors and Embedding Models

> Personal study notes. This is the idea that fixes the toy RAG's weaknesses (file 52).
> Read file 52 first. The "meaning map" picture below is the version that clicked.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. There are **two kinds of LLM**. The kind you've used so far is **autoregressive** (predicts the next token). The new kind is an **autoencoding LLM**, also called an **encoder** or **embedding model**: it reads a whole input and produces **one output representing all of it**.
2. That output, a list of numbers, is a **vector** (a point in space). Text with similar **meaning** gets similar numbers, so it lands **close together** on a "meaning map."
3. **Tokens are inputs, vectors are outputs.** Text becomes token IDs (simple lookup), the model processes them, and a vector comes out.
4. **WHY this matters for RAG:** instead of matching exact words (the toy version), you turn the question and every document into vectors and fetch the documents **closest in meaning**. "Who runs the company?" can find Avery Lancaster's file with zero words in common.

5. "Numbers represent meaning" shows up in two ways: (a) **close together = similar meaning** (this is what RAG uses), and (b) **word2vec arithmetic**, king - man + woman lands nearest to **queen** (a bonus proof that the numbers really capture meaning).

---

## 1. The Picture That Makes It Click: The Meaning Map

Remember the 2D animal map from file 43? Dog and cat sit close together because their meanings are similar.

Do the same with **whole sentences**. *(Illustration only: I placed these by hand to show the idea.)*

```
   |   "Avery Lancaster is the CEO"
   |        "Who runs the company?"          ← these two sit CLOSE
   |
   |   "CarLLM is a car insurance product"
   |        "Tell me about auto coverage"    ← these two sit CLOSE
   |
   |   "What's the weather today?"           ← far from everything else
```

"Who runs the company?" and "Avery Lancaster is the CEO" share **no words**, yet they sit close because their **meanings** are related.

**An embedding model is the machine that places text on this map.** You give it text; it gives back the coordinates (a list of numbers). It doesn't generate text or answer questions. Text in, coordinates out.

---

## 2. Two Kinds of LLM

| | Autoregressive LLM (what you've used) | Autoencoding LLM (new) |
|---|---|---|
| Other names | The ordinary "LLM" (GPT, Claude, Gemini, DeepSeek, Grok, Llama) | **Encoder**, **embedding model**, vector embedding model |
| Input | A sequence of tokens | A sequence of tokens |
| Output | **The next token**; feed it back in; repeat | **One output reflecting the whole input** |
| Job | Writing text | Capturing what an entire input *means* |
| Trained by | Lots of (input sequence → next token) examples | Trained to produce a useful whole-input output |

If someone says "LLM" with no extra framing, they almost certainly mean the autoregressive kind. You met "autoregressive" in file 42: the model feeds its own output back in.

### What encoders are used for
- **Classification**: one output for the whole input. Example: **sentiment analysis** (is this review positive or negative?). You ran this as a pipeline in week 3 (file 34b).
- **Vector embeddings**: turn a whole piece of text into a list of numbers capturing its meaning. **This is the one RAG needs.**

---

## 3. What a Vector Is

A **vector** is a list of numbers, read as the **coordinates of a point in space**.

| Numbers in the list | What it is |
|---|---|
| 2 | A point on a flat map: (x, y) |
| 3 | A point in a room: (x, y, z) |
| 10 | A point in 10-dimensional space. Same idea; just impossible to draw. |

"10-dimensional space" sounds fancy. It only means **ten numbers used as coordinates**.

When you turn a sequence of tokens into such a list of numbers, the result is a **vector embedding**:

```
"Avery Lancaster is the CEO of Insurellm"   →   [0.12, -0.83, 0.45, ...]
```

The numbers are meant to reflect the **meaning** of the text. Similar meanings give nearby points. That's the whole basis of "fuzzy lookup."

*(Extra, not from the lecture: real embedding vectors are much longer than 10 numbers. For example, `all-MiniLM-L6-v2` produces 384 numbers per text, and OpenAI's `text-embedding-3-large` produces 3,072 by default.)*

---

## 3b. What "Numbers Represent Meaning" Really Means (two ways)

The lecture shows this in two different ways. Keep them separate.

### Way 1: Close together means similar meaning (the one RAG uses)

Take three texts:

- **A:** "What are ticket prices to travel from New York to London?"
- **B:** "What's the price of a flight from JFK to Heathrow Airport?"
- **C:** "What is the best recipe for banana bread?"

Turn each into a vector with an embedding model. **A and B land close together. C lands far away.** A and B share almost no exact words (JFK vs New York, Heathrow vs London), yet they mean nearly the same thing.

This is a **trained property**, not a coincidence. The model was trained so that similar meanings get similar numbers.

**WHY it matters for RAG:** this is exactly how "Who runs the company?" finds Avery Lancaster's file. Question and document sit close on the meaning map, so the page-flipper fetches that page.

**What can become a vector?** Almost anything: a character, a token, a word, a sentence, a paragraph, a whole document, and even abstract things (the lecturer's example: job postings and careers). In RAG we will mostly use **chunks of documents**.

**Real vectors are long:** hundreds or thousands of numbers (dimensions), not 2 or 3.

### Way 2: word2vec arithmetic (a bonus proof, not needed for RAG)

An early model called **word2vec** gave each word a vector. People noticed you could do arithmetic on the vectors:

```
king - man + woman = point X
nearest known word to X = queen
```

Another example: **Paris - France + England = London**.

It is **two steps**:

1. Do the arithmetic on the vectors. The result is a new point X (it is not a word yet).
2. Find the **nearest known word** to X. That word is "queen".

*(Illustration only, my own toy example: imagine just two axes, "royal" and "male". king = (royal, male), man = (not royal, male), woman = (not royal, not male). Take king, remove "male", add "not male", keep "royal". You land where a royal, non-male word sits: queen.)*

**Why the lecturer shows it:** it is evidence that the numbers capture real meaning, including relationships. You do not need it to build RAG.

### Cosine similarity (named only)

The real way "closeness" is measured is called **cosine similarity**. The lecturer names it as a technicality to revisit later. *(Extra, not from the lecture: it compares the direction two vectors point in, rather than the distance between them.)*

---

## 4. Real Embedding Models You'll Meet

| Model | Made by | Notes |
|---|---|---|
| **BERT** | Google, 2018 | Bidirectional Encoder Representations from Transformers. Early, popular, still used. The lecturer says it predates GPT; strictly, the first GPT appeared a few months earlier in 2018, but BERT long predates the term "LLM" becoming common. |
| **text-embedding-3-large** and **-small** | OpenAI | Paid API. The lecturer uses **-large**. |
| **all-MiniLM-L6-v2** | Open source | Free; the course experiments with it. |

---

## 5. Tokens vs Vectors (the common confusion)

| | Tokens | Vectors |
|---|---|---|
| Role | **Input** | **Output** |
| What they are | Text turned into ID numbers | Numbers capturing **meaning** |
| Made by | The tokenizer: a simple lookup, no understanding | The model, after it has processed the tokens |
| Example | `"cat sat"` → `[9246, 7731]` | → `[0.12, -0.83, 0.45, ...]` |

**WHY tokens exist at all:** a model only adds and multiplies, so it can't take a word. Each word fragment is first mapped to a number (file 43). Trying whole words or single letters both ran into problems (file 07), so fragments won.

**The flow:**
```
text → tokenizer → token IDs → embedding model → ONE vector (meaning)
```

Even embedding models take **tokens** in. Tokens are the text in number form. The vector is what comes out once the model has understood it.

### The naming trap: "embedding" has two related meanings

| | File 43 (inside the model) | This lecture (RAG) |
|---|---|---|
| What gets a vector | **Each token** | **A whole piece of text** |
| Where it lives | Inside every LLM, between layers | The **output** of an embedding model |
| Example | "cat" → 2,048 numbers | "Avery is the CEO..." → one list of numbers |

Same core idea (numbers that represent meaning), different scope. The lecturer calls the inside-the-model kind a "pro" detail you don't need to worry about. **For RAG, what matters is one vector per piece of text.**

---

## 6. WHY This Fixes the Toy RAG

```
User asks: "Who runs the company?"
      ↓
YOUR CODE sends the question to the embedding model
      ↓
Embedding model returns coordinates, e.g. [0.82, 0.13, ...]
      ↓
YOUR CODE compares those coordinates against every document's coordinates
      ↓
"Avery Lancaster is the CEO" has the CLOSEST coordinates
      ↓
YOUR CODE puts that document in the prompt
      ↓
LLM answers: "Avery Lancaster is the CEO of Insurellm"
```

| | Toy RAG (file 52) | Real RAG (coming next) |
|---|---|---|
| How it finds pages | Exact word match: `"lancaster"` equals `"lancaster"` | **Meaning match**: "who runs the company" is near "CEO" |
| Fails when | Words don't match ("Who is Avery?", a typo, a description) | Rarely, since meaning is compared, not spelling |
| What does the matching | A Python dictionary lookup | An **embedding model** placing text on a meaning map |
| Wrong-match risk | "Alex Lancaster" fetches Avery's file | Still possible, but the match is by meaning, not just one shared word |

**Open-book exam picture:** the page-flipper used to scan the index for exact words. Now it uses a meaning map, and opens the pages whose meaning sits closest to the question.

*(What's still to come in the course: how the vectors are stored, how "closest" is measured in detail (cosine similarity was only named), and how documents are split into pieces. Not covered in this lecture, so not filed here.)*

---

## 7. How to Explain This to Someone

### If a non-technical person asks "What's a vector embedding?"

"It's a way to turn a sentence into a point on a map, where sentences with similar meaning land near each other. 'Who runs the company?' and 'Avery is the CEO' end up as neighbours even though they share no words. That lets a computer search by meaning instead of by exact spelling."

### If a technical person asks

"An embedding model is an encoder (autoencoding) transformer: it consumes a full token sequence and emits a single dense vector representing the whole input, rather than predicting the next token as an autoregressive decoder does. Semantically similar texts map to nearby points, enabling similarity-based retrieval. For RAG, you embed the query and the documents with the same model and retrieve the nearest documents. Examples: BERT, OpenAI text-embedding-3-large/small, all-MiniLM-L6-v2. Note the distinction from the per-token embeddings inside a decoder LLM. Embeddings capture relationships well enough for vector arithmetic (word2vec: king - man + woman is nearest to queen), and closeness is typically measured with cosine similarity."

### The analogy

A meaning map: the embedding model places any text on a map so that similar meanings sit close together. Finding relevant documents becomes "which points are nearest to my question?"

### The one-liner

"An embedding model turns text into a point on a meaning map, so RAG can find documents by meaning instead of exact words."

---

## 8. Self-Check

1. What are the two kinds of LLM? What does each output?
2. What other names does an autoencoding LLM go by?
3. What is a vector? What does "10-dimensional space" literally mean?
4. Why do "Who runs the company?" and "Avery Lancaster is the CEO" end up close together?
5. Name three embedding models and who made each.
6. "Tokens are inputs, vectors are outputs." Explain.
7. Do embedding models take tokens or text? (Trick question: what happens first?)
8. The word "embedding" appears in file 43 and here. How do the two meanings differ?
9. What does the embedding model do in RAG, and what does it NOT do?
10. How does this fix the toy RAG's "Who is Avery?" miss?
11. Texts A (NY to London ticket prices) and B (JFK to Heathrow flight price) share few words. Why do they still land close together, and why does C (banana bread) land far?
12. Walk through "king - man + woman" in two steps. What is the result of step 1, and what does step 2 do?
13. Is the king/queen trick needed to build RAG? What is it for?
14. What is cosine similarity, in one line?

---

## 9. Quick Glossary

| Term | Plain meaning |
|---|---|
| Autoregressive LLM | Predicts the next token, feeds it back in, repeats (GPT, Claude, Llama) |
| Autoencoding LLM / encoder | Reads a whole input, produces one output representing all of it |
| Embedding model | An encoder used to turn text into a vector |
| Vector | A list of numbers read as coordinates of a point in space |
| Vector embedding | The vector an embedding model produces for a piece of text |
| Dimension | One number in the vector (a 10-number vector is "10-dimensional") |
| Meaning map | The mental picture: similar meanings sit close together |
| BERT | Google's early (2018) encoder model |
| text-embedding-3-large / -small | OpenAI's paid embedding models |
| all-MiniLM-L6-v2 | A popular free, open-source embedding model |
| Token vs vector | Token = input (ID number); vector = output (meaning numbers) |
| word2vec | An early model giving each word a vector; famous for king - man + woman = queen |
| Vector arithmetic | Adding and subtracting vectors; the result is a point, then you find the nearest known word |
| Cosine similarity | The real measure of closeness between two vectors (named only; revisit later) |

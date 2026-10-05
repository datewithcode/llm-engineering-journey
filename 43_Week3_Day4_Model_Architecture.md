# LLM Engineering – Week 3, Day 4 (Part 2)
## Inside the Model: Embeddings, Layers, and the LM Head

> Personal study notes. This is where **vectors** finally appear, promised since the tokenizer lecture.
> Notebook: week3/day4.ipynb (Colab)

---

## READ THIS FIRST (the whole model in one picture)

```
   WORDS COME IN
        ↓
  ┌─────────────┐
  │  STATION 1  │   Turns each word into a "profile"
  │  EMBEDDING  │   (a long list of numbers describing that word)
  └─────────────┘
        ↓
  ┌─────────────┐
  │  STATION 2  │   16 workbenches in a row.
  │  16 LAYERS  │   Each one refines the profiles a bit more.
  └─────────────┘   This is where the thinking happens.
        ↓
  ┌─────────────┐
  │  STATION 3  │   Looks at the finished profiles and says
  │   LM HEAD   │   "the next word should probably be ___"
  └─────────────┘
        ↓
   NEXT WORD OUT
```

**Three stations. Words in, meaning-numbers, thinking, next word out.** That's the whole model.

---

## WHY: The Purpose of Each Station

| Station | Why it exists |
|---|---|
| **Embedding** | A token ID (like 9246) carries no meaning. 9246 and 9247 are adjacent numbers but "cat" and "table" have nothing in common. The model needs numbers that actually encode meaning, so similar words end up near each other. |
| **Layers** | A word's meaning depends on context. "Bank" means different things near "river" vs "money." The layers adjust each word's meaning based on the surrounding words (that's attention), 16 times over, refining each pass. |
| **LM Head** | The layers produce meaning-numbers, but you need an actual word. The LM head converts meaning back into a score for every possible token, so one can be picked. |

---

## Printing a Model Shows Its Structure

```python
print(model)
```

PyTorch models print as a tree. Real output for Llama 3.2 1B:

```
LlamaForCausalLM(
  (model): LlamaModel(
    (embed_tokens): Embedding(128256, 2048)        ← STATION 1
    (layers): ModuleList(
      (0-15): 16 x LlamaDecoderLayer(...)          ← STATION 2
    )
  )
  (lm_head): Linear(in_features=2048, out_features=128256)   ← STATION 3
)
```

This is the first time you see what "a neural network with billions of parameters" actually looks like.

---

## STATION 1: Embedding (where vectors appear)

**The code:**
```
(embed_tokens): Embedding(128256, 2048)
```

**Reading it:** `Embedding(in, out)`. Takes one of 128,256 possible tokens, produces 2,048 numbers.

| Number | What it is | Where it comes from |
|---|---|---|
| 128,256 | Vocabulary size | The tokenizer's dictionary (file 40) |
| 2,048 | Vector size ("hidden dimension") | Design choice for this model |

**What actually happens:**
```python
token_id = 9246                                    # "cat"
vector = [0.23, -0.81, 0.44, ... 2045 more]        # what comes out
```

That output list is a **vector embedding**. 2,048 numbers = a 2,048-dimensional vector.

**Visualise it as a lookup table:**

| Token ID | Col 1 | Col 2 | ... | Col 2048 |
|---|---|---|---|---|
| 0 | 0.11 | -0.42 | ... | 0.03 |
| 9246 ("cat") | 0.23 | -0.81 | ... | 0.44 |
| 128255 | -0.09 | 0.55 | ... | 0.17 |

128,256 rows, 2,048 columns. The model looks up the row for whatever token came in. **Those numbers were learned during training** — they're parameters, the knobs from Week 1.

### First: why must text become numbers at all?

The model is a giant calculator. Every one of its billions of parameters does the same thing:

```
input number × parameter + other number = output number
```

You cannot multiply a word by a number. Try it in Python:

```python
"cat" * 0.5
# TypeError: can't multiply sequence by non-int of type 'float'
```

Python refuses. The model has exactly the same problem. It can't do `"cat" × 0.5`, but it can do `9246 × 0.5`. **So text must become numbers before the model can do anything with it.** Not because numbers are smarter, but because the machine only does arithmetic.

That's step one (the token ID). The next question is why **one** number per token isn't enough.

### Why 2,048 numbers instead of one?

A token ID is like an employee number: 4471 tells you nothing about the person. An embedding is like a full profile: 2,048 measurements describing skills, department, experience. Now you can compare people meaningfully.

The model learns to place similar words near each other in that 2,048-dimensional space:
- "cat" and "dog" → similar vectors (both animals, both pets)
- "cat" and "table" → distant vectors
- "king" − "man" + "woman" → lands near "queen"

### Seeing an embedding space: the 2D animal picture (from an external course)

A 2,048-dimensional space is impossible to picture. So shrink it to 2 dimensions you can draw.

Two axes: **size** (left to right) and **friendliness** (bottom to top). Place some animals:

```
friendly
   ↑
   |   ladybug           dog (0.5, 0.9)
   |                  cat (0.4, 0.7)
   |
   |
   |   mosquito                          hippo
   └──────────────────────────────────────→ size
```

| Word | Embedding vector (size, friendliness) |
|---|---|
| dog | (0.5, 0.9) |
| cat | (0.4, 0.7) |
| ladybug | small, friendly |
| mosquito | tiny, unfriendly |
| hippo | huge, very unfriendly |

Each word is now a **point**. Dog and cat sit close together. Hippo sits far away. Distance on this chart = difference in meaning.

That list of two numbers per word is an **embedding vector**. The whole chart is an **embedding space**. A real model does exactly this, but with 2,048 axes instead of 2.

### Three things the toy picture gets wrong (important)

| Toy picture | Real model |
|---|---|
| 2 dimensions | Thousands of dimensions (2,048 for Llama 3.2 1B, several thousand for frontier models) |
| Axes have human names (size, friendliness) | Axes are **not human-interpretable**. The model invents its own directions during training. |
| Fixed positions | **Positions change with context** (see below) |

### Embeddings are dynamic: they move with context

The embedding table gives each token a **starting** position. Then the 16 layers move it based on the surrounding words.

- Chatting about a **Chihuahua**, then you say "dog" → "dog" shifts toward the small end of the size axis
- A cartoon where a **hippo** is cute and grants wishes → "hippo" shifts up the friendliness axis

**WHY this matters:** this is what the 16 layers are actually doing. They take each word's starting point and nudge it to where it belongs **in this specific sentence**. Same idea as "bank" near "river" vs "bank" near "money."

### Why token IDs can't do this

Spain and France are related (neighbouring European countries). Their token IDs are two arbitrary integers with no relationship. Their embeddings, however, sit close together in the space. **Integers can't express relationships. Vectors can.**

### Key correction: models work on embeddings, not tokens

Tokens are only an intervening step:

```
text → tokens → token IDs → EMBEDDINGS → (all the real work happens here) → unembedding → token IDs → text
```

Everything in the 16 layers, including attention, is modifying embeddings. **"Unembedding matrix"** is another name for the LM head: it converts embeddings back into token scores.

### Rotary embedding (Llama's specific technique)

"The cat chased the dog" and "the dog chased the cat" have identical words, different meanings. The model needs to know **word order**. Rotary embedding builds position information into the vectors. Worth knowing the name; details beyond this course.

---

## STATION 2: The 16 Layers (where thinking happens)

**The code:**
```
(layers): ModuleList(
  (0-15): 16 x LlamaDecoderLayer(...)
)
```

16 identical components, numbered 0 to 15. (Llama 3.1 8B has 32 — bigger model, more layers.)

**What each layer does:** 2,048 numbers in, transformed, 2,048 numbers out. Same size in and out, so they stack.

```
vector (2048) → layer 0  → vector (2048)
              → layer 1  → vector (2048)
              → ...
              → layer 15 → vector (2048)
```

**What "transformed" means:** each layer contains attention (Week 1 — every word looking at every other word) plus more parameters that blend the numbers. Millions of parameters per layer.

### Two ways to visualise it

**Audio mixing desk** (the lecturer's): picture a mixing desk with hundreds of sliders. Signals come in, you adjust sliders, a new blend comes out. Each layer is a mixing desk. The sliders are the parameters. Stack 16 desks in a row; each refines what the previous produced.

**Relay race:** the vector gets passed from runner to runner, each modifying it slightly. Enters as "what this word means in isolation," exits as "what this word means in this sentence, and what should follow."

**Why 16?** Design choice. More layers = more transformation = more capability, but more memory and slower.

---

## STATION 3: LM Head (meaning back to words)

**The code:**
```
(lm_head): Linear(in_features=2048, out_features=128256)
```

**Reading it:** 2,048 in, 128,256 out. **Exactly reversed from the embedding layer.** That's deliberate.

| | In | Out | Direction |
|---|---|---|---|
| Embedding | 128,256 (vocabulary) | 2,048 (meaning) | vocabulary → meaning |
| LM Head | 2,048 (meaning) | 128,256 (vocabulary) | meaning → vocabulary |

**What comes out:** a score for every possible token.
```python
[0.001, 0.003, ..., 8.2, ..., 0.0001]    # 128,256 scores
#                    ↑
#              token 65756 (" sat") scores highest
```

Those raw scores are **logits** (the word from file 41). Softmax turns them into probabilities. Then temperature and top_p decide which gets picked.

**"LM head" = language model head.** "Head" means the final output layer. Also called a **fully connected layer**.

---

## The Model Is a Classifier

Traditional data science: a **classifier** sorts things into buckets. "Spam or not spam?" = 2 buckets.

An LLM is a classifier with **128,256 buckets**, one per token. Its job: given this input, which bucket does the next token belong in?

**Why this framing matters:** it demystifies the model. It's not "thinking" or "understanding." It's a very large classifier choosing among 128,256 options, over and over.

---

## The Full Chain with Real Values

```
"The cat"
    ↓ tokenizer
[128000, 791, 8415]                              ← token IDs
    ↓ Embedding(128256, 2048)
[[...2048 numbers], [...2048], [...2048]]        ← one vector per token
    ↓ 16 × LlamaDecoderLayer
[[...2048 numbers], [...2048], [...2048]]        ← same shape, transformed meaning
    ↓ Linear(2048, 128256)
[0.001, 0.003, ..., 8.2, ...]                    ← 128,256 logits
    ↓ softmax + temperature + top_p
65756                                             ← chosen token ID
    ↓ tokenizer.decode
" sat"
```

Every concept from weeks 1-3 in one picture: tokens, vectors, layers, parameters, probability distribution, temperature.

---

## How to Hold It in Your Head: Three Numbers

| Number | What it is | Where it comes from |
|---|---|---|
| **128,256** | Vocabulary size | The tokenizer's dictionary |
| **2,048** | Vector size (hidden dimension) | Design choice for this model |
| **16** | Number of layers | Design choice for this model |

Every model has these three numbers:
- Llama 3.2 1B: vocab 128,256, vectors 2,048, layers 16
- Llama 3.1 8B: vocab 128,256, vectors 4,096, layers 32

Bigger model = bigger vectors + more layers. **Same three stations.**

**The shape rule:** vocabulary → meaning → (thinking) → meaning → vocabulary. Wide, narrow, narrow, wide.

---

## How to Explain This to Someone

### If a non-technical person asks "What's inside an AI model?"

"Three parts, like a factory. The first turns each word into a long list of numbers that describes what the word means. The middle part has sixteen workbenches in a row, each one adjusting those numbers based on the surrounding words. The last part looks at the result and picks the most likely next word. That's it, repeated for every word it writes."

### If a technical person asks

"A decoder-only transformer has three components: an embedding table mapping vocab indices to dense vectors (128256 × 2048 for Llama 3.2 1B), a stack of N decoder layers each applying self-attention and feed-forward transformations while preserving the hidden dimension, and a linear LM head projecting back to vocab size to produce logits. Softmax over those logits gives the next-token distribution, which sampling parameters then modify. Architecturally it's a 128K-way classifier applied autoregressively."

### The analogy

A factory with three stations: turn words into profiles, refine the profiles through 16 workbenches, then convert back into a word choice. Or: the embedding is a lookup table, the layers are mixing desks, the head is a scorer.

### The one-liner

"A model is three parts: embedding turns words into meaning-numbers, layers refine that meaning, and the head converts it back into a next-word prediction."

---

## Self-Check

1. Name the three stations and what each does.
2. Why can't the model just use the token ID directly?
3. What is a vector embedding? How many numbers for Llama 3.2 1B?
4. Why are the embedding and LM head shapes reversed?
5. What happens inside each of the 16 layers?
6. What are logits? Where do they come from?
7. Why is an LLM technically a classifier? How many buckets?
8. What are the three numbers that describe any model's architecture?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| Embedding layer | Converts token IDs into vectors (lists of numbers encoding meaning) |
| Vector embedding | The list of numbers representing one token (2,048 for Llama 3.2 1B) |
| Hidden dimension | The vector size; how many numbers represent each token inside the model |
| Rotary embedding | Llama's technique for encoding word position into the vectors |
| Decoder layer | One of the stacked transformer layers; contains attention and feed-forward parts |
| LM head | The final layer; converts vectors back into a score per vocabulary token |
| Logits | The raw scores the LM head produces, before softmax |
| Fully connected layer | Another name for the LM head |
| Classifier | A model that sorts input into buckets; an LLM has 128,256 buckets (one per token) |
| `print(model)` | Shows the full architecture as a nested tree |

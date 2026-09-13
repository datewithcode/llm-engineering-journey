# LLM Engineering – Week 1, Day 4 (Part 4)
## Tokens: Why Chunks, Tokenizer vs Transformer, Word Stems

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Builds on the dictionary picture from 03_Week1_Day3_ChatGPT_Demo_Tokens.md.

---

## READ THIS FIRST (tokens in 4 lines)

1. The model can't read text. A small program called the **tokenizer** chops text into chunks and looks each one up in a dictionary: `"the cat sat"` → `[1, 2, 3]`. The model receives only the numbers.
2. A chunk (token) can be a whole common word, a piece of a rare word, or a single letter. Nothing is ever "unknown" because rare words are built from smaller pieces.
3. **Tokenizer = the translator at the door** (tiny, no learning, just a lookup). **Transformer = the brain inside** (huge, this is the model, this is what gets trained). They are NOT the same thing.
4. Tokens match word stems nicely: "play" is one chunk, "ing"/"ed"/"er" are separate chunks, so the model learns "play" once and reuses it.

---

## 0. What I Already Had

Text → tokenizer (dictionary lookup) → list of numbers → model. `"the cat sat"` → `[1, 2, 3]`. The model never sees letters, only numbered chunks.

---

## 1. Why Tokens — Three Attempts

The model needs text turned into numbers. Three ways to chop the text up were tried.

### Attempt 1: One letter = one number
- Dictionary of ~100 entries (a–z, A–Z, punctuation). Tiny and simple.
- Problem: the model had to learn *everything* from scratch — that b-a-n-a-n-a is a fruit, that c-a-t and c-a-t-s are related, plus what all words mean. Too much left to the network. Learned slowly.

### Attempt 2: One whole word = one number
- Obvious next step.
- Problem: hundreds of thousands of words plus every name, place, product, made-up word. Dictionary exploded. Rare words got left out → when the model met one, it simply didn't understand. People lived with this for years.

### Attempt 3: Chunks = tokens (the middle ground)
- A chunk can be a whole common word, a fragment, or even two common words together.
- Dictionary stays manageable (~50,000–200,000 entries).
- **Any** word can be handled: if not in the dictionary, build it from smaller chunks, down to single letters if needed. Nothing is ever "unknown."

**Same point as the transformer:** nothing magical about tokens. Letters or words could have worked. Tokens were the efficient compromise — small enough dictionary, meaningful enough chunks, nothing left out.

---

## 2. Tokenizer vs Transformer — NOT the same thing

**Tokenizer** = the front door. A small program with a dictionary. Only job: text → numbers, and back. No learning. Built once before training, never changes.

**Transformer** = the machine inside the building. Takes the numbers, does the heavy work (attention, billions of parameters), produces the next number. This *is* the model — it's where all the parameters live and where training happens.

```
your text
   ↓
tokenizer      (text → numbers)          ← tiny, just a lookup
   ↓
transformer    (numbers → next number)   ← huge, this is "the model", this is what gets trained
   ↓
tokenizer      (number → text)           ← same lookup in reverse
   ↓
reply shown to you
```

**Tokenizer = translator at the door. Transformer = the brain inside.**

---

## 3. Two Loose Ends

### Word stems — why chunks fit language nicely
English builds words from a core plus endings: play, play**ing**, play**ed**, play**er**, play**ful**. With tokens, "play" is one chunk and each ending is another. The model learns "play" once and reuses it — it sees that "playing" and "played" share a core and differ only in the modifier. Same for un-, re-, -ness, -tion.
- Letters can't do this (too small). Whole words can't (each form is a separate unknown).
- Tokens land at exactly the right size for how we spell things. This is the "nice extra property."

### A token is not a vector
- A **token** is just an ID number from the dictionary (`2` for "cat"). It's the *very first* input to the model.
- A **vector** is something different that appears *inside* the model, further down. Not covered yet.
- Hold: **token ID goes in first; vectors come later; they are not the same thing.**

---

## 4. My Questions Answered

### Are the numbers random?
Not random — arbitrary but fixed. They're just the position in the dictionary when it was built (entry 1, 2, 3...). Which chunk gets which number doesn't matter; the model doesn't care. What matters is it's **fixed forever**: "cat" is always the same number for that model. Consistency is the point — the model learns everything about "cat" under that one ID.
(Real tokenizers use ~5-digit IDs, e.g. "cat" = 9246, because there are ~100,000 entries. 1, 2, 3 was just to keep the example small.)

### What is a token?
A chunk of text that has its own entry in the tokenizer's dictionary. It can be:
- a whole common word ("cat", "the")
- part of a word ("un", "believ", "able")
- occasionally two common words stuck together
- at the smallest, a single letter or a space

Common = whole word gets one token. Rare = split into pieces. Every token has a fixed ID.

---

## 5. Try It

OpenAI's tokenizer page: platform.openai.com/tokenizer. Type text and watch it split into chunks with ID numbers. Try "playing", "unbelievable", my own name.

---

## 6. One-Line Recap

1. Letters = too small (model learns too slowly). Words = too many (rare ones left out). Tokens = the efficient middle: small dictionary, nothing unknown.
2. Tokenizer is the translator at the door (no learning). Transformer is the brain inside (this is the model, this is what trains).
3. Tokens match word stems (play + ing/ed/er), so the model reuses what it learns.
4. Token ID ≠ vector. Token goes in first; vectors come later.

---

## How to Explain This to Someone

### If a non-technical person asks "What is a token?"
"A token is a chunk of text — usually a whole common word, or a piece of a rare word. Before the AI reads your message, it gets chopped into these chunks and each chunk becomes a number. 'Playing' might become 'play' + 'ing.' The AI works on the numbers, not the letters."

### If a technical person asks
"Tokens are subword units produced by a tokenizer (typically BPE or similar) with a fixed vocabulary of ~50k-200k entries. Common words are single tokens; rare words decompose into pieces down to characters if needed, so nothing is out-of-vocabulary. The tokenizer is a stateless lookup built before training and never changes. The transformer operates only on token IDs. Tokenizer ≠ transformer: one is the translator at the door, the other is the model itself."

### The analogy
Tokenizer = translator at the door (tiny, no learning). Transformer = the brain inside (huge, this is what trains). Word stems: "play" is one chunk, "ing"/"ed"/"er" are separate, so the model learns "play" once and reuses it.

### The one-liner
"A token is a chunk of text turned into a number — the tokenizer chops, the transformer thinks."

---

## 7. Self-Check Questions

1. What was wrong with one-letter-per-number? With one-word-per-number?
2. Why can a token-based model handle a word it has never seen?
3. Tokenizer vs transformer — which one learns? Which one is "the model"?
4. Explain the word-stem advantage with "play".
5. Are token ID numbers random? What matters about them?
6. What is a token, in one sentence?
7. Is a token the same as a vector?

---

## 8. Quick Glossary

| Term | Plain meaning |
|---|---|
| Token | A chunk of text (whole word, part of a word, or two words) with its own dictionary entry |
| Token ID | The fixed number for that chunk in the dictionary |
| Tokenizer | The program that converts text ↔ token IDs; a lookup, no learning |
| Vocab / vocabulary | The tokenizer's dictionary of all chunks |
| Transformer | The model itself — takes token IDs, uses attention and parameters, outputs the next token; this is what gets trained |
| Word stem | The core of a word ("play") that endings attach to |
| Vector | Something inside the model, further down — different from a token (later) |

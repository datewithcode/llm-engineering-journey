# LLM Engineering – Week 3, Day 3 (Part 2)
## Exploring the Vocabulary and BPE (Byte Pair Encoding)

> Personal study notes.
> **Accuracy note:** section 4b is what the lecture actually showed (special-token list, vocab size, comparing four models' tokenizers). BPE (section 3) and the vocabulary ranges (section 2) are **extra explanation**, correct but not shown in the lecture.
> Notebook: week3/day3.ipynb (Colab)

---

## READ THIS FIRST (whole lecture in 3 lines)

1. The tokenizer's vocabulary is a Python dictionary you can inspect: `tokenizer.vocab` has 128,256 entries for Llama 3.1. Low IDs = single characters, middle = word fragments, high = full common words, highest = special tokens.
2. **BPE (Byte Pair Encoding)** is the algorithm that builds this dictionary: start with individual characters, find the most common pair, merge them into a new token, repeat until you reach the target vocabulary size. That's why common words get their own token and rare words are built from pieces.
3. The vocabulary size is a design choice — bigger = more full words get their own token (efficient), but uses more memory. Llama chose ~128K entries.

---

## 1. The Vocabulary as a Python Dictionary

```python
tokenizer.vocab              # a dict: {"token_text": token_id, ...}
len(tokenizer.vocab)          # → 128,256 for Llama 3.1
```

128,256 entries. Every possible chunk of text has a number. You can look up any word:

```python
tokenizer.vocab["the"]       # → some number
tokenizer.vocab[" the"]      # → a DIFFERENT number (with space = different token)
```

Remember from Week 1 (file 08): " important" (with space, ID 3378) and "important" (no space, ID 31371) are different tokens. Same thing visible here in the actual dictionary.

---

## 2. Structure of the Vocabulary — Low, Middle, High

*(Extra explanation, not shown in the lecture. You can explore this yourself by sorting `tokenizer.vocab` by ID; see section 4.)*

| Token ID range | What's there | Examples |
|---|---|---|
| 0–255 (lowest) | Single characters, individual bytes | `!`, `"`, `#`, `A`, `B`, `a`, `b`, single letters |
| 256–~1,000 | Small common fragments | `th`, `in`, `er`, `an`: pieces that appear inside many words |
| ~1,000–~128,000 | Full words and longer pieces | `the`, `play`, `important` |
| 128,000–128,255 (highest) | **Special tokens** | `<\|begin_of_text\|>` (128000), `<\|end_of_text\|>` (128001), role headers, many reserved slots |

**Why this order?** Because of how the vocabulary was built (BPE, next section). Single characters were added first, common pairs next, full words later. The ID number reflects when the token was added during vocabulary construction.

---

## 3. BPE (Byte Pair Encoding) — How the Vocabulary Is Built

*(Extra explanation, not covered in the lecture.)*

Before training the model, someone has to build the dictionary. The algorithm is called **BPE**. Here's how it works:

### Step by step

1. **Start with every single byte** (character). ~256 entries: every letter, digit, punctuation.
2. **Scan the entire training text.** Find the pair of adjacent tokens that appears most often. Maybe `t` next to `h` appears billions of times.
3. **Merge that pair into a new token:** `th`. Add it to the dictionary as entry 256.
4. **Scan again with the updated dictionary.** Now maybe `th` next to `e` appears most often. Merge into `the`. Add as entry 257.
5. **Repeat** until you reach the target vocabulary size (128,000 for Llama).

### A tiny example

Training text: `"aaabaaab"`

| Step | Most common pair | New token | Dictionary so far |
|---|---|---|---|
| Start | — | — | `a`, `b` |
| 1 | `a` + `a` (appears 4 times) | `aa` | `a`, `b`, `aa` |
| 2 | `aa` + `a` (appears 2 times) | `aaa` | `a`, `b`, `aa`, `aaa` |
| 3 | `aaa` + `b` (appears 2 times) | `aaab` | `a`, `b`, `aa`, `aaa`, `aaab` |

Now the text `"aaabaaab"` tokenizes as just two tokens: `aaab` + `aaab`. Started as 8 characters, compressed to 2 tokens.

### Why this explains everything about tokenization

| Observation from earlier weeks | BPE explains it |
|---|---|
| Common words ("the", "and") are one token | They were common pairs that got merged early |
| Rare words ("unbelievable") are split into pieces | Their pieces got merged, but the full word wasn't common enough to earn its own slot |
| Nothing is ever "unknown" | Every character exists as a single-byte token (the starting set). Worst case, a word is split into individual characters. |
| Low IDs = small fragments, high IDs = full words | Fragments were added first (step 1), full words were added later (steps 100,000+) |

### Vocabulary size is a design choice

| Larger vocab | Smaller vocab |
|---|---|
| More full words get their own token | Fewer, more splitting |
| More efficient (fewer tokens per sentence) | Less efficient |
| More memory for the embedding table | Less memory |
| Llama chose ~128K | Some models use 32K or 64K |

---

## 4. Exploring the Vocabulary Yourself (try these)

```python
# Sort by ID to see the structure
sorted_vocab = sorted(tokenizer.vocab.items(), key=lambda x: x[1])

# Look at the bottom (single characters)
sorted_vocab[:20]

# Look at the middle (fragments and words)
sorted_vocab[1000:1020]

# Look near the top (long common tokens)
sorted_vocab[-300:-280]

# Look at the very top (special tokens)
sorted_vocab[-20:]

# Look up a specific word
tokenizer.vocab.get("hello")       # with no space
tokenizer.vocab.get(" hello")      # with space (different token!)
```

---

## 4b. What the Lecture Actually Showed (Week 3 Day 3)

### The special tokens: `get_added_vocab()`
```python
tokenizer.get_added_vocab()
```
Lists every **special token** in the vocabulary: `<|begin_of_text|>`, `<|end_of_text|>`, header tokens, and many **reserved** tokens (slots set aside for future use).

### The vocabulary size: 128,256
```python
len(tokenizer.vocab)     # → 128256
```
**128,000 regular tokens + 256 special tokens** tacked on at the end. That's the full size of Llama's tokenizer. (The lecturer first thought 128,000 was the top ID; the 256 special ones sit above it.)

### Comparing four models' tokenizers on the same sentence
He tokenized: *"I am curiously excited to show Hugging Face Tokenizers in action to my LLM engineers"* with four tokenizers:

| Model | Maker | What he observed |
|---|---|---|
| Llama 3.1 | Meta | Starts with the `<\|begin_of_text\|>` special token |
| Phi-4 mini instruct | Microsoft | **Completely different ID numbers.** Does **not** start with a special token. Splits "Hugging Face" differently from Llama. |
| DeepSeek 3.1 | DeepSeek | Different IDs again. Its chat template has a beginning-of-sentence token, then user and assistant markers, arranged differently. |
| Qwen 2.5 Coder | Alibaba Cloud | A tokenizer for a **coding** model |

**The Qwen Coder demo:** he tokenized a tiny Python function (`def hello_world(person): print("Hello", person)`) and printed each token next to its text. Common code constructs get their own tokens: for example `_world` is one token, and `):` is a single token. His guess: a tokenizer built for a coding model likely gives more tokens to common code patterns, so each token carries more meaning for code.

### The lessons from the comparison
- **Every model has its own tokenizer.** Different IDs, different splits, different special tokens, different chat templates.
- **The numbers themselves don't matter.** Only consistency with that model's training data matters.
- **Don't obsess over token counts.** One tokenizer producing fewer tokens saves a fraction of a cent. Output **quality** matters far more.
- **Models only understand token IDs.** Not language, and not lists of dicts.

---

## 5. How to Explain This to Someone

### If a non-technical person asks "How does the AI's dictionary get built?"

"Imagine you're creating a shorthand for writing faster. You start with individual letters. Then you notice 't' and 'h' always appear together, so you make a shorthand for 'th.' Then 'th' and 'e' always appear together, so you make one for 'the.' You keep going until you have shortcuts for all the common words. That's exactly how the AI's dictionary is built — an algorithm scans billions of words and creates shortcuts for the most common combinations."

### If a technical person asks

"Llama uses Byte Pair Encoding (BPE) to build its 128K-entry vocabulary. Starting from the 256 byte-level tokens, it iteratively merges the most frequent adjacent pair into a new token until the target vocab size is reached. Token IDs reflect merge order: low = single bytes, mid = common subwords, high = full words and code fragments, top = reserved special tokens. The vocab is a static artifact built before pre-training and frozen thereafter. It's accessible as `tokenizer.vocab`, a Python dict mapping token strings to integer IDs."

### The analogy

Building a shorthand system by watching what combinations appear most often, then making a symbol for each one. Start with letters → merge common pairs → end up with shortcuts for whole words.

### The one-liner

"BPE builds the tokenizer's dictionary by repeatedly merging the most common adjacent pair, starting from single characters up to full words."

---

## 6. Self-Check

1. How many entries does Llama 3.1's vocabulary have?
2. What's at the low end of the vocabulary? The high end? The very top?
3. Explain BPE in three steps.
4. Why are common words single tokens and rare words split into pieces? (Answer using BPE.)
5. Why is nothing ever "unknown" to the tokenizer?
6. Why is vocabulary size a design choice? What's the trade-off?
7. How do you look up a specific word's token ID in code?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| `tokenizer.vocab` | The full vocabulary as a Python dict: token string → token ID |
| Vocabulary size | How many entries in the dictionary (128,256 for Llama 3.1) |
| BPE (Byte Pair Encoding) | Algorithm that builds the vocabulary by repeatedly merging the most common adjacent pair |
| Byte-level tokens | The starting set: ~256 entries, one per character/byte |
| Merge | Combining two adjacent tokens into one new token during BPE |
| Merge order | Low IDs = merged first (small fragments), high IDs = merged later (full words) |
| `batch_decode` | Decodes each token ID separately, showing individual splits (from previous lecture) |

# LLM Engineering – Week 3, Day 2 (Part 1)
## Pipelines (the Easy Way) and the Tokenizer in Real Code

> Personal study notes. The tokenizer section connects directly to Week 1's dictionary picture.
> Notebook: week3/day2.ipynb (Colab)

---

## READ THIS FIRST (whole lecture in 4 lines)

1. Hugging Face's `transformers` library has two levels: **pipelines** (pre-baked, one line, handles everything) and **low-level** (manual tokenizer + model, full control). You're learning both; the low level is the one that matters.
2. `pipeline("text-classification")` does sentiment analysis in one line. Useful, but it hides what's happening inside.
3. `AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")` downloads the actual tokenizer for Llama. It's the dictionary from Week 1, alive in code: `.encode()` = text → numbers, `.decode()` = numbers → text.
4. **Special tokens:** `<|begin_of_text|>` (added to every input automatically) and `<|end_of_text|>` (the model outputs this when it's done). Every model has its own special tokens.

---

## 1. Two Levels of the Transformers Library

| Level | What it is | Analogy |
|---|---|---|
| **Pipelines** (top) | Pre-baked, one-line. Say "do text classification" and it handles everything. | A recipe box — pick, follow, done. |
| **Low-level** (bottom) | Manually load tokenizer, load model, feed tokens, read outputs. Full control. | Walking into the kitchen — chop, cook, plate, everything by hand. |

Pipelines are great for quick tasks. The low level is what you need for fine-tuning, custom models, and understanding what's actually happening.

---

## 2. Pipelines — the Pre-Baked Way

### Text classification (sentiment analysis)

```python
from transformers import pipeline

classifier = pipeline("text-classification")
result = classifier("I love this course!")
# → [{"label": "POSITIVE", "score": 0.9999}]
```

One line. Behind the scenes, the pipeline:
1. Downloaded a default model suited for text classification
2. Tokenized the text (text → numbers)
3. Ran the model (numbers → prediction)
4. Interpreted the output (prediction → "POSITIVE" with confidence 0.9999)

You didn't choose the model, load it, or handle tokens. The pipeline did everything.

### Batch processing

```python
results = classifier(["I love this!", "This is terrible!", "It's okay I guess"])
# → [POSITIVE 0.99, NEGATIVE 0.99, NEGATIVE 0.82]
```

Pass a list, get a list back. The "It's okay" being classified as negative with 0.82 confidence shows the model isn't perfect — arguably "okay" is neutral, not negative.

### Real-world use case

Sentiment analysis on Yelp/Amazon reviews = a billion-dollar business problem. Companies need to process millions of reviews to understand customer satisfaction. This pipeline does it in one line.

### Other pipeline tasks (examples from the lecture)

- `pipeline("text-generation")` — generate text (you'll use this)
- `pipeline("image-to-text")` — describe an image
- `pipeline("text-to-speech")` — generate audio (yesterday's demo)

---

## 3. The Tokenizer in Real Code (the Week 1 dictionary, alive)

### Loading a tokenizer

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
```

This downloads Llama's tokenizer from Hugging Face. It's the exact same concept as `tiktoken` from Week 1 — a dictionary that converts text to numbers and back. But this time it's the ACTUAL tokenizer the model uses.

`AutoTokenizer` means "figure out the right tokenizer class for this model automatically." Different models have different tokenizer implementations; `Auto` handles that for you.

### Encoding (text → numbers)

```python
tokens = tokenizer.encode("Life is short")
# → [128000, 26833, 374, 2875]
```

Three words, but FOUR numbers. The first one (`128000`) is a **special token** — see below.

### Decoding (numbers → text)

```python
tokenizer.decode(tokens)
# → "<|begin_of_text|>Life is short"
```

The `128000` decodes to `<|begin_of_text|>`. Not a real word — a signal.

### Connecting to Week 1

| Week 1 concept | What you see now in real code |
|---|---|
| Dictionary lookup (`"the cat sat"` → `[1, 2, 3]`) | `tokenizer.encode("Life is short")` → `[128000, 26833, 374, 2875]` |
| Reverse lookup (`[1, 2, 3]` → `"the cat sat"`) | `tokenizer.decode(...)` → `"<\|begin_of_text\|>Life is short"` |
| `tiktoken` (OpenAI's tokenizer) | `AutoTokenizer` (Hugging Face, works with any model) |
| "The model sees numbers, not text" | encode/decode proves it — text goes in, numbers come out |

---

## 4. Special Tokens (new concept)

Every model has special tokens that aren't real words. They're signals baked into the vocabulary.

### BOS — Beginning of Sequence

```python
tokenizer.bos_token        # → "<|begin_of_text|>"
tokenizer.bos_token_id     # → 128000
```

Added **automatically** to the start of every input by `.encode()`. Tells the model "a new input starts here." Like a bell that rings before the teacher starts speaking.

### EOS — End of Sequence

```python
tokenizer.eos_token        # → "<|end_of_text|>"
tokenizer.eos_token_id     # → 128001
```

When the model **generates** this token, it means "I'm done talking." This is the "stop" signal. Your code sees this and stops asking for more tokens.

**Connection to tools:** the `finish_reason == "stop"` from Week 2's tool-calling code is exactly this — the model output the EOS token.

### Every model has different special tokens

| Model | BOS token | EOS token |
|---|---|---|
| Llama | `<\|begin_of_text\|>` (128000) | `<\|end_of_text\|>` (128001) |
| GPT | Different format, different IDs | Different |
| Other models | Different | Different |

That's why you download the tokenizer **matched to the model**: `AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")`. Using the wrong tokenizer with a model would produce garbage, because the IDs wouldn't match.

---

## 5. How to Explain This to Someone

### If a non-technical person asks "What's a pipeline?"

"Imagine you want to know if a customer review is positive or negative. Instead of understanding all the math behind AI, you just say 'analyze this review' and get the answer in one line. A pipeline is a pre-built recipe that handles all the complicated parts for you."

### If a technical person asks

"Hugging Face pipelines are high-level abstractions over the transformers library. You specify a task (`text-classification`, `text-generation`), and the pipeline auto-selects a default model, tokenizes input, runs inference, and post-processes the output. Under the hood it's `AutoTokenizer` + `AutoModel` + task-specific head. For production or fine-tuning, you go one level deeper and manage those components yourself."

### If someone asks "What are special tokens?"

"Every AI model has invisible markers in its vocabulary — like how a book has a title page before chapter 1 and 'THE END' on the last page. The model needs these to know where the input starts and where its reply should stop. Different models use different markers, which is why you always use the tokenizer that matches the model."

### The analogy
Pipeline = ordering from a menu. Low-level = cooking it yourself. The tokenizer = the dictionary from week 1, alive in code. Special tokens = the title page and 'THE END' of a book.

### The one-liner

"A pipeline does AI in one line; the tokenizer is the dictionary that turns your words into numbers the model can read."

---

## 6. Self-Check

1. What are the two levels of the transformers library? Which one gives more control?
2. What does `pipeline("text-classification")` do behind the scenes? (Four steps.)
3. What is `AutoTokenizer` and why is it called "Auto"?
4. `tokenizer.encode("Life is short")` returns 4 numbers for 3 words. Why?
5. What does `<|begin_of_text|>` mean? Who adds it?
6. What does `<|end_of_text|>` mean? When is it generated?
7. Why must the tokenizer match the model?
8. How does the EOS token connect to `finish_reason == "stop"` from Week 2?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| Pipeline | Pre-baked, one-line interface: specify a task, it handles everything |
| `pipeline("text-classification")` | Sentiment analysis in one line |
| AutoTokenizer | Downloads the correct tokenizer for any model automatically |
| `.encode(text)` | Text → list of token IDs (including special tokens) |
| `.decode(ids)` | List of token IDs → text |
| `.from_pretrained("model-name")` | Download from Hugging Face Hub |
| Special tokens | Signals in the vocabulary that aren't real words (BOS, EOS) |
| BOS (beginning of sequence) | Token added to every input: "input starts here" |
| EOS (end of sequence) | Token the model generates when done: "I'm finished" |
| `eos_token_id` | The number for the EOS token in this model's vocabulary |
| `finish_reason == "stop"` | The API's way of saying "the model output EOS" |

# LLM Engineering – Week 3, Day 3 (Part 1)
## Gated Models, Terms of Service, and batch_decode

> Personal study notes. Two new practical things; the rest reinforces earlier weeks.
> Notebook: week3/day3.ipynb (Colab, but runs fine on CPU — no GPU features used today)

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Some models are **gated** — you must agree to the creator's terms on Hugging Face before downloading. Llama 3.1 requires this. Tip: use the same email as your HF account and say "personal education" to avoid delays.
2. **`batch_decode`** is a third tokenizer method: it decodes each token ID separately into a list of individual token strings, so you can see exactly how text was split.
3. If you can't get Llama approved, use **Qwen or DeepSeek** instead — no approval needed, equally capable.

---

## 1. Gated Models — Terms of Service

### What is a gated model?

Some models on Hugging Face are marked "gated." You can't download them until the creator approves you. This is common for models from big labs (Meta, Google) who want to track usage.

### How to get approved for Llama 3.1

1. Visit the model page: `https://huggingface.co/meta-llama/Llama-3.1-8B`
2. You'll see a form instead of a download button. Fill it out.
3. **Tips to avoid delays:**
   - Use the **same email** as your Hugging Face account. Mismatched emails trigger extra review.
   - For "organization/affiliation," write something like **"[Your Name] - Personal Education"**. Meta checks you're not a competitor. A company name they don't recognise means deeper review.
   - For role, use something like "AI developer" or "AI researcher."
4. **Approval timeline:**
   - Seconds/minutes: algorithmic approval if your info looks standard
   - A day or two: quick human review
   - Several weeks: something flagged deeper review (try to avoid this)

### If you can't get approved

It doesn't matter. Use **Qwen** or **DeepSeek** instead — they don't require approval and work just as well. The lecturer uses Llama because it's an industry standard and you'll see it on the job, but it's not required for the course.

### Why Llama 3.1 8B specifically?

Even though it's over a year old, for its size (8 billion parameters) it's still a widely-used industry standard. You'll encounter it in production systems. Worth being familiar with it.

---

## 2. Three Tokenizer Methods (complete set)

```python
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
text = "I am excited to show Tokenizers in action to my LLM engineers"
```

### encode: text → list of token IDs
```python
tokens = tokenizer.encode(text)
# → [128000, 40, 1097, 12304, 311, 1501, ...]
```
61 characters, 12 words → 15 tokens. Roughly matches the 0.75 words-per-token rule of thumb.

### decode: list of token IDs → one string
```python
tokenizer.decode(tokens)
# → "<|begin_of_text|>I am excited to show Tokenizers in action to my LLM engineers"
```
Notice `<|begin_of_text|>` at the start — that's token `128000`, the special "start" token added automatically.

### batch_decode: list of token IDs → list of individual token strings (NEW)
```python
tokenizer.batch_decode(tokens)
# → ["<|begin_of_text|>", "I", " am", " excited", " to", " show", " Token",
#     "izers", " in", " action", " to", " my", " L", "LM", " engineers"]
```

**What batch_decode shows you:**
- Which chunks have a **leading space** (" am", " excited") = beginning of a new word
- Which chunks have **no space** ("izers", "LM") = fragment inside a word
- How the tokenizer split compound words: "Tokenizers" → "Token" + "izers", "LLM" → "L" + "LM"

This is the same observation from the tokenizer page in Week 1 (file 08), now in code.

### Summary table

| Method | Input | Output | Use case |
|---|---|---|---|
| `encode(text)` | A string | List of token IDs | Preparing input for the model |
| `decode(ids)` | List of token IDs | One string | Reading the model's output |
| `batch_decode(ids)` | List of token IDs | List of individual token strings | Inspecting how text was split |

---

## 3. Reinforcement of Earlier Concepts (confirmed in this lecture)

| Concept | Where you learned it | Confirmed here |
|---|---|---|
| Token ID 128000 = special start token | File 34, 37 | Yes, shows up at the start of encode output |
| Leading space = part of the token | File 08 (tokenizer page) | batch_decode shows " am" vs "LM" |
| ~0.75 words per token rule of thumb | File 08 | 12 words → 15 tokens ≈ 0.8 |
| Token vs Token ID (people say "token" for both) | File 37 | Lecturer says "to be pedantic, it's token IDs" |
| Numbers go into the model, not text | File 03, 07, 34 | encode produces numbers, that's what the model receives |
| Ollama named after Llama (the confusion) | New detail | O-llama was an homage to Meta's Llama |

---

## 4. How to Explain This to Someone

### If a non-technical person asks "Why do you need permission to use some AI models?"

"Some AI companies want to make sure their models aren't misused. So they put a gate on it — you fill out a short form saying who you are and what you're using it for, and they approve you. It's like signing a terms-of-use agreement. Most models don't require this; some big ones do."

### If a technical person asks

"Gated models on Hugging Face require ToS acceptance via the model card page. Meta's Llama requires email verification (must match your HF account email) and organizational disclosure. Approval is typically algorithmic for straightforward applications. Non-gated alternatives like Qwen and DeepSeek are functionally equivalent and require no approval. `batch_decode` complements `encode`/`decode` by returning per-token strings, useful for inspecting subword splits and whitespace boundaries."

### The analogy

Gated model = a library that requires a membership card before you can borrow books. Most libraries are open; a few check your ID first. The books inside are the same kind either way.

### The one-liner

"Some models need a terms-of-service agreement on Hugging Face; batch_decode shows you exactly how text was split into tokens."

---

## 5. Self-Check

1. What is a gated model? How do you get access?
2. Two tips to avoid delays when applying for Llama access.
3. What alternatives can you use if Llama isn't approved?
4. What does `batch_decode` return that `decode` doesn't?
5. In the batch_decode output, how do you tell "beginning of word" from "fragment inside a word"?
6. Why is Llama 3.1 8B still used even though it's over a year old?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| Gated model | A model that requires terms-of-service approval before you can download it |
| `batch_decode` | Decodes each token ID separately → a list of individual token strings |
| Llama 3.1 8B | Meta's 8-billion-parameter model, an industry standard for its size |
| Qwen | Alibaba's open-source model family, no approval needed, good alternative to Llama |
| DeepSeek | Chinese lab's open-source model, no approval needed |
| Ollama vs Llama | Ollama = the local runner app (named as an homage). Llama = Meta's model. |

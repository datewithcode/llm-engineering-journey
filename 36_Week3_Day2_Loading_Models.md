# LLM Engineering – Week 3, Day 2 (Part 3)
## Loading Models, Quantization, and Generating Text

> Personal study notes. This completes the full pipeline: dicts → template → tokens → model → output → text.
> Notebook: week3/day2.ipynb (Colab)

---

## READ THIS FIRST (whole lecture in 4 lines)

1. `AutoModelForCausalLM.from_pretrained("model-name")` downloads and loads the actual neural network. "Causal" means it predicts left to right, never peeking ahead.
2. **Quantization** = store parameters with fewer bits (32 → 16 → 8 → 4) to squeeze a model into less GPU memory. Slight quality loss, but it runs on hardware that couldn't hold it otherwise.
3. `model.generate(inputs, max_new_tokens=200)` = THE line. Feed token numbers in, model predicts one token at a time. This is Day 1's autocomplete, running live.
4. The complete pipeline: dicts → `apply_chat_template` → token numbers on GPU → `model.generate` → output numbers → `tokenizer.decode` → readable text.

---

## 1. Loading the Actual Model

```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B",
    device_map="auto"
)
```

### What the name means, word by word

- **Auto** = figure out the right class for this model automatically (same idea as `AutoTokenizer`)
- **Model** = the actual neural network with billions of parameters
- **For** = specialized for
- **Causal** = can only look backward, not forward. When predicting the next word, it sees everything BEFORE that word but nothing after. Like reading left to right with a curtain covering the right side.
- **LM** = Language Model

**"Causal Language Model"** = a model that predicts the next token using only the tokens that came before it. GPT, Llama, Claude — all of them. "Causal" just means "left to right, no peeking ahead."

### `device_map="auto"`

Put the model on the GPU automatically. Without this, it loads on the CPU and runs much slower.

---

## 2. Quantization — Squeezing a Model Into Memory

Llama 3.2 1B has 1 billion parameters. Each parameter is normally stored as a 32-bit number = 4 bytes.

```
1 billion × 4 bytes = 4 GB
```

That fits on the T4 (15GB). But a 7B model at full precision would need 28GB — too big.

**Quantization = store each parameter with fewer bits.** Like rounding 3.14159 to 3.14. Less precise, but takes less space.

| Precision | Bytes per parameter | 7B model size | Quality |
|---|---|---|---|
| 32-bit (full) | 4 | 28 GB | Best |
| 16-bit (half) | 2 | 14 GB | Nearly the same |
| 8-bit | 1 | 7 GB | Slight loss |
| 4-bit | 0.5 | 3.5 GB | More loss, still usable |

### In code

```python
from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(load_in_4bit=True)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B",
    quantization_config=quant_config,
    device_map="auto"
)
```

A model that would need 4GB now fits in ~1GB. Answers are slightly less precise, but it runs on hardware that couldn't hold it otherwise.

---

## 3. Generating Text — THE Line

```python
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
outputs = model.generate(inputs, max_new_tokens=200)
result = tokenizer.decode(outputs[0])
```

### Line by line

1. **`apply_chat_template(messages, return_tensors="pt")`** — converts dicts → string with markers → token numbers as a PyTorch tensor. `.to("cuda")` moves the numbers to the GPU.

2. **`model.generate(inputs, max_new_tokens=200)`** — THE line. Feed token numbers in, model predicts one token at a time (up to 200 new tokens), each one based on everything before it. This is Day 1's autocomplete, running live.

3. **`tokenizer.decode(outputs[0])`** — convert output numbers back to text so you can read them. `[0]` because generate can produce multiple outputs; we take the first.

### Three levels of apply_chat_template (my question, answered)

When you pass `return_tensors="pt"`, it automatically tokenizes. You don't need `tokenize=True` separately — `return_tensors` implies it.

```python
# Level 1: String only (for reading/debugging)
tokenizer.apply_chat_template(messages, tokenize=False)
# → "<|begin_of_text|><|start_header_id|>system..."

# Level 2: Token numbers as a plain Python list (rarely used alone)
tokenizer.apply_chat_template(messages, tokenize=True)
# → [128000, 128006, 9125, ...]

# Level 3: Token numbers as a PyTorch tensor (what you actually use)
tokenizer.apply_chat_template(messages, return_tensors="pt")
# → tensor([128000, 128006, 9125, ...])
```

The model requires PyTorch tensors (a special data format for GPU math), not plain Python lists. `return_tensors="pt"` says "tokenize it AND wrap the result in a PyTorch tensor."

**`"pt"` stands for PyTorch.** (`"tf"` would be TensorFlow. Nearly everyone uses PyTorch.)

In real code, almost always go straight to level 3.

---

## 4. The Complete Pipeline (end to end)

```
Your Python list of dicts
      ↓
apply_chat_template → string with role markers → token numbers (as PyTorch tensor, on GPU)
      ↓
model.generate → predicts next tokens one by one → output token numbers
      ↓
tokenizer.decode → readable text
      ↓
"The answer is 4"
```

That's everything from Week 1 made concrete:
- The tokenizer at the door (apply_chat_template + encode)
- The transformer brain inside (model.generate)
- The tokenizer again at the exit (decode)

---

## 5. How to Explain This to Someone

### If a non-technical person asks "What happened when you ran the model?"

"I typed a question, the computer converted my words into numbers, the AI model processed those numbers to predict the answer one word at a time, then the computer converted the numbers back into words I could read. The whole thing happened on a powerful graphics card in the cloud."

### If a technical person asks

"I loaded a quantized Llama 3.2 1B model using Hugging Face's `AutoModelForCausalLM` with 4-bit quantization via BitsAndBytes. Tokenized the input with `apply_chat_template` to produce PyTorch tensors with model-specific special tokens, moved them to the CUDA device, and ran `model.generate` with a 200-token cap. Decoded the output sequence back to text with the tokenizer. Full local inference on a T4 GPU."

### The analogy
The tokenizer at the door, the transformer brain inside, the tokenizer again at the exit. Quantization = rounding 3.14159 to 3.14 for every parameter so the model fits in less memory.

### The one-liner

"Loading a model and generating text locally is three lines: tokenize the input, run model.generate, decode the output."

---

## 6. Self-Check

1. What does "Causal" mean in `AutoModelForCausalLM`?
2. What does `device_map="auto"` do?
3. What is quantization? Why would you use it?
4. How much memory does a 7B model need at 32-bit vs 4-bit?
5. What are the three lines for generating text? What does each do?
6. Why `return_tensors="pt"` instead of `tokenize=True`? What does "pt" stand for?
7. Draw the complete pipeline from dicts to readable text.

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| `AutoModelForCausalLM` | Auto-loads the right model class for left-to-right text prediction |
| Causal | Left to right only. Can see everything before, nothing after. |
| `from_pretrained("model")` | Download the model from Hugging Face Hub |
| `device_map="auto"` | Put the model on the GPU automatically |
| Quantization | Store parameters with fewer bits to fit in less memory |
| BitsAndBytesConfig | The config object for quantization settings |
| `load_in_4bit=True` | Use 4-bit precision (smallest, most compressed) |
| `return_tensors="pt"` | Return PyTorch tensors (implies tokenization) |
| `.to("cuda")` | Move data to the GPU (CUDA = Nvidia's GPU programming platform) |
| `model.generate` | Feed tokens in, predict new tokens one by one |
| `max_new_tokens` | Cap on how many tokens the model can generate |
| `tokenizer.decode` | Convert output token numbers back to readable text |
| CUDA | Nvidia's platform for running code on GPUs |
| PyTorch tensor | A data format optimized for GPU math (what the model needs) |

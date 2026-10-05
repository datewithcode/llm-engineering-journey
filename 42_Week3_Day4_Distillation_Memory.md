# LLM Engineering – Week 3, Day 4 (Part 1)
## Quantization (the Dimmer Switch), Distillation, and the Model-Loading Setup

> Personal study notes. Rewritten during an accuracy check: an earlier version contained a model list and a CPU-vs-GPU timing that were not from the lecture. This version matches the lecture.
> Notebook: week3/day4 Colab. Companions: file 43 (architecture), file 44 (decoder internals and the model runs).

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **Quantization** = store each parameter with fewer bits (16 or 32 bits → 8 or 4). Like turning a smooth **dimmer switch** into one that clicks between a few settings. It saves a lot of memory and costs only a **little** accuracy.
2. The surprise: lowering precision on **all** parameters hurts far less than **deleting** three-quarters of them, even though it seems like the same loss of information. Nobody fully knows why; it just works experimentally.
3. **NF4** makes 4-bit usable: its 16 values are placed where parameters actually cluster (near zero), not as the integers 0 to 15.
4. The loading recipe: `BitsAndBytesConfig` → tokenizer (set pad token) → `apply_chat_template(..., return_tensors="pt").to("cuda")` → `AutoModelForCausalLM.from_pretrained(...)`. Five models are compared (results in file 44).

---

## 1. Quantization: The Dimmer Switch (the lecturer's explanation)

### What parameters normally look like
Billions of parameters, set during training, each stored as a **16-bit or 32-bit** number. With that many bits, each number can take a huge range of very precise values.

### The dimmer switch analogy
Think of each parameter as a **dimmer switch** for a light.
- **32 or 16 bits:** so many settings the knob turns **smoothly**. Almost any brightness.
- **8 bits:** only **256** settings. The knob starts to click.
- **4 bits:** only **16** settings. Click, click, click. The light can only be one of 16 brightness levels.

**Quantization** = turning every dimmer switch in the network into a clicky one. The name comes from "quantize": making something take only discrete values.

### WHY do it
- **Memory:** going from 16 bits to 4 bits uses **4 times less** memory
- **Simpler calculations**
- Lets a model fit on hardware that couldn't hold it otherwise (like the free T4)

### The objection, and the surprising answer
**Objection:** "If each parameter now carries a quarter of the information, isn't that the same as keeping full precision but throwing away three-quarters of the parameters? Same total information either way."

**Answer:** experimentally, **no**.
| Change | Effect on quality |
|---|---|
| Keep all parameters, reduce precision to 4 bits | Quality drops **a little** |
| Keep full precision, delete 3/4 of the parameters | Quality drops **a lot** |

**Why?** Not fully understood. The best guess: models didn't need so many parameters in the first place, and lower precision happens to be an efficient way to pack the same knowledge into less space. The lecturer calls it "a hack" that "just kind of works."

---

## 2. NF4: Why Not Just Use the Integers 0 to 15?

### The problem
4 bits = 16 possible values. If those were the integers `0, 1, 2 ... 15`, a parameter like `0.0234` would round to `0`. Almost every parameter is a small decimal near zero, so they'd all become `0`. The model would be destroyed.

### The fix: NF4 ("NormalFloat 4")
The 16 slots represent **decimal values** spread across the range where parameters actually live (roughly -1 to +1), placed **densely near zero** and sparsely at the extremes, because parameters follow a **bell curve** (normal distribution).

```
-1.0, -0.70, -0.53, -0.39, -0.28, -0.18, -0.09, 0.0,
 0.08, 0.16, 0.25, 0.34, 0.44, 0.56, 0.72, 1.0
```
Now `0.0234` rounds to `0.0` and `0.1522` rounds to `0.16`. Close enough.

### Parking analogy (the version that clicked)
You have only **16 parking spaces** for a whole street. Most drivers want to park near the shop; almost nobody parks a kilometre away. So you put most spaces near the shop and a few spread out along the rest of the street. NF4 places its 16 values where the parameters actually are.

---

## 3. Distillation (concept referenced in this lecture)

The lecture runs **DeepSeek-R1-Distill-Qwen-1.5B**. The lecturer reminds us that this is DeepSeek's big reasoning model **distilled** into a small Qwen model: "they trained Qwen with data produced by DeepSeek."

### How distillation works
1. A **big teacher model** (DeepSeek R1, very large and expensive to run)
2. A **small student model** (Qwen 1.5B)
3. Train the student on the **teacher's outputs**, not on raw internet text
4. The student learns to imitate the teacher's style and reasoning

### WHY
A small, cheap model that behaves much more like the big one than its size suggests.

**Analogy:** a professor trains an apprentice. The apprentice can't match every bit of the professor's experience but handles most questions the same way, at a fraction of the cost.

| Way to make a model better | Cost |
|---|---|
| Train from scratch | Enormous (only big labs) |
| Fine-tune on your task data | Moderate (Weeks 6-7) |
| Distill from a bigger model | Moderate; produces a small model that imitates a big one |

---

## 4. The Setup Code, Step by Step

### Step 1: Install two libraries
```python
!pip install -q bitsandbytes accelerate
```
| Library | Purpose |
|---|---|
| `bitsandbytes` | Hugging Face's quantization library (the name is a pun on "bits and bytes") |
| `accelerate` | Helps models run efficiently on GPUs |

### Step 2: Log in to Hugging Face
Turn on notebook access for `HF_TOKEN` (the key icon), then `login(hf_token)`. Llama 3.2 may need a separate access request; if not approved, use Llama 3.1 (bigger, slower) or skip Llama.

### Step 3: The quantization config
```python
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)
```
| Setting | What it does |
|---|---|
| `load_in_4bit=True` | Store parameters in 4 bits |
| `bnb_4bit_use_double_quant=True` | Quantize a second time for extra savings (quantization produces some scaling numbers; this compresses those too) |
| `bnb_4bit_compute_dtype=torch.bfloat16` | Storage is 4-bit, but **calculations** happen in 16-bit |
| `bnb_4bit_quant_type="nf4"` | Use the NF4 format (section 2) |

### Step 4: The tokenizer, and the pad-token line
```python
tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token
```
**The pad token:** when several inputs are processed together, shorter ones are filled with a meaningless **pad** token to match lengths. Most tokenizers don't define one, so you set it to the end-of-sequence token. Without this line, you get an error elsewhere. The lecturer wonders why it isn't a default. You'll see it in nearly every script.

### Step 5: Inputs as a tensor on the GPU
```python
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
```
- `return_tensors="pt"` → return a **PyTorch tensor** (a tensor is basically a matrix of numbers)
- `.to("cuda")` → move it onto the GPU (CUDA is Nvidia's GPU technology)

**WHY a tensor, not a Python list?** A GPU needs numbers that are (1) in **one continuous block** so thousands of cores can read them at once, (2) in **GPU memory**, which is separate from your computer's RAM, and (3) all of **one fixed type**. A Python list is none of these. A tensor is all three.

**Analogy:** a Python list is loose papers scattered across desks. A tensor is a bound book on one desk. If 1,000 people must read at once, you need the book.

### Step 6: Load the model
```python
model = AutoModelForCausalLM.from_pretrained(LLAMA, device_map="auto", quantization_config=quant_config)
```
- The model downloads at **full precision** first, then is reduced to 4-bit in memory. So downloads take a while even though the final footprint is small.
- Llama 3.2 1B: about **1 GB** memory footprint after quantization.

---

## 5. "Causal" and "Autoregressive" (the same thing, two names)

**Causal:** the model only sees the past, never the future (cause comes before effect).

**Autoregressive:** "auto" = self. The model feeds **its own output back in** as the next input.
```
Round 1: "The"              → "cat"
Round 2: "The cat"          → "sat"    ← "cat" fed back in
Round 3: "The cat sat"      → "on"     ← "sat" fed back in
```
Two descriptions of one behaviour: causal describes what it can **see**; autoregressive describes what it **does**. Hugging Face uses "causal" in `AutoModelForCausalLM`; papers often say "autoregressive." When people say "LLM" today, this is usually what they mean.

**Contrast:** encoder models (like BERT) see the whole sentence at once and fill in blanks. Not used in this course.

---

## 6. The Five Models Compared

| Model | Size | Notes |
|---|---|---|
| Llama 3.2 1B Instruct | 1B | Meta. Gated (needs approval). |
| Phi-4 mini instruct | about 4B | Microsoft |
| Gemma 3 270M | 270M | Google. Tiny. Couldn't be quantized (PyTorch error), so loaded without it. |
| Qwen 3 4B Instruct | 4B | Alibaba. Recent (July 2025). |
| DeepSeek-R1-Distill-Qwen-1.5B | 1.5B | **Reasoning** model. First reasoning model run through code. |

All are **instruct** variants. The prompt: "Tell a joke for a room of data scientists." Results are in **file 44**.

---

## 7. Freeing GPU Memory Between Models

```python
del model, inputs, tokenizer
import gc
gc.collect()                    # Python garbage collection
import torch
torch.cuda.empty_cache()        # ask the GPU to release cached memory
```
The lecturer's note: sometimes the resource panel doesn't visibly drop even though memory has been freed. If in doubt, **Runtime → Restart session**.

---

## 8. How to Explain This to Someone

### If a non-technical person asks "How do you fit a big AI model on a small computer?"

"Every AI model is billions of numbers. Normally each number is stored very precisely. Quantization stores them less precisely, like a light switch that clicks between 16 brightness levels instead of turning smoothly. It uses about a quarter of the memory, and surprisingly the AI barely gets worse."

### If a technical person asks

"4-bit NF4 quantization via bitsandbytes: weights stored as 4-bit NormalFloat (quantiles of a normal distribution, matching the empirical weight distribution), with double quantization of the scaling constants and bfloat16 compute. It degrades quality far less than pruning an equivalent fraction of parameters, which suggests heavy over-parameterisation. Loading: `BitsAndBytesConfig` passed to `AutoModelForCausalLM.from_pretrained(device_map='auto')`, inputs from `apply_chat_template(return_tensors='pt').to('cuda')`, pad token set to EOS."

### The analogy

A dimmer switch turned into a clicky switch with 16 settings, with those 16 settings placed where you actually use the light most (NF4).

### The one-liner

"Quantization stores every parameter with fewer bits, cutting memory about 4x while losing only a little quality."

---

## 9. Self-Check

1. Explain quantization using the dimmer switch.
2. How many values can 8 bits represent? 4 bits?
3. Why isn't reducing precision the same as deleting 3/4 of the parameters?
4. Why would plain 4-bit integers (0 to 15) destroy a model? How does NF4 fix it?
5. What does DeepSeek-R1-Distill-Qwen-1.5B mean? What is distillation?
6. What do `bitsandbytes` and `accelerate` do?
7. What are the four `BitsAndBytesConfig` settings?
8. Why set `pad_token = eos_token`?
9. Why must inputs be a PyTorch tensor on the GPU?
10. What's the difference between "causal" and "autoregressive"?
11. Which model couldn't be quantized?

---

## 10. Quick Glossary

| Term | Plain meaning |
|---|---|
| Quantization | Storing parameters with fewer bits to save memory |
| Precision | How many bits (and so how many possible values) each number has |
| NF4 | NormalFloat 4: 16 values placed to match the bell-curve spread of parameters |
| Double quantization | Also compressing the scaling numbers that quantization itself creates |
| Compute dtype | The precision used for calculations (bfloat16), separate from storage (4-bit) |
| bitsandbytes | Hugging Face's quantization library |
| accelerate | Library that helps models run efficiently on GPUs |
| Pad token | Filler token used to make batched inputs the same length |
| Tensor | A matrix of numbers in a GPU-friendly format |
| CUDA | Nvidia's GPU technology; `.to("cuda")` moves data onto the GPU |
| Causal / autoregressive | Predicts left to right, feeding its own output back in |
| Distillation | Training a small student model on a big teacher model's outputs |

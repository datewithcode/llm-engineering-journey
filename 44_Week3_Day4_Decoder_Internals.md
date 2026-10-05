# LLM Engineering – Week 3, Day 4 (Parts 3-4)
## Decoder Layer Internals, Non-Linearity, Running Models, and Reasoning Tricks

> Personal study notes. The non-linearity section is the deep concept. The rest is running models.
> Notebook: week3/day4.ipynb (Colab)

---

## READ THIS FIRST (whole lecture in 4 lines)

1. Each of the 16 layers has three parts: **attention** (which words matter?), **MLP** (expand → filter → shrink), and **layer norm** (keep numbers tidy). The decoder layer is the building block of the transformer.
2. The **activation function** (SiLU) is a filter between layers. Without it, 16 layers collapse into 1 and all parameters are wasted. With it, each layer genuinely contributes.
3. **TextStreamer** lets you stream output from HF models token by token, like the API's `stream=True`.
4. Reasoning models use trick words like **"wait"** and **"alternatively"** in their thinking to force self-reflection.

---

## 1. Inside Each Decoder Layer

Each of the 16 `LlamaDecoderLayer` components has three parts:

```
  ┌──────────────────────────────┐
  │  1. ATTENTION                │  "what should I pay attention to?"
  ├──────────────────────────────┤
  │  2. MLP                      │  "process this more deeply"
  ├──────────────────────────────┤
  │  3. LAYER NORM (× 2)         │  "keep the numbers well-behaved"
  └──────────────────────────────┘
```

### Why "decoder only"
Original transformers had encoders AND decoders. Modern LLMs (GPT, Llama, Claude) use **decoder layers only**. You'll see "decoder-only transformer" in papers. Encoders are different (BERT-style), not used in this course.

---

## 2. Attention — Q, K, V, O

### What each letter means

| Letter | Name | What it asks |
|---|---|---|
| **Q** | Query | "What am I looking for?" |
| **K** | Key | "What do I have to offer?" |
| **V** | Value | "Here's my actual information" |
| **O** | Output | "Here's the combined result" |

### Library analogy
You walk into a library with a question (**Query**). Each book has a label (**Key**). You compare your question against labels to find matches. High-scoring matches: you read the book's contents (**Value**). What you take away = **Output**.

### For "the cat sat on the mat because it was tired":
- "it" sends a Query: "I'm a pronoun, what do I refer to?"
- Every word offers a Key. "cat" scores high (subject, alive). "mat" scores low.
- The Values from high-scoring words blend into "it"'s representation.

All four (Q, K, V, O) are learned parameter sets. 2,048 in, 2,048 out.

---

## 3. MLP — Expand, Filter, Shrink

**MLP** = Multi-Layer Perceptron. Standard deep learning, not transformer-specific.

```
2,048 numbers
    ↓  up_proj (expand)
8,192 numbers             ← 4x wider, more room to work
    ↓  gate + activation (filter)
8,192 numbers
    ↓  down_proj (shrink)
2,048 numbers             ← back to original size
```

### Why expand then shrink?
Like spreading papers across a large table to sort them, then filing the result into a slim folder. Expansion gives working space. Shrink keeps the output stackable (must match 2,048 for the next layer).

---

## 4. Layer Norm — Housekeeping

Keeps numbers from growing too large or shrinking to nothing across 16 layers. Without it, values explode or vanish and training breaks. The lecturer's words: "mathematical trickery, not super important." Know it exists, know its purpose, move on.

---

## 5. Non-Linearity: WHY Layers Need a Filter (the key insight)

### The problem

If layers can only MIX (multiply and add), then 16 mixes = 1 mix. Mixing paint 16 times gives you one final colour. You could have mixed it in one go. The 16 steps added nothing.

Mathematical rule: **a linear combination of linear combinations is still just a linear combination.** All billions of parameters collapse into a tiny equivalent. The depth of the network is meaningless.

### The fix

Give each layer one extra power: **the power to throw away.**

Mix, then throw away what's not useful. Mix again, throw away again. Sixteen times.

Now the steps matter. What you throw away at step 2 changes what's available at step 3. You can't do this in one go anymore.

### The throw-away rule (activation function)

**ReLU** (most common, simplest):
```python
def relu(x):
    if x < 0:
        return 0    # throw away
    return x        # keep
```

Negative → zero (discarded). Positive → passes through unchanged.

**SiLU** (what Llama uses): same idea but with a smooth curve instead of a sharp corner. Trains slightly better.

History: sigmoid (1950s-2000s) → ReLU (2010s) → SiLU/GELU (now). Which one matters less than having one.

### In plain words

- ReLU/SiLU = the filter between layers
- Zero = "discarded, ignore this signal"
- Different inputs produce different negatives, so different things get filtered each time
- That's how the same 16 layers handle millions of different questions differently
- **Without filtering, stacking layers is pointless. With filtering, each layer genuinely contributes.**

### Why it was discovered

1950s researchers hit this exact wall: stacking linear operations was pointless. Inspiration came from biological neurons — a neuron either fires or it doesn't, which is inherently non-linear. So they added a threshold function.

---

## 6. The Complete Decoder Layer

```
input: 2,048 numbers
    ↓
LAYER NORM (tidy the numbers)
    ↓
ATTENTION (Q, K, V, O)
    ↓
LAYER NORM (tidy again)
    ↓
MLP: expand to 8,192 → gate + SiLU filter → shrink to 2,048
    ↓
output: 2,048 numbers → goes to the next layer
```

Repeat 16 times. Then the LM head scores every possible next token.

---

## 7. Running Models and Comparing Results

### The generate function

```python
outputs = model.generate(inputs, max_new_tokens=80)
result = tokenizer.decode(outputs[0])
```

He then wraps this into a bigger function with:
- Optional quantization
- Attention mask (to suppress a warning; explained in week 7)
- **TextStreamer** for streaming output

### TextStreamer (NEW)

```python
from transformers import TextStreamer

streamer = TextStreamer(tokenizer)
model.generate(inputs, max_new_tokens=200, streamer=streamer)
```

**Why:** same concept as `stream=True` in the API (file 14/22). Tokens print to screen as they're generated instead of waiting for the full output. You see the model "typing" in real time.

### Quantized layers visible in `print(model)`

When quantization is active, the printed model shows `Linear4bit` instead of `Linear`. That's the 4-bit compression visible in the architecture.

### Models compared (joke-telling)

| Model | Size | Result |
|---|---|---|
| Llama 3.2 1B Instruct | 1B (quantized) | Good panda/pandas pun. **Winner.** |
| Phi-4 (Microsoft) | ~4B (quantized) | Decent joke about data dumping |
| Gemma 3 (Google) | 270M (NOT quantized, too small for it) | Started a joke, never finished. Too tiny. |
| Qwen 3 4B Instruct | 4B (quantized) | Nerdy correlation/p-value joke |
| DeepSeek R1 Distill Qwen 1.5B | 1.5B (quantized, **reasoning**) | Spent 500 tokens agonizing, never told a joke |

**Gemma note:** quantization didn't work with this tiny 270M model (PyTorch error). Had to load without it. Some models are too small to quantize.

---

## 8. Reasoning Model Tricks: "wait" and "alternatively"

DeepSeek R1's thinking output revealed self-reflection tokens:

```
<think>
Okay, I need to come up with a joke...
Hmm, where do I start?
Wait, maybe I should try another angle...
Alternatively, what about statistics humor...
Wait, let me reconsider...
</think>
```

The words **"wait"** and **"alternatively"** are deliberately trained into the reasoning process. They force the model to **pause and self-reflect** rather than rushing to an answer. Same concept as the "Wait" trick from Week 1 Day 3 (budget forcing), now visible in the actual output.

At 1.5B parameters, the model was too small to finish a joke even with 500 reasoning tokens. Reasoning helps quality but needs a minimum model size to be effective.

---

## 9. How to Explain This to Someone

### If a non-technical person asks "What's inside each layer of an AI model?"

"Each layer does two things: it looks at all the words and figures out which ones are connected to each other (attention), then it processes that information and throws away what isn't useful (MLP with a filter). After 16 rounds of this, the model has a very refined understanding of what should come next."

### If a technical person asks

"Each LlamaDecoderLayer has three components: multi-head self-attention (Q/K/V/O projections with rotary position encoding), a gated MLP (up-projection 2048→8192, SiLU activation, down-projection 8192→2048), and RMSNorm layers for stability. The non-linearity in the MLP is critical — without it, the entire depth of the network collapses to a single linear transformation. SiLU is the activation function of choice for Llama; it replaced ReLU for smoother gradient flow during training."

### The analogy

Each layer: mix the signals (attention), then filter out what doesn't matter (activation function). Like a relay race where each runner adjusts the baton slightly, and also drops anything the next runner won't need.

### The one-liner

"Each layer pays attention to what matters, then filters out what doesn't. Stack 16 of them and you get understanding."

---

## 10. Self-Check

1. What three parts does each decoder layer have?
2. What do Q, K, V, O stand for in attention? (Use the library analogy.)
3. What does the MLP do? What's the expand-filter-shrink pattern?
4. Why is non-linearity essential? What happens without it? (One sentence.)
5. What is ReLU? What is SiLU? Which does Llama use?
6. What is TextStreamer and what does it do?
7. What trick words appear in DeepSeek R1's thinking output? What's their purpose?
8. Which model won the joke test? Which was too small to even finish?
9. Why couldn't Gemma be quantized?

---

## 11. Quick Glossary

| Term | Plain meaning |
|---|---|
| Decoder layer | One building block of the transformer: attention + MLP + layer norm |
| Decoder-only | Modern LLMs use only decoder layers, no encoder (unlike original transformer) |
| Q/K/V/O | Query, Key, Value, Output — the four parameter sets in attention |
| MLP | Multi-Layer Perceptron — the expand-filter-shrink processing step |
| up_proj / down_proj | The expansion (2048→8192) and compression (8192→2048) in the MLP |
| Layer norm | Keeps numbers from exploding or vanishing between layers |
| Activation function | The filter (ReLU, SiLU) that makes deep networks meaningful |
| Non-linearity | Any operation that isn't multiply-and-add; breaks linear collapse |
| ReLU | "If negative, make it zero." The classic activation. |
| SiLU | Llama's activation function. Smooth version of ReLU. |
| Linear4bit | What quantized layers show in `print(model)` |
| TextStreamer | HF class that prints tokens as they're generated (streaming) |
| "wait" / "alternatively" | Self-reflection tokens trained into reasoning models to force deeper thinking |
| Attention mask | Tells the model which tokens to attend to; deferred to week 7 |

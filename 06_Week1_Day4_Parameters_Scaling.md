# LLM Engineering – Week 1, Day 4 (Part 3)
## Parameters, Model Sizes, and Two Ways to Scale

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Companions: 04_Week1_Day4_GPT_Transformer.md, 05_Week1_Day4_Transformer_Buzzwords.md

---

## READ THIS FIRST (whole lecture in 4 lines)

1. A **parameter** is a number inside the model that stores learned knowledge. Like a knob: random before training, adjusted automatically during training by the guess-check-nudge loop, fixed afterward. GPT-4 has ~1.76 trillion of them. Nobody sets them by hand.
2. Models come in sizes (Haiku/Sonnet/Opus, nano/mini) because bigger = more parameters = smarter but more expensive. Not every task needs the biggest model.
3. **Training-time scaling** = build a bigger model (more parameters, more data). **Inference-time scaling** = use the same model more cleverly (reasoning, putting better info in the prompt via RAG).
4. Two independent levers. A big model + reasoning + good context beats any one alone.

---

## 1. What Is a Parameter?

Start with the bank credit-score example. Suppose the program is:

```
score = (a × income) + (b × age) − (c × number_of_loans)
```

`a`, `b`, `c` are the **parameters** — the knobs. Before training they're random. After training, maybe `a = 0.5`, `b = 2`, `c = 30`. Those learned numbers *are* the model's knowledge.

**Definition:** a parameter is a number inside the model that gets adjusted during training and stores what the model learned.

- Old-school models: 20–200 knobs.
- A neural network is thousands of tiny programs wired together, each with its own knobs → the count explodes. "Llama has 8 billion parameters" = 8 billion adjustable numbers.
- Everything the model "knows" (Paris is the capital of France, how to write Python, what "it" refers to) is stored as patterns across those numbers. No database of facts inside. Just knobs.

### How does the model know a guess is good or bad?
**The training data already contains the correct answers.**

| income | age | loans | actual score |
|---|---|---|---|
| 50,000 | 30 | 2 | 680 |
| 80,000 | 45 | 0 | 790 |

- Model guesses 400 for the first person. Actual is 680. Gap = 280. That gap is the **error** (or **loss**).
- No judgment — just subtraction: guess minus correct answer.
- Nudge the knobs a tiny bit, guess again, is the gap smaller? Keep whichever direction shrinks the gap. Repeat across all 10,000 people, millions of times. Knobs settle where gaps are smallest. That's **training**.

**For a language model it's even simpler:** the correct answer for "what word comes next?" is just the next word in the text.
- "The cat sat on the ___" → hide the last word. Model guesses "dog." Actual was "mat." Wrong → nudge.
- Do this for trillions of sentences. No human labels anything — the internet labels itself, because every sentence contains its own next word.

**Good or bad = how far the guess is from the real answer already in the data.**

### Are billions of parameters set by themselves?
Yes. Nobody sets them by hand.

**Humans decide:**
- The architecture (how many neurons, how wired — the transformer design)
- How many knobs (8B, 175B...)
- What training data to feed in
- The nudging rule (big gap → nudge more; small gap → nudge less)

**The training process does automatically:**
- Setting the actual value of every knob. Starts random, runs guess → gap → nudge trillions of times on thousands of computers for weeks or months. Knobs drift to where gaps are smallest.

Nobody can say what parameter number 3,482,117,905 "means." No human wrote it. This is part of why emergent intelligence is a mystery: humans built the loop, the loop found the knowledge.

**Mental picture:** humans built the school and the curriculum; the model did the studying.

---

## 2. How Many Parameters, and Why Models Come in Sizes

### The growth

| Model | Parameters |
|---|---|
| Old-school credit model | 20–200 |
| GPT-1 (2018) | 117 million |
| GPT-2 (2019) | 1.5 billion |
| GPT-3 (2020) | 175 billion |
| GPT-4 (2023) | ~1.76 trillion (unconfirmed) |
| GPT-5, Claude, Gemini today | not revealed — probably tens of trillions |

Lecturer at GPT-1: "117 million, we'll never need bigger." Wrong by ~10,000×.

**General rule:** more parameters = more knowledge absorbed = smarter. But more expensive to train, and more expensive to run (every reply calculates through all those numbers).

**Exception:** we've gotten better at packing knowledge into fewer knobs. Gemma's smallest (270M) is smaller than GPT-2 yet far more capable. "More = smarter" is a rule of thumb, not a law.

### Why models come in sizes
- OpenAI: GPT-5 **nano** < **mini** < GPT-5
- Anthropic: **Haiku** < **Sonnet** < **Opus**
- Meta: Llama 3.2 (3B) < Llama 3.1 (8B) < bigger

Same family, different numbers of knobs. Small = cheaper, faster, less smart. Big = expensive, slower, smarter. API price differs by size — you pay for how many numbers get calculated. (Labs don't confirm exact counts, but this is the understanding.)

**In my own words:** Training huge numbers of parameters is expensive, and expensive isn't needed every day. So labs introduced smaller-parameter versions — cheaper, still good answers.

### Two extras
- **Logarithmic scale:** on the lecturer's chart each tick is 10× (1B, 10B, 100B, 1T), not 1, 2, 3, 4. Otherwise small models would be invisible dots next to the giants.
- **Mixture of experts (MoE):** big models like DeepSeek (671B) aren't one giant blob. Inside are many smaller "expert" models; only the relevant ones switch on per question. A 671B model doesn't calculate all 671B every time — cheaper than it looks.

### Open-source sizes mentioned
Llama 3.2 (3B), Llama 3.1 (8B), Llama 3.3, Llama 4 (multiple varieties), gpt-oss (20B and 120B), DeepSeek (671B, MoE).

---

## 3. Two Ways to Make a Model Smarter

**Vocabulary:**
- **Training** = building the model (the knob-nudging loop). Happens once.
- **Inference** = using the model. Every message you send = inference.

### Way 1: Training-time scaling — build a bigger model
More parameters, more training data, more computers, more months. Everything in Section 2. Until ~2 years ago, the only game: bigger is better.

**Chinchilla scaling laws:** parameters should roughly match the amount of training data — a bigger model absorbs more text; a small one can't absorb the whole internet no matter how long you train. Not talked about much now; just know the name.

### Way 2: Inference-time scaling — use the same model more cleverly
Don't change the model. Change what happens when you *run* it. Two tricks I already know:
1. **Reasoning** — write out thinking before answering (Day 3). More tokens at answer time = better answer. The "Wait" trick pushes further.
2. **Put the right information in the input** — the ticket-prices example. Feed it the facts and it draws on them. This is the idea behind **RAG** (later in the course).

Neither touches the knobs. Same model, smarter use.

**Why it matters now:** for years everyone chased Way 1. In the last two years Way 2 took off — first RAG, then reasoning models. They're independent; you can do both. Big model + reasoning + good context beats any one alone.

**In my own words:** Training-time is about working with parameters and adjusting values until it works correctly. Inference-time keeps the model as it is — no updating — and uses external things like RAG or reasoning to make it more powerful.

---

## 4. One-Line Recap

1. A parameter is a knob — a number that stores learned knowledge. Set automatically by training: guess, measure the gap from the known answer, nudge, repeat.
2. Counts grew from millions to trillions. Models come in sizes (Haiku/Sonnet/Opus, nano/mini) because bigger = smarter but more expensive; use the size the task needs.
3. Two independent ways to get more: training-time scaling (bigger model) and inference-time scaling (reasoning, better input/RAG).

---

## How to Explain This to Someone

### If a non-technical person asks "What are parameters?"
"They're the knobs inside the AI. Imagine a machine with 8 billion dials. When you train it, you show it examples and it adjusts the dials until its answers match. After training, those dial positions ARE the knowledge. Nobody sets them by hand — the training process finds them automatically."

### If a technical person asks
"Parameters are the learnable weights in the network — adjusted by gradient descent during training to minimize loss against labeled data. For LLMs, the label is simply the next token in the text, so the internet labels itself. Model size scales from millions (GPT-1) to trillions (GPT-4+). Two orthogonal ways to improve output: training-time scaling (bigger model, more data) and inference-time scaling (reasoning tokens, better context via RAG)."

### The analogy
Knobs on a machine. Training = guess, measure the gap from the right answer, nudge the knobs, repeat billions of times. Humans build the school; the model does the studying.

### The one-liner
"Parameters are billions of learned numbers that store the model's knowledge; you improve results by building a bigger model or using the same model more cleverly."

---

## 5. Self-Check Questions

1. What is a parameter? Give the credit-score formula example.
2. How does training know whether a guess is good or bad? Where does the "correct answer" come from?
3. Why is training a language model easier to label than a credit model?
4. What do humans decide vs. what does training decide automatically?
5. Why do Haiku, Sonnet, and Opus exist? What's the trade-off?
6. Is "more parameters = smarter" always true? Give the counter-example.
7. What is a mixture-of-experts model?
8. Training-time vs. inference-time scaling: one line each, and one example of each.

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| Parameter | An adjustable number inside the model that stores learned knowledge (a knob) |
| Training | The loop that sets the knobs: guess → measure gap → nudge → repeat |
| Error / loss | The gap between the model's guess and the correct answer |
| Inference | Running / using the trained model |
| Training-time scaling | Getting better results by building a bigger model |
| Inference-time scaling | Getting better results from the same model by using it more cleverly (reasoning, better input) |
| Chinchilla scaling laws | Parameters should roughly match training data size |
| RAG | Putting relevant retrieved information into the input (later in course) |
| Logarithmic scale | Each tick is 10× the previous |
| Mixture of experts (MoE) | Many smaller expert models inside one; only relevant ones activate per question |
| Nano / mini, Haiku / Sonnet / Opus | Size tiers of the same model family |

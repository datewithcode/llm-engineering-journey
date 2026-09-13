# LLM Engineering – Week 1, Day 4 (Part 1)
## GPT and the Story of the Transformer

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Status: Attention = partial understanding. The lecturer said he's being hand-wavy on purpose and will show the insides through code over the next 8 weeks. Revisit this file then.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. A neural network is a machine that learns patterns from examples. A **transformer** is a specific way to wire that machine, invented by Google in 2017.
2. The transformer's trick: every word looks at every other word in the sentence and scores which ones matter for understanding it. That's called **attention**. "The cat sat on the mat because **it** was tired" — attention links "it" to "cat" (not "mat") because of "tired."
3. OpenAI used this wiring, made it bigger each year, and that became GPT (Generative Pre-trained Transformer). G = generates text, P = pre-trained on internet data, T = transformer architecture.

*(Attention is marked as partial understanding. The lecturer will show the insides through code over the next 8 weeks.)*

---

## 0. The Whole Lecture in Three Sentences

1. A neural network is a machine that learns patterns from examples.
2. In 2017, Google found a better way to wire that machine so it could read text and learn to *pay attention to the right words*. That wiring is called the **transformer**.
3. OpenAI used that wiring, made it bigger every year, and that became GPT.

*(The first two minutes about the game competition and rankings is just fun — skip.)*

---

## 1. G-P-T

- **G = Generative** — generates text by guessing the next token, over and over (Day 1 idea).
- **P = Pre-trained** — trained once, in advance, on a huge pile of internet data. Built once, then frozen (my Docker-image idea). "Controversially" because much data was scraped without asking.
- **T = Transformer** — the *type of machine* inside GPT, Claude, Gemini, and nearly every modern LLM.

GPT = a text-generating, already-trained machine, built in the transformer style.

---

## 2. The Story in Four Steps

### Step 1: Traditional data science
Bank wants to guess a new customer's credit score. It has 10,000 past customers (age, income, loans, known score). One statistical program finds the pattern and uses it to guess.

- **Training data** = the examples.
- **Parameters** = the knobs inside the program that get adjusted to fit the pattern.
- One program, learning one pattern from examples.

### Step 2: Neural networks (idea from the 1950s)
Instead of one program, connect *lots* of tiny ones, loosely like brain neurons. Each tiny program = an **artificial neuron**. Thousands wired together learn more complicated patterns.

Went in and out of fashion for decades. Breakthroughs were mostly about making them **bigger**: stacking more layers. More layers = "deeper" = **deep learning** / **deep neural network**. Deeper = smarter.

One program → many connected tiny programs → many *stacked* layers.

### Step 3: 2017 — the transformer
How neurons are wired = the **architecture**. Google scientists published **"Attention Is All You Need"** describing a new architecture for text, with a special layer called **self-attention** (see Section 3).

The scientists didn't realise how big it was — they thought it was a nice optimization. (Title follows a joke pattern in papers: "X is all you need.")

Why it was huge: this wiring let networks get much bigger and train on much more data, faster and cheaper. That's why LLMs exist today.

### Step 4: The GPT timeline
Google invented the transformer; a small unknown company, OpenAI, ran with it:
- **2018 GPT-1** — basic
- **2019 GPT-2** — people started noticing
- **2020 GPT-3** — lecturer told his dad "this is huge"; dad: "it's just statistics"
- **2022 ChatGPT** — GPT-3.5 + RLHF (trained on conversations, Day 3). The world went wild
- **2023 GPT-4** — big jump
- **2024 GPT-4o** — multimodal (images, audio)
- **2025 GPT-5**

---

## 3. Attention — what I have so far (revisit later)

### The "it" example
> "The cat sat on the mat because **it** was tired."

Can a mat be tired? No. Can a cat? Yes. So "it" = cat.

Change one word:
> "The cat sat on the mat because **it** was soft."

Now "it" = mat. Same word, meaning flips depending on the surrounding words. "tired" points to cat; "soft" points to mat.

**Attention** = for each word, look at the surrounding words and work out which ones matter for understanding this one.

### It's not just "it" — it's every word
The transformer does this for **every word at the same time**:
- Working on "sat" → "cat" matters (who?), "mat" matters (where?)
- Working on "it" → "tired" and "cat" matter
- "I went to the **bank** to withdraw money" vs. "I sat on the **bank** of the river" — "withdraw money" or "river" decides which bank.

Every word looks at every other word and scores how much each one helps.

### Before vs. after
- **Before:** the machine read one word at a time through a keyhole, keeping only a blurry memory of earlier words. By "it," memory of "cat" was faded. Longer sentence = worse.
- **Transformer:** sees the *whole sentence at once*, laid on a table. Working on "it," it directly looks at every other word and gives each a score: "tired" high, "cat" high, "mat" low. Uses high-scoring words to understand "it." That scoring = attention.

**The entire invention:** see everything at once, and score which words matter for each word.

**In my own words:** The transformer now understands what word we are referring to for which situation. "It" links to "cat" when the sentence says "tired," and to "mat" when it says "soft." Same word, different link, depending on the situation. And that's what understanding language mostly is: knowing what each word refers to, given everything around it.

### Why it changed everything
Seeing everything at once can be done in parallel on many computers → train far bigger machines on far more text. Big machine + huge text = GPT.

---

## 4. The Lecturer's One Opinion

Don't think of the transformer as magic. It's an **efficiency trick**. Without it we'd probably still have reached today's models — just slower, maybe 10–100× more expensive.

Rival architectures exist (state-space models, hybrids). None has beaten the transformer yet, so it remains the standard. But nothing about attention is fundamentally *required* to predict tokens.

---

## How to Explain This to Someone

### If a non-technical person asks "What is a transformer?"
"It's the design of the AI's brain. Before 2017, AI read sentences one word at a time and forgot earlier words. The transformer reads the whole sentence at once and figures out which words are connected to which. Like reading 'the cat sat on the mat because it was tired' and knowing 'it' means the cat, not the mat."

### If a technical person asks
"The transformer is a neural network architecture from Google's 2017 paper 'Attention Is All You Need.' Its key innovation is self-attention: for each token, compute a weighted relevance score against every other token in the sequence, so each position's representation is informed by context. This replaces recurrence, enabling full parallelization across the sequence, which made training on massive datasets tractable. GPT = Generative Pre-trained Transformer."

### The analogy
"The cat sat on the mat because it was tired" → "it" links to "cat." Change "tired" to "soft" → "it" links to "mat." Attention is the mechanism that figures out those links for every word.

### The one-liner
"A transformer is a neural network where every word looks at every other word to figure out what matters — that's what let AI understand language."

---

## 5. Self-Check Questions

1. What do G, P, and T stand for? One line each.
2. What's the difference between traditional data science and a neural network?
3. What does "deep" in deep learning mean?
4. What is an architecture?
5. In "the cat sat on the mat because it was tired," why does "it" mean cat? What if the last word were "soft"?
6. Does attention only work on the word "it"? Explain.
7. What's the before/after difference in how a machine reads a sentence?
8. Why does the lecturer call the transformer an efficiency trick rather than a fundamental discovery?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| Generative | Produces text by guessing the next token |
| Pre-trained | Trained once in advance on huge data, then frozen |
| Transformer | The type of neural-network wiring inside modern LLMs |
| Training data | The examples a model learns from |
| Parameters | The adjustable knobs inside a model |
| Neural network | Many tiny programs (artificial neurons) wired together |
| Deep learning | Neural networks with many stacked layers |
| Architecture | The way neurons are wired together |
| Attention / self-attention | Each word looks at all other words and scores which ones matter |
| "Attention Is All You Need" | The 2017 Google paper that introduced the transformer |
| RLHF | Training on conversations with human ratings (turned GPT-3.5 into ChatGPT) |
| Multimodal | Handles images/audio, not just text (GPT-4o) |
| State-space model | A rival architecture to the transformer |

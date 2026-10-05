# LLM Engineering – Week 3, Day 5 (Part 1)
## Watching Token Prediction Live, logprobs, and Meeting Minutes Preview

> Personal study notes. The visualization is the "aha moment" of the course.
> Code: week3/day5 in Cursor (visualizer), then Colab for the project.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Using **logprobs**, you can see the model's top candidate tokens and their probabilities at each step. "Blue" (99.9%) → "is" (62%) → "the" → "cool" (87%) → ... builds into a poetic sentence, one ordinary prediction at a time.
2. This removes the magic: each step is "given everything so far, what's the most likely next word?" The chain of ordinary predictions produces extraordinary output.
3. The commercial project: audio recording → speech-to-text → open-source LLM → meeting minutes with summary and action items. A real product people sell.

---

## 1. The Token-by-Token Visualization (the key insight)

### What he built

He calls GPT-4.1-mini with the prompt: "In one sentence, describe the color blue to someone who's never been able to see." But instead of just getting the answer, he uses the **logprobs** feature to see the top candidates at each step.

### The results, step by step

| Step | Input so far | Top candidates | Chosen |
|---|---|---|---|
| 1 | (the prompt) | "blue" 99.9%, "imagine" 0.1% | "blue" |
| 2 | "blue ___" | "is" 62%, "feels" 38%, "can" tiny | "is" |
| 3 | "blue is ___" | "the", "a", "like" | "the" |
| 4 | "blue is the ___" | "cool" 87%, "feeling", "calm" | "cool" |
| 5+ | continues... | each step equally predictable | ... |

Final sentence: **"Blue is the cool, calming feeling of a gentle breeze on your skin"**

### Why this matters

At no point did the model "understand" blue or "plan" a poetic sentence. Each step is: "given everything so far, what's the statistically most likely next word?"

- "blue" after a question about blue → of course
- "is" after "blue" → very plausible
- "the" after "blue is" → common
- "cool" after "blue is the" → makes sense

Each prediction is ordinary. The chain of ordinary predictions produces something extraordinary.

### The purpose

**Removes the magic.** You see the machine behind the curtain. "The Wizard of Oz analogy" — when you see the man behind the curtain, the trick loses its sparkle. That's intentional. You should feel: "is that all?" Because it IS all. Statistical prediction, one token at a time.

---

## 2. logprobs — How to See This Yourself

### With the OpenAI API

```python
response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    logprobs=True,          # show probabilities
    top_logprobs=3          # show top 3 candidates at each step
)
```

Each token in the response comes with the top 3 alternatives and their probabilities. You can then visualize this as a chart.

### With Hugging Face

Also possible — the model's output layer (LM head) produces scores for every token. You can access them directly since you have the full model code. The lecturer says reimplementing his visualizer for HF models would be straightforward.

### Why: when you'd use this

| Use case | Why logprobs helps |
|---|---|
| Understanding model behaviour | See WHY it chose a particular word |
| Debugging wrong outputs | See what alternatives it considered |
| Measuring confidence | High probability = confident, low = uncertain |
| Building the visualization | Show the prediction process step by step |

---

## 3. Temperature Connection (reinforcement of file 41)

**Temperature 0:** always pick the highest-probability token at each step. "blue" (99.9%), "is" (62%), "the", "cool" (87%). Same answer every time.

**Higher temperature:** willing to sample lower-probability tokens. Might get "blue feels" (38%) instead of "blue is" (62%). More variety, same mechanism.

The visualization makes temperature concrete: you can SEE which alternatives exist at each step and imagine what would change if the model picked the second or third option instead.

---

## 4. Meeting Minutes Project Preview

### What it does
Takes an audio recording of a meeting → produces written minutes with summary and action items.

### Three steps

```
Audio file (someone recorded a meeting)
      ↓
Step 1: Speech-to-text model (frontier)
      ↓
Text transcript of the meeting
      ↓
Step 2: Open-source LLM (generates the minutes)
      ↓
Meeting minutes with summary + action items
      ↓
Step 3: Stream the output in markdown
```

### Why this matters commercially
Products like Otter.ai, Fireflies.ai, and many others do exactly this and charge subscription fees. It's a real, profitable product. This project is a basic version built in a few hours.

### What's new technically
- **Speech-to-text** — the reverse of text-to-speech from Day 1. A "frontend" model that converts audio → text.
- **Open-source model** for the actual writing — you're using the tokenizer + model code you learned this week.
- **Streaming** — using TextStreamer (file 44) to show the output building live.

---

## 5. How to Explain This to Someone

### If a non-technical person asks "How does AI actually write sentences?"

"One word at a time. It looks at everything written so far and asks: what's the most likely next word? Then it adds that word, asks again, adds the next word, and repeats. It's like the world's most powerful autocomplete. Each individual prediction is simple and obvious. But the chain of predictions produces surprisingly good writing."

### If a technical person asks

"Autoregressive inference: the model produces a probability distribution over the full vocabulary at each step, conditioned on the entire prior sequence. Token selection is typically greedy (argmax) or sampled (with temperature/top-p). The `logprobs` parameter on the API exposes the top-k candidates with their log-probabilities at each position, which you can visualize to see the step-by-step reasoning. There's no lookahead or planning — each token is committed before the next is predicted, yet the conditional dependencies create coherent, expressive output."

### The analogy

The Wizard of Oz. You pull back the curtain and see the man operating the machine. It's less magical but more understandable. The magic of LLMs = a chain of ordinary predictions that produces extraordinary output.

### The one-liner

"Each word is the most likely next word. That's the whole trick. The chain of ordinary predictions produces extraordinary writing."

---

## 6. Self-Check

1. What does `logprobs=True` show you that a normal API call doesn't?
2. Walk through the first four tokens of the "blue" example. What were the alternatives at each step?
3. Why does the chain of ordinary predictions produce something that seems intelligent?
4. How does the visualization make temperature concrete?
5. What are the three steps of the meeting minutes project?
6. What's the difference between speech-to-text and text-to-speech?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| logprobs | API parameter that shows the probability of each chosen token and its alternatives |
| top_logprobs | How many alternative candidates to show at each step |
| Autoregressive inference | Predict one token, add it to input, predict next, repeat |
| Greedy decoding | Always pick the highest-probability token (temperature = 0) |
| Sampling | Pick from the distribution with some randomness (temperature > 0) |
| Speech-to-text (STT) | Convert audio to a written transcript |
| Text-to-speech (TTS) | Convert written text to audio (done in Day 1) |
| Otter.ai / Fireflies.ai | Commercial products that do meeting minutes from audio |

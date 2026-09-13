# LLM Engineering – Week 1, Day 4 (Part 7)
## Context Window and API Costs

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Includes what I saw in Cursor's session info panel.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. **Context window** = how much text the model can read at once, measured in tokens. Like a whiteboard of fixed size. Everything (system prompt, conversation history, documents, AND the reply being generated) must fit on it.
2. Each model has a fixed size: GPT-5 = 400K tokens, Claude = 200K, Gemini = 1M. Too much input → the call fails.
3. API costs: you pay per million tokens, input and output separately. Output includes hidden reasoning tokens. For individual experiments the cost is trivially small; it matters at scale.

---

## 1. Context Window

### The one-sentence answer
**"The context window is how much text the model can read at once, input and output together."**

### The whiteboard picture
The model is a person who can only read from a single whiteboard. Everything it should consider — instructions, the conversation so far, any document, and the answer it's writing — has to be on that whiteboard. The whiteboard has a fixed size. That size is the context window.

- Small whiteboard (old models, ~4,000 tokens): a few pages of chat and it's full. Older text falls off the edge; the model can't see it.
- Big whiteboard (Gemini, 1,000,000 tokens): a whole book fits, and the model can look at any part while answering.

**In my own words:** the whiteboard size = the context window. Every model has a fixed size. Input and output share the one whiteboard.

### What has to fit inside
1. The system prompt
2. Every user message so far
3. Every assistant reply so far (the copied-back history)
4. Anything extra stuffed in (ticket prices, documents, examples, RAG)
5. **The reply currently being generated**

Point 5: the model produces one token at a time. To write "Your name is Ed," it runs four times — input → "Your"; input + "Your" → "name"; and so on. Each generated token is added to the input for the next step, so the output eats into the same window.

### Can I paste 1,000,000 tokens into a 1M model?
Almost. The window is shared between input and output. Fill it entirely with input and there's no room for the reply. In practice ~950,000 input, leaving room for the answer.

### Why it's measured in tokens
Tokens are what the model actually reads. 1,000 tokens ≈ 750 words, so a 200K window ≈ 150,000 words ≈ a long novel.

### Why I care as an engineer
Every call, the whole conversation plus anything added has to fit. Too-long chat or too-big document → the call fails. Fix: pick a model with a bigger window, or trim what you send. All the inference-time tricks (long history, many examples, RAG) spend this budget. Claude Code / Cursor users feel it as the window fills over a long session.

### Sizes today (Vellum leaderboard)
| Model | Context window |
|---|---|
| GPT-5 | 400,000 tokens |
| Claude | 200,000 tokens |
| gpt-oss (open source) | ~130,000 tokens |
| Gemini 2.5 Flash | **1,000,000 tokens** |

Shakespeare's complete works ≈ 1.2M tokens, so only Gemini can nearly swallow all of it in one prompt.

### What I saw in Cursor (proof of all the above)
Session info panel showed: **Context Window: 65.7K / 1M tokens — 7%**, with a breakdown of what's using the space:
- System Instructions 0.9% — the system prompt
- Tool Definitions 0.7% — descriptions of tools it can use (next week)
- Messages 1.3% — my chat so far
- Files 2.8% — day5.ipynb etc.
- Tool Results 0.9% — what came back when it ran tools
- A striped bar **"Reserved for response"** — space kept for the answer (point 5 above)

Other things in the settings:
- **Context Size: 200K or 1M** — you can pick a smaller whiteboard. Bigger = more to read every call = more cost.
- **Thinking Effort: Low / Medium / High / Extra High / Max** — the reasoning-budget dial from Day 3.
- **"Compact Conversation"** button — summarizes old chat into a shorter version to free space. An engineer's trick for living inside the limit.
- Note: "Changing these options mid-session resets the prompt cache and may increase cost" — see caching below.

---

## 2. API Costs (skimmed — lower priority for now)

### Two separate ways to pay
- **Chat products** (ChatGPT, Claude app): monthly subscription, $20–$200. Flat fee, some usage limits. Nothing to do with the API.
- **API**: pay per use, no subscription. What you use when you *build* something. Pays for the electricity of trillions of calculations, plus a bit toward the $100M+ training bill.

### What you pay for
Input tokens and output tokens, priced separately, per million.

| Model | Input (per 1M) | Output (per 1M) |
|---|---|---|
| GPT-5 | $1.25 | $10 |
| GPT-5 nano | $0.05 | $0.40 |

Shakespeare scale: generate all of Shakespeare with GPT-5 ≈ $10; with nano < $1. Output is always pricier than input.

### Two catches
1. **Input includes the whole conversation** — the illusion-of-memory history, RAG documents, everything on the whiteboard. Costs grow as chats get longer. You could send only the last message, but answers get worse. You're paying for the model to look back; that's what you want.
2. **Output includes reasoning tokens** — thinking counts as output even when hidden (OpenAI hides it). Costs can be unpredictable with reasoning on. Cursor's "Thinking Effort" dial is exactly this.

### Reassurance
For everyday experiments ("Hi, my name is Ed" ≈ 10 tokens) you pay a millionth of these numbers. The $5 upfront lasts a long time. Costs only matter at scale (thousands of users) or with agent loops that chew through tokens.

### Caching
Send the same input twice within a few minutes → OpenAI charges less automatically. Claude: depends, more setup. More later.

---

## 3. Where I Am After Day 4 (lecturer's recap)

Can already: call OpenAI and Ollama in code, summarize a web page, compare frontier models.
Now grounded in: transformers, tokens, context windows, API costs, the illusion of memory.
Next: chat completions API, one-shot prompting, streaming, markdown, JSON results, a business solution in a few minutes.

---

## How to Explain This to Someone

### If a non-technical person asks "What's a context window?"
"It's how much text the AI can read at once. Think of a whiteboard — everything the AI needs (your question, the conversation so far, any documents, and its own answer) has to fit on that whiteboard. If it's full, the oldest stuff falls off. Bigger models have bigger whiteboards."

### If a technical person asks
"The context window is the maximum sequence length in tokens the model can attend to in one forward pass. It's shared between input (system prompt, history, documents) and output (generated tokens). GPT-5: 400K, Claude: 200K, Gemini: 1M. Exceeding it fails the request. Inference-time techniques like RAG and multi-shot prompting consume context budget. Cost is per million tokens, output priced higher than input, and reasoning tokens count as output."

### The analogy
A whiteboard of fixed size. Input and output share it. Reserved space for the answer. When it fills, compact the old conversation.

### The one-liner
"The context window is how much text the model can read at once — input and output together, measured in tokens."

---

## 4. Self-Check Questions

1. Define the context window in one sentence.
2. List the five things that must fit inside it.
3. Why does the output eat into the same window?
4. Can a 1M-token model take exactly 1M tokens of input? Why not?
5. Which model has the biggest context window today? Roughly how big is Shakespeare?
6. In Cursor's panel, what did "Reserved for response" and "Compact Conversation" mean?
7. What are the two API-cost catches?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| Context window | The max text (tokens) a model can read at once, input + output |
| Reserved for response | Space in the window kept for the answer being generated |
| Compact conversation | Summarize old chat into fewer tokens to free window space |
| Multi-shot prompting | Putting several example Q&As in the input (uses window space) |
| Input tokens | What you send; priced per million |
| Output tokens | What the model generates, including hidden reasoning; priced per million |
| Prompt caching | Discount for resending the same input soon after |
| Vellum leaderboard | Website comparing models' context windows and prices |

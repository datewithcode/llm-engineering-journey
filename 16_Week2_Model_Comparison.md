# LLM Engineering – Week 2
## Comparing Models: reasoning_effort, Puzzles, and Model Character

> Personal study notes. Mostly a demo to get comfortable with the API, but three
> things here are worth keeping: the scaling demo, the Groq/Grok distinction,
> and the idea that models have character.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **`reasoning_effort`** is a new API parameter: `minimal`, `low`, `medium`, or `high`. Controls how much a reasoning model thinks before answering.
2. **The two-coins puzzle demo** proves both scaling levers: gpt-5-nano on minimal got it wrong; turn up reasoning to low → right (inference-time scaling); OR use gpt-5-mini on minimal → right (training-time scaling). Two independent ways to fix it.
3. **Models have character:** on the prisoner's dilemma, Claude and OpenAI models chose "share" (cooperate); DeepSeek and Grok chose "steal" (defect). Not random, it reflects each lab's training. Consider this when picking a model for a product.
4. **Groq (with a q)** = a hardware company that runs open-source models extremely fast on custom chips. **Grok (with a k)** = xAI's model, Elon Musk. Different things.

---

## 1. `reasoning_effort` — the two scaling axes, made visible

Day 4 taught two independent ways to get better answers. This demo shows both on one puzzle.

**The puzzle:** "You toss two coins, one of them is heads. What's the chance the other is tails? Answer with the probability only."

| Model | reasoning_effort | Answer | Correct? |
|---|---|---|---|
| gpt-5-nano | minimal | one third | No |
| gpt-5-nano | low | **two thirds** | Yes |
| gpt-5-**mini** | minimal | **two thirds** | Yes |

- Rows 1→2: same model, **more thinking** → right answer. **Inference-time scaling.**
- Rows 1→3: same thinking, **bigger model** → right answer. **Training-time scaling.**

Two different levers; either one fixes it. That's the whole point.

### The new parameter
`reasoning_effort` takes `minimal`, `low`, `medium`, or `high` (minimal is new — used to be three). Minimal makes a reasoning model behave almost like a fast chat model, though still slower.

**Parameters seen so far on `chat.completions.create`:** `model`, `messages`, `response_format`, `stream`, `reasoning_effort`.
Same dial as Cursor's "Thinking Effort: Low/Medium/High/Max".

### Why the answer is two thirds
Four equally likely outcomes:

| Coin 1 | Coin 2 |
|---|---|
| H | H |
| H | T |
| T | H |
| T | T |

"One of them is heads" eliminates TT. Three cases remain; in two of them (HT, TH) the other is tails → **2/3**.

The instinct "it's 1/2" comes from hearing it as "the *first* coin is heads," which leaves only HH and HT. The question never says *which* coin.

---

## 2. The Bookworm Puzzle — answer 4mm

**The puzzle:** Two volumes of Pushkin side by side on a shelf, volume 1 then volume 2. The pages of each volume are 2cm thick; each cover is 2mm. A worm gnaws perpendicular to the pages from the first page of volume 1 to the last page of volume 2. What distance did it travel?

**The answer: 4mm.**

Page 1 is at the *front* of a book. On a shelf with spines facing out, the front of the book is on the **right**. So:

```
[Vol 1 back cover ... pages ... front cover][Vol 2 front cover ... pages ... back cover]
                                       ↑    ↑
                        first page of Vol 1  last page of Vol 2
```

They are **touching in the middle**. The worm chews through two covers only: 2mm + 2mm = 4mm. It never touches a single page.

### Results
| Model | Answer |
|---|---|
| GPT-5 | **4mm** (correct, 18 seconds) |
| Gemini 2.5 Pro | **4mm** (correct) |
| Claude Sonnet 4.5 | 8mm (wrong) |
| Grok 4 | didn't finish in several minutes |
| GPT-5-nano | 4.3cm (wrong) |

**Takeaway:** on a single hard problem, frontier models disagree, and the biggest isn't always right. Don't assume "frontier model = correct."

---

## 3. Prisoner's Dilemma — Model Character

**The setup:** You and a partner are in separate rooms. Both share → $1,000 each. You steal + they share → you get $2,000. Both steal → nothing. Game theory says steal.

| Model | Choice |
|---|---|
| Claude Sonnet 4.5 | **Share** |
| gpt-oss 120B (OpenAI open source) | **Share** |
| DeepSeek Reasoner | **Steal** |
| Grok 4 (xAI) | **Steal** |

Anthropic and OpenAI models cooperate; DeepSeek and Grok defect. Not random — it reflects how each lab trained its model. Anthropic is known for heavy focus on alignment and safety, which shows as a cooperative disposition. Grok doesn't always choose steal, but usually does.

**The point:** models have distinguishable *character*, and that's a real factor when choosing one for a product, alongside price and capability.

*(Side note: DeepSeek has two variants — `deepseek-chat` (chat model) and `deepseek-reasoner` (reasoning model).)*

---

## 4. Groq vs Grok — get this straight

- **Grok** (with a **k**) = xAI's **model**. Elon Musk's company.
- **Groq** (with a **q**) = a **company that runs open-source models** on custom hardware. Not a model — a hosting provider.

Groq built specialized chips for LLM inference, so it runs models dramatically faster than normal cloud GPUs. In the demo, gpt-oss 120B (far too big for a laptop) answered almost instantly.

**Why this matters:** it's a third option beyond "big paid API" and "run it locally on Ollama." Large open-source models, fast, without owning hardware. Relevant to JobRadar's week 3–4 cost/quality comparison.

Groq the company predates Grok the model — xAI copied the name, not the other way round.

---

## How to Explain This to Someone

### If a non-technical person asks "Are all AI models the same?"
"No — they have different personalities and strengths. On a puzzle, some get it right and some don't. On a 'cooperate or cheat' game, Claude and OpenAI models chose to cooperate; DeepSeek and Grok chose to cheat. That reflects how each company trained them. Picking the right model for a task is a real skill."

### If a technical person asks
"`reasoning_effort` (minimal/low/medium/high) controls reasoning-token budget on GPT-5 models. The two-coins puzzle demonstrates both scaling axes: nano+minimal fails, nano+low succeeds (inference-time scaling), mini+minimal succeeds (training-time scaling). Frontier models disagree on hard problems — Claude Opus 4.5 got the bookworm puzzle wrong, GPT-5 and Gemini got it right. Model character (cooperative vs competitive on prisoner's dilemma) reflects lab training choices. Groq (q) = hardware inference provider; Grok (k) = xAI's model."

### The analogy
Same question, different models = asking the same question to different people. They have different knowledge, different reasoning styles, and different personalities.

### The one-liner
"Models differ in capability and character; reasoning_effort and model size are two independent ways to get better answers."

---

## 5. Self-Check

1. What are the two ways to get a model to solve a harder problem? Which parameter controls one of them?
2. What values can `reasoning_effort` take?
3. Why is the two-coins answer 2/3 and not 1/2?
4. Why is the bookworm answer 4mm?
5. Which frontier models got the bookworm puzzle wrong? What does that teach?
6. Which labs' models chose share, and which chose steal? Why isn't that random?
7. Groq vs Grok — what is each one?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| `reasoning_effort` | Parameter setting how much a reasoning model thinks: minimal / low / medium / high |
| Training-time scaling | Better answers from a bigger model |
| Inference-time scaling | Better answers from more thinking at run time |
| Groq (q) | Hardware company hosting open-source models at very high speed |
| Grok (k) | xAI's frontier model |
| gpt-oss 120B | OpenAI's large open-source model; too big for a laptop, fine on Groq |
| deepseek-chat / deepseek-reasoner | DeepSeek's chat and reasoning variants |
| Model character | A model's disposition (cooperative, competitive) from how its lab trained it |

# LLM Engineering – Week 4, Day 1
## Which Is the Best LLM? (The Wrong Question, and the Right Strategy)

> Personal study notes. This is a strategy lecture, not a coding one. Every factor here matters when choosing a model for a real project.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **"What's the best LLM?" is the wrong question.** The right question: "What's the best LLM for THIS task, given THESE constraints?"
2. The selection strategy: understand requirements → filter by **basics** (parameters, cost, speed, license) → evaluate with **benchmarks** (coding ability, reasoning, language understanding).
3. This lecture covers the **basics filter**: twelve properties you check before running any benchmarks. They narrow 2 million models to a shortlist of candidates.
4. **Time to market** is a model-selection factor most people forget: bigger/expensive models ship faster (less build work), smaller/cheaper models need more engineering.

---

## 1. The Selection Strategy (three steps)

| Step | What you do | Covered |
|---|---|---|
| 1. Understand requirements | Define what the model must do, what constraints exist | Later |
| 2. Filter by basics | Check properties like cost, size, license → get a shortlist | **This lecture** |
| 3. Evaluate with benchmarks | Compare shortlisted models on relevant performance metrics | Next lectures |

---

## 2. The Basics: Twelve Properties to Check

### Group 1: Model identity (from the model card)

| Property | What it tells you | WHY it matters |
|---|---|---|
| **Open source vs closed source** | Can you see/modify the code, or is it a black-box API? | Open source = more control, cheaper at scale. Closed source = easier to start, better out-of-the-box. |
| **Chat vs reasoning vs hybrid** | How the model approaches problems | Reasoning = better at hard problems but slower, worse at creative content. Chat = fast, natural. Hybrid = adapts. Not always best to pick reasoning. |
| **Release date** | How recent the model is | Newer models usually outperform older ones at the same size. |
| **Knowledge cutoff** | The date training data ends | Anything after this date, the model doesn't know. You'd need RAG or tools to provide that info. |
| **Number of parameters** | Rough indicator of capability | Bigger generally = smarter, but recent small models punch above their weight. Don't overfocus on this. |
| **Training tokens** | How much data was used to train | More data = more knowledge. |
| **Context window** | Max tokens the model can read at once | Everything (system prompt, history, documents, response) must fit. |

**Where to find this info:** the **model card**, published by every provider. Google "[model name] model card" or check Hugging Face.

### Group 2: Practical factors (NOT on the model card)

| Property | What it tells you | WHY it matters |
|---|---|---|
| **API cost** | Price per million tokens (input and output) | Some tasks process millions of tokens daily. Costs add up. |
| **Compute cost** | Cost of running locally (GPU rental, electricity) | "Free" local models still cost compute. Running on your own hardware has a price. |
| **Training cost** | Cost to fine-tune the model for your task | If you plan to fine-tune (weeks 6-7), factor this in. |
| **Build cost / time to market** | How long until your product ships | See below, this is the surprising one. |
| **Rate limits** | How often you can call the API per minute/hour | Some providers cap calls. Higher tiers = higher limits. Even top tiers have limits. |
| **Speed** (tokens/second) | How fast the model generates output | Gemini Flash, GPT-5-nano, GPT-4.1-nano are fast. Matters for user-facing apps. |
| **Latency** (time to first token) | How long before the first word appears | Reasoning models think before responding, so latency is high. Matters for streaming UIs. |
| **License** | What you're legally allowed to do with the model | Some are fully permissive. Some have revenue caps. Some require agreements (Meta). Get lawyers involved for commercial use. |

---

## 3. The Surprising Factor: Time to Market

Most people compare models on quality and cost. They forget **how long it takes to ship a product**.

| Model choice | Runtime cost | Build effort | Time to ship |
|---|---|---|---|
| GPT-5 / Claude (big frontier) | Expensive per call | Low (it just works out of the box) | Fast (days/weeks) |
| Small open-source model | Cheap per call | High (need to fine-tune, optimize, engineer prompts) | Slow (weeks/months) |

**The trade-off:** a big expensive model might cost more per call but gets you to market in days. A small cheap model saves on runtime but takes months of engineering to match the quality.

**WHY this matters:** often the right first move is to use a big model to ship fast, then gradually migrate to a smaller cheaper model once you have revenue and data. Starting with the cheapest model is an optimization trap that delays your launch.

---

## 4. Speed vs Latency (they're different)

| | Speed | Latency |
|---|---|---|
| What it measures | Tokens generated per second (overall throughput) | Time until the FIRST token appears |
| What affects it | Model size, hardware, quantization | Reasoning (model "thinks" before responding) |
| Why it matters | How fast the full answer appears | How long the user stares at a blank screen |
| Example | GPT-5-nano: fast. GPT-5 with high reasoning: slow. | A reasoning model might take 10 seconds of silence before the first word streams. |

For a chat UI, **latency matters more than speed**. Users tolerate slow typing (streaming) better than long silence (waiting for the first word).

---

## 5. Chinchilla Scaling Law (theory, less prominent now)

### The rule

**Double the parameters → need double the training data** (and vice versa). Parameters and training data must scale together.

Named after Google DeepMind's model "Chinchilla" (which came after "Gopher").

### WHY: what happens if you don't scale together

| Scenario | Result |
|---|---|
| Double parameters, same data | Extra parameters wasted. Nothing new to learn from. Model isn't much better. |
| Same parameters, double data | Model can't absorb it. Diminishing returns. "Stuck" halfway through training. |
| Double both | Model improves proportionally. The scaling law holds. |

### The "stuck" signal

If you're training and the model stops improving halfway through your data, the model has absorbed all it can at this size. You need more parameters to absorb the remaining data.

### WHY it's less emphasized now (two reasons)

1. **Better compression.** Techniques like pruning, distillation, and better architectures squeeze more knowledge into fewer parameters. Llama 3.2 (small) is very capable. Gemma 3 at 270M is far better than early GPT models at the same size. The "double data for double parameters" rule isn't as rigid as it seemed.

2. **Inference-time scaling.** Chinchilla is about training-time scaling only. Now we know inference-time techniques (reasoning, RAG, better prompts) improve output without touching training at all. Training isn't the only lever anymore.

### Connection to week 1

You learned two scaling axes: training-time (bigger model, more data) and inference-time (reasoning, RAG, better prompts). Chinchilla is about axis 1 only. It's less dominant now because axis 2 turned out to be equally powerful.

### Practical takeaway

Still a useful rule of thumb: if you're comparing two models with the same architecture, the one trained on proportionally more data for its size will likely perform better. But don't use it as a hard law.

---

## 7. How to Explain This to Someone

### If a non-technical person asks "Which AI is the best?"

"There's no 'best.' It's like asking 'what's the best car?' It depends: commuting? A sedan. Off-roading? A truck. Racing? A sports car. Same with AI: fast and cheap? One model. Super accurate? Another. Good at code? Another. You pick based on what you need, what you can afford, and how fast you need to ship."

### If a technical person asks

"Model selection is multi-criteria: start by filtering on hard constraints (context window, license, rate limits, cost ceiling), then evaluate the candidate set against task-specific benchmarks (MMLU for general knowledge, HumanEval for code, GSM8K for math). Don't neglect time-to-market: a frontier model via API ships in days; a fine-tuned open-source model might take months to reach parity but saves at scale. Also consider speed vs latency separately, especially for reasoning models where TTFT can be 10x higher than chat models."

### The analogy

Choosing a model is like choosing a car. You don't ask "what's the best car?" You ask "what do I need it for, what's my budget, and when do I need it?"

### The one-liner

"There's no best LLM. There's only the best LLM for your task, budget, and timeline."

---

## 6. Self-Check

1. Why is "what's the best LLM?" the wrong question?
2. What are the three steps of the model selection strategy?
3. Name five basic properties you'd check from the model card.
4. Name four practical factors NOT on the model card.
5. What's the difference between speed and latency? Which matters more for a chat UI?
6. Why might a big expensive model be the right first choice even if it costs more per call?
7. What is a model card? Where do you find it?
8. Why do licenses matter for open-source models?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| Model card | A published document describing a model's properties (size, cutoff, benchmarks) |
| Knowledge cutoff | The date training data ends; the model knows nothing after this |
| Rate limit | Max number of API calls allowed per time period |
| Speed (tokens/sec) | How fast the model generates text overall |
| Latency / TTFT | Time to first token; how long before the first word appears |
| License | Legal terms for using the model (permissive, restrictive, revenue-capped) |
| Time to market | How long until your product ships; affected by model choice |
| Candidate set | The shortlist of models that pass the basics filter |
| Benchmarks | Standardized tests that measure model performance (next lecture) |
| Leaderboard | A table ranking models by benchmark scores |
| Arena | A platform where models compete head-to-head |
| Hybrid model | Can switch between chat mode and reasoning mode depending on the task |

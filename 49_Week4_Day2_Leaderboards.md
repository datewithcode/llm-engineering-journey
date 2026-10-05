# LLM Engineering – Week 4, Day 2 (Part 1)
## Five Leaderboards and Where the Gains Are Really Coming From

> Personal study notes. Bookmark the leaderboards, don't memorize the rankings (they change monthly).
> The training-time vs inference-time observation is the insight worth holding.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. Five leaderboards to know: **Artificial Analysis** (best overall), **Vellum** (costs and context windows), **SEAL/Scale** (specialized expert benchmarks), **Hugging Face** (many leaderboards, old main one retired), **LiveBench** (anti-contamination focus).
2. The **Intelligence Index** on Artificial Analysis combines 10 benchmarks (GPQA, MMLU Pro, HLE, AIME, LiveCodeBench, etc.) into one score. Check it for the current standings, not what the lecturer says.
3. The first **open-source** model to appear among the top frontier models: GPT-OSS 120B (from OpenAI). Significant milestone.
4. **Key insight:** the performance timeline looks steep, but recent gains are mostly from **inference-time techniques** (reasoning, tools, RAG), NOT training-time improvements. Without inference-time tricks, the curve would be flattening.

---

## 1. Five Leaderboards to Bookmark

| Leaderboard | What it's best for | WHY to use it |
|---|---|---|
| **Artificial Analysis** | Overall comparison: intelligence, speed, price | The lecturer's favourite. Clear charts. Combines 10 benchmarks into one Intelligence Index. Start here. |
| **Vellum** | API costs and context windows side by side | One page showing every major model's pricing and context window. Useful for the "basics filter" from Day 1. |
| **SEAL (Scale)** | Expert, specialized benchmarks | Deep, narrow evaluations. Good for specific domains (coding, math, reasoning). Partly owned by Meta. |
| **Hugging Face** | Many community leaderboards | The old "Open LLM Leaderboard" was retired (people were gaming it). Many others exist as Spaces. Browse but don't rely on one. |
| **LiveBench** | Anti-contamination evaluations | Specifically designed to prevent training-data contamination. Rotates questions. If you're worried about inflated scores, check here. |

### WHY the old HF leaderboard was retired
People were **gaming it** — training models specifically to score well on its benchmarks, inflating scores without real improvement. Another example of the overfitting limitation from Day 1.

---

## 2. The Intelligence Index (Artificial Analysis)

### What it is
A single score combining 10 different benchmarks:
- MMLU Pro (general knowledge)
- GPQA (science)
- HLE (superhuman questions)
- AIME (math)
- LiveCodeBench (coding)
- And 5 others

Weighted slightly toward coding/agentic tasks.

### Current top models (as of the lecturer's recording, WILL be outdated — check the site)

| Rank | Model | Type | Notable |
|---|---|---|---|
| 1 | GPT-5 Codex | Closed, coding-optimized | Optimized for agentic coding |
| 2 | GPT-5 (high reasoning) | Closed, reasoning | Nearly tied with Codex |
| 3 | Grok 4 | Closed (xAI) | Was #1 before GPT-5 |
| 4 | Claude 4.5 Sonnet | Closed (Anthropic) | Very high but slightly behind |
| 5 | Grok 4 (fast mode) | Closed (xAI) | Speed variant |
| 6 | Gemini 2.5 Pro | Closed (Google) | Was #1 when it launched |
| ~8 | **GPT-OSS 120B** | **Open source** (OpenAI) | **First open-source model among the top. Fast and cheap.** |
| ~9 | Qwen 3 | Open source (Alibaba) | Strong open-source contender |
| ~10 | DeepSeek V3.2 | Open source (DeepSeek) | Still experimental at time of recording |

**The pattern:** each new release briefly takes #1, then gets overtaken. Gemini → Grok → GPT-5. The rankings are a snapshot, not permanent. What matters is checking the leaderboard when YOU need to make a decision.

---

## 3. The Timeline Chart (the important insight)

Artificial Analysis has a chart showing model performance over time, from November 2022 (ChatGPT launch) to now.

**What it looks like:** a steep, continuous upward line. No sign of slowing down.

**But the lecturer's observation changes the picture:**

| Period | Where the gains came from |
|---|---|
| 2022-2024 | Mostly **training-time** scaling (bigger models, more data, better architectures) |
| 2024-now | Mostly **inference-time** techniques (reasoning, tools, RAG, prompt engineering) |

**If you removed inference-time gains:** the curve would be **flattening**. Training-time improvements are hitting diminishing returns. The steep trajectory continues because labs are getting better at using the SAME model more cleverly.

**WHY this matters for you as an engineer:**
- Training a better base model = the lab's job (costs $100M+, takes months)
- Using the model more cleverly = YOUR job (reasoning prompts, RAG, tools, fine-tuning)
- The second lever is where most of the recent improvement comes from
- That's exactly what this course teaches you (weeks 5-8)

**Connection to Week 1:** the two scaling axes. Axis 1 (training-time) is flattening. Axis 2 (inference-time) is accelerating. The course is primarily about axis 2.

---

## 4. How to Explain This to Someone

### If a non-technical person asks "Which AI is winning right now?"

"The rankings change every month. Right now OpenAI and Anthropic trade the top spot. But the more interesting thing is WHERE the improvement comes from. Building bigger models (like building a bigger engine) is hitting limits. The recent gains are from using the same model more cleverly, like a driver learning better racing lines with the same car. That's what AI engineers focus on."

### If a technical person asks

"The Artificial Analysis Intelligence Index aggregates 10 benchmarks (MMLU Pro, GPQA, HLE, AIME, LiveCodeBench, etc.) into a composite score. Current leaders: GPT-5 Codex, GPT-5 high, Grok 4, Claude 4.5 Sonnet, Gemini 2.5 Pro. First open-source entrant in the top tier: GPT-OSS 120B. The performance timeline's steep trajectory is misleading — decompose it and you see training-time gains plateauing while inference-time techniques (CoT reasoning, tool use, RAG) drive most recent improvements. Vellum is useful for API pricing comparisons, LiveBench for contamination-resistant evaluation."

### The analogy

A car race leaderboard. The rankings change every season. But the big story isn't who's #1 today — it's that cars stopped getting faster engines (training) and started winning through better driving (inference techniques). The driver (you, the engineer) matters more than ever.

### The one-liner

"Check Artificial Analysis for current rankings, but know that recent gains are from inference-time techniques — and that's what you're learning to do."

---

## 5. Self-Check

1. Name the five leaderboards and what each is best for.
2. Why was the old Hugging Face Open LLM Leaderboard retired?
3. What does the Intelligence Index combine?
4. What's significant about GPT-OSS 120B appearing in the top rankings?
5. The performance timeline looks steep. Where are the recent gains really coming from?
6. Why does the training-time vs inference-time distinction matter for your career?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| Artificial Analysis | The lecturer's favourite leaderboard. Combines 10 benchmarks into an Intelligence Index. |
| Vellum | Leaderboard focused on API costs and context windows side by side |
| SEAL (Scale) | Expert, specialized benchmark leaderboards from Scale AI |
| LiveBench | Leaderboard focused on preventing training-data contamination |
| Intelligence Index | Composite score from 10 benchmarks on Artificial Analysis |
| GPT-OSS | OpenAI's open-source model family (20B and 120B variants) |
| Gaming a benchmark | Training specifically to score well, inflating scores without real improvement |
| Inference-time techniques | Reasoning, RAG, tools, prompt engineering — using the same model more cleverly |
| Training-time techniques | Building a bigger model with more data — the lab's job |

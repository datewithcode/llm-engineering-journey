# LLM Engineering – Week 2 (Bonus)
## SVG Drawing Challenge: Comparing Models Visually

> Personal study notes. A fun bonus, not a core lecture. One insight worth keeping.

---

## READ THIS FIRST (the bonus in 3 lines)

1. He asked 8 different models to draw a "panda rollerblading to work" — not as an image, but as an **SVG** (text that describes shapes and lines). This tests the model's spatial reasoning, not image generation.
2. Used **OpenRouter** to call all models through one API key. Results ranged from basic to impressive. Gemini 3 Pro won. GPT-5-nano failed.
3. This previews **week 4**: picking the right model for a task. Different models have different strengths.

---

## 1. SVG Generation vs Image Generation — the one insight

**Image generation** (DALL-E, Midjourney): uses a special diffusion model trained on millions of images. A different kind of AI, purpose-built for pictures.

**SVG generation**: an SVG is just text — XML instructions like "draw a circle at 100,200 with radius 50, fill it black." Asking a *text* model to write SVG forces it to **think through how to construct a picture from shapes and lines, step by step, as text.**

That's a test of spatial reasoning and planning, not image training. The model has to understand what a panda looks like, what rollerblades look like, and figure out how to express both using only geometric instructions.

---

## 2. The Models Tested

All called through OpenRouter, one after another (could be made async for parallel execution):

| Model | Type | Result |
|---|---|---|
| gpt-oss 120B | Open source (OpenAI) | Good — nice rollerblades |
| GPT-5-nano (low reasoning) | Frontier, smallest | Failed — couldn't generate |
| DeepSeek 3.2 | Open source (China) | Decent — big diagram |
| Kimi K2 (Moonshot AI) | Open source, strongest at time | Interesting interpretation |
| Grok 4.1 Fast (xAI) | Frontier | Fun — "WORK" written assertively |
| Claude Opus 4.5 (Anthropic) | Frontier, largest | Impressive — action lines, "OFFICE" label |
| GPT-5.2 (high reasoning) | Frontier, strongest OpenAI | Great — swirly action lines |
| Gemini 3 Pro (Google) | Frontier, strongest Google | **Winner** — flailing rollerblades, best overall |

**Takeaway:** model size and reasoning ability roughly correlate with SVG quality, but not perfectly. The smallest model failed; the biggest competed closely. Worth experimenting with your own challenge.

---

## 3. How to Try It Yourself

1. Pick a challenge: "a cat skateboarding," "a robot cooking," anything visual but not too complex
2. Prompt: "Generate an SVG of [challenge]. Respond with the SVG only."
3. Call through OpenRouter (one API key for all models)
4. Compare results — a fun way to get a feel for model differences before week 4's systematic approach

---

## 4. Connection to the Course

- **Week 4** will cover model selection scientifically — benchmarks, leaderboards, cost-quality tradeoffs
- **OpenRouter** makes comparison easy: swap `model="provider/model"` and test
- For **JobRadar**: similar approach when comparing which model extracts job postings most accurately (week 4)

---

## How to Explain This to Someone

### If a non-technical person asks "How do you compare AI models?"
"One fun way: ask them all to draw the same picture using only text instructions — like 'draw a circle here, a line there.' It's not about art; it's about whether the AI can think through how to build a picture step by step. Some models did great, some couldn't manage it. It shows they're genuinely different."

### If a technical person asks
"SVG generation as a benchmark: unlike diffusion-based image generation, this tests a text model's spatial reasoning and planning — it must serialize a visual concept as XML draw commands. Called 8 models via OpenRouter with the same prompt. Results correlated roughly with model scale and reasoning capability (Gemini 3 Pro best, GPT-5-nano failed). Previews week 4's systematic model selection."

### The analogy
Asking a writer to describe a painting so precisely that someone else could reproduce it — tests understanding, not painting skill.

### The one-liner
"Asking models to write SVG tests their reasoning, not their image training — a quick way to feel model differences."

---

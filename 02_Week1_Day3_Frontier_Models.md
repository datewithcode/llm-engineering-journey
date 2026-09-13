# LLM Engineering – Week 1, Day 3 (Part 2)
## Frontier Models: The Players, What They're Great At, Where They Go Wrong

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Companion to: 01_Week1_Day3_LLM_Types.md (base / chat / reasoning models).

---

## READ THIS FIRST (whole lecture in 5 lines)

1. Each big lab (OpenAI, Anthropic, Google, xAI, DeepSeek) builds its own model from scratch. Smaller companies build on open-source ones.
2. Models are great at: summarizing big content, expanding short requests into big output, writing code, fixing code.
3. **Knowledge cutoff:** the model is frozen at training time (like a Docker image). Confidently wrong about anything after.
4. **Hallucination:** the model guesses believable-sounding text, not truth. Wrong answers sound just as confident as right ones.
5. **Jumps to conclusions:** fixes the nearest symptom instead of stepping back (the wrong-key story). So supervise it like a junior employee.

Everything below gives the detail and the examples.

---

## 1. The Players — Lab vs. Model vs. Chat Product

**Three words that get mixed up. Think of cars:**

- **The lab** = the car company (e.g. Toyota). The company doing the work.
- **The model** = the engine. The actual AI that does the next-word guessing.
- **The chat product** = the finished car you sit in. A website/app wrapped around the engine so you can use it easily.

**In my own words:** The lab is the company; the model is the core thing that gets better with each new version; the product is what the lab builds so you can use the model easily.

| Lab (company) | Model (engine) | Chat product (what you open) |
|---|---|---|
| OpenAI | GPT-5 (hybrid), GPT-4.1 (pure chat, faster), "o" series (pure reasoning) | ChatGPT |
| Anthropic | Claude — 3 sizes: Haiku (small), Sonnet (medium), Opus (large) | Claude |
| Google | Gemini | Gemini |
| xAI (Elon Musk) | Grok | Grok |
| DeepSeek (China) | DeepSeek | DeepSeek |

**Extra vocabulary:**
- **Frontier model** = the most advanced models from these labs.
- **Foundation model** = roughly the same thing; used interchangeably. Strictly, a "foundation" is the base others build on.
- **Open source** = the lab gives the model away for free so you can download and run it yourself (like Ollama on Day 1).
  - **DeepSeek is the odd one out**: it open-sourced everything, including its biggest model.
  - OpenAI released one open-source model (gpt-oss), probably provoked by DeepSeek.

**Note connecting to Part 1:** The lecturer still likes GPT-4.1 because it's a pure chat model — faster than GPT-5 even on lowest reasoning. Chat models win on speed.

### Do labs share a base model?
**No.** Each big lab (OpenAI, Anthropic, Google, xAI, DeepSeek) collects its own data and trains its own base model from scratch. GPT and Claude are completely separate engines. Training from scratch costs hundreds of millions of dollars, so only a few companies can do it.

**Everyone else** (smaller companies) takes an open-source model (Llama, DeepSeek, gpt-oss) and builds on top of it with their own training. That's what "foundation model" means — a base others build on. Later in the course I'll do this myself.

---

## 2. What Frontier Models Are Great At

Four things, in everyday terms:

1. **Give it a lot, get back a little** — paste a long article, ask "summarize in 5 lines." (Lecture word: *synthesizing*.) My Day 2 web-page summarizer did this.
2. **Give it a little, get back a lot** — "write an email asking for leave" → full email. "Plan to learn Python in 3 months" → full plan. (Lecture word: *generating content*.) Lecturer uses this to kick off new projects and bounce ideas.
3. **Write code** — "write a Python program that adds two numbers" → done.
4. **Fix code** — paste broken code, ask why → it finds the bug and explains the fix. Can loop: write → test → fix → write more.

**In my own words:** Summarize big content into few key ideas, or expand a short request into a big result; generate code and fix code.

**Side note:** Stack Overflow (website where programmers posted questions and waited for humans to answer) is dying — people ask ChatGPT/Claude instead and get instant answers.

---

## 3. Where They Go Wrong (the important part)

### Weakness 1: Knowledge Cutoff

- A model reads its training data **once**, then stops. The stop date = **knowledge cutoff**.
- **Analogy:** A person reads every newspaper up to Dec 2024, then goes into a cave with no phone. Ask about 2025 → they don't know, and may confidently say "that doesn't exist."
- **My analogy:** A model is like a Docker image — frozen at build time. It works up to where it was trained; anything after that, it will confidently give a wrong answer.
- **Lecturer's real example:** Gemini "fixes" his code by deleting `GPT-4.1` (released after Gemini's cutoff), insisting it doesn't exist, and replacing it with a two-year-old model. Confidently, even angrily.
- **"But ChatGPT can search the web?"** Yes — but that is **extra code** engineers wrote around the model, not the model itself. The model is still in the cave; someone passes newspapers through the door. Building this kind of thing is part of being an AI engineer.

### Weakness 2: Hallucination — confident mistakes

- Back to the core idea: the model guesses the most likely next word. It is **not** checking if the words are true. It was trained to produce text that *sounds right* (lecture word: **plausible**).
- Surprising part: usually the most believable-sounding words *are* the truth (true things appear more in training data), so models are right most of the time. We should almost be surprised they aren't wrong more often.
- Sometimes the believable answer is simply wrong. The model doesn't know. It writes the wrong answer in the **same confident tone** as a right one. That's a **hallucination**.
- Example: ask for a book on a topic → it may invent title, author, year that sound real and don't exist.
- **Why dangerous:** a human expert who's unsure *sounds* unsure. A model never does. You can't judge by tone — you have to check.

**In my own words:** Hallucination is giving a response that may not be true, but the model believes it's correct — there's no way for it to know if the next predicted word is true or not.

### Weakness 3: Jumping to conclusions — the student's story

**Everyday version (the wrong key):**
Your car key won't turn. You call a mechanic. He says "the lock doesn't accept this key — I'll rebuild the whole lock" and spends three hours on it. Real problem: you picked up your neighbour's keys. Real fix: use the right key, ten seconds. The mechanic correctly saw "key and lock don't match" but fixed the wrong side and never asked "is this the right key?"

**The real story, step by step:**
1. A student wanted to chat with an open-source model. You do that by typing the model's name in code.
2. The model has two similarly named versions — chat and base. The student typed the **base** one by mistake. *(Wrong key.)*
3. Their code sent chat messages (system prompt, user prompt) to the base model. Base models weren't trained on conversations → error. *(Key doesn't turn.)*
4. The student asked an LLM to fix it. *(Called the mechanic.)*
5. The LLM saw "this model doesn't understand chat messages" and decided to write pages of complicated code to *teach* the base model to be a chat model. *(Rebuilding the lock.)*
6. The real fix: change one word — the model name — to the chat version. *(Use the right key.)*

**Why the student didn't catch it:** they were new. Couldn't tell "complicated code that's needed" from "complicated code that's a waste." It looked like progress, so they trusted it. When it broke, they had pages of code they didn't understand.

**Lecture phrase:** the LLM applied a **Band-Aid** — fixed the nearest symptom and pushed forward instead of stepping back to find the root cause.

**In my own words:** It's about being aware of which key needs to be used, instead of implementing everything from scratch.

---

## 4. The Big Lesson — The Junior Analyst

Treat an LLM like a **tireless junior employee**:
- Very hard-working, produces lots of output fast.
- But it's **your job** to check the work, keep it on track, and challenge it when it wanders off.
- LLMs perform best **under supervision**.

**Surprising twist:** people expected LLMs to help beginners the most. Actually they help **seniors** most — a senior can spot when the LLM goes wrong. A beginner can't, so the LLM can lead them astray.

Someone in the loop has to know enough to ask "wait, are we even using the right key?" — that's the supervisor's job, and that's me.

---

## 5. One-Line Recap

1. **Players** — lab → model → product. Each lab builds its own model; small companies build on open-source ones. DeepSeek open-sourced everything.
2. **Strengths** — shrink big content, expand small requests, write code, fix code.
3. **Knowledge cutoff** — frozen like a Docker image; confidently wrong about anything after. Web search is extra code, not the model.
4. **Hallucination** — believable-sounding guesses with no truth check; wrong answers sound as confident as right ones.
5. **Jumps to conclusions** — fixes the nearest symptom instead of stepping back (wrong-key story). So supervise it like a junior employee.

---

## How to Explain This to Someone

### If a non-technical person asks "Who makes these AI models and what are they bad at?"
"A handful of companies build them: OpenAI makes ChatGPT, Anthropic makes Claude, Google makes Gemini. They're great at summarizing, writing, and coding. But they have three big weaknesses: they only know things up to a certain date, they sometimes make up facts and say them confidently, and they tend to fix the nearest problem instead of finding the real cause. So you have to check their work."

### If a technical person asks
"The frontier labs are OpenAI, Anthropic, Google, xAI, and DeepSeek — each trains its own foundation model from scratch. Key limitations: knowledge cutoff (training data is frozen at a point in time), hallucination (the model optimizes for plausibility, not truth, so wrong answers sound identical to right ones), and a tendency toward local fixes rather than root-cause analysis. LLMs perform best under supervision by someone who can catch these failures."

### The analogy
Knowledge cutoff = a Docker image, frozen at build time. Hallucination = confident-sounding text with no truth check. Jumping to conclusions = a mechanic rebuilding the lock when you brought the wrong key.

### The one-liner
"Frontier models are built by five big labs, excel at language tasks, but are frozen in time, sometimes confidently wrong, and need a supervisor."

---

## 6. Self-Check Questions

1. What's the difference between a lab, a model, and a chat product? Give one example of each.
2. Which lab is the odd one out and why?
3. Do OpenAI and Anthropic share a base model? Who *does* build on someone else's model?
4. Name the four strengths in everyday terms.
5. What is a knowledge cutoff? Why doesn't web search in ChatGPT fix it?
6. What is a hallucination? Why is it dangerous?
7. Tell the wrong-key story in three sentences. What was the real fix?
8. Why do LLMs help senior developers more than beginners?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| Lab | The company building the AI (OpenAI, Anthropic, Google, xAI, DeepSeek) |
| Model | The engine — the AI that guesses next words (GPT, Claude, Gemini, Grok, DeepSeek) |
| Chat product | The app/website wrapped around the model (ChatGPT, Claude, Gemini, Grok, DeepSeek) |
| Frontier model | The most advanced models from the big labs |
| Foundation model | Same idea; strictly, a base model others build on |
| Open source | Model given away free to download and run yourself |
| Haiku / Sonnet / Opus | Claude's small / medium / large sizes |
| Knowledge cutoff | The date the model's training data stops |
| Plausible | Believable-sounding — what the model is trained to produce |
| Hallucination | A made-up fact delivered with full confidence |
| Band-Aid | Fixing the nearest symptom instead of the root cause |
| Junior analyst | The right mental model for an LLM: hardworking, needs supervision |

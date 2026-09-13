# LLM Engineering – Week 1, Day 3
## The Three Types of Language Models (Base, Chat, Reasoning)

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Rule for reading these notes: don't move to the next section until the current one feels obvious.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. A language model is autocomplete: it guesses the next word, over and over, very fast.
2. **Base model** = trained on the internet, only continues text, doesn't know how to reply to you.
3. **Chat model** = same knowledge, additionally trained on conversations, so it replies. This is ChatGPT.
4. **Reasoning model** = same again, additionally trained to show its working before answering, so it's more accurate on hard questions.

Everything below explains HOW and WHY.

---

## 0. The One Idea Everything Depends On

**A language model is autocomplete.**

- Your phone keyboard suggests the next word ("Good" → "morning" → "everyone").
- It isn't thinking or answering. It has seen millions of messages and knows what word *usually* comes next.
- ChatGPT is the same "guess the next word" machine, trained on the whole internet instead of your text messages, so its guesses are extremely good.
- When it writes a paragraph, it guesses one word, adds it, guesses the next, adds it — hundreds of times, very fast.
- Each small chunk of text it guesses is called a **token** (roughly a word or part of a word).

**Why this matters:** Every other idea below is just a different way of using this autocomplete. If something feels confusing later, come back here.

---

## 1. Base Model — "Knows things, but only continues text"

**What it is:** The raw model. It has read the whole internet (books, websites, code). It is very knowledgeable. It is NOT untrained.

**What it's missing:** The habit of having a conversation.

**Analogy:** A person who has read every book in the world but has never talked to a human. Ask them "What is the capital of France?" and they might just continue: "What is the capital of Spain? What is the capital of Italy?" — because in books, questions are often followed by more questions. They know the answer; they just don't know you want a reply.

**How people forced answers out of base models (early prompt engineering):**
```
Q: What is the capital of France?
A: Paris
Q: What is 2+2?
A: 4
Q: Who wrote Hamlet?
A:
```
The pattern makes "an answer" the most likely next text.

**Example:** GPT-3 (before ChatGPT existed).

**When to use:** Only when you want to train your own model to do something new (later in the course). It's a blank slate, not locked into any habit yet.

---

## 2. Chat Model (also called Instruct Model) — "Knows things AND replies to you"

**What it is:** A base model that was additionally trained on millions of example conversations. Same knowledge, new habit: *when someone asks, answer.*

**Analogy:** Take the well-read person from Section 1 and let them practice millions of conversations. Now when you ask "capital of France?" they naturally say "Paris."

**The conversation structure they were trained on (you already use this in code):**

| Role | Meaning | Example |
|---|---|---|
| **System prompt** | One overall instruction for the whole chat — who the AI is, how to behave | "You are a helpful assistant. Answer in simple English." |
| **User prompt** | A message from the human | "Summarize this web page." |
| **Assistant** | The model's reply | "This page is about..." |

Order: system → user → assistant → user → assistant → ...

**How it was trained — RLHF (Reinforcement Learning from Human Feedback):**
1. Start with a base model.
2. Show it conversation-shaped examples.
3. Humans rate which model replies are better.
4. Adjust the model to produce more of the "better" kind.

This turned GPT (base) into **ChatGPT** (chat) in 2022.

**Words that mean the same thing:** chat model = instruct model = chat variant.

---

## 3. Chain of Thought — the "think step by step" trick

**Discovery:** If you end your question with **"Please think step by step"**, chat models give better answers, especially on math and logic.

**Analogy:** Ask someone "What is 47 × 23?" instantly, no paper → probably wrong. Let them write it out (47×20 = 940, 47×3 = 141, 940+141 = 1081) → right. Same brain, same knowledge. The only difference is writing the steps first.

**Why it works (back to Section 0):** The model autocompletes. If told to think step by step, the most likely continuation is a chain of small steps. The final answer is then predicted *after* correct working, instead of straight after the question — so it's more likely right.

**Name:** Chain of Thought (CoT) prompting.

---

## 4. Reasoning Model (Thinking Model) — "Shows its working automatically"

**What it is:** A chat model that was additionally trained on millions of examples of "show your working, then answer." So it does the step-by-step thinking on its own — you don't have to ask.

**What you see:** Before the final answer, it writes out its thinking (called the **thinking tokens** or **reasoning trace**). Seen on Day 1 with OpenAI's open-source model (gpt-oss).

**In my own words:** If a question is a bit tricky and needs calculation or thought before answering, the reasoning model takes the step-by-step approach without me prompting it to.

**The full progression in one line:**

Base model → (train on conversations) → **Chat model** → (train on step-by-step reasoning) → **Reasoning model**

---

## 5. Hybrid Model — "Decides how much to think"

**Problem:** A model that thinks before *every* answer is wasteful. "Hi" doesn't need three paragraphs of thinking. Thinking is slow, and you pay per token, so it's expensive.

**Solution:** The newest models (GPT-5, Gemini 2.5 Pro, Claude Sonnet 4, etc.) are **hybrid**:
- Easy question → answers immediately, like a chat model.
- Hard question → shows working first, like a reasoning model.

**Vocabulary:**
- **Reasoning budget / reasoning effort** = how much thinking the model does. Often settable: low / medium / high.
- Some open-source models are released in separate versions (chat-only, reasoning-only, hybrid) so you can pick.

---

## 6. Budget Forcing and the "Wait" Trick (S1 paper, Jan 2025)

*(Marked as "skip for now" — not needed to continue the course. Kept here for later.)*

**Budget forcing** = forcing a reasoning model to think longer than it planned.

**The trick:** When the model finishes its thinking and is about to answer, insert the word **"Wait"** into its thinking and let it continue.

**Why it works:** The model is autocomplete. What usually comes after "Wait"? Doubt: "...let me double-check that", "...actually, I'm not sure about step 2." So it re-examines its own work and catches mistakes. Repeat "Wait" several times to force more re-checking.

**Example:**
- Question: pens are 3 for ₹10, how much for 14 pens?
- Model thinks: "14 ÷ 3 = 4.67 groups × ₹10 = ₹46.67." About to answer.
- Insert "Wait" → model continues: "Wait, can you buy 4.67 groups? No — 4 full groups is 12 pens, plus 2 extra... the single-pen price isn't given. Let me reconsider..."
- It caught the problem without being taught anything.

**How it's physically possible:** The model produces one word at a time, and a program controls the loop. When the model sends its "done thinking" signal, the program ignores it, writes "Wait" into the text, and asks for the next word. Only whoever runs the model (researchers, or you running a local model with Ollama) can do this — not users of the ChatGPT app.

**Note:** The transcript says "weight" — it's a mishearing. The word is "wait".

---

## 7. Which Model to Use When

| Situation | Use | Why |
|---|---|---|
| Hard problems, puzzles, math, logic, accuracy matters | **Reasoning model** (high budget) | Highest scores on nearly all benchmarks |
| Quick interactive chat, real-time apps | **Chat model** | No thinking tokens → faster and cheaper |
| Emails, stories, creative writing | **Chat model** (probably) | Reasoning models sometimes overthink and sound stiff. This is opinion, not proven — test it yourself |
| Training your own model to do something new | **Base model** | Blank slate, not locked into any habit |

**Why not always use reasoning?** Two costs: **time** (thinking tokens must be generated first) and **money** (you pay per token, thinking tokens count).

---

## 8. Bonus: Where Does the Training Data Come From?

1. **The public web** — programs called **crawlers** visit pages, save the text, follow links, repeat. Common Crawl (non-profit) gives away billions of pages for free; AI companies also run their own crawlers.
2. **Wikipedia** — free to download in full, high quality.
3. **Books** — public-domain books plus scanned collections (some legally controversial; ongoing lawsuits).
4. **Code** — public repositories on GitHub. This is how models learned to program.
5. **Licensed data** — paid deals with news publishers (e.g. Associated Press), Reddit, Stack Overflow.
6. **Human-written conversations** — hired people write example chats and rate answers (the RLHF part).
7. **Synthetic data** — text written by older models, e.g. millions of worked step-by-step solutions to train reasoning models.

Then it's cleaned: duplicates, spam, junk removed. What remains is trillions of words → that's what the base model reads.

**Why it matters:** Models sometimes get things wrong or "sound like the internet" — because that's literally what they learned from.

---

## How to Explain This to Someone

### If a non-technical person asks "What is an AI language model?"
"It's like the autocomplete on your phone keyboard, but trained on the entire internet. When you type, your phone guesses the next word. ChatGPT does the same thing, just far better, one word at a time, hundreds of times per answer. Everything it does is guessing the next word."

### If a technical person asks
"An LLM is a next-token predictor. A base model is trained purely on text continuation. A chat model adds RLHF training on conversation data so it responds in a system/user/assistant format. A reasoning model is further trained to produce a chain-of-thought trace before the final answer. Hybrid models dynamically allocate reasoning budget per query. All three are the same underlying mechanism with different training on top."

### The analogy
Phone keyboard autocomplete. Base model = the raw autocomplete. Chat model = autocomplete that learned from millions of conversations. Reasoning model = autocomplete that shows its working first.

### The one-liner
"An LLM is autocomplete trained on the internet — base models continue text, chat models reply to you, reasoning models think before replying."

---

## 9. Self-Check Questions (answer in your own words)

1. What is the *only* thing a language model does, at the most basic level?
2. Is a base model untrained? What is it actually missing?
3. What are the three message roles in a chat model? Which one describes the whole conversation?
4. What does adding "think step by step" change?
5. How is a reasoning model different from a chat model that was told to think step by step? *(Hint: trained-in vs. asked-for)*
6. What does a hybrid model decide on its own?
7. Give two reasons you'd pick a chat model over a reasoning model.
8. Name three places training data comes from.

---

## 10. Quick Glossary

| Term | Plain meaning |
|---|---|
| Token | A small chunk of text (roughly a word or part of a word) the model guesses one at a time |
| Base model | Read the internet, only continues text |
| Chat / Instruct model | Trained on conversations, replies to you |
| System prompt | Overall instruction for the whole conversation |
| User prompt | The human's message |
| RLHF | Training using human ratings of model replies |
| Chain of Thought (CoT) | Asking the model to think step by step |
| Reasoning / Thinking model | Shows its working automatically before answering |
| Thinking tokens / reasoning trace | The written-out thinking a reasoning model produces |
| Hybrid model | Decides how much thinking each question needs |
| Reasoning budget / effort | How much thinking the model does (low/medium/high) |
| Budget forcing | Forcing the model to think longer, e.g. the "Wait" trick |
| Crawler | A program that visits web pages and saves their text |

# LLM Engineering – Week 1, Day 3 (Part 3)
## Trying ChatGPT: Six Questions and the Idea of Tokens

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Companions: 01_Week1_Day3_LLM_Types.md, 02_Week1_Day3_Frontier_Models.md

---

## READ THIS FIRST (whole lecture in 3 lines)

1. This is a demo: the lecturer types 6 questions into ChatGPT to show what models are good at. No code.
2. The only new concept: **tokens**. The model never sees letters. Text is chopped into chunks and each chunk becomes a number (`"the cat sat"` → `[1, 2, 3]`). That's why "count the letter A" used to fail: the model receives `[1, 2, 3]`, and the letters are gone.
3. Side lesson: not every problem needs an LLM. Messy human language or judgment → LLM. Exact rules and numbers → ordinary code.

---

## 0. Why This Lecture Exists

Most of the course is code — talking to models through APIs (cloud) or Ollama (my computer). This one lecture uses the normal ChatGPT website so I can see the model's behaviour with my own eyes before writing code. It's a demo, not new theory — except for one new concept: **tokens** (Section 3).

---

## 1. Group 1 — "It's great at this" questions

### Q1: "How do I decide if a business problem is suitable for an LLM solution?"
Shows the kind of question models are best at: a thoughtful, structured explanation with headings, bullets, both sides, a checklist. (Strength: short request → big, well-organized result.)

### Bonus takeaway: not every problem should use an LLM
LLMs are good at messy human language and judgment; weak at exact rules and numbers (slow, cost per word, sometimes wrong).

**Bad fit (use normal code):**
- Calculating salaries — fixed rules and math
- Checking a password is 8+ characters — one line of code
- Sorting 10,000 orders by date — milliseconds in ordinary code

**Great fit (use an LLM):**
- Reading 500 complaint emails and grouping by topic
- Drafting a reply to each complaint
- "Does this contract mention late payment?"

**Rule of thumb:** messy language or judgment → LLM. Exact rules and numbers → normal code.

### Q2: "What are you best at, what's challenging, which other LLMs complement you?"
Tests self-awareness. Answer matched last lecture:
- Good at: explaining, structuring, combining knowledge across topics
- Struggles: fresh info (knowledge cutoff), long math derivations, replacing a doctor/lawyer/therapist
- Praises rivals: Claude for long documents and natural conversation, Gemini for real-time and images/video

**In my own words:** Models are self-aware and know where they are lacking — and they give balanced, honest answers.

---

## 2. Group 2 — The "human" questions

### Q3: "What does it feel like to be jealous?"
Tests something deeply human. Answer: a mix of fear, insecurity, anger, longing; tight chest, racing thoughts. Thoughtful and human-sounding.

Lecturer's caveat: maybe easy because the internet has thousands of jealousy articles. Later labs ask questions definitely *not* in training data — he says the answers are just as good. **Challenge:** think of the hardest, most human question I can, ask GPT-5, see.

### Q4: "How many rainbows does it take to jump from Hawaii to 17?"
Nonsense question. Years ago, early GPT gave a silly answer — it just autocompleted nonsense with more nonsense. Today GPT-5 says: sounds like a riddle; rainbows aren't a unit of distance; if metaphorical, it could mean... It recognises nonsense and responds sensibly.

**In my own words:** Models know what kind of question it is and are aware of how to respond.

---

## 3. Group 3 — Trick questions, and the new concept: TOKENS

### Q5: "How many times does the letter A appear in this sentence?"
GPT-5 gets it right instantly. A couple of years ago, models got this wrong all the time. Two reasons:

**Reason 1 — autocomplete.** Counting is analysis, not next-word guessing. A pure chat model blurts a plausible number. (Reasoning models write the counting steps first, which works.)

**Reason 2 — tokens.** The model never sees letters. Text is chopped into chunks called **tokens** before the model sees it.

### Tokens — the dictionary picture (the version that made it click)

Imagine a dictionary built before the model is trained:

```python
vocab = {"the": 1, "cat": 2, "sat": 3, "on": 4, "mat": 5}
```

I type: `"the cat sat on the mat"`
The **tokenizer** does a lookup: `[1, 2, 3, 4, 1, 5]`

**That list of numbers is what the model receives.** Not the string.

The model works on numbers and outputs numbers, e.g. `[2, 3, 4, 5]`. The tokenizer reverses the lookup and shows me `"cat sat on mat"`.

**Text → numbers → model → numbers → text. The model never touches text.**

**Why letter-counting was hard:** "how many t's in 'the cat sat'?" → model receives `[1, 2, 3]`. The letters are gone. It can only guess from memory.

**Who decides one token vs. three?** Not the model — the tokenizer, built by counting the most common chunks in the training text.
- Common word ("the", "banana") → its own token
- Rare word ("unbelievable") → built from smaller common chunks: `un` `believ` `able`

**Why not just send letters?**
1. **Length** — 1,000 words ≈ 5,000 letters but only ≈ 1,300 tokens. Heavy math per piece, so fewer pieces = faster and cheaper.
2. **Meaning** — "b" means nothing; "banana" carries meaning. Easier to learn from meaningful pieces.

Tokens are the middle ground: bigger than letters, smaller than whole words, so rare/new words can still be built from parts.

**Other analogies used:** "banana" → the model gets `4821`, can't see inside it. Cake slices (tokens) vs. crumbs (letters) — you can count slices, not the crumbs inside.

**Why it's fine now:** reasoning models spell it out in thinking steps; newer models trained on more spelling/counting examples.

*(Tomorrow's lecture goes deep on tokens — this dictionary picture is the foundation.)*

### Q6: "How many words are there in your answer to this question?"
A trap — the model must count words in an answer it hasn't written yet, and the number it writes changes the count. GPT-5's answer: **"One."** One word, correct count.

---

## 4. One-Line Recap

1. Q1–Q2: great at structured, balanced explanations; self-aware about weaknesses and rivals. Not every problem needs an LLM.
2. Q3–Q4: handles deep human questions and nonsense questions like a thoughtful person.
3. Q5–Q6: trick questions that used to fail now work. Letter-counting was hard because the model sees **tokens** (numbered chunks), not letters.

---

## How to Explain This to Someone

### If a non-technical person asks "Why couldn't AI count letters in a word?"
"The AI never sees letters. Before your text reaches it, a program chops it into chunks and replaces each chunk with a number. So 'banana' becomes one number, like 4821. Ask 'how many a's in banana?' and the AI only sees 'how many a's in 4821?' — it can't look inside the number."

### If a technical person asks
"Tokenization converts text to integer IDs via a fixed vocabulary lookup before the model sees anything. Common words map to single tokens; rare words are split into subword pieces. The model operates entirely on token IDs, so character-level tasks like letter counting are inherently difficult — the model has no direct access to the characters inside a token. Modern models handle this via reasoning steps and training on more character-level examples."

### The analogy
A Python dictionary: `{"the": 1, "cat": 2, "sat": 3}`. `"the cat sat"` → `[1, 2, 3]`. The model receives only the numbers. The letters are gone.

### The one-liner
"The model sees numbered chunks, not letters — that's why counting letters used to be hard."

---

## 5. Self-Check Questions

1. Give one business problem that's a bad fit for an LLM and one that's a good fit. What's the rule of thumb?
2. What did the "what are you best at?" question demonstrate?
3. Why did early GPT fail the rainbow question and why does GPT-5 pass it?
4. Walk through "the cat sat" → what does the model actually receive?
5. Who decides whether a word is one token or three? On what basis?
6. Two reasons we use tokens instead of letters.
7. Why was letter-counting hard for older models? (Two reasons.)
8. What was GPT-5's answer to "how many words in your answer?" and why is it clever?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| Token | A chunk of text (whole word or piece of a word) converted to a number before the model sees it |
| Tokenizer | The small program (a dictionary lookup) that turns text into token numbers and back |
| Vocabulary (vocab) | The tokenizer's dictionary of all chunks and their numbers |
| Context window | How much text the model can handle at once (tomorrow's topic) |
| Litmus test | A quick check to decide something (e.g. "does this problem need an LLM?") |
| Meta question | A question about the answer itself ("how many words in your answer?") |

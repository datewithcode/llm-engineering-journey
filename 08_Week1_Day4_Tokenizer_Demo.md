# LLM Engineering – Week 1, Day 4 (Part 5)
## Tokenizer Demo: Spaces, Line Breaks, Numbers, and Rules of Thumb

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Includes my own experiments on platform.openai.com/tokenizer.

---

## READ THIS FIRST (whole lecture in 4 things)

1. Common words = one token each. Rare words = split into pieces.
2. The space before a word is part of the token. " important" (with space) and "important" (no space, inside "unimportant") are DIFFERENT tokens with different IDs. I proved this myself: 3378 vs 31371.
3. Invisible characters like Enter are tokens too. That's why my two-line text gave 12 tokens, not 11.
4. Rule of thumb: 1 token ≈ 4 characters ≈ ¾ of a word. **1,000 tokens ≈ 750 words.** API prices are quoted per million tokens.

Everything else (3-digit numbers, Shakespeare, code) is extra detail.

---

## 1. What the Tokenizer Page Shows

**Example 1 (lecture, and I reproduced it):**
"An important sentence for my class of AI engineers" → **9 tokens, 50 characters.** Every word is common, so each word = one token, each in its own colour.

**Example 2 (lecture):**
"An exquisitely handcrafted quip for my mastera of LLM witchcraft" → **18 tokens, 66 characters.**
- "exquisitely" → several fragments
- "handcrafted" → `hand` + `crafted`
- "mastera" (invented) → `master` + `a`
- "witchcraft" → `witch` + `craft`
- "LLM" → 2 tokens (wasn't a common term when this tokenizer was built)

Splitting "handcrafted" into hand + crafted lets the model reuse what it knows about "hand" and about things being "crafted" — the word-stem idea, live.

**Different models, different tokenizers:** the page lets you pick a model and the splits differ slightly. Not important; don't worry about picking a "more efficient" one.

---

## 2. The Space Is Part of the Token

On the page, each token's colour covers the *space before* the word. The token isn't "important" — it's " important" (space + important). The space means "a new word starts here."

So there are two different tokens:
- " important" (with space) = the word at the start of a word
- "important" (no space) = same letters in the *middle* of a word, e.g. "unimportant" → `un` + `important`

**My proof (Token IDs view):**
- " important" in the sentence = **3378**
- "important" inside "unimportant" = **31371**

Same letters, different ID, because of the space.

Tokens like `crafted` and `craft` with no leading space are "end of word" chunks.

---

## 3. Line Breaks Are Tokens (my "why 12 not 11?" question)

I typed the sentence, pressed Enter, typed "unimportant." Got **12 tokens**, expected 11.

- Line 1: 9 tokens
- The Enter key (new-line character): 1 token — ID **198** in my screenshot
- "unimportant": 2 tokens (`un` = 373, `important` = 31371)
- Total: 12

Invisible characters (new lines, sometimes spaces on their own) are tokens too.

---

## 4. Numbers Are Chopped Every 3 Digits

There are infinitely many numbers, so you can't give each its own token. OpenAI's tokenizer instead has a token for **every 3-digit combination** (000–999 = 1,000 entries). Any number is built from 3-digit blocks, cut left to right, **up to** 3 digits per token:

| Number | Tokens |
|---|---|
| 7 | `7` → 1 |
| 42 | `42` → 1 |
| 999 | `999` → 1 |
| 1234 | `123` + `4` → 2 |
| 20000 | `200` + `00` → 2 |
| 3.141592653589793 | `3` `.` `141` `592` `653` `589` `793` → 7 |

Same idea as `un` + `believ` + `able`: a rare thing built from common pieces. Numbers are chopped by count instead of by meaning, because digits don't have word stems.

**Why 3?** A compromise. 1 digit per token → numbers get very long. 5 digits → 100,000 dictionary entries just for numbers. 3 is the middle.

**Caveats:**
- This is OpenAI's choice. Llama makes every single digit its own token (1234 → 4 tokens). Each lab picks its own rule.
- Chunking is by digit count, not place value: `1234` → `123|4`, not `1|234`.

**Old joke:** early GPT did 3-digit maths fine (one token + one token, seen in training) but flopped on 4-digit, because 4 digits = two tokens and it didn't "see" one number. Fixed now with better training.

---

## 5. Rules of Thumb (memorize)

- 1 token ≈ 4 characters
- 1 token ≈ ¾ of a word
- **1,000 tokens ≈ 750 words**
- Complete works of Shakespeare ≈ 900,000 words ≈ **1.2 million tokens**

**Why it matters:** API pricing is quoted **per million tokens**. "$3 per million tokens" ≈ "$3 to process all of Shakespeare." That's the mental picture.

**Exception:** code, math, scientific text use *more* tokens per word — odd variable names and symbols split into many pieces, sometimes close to one token per character. Paste code into the tokenizer to see.

---

## 6. Things to Try on the Tokenizer Page

- Click **Token IDs** to see the real numbers behind the colours.
- Type "important" and "unimportant" → compare IDs.
- Type `42`, `1234`, `1234567` on separate lines → watch the counts.
- Paste some Python code → see how many tokens vs. words.
- For Python code: the `tiktoken` package does the same thing programmatically.

---

## How to Explain This to Someone

### If a non-technical person asks "How much does AI cost per word?"
"AI companies charge per 'token,' which is roughly three-quarters of a word. A thousand tokens is about 750 words. The complete works of Shakespeare is about 1.2 million tokens. Prices are quoted per million tokens — so '$3 per million' means about $3 to process all of Shakespeare."

### If a technical person asks
"Rule of thumb: 1 token ≈ 4 characters ≈ 0.75 words for English prose. Leading spaces are part of tokens (' important' ≠ 'important'). Newlines and whitespace are tokens. Numbers are chunked in up to 3 digits for OpenAI's tokenizer. Code and non-English text tokenize less efficiently. API pricing is per million tokens, input and output priced separately."

### The analogy
1,000 tokens ≈ 750 words. Shakespeare ≈ 1.2M tokens. "$3 per million tokens" ≈ "$3 for all of Shakespeare."

### The one-liner
"A token is about three-quarters of a word; 1,000 tokens is roughly 750 words; APIs charge per million."

---

## 7. Self-Check Questions

1. Why did "An important sentence for my class of AI engineers" give exactly 9 tokens?
2. Why are " important" and "important" different tokens? What were their IDs?
3. Why did my two-line text give 12 tokens instead of 11?
4. How does the tokenizer handle a long number? Why 3 digits?
5. Is 42 one token or two? Is 1234?
6. 1,000 tokens is roughly how many words? Why does "per million tokens" matter?
7. Does code use more or fewer tokens per word than English? Why?

---

## 8. Quick Glossary

| Term | Plain meaning |
|---|---|
| Beginning-of-word token | A token that includes the leading space, marking a new word |
| Word-ending token | A token with no leading space, continuing a word (`crafted`, `craft`) |
| New-line token | The Enter key as a token (ID 198 in GPT-5's tokenizer) |
| 3-digit chunking | OpenAI's rule: numbers split into up to 3 digits per token |
| Per million tokens | The unit API prices are quoted in |
| tiktoken | OpenAI's Python package for tokenizing text |

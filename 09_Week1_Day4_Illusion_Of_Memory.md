# LLM Engineering – Week 1, Day 4 (Part 6)
## Tokenizing in Code, and the Illusion of Memory

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Notebook: week1/day4.ipynb

---

## READ THIS FIRST (whole lecture in 4 lines)

1. `tiktoken` is a Python library that converts text → token IDs and back. It's the tokenizer page as a function call. No cloud, no AI, just a local dictionary lookup.
2. Every API call to an LLM is **stateless** — the model forgets everything between calls. It's a brand-new stranger every time.
3. The "memory" trick: don't make a fresh messages list each call. Keep one list, keep appending, send the whole list every call. The LIST remembers, not the model.
4. Three roles go in the list: `system` (instructions), `user` (human messages), `assistant` (model's own past replies copied back as history).

---

## 1. tiktoken — the tokenizer page as Python

```python
import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4.1-mini")
tokens = encoding.encode("Hi my name is Ed and I like banoffee pie")
```

- `tiktoken` = OpenAI's tokenizer library. The "translator at the door" as a Python package.
- `encoding_for_model("gpt-4.1-mini")` loads that model's dictionary (different models, slightly different dictionaries).
- `encode(...)` = text → list of token IDs, e.g. `[12194, 922, 1308, 382, 6117, ...]`

**Not an API call.** Nothing goes to the cloud. Local dictionary lookup, same as the web page.

```python
for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")
```

- `decode` = token ID → text (reverse lookup).
- Prints each number next to its chunk: `12194 = Hi`, `6117 = Ed`, and "banoffee" → `ban` + `offee`.

```python
encoding.decode([326])   # → "and"
```

**In my own words:** encode converts text into number IDs; decode reverts IDs back to text.

Play: find words with very small or very large IDs. Not meaningful, just for feel.

---

## 2. The Illusion of Memory

### The experiment (three API calls)

**Call 1:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Ed!"}
]
```
Reply: *"Hi Ed! How can I assist you today?"*

**Call 2:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
]
```
Reply: *"I don't have access to your personal information."*

**Call 3:**
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Ed!"},
    {"role": "assistant", "content": "Hi Ed! How can I assist you today?"},
    {"role": "user", "content": "What's my name?"}
]
```
Reply: *"Your name is Ed."*

### Why call 2 failed: every call is stateless
The model has no memory between calls. Each call: hand it an input, it predicts next tokens, done. It doesn't know you called 20 seconds ago. Day 1 idea: autocomplete only sees what's in front of it right now. In call 2, "Ed" is nowhere in the input → "I don't know your name."

### Why call 3 worked: the list remembered, not the model
**The programmer builds `messages`. It's a plain Python list. The model only sees what's in the list.**

The trick: don't make a fresh list each call. Keep one list, keep appending, send the whole list every call.

```python
messages = [{"role": "system", "content": "You are a helpful assistant"}]

# human types → append
messages.append({"role": "user", "content": "Hi! I'm Ed!"})
# send → reply "Hi Ed! ..." → append the reply too
messages.append({"role": "assistant", "content": "Hi Ed! How can I assist you today?"})
# human types → append
messages.append({"role": "user", "content": "What's my name?"})
# send the whole list (4 items)
```

The model reads item 2 ("I'm Ed") and item 4 ("What's my name?") → most likely next tokens: "Your name is Ed." Not memory — autocomplete on a longer text.

**The model never remembers. The list remembers, because the programmer keeps appending to it.**

### Analogy: strangers and paper
Every call goes to a brand-new stranger who never met you. They only know what's on the paper you hand them.
- Call 2 paper: "What's my name?" → stranger honestly says "I don't know."
- Call 3 paper: the whole history, three lines → stranger reads "I'm Ed" three lines up → "Your name is Ed."

They didn't remember. They *read* it.

### The ChatGPT app does this silently
Every message you send, it resends the entire chat so far. Your 10th message actually sends all 10 messages plus all 9 replies. That's why it "remembers."

### Cost
Yes, you pay for the whole conversation every call, and it grows each message. Fair — you're asking the model to read and compute over more text. Input tokens are very cheap, so it's small, but it's there.

---

## 3. The `role` Field — fixed values only

| role | Who is speaking | When to use |
|---|---|---|
| `"system"` | The programmer giving instructions | Once, at the top |
| `"user"` | The human typing | Every human message |
| `"assistant"` | The model | Every earlier model reply, copied back as history |

- You cannot invent your own role; the API rejects anything else. (A fourth, `"tool"`, appears next week.)
- `"content"` is free text. Only `"role"` is locked.
- These are the same three from Day 3 (system prompt, user prompt, assistant reply) — this is where they live in code.
- Why it matters: the label tells the model who said each line. It reads the list like a script and writes the next `assistant:` line.

```
system:    You are a helpful assistant
user:      Hi! I'm Ed!
assistant: Hi Ed! How can I assist you today?
user:      What's my name?
assistant: ← model writes this
```

---

## 4. The Lecturer's Five Points (must be second nature)

1. Every call to an LLM is stateless.
2. We pass in the entire conversation so far, every time.
3. This gives the illusion the LLM has memory.
4. It's a trick — a by-product of sending everything every time.
5. The LLM just predicts the next tokens; if the sequence contains "My name is Ed" and later "What's my name?", it predicts "Ed."

---

## How to Explain This to Someone

### If a non-technical person asks "Does ChatGPT remember our conversation?"
"No — and that surprises people. Every time you send a message, the AI forgets everything. What actually happens: the app quietly resends your ENTIRE conversation with every message. So the AI reads the whole chat from the top each time. It looks like memory, but it's just reading a longer and longer document."

### If a technical person asks
"LLM API calls are stateless. The illusion of memory is implemented client-side: the application maintains a growing messages array (system, user, assistant, user, assistant...) and sends the full array on every call. The model conditions on the entire context each time. Cost scales with conversation length because the full history is re-processed on every request. Prompt caching mitigates this for repeated prefixes."

### The analogy
A brand-new stranger every call, reading a piece of paper. The paper gets longer each turn because you copy the whole conversation onto it. The stranger didn't remember — they read it.

### The one-liner
"The model forgets everything between calls; the app resends the whole conversation each time, which looks like memory."

---

## 5. Self-Check Questions

1. What do `encode` and `decode` do? Does `encode` call the cloud?
2. Why did call 2 return "I don't know your name"?
3. What is different about the list in call 3?
4. Who builds the `messages` list? What does "send the whole conversation" mean mechanically?
5. What does the `"assistant"` role represent in the list?
6. Can I set `"role": "customer"`? Why not?
7. Why does a long conversation cost more per message?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| tiktoken | OpenAI's Python tokenizer library |
| encode | Text → list of token IDs |
| decode | Token IDs → text |
| Stateless | Each call is independent; the model keeps nothing between calls |
| messages | The Python list of role/content dicts sent to the model |
| system / user / assistant | The three allowed roles: instructions / human / model's past replies |
| Illusion of memory | The model seems to remember only because the whole conversation is resent every call |

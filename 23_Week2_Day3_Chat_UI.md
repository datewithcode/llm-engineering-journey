# LLM Engineering – Week 2, Day 3
## Chat UI, Conversation History, and the Clothes Store Assistant

> Personal study notes. The ChatInterface callback shape (message, history) is the key new concept.
> Notebook: week2/day3.ipynb

---

## READ THIS FIRST (whole lecture in 4 lines)

1. `gr.ChatInterface` builds an instant-message-style UI. Your callback receives TWO things: `message` (what the user just typed) and `history` (the full conversation so far, as a list of role/content dicts).
2. Inside the callback, you build the messages list: system prompt + cleaned history + new message, then send to OpenAI. Gradio tracks the history for you (the Day 4 growing-list trick, automated).
3. The clothes store demo shows three prompting techniques in one system prompt: persona ("you are a shop assistant"), business rules (hats 60% off), and one-shot example ("if customer says X, reply like Y").
4. The dynamic system message for "belt" is the first glimpse of RAG: detect what the user needs, add relevant info to the prompt for that call only. RAG in week 5 replaces the hacky keyword check with a smart search.

---

## 1. `gr.ChatInterface` — Chat with History

Yesterday: `gr.Interface` — one input, one output, no memory.
Today: `gr.ChatInterface` — an instant-message-style UI with conversation history built in.

```python
def chat(message, history):
    return "bananas"

gr.ChatInterface(fn=chat, type="messages").launch()
```

Produces: scrolling conversation area, text box at the bottom, send button. No inputs/outputs to define — Gradio handles everything.

### The callback shape (different from yesterday)

| Parameter | What Gradio passes in |
|---|---|
| `message` | The text the user just typed |
| `history` | The entire conversation so far, as a list of dicts |

`type="messages"` tells Gradio to format history like OpenAI:
```python
[
    {"role": "user",      "content": "hi there"},
    {"role": "assistant", "content": "bananas"},
    {"role": "user",      "content": "how are you"},
    {"role": "assistant", "content": "bananas"}
]
```
(Extra metadata fields too, but role and content are the ones you use.)

### The "bananas" demo proves it
```python
def chat(message, history):
    return f"You said {message} and the history is {history} but I still say bananas"
```
First message: history is `[]` (empty). Second message: history contains the first exchange. **Gradio is tracking the conversation and handing it to you each time.** This is Day 4's illusion of memory — Gradio builds the growing list for you instead of you doing it manually.

---

## 2. Connecting to OpenAI

Replace bananas with a real LLM call:

```python
def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content
```

Line by line:
1. **Clean history** — Gradio's history has extra metadata. This keeps only `role` and `content`, what OpenAI needs.
2. **Build messages list** — system prompt first, then all past conversation, then new message at end. Exactly the growing list from Day 4, but Gradio hands you the history so you don't build it yourself.
3. **Call OpenAI** — same as always.
4. **Return the reply** — Gradio displays it in the chat bubble.

### Detailed Walkthrough — Three Messages, Step by Step

**MESSAGE 1: You type "Hi, I'm Vaibhav"**

Screen is empty. Gradio passes:
- `message = "Hi, I'm Vaibhav"`
- `history = []` (empty)

Function builds:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},   # always first
    # nothing from history
    {"role": "user", "content": "Hi, I'm Vaibhav"}                 # new message, always last
]
```
→ 2 items sent to OpenAI → Reply: "Hello Vaibhav! How can I help you?"

Screen now shows:
```
You:       Hi, I'm Vaibhav
Assistant: Hello Vaibhav! How can I help you?
```

**MESSAGE 2: You type "I'm learning about LLMs"**

One exchange on screen. Gradio passes:
- `message = "I'm learning about LLMs"`
- `history = [user: "Hi, I'm Vaibhav", assistant: "Hello Vaibhav!..."]`

Function builds:
```python
messages = [
    {"role": "system",    "content": "You are a helpful assistant"},         # always first
    {"role": "user",      "content": "Hi, I'm Vaibhav"},                    # from history
    {"role": "assistant", "content": "Hello Vaibhav! How can I help you?"},  # from history
    {"role": "user",      "content": "I'm learning about LLMs"}             # new message
]
```
→ 4 items → Reply: "That's great! What would you like to know?"

**MESSAGE 3: You type "What's my name?"**

Two exchanges on screen. Gradio passes history with all four messages.

Function builds:
```python
messages = [
    {"role": "system",    "content": "You are a helpful assistant"},                # always first
    {"role": "user",      "content": "Hi, I'm Vaibhav"},                           # history
    {"role": "assistant", "content": "Hello Vaibhav! How can I help you?"},         # history
    {"role": "user",      "content": "I'm learning about LLMs"},                   # history
    {"role": "assistant", "content": "That's great! What would you like to know?"}, # history
    {"role": "user",      "content": "What's my name?"}                            # new message
]
```
→ 6 items → OpenAI reads all six, sees "I'm Vaibhav" in item 2 → Reply: "Your name is Vaibhav!"

### The list grows every turn

```
Call 1:  system + message                    → 2 items
Call 2:  system + history(2) + message       → 4 items
Call 3:  system + history(4) + message       → 6 items
Call 10: system + history(18) + message      → 20 items
```

The model reads the whole list each time. "Knows" your name because your name is on the list. Not memory, just a longer input. Day 4's illusion of memory, with Gradio building the list for you.

### Who does what

| Job | Who does it |
|---|---|
| Track the conversation on screen | Gradio |
| Pass it as `history` to your function | Gradio |
| Add the system prompt at the top | Your function |
| Add the new message at the bottom | Your function |
| Send the whole list to OpenAI | Your function |
| Predict the next tokens | OpenAI |
| Show the reply in a chat bubble | Gradio |

Your function is the middle layer connecting Gradio (UI) to OpenAI (brain). Four lines long. Does the trick that makes stateless feel like memory.

### Streaming version (same pattern as before)

```python
def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response
```

Same streaming pattern: `stream=True`, accumulate chunks, `yield` the growing text. Gradio detects the generator and updates the chat bubble live.

---

## 3. The Clothes Store Assistant — Prompts in Action

### The system prompt with three techniques

```python
system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage \
the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. \
For example, if the customer says 'I'm looking to buy a hat', \
you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.' \
Encourage the customer to buy hats if they are unsure what to get."
```

Three things visible in one prompt:
1. **Persona** — "You are a helpful assistant in a clothes store"
2. **Business rules** — hats 60% off, other items 50%
3. **One-shot example** — "if the customer says X, reply something like Y"

### Iterate and refine (the Day 5 lesson again)
He asks about shoes, model recommends them. Fix:
```python
system_message += "\nIf the customer asks for shoes, respond that shoes are not on sale today, but remind them about hats!"
```
Run it, see what's wrong, fix the prompt.

### Dynamic system message — a tiny taste of RAG

```python
def chat(message, history):
    ...
    relevant_system_message = system_message
    if 'belt' in message.lower():
        relevant_system_message += " The store does not sell belts; point out other items on sale."
    messages = [{"role": "system", "content": relevant_system_message}] + history + [...]
```

If user mentions "belt," extra info injected into the system prompt **for that call only**. Same idea as RAG at scale: detect what the user needs, fetch relevant info, stuff it in the prompt. Here it's a hardcoded `if`; in Week 5 it'll be a database lookup.

### What RAG actually is (explained clearly here)

That hacky `if 'belt' in message` is the first glimpse of RAG. All RAG does is:
1. Figure out what the user is asking about
2. Find the relevant information
3. Stuff it into the prompt

The sophistication is in step 1. Here it's a dumb keyword check that breaks if the user says "waist strap" instead of "belt." RAG in Week 5 replaces that keyword check with something smarter (e.g. a database lookup using meaning, not exact words).

### The phone-helper analogy (the version that made it click)

You run a phone line for a shop with 1,000 products. You hire a helper (the LLM) who is smart but knows nothing about your shop.
- **Approach 1 (no info):** Helper guesses → "Yes, we have belts!" (wrong, hallucination)
- **Approach 2 (all info):** Give them all 500 pages → slow, confused, expensive, mixes things up
- **Approach 3 (RAG):** You sit next to the helper. When a customer calls, you listen, quickly pull out ONLY the relevant page, hand it to the helper. Fast, accurate, cheap.

| Analogy | Real thing |
|---|---|
| The helper | The LLM |
| The 500-page stack | All your business information |
| You sitting next to them, picking the right page | The RAG system (your code) |
| The one page you hand over | The text stuffed into the system prompt |

### Critical point: the LLM does NOT call RAG

The LLM has no idea RAG exists. **Your code does the searching, not the LLM.** The actual order:

```
Customer types: "Do you sell belts?"
      ↓
YOUR CODE sees the question
      ↓
YOUR CODE searches the 500 pages → finds the belt page
      ↓
YOUR CODE builds the prompt:
    system: "You are a shop assistant. FACT: We don't carry belts."
    user: "Do you sell belts?"
      ↓
YOUR CODE sends that prompt to the LLM
      ↓
LLM reads the prompt, sees "We don't carry belts", replies accordingly
```

The LLM never searched anything. It never touched the 500 pages. It just read what your code put in front of it.

### Is RAG only for custom, application-specific things?

Yes, that's the point. The LLM already knows generic stuff (Python, Shakespeare, gravity). RAG is for things the LLM was never trained on:
- Your company's products
- Internal HR policies
- A customer's order history
- JobRadar's saved job postings

Information that exists nowhere on the internet, or that changes frequently.

### How does the code know WHEN to search?

**It always searches. Every single call.**

```
Customer asks anything
      ↓
Your code ALWAYS searches your documents for anything related
      ↓
Found something relevant? → paste it into the prompt
Found nothing relevant? → send the prompt without extra info
      ↓
Send to LLM
```

No "should I search or not?" decision. Always search. If nothing relevant comes back, the prompt is just the normal system message plus the question, and the LLM answers from its own knowledge. No harm done.

The "smart" part is HOW you search. Week 5: convert the question into a number (a vector), compare against all documents (also numbers), find the closest match. That's how "waist strap" finds the belts page even without the word "belt."

**The concept: always search your documents, paste whatever's relevant into the prompt, send to LLM.**

### Why not just put everything in the prompt all the time?
- 5 products → sure, put them all in.
- 1,000 products → prompt becomes enormous, accuracy **degrades** (model loses focus in too much text), and you pay thousands of extra tokens every call for no reason.

So you select what's relevant and add only that. That selection is what RAG is.

**RAG in one line:** code searches your documents for relevant info and pastes it into the prompt so the LLM can answer accurately. That's the whole thing.

This is an **inference-time technique** — nothing to do with training the model. Same model, better input, better answers.

### Progress note
20% through the course. Can now: use the chat completions API, build an AI chatbot with an interactive UI, share it, add auth, use multi-shot prompting, and dynamically inject context into the system prompt.

**Tomorrow: tools** — letting the LLM call functions. First step toward agentic AI.

---

## 4. Key Concepts Map

| Concept | Where you first learned it | How it appears today |
|---|---|---|
| Illusion of memory | Day 4, manual growing list | Gradio builds the history list for you |
| Streaming with yield | Day 5 brochure, Day 2 Gradio | Same pattern inside `chat` callback |
| System prompt as persona | Day 3, three roles | Clothes store assistant identity |
| One-shot prompting | Day 5, JSON example | "if customer says X, reply like Y" |
| Iterate the prompt | Day 5, "do not include" line | Adding the shoes rule, the belts rule |
| Context engineering | Day 4 buzzwords | Dynamic system message based on user input |

---

## How to Explain This to Someone

### If a non-technical person asks "What is RAG?"
"Imagine a phone-support helper who's smart but knows nothing about your shop. RAG is you sitting next to them: when a customer asks about belts, you quickly hand the helper the one page about belts. The helper reads it and answers correctly. RAG = search your documents for what's relevant, hand it to the AI, let the AI answer."

### If a technical person asks
"`gr.ChatInterface(fn=chat, type='messages')` calls `chat(message, history)` where history is the prior conversation as OpenAI-format dicts. Build `[system] + history + [user]` and send. RAG preview: the `if 'belt' in message` hack injects context into the system prompt per-call. Real RAG replaces the keyword check with embedding-based retrieval: embed the query, similarity-search a document store, inject top-k chunks. The LLM never calls RAG — your code retrieves before the LLM call. Always search; inject only what's relevant; avoid dumping everything (context bloat, degraded accuracy, cost)."

### The analogy
The phone-helper: your code sits next to the LLM, picks the one relevant page, hands it over. The LLM reads and answers. The LLM never searched anything.

### The one-liner
"RAG: your code searches your documents for what's relevant and puts it in the prompt so the AI can answer accurately."

---

## 5. Self-Check

1. What two parameters does a `gr.ChatInterface` callback always receive?
2. What does `type="messages"` tell Gradio?
3. Why is the first line inside `chat` a list comprehension that cleans history?
4. How is the messages list built? What order: system, history, or new message?
5. What three prompting techniques are visible in the clothes-store system prompt?
6. What does the dynamic system message for "belt" demonstrate? What will it become in Week 5?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| `gr.ChatInterface` | Gradio's chat UI builder: scrolling conversation, text box, send button |
| `message` | The text the user just typed (first callback parameter) |
| `history` | The full conversation so far as a list of role/content dicts (second parameter) |
| `type="messages"` | Tell Gradio to format history like OpenAI's messages format |
| Persona | The identity given to the model via the system prompt |
| Business rules | Facts (prices, policies) injected into the system prompt |
| Dynamic system message | Changing the system prompt per call based on what the user asked |

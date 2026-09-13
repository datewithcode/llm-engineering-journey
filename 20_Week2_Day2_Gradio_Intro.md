# LLM Engineering – Week 2, Day 2 (Part 1)
## Gradio Introduction, Chat Completions vs Responses API, Knowledge Cutoff

> Personal study notes. The Chat Completions sidebar is the decision to remember.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. **Gradio** = Python library that turns a function into a web UI. You write the function, Gradio builds the page. For people who don't want to write frontend code.
2. **Use Chat Completions API, not OpenAI's newer Responses API.** Chat Completions does one thing (messages in, reply out) and every provider speaks it. Responses API has paid extras and locks you to OpenAI only.
3. **Knowledge cutoff live:** ask GPT-4.1-mini "what's today's date?" and it says June 2024. ChatGPT gets it right only because engineers inject the date into the system prompt. Product = model + engineering.

---

## 1. What Is Gradio

A Python library (owned by Hugging Face) that builds a web UI from a Python function. Made for people who can't or don't want to write frontend code.

```python
import gradio as gr

def greet(name):
    return "Hello " + name

gr.Interface(fn=greet, inputs="text", outputs="text").launch()
```

Give it a function, say what the inputs and outputs look like → a web page with a text box, a submit button, and an output area. Press submit, Python function runs, result appears.

### Notes
- `import gradio as gr` is the universal convention. Import is slow (up to 10 seconds). Not a hang.
- Under the hood it's a React app. Explained later; accept the magic for now.
- **Streamlit** is the main alternative (the Outsmart game uses it). Lecturer likes both, prefers Gradio by a hair.

### Today's plan
- A UI for API calls
- The week-1 brochure generator with a UI
- Streaming and markdown inside the UI

---

## 2. Chat Completions API — What It Is and Why It's the Default

### What it does (one thing)
**You send in messages, it sends back the next reply.**

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is Python?"}
]
response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
# → "Python is a programming language..."
```

Input messages in, output text out. Every feature used so far (streaming, JSON format, reasoning effort) is just an option on top of that one action.

### Why it matters
**Everyone uses the same shape.** OpenAI, Anthropic, Gemini, Ollama, OpenRouter, Groq, LiteLLM — they all accept the same list of role/content dicts and return `response.choices[0].message.content`. Write code once, swap `model=` and `base_url=`, works with any provider. It's the universal plug that fits every socket.

### Chat Completions vs Responses API
OpenAI's docs push the newer **Responses API**. The lecturer advises against it:

1. **Extra functionality is mostly paid.** Managed tools (remote code execution, remote browsers) cost extra. A few are free; most aren't.
2. **Locks you into OpenAI.** Chat Completions is the standard across every provider. Responses API is OpenAI-only. Adopt it and you can't swap providers.

**Rule of thumb: use Chat Completions.** A few exceptions exist, but that's the default.

**For JobRadar:** week 4 asks comparing models on cost and accuracy. Only works if code isn't tied to one provider.

---

## 3. Knowledge Cutoff — Seen Live

He writes `message_gpt("What is today's date?")`. GPT-4.1-mini answers: **June 7, 2024.** Confidently wrong by over a year.

That's the knowledge cutoff — the Docker image analogy from Day 3. The model was frozen in mid-2024; it has no idea time has passed.

**ChatGPT gets this right**, but not because the model knows. Engineers at OpenAI inject the current date into the system prompt before the message reaches the model.

**Product = model + engineering.** Call the model directly → raw limitations. Use the product → someone has papered over them. That's exactly the work being learned in this course.

---

## How to Explain This to Someone

### If a non-technical person asks "How do you make a website for an AI?"
"There's a tool called Gradio. You write a Python function, tell Gradio what the inputs and outputs look like, and it builds a web page for you. No web design skills needed. A few lines of code, and you have a working app."

### If a technical person asks
"Gradio (owned by Hugging Face) generates a Svelte frontend and Starlette backend from a Python function signature. Use the Chat Completions API rather than OpenAI's Responses API — Chat Completions is the cross-provider standard; Responses is OpenAI-locked with paid extras. Knowledge cutoff demo: GPT-4.1-mini reports June 2024 as today; ChatGPT gets it right because the product injects the date into the system prompt. Product = model + engineering."

### The analogy
Gradio turns a function into a web app the way a printer turns a document into paper — you write, it renders.

### The one-liner
"Gradio builds a web UI from a Python function; use Chat Completions because every provider speaks it."

---

## 4. Self-Check

1. What is Gradio, in one sentence?
2. What is the one thing Chat Completions does?
3. Why is Chat Completions preferred over the Responses API? (Two reasons)
4. Why did GPT-4.1-mini get today's date wrong?
5. How does ChatGPT get the date right if the model doesn't know it?
6. What does "product = model + engineering" mean?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| Gradio | Python library that builds a web UI from a function |
| `gr.Interface` | Gradio's simplest UI builder: function + inputs + outputs |
| Streamlit | The main alternative to Gradio |
| Chat Completions API | The standard API: messages in, reply out; works with every provider |
| Responses API | OpenAI's newer, more powerful API; paid extras, locks you to OpenAI |
| Knowledge cutoff | The date a model's training data ends; it knows nothing after |
| Product vs model | The product (ChatGPT) wraps the model (GPT) with extra engineering |

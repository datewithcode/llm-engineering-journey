# LLM Engineering – Week 2
## Local Models, Provider Libraries, and Routers

> Personal study notes. The important new concept here is routers vs abstraction layers.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. **Local models via Ollama** are genuinely capable now. gpt-oss 20B on a laptop solved a puzzle that GPT-5-nano on minimal reasoning got wrong. Needs 16GB+ RAM.
2. Every provider (Google, Anthropic) has its own Python library, but they all look the same: create client, pass model and messages, extract the text. **Just use the OpenAI library for everything.**
3. **Router** (like OpenRouter) = a remote service that forwards your request to any provider. One API key, one bill, all models. Call it with the OpenAI library using `model="provider/model"`. **Abstraction layer** (like LiteLLM) = a library on your machine doing the same job locally. Router = server elsewhere; abstraction layer = code on your computer.

---

## 1. Local Models via Ollama

```bash
ollama serve          # if not already running
ollama pull llama3.2  # or llama3.2:1b for the really tiny one
ollama pull gpt-oss:20b
```

Called through the OpenAI library, just pointed at localhost.

**Two-coins puzzle results:**
| Model | Answer |
|---|---|
| llama 3.2 (3B) | "50/50" — wrong, the intuitive answer |
| gpt-oss 20B (local) | **two thirds** — correct |

A 20B open-source model on a laptop solved a puzzle GPT-5-nano on minimal reasoning got wrong.

**Requirements:** gpt-oss:20b needs at least **16GB RAM**. Lecturer has 32GB. Skip it below 16GB.

**Relevant to JobRadar week 3:** local models are genuinely capable now, and free to run.

---

## 2. Other Providers' Own Client Libraries

Every lab shipped its own Python library before everyone standardized on OpenAI's format. Worth recognizing on someone else's team.

**Google:**
```python
from google import genai
client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Describe the colour blue to someone who has never been able to see, in one sentence"
)
print(response.text)
```

**Anthropic:**
```python
from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(
    model="...",
    messages=[...],
    max_tokens=1000        # MANDATORY for Anthropic
)
print(response.content[0].text)
```

**The pattern is the same everywhere:** create a client, pass a model and messages, dig the text out of the response. Only method names and the unwrapping differ.
- OpenAI: `response.choices[0].message.content`
- Google: `response.text`
- Anthropic: `response.content[0].text`

Anthropic's extra mandatory field `max_tokens` caps how much it may generate.

**Advice: just use the OpenAI library for everything.** These are shown for recognition only.

---

## 3. Routers and Abstraction Layers (the new concept)

**The problem:** five providers = five API keys, five accounts, five billing setups, five slightly different libraries.

Two solutions, same goal, different location:

| | What it is | Where it runs |
|---|---|---|
| **Router** | A service between you and the providers. You send your request to it; it forwards to whichever model you named. One key, one bill, all models. | A remote server |
| **Abstraction layer** | A library you call with one consistent API; it decides how to call each provider. No middleman service. | Code on your own machine |

**The distinction: router = a server somewhere else. Abstraction layer = code running locally.**

### OpenRouter (the router demoed)
Use OpenAI's own library, pointed at OpenRouter, and name any model as `provider/model`:

```python
response = openrouter.chat.completions.create(
    model="z-ai/glm-4.5",
    messages=[...]
)
```

He picked **GLM 4.5** (open source, from Chinese startup Z.ai) and asked for a joke. The joke was bad — GLM is strong at coding and problem solving, not comedy. Pricing and performance for every model are on OpenRouter's site; some are free.

### Why OpenRouter matters for JobRadar
One key, one prepaid balance, access to everything including free models. Week 4 asks you to compare models for cost and accuracy on extraction — OpenRouter lets you swap `model="..."` and test a dozen options without opening a dozen accounts. Worth setting up.

---

## How to Explain This to Someone

### If a non-technical person asks "What's a router in AI?"
"It's like a travel agent for AI models. Instead of signing up with five different AI companies and managing five accounts, you sign up with one router (like OpenRouter). You tell it which model you want, it forwards your request. One account, one bill, any model."

### If a technical person asks
"Router = a remote service (OpenRouter) that proxies requests to multiple providers behind one API key and one billing account; call it with the OpenAI client and `model='provider/model'`. Abstraction layer = a local library (LiteLLM, LangChain) providing a unified interface while your code still talks to each provider directly. Router runs elsewhere; abstraction layer runs on your machine. Local models via Ollama are viable — gpt-oss 20B solved a puzzle GPT-5-nano failed. Every provider's client library follows the same shape: create client, pass model+messages, extract text."

### The analogy
Router = a server somewhere else forwarding your requests. Abstraction layer = a translator library on your own machine. Both give you one interface to many models.

### The one-liner
"A router forwards your request to any provider with one key; an abstraction layer does the same locally as a library."

---

## 4. Self-Check

1. What does `ollama serve` do, and when do you need it?
2. Which local model got the coins puzzle right? What's the RAM requirement?
3. How do you get the reply text out of an OpenAI, Google, and Anthropic response?
4. What extra mandatory field does Anthropic require?
5. Router vs abstraction layer — what's the difference?
6. How do you name a model when calling OpenRouter?
7. Why is OpenRouter useful for comparing models?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| `ollama serve` | Starts the local Ollama server so code can call local models |
| gpt-oss:20b | OpenAI's 20-billion-parameter open-source model; runs locally with 16GB+ RAM |
| `max_tokens` | Cap on generated tokens; mandatory for Anthropic |
| Router | Remote service that forwards your request to any provider; one key, one bill |
| Abstraction layer | Local library giving one consistent API across providers |
| OpenRouter | The most popular router; call it with the OpenAI library using `provider/model` |
| GLM 4.5 | Open-source model from Z.ai; strong at coding and problem solving |

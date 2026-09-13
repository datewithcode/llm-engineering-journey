# LLM Engineering – Week 2
## Abstraction Layers and Prompt Caching

> Personal study notes. The one thing that really matters here is prompt caching (section 3).

---

## READ THIS FIRST (prompt caching in 3 lines)

1. **Prompt caching** = if you send the same large block of text in your prompt twice within a few minutes, the provider charges you less the second time (up to 5x or 10x cheaper). The provider recognizes "I already processed this text" and reuses its work.
2. **The trap:** the cache matches from the BEGINNING of your prompt forward. Put the unchanging part (the document, the instructions) at the START. Put the changing part (the question, today's date) at the END. Wrong order = no cache = full price every time.
3. **Minimum size:** caching only kicks in for large blocks (~1,000+ tokens). A short repeated line won't trigger it.

---

## 1. Abstraction Layers (frameworks)

Recall the distinction: **router** = a service you call (OpenRouter). **Abstraction layer** = a library on your own machine.

### LangChain — the heavyweight
The most famous framework. Covered properly in week 5. The lecturer is a mild skeptic: powerful and mighty, but heavyweight with a lot of abstractions to learn.

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-5-mini")
response = llm.invoke(messages)
```

Looks harmless at this size. It gets much bigger in week 5.

### LiteLLM — the lightweight (his preference)
```python
from litellm import completion
response = completion(model="openai/gpt-4.1", messages=messages)
print(response.choices[0].message.content)
```

Nearly identical to the OpenAI library — swap `openai.chat.completions.create` for `completion`; the response unwraps the same way. Model names use `provider/model`, same shape as OpenRouter.

**Its reach is the selling point:** not just the labs, but managed cloud services too — `bedrock/...` (AWS), `azure/...`, `vertex/...` (Google). One interface for everything.

---

## 2. Cost Tracking with LiteLLM

LiteLLM reports input tokens, output tokens, and dollar cost for each call.

A GPT-4.1 joke cost **$0.00023** — two hundredths of a cent. Worth remembering when per-million pricing sounds alarming: individual calls are trivially cheap. Costs matter for unit economics at scale, not for experiments.

The lecturer has built production systems on LiteLLM for exactly this: track spend per user request, compare against revenue, watch unit economics per client.

---

## 3. Prompt Caching (the pro feature)

### The situation
You send the model a huge prompt: all of Hamlet (53,000 tokens) plus a question. You pay for 53,000 input tokens.

Now you ask a *second* question about Hamlet. You have to send all of Hamlet again — the model is stateless. So you'd pay 53,000 tokens again.

### Caching means you don't
The provider notices "I just processed this exact text a minute ago," keeps it ready, and charges much less. In the demo, the second identical call cost **five times less**, and the report showed **53,200 cached tokens**.

### The trap — order matters
The provider only reuses the cache if your prompt **starts** with the same text. It compares from the first character forward and stops at the first difference.

**Bad order:**
```
Call 1: "Where is my father?" + [all of Hamlet]
Call 2: "Who kills Claudius?" + [all of Hamlet]
```
Differ at character one → no match → full price every time.

**Good order:**
```
Call 1: [all of Hamlet] + "Where is my father?"
Call 2: [all of Hamlet] + "Who kills Claudius?"
```
First 53,000 tokens identical → cache matches → full price once, cheap after.

### The rule in one line
**Put the unchanging content at the START, the changing content at the END.**

Same text, different order, five times the cost. Applies to anything variable — today's date at the top of a prompt kills caching entirely.

### Caveat: it only applies to big blocks
Providers have a minimum, typically around **1,000 tokens**. A short repeated line ("my name is Troy") is too small to cache. It works with long system prompts, big documents, or long conversation history.

### Provider differences
| Provider | How it works |
|---|---|
| **OpenAI** | Automatic; matches from the start of the prompt |
| **Anthropic** | Manual — you mark what to cache. Pay **25% more** to prime it, then **10× less** on reuse. Small upfront cost, much bigger saving |
| **Gemini** | Supports both implicit (automatic) and explicit (manual) modes |

### For JobRadar
If the same long extraction instructions go with every posting: **instructions first, posting last.** Free money at volume.

---

## 4. The Hamlet Demo — two other lessons

**Hallucination.** Asked "In Hamlet, when Laertes asks 'Where is my father?', what's the reply?" without context, Gemini Flash Lite confidently invented an answer. The correct reply is "Dead." It didn't know, but it must produce something, and confident-sounding text is the most likely continuation. A confident hallucination — exactly the Day 3 lesson.

**Context fixes it.** Paste the entire play into the prompt, ask again → correct answer "Dead." Inference-time scaling in one step: same model, right information in the input, right answer. Cost rose from $0.00003 to half a cent.

---

## How to Explain This to Someone

### If a non-technical person asks "What's prompt caching?"
"If you send an AI the same long document twice within a few minutes, the second time is much cheaper — the AI company remembers it already processed that text. But there's a catch: the cache only works if the repeated part is at the START of your message. Put the document first, your question last."

### If a technical person asks
"Prompt caching: providers cache the KV state for prompt prefixes. Subsequent requests with an identical prefix (matched from token 0) get discounted input pricing — ~5x for OpenAI (automatic), ~10x for Anthropic (explicit cache_control breakpoints, 25% surcharge to write). Minimum ~1024 tokens. Structure prompts as static content first, variable content last. LiteLLM exposes cached_tokens in response metadata for cost tracking."

### The analogy
Unchanging content first, changing content last. Same text, different order, five times the cost.

### The one-liner
"Prompt caching cuts cost when a large prompt prefix repeats — put the static part first, the question last."

---

## 5. Self-Check

1. LangChain vs LiteLLM — which is heavyweight, which is light? Both are which category (router or abstraction layer)?
2. How do you call a Bedrock or Azure model through LiteLLM?
3. What does LiteLLM report after each call, and why is that useful in production?
4. What is prompt caching, in one sentence?
5. Why does the order of your prompt matter for caching? Give the bad and good version.
6. Why wouldn't a short repeated line get cached?
7. How does Anthropic's caching differ from OpenAI's?
8. Why did the model hallucinate the Hamlet answer, and what fixed it?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| LangChain | Heavyweight LLM framework; week 5 |
| LiteLLM | Lightweight abstraction layer; one interface to every provider and cloud service |
| `completion(...)` | LiteLLM's call, near-identical to OpenAI's |
| Cached tokens | Input tokens billed at a reduced rate because they were processed recently |
| Prompt caching | Paying less when the start of your prompt matches a recent call |
| Priming the cache | Anthropic: paying 25% extra once to store a prompt prefix for cheap reuse |
| Unit economics | Cost per user request vs revenue per user |

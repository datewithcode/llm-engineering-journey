# LLM Engineering – Week 2, Day 5 (Part 2)
## The Multimodal Assistant and Week 2 Wrap-Up

> Personal study notes. This is the finale of week 2.
> Notebook: week2/day5.ipynb

---

## READ THIS FIRST (the whole demo in 4 lines)

1. The finished airline assistant has a three-row UI: chatbot + image (row 1), audio player (row 2), text input (row 3). It has login auth.
2. When you ask about a destination, it runs ~4 LLM calls: one to request the tool, one to answer with the price (after running the SQLite query), one to generate an image of the city, one to generate audio.
3. It uses everything from the whole week: system prompt, chat history, tool calling with the `while` loop, database queries, image generation, audio generation, Gradio UI with auth.
4. The point isn't the airline app. It's that you built a multimodal, tool-using AI assistant with a real UI in a couple of hours.

---

## 1. The Multimodal Assistant in Action

### What the UI looks like
- **Row 1:** Chat window (left) + Generated image (right)
- **Row 2:** Audio player
- **Row 3:** Text input ("Chat with our AI assistant")
- **Login:** `auth=("ed", "bananas")` — you must log in first

### A sample conversation (what happens behind the scenes)

```
Customer types: "I'd like to go to London, please"
      ↓
SECRETARY receives it via Gradio
      ↓
SECRETARY sends to LLM with tool menu (call 1)
      ↓
LLM writes back: "run get_ticket_price('London')"
      ↓
SECRETARY runs get_ticket_price → queries SQLite → $799
      ↓
SECRETARY sends result back to LLM (call 2)
      ↓
LLM writes: "A return ticket to London costs $799. Would you like to book?"
      ↓
SECRETARY shows the text in the chat window
      ↓
SECRETARY also sends a request to generate an image of London (call 3)
      ↓
Image generation LLM returns an image (London Eye, Big Ben, umbrellas, buses)
      ↓
SECRETARY shows the image in the image panel
      ↓
SECRETARY also sends the text to a text-to-speech API (call 4)
      ↓
Audio comes back
      ↓
SECRETARY plays it in the audio panel
```

**~4 LLM calls** stitched together by your code (the secretary). Each one does something different: tool routing, answering, image generation, audio generation. The customer sees one seamless experience.

### "Is it cheaper to go to Paris or Tokyo?"

The LLM asks for TWO tool calls (London and Paris prices). The secretary runs both database queries. The LLM compares prices and answers. Then image generation creates a picture of the cheaper city (Paris). All working together.

---

## 2. What This Week Built (everything stacked)

| Layer | Where you learned it | How it appears here |
|---|---|---|
| System prompt with persona and rules | Day 3 (chat UI) | "You are an airline assistant. Be courteous. If you don't know, say so." |
| Chat history (illusion of memory) | Week 1 Day 4 | Gradio's `message` + `history` callback, full conversation resent |
| Tool calling | Day 4 (boss and secretary) | `get_ticket_price` via SQLite, JSON description, `while` loop |
| Multiple tool calls | Day 4 (improvement) | `handle_tool_calls` iterates through all requests |
| Agentic `while` loop | Day 4 (improvement) | Keeps calling until `finish_reason` is `"stop"` |
| Image generation | Day 5 (new) | Separate LLM call to generate an image of the destination |
| Audio generation | Day 5 (new) | Text-to-speech call for the response |
| Gradio UI with auth | Day 2 (callbacks, share, auth) | Three-row layout, login required |

---

## 3. Exercises

1. **Add tools from yesterday** — set ticket price, make a booking (write a booking record to SQLite)
2. **Connect to a real API** — a student connected to the Amadeus booking API for real prices and flight times
3. **Apply to your business** — now that you can generate text, images, and audio with tool calling, think of something with real commercial value. You can build it in a couple of hours.
4. **Submit to community contributions** — clear notebook outputs, add explanation, make a PR
5. **Post on LinkedIn** — the lecturer amplifies student work

---

## 4. Week 2 Complete — 25% Progress

### What I can now do
- Give an overview of transformers, tokens, context windows, parameters
- Confidently code with the Chat Completions API (and several other APIs)
- Build a multimodal AI assistant with Gradio, tools, image generation, and audio
- Use routers (OpenRouter), abstraction layers (LiteLLM), prompt caching
- Apply tools for commercial functionality (database queries, bookings, calculations)

---

## 5. Week 3 Preview — Completely Different

| What changes | From (weeks 1-2) | To (week 3) |
|---|---|---|
| Models | Frontier closed-source (GPT, Claude) | **Open-source** models |
| How you access them | API calls / Ollama | **Hugging Face code** — actual neural network code you run yourself |
| Where it runs | Cloud (OpenAI servers) / local (Ollama wraps it) | **GPUs** — your own or free ones on **Google Colab** |
| What you see | Input → output (black box) | **Under the hood**: tokenizers, pipelines, transformers in code |

Week 3 is about getting your hands inside the model, not just calling it from outside. You'll work with:
- **Hugging Face** — the open-source hub and library
- **Tokenizers** — the dictionary lookup you learned, now as actual code
- **Pipelines** — pre-built workflows for common tasks
- **Transformers** — the actual neural network architecture, in Python
- **GPUs** — graphics cards used for the heavy math (Google Colab gives you free ones)
- **Running inference** — using the model directly, not through an API

---

## How to Explain This to Someone

### If a non-technical person asks "What did you build in week 2?"
"An airline customer service assistant. You chat with it, it looks up real ticket prices from a database, generates a picture of the destination, and reads the answer aloud. All from a few hours of work, using free tools."

### If a technical person asks
"A multimodal Gradio app: ChatInterface with tool-calling (SQLite price lookup via `while` loop), plus separate calls for image generation (diffusion model) and text-to-speech. Roughly four LLM/model calls per interaction, orchestrated by Python. Auth via `launch(auth=...)`. Everything from weeks 1-2 stacked: system prompts, conversation history, tools, JSON schemas, streaming patterns, Gradio callbacks."

### The analogy
Every technique from two weeks, stacked like layers in one working product.

### The one-liner
"A multimodal AI assistant with tools, images, and audio — built in a couple of hours from the week 1-2 toolkit."

---

## 6. Self-Check

1. How many LLM calls are involved when you ask about a flight to London? Name each one.
2. What does each row of the multimodal UI show?
3. List every technique from weeks 1-2 that appears in the final assistant.
4. What's different about week 3 compared to weeks 1-2?
5. What is Google Colab and why does it matter?

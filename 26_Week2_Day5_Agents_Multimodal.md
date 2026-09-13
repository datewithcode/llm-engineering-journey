# LLM Engineering – Week 2, Day 5 (Part 1)
## Agent Definitions, Five Hallmarks, and the Multimodal Setup

> Personal study notes. The secretary is in every step. No shortcuts.
> Notebook: week2/day5.ipynb

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Two real definitions of "agent": (a) the LLM controls the workflow via its output tokens, or (b) an LLM runs tools in a loop to achieve a goal (the `while` loop from yesterday, made real).
2. Five hallmarks: memory, planning, autonomy, orchestration, tools. The more you tick, the more "agentic."
3. Structured outputs and tool calls are basically the same thing — LLM writes structured text, your code reads it and acts. The secretary reads the boss's note either way.

---

## 1. Two Real Definitions of "Agent"

Day 4 gave loose definitions. This lecture sharpens them.

### Definition 1: The LLM controls the workflow

The LLM's output tokens determine what happens next. Not "the LLM decides" in a magical sense — it predicts tokens, and those tokens get interpreted as decisions by your code (the secretary). Your code reads the tokens and acts on them.

Example: the LLM outputs "run search_flights, then run search_hotels." Your code follows that order. The LLM controlled the workflow — through text, not through magic.

### Definition 2 (newer, the one taking hold): An LLM runs tools in a loop to achieve a goal

This is the Claude Code picture: the LLM has a goal, it calls tools repeatedly, checks progress, continues until the goal is met.

The `while` loop from yesterday's code IS this definition, made real:

```python
while response.choices[0].finish_reason == "tool_calls":
    # handle tools, call LLM again
```

The LLM keeps going until `finish_reason` is no longer `"tool_calls"` — meaning it's achieved the goal and has a final answer.

### The loose definition (mentioned but not endorsed)

Some people call anything "agentic" if it involves multiple LLM calls stitched together. The brochure lab (Week 1, Day 5) would qualify under this definition. The lecturer doesn't really endorse this — the two definitions above are more precise.

---

## 2. Five Hallmark Characteristics of an Agent

The more you tick, the more "agentic" it is. You don't need all five.

| Characteristic | What it means | Example |
|---|---|---|
| **Memory** | Keeps track of what happened across multiple steps | The conversation history, saved to a database (not just Gradio's UI) |
| **Planning** | Can lay out a sequence of steps before starting | The to-do list from the tools lecture: "1. Fetch careers page, 2. Extract postings, 3. Score them, 4. Summarize" |
| **Autonomy** | Its output tokens determine what happens next (not a human scripting each step) | The LLM decides to search flights before hotels — nobody told it that order |
| **Orchestration** | Can call other LLMs or coordinate multiple activities via tools | A main LLM calls a translation LLM, then a summarization LLM |
| **Tools** | Can take actions (database, API, code execution) | `get_ticket_price`, `book_flight`, `run_python_code` |

---

## 3. Structured Outputs and Tools Are "Basically the Same Thing"

A throwaway line from the lecturer, but worth holding:

**Tool call version:**
```
LLM outputs: tool_call = get_ticket_price("London")
Your code: sees the tool call → runs get_ticket_price("London") → sends result back
```

**Structured output version:**
```
LLM outputs: {"next_agent": "translator", "task": "translate to Spanish", "text": "..."}
Your code: reads the JSON → calls the translator → sends result back
```

Same pattern. LLM writes structured text. Your code (the secretary) reads it and acts. Whether the API calls it a "tool call" or a "structured output," the mechanism is identical. The secretary reads the boss's note either way.

People who work with agents know these are the same thing with different names. Worth remembering when frameworks present them as separate concepts.

---

## 4. What This Lecture Builds (preview)

Today adds three things to the airline assistant:
1. **Image generation** — a separate LLM call that generates images, shown in the UI
2. **Sound generation** — another LLM call that creates audio
3. **Stitched together** — multiple LLM calls orchestrated into one solution

Not full agentic AI, but a step in that direction. Healthy use of tools.

The full agentic patterns (agent frameworks, OpenAI Agents SDK, MCP) are covered in the companion Agentic AI course (course #5 in the curriculum).

---

## 5. The Recap (first half of the notebook)

The first 10+ cells re-run everything from yesterday to confirm it works:
- System prompt with "if you don't know, say so"
- `get_ticket_price` querying the SQLite database
- The JSON tool description
- The `while` loop version of the chat callback
- `handle_tool_calls` iterating through multiple tool requests
- Gradio ChatInterface

If you run this and ask "How much is a flight to London?" you should see "Database tool called" printed in the notebook and the price appearing in the chat. If not, re-run the Day 4 notebook to populate the database first.

---

## How to Explain This to Someone

### If a non-technical person asks "What makes something an 'agent'?"
"An AI that doesn't just answer — it works toward a goal. It plans steps, does them one at a time using tools, checks the results, and keeps going until the job is done. Five signs: it remembers, it plans, it decides its own next step, it can coordinate other AIs, and it can take actions."

### If a technical person asks
"Two accepted definitions: (1) the LLM controls the workflow — its output tokens determine the next action; (2) an LLM runs tools in a loop to achieve a goal. Hallmarks: memory persistence, planning, autonomy, orchestration (tools that invoke other LLMs), and tool use. Structured outputs and tool calls are mechanically equivalent — the model emits structured text, the runtime interprets it. Frameworks (OpenAI Agents SDK, MCP) formalize this; the manual `while` loop from the airline lab is the same thing."

### The analogy
The difference between asking someone a question (chatbot) and handing them a task to complete (agent).

### The one-liner
"An agent is an LLM running tools in a loop, deciding each step, until the goal is met."

---

## 6. Self-Check

1. State the two real definitions of "agent" — one sentence each.
2. Name the five hallmark characteristics. Which ones does the airline assistant have so far?
3. How are structured outputs and tool calls "the same thing"?
4. Which definition does the `while` loop from yesterday match?
5. What does "the LLM controls the workflow" actually mean, mechanically? (Hint: tokens.)

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| Agent (definition 1) | A system where the LLM's output tokens control what happens next |
| Agent (definition 2) | An LLM running tools in a loop to achieve a goal |
| Memory (agent feature) | Keeping track of what happened across steps |
| Planning (agent feature) | Laying out steps before starting |
| Autonomy | The LLM's tokens determine the next action, not a human script |
| Orchestration | Calling other LLMs or coordinating multiple tools |
| Structured output | JSON the LLM writes that your code interprets as instructions — same mechanism as tool calls |
| OpenAI Agents SDK | A framework that handles tool JSON, routing, streaming, and conversation history for you |

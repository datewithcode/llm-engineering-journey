# Rebuild notes

## 01_tool_calling.py — attempt 1 (Sep 14–15, 2026)

**Result:** working. `answer: The price of a ticket to Tokyo is $1400`
**Mode:** guided — built in 4 chunks with fill-in-the-blank hints. Not yet from a blank file unaided.
**Time taken:** not recorded

### Where I got stuck — and the fix

| Stuck on | What I learned |
|---|---|
| The `openai` import line | Import lines are look-up-level: `from openai import OpenAI` |
| `ModuleNotFoundError: No module named 'openai'` | Right code, wrong Python. ▶ used uv's raw Python. Activate the venv, then `python file.py` |
| `.get("tokyo")` found nothing | Dict keys are case-sensitive — lowercase **both** the keys and the lookup |
| Unknown city printed `None` | `.get(key, "unknown")` — second value is the default |
| Message list shape | `[ ]` list of `{ }` notes; keys are `"role"` and `"content"`; system → user |
| Where the model's words live | `response.choices[0].message.content` |
| Menu typos `parameter`, `destination` | Must be `parameters` and `description`. Python doesn't care; the model does — it guessed the wrong argument name 2/4 times |
| `json.decoder(...)` → "module not callable" | `json.loads` = load from a **s**tring. Arguments arrive as text, not a dict |
| Which key holds the city | Read it off the output: `{"destination_city": "Tokyo"}` |
| Role of the result note | `"tool"` (the secretary), not `"assistant"` (the boss) |
| `"content": "result"` | Quotes = the word "result". No quotes = the variable |
| `tool_call.finish_reason` → AttributeError | The sticker is on `response.choices[0]`; the job has a ticket number: `tool_call.id` |
| Forgot to append the model's job note | Ollama allowed it (8/8 still correct on qwen). OpenAI rejects it with a 400. Always append it first |

### Next attempt
Delete the file. Rebuild from a blank file — no hints — timed. Target: before **Sep 19**.


## 03_from_memory.py — attempt 3, the Sep 19 test

**Result:** working. `A ticket to Tokyo costs $1200.`
**Mode:** blank file, no AI, no old files open. **One lookup:** the tools-menu bracket shape
(note 25) — always classed as look-up-level. Wrote the flow as comments first, from memory,
before any code.
**Time taken:** ~45 minutes, including debugging

### Written from memory, no help
Client + `base_url` + `MODEL` · price dict and `get_price_ticket` with `.lower()` and a
default · `system_message` · the message list · the menu's three connections · the first call
with `tools=tools` · `tool_calls[0].id` · `json.loads` · pulling `destination_city` out ·
appending note [2] and note [3] · the second call · printing the answer.

### The four bugs, and what each taught

| Bug | What the pile showed | Lesson |
|---|---|---|
| Appended `result_tools` (the whole response) instead of `.choices[0].message` | `400 invalid message content type: <nil>` | The envelope is not the note |
| Note [3] keys invented: `destination_city`, `tool_job_id` | same `<nil>` | Only `role`, `content`, `tool_call_id` mean anything |
| **Never called `get_price_ticket`** — note [3] carried `'Tokyo'` | `3 {'role': 'tool', 'content': 'Tokyo', ...}` and the boss answered "one unit of currency" | The city is the **input**; the price is the **result**. Answer the question that was asked |
| Menu `name` said `get_ticket_price`, function was `get_price_ticket` | note [2] showed `name='get_ticket_price'` | Connection #1: the menu name must match the function exactly |

### Debugging method that worked
Printing the whole pile with `for i, m in enumerate(llm_data): print(i, m)` showed note [3]
holding `'Tokyo'`. **Read the pile, not the code.**

### Next
Rebuild again without the menu lookup, and with the function call in place from the start.

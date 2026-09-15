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

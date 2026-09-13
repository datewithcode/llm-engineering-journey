# LLM Engineering – Week 1, Day 5 (Part 4)
## Call #2, Streaming, and Changing Tone with One Prompt

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Notebook: week1/day5.ipynb, cells 22-27. This completes the brochure lab.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **Call #2** uses gpt-4.1-mini (fast chat model) instead of gpt-5-nano (slow reasoning model), because writing a brochure doesn't need deep reasoning. Match the model to the job.
2. **Streaming** = `stream=True` on the API call, then loop over chunks, accumulate the text, and display the growing result. Token by token, typewriter effect. Same pattern as every streaming function in the course.
3. **Changing tone:** swap the system prompt from "professional" to "humorous, witty" and the same code produces a completely different brochure. Tone is a prompt decision, not a code decision.
4. The humorous brochure is full of made-up facts. That's a success, not a failure, because you *asked* for imaginative output. Judge output by whether it serves the objective you set.

---

## 1. create_brochure — call #2 at last (cells 22–23)

```python
def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
    )
    result = response.choices[0].message.content
    display(Markdown(result))
```

Same shape as call #1, minus `response_format` — this time you want prose, not JSON.

### Two things worth noting

**Different model.** Call #1 = `gpt-5-nano`; call #2 = `gpt-4.1-mini`.
- Nano is a reasoning model: thinks before answering, slow (~30s).
- 4.1-mini is a pure chat model: faster, and writing a brochure doesn't need deep reasoning.
- The Day 3 lesson applied: **match the model to the job.** Cheap and slow for filtering, fast and fluent for writing.

**`display(Markdown(result))`** — the model returns markdown (`# headings`, `**bold**`). Plain `print` would show raw symbols. `Markdown()` renders it. This is why the system prompt says "without code blocks" — fences would stop it rendering.

### What happens when cell 23 runs
1. `get_brochure_user_prompt` → `fetch_page_and_all_relevant_links` → **GPT-5-nano** (call #1, ~30s, found 13 links)
2. Those pages get scraped into the user prompt
3. **GPT-4.1-mini** called (call #2) → brochure in markdown
4. Rendered: "What we offer", "Our community", "Company culture", "Careers"

Both calls fire from one function call. The chain is complete.

---

## 2. Streaming (cells 25–26)

```python
def stream_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[...same...],
        stream=True
    )
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        update_display(Markdown(response), display_id=display_handle.display_id)
```

**The core idea:** the model generates token by token anyway, so why wait for all of it? Show each token as it arrives.

- **`stream=True`** — the fourth parameter so far (model, messages, response_format, stream). Changes what comes back: not a finished response object, but a **stream** you loop over. Each turn gives one **chunk** (a token or few).
- **`chunk.choices[0].delta.content`** — compare with non-streaming `response.choices[0].message.content`. `message` → `delta`. **Delta = the new bit only**, not the whole answer. So you accumulate yourself with `response += ...`.
- **`or ''`** — guards against `None`. Some chunks carry no text (metadata, the stop signal), and `None` would crash the `+=`.

### The three fiddly lines
Plain text would just be `print(chunk..., end='')`. It's longer here only because of markdown:
- `display(Markdown(""), display_id=True)` — put an empty markdown block on screen, keep a handle
- `update_display(...)` — each loop, overwrite that same block with the **full text so far**

Not appending letters — redrawing the whole block many times a second. That's what makes markdown render live.

### Why it matters beyond looks
Streaming isn't just nicer UX — it's the model's actual behaviour made visible. Token → feed back in → next token. Watching Day 1's autocomplete happen in real time. (Transport protocol: SSE, Server-Sent Events. Just a name.)

---

## 3. The Humorous Version (cell 27)

Comment out the first system prompt in cell 19, uncomment the humorous one, rerun cell 19 and cell 27. Output:

> "Keep it open, keep it ethical, keep it hugging." / "What's cooking in the AI kitchen?" / "Casual tea drinkers and serious problem solvers" / "Ready to join the AI hug circle?"

Completely different personality. **Same code, same data, one changed prompt.** Tone, audience, and style are prompt decisions, not code decisions.

### The honest bit about hallucination
It's all invented — that isn't Hugging Face's motto, nobody mentioned tea. Normally a failure. Here it isn't, because you *asked* for a humorous, imaginative take.

**The standard isn't "is it factually true?" but "does it serve the objective I set?"** Playful brochure wanted → success. Facts wanted → go back and change the prompt. Iterate until the output matches the objective.

### The notebook note (globals)
Why no need to rerun cells 20, 22, 25 after changing the system prompt? Because `brochure_system_prompt` is a **global variable** in the notebook. Rerunning cell 19 replaces its value everywhere; existing functions pick up the new one when next called.

Bad practice in production software. Correct in a notebook when exploring prompts as a scientist: change one cell, rerun one cell, see the result in seconds. Fast experimentation is the point.

---

## 4. The Whole Lab in One Picture

```
create_brochure("HuggingFace", "https://huggingface.co")
   │
   ├─ get_brochure_user_prompt
   │     └─ fetch_page_and_all_relevant_links
   │           ├─ fetch_website_contents(url)          ← Python scrape
   │           ├─ select_relevant_links(url)           ← LLM CALL #1 (gpt-5-nano, JSON)
   │           └─ fetch_website_contents(each link)    ← Python scrape
   │     └─ truncate to 5,000 chars
   │
   └─ chat.completions.create                          ← LLM CALL #2 (gpt-4.1-mini, markdown)
         └─ display(Markdown(...))  or  stream=True for typewriter
```

---

## How to Explain This to Someone

### If a non-technical person asks "Why does ChatGPT type out its answer word by word?"
"Because that's genuinely how it works. The AI generates one word at a time, and the app shows each word as it arrives instead of making you wait for the whole answer. It's not an animation — you're watching the AI think in real time."

### If a technical person asks
"Streaming: pass `stream=True` to the API; instead of one response object, you get an iterator of chunks. Each chunk contains `choices[0].delta.content` — the new tokens only. Accumulate them into a running string and re-render. The transport is SSE. For markdown, re-render the accumulated string on each chunk rather than appending. Model selection matters: use a fast chat model (gpt-4.1-mini) for generation tasks that don't need reasoning."

### The analogy
A waiter bringing each course as it's ready instead of waiting until the whole meal is cooked.

### The one-liner
"Streaming shows tokens as they're generated — set stream=True, loop over chunks, accumulate the delta."

---

## 5. Self-Check Questions

1. Why use gpt-4.1-mini for call #2 instead of gpt-5-nano?
2. Why `display(Markdown(result))` instead of `print`?
3. What are the four parameters seen so far on `chat.completions.create`?
4. What does `delta` mean, and why is `response +=` needed?
5. What is `or ''` protecting against?
6. Why is the streaming code longer than a simple print?
7. The humorous brochure is full of made-up facts. Why is that a success here?
8. Why didn't the other cells need rerunning after changing the system prompt?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| `stream=True` | Return tokens as they're generated instead of one finished reply |
| Chunk | One small piece of a streamed response |
| `delta` | The new text in this chunk only (vs `message` = the whole reply) |
| `display` / `update_display` | Jupyter: draw a block, then overwrite it in place |
| SSE (Server-Sent Events) | The protocol streaming uses |
| Global variable | A notebook variable visible to all cells; rerun one cell to change it everywhere |
| Objective-based evaluation | Judge output by whether it serves your goal, not only by factual accuracy |

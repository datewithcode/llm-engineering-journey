# LLM Engineering – Week 2, Day 2 (Part 3)
## Gradio: Markdown, Streaming with yield, and Swapping Models

> Personal study notes. The yield concept is the important new thing here.
> Run `92_REF_return_vs_yield_demo.py` if this feels fuzzy — it shows the difference live.

---

## READ THIS FIRST (yield in 3 lines)

1. `return` = hand the full answer to the caller ONCE, function ends. The caller waits until everything is ready.
2. `yield` = hand a partial answer to the caller, function PAUSES, continues when asked for more. Like a vending machine: press → get item → machine stops → press again.
3. Gradio needs `yield` (not `print`) because Gradio is the caller waiting to receive values to update the UI. `print` sends text to your notebook terminal, which Gradio isn't watching.

---

## 1. Markdown Output

Two small changes to the basic Gradio UI:

- System prompt: add `"respond in markdown without codeblocks"`
- Output field: change `gr.Textbox` to `gr.Markdown` — tells Gradio to render headings, bold, etc. instead of showing raw `#` and `**` symbols

Everything else stays the same.

---

## 2. return vs yield vs print (the key concept)

### return — waiter brings the full meal at once
```python
def make_meal():
    meal = "starter + main + dessert"
    return meal

result = make_meal()   # result = "starter + main + dessert"
```
Wait, wait, wait, then everything arrives at once. The caller has the value.

### print — you shout to nobody
```python
def make_meal():
    print("starter")
    print("starter + main")

result = make_meal()   # result = None ← the caller got NOTHING
```
Text appears on your terminal screen, but the caller has nothing. print talks to the screen, not to the caller.

### yield — hand each course to the waiter as it's ready
```python
def make_meal():
    yield "starter"
    yield "starter + main"
    yield "starter + main + dessert"

for course in make_meal():
    print(course)       # caller RECEIVES each value and decides what to do
```
Text arrives one by one AND the caller has the value each time. The caller decides: print it, send to Gradio, save to a file.

A function with `yield` instead of `return` is called a **generator**.

### The generator waits
The function **stops at each yield** and doesn't continue until the caller asks for the next value. Like a vending machine — press button → get item → machine stops → press again → next item.

```python
gen = make_meal()       # nothing runs yet
first = next(gen)       # runs to first yield → "starter", then freezes
second = next(gen)      # runs to second yield → "starter + main", then freezes
```

A `for` loop automatically presses the button each time. When yields stop, the loop ends.

### The Gradio connection
Gradio is the caller. It's standing at the kitchen door waiting for you to hand it something.

- `print` → text goes to your notebook terminal. Gradio isn't watching your terminal. UI shows blank.
- `yield` → text goes to Gradio. Gradio receives it and updates the UI.

That's why Gradio needs `yield`, not `print`.

---

## 3. Streaming in Gradio

### Without streaming (return)
```python
def message_gpt(prompt):
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=...)
    return response.choices[0].message.content
    # User sees: nothing... nothing... FULL ANSWER
```

### With streaming (yield)
```python
def stream_gpt(prompt):
    stream = openai.chat.completions.create(model="gpt-4.1-mini", messages=..., stream=True)
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ''
        yield result    # hands the growing text to Gradio each time
    # User sees: "The"... "The trans"... "The transformer is"... word by word
```

**Gradio code: exactly one change** — `fn=stream_gpt` instead of `fn=message_gpt`. Gradio detects the generator automatically and keeps refreshing the display.

Note: `result` is **cumulative** (the whole text so far, not just the new chunk). Gradio replaces the entire output each yield, so it needs the full text each time.

### Line-by-line trace of the streaming loop

Suppose GPT is generating "Hello there friend":

| Loop # | `chunk` gives you | `result` after `+=` | what gets yielded to Gradio |
|---|---|---|---|
| 1 | "Hello" | "Hello" | "Hello" |
| 2 | " there" | "Hello there" | "Hello there" |
| 3 | " friend" | "Hello there friend" | "Hello there friend" |

Inside the loop:
- `chunk.choices[0].delta.content` — the new piece that just arrived. Just a word or two. (`delta` = "the new bit only," not the whole answer.)
- `or ''` — some chunks have no text (metadata, stop signal). Without this, `None + "Hello"` crashes. `or ''` turns `None` into an empty string.
- `result +=` — glue the new piece onto everything so far.
- `yield result` — hand the ENTIRE text so far to Gradio. Gradio replaces the screen each time.

### The whole flow in one picture
```
User presses Submit
       ↓
Gradio calls stream_gpt("explain transformers")
       ↓
stream_gpt sends messages to GPT with stream=True
       ↓
GPT generates tokens one by one
       ↓
Loop: chunk arrives → glue onto result → yield result to Gradio → screen updates
      chunk arrives → glue onto result → yield result to Gradio → screen updates
      ...
       ↓
No more chunks → function ends → Gradio stops refreshing
```

That loop — chunk arrives, glue it on, yield the growing text — is the same pattern in every streaming function in the course.

### When to use which

| Use `return` | Use `yield` |
|---|---|
| Complete answer before showing anything | Show progress as it builds (typewriter) |
| Short, fast calls | Long calls where user would stare at blank |
| JSON responses (need whole thing to parse) | Text/markdown (partial text is readable) |

**Simple rule:** if the user benefits from seeing the answer build up, use `yield` + `stream=True`. Otherwise use `return`.

---

## 4. Swapping Models

`stream_claude` is identical code to `stream_gpt`, but:
- `openai` → `anthropic` (still using the OpenAI library pointed at Anthropic's endpoint)
- Model name changes to Claude Sonnet 4.5

Gradio code: swap `fn=stream_claude`, change `title="Claude"`. Nothing else.

**The point:** Gradio doesn't care which model you call. Same callback pattern. Swap one function, get a different model's answers, same UI.

### Model selector dropdown

A function that streams from GPT *or* Claude, based on a second input:

```python
def stream_model(prompt, model):
    if model == "GPT":
        result = stream_gpt(prompt)
    elif model == "Claude":
        result = stream_claude(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result
```

**New Python trick: `yield from`.** It's a shortcut. These two are identical:

```python
# Long way
for chunk in result:
    yield chunk

# Short way (same thing)
yield from result
```

"Yield each item from this generator" in two words instead of two lines.

**The Gradio part — adding a dropdown:**

```python
model_selector = gr.Dropdown(choices=["GPT", "Claude"], label="Select model", value="GPT")

gr.Interface(
    fn=stream_model,
    inputs=[message_input, model_selector],   # TWO inputs now
    outputs=gr.Markdown(...),
    examples=[
        ["Explain transformers to a layperson", "GPT"],
        ["Explain transformers to an aspiring AI engineer", "Claude"]
    ]
)
```

Three differences from before:
1. `gr.Dropdown` — a new input type. `choices` lists the options, `value` sets the default.
2. `inputs` is a **list of two things**. Gradio passes both to the function: first input → first argument (`prompt`), second input → second argument (`model`).
3. `examples` is a list of lists — each inner list has two items matching the two inputs.

### The brochure generator in a UI

Same pattern, three inputs (company name, URL, model), one output:

```python
def stream_brochure(company_name, url, model):
    # fetch website contents, build prompt, stream from GPT or Claude
    yield from result

gr.Interface(
    fn=stream_brochure,
    inputs=[company_name_input, url_input, model_selector],
    outputs=gr.Markdown(...),
    examples=[
        ["HuggingFace", "https://huggingface.co", "GPT"],
        ["Edward Donner", "https://edwarddonner.com", "Claude"]
    ]
)
```

A working brochure-generator UI in minutes. Focus on the Python function, Gradio handles the interface.

**Limitation:** this UI has no conversation history. One message in, one answer out. Day 3 fixes that with `gr.ChatInterface`.

---

## 5. Notebook Globals (reminder)

He redefines `system_message` in a later cell without re-running the function's cell. It works because `system_message` is a global variable — the function reads its current value when called, not when defined. Scientist hat (experiment, iterate, change) not engineer hat (avoid globals). Same explanation as the brochure lab.

---

## How to Explain This to Someone

### If a non-technical person asks "What's the difference between return and yield?"
"A waiter who brings the whole meal at once (return) versus a waiter who brings each course as it's ready (yield). For AI apps, yield lets the answer appear word by word instead of making you wait for the whole thing."

### If a technical person asks
"`return` ends the function with a single value. `yield` makes it a generator: it emits a value, pauses, and resumes on the next iteration request. Gradio detects generator callbacks and re-renders the output on each yield. For streaming: `stream=True` on the API call, accumulate `chunk.choices[0].delta.content` into a running string, yield the full string each time (Gradio replaces the output, so it needs cumulative text). `print` won't work — Gradio isn't watching stdout; it's the caller receiving yielded values. `yield from` delegates to another generator."

### The analogy
Vending machine: press → get item → machine stops → press again. The function pauses at each yield until asked for more.

### The one-liner
"yield hands partial results to the caller one at a time; that's how Gradio streams AI output live."

---

## 6. Self-Check

1. What do you change in Gradio to render markdown instead of plain text? (Two things)
2. What is the difference between `return` and `yield`? Use the kitchen analogy.
3. Why can't Gradio use `print`? What does it need instead?
4. What happens if you yield three times but only consume one?
5. What is one change needed in the Gradio code to switch from return to streaming?
6. Why is `result` cumulative in the streaming function?
7. What changes to swap from GPT to Claude in Gradio?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| `return` | Hand the full answer to the caller once, function ends |
| `yield` | Hand a partial answer to the caller, function pauses, continues when asked |
| Generator | A function that uses `yield` — produces values one at a time on demand |
| `gr.Markdown` | Gradio output that renders markdown formatting |
| `stream=True` | API parameter: get tokens as they're generated instead of all at once |
| Cumulative result | The whole text so far, not just the new chunk — what Gradio needs each yield |

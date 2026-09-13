# LLM Engineering – Week 2, Day 2 (Part 2)
## Gradio Basics: First UI, Callbacks, and Sharing

> Personal study notes. The callback concept is the one new programming idea here.

---

## READ THIS FIRST (Gradio in 3 lines)

1. Gradio is a Python library that builds a web UI from a function. You write the function, tell Gradio what the inputs and outputs look like, call `.launch()`, and a web page appears.
2. A **callback** = you hand your function to Gradio (like giving someone a recipe card). Gradio calls it when the user presses Submit. You're NOT calling the function yourself.
3. Gradio doesn't know or care what your function does. `shout` (uppercase text) and `message_gpt` (call GPT on the cloud) look the same to Gradio: one input, one output, called on Submit.

---

## 1. First Gradio UI — Four Lines

```python
def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch()
```

### What each piece does

| Piece | Meaning |
|---|---|
| `fn=shout` | "When the user presses Submit, call this function." Not calling `shout()` — handing the function itself to Gradio. That handoff = a **callback**. |
| `inputs="textbox"` | Put a text box on screen; whatever the user types goes into the function's input |
| `outputs="textbox"` | Put another text box; whatever the function returns gets displayed there |
| `flagging_mode="never"` | Turns off a data-science feature (flagging bad results) you don't need |
| `.launch()` | Starts a local web server, generates a React app, shows it. One word does all of that. |

Type "hello" → press Submit → function runs → "HELLO" appears. The `print` statement shows in the notebook below, proving Python actually ran.

The link at the bottom (e.g. `http://127.0.0.1:7860`) opens the same UI in a full browser tab. Each relaunch picks the next port number.

### The callback concept
`fn=shout` passes the function as a variable, not calling it. Like handing someone a recipe card versus cooking the meal yourself. You give Gradio the recipe; it cooks whenever a user presses Submit.

Under the hood, Gradio is running an app server and serving a React front-end. All of that happens inside `.launch()`.

### The "aha" moment: swap one function, get a ChatGPT-like UI

Earlier in the notebook there's a function the lecturer wrote (NOT a Gradio built-in, just ordinary Python):

```python
def message_gpt(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content
```

Takes a string, calls GPT, returns a string. One input, one output — same shape as `shout`.

So swap one word:

```python
fn=shout          # types text in caps
fn=message_gpt    # calls GPT on the cloud
```

Everything else stays identical. Run it, and now you have a ChatGPT-like interface. Type "Hello", press Submit, GPT replies.

**The point:** Gradio doesn't know or care that it just called an LLM. It's a UI framework, not an AI framework. It hooks up input → function → output through a Submit button. Whether the function uppercases text or calls a trillion-parameter model is irrelevant to Gradio. You focus on the Python function (the AI part), Gradio handles the UI part, and neither knows about the other.

### Customizing the UI (more control)

Instead of just `inputs="textbox"`, you can spell out the fields:

```python
message_input = gr.Textbox(label="Your message", info="Enter a message to be shouted", lines=7)
message_output = gr.Textbox(label="Response", lines=8)

view = gr.Interface(
    fn=shout,
    inputs=message_input,
    outputs=message_output,
    title="Shout",
    examples=["Hello", "Howdy"],
    flagging_mode="never"
)
view.launch()
```

Labels, help text, line count, a title, and clickable examples that pre-fill the input. Same callback idea, just more control over the page.

### Small features (reference only)
- `.launch(in_browser=True)` — auto-opens a browser tab
- `.launch(auth=("username", "password"))` — adds login. Pass a list of tuples for multiple users. Don't put real passwords in plain text; use `.env` at minimum
- Dark/light mode can be forced with JavaScript, but Gradio recommends leaving it to the user's system preference
- If your mouse is over the Gradio UI, the scroll wheel scrolls inside it. Move the mouse off to scroll the page.

---

## 2. `share=True` — Public Link

```python
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)
```

One added parameter. What changes:

| | Without `share` | With `share=True` |
|---|---|---|
| Who can access | Only you (localhost) | Anyone with the link |
| URL | `http://127.0.0.1:7860` | `abc123.gradio.live` |
| Where function runs | Your computer | **Still your computer** |

The public server tunnels the request back to your machine. That's called **HTTP tunneling** (same idea as ngrok if you've heard of it).

- The link expires in **one week**.
- For proper permanent hosting: `gradio deploy` (covered in other courses).
- The callback only works while your notebook is running. Stop the notebook → the public link stops working.

### Warning
If you're on a corporate network with strict security, **skip `share=True`**. HTTP tunneling can flag security monitoring. The lecturer was clear about this.

### For JobRadar
`share=True` is how you'd demo it to someone without deploying anything. Show the brochure generating, hand them the link.

---

## 3. How Gradio Actually Works (under the hood)

Gradio does exactly three things. Together they produce the "magical" effect of a UI from one line of Python.

**Step 1: Generate a frontend.** Your Python description (`gr.Textbox`, `gr.ChatInterface`) gets translated into JavaScript using a framework called **Svelte**. You described the UI in Python; Gradio wrote the HTML/JavaScript for you.

**Step 2: Start a web server.** `.launch()` starts a server using **Starlette** (a Python web server framework). Default port: 7860. If taken, it tries 7861, 7862, etc. Anyone visiting `http://localhost:7860` gets the generated frontend. The notebook shows it inline because notebook output cells can render web content (like a mini browser inside the cell).

**Step 3: Wire up callbacks as routes.** For each function you gave Gradio (`fn=chat`), the server creates a backend **route** (a URL path). The generated frontend knows: Submit button → send input to that route → server calls your Python function → result comes back → frontend shows it. All this wiring happens inside `.launch()`.

```
You write: gr.ChatInterface(fn=chat, ...).launch()
      ↓
STEP 1: Gradio generates a Svelte/JavaScript frontend
STEP 2: Gradio starts a Starlette web server on port 7860
STEP 3: Gradio creates a route: Submit → calls chat() → result shown on screen
      ↓
Result: a working web app from one line of Python
```

**Two practical takeaways:**
- Starlette servers are **scalable** — not a toy. Can handle real internal apps with real load.
- Gradio can run in **API-only mode** (no frontend). Build a custom frontend in React/Next.js later, keep Gradio's backend. Natural migration from prototype to production.

---

## How to Explain This to Someone

### If a non-technical person asks "What's a callback?"
"You hand a recipe card to a chef and say 'cook this when a customer orders.' You're not cooking it yourself — you're giving the chef the instructions to use later. In Gradio, you hand your function to Gradio, and Gradio runs it when the user presses Submit."

### If a technical person asks
"`gr.Interface(fn=shout, inputs='textbox', outputs='textbox').launch()` — pass the function reference (not a call) as `fn`; Gradio registers it as a callback bound to a route. `.launch()` generates a Svelte frontend, starts a Starlette server on port 7860, and wires Submit → route → callback → output. `share=True` tunnels via Hugging Face for a temporary public URL. `auth=(user, pass)` adds login. Swapping `fn=shout` for `fn=message_gpt` gives a ChatGPT-like UI with zero other changes."

### The analogy
Handing someone a recipe card (callback) vs cooking the meal yourself (calling the function).

### The one-liner
"A callback is a function you hand to Gradio to run later; .launch() turns it into a web app in one line."

---

## 4. Self-Check

1. What does `fn=shout` do? Why no parentheses after `shout`?
2. What is a callback, in one sentence?
3. What three things does `.launch()` do behind the scenes?
4. What does `share=True` change? Where does the Python function still run?
5. What is HTTP tunneling?
6. When should you skip `share=True`?
7. What frontend framework does Gradio use? What backend framework?
8. How could you migrate a Gradio prototype to a production app with a custom frontend?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| `gr.Interface` | Gradio's simplest UI builder: function + inputs + outputs |
| Callback | A function handed to another piece of code so it can be called later |
| `.launch()` | Does three things: generates frontend, starts server, wires up callbacks |
| Svelte | The JavaScript framework Gradio uses to generate the frontend |
| Starlette | The Python web server framework Gradio uses (scalable, production-capable) |
| Route | A URL path on the server that triggers a specific callback function |
| Port 7860 | Gradio's default port; increments if taken |
| `share=True` | Makes the app publicly accessible via a temporary Hugging Face link |
| HTTP tunneling | Public server forwards requests back to your local machine |
| API-only mode | Run Gradio as just a backend, no generated frontend; for production migration |
| Flagging | A data-science feature to mark bad results; turned off with `flagging_mode="never"` |

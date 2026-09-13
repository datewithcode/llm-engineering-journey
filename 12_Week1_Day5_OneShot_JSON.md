# LLM Engineering – Week 1, Day 5 (Part 2)
## LLM Call #1: One-Shot Prompting, JSON, and `response_format`

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Notebook: week1/day5.ipynb, cells 5–10.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **One-shot prompting** = include ONE example of the answer you want inside the prompt. The model copies the shape. (Zero examples = zero-shot, two or more = multi-shot.)
2. **Why JSON:** the model was trained on tons of JSON, and Python can parse it directly with `json.loads()`. Describing a format in English is unreliable; showing JSON is clean.
3. **`response_format={"type": "json_object"}`** = force the API to return valid JSON. The prompt example makes JSON *likely*; this parameter makes it *guaranteed* by blocking any token that would break the JSON.
4. **The most important lesson:** iterate. Run the prompt, see what's wrong ("it kept returning privacy links"), add a fix ("do not include Privacy"), run again. Nobody writes the perfect prompt first time.

---

## 0. The Rule for Starting Any LLM Task
Start by thinking about the prompts: what input sequence makes the right tokens most likely? Always a system prompt + a user prompt.

---

## 1. The System Prompt — cell 5

```python
link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""
```

### One-shot prompting
**Definition: one example of the desired answer is included in the prompt.** That's it.
- Zero examples = zero-shot. One = one-shot. Two or more = multi-shot.
- Strictly, multi-shot = example question + good answer, repeated. Just multiple example answers also counts loosely.
- Why it works: if the input ends with an example in a certain shape, the most likely next tokens are more text in that shape. Not teaching a rule — making the right shape the most probable continuation.
- (Correction to my first attempt: one-shot is *one specific trick* inside good prompting, not a synonym for it.)

### Why JSON
The lecturer invented this structure himself (`links` key → list → each with `type` and `url`). Models were trained on three kinds of text in bulk:
1. Natural language
2. Markdown (websites turned into markdown; models love generating it)
3. JSON

JSON feels native. Describing a layout in English ("first bullet this, second that") is clumsy and unreliable. Showing JSON is clean, and it comes back as something Python parses directly.

**In my own words:** JSON provides clear key/value responses that are easy to interpret.

*(Week 8: "structured outputs" — forcing JSON to match a strict schema.)*

---

## 2. The User Prompt Function — cells 6–7

```python
def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company,
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt
```

**Why a function, not a variable?** The system prompt never changes → constant. The user prompt changes per URL → function that builds the string fresh: fetch the links, append one per line.

**Cell 7** prints the result for edwarddonner.com. Still no AI — just the string that *will* be sent.

### The "do not include" line — the most important lesson
That line wasn't there originally. The lecturer ran it, the model kept returning privacy-policy links, so he added it. A negative example — the opposite of one-shot.

**The iterate-and-refine loop is THE skill of LLM engineering.** Run it, see what's wrong, adjust the prompt, run again, add examples. Part engineer, part data scientist running experiments. Nobody writes the perfect prompt first time.

---

## 3. The API Call — cell 8

```python
def select_relevant_links(url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    return links
```

- `model=MODEL` → gpt-5-nano
- `messages` → system constant + user function
- `response.choices[0].message.content` → reply text (Day 4)
- `json.loads(result)` → JSON text → Python dict. Ordinary Python.

### The new line: `response_format={"type": "json_object"}`
Tells the API the reply **must** be valid JSON. Not "please" — must.

### How it's enforced (the sneaky part)
The model doesn't pick one next token. At each step it produces a **probability for every token in the vocabulary** ("your" 40%, "the" 20%, "hello" 0.01%...). Normally the highest is picked, or one is sampled.

With `json_object` on, OpenAI's code sits in that picking step and **blocks any token that would break the JSON**. If the text so far is `{"links": [`, a token like `hello` is not allowed, whatever its probability. Only tokens that keep JSON well-formed can be chosen.

**Two things working together:**
- The example in the prompt makes JSON the *most likely* output (soft — the model's own tendency).
- `response_format` makes non-JSON *impossible* (hard — enforced at pick time).

The model doesn't "understand" JSON rules. It just never gets to output a bad token. Same picking-step trick as the "Wait" insertion (Day 3): control at inference time without changing the model.

**In my own words:** `response_format` says the reply must be JSON. Prompt makes JSON *likely*; `response_format` makes it *guaranteed*.

**Cell 10** runs it → a clean Python dict of relevant links with full URLs. Call #1 done.

---

## How to Explain This to Someone

### If a non-technical person asks "How do you get AI to answer in a specific format?"
"Show it an example. If you want a list of links with a type and a URL, put one example of exactly that in your instructions. The AI copies the shape. It's called one-shot prompting — one example. And then there's a setting that forces the reply to be valid JSON so code can read it reliably."

### If a technical person asks
"One-shot prompting: include a single exemplar of the target output format in the system prompt; the model's next-token distribution shifts toward that structure. For guaranteed parseable output, pair it with `response_format={"type": "json_object"}` — the API applies constrained decoding, masking any token that would break JSON validity at sampling time. Prompt makes JSON likely; response_format makes it guaranteed. Iterate on the prompt when outputs drift (e.g., add negative examples)."

### The analogy
The prompt example = showing someone a filled-in form so they fill theirs the same way. `response_format` = the form only accepts valid entries; anything else is rejected at the door.

### The one-liner
"Show one example of the format you want (one-shot), and use response_format to guarantee valid JSON."

---

## 4. Self-Check Questions

1. Define one-shot prompting in one sentence. What are zero-shot and multi-shot?
2. Why does putting an example in the prompt work? (Day 1 idea.)
3. Why JSON rather than describing the layout in English? What three kinds of text were models trained on in bulk?
4. Why is the system prompt a variable but the user prompt a function?
5. Where did the "Do not include..." line come from? What lesson does it teach?
6. What does `response_format={"type": "json_object"}` do?
7. How is it enforced — what happens at the token-picking step?
8. What's the difference between the prompt's example and `response_format`? (soft vs hard)

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| Zero / one / multi-shot | Number of examples included in the prompt |
| Negative example | Telling the model what NOT to produce |
| Iterate | Run, inspect, adjust prompt, run again — the core skill |
| `response_format` | API parameter forcing the reply into a format (here JSON) |
| Probability distribution | The model's score for every possible next token at each step |
| Constrained decoding | Blocking tokens at pick time so output must stay valid (JSON) |
| `json.loads` | Python: JSON text → dict |
| Structured outputs | Week 8: forcing JSON to match a strict schema |

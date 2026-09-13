# LLM Engineering – Week 1, Day 5 (Part 3)
## Running Call #1, Wrapping LLM Calls in Functions, and the Brochure Prompts

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Notebook: week1/day5.ipynb, cells 13-21.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Call #1 worked: the LLM returned a clean Python dict of relevant links, exactly matching the JSON example shape. It kept LinkedIn (relevant to the person) and dropped Hacker News (not relevant). No rule-based code could make that judgment.
2. **Wrapping an LLM call in a plain function:** `fetch_page_and_all_relevant_links(url)` scrapes the home page, calls the LLM to pick links, scrapes those pages, and glues everything into one big text block. From the outside it looks like ordinary Python. That's what agentic workflows are: LLM calls hidden inside normal functions.
3. The brochure prompts: system prompt = "you write brochures, respond in markdown, only include info you actually have." User prompt = "here's the company name and all the page content, write the brochure." Truncated to 5,000 characters to save cost.

---

## 1. Running Call #1 (cells 13–15)

`select_relevant_links("https://edwarddonner.com")` returns a Python dict shaped **exactly** like the example in the system prompt:

```python
{"links": [
    {"type": "home page",  "url": "https://edwarddonner.com/"},
    {"type": "about page", "url": "https://edwarddonner.com/about/"},
    {"type": "blog post",  "url": "..."}
]}
```

- **One-shot prompting worked:** same keys, same shape as the example.
- **The judgment worked:** kept LinkedIn and Facebook (relevant to him personally), dropped Hacker News (not about him). No rule-based code could make that call.

**Cell 13** = same function with two `print` statements ("Selecting relevant links for X...", "Found N relevant links"). Purely to watch progress during the ~30-second call. Good habit for slow steps.

**Cell 15** on `huggingface.co` → 3 relevant links (brand, careers, company) out of many.

**Note:** the count varies between runs (3 one time, 11 or 7 another). Same input, different output — the model samples from probabilities rather than always picking the top token. Expect this.

---

## 2. Wrapping an LLM Call Inside a Plain Function (cell 17)

```python
def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)          # ← this is the AI call
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result
```

1. Scrape the landing page → text
2. `select_relevant_links(url)` → the AI call from part 1
3. Build a big text block: "## Landing Page" + content
4. Loop each relevant link: "### Link: careers page" heading, then scrape and append that page
5. Return one giant string = landing page + every relevant page

`##` and `###` are markdown level-2 and level-3 headings. They give structure so the model can tell where one page ends and the next begins.

### The interesting idea
From the outside, `select_relevant_links(url)` looks like an ordinary Python function call. Inside, it goes to the cloud, runs GPT-5-nano, waits 30 seconds, parses JSON. The caller doesn't know or care.

**That's what agentic workflows are: Python code and LLM calls stitched together, with the LLM calls hidden inside ordinary functions.** No magic — just functions that happen to consult a model.

---

## 3. The Brochure Prompts (cells 19–21)

Same pattern as call #1: system prompt = constant, user prompt = function.

### Cell 19 — system prompt
```python
brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""
```

Three things to notice:
- **"Respond in markdown"** — comes back formatted, ready to display.
- **"without code blocks"** — otherwise the model wraps it in ``` fences and it shows as raw text instead of rendering. Another fix born from experimentation, like the "do not include" line.
- **"if you have the information"** — a guard against hallucination. Without it, the model would invent a culture section for a company that never mentioned one.

**Tone is trivial to change:** the notebook has a commented-out version asking for a "short, humorous, entertaining, witty" brochure. Same code, a few words changed, completely different output.

### Cell 20 — user prompt function
```python
def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000]   # truncate
    return user_prompt
```

Takes company name + URL, writes the instruction, appends the giant text block from part 2.

**The truncation line** `[:5_000]` keeps only the first 5,000 characters. Why: cost and context window. Scraped pages can be enormous; 5,000 chars ≈ 1,250 tokens keeps the call cheap. It's a blunt cut — you lose what follows — but fine for a demo. In production you'd summarize or prioritize instead of chopping.

### Cell 21
Runs it and prints the finished prompt. **No second AI call yet** — you're inspecting what will be sent. It does trigger call #1 internally, which is why it takes ~30 seconds.

---

## How to Explain This to Someone

### If a non-technical person asks "How do you connect AI to regular code?"
"You wrap the AI call inside an ordinary function. From the outside it looks like any other function — you call it, it returns a result. Inside, it sends a request to the AI and waits. The rest of your program doesn't know or care that AI was involved."

### If a technical person asks
"`fetch_page_and_all_relevant_links(url)` wraps `select_relevant_links(url)` (an LLM call) as a regular function. The caller sees a normal Python interface. This is the pattern for agentic workflows: LLM calls become composable functions in a larger pipeline. Prompt design: system prompt sets role and output format ('markdown, no code blocks, only include information you have'), user prompt supplies the data. Truncate input to control cost and context usage."

### The analogy
An LLM call hidden inside a plain function is like a phone call hidden inside a "get quote" button — the person pressing the button doesn't see the call happen.

### The one-liner
"Wrap LLM calls in ordinary functions — that's what agentic workflows are, Python and LLM calls stitched together."

---

## 4. Self-Check Questions

1. What did the returned dict prove about the one-shot example? What did it prove about judgment?
2. Why does the link count change between runs on the same site?
3. What does `fetch_page_and_all_relevant_links` return? Why the `##` and `###` headings?
4. Where is the LLM call hidden in that function, and why does that matter?
5. Why "without code blocks" in the system prompt?
6. Why "if you have the information"?
7. What does `[:5_000]` do and why is it there? What's the downside?
8. Does cell 21 make the brochure call? What does it do?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| Sampling | Model picks from probabilities, so the same input can give different output |
| Progress prints | `print` statements around slow calls so you can watch what's happening |
| `##` / `###` | Markdown level-2 / level-3 headings |
| Agentic workflow | Python code and LLM calls stitched together, LLM calls wrapped in functions |
| "without code blocks" | Stops the model wrapping output in ``` fences |
| Truncation | Cutting input to a character limit to control cost and context usage |

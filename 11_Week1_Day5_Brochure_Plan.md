# LLM Engineering – Week 1, Day 5 (Part 1)
## The Brochure Project: Plan, Two Chained Calls, and the Link Problem

> Personal study notes. Written in plain language, in the order the ideas were learned.
> Notebook: week1/day5.ipynb, cells 1-3 covered here.

---

## READ THIS FIRST (the brochure lab in 5 lines)

1. The project: give a company URL, get a sales brochure built from several pages of their site.
2. Five steps done manually: fetch home page → grab all links → decide which matter → fetch those pages → write the brochure.
3. Python fetches pages (steps 1, 2, 4). The LLM judges relevance (step 3) and writes the brochure (step 5). Neither can do the other's job.
4. That's why it needs TWO LLM calls with Python acting in between: call 1 picks the relevant links, Python fetches them, call 2 writes the brochure.
5. This is the same pattern as tools/agents (week 2, day 4), just done manually instead of with a tool loop.

---

## 1. What We're Building

Day 1: give a URL → summary of one page.
Day 5: give a company URL → a **sales brochure** built from *several* pages of their site, for customers, investors, or job candidates.

### The two-call chain
```
Company URL
   │
   ▼
Python: scrape the home page, collect every link
   │
   ▼
LLM call #1 (gpt-5-nano): "Which links are relevant for a brochure?" → short list as JSON
   │
   ▼
Python: scrape each relevant page
   │
   ▼
LLM call #2 (gpt-4.1-mini): "Here's all the content, write a brochure" → markdown, streamed
```

Call #1's output feeds call #2. **Chaining LLM calls** — the notebook calls this the first taste of agentic design.

### Four techniques today (fancy names, simple things)
- **Chat Completions API** — `openai.chat.completions.create(...)`, already used
- **One-shot prompting** — put one example of the answer you want inside the prompt
- **JSON results** — ask the model to reply in JSON so code can read it
- **Streaming** — typewriter effect, tokens appear as generated

---

## 2. Why Two LLM Calls, Not One? (my question)

**The LLM cannot scrape.** It only reads text you give it and writes text back. No internet, no fetching. Fetching is done by *my Python code*.

| Step | Who can do it |
|---|---|
| Fetch home page, pull out links | Python only |
| Decide which links are relevant | LLM only (needs judgment) |
| Fetch those relevant pages | Python only |
| Write the brochure | LLM only |

Step 3 needs step 2's result. Python can't fetch "relevant pages" until the LLM says which; the LLM can't write until Python has fetched. Control bounces: Python → LLM → **back to Python** → LLM. One call can't pause halfway and wait for Python.

**One call would only work** if you fetched every link's page up front — dozens of mostly irrelevant pages, blowing the context window and cost. The cheap first call exists to filter.

**Next week:** give the LLM a `fetch_page` tool → it can say "fetch /about" mid-task, code runs it, result fed back, it continues (the agent loop). Today, without tools, I do that loop by hand.

---

## 3. RAG vs Tools (my assumption, corrected)

I assumed RAG would let the LLM handle the Python part. Not quite:

- **RAG** = Retrieval-Augmented Generation. Store documents in advance; when a question comes, *code* retrieves relevant pieces and pastes them into the prompt. Still Python doing the fetching. RAG *is* a Python part.
- **Tools / function calling** (next week) = tell the LLM "here's `fetch_page(url)` you can ask for." The LLM writes "call fetch_page('/about')," code runs it, hands text back, LLM continues. This is what I was describing.

Python never disappears — I always write the functions and the loop. What changes is *who decides when to call them*.

| | Who fetches | Who decides what to fetch |
|---|---|---|
| Today (two calls) | Python | Python, using the LLM's list |
| RAG | Python | Python (similarity search) |
| Tools / agents | Python | **LLM** |

---

## 4. "Isn't This Just a GPT Wrapper?"

Yes, ChatGPT could do this with enough prompting. But:
- ChatGPT is itself a product OpenAI engineers built on top of GPT.
- Duolingo's AI chat just calls GPT behind the scenes, and people pay for it: crafted prompts, set-up context, convenience.
- Focused business logic around a model has real commercial value. Today's project is a "GPT wrapper" and that's a fine starting point; the course moves toward bespoke systems over 8 weeks.

---

## 5. Cells 1–3 and the Link Problem

**Cell 1 — imports.** New: `from scraper import fetch_website_links, fetch_website_contents`. Helper functions in a file the lecturer wrote (BeautifulSoup scraping, not AI, don't need the insides).
- `fetch_website_contents(url)` — Day 1, returns page text
- `fetch_website_links(url)` — new, returns every link on the page as a list

**Cell 2 — setup.** Load API key, create client. `MODEL = 'gpt-5-nano'` — cheapest GPT-5, because the first job is easy.

**Cell 3 — try it:**
```python
links = fetch_website_links("https://edwarddonner.com")
links
```
Returns a raw list of every `<a href>` on the page. Dozens.

### Two problems with the raw list
1. **Most are junk** — Hacker News, Y Combinator, Terms of Service, email links. Not about the company.
2. **Some are relative** — `/about` instead of `https://edwarddonner.com/about`. Need full URLs to fetch later.

Problem 2: solvable with ordinary code (fiddly). Problem 1: needs judgment about *meaning*. A LinkedIn profile off-site is relevant; a Hacker News link isn't. No rule can capture that.

**Lecturer's point:** four years ago this was impossible to code. Now it's one cheap API call: hand the LLM the messy list, say "pick the relevant ones, give full URLs," and it does both jobs. Same technique works on resumes, restaurant reviews, support tickets — anything needing human-like categorization.

---

## How to Explain This to Someone

### If a non-technical person asks "What did you build?"
"A tool that reads a company's website and writes a sales brochure. You give it the URL. It reads the home page, finds the important links (About, Careers), reads those too, and writes a brochure from everything it found. Two AI calls: one to pick the important pages, one to write the brochure."

### If a technical person asks
"A two-stage LLM pipeline. Stage 1: scrape the landing page, extract all links, send them to a cheap model (gpt-5-nano) with a one-shot JSON example to classify which are brochure-relevant. Stage 2: scrape those pages, concatenate content, send to a chat model (gpt-4.1-mini) with a brochure-writing system prompt, stream the markdown output. Python orchestrates between stages because the LLM can't fetch URLs itself — that's the tool-calling pattern done manually."

### The analogy
Doing it by hand: open the site → look at the menu → decide which pages matter → open those → write the brochure. Python does the opening, the LLM does the deciding and writing.

### The one-liner
"Two chained LLM calls — one picks the relevant pages, Python fetches them, one writes the brochure."

---

## 6. Self-Check Questions

1. Describe the two-call chain. What does call #1 produce, and where does it go?
2. Why can't this be one LLM call? What can the LLM not do?
3. RAG vs tools — who decides what to fetch in each?
4. What's the answer to "ChatGPT can already do this"?
5. What do `fetch_website_links` and `fetch_website_contents` return?
6. Two problems with the raw link list. Which one needs an LLM and why?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| Chaining LLM calls | Output of one call becomes input to the next |
| One-shot prompting | Including one example of the desired answer in the prompt |
| JSON results | Asking the model to reply in JSON so code can parse it |
| Streaming | Receiving tokens as they're generated (typewriter effect) |
| GPT wrapper | A product built around calls to GPT; still commercially valuable |
| Relative link | `/about` — missing the domain; must be made absolute to fetch |
| RAG | Code retrieves stored documents and puts them in the prompt |
| Tools / function calling | LLM asks code to run a function; code runs it and returns the result |
| BeautifulSoup | Python library for scraping HTML (used inside `scraper.py`) |

# LLM Engineering – Week 5, Day 1 (Part 1)
## RAG: The Small Idea, and a Toy Version for Insurellm

> Personal study notes. You already know the small idea: it's the "belt" trick from the clothes store (file 23), done with real company files.
> Notebook: week5/day1.ipynb

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **RAG = Retrieval Augmented Generation.** Retrieve relevant information, add it to the prompt, let the LLM generate the answer.
2. **Why it exists:** the LLM has never seen your company's private documents. Retraining is expensive and slow. RAG fetches the relevant facts at question time instead. Quick to market, low cost.
3. **The small idea:** when a question arrives, your code searches a **knowledge base** (any collection of useful information) for anything relevant and puts it in the prompt. The LLM never searches; your code does.
4. **The toy version** matches words in the question against employee surnames and product names, then dumps the whole matching documents into the system prompt. It works, but it's a blunt instrument, which sets up the "big idea" next.

5. **Two lessons from testing it:** retrieval fails in two ways (a **miss**: "Who is Avery?" finds nothing; a **wrong match**: "Who is Alex Lancaster?" fetches Avery's file), and conversation **history** can hide a miss, so always test retrieval in a **fresh chat**.

---

## The Picture That Makes It Click: Open-Book Exam

**Closed-book exam:** a very smart student answers from memory only. Ask "Who is Avery Lancaster at Insurellm?" and they've never heard of Insurellm. They either say "I don't know" or make something up. **That's an LLM on its own.**

**Open-book exam:** same student, but before each question someone flips the textbook to the right page and puts it in front of them. The student reads the page and answers correctly. **That's RAG.**

| Exam picture | Real thing |
|---|---|
| The smart student | The LLM |
| The textbook | The company's files (the knowledge base) |
| The person who flips to the right page | Your code |
| Putting the page in front of the student | Adding the retrieved text to the prompt |

**Today's toy page-flipper** has one simple-minded rule: "If I see a name from the book's index in the question, I open that chapter."

```
"Who is Lancaster?" → "Lancaster" is in the index → opens that chapter → correct answer
"Who is Avery?"      → "Avery" isn't in the index (only surnames are) → opens nothing → "I don't know"
```

**Next (the big idea):** a smarter page-flipper that finds pages by **meaning**, not exact words, using vector embeddings (the "meaning map" idea from file 43).

---

## 1. Where We Are: The Second Half of the Course

| Week | Topic |
|---|---|
| 1-4 | Foundations, frontier APIs, open source, model selection |
| **5** | **RAG: an expert question-answering assistant** ← you are here |
| 6 | Capstone begins: fine-tune a frontier model |
| 7 | Fine-tune your own open-source model to compete with frontier ones |
| 8 | Finale: agents |

---

## 2. What RAG Stands For

| Letter | Meaning | In plain words |
|---|---|---|
| **R**etrieval | Find relevant information | Your code searches the knowledge base |
| **A**ugmented | Add it to the prompt | The found text goes into the system prompt |
| **G**eneration | The LLM writes the answer | Same next-token prediction as always |

### WHY RAG exists

| Option | Problem |
|---|---|
| Just ask the LLM | It has never seen your private documents. It will guess or hallucinate. |
| Retrain / fine-tune the model on your documents | Expensive, slow, and must be redone whenever documents change |
| **RAG** | Fetch the relevant facts at question time. Cheap, fast, always up to date. |

The notebook calls RAG "perhaps the most immediately applicable technique" in the course. Commercial products do exactly this: nuanced querying across contracts, product specs, internal wikis.

### It continues what you've already done

Every earlier technique was "put useful information in the prompt":
- Multi-shot prompting: examples in the prompt (file 12)
- Tools: fetched data added to the conversation (file 24)
- Dynamic system prompt: the "belt" hack (file 23)

RAG makes this systematic. **More relevant information in the prompt = more expertise from the LLM.**

---

## 3. The Small Idea (your code in every step)

```
User types: "What are ticket prices to London?"
      ↓
YOUR CODE receives the question
      ↓
YOUR CODE checks: does the question contain a known name? Finds "London"
      ↓
YOUR CODE queries the knowledge base for anything about London
      ↓
YOUR CODE builds the prompt:
    system: "You're an expert assistant. This background info might be relevant: [London data]"
    user:   "What are ticket prices to London?"
      ↓
YOUR CODE sends the prompt to the LLM
      ↓
LLM writes an answer that uses the London data
      ↓
YOUR CODE shows the answer to the user
```

**The LLM never searches anything.** Your code searches, then hands the results over (the phone-helper analogy from file 23).

### Knowledge base
Just a fancy name for a collection of useful information your code can search: a database, a folder of documents, a company shared drive.

### WHY the LLM uses the retrieved data
It generates tokens that are consistent with its input. If the prompt contains "London return ticket: $799," the most likely continuation of an answer about London prices includes $799.

### WHY a bit of irrelevant info is OK
You tell the LLM the context "**might** be relevant." It uses what fits and ignores the rest. (Within limits: too much bloats the prompt, costs more, and degrades accuracy, as in the 1,000-product store example in file 23.)

---

## 4. The Project: Insurellm

| Item | Detail |
|---|---|
| Company | Insurellm, a fictional insurance tech startup |
| Knowledge base | The company's shared drive: folders of employee and product documents |
| Goal | An expert assistant employees can ask about the company, its people, and products |
| Requirements | **Accurate** and **low cost** |
| Model | `gpt-4.1-nano` (cheap, to meet the low-cost requirement) |

This follows week 4's lesson: define the business problem and success criteria (accurate, cheap) before building.

### The knowledge base folder structure

```
week5/knowledge-base/
    company/       ← about Insurellm itself
    contracts/     ← many customer contracts
    employees/     ← one markdown file per employee (e.g. Avery Lancaster.md)
    products/      ← one markdown file per product (e.g. CarLLM, ClaimLLM, all ending in "llm")
```

All files are **markdown**. In Cursor, right-click a file and choose "Open Preview" to see it formatted.

**Today's toy only loads `employees/` and `products/`.** Company and contracts are ignored for now.

**Avery Lancaster** is the co-founder and CEO of Insurellm.

### The data is synthetic (LLM-generated)

Every file is fake data that the lecturer generated with an LLM, the same technique as the week 3 assignment (synthetic data generator).

### A lesson from generating it: LLMs lean overly positive

The first batch of employee reviews was **all glowing**. Every employee "exceeded expectations."

**WHY:** LLMs are fine-tuned on human feedback, and people tend to reward pleasant, positive answers. So models drift toward being effusive and optimistic.

**The fix:** he changed the prompt to ask for a realistic range of performance. That's why even the CEO, Avery Lancaster, has a "below expectations" period during the COVID-19 pandemic.

**The lesson: always check LLM output. It can carry a hidden bias you didn't ask for.** This matters for any synthetic data you generate, and for any LLM output you rely on.

### RAG vs fine-tuning (the lecturer's framing)

Commercial "expert knowledge worker" products already exist that attach to a company's shared drive and answer questions. You can build your own this week.

The older, harder way to get company knowledge into a model was **fine-tuning** (training the model further on your data). **RAG is much quicker to market**, lower cost, and a lower barrier to entry.

### Two small code notes

- **Forward slashes in paths:** `glob.glob("knowledge-base/employees/*")` uses forward slashes. This works on Windows too with `glob`.
- **Stripping punctuation:** the character-by-character line keeps only letters and spaces. A **regex** (regular expression) could do this more concisely, but this version is easier to read.

---

## 5. The Toy RAG in Code

### Step 1: Load every file into a dictionary

```python
knowledge = {}

for filename in glob.glob("knowledge-base/employees/*"):
    name = Path(filename).stem.split(' ')[-1]      # last word of the file name = surname
    with open(filename, "r", encoding="utf-8") as f:
        knowledge[name.lower()] = f.read()          # "lancaster" → the whole file's text

for filename in glob.glob("knowledge-base/products/*"):
    name = Path(filename).stem                      # whole file name = product name
    with open(filename, "r", encoding="utf-8") as f:
        knowledge[name.lower()] = f.read()          # "carllm" → the whole file's text
```

| Piece | Meaning |
|---|---|
| `glob.glob("folder/*")` | List every file in that folder |
| `Path(filename).stem` | File name without the folder path or extension: `"knowledge-base/employees/Avery Lancaster.md"` → `"Avery Lancaster"` |
| `.split(' ')[-1]` | Take the last word, so "Avery Lancaster" becomes "Lancaster" |
| `.lower()` | Lowercase so "Lancaster" and "lancaster" match |

Result: a dictionary like `{"lancaster": "...Avery Lancaster's file...", "carllm": "...CarLLM product doc..."}`

### WHY employees use only the surname, but products use the full name

The page-flipper reads the question **one word at a time**, so every key must be a **single word** or it can never match.

| Folder | File name | Words in the name | Key used |
|---|---|---|---|
| employees | `Avery Lancaster.md` | **two** | `"lancaster"` (surname only) |
| products | `CarLLM.md` | **one** | `"carllm"` (full name) |

If the employee key were the full name `"avery lancaster"`, the question "Who is Avery Lancaster?" splits into `["who", "is", "avery", "lancaster"]`. None of those single words equals `"avery lancaster"`, so it would **never** match.

So for employees the code picks **one** word: the **surname**, because it's more unique than a first name (there could be several Averys, but probably one Lancaster). Products are already one word, so the full name works.

**In the exam picture:** the book's index can only list single words, because the page-flipper scans the question word by word.

**The side effect:** "Who is Avery?" finds nothing, since only `"lancaster"` is in the index.

### Step 2: Find matching words in the question

```python
def get_relevant_context(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())   # keep only letters and spaces
    words = text.lower().split()                                            # lowercase, split into words
    return [knowledge[word] for word in words if word in knowledge]         # any word that's a key → its file
```

Example: "Who is Lancaster and what is carllm?" → words include "lancaster" and "carllm" → returns both whole documents.

(The notebook also shows a longer loop version, `get_relevant_context_simple`. Same logic; the list comprehension is the Pythonic version.)

### Step 3: Wrap the results as text for the prompt

```python
def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        return "There is no additional context relevant to the user's question."
    result = "The following additional context might be relevant in answering the user's question:\n\n"
    result += "\n\n".join(relevant_context)
    return result
```

### Step 4: Add it to the system prompt on every message

```python
SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""

def chat(message, history):
    system_message = SYSTEM_PREFIX + additional_context(message)
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

gr.ChatInterface(chat, type="messages").launch(inbrowser=True)
```

- The context is recalculated for **each new message**, then placed in the system prompt
- "If you don't know the answer, say so" is the anti-hallucination line: with no context found, it admits it instead of inventing
- `inbrowser=True` opens the Gradio app in a browser tab automatically
- Same `gr.ChatInterface` callback from file 23

---

## 5b. The Code Walkthrough, Piece by Piece (the version that clicked)

Same code as section 5, explained one piece at a time using the open-book exam picture.

### Piece 1: The page-flipper builds an index (once, before any questions)

For each file: take the name, keep one word, lowercase it, store the whole file under that word.

```python
{
    "lancaster": "Avery Lancaster is the CEO of Insurellm...",
    "carllm":    "CarLLM is Insurellm's car insurance product...",
}
```

That dictionary **is** the index at the back of the book. Name on the left, whole chapter on the right. (Why surname only for employees: see "WHY employees use only the surname" in section 5.)

### Piece 2: The page-flipper checks the question against the index

```python
def get_relevant_context(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()
    return [knowledge[word] for word in words if word in knowledge]
```

Follow one question: **"Who is Lancaster and what is CarLLM?"**

**Line 1: keep only letters and spaces**
```
"Who is Lancaster and what is CarLLM?"  →  "Who is Lancaster and what is CarLLM"
```
WHY: otherwise the last word is `"carllm?"`, which isn't in the index. One question mark would break the match.

**Line 2: lowercase, then split into single words**
```
["who", "is", "lancaster", "and", "what", "is", "carllm"]
```
WHY lowercase: the index keys were stored lowercase. `"Lancaster"` and `"lancaster"` are different to a computer.

**Line 3: for each word, if it's in the index, grab its chapter**

| Word | In the index? | Action |
|---|---|---|
| who | no | skip |
| is | no | skip |
| lancaster | **yes** | grab Avery Lancaster's file |
| and | no | skip |
| what | no | skip |
| is | no | skip |
| carllm | **yes** | grab the CarLLM file |

Result: a **list** of two whole documents.

**The list comprehension, unpacked.** This one line:
```python
return [knowledge[word] for word in words if word in knowledge]
```
does exactly the same as this loop:
```python
relevant_context = []
for word in words:
    if word in knowledge:
        relevant_context.append(knowledge[word])
return relevant_context
```
Read it as: "give me `knowledge[word]`, for each `word` in `words`, but only if `word` is in `knowledge`."

**Gotcha:** "What is CarLLM's price?" → removing the apostrophe gives `"carllms"`, which isn't in the index. Nothing found.

**Exam picture:** the page-flipper reads the question word by word, checks each word against the index, and pulls out every chapter that matches.

### Piece 3: The page-flipper staples the pages together with a note on top

A prompt is **one block of text**, not a list. So the list becomes one string:

```python
def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        return "There is no additional context relevant to the user's question."
    result = "The following additional context might be relevant in answering the user's question:\n\n"
    result += "\n\n".join(relevant_context)
    return result
```

**Outcome A: nothing found** ("Who is Avery?")
```
There is no additional context relevant to the user's question.
```
WHY say this instead of returning nothing: it tells the LLM clearly it has no pages. Combined with "If you don't know the answer, say so" in the system prompt, it answers "I don't know" instead of inventing.

**Outcome B: chapters found** ("Who is Lancaster and what is CarLLM?")
```
The following additional context might be relevant in answering the user's question:

Avery Lancaster is the CEO...

CarLLM is Insurellm's car insurance product...
```

**What `"\n\n".join(...)` does:** glues list items into one string with a blank line between each (`\n` = new line, `\n\n` = a blank line).
```python
"\n\n".join(["A", "B", "C"])    # → "A\n\nB\n\nC"
```

WHY "might be relevant": gives the LLM permission to ignore parts that don't fit. The page-flipper isn't smart, so some pages may not help.

**Exam picture:** the page-flipper staples the chapters together and sticks a note on top: "These pages might help." If nothing matched, it hands over just a note: "I couldn't find any relevant pages."

### Piece 4: The pages go onto the student's desk with the question

```python
def chat(message, history):
    system_message = SYSTEM_PREFIX + additional_context(message)
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content
```

The only new line is the first one: **system prompt = fixed instructions + the stapled pages.** For "Who is Lancaster?" the system prompt becomes:

```
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
The following additional context might be relevant in answering the user's question:

Avery Lancaster is the CEO of Insurellm...
```

The rest is the same `chat` shape since week 2: system prompt, then history, then the new question, sent to the LLM.

**Exam picture:** the page-flipper places the stapled pages on the student's desk next to the question. The student reads both and writes the answer.

### The full flow (your code in every step)

```
User types "Who is Lancaster?" into Gradio
      ↓
Gradio calls chat(message, history)
      ↓
YOUR CODE (piece 2) finds "lancaster" in the index → grabs Avery's file
      ↓
YOUR CODE (piece 3) staples it with a note: "might be relevant"
      ↓
YOUR CODE (piece 4) puts fixed instructions + stapled pages into the system prompt
      ↓
YOUR CODE sends system + history + question to gpt-4.1-nano
      ↓
LLM reads the pages and writes: "Avery Lancaster is the CEO of Insurellm."
      ↓
YOUR CODE returns the reply → Gradio shows it
```

### One thing to notice: follow-up questions

`additional_context(message)` searches only the **current** message. Ask "Who is Lancaster?" then "What's her role?" and the second question contains no name, so **retrieval finds no pages**.

**But the LLM may still answer correctly**, because the whole conversation history is sent too, and the earlier answer about Avery is in it. In the exam picture: the page-flipper brought no pages, but the student can still read the transcript of everything said earlier. This is the **history trap** (section 6b): it can hide retrieval failures when you test.

---

## 6. Why It's a "Blunt Instrument" (limitations)

You can spot these just by reading the code:

| Question | What happens | Why |
|---|---|---|
| "Who is Avery?" | Nothing found | Only the surname is a key |
| "What is CarLLM's price?" | Nothing found | Stripping the apostrophe gives "carllms", not "carllm" |
| "Tell me about the car insurance product" | Nothing found | The meaning matches, but the exact word doesn't |
| "Who is Lancaster?" then "What's her role?" | Retrieval finds nothing for the second question (though history may still rescue the answer, see 6b) | Context is searched from the current message only |
| **"Who is Alex Lancaster?"** | **Fetches Avery Lancaster's file: the wrong person** | "lancaster" matches; the code never checks the first name |
| Any match at all | The whole document is dumped in | No way to pick just the relevant section |

### Two kinds of failure

| Failure | Example | Result |
|---|---|---|
| **Miss** (finds nothing) | "Who is Avery?" | No context, so the LLM says "I don't know" |
| **Wrong match** (finds the wrong thing) | "Who is Alex Lancaster?" | Avery Lancaster's file is fetched for a question about someone else |

In the exam picture: a miss means the page-flipper brings no pages. A wrong match means it confidently brings the **wrong** pages.

**Where "Alex Lancaster" comes from:** the notebook's test question `additional_context("Who is Alex Lancaster?")` is a **deliberate trick** to show the wrong-match failure. The real CEO is Avery Lancaster.

**An easy fix the lecturer deliberately skips:** also store each employee under their **first name**, which would fix "Who is Avery?". He leaves it out to show how brittle exact word matching is. (A typo like "Lancastre" would still fail.)

These are the same weaknesses of keyword matching as "belt" vs "waist strap" (file 23). **Exact word matching can't match meaning.** That sets up the "big idea" behind RAG in the next lecture.

---

## 6b. The Conversation History Trap (important when testing)

### What happened in the demo
In **one** chat:
1. "Who is Avery Lancaster?" → retrieval finds "lancaster" → correct answer
2. "Who is Avery?" → retrieval finds **nothing** → yet the answer is still correct: "Avery refers to Avery Lancaster, co-founder and CEO"

### WHY
Every call sends the **whole conversation history** (system prompt + history + new message). The earlier answer about Avery Lancaster is in that history, so the LLM answers from history, not from retrieval.

### Proving it with a fresh chat
Rerun the Gradio cell to get a **brand-new chat**, then ask "Who is Avery?" Now: "I don't have information about Avery." Ask "who is lancaster" (lowercase works) and it answers. From then on in that chat, "Avery" works too, because of history.

### The testing lesson
**When testing whether retrieval works, start a fresh chat for each test.** Otherwise earlier answers can hide a retrieval failure and make your RAG look better than it is.

---

## 6c. More Demo Questions

| Question | Result |
|---|---|
| "Who is Avery Lancaster?" | Co-founder and CEO of Insurellm |
| "What is carllm?" | An auto insurance product developed by Insurellm |
| "Who is Thompson?" | Maxine Thompson, a senior data engineer |
| A pricing question about one of the products | Answered correctly from the product document |

You're not limited to "what is X." Deeper questions work too, because the whole document is in the prompt.

### Suggested exercise
Add `print` statements to see the **retrieved context** and the **full prompt** sent to the LLM. It builds intuition for exactly what the model sees.

### What the big idea will fix
The goal: **fuzzy matching**. Find the right context even if the user types a first name, misspells "Lancaster," or describes something instead of naming it. That's what real RAG solves.

---

## 7. How to Explain This to Someone

### If a non-technical person asks "What is RAG?"

"An AI like ChatGPT doesn't know anything about your company's private files. RAG fixes that without retraining it. When someone asks a question, the system first looks through your company documents for anything relevant, then hands those pages to the AI along with the question. The AI reads them and answers. It's like giving an expert consultant the right folder before they answer."

### If a technical person asks

"RAG augments generation with retrieved context: at query time, retrieve relevant documents from a knowledge base and inject them into the prompt, typically the system message. The toy version here is keyword retrieval: a dict mapping surnames and product names to full documents, matched against tokenized, normalized query words. It's brittle (no fuzzy or semantic matching, no chunking, no conversation-aware retrieval), which is what embedding-based vector retrieval solves."

### The analogy

A consultant who's brilliant but has never seen your company. Before each question, an assistant runs to the filing cabinet and pulls out the folders that seem relevant. The consultant reads them and answers. The assistant is your code; the filing cabinet is the knowledge base; the consultant is the LLM.

### The one-liner

"RAG means your code finds the relevant documents first, then gives them to the LLM with the question."

---

## 8. Self-Check

1. What do the R, A, and G in RAG stand for?
2. Why use RAG instead of retraining the model on company documents?
3. In the flow, who searches the knowledge base: the LLM or your code?
4. What is a knowledge base?
5. What are Insurellm's two requirements, and how does the model choice reflect one of them?
6. For employees, what's the dictionary key? For products?
7. What does `get_relevant_context` do, step by step?
8. Why does "Who is Avery?" find nothing?
9. A follow-up like "What's her role?" finds no context. Why might the LLM still answer correctly?
10. How is this toy version the same idea as the "belt" hack from week 2?
11. What are the four folders in the knowledge base? Which two does the toy load?
12. Why were the first LLM-generated employee reviews all glowing? What's the lesson?
13. Why is RAG quicker to market than fine-tuning?
14. What are the two kinds of retrieval failure? Give an example of each.
15. Why does "Who is Alex Lancaster?" return the wrong person's file?
16. Why should you start a fresh chat when testing retrieval?

---

## 9. Quick Glossary

| Term | Plain meaning |
|---|---|
| RAG | Retrieval Augmented Generation: find relevant info, add it to the prompt, generate the answer |
| Retrieval | Searching the knowledge base for relevant information |
| Knowledge base | Any searchable collection of useful information (database, documents, shared drive) |
| Context | The retrieved text added to the prompt |
| Insurellm | The fictional insurance tech company used as this week's project |
| `glob.glob` | Python function to list files matching a pattern |
| `Path(...).stem` | File name without folder path or extension |
| Keyword matching | Finding documents by exact word matches (brittle, can't match meaning) |
| Blunt instrument | A simple approach that works but lacks precision |

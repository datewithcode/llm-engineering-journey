# LLM Engineering – Week 2, Day 4 (Part 1)
## Tools: What They Are and How They Actually Work

> Personal study notes. This is the foundation of everything agentic.
> The boss-and-secretary analogy is the version that made it click.

---

## READ THIS FIRST (the whole lecture in 5 lines)

1. A "tool" is a Python function YOU wrote (database lookup, price check, booking). The LLM cannot run it.
2. You TELL the LLM what tools exist by describing them in JSON when you call the API.
3. If the LLM needs a tool, its reply says "please run this tool" instead of answering the customer.
4. YOUR CODE checks the reply, sees the tool request, runs the function, gets the result.
5. YOUR CODE calls the LLM a SECOND time with the result added to the history. Now the LLM answers the customer.

**Two LLM calls, one tool call in between, all orchestrated by your code. The LLM only ever reads and writes text.**

---

## 1. The Scary Version (wrong)

People imagine: the LLM reaches out of its box, runs code on your computer, searches a database, books a flight. Like it has arms and legs.

**Reality: the LLM just writes text that says "please call this tool."** It never calls anything. It never runs code. It never touches a database. It produces tokens, same as always. Some of those tokens happen to say "I'd like you to run a tool."

---

## 2. The Boss and Secretary Analogy

**The boss (LLM):** locked in an office. Can only read notes and write notes. Cannot use a phone, cannot leave, cannot do any real-world action. But very smart — understands language, makes judgments, writes beautifully.

**The secretary (your Python code):** sits outside the office. Can use the phone, look things up, run tools, talk to the customer. But cannot understand language or make judgments — just follows instructions.

**The customer** never talks to the boss directly. Everything goes through the secretary.

```
Customer ←→ YOUR CODE (secretary) ←→ LLM (boss)
                  ↕
            Tools (phone, database)
```

### Why you need BOTH

| Job | Who can do it | Why |
|---|---|---|
| Understand "beach, warm, Europe" | Boss only | Language understanding |
| Decide which cities to look up | Boss only | Judgment |
| Actually look up the prices | Secretary only | Boss has no phone |
| Write a friendly, natural reply | Boss only | Language generation |
| Show the reply to the customer | Secretary only | Boss is locked in the office |

**LLM = the brain (understands, decides, writes). Your code = the hands (fetches, runs, delivers).**

### The customer always goes to the secretary first
The customer NEVER talks to the boss directly. Everything goes through the secretary (your code). The secretary receives the question, writes it on a note, slides it under the door. The customer doesn't even know the boss exists.

### What happens if the secretary works alone (no LLM)?
Customer asks: "I'm thinking about a beach holiday somewhere warm, maybe Europe. What would that cost?"

Your code sees this message. Now what?
- Which city should it look up? The customer didn't name one.
- Is it Paris? Barcelona? Athens? Crete?
- Should it suggest multiple options?
- How should it respond in a friendly way?

Your code can't figure any of that out. It can run `fetch_price("Paris")` but only if someone TELLS it to fetch Paris. It doesn't understand language. It just follows instructions. **Hands without a brain.**

### What happens if the boss works alone (no tools)?
Same question. The LLM understands perfectly: "beach + warm + Europe = probably Greece, Spain, southern France." It could suggest three cities and write a beautiful reply.

But it doesn't know today's prices. It was trained months ago. Prices change daily. If it guesses, it hallucinates. It's locked in the office with no phone. **Brain without hands.**

### Both together — the beach holiday example
```
Customer: "I'm thinking about a beach holiday somewhere warm, maybe Europe."
      ↓
Secretary receives the question (can't understand it)
      ↓
Secretary slides it to Boss
      ↓
Boss reads it, THINKS: "beach + warm + Europe = Barcelona, Athens, Nice"
Boss writes back: "Please run:
  fetch_price('Barcelona')
  fetch_price('Athens')
  fetch_price('Nice')"
      ↓
Secretary runs all three lookups → $199, $249, $279
      ↓
Secretary slides results back to Boss
      ↓
Boss writes: "Great news! Here are some beautiful beach destinations:
  Barcelona — $199, Athens — $249, Nice — $279.
  Barcelona is the best deal right now!"
      ↓
Secretary shows it to customer
```

The boss chose which cities. The secretary looked up the prices. The boss wrote the friendly reply. Neither could do this alone.

---

## 3. The Five Steps, Note by Note

Customer asks: "How much is a flight to Paris?"

**Note 1: Secretary → Boss (first LLM call)**
Secretary writes a note with: the job description, a list of tools available, and the customer's question. Slides it under the door.

```python
messages = [
    {"role": "system", "content": "You are an airline support agent"},
    {"role": "user", "content": "How much is a flight to Paris?"}
]
tools = [{"name": "fetch_price", "parameters": {"city": "string"}}]
response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
```

**Note 2: Boss → Secretary (LLM's reply)**
Boss doesn't know the price. But he sees the secretary can look it up. He writes back: "Please run fetch_price('Paris')"

The LLM didn't run anything. It wrote text that says "run this tool." That's all.

**Note 3: Secretary does the actual work**
Secretary reads the note, picks up the phone, gets the answer: $299.

```python
def fetch_price(city):
    prices = {"Paris": 299, "London": 249, "Tokyo": 599}
    return prices.get(city, "Unknown")

price = fetch_price("Paris")   # YOUR code runs, gets 299
```

**Note 4: Secretary → Boss (second LLM call)**
Secretary writes a new note with the FULL history: the original question, the tool request, and the tool result. Slides it under the door.

```python
messages = [
    {"role": "system", "content": "You are an airline support agent"},
    {"role": "user", "content": "How much is a flight to Paris?"},
    {"role": "assistant", "tool_calls": [...]},     # boss asked for the tool
    {"role": "tool", "content": "299"},              # result from the tool
]
response = openai.chat.completions.create(model=MODEL, messages=messages)
```

Full history goes back — the LLM is stateless (illusion of memory, same as always). The tool result is just another item in the list, with `role: "tool"`.

**Why TWO LLM calls?** The LLM can't pause mid-reply, wait for your code to run a function, then continue. Each call is one complete read-and-write. So: call 1 = "what should I do?" (answer: use a tool). Your code runs the tool. Call 2 = "here's the tool result, now answer the customer." Same reason the brochure lab needed two calls — your code has to act in between.

**The fourth role.** You learned three roles on Day 3: `system`, `user`, `assistant`. Now there's a fourth: `"tool"`. It means "this is the result that came back from a tool your code ran." The LLM has been trained to recognize it and use the information in its next answer.

**Note 5: Boss → Secretary (final answer)**
Boss reads the whole history, sees $299, writes a reply for the customer.

```python
response.choices[0].message.content
# "A flight to Paris costs $299! Would you like to book one?"
```

Normal text. No tool call. Secretary shows it to the customer. Done.

---

## 4. The Flow as a Picture

```
Customer: "How much is a flight to Paris?"
      ↓
YOUR CODE sends question + tool descriptions to LLM     ← Note 1
      ↓
LLM replies: "call fetch_price('Paris')"                ← Note 2 (just text!)
      ↓
YOUR CODE runs fetch_price("Paris") → $299              ← Note 3 (real work)
      ↓
YOUR CODE sends full history + tool result to LLM       ← Note 4
      ↓
LLM replies: "A flight to Paris costs $299!"            ← Note 5 (final answer)
      ↓
YOUR CODE shows it to the customer
```

---

## 5. What If No Tool Is Needed?

Customer asks: "What's your refund policy?"

The LLM doesn't need a price — it can answer from its training or the system prompt. So it just replies with the answer. Normal text, no tool request. **One call, done.**

```python
response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

# Check: did the LLM ask for a tool, or did it just answer?
if response.choices[0].message.tool_calls:
    # YES — the LLM wants a tool. Run it yourself, then call the LLM again.
    tool_name = response.choices[0].message.tool_calls[0].function.name   # e.g. "fetch_price"
    tool_args = response.choices[0].message.tool_calls[0].function.arguments  # e.g. '{"city":"Paris"}'
    result = fetch_price("Paris")   # YOUR code runs the function
    # ... add result to messages, call the LLM a second time ...
else:
    # NO tool needed — the LLM answered directly. Show it to the customer.
    print(response.choices[0].message.content)
```

Tools are **optional**. You list them so the LLM *can* use them. It only asks for one when it actually needs it.

---

## 6. Three Things That Are NOT Happening

1. The LLM does NOT run your function. It writes "please run this." Your code runs it.
2. The LLM does NOT reach into your computer. Your code is the only thing that runs locally.
3. The LLM does NOT remember the first call. The second call includes the full history, same as always.

---

## 7. How the LLM Knows About Tools

In the first call, you include a `tools` parameter describing what tools exist, in JSON. Here's what it actually looks like:

```python
tools = [{
    "type": "function",
    "function": {
        "name": "fetch_price",                          # the function name
        "description": "Look up the ticket price for a city",  # plain English for the LLM
        "parameters": {                                  # what arguments the function takes
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The destination city"}
            },
            "required": ["city"]
        }
    }
}]
```

This is NOT code the LLM runs. It's a DESCRIPTION — like handing the boss a menu of what the secretary can do. The LLM reads the description and decides whether to ask for a tool. It has been trained on this JSON format, so it knows how to reply with a matching tool request.

The lecturer's live proof: he typed into ChatGPT (no API, just the chat product):
```
You are a support agent. You can query ticket prices.
Just respond "USE TOOL fetch_price(city)" to look up a price.
User: I'd like to go to Paris. How much is a flight?
```
ChatGPT replied: `USE TOOL fetch_price(Paris)`

It didn't run anything. It wrote text matching the pattern it was told to use. That's all tool calling is.

---

## 8. Connecting to What I Already Know

| Earlier concept | How it appears in tools |
|---|---|
| LLM = autocomplete (Day 1) | Tool calls are just predicted tokens like any other output |
| Stateless / illusion of memory (Day 4) | Second call includes full history with tool result added |
| Chaining LLM calls (Day 5 brochure) | Same pattern: call 1 → your code acts → call 2 |
| Agentic AI = LLM in a loop with tools (Day 4) | This IS that loop |
| Context engineering (Day 4) | Tool descriptions are context that enables new behavior |

**In my own words:** LLM understands the user's text and can reply, but cannot perform actions by itself. So we use tools — your code acts as the hands. The LLM tells your code what to do, your code does it, returns the result to the LLM, and the LLM writes the final answer.

---

## 9. What Do People Use Tools For? (five common types)

A tool is a Python function YOU write. The LLM only sees a description of it. Here are five common types:

| Tool type | What it does | Example |
|---|---|---|
| **Database lookup** | Fetch information the model doesn't have | "What's the price for Paris?" → your function queries a database, returns $299 |
| **Take an action** | Do something in the real world | Book a meeting, send an email, buy airline tickets |
| **Calculation** | Do maths (LLMs are famously bad at it) | LLM asks "multiply 47.3 × 928" → your function returns 43,894.4. ChatGPT likely has this built in |
| **Run code** | Execute Python in a sandboxed environment (Docker container) | The LLM writes code, your tool runs it safely, returns output. Called a **coder agent** |
| **Modify the UI** | Produce something visual immediately | Generate a chart that appears on the user's screen |

The pattern is always: the LLM asks (by writing text), your code does (by running the function).

### The phone-and-friend analogy

You can think and talk, but can't use your hands. You sit in a chair. Your friend sits next to you with a phone.

- You = the LLM. Can think, can speak, cannot act.
- Your friend = your Python code (the secretary). Can use hands, but only does what you ask.
- Google Maps = one tool (lookup).
- Booking app = another tool (action).

```
You say to friend: "Open Maps, search restaurants near me"
Friend opens Maps, reads results, tells you: "Pizza 5 min, biryani 10 min"
You say to friend: "Book a table at biryani for 7pm"
Friend opens booking app, books it, tells you: "Done"
```

Without your friend, you know you want biryani but can't find or book it.
Without you, your friend has hands but doesn't know what to search for.

### Who writes these tool functions?

**You, the engineer.** Ordinary Python functions:

```python
def search_restaurants(location):
    # YOUR code that calls Google Maps API
    results = google_maps.search(location)
    return results

def book_table(restaurant, time):
    # YOUR code that calls a booking service
    booking = booking_api.reserve(restaurant, time)
    return booking
```

You write them. You decide what they do. The LLM never sees the code. It only sees the *description* you give it in the `tools` JSON: "search_restaurants finds nearby restaurants." Based on that description, it decides when to ask for one.

---

## 10. Tools as the Foundation of Agentic AI

### Tool calling vs agentic AI

**Tool calling (this lecture):** secretary sends message to LLM → LLM asks for one tool → secretary runs it → secretary sends result to LLM → LLM writes the final answer → secretary shows it to customer. **One loop. Done.**

**Agentic AI = the same loop running multiple times, LLM deciding each step:**

```
Customer types "Plan my whole trip to Japan" into the UI
      ↓
SECRETARY receives it
      ↓
SECRETARY sends it to LLM
      ↓
LLM writes back to secretary: "run search_flights(Tokyo)"
      ↓
SECRETARY runs search_flights → 3 results
      ↓
SECRETARY sends results to LLM
      ↓
LLM writes back to secretary: "run search_hotels(Tokyo, March 10-17)"
      ↓
SECRETARY runs search_hotels → 4 results
      ↓
SECRETARY sends results to LLM
      ↓
LLM writes back to secretary: "run book_flight(Flight 302)"
      ↓
SECRETARY runs book_flight → booked
      ↓
SECRETARY sends confirmation to LLM
      ↓
LLM writes: "Here's your complete itinerary!"
      ↓
SECRETARY shows it to customer
```

Same boss-and-secretary. Same notes under the door. Just **more rounds**. Nobody told the LLM "flights first, then hotels." It figured out the order.

| Term | What it means |
|---|---|
| **Tool** | One function you wrote |
| **Tool calling** | LLM asks your code to run one tool, once |
| **Agentic AI** | LLM keeps asking for tools in a loop, deciding each step, until done |

Agentic AI is NOT a different thing from tool calling. It's tool calling **repeated in a loop**, with the LLM steering.

### Two specific agentic ideas from the lecture

**Idea 1: A tool that calls another LLM (orchestration).**

```
Customer sends "Translate this brochure to Spanish" to SECRETARY
      ↓
SECRETARY sends it to MAIN LLM
      ↓
Main LLM writes to secretary: "run translate_tool(text, Spanish)"
      ↓
SECRETARY runs translate_tool → which calls a DIFFERENT LLM specialized in translation
      ↓
Translation result comes back to SECRETARY
      ↓
SECRETARY sends it to main LLM
      ↓
Main LLM writes the final answer including the translation
      ↓
SECRETARY shows it to customer
```

The main LLM controlled a workflow of other LLM calls. **Orchestration.**

**Idea 2: A to-do list tool (the agentic loop).**

```
SECRETARY sends the task to LLM
      ↓
LLM writes a to-do list:
  1. Fetch the careers page
  2. Extract job postings
  3. Score each posting
  4. Write a summary
      ↓
LLM writes to secretary: "run step 1"
      ↓
SECRETARY does it → result back to LLM
      ↓
LLM writes: "Step 1 done ✓. Run step 2"
      ↓
SECRETARY does it → result back to LLM
      ↓
...continues until all steps done...
      ↓
LLM writes: "All done. Here's the summary."
      ↓
SECRETARY shows it to customer
```

This is the **agentic loop**: plan → execute (via tools) → evaluate → continue. You saw this with Claude Code: the to-do list on screen, items ticked off one by one.

---

## 11. What If the User Gives Incomplete Information?

Customer says "Plan my trip to Japan" but doesn't say when, from where, or budget. What happens?

**The LLM gathers info BEFORE using tools.** A well-prompted LLM doesn't guess. It asks. The secretary is in EVERY step.

```
Customer types: "Plan my trip to Japan"
      ↓
SECRETARY receives it
      ↓
SECRETARY sends it to LLM (with system prompt, tool descriptions, full history)
      ↓
LLM reads it. Doesn't have enough info to search. Writes back to SECRETARY:
   "I'd love to help! A few things I need:
    - What dates?
    - Flying from which city?
    - Budget range?"
      ↓
SECRETARY shows that text to the customer on screen
      ↓
Customer types: "March 10-17, from Toronto, budget $3000"
      ↓
SECRETARY receives it
      ↓
SECRETARY sends FULL HISTORY to LLM (system + previous exchange + new message)
      ↓
LLM now has enough info. Writes back to SECRETARY: "run search_flights(Toronto, Tokyo, March 10)"
      ↓
SECRETARY sees it's a tool request. Runs search_flights → finds 3 flights
      ↓
SECRETARY sends result back to LLM
      ↓
LLM writes back to SECRETARY: "I found 3 flights:
   1. Air Canada $800
   2. JAL $950 (direct)
   3. Budget Air $600 (2 stops)
   Which one would you prefer?"
      ↓
SECRETARY shows that to the customer on screen
      ↓
Customer types: "JAL please"
      ↓
SECRETARY receives it
      ↓
SECRETARY sends full history to LLM
      ↓
LLM writes to SECRETARY: "run book_flight(JAL, March 10)"
      ↓
SECRETARY runs book_flight → booked
      ↓
SECRETARY sends confirmation to LLM
      ↓
LLM writes: "Your JAL flight is booked! Now let me search hotels..."
      ↓
SECRETARY shows that to customer, AND the loop continues for hotels...
```

### Two rules you control through the system prompt

**Rule 1: Gather before acting.**
```
system: "Before booking anything, confirm all details with the customer first."
```
This prevents the LLM from guessing dates or cities.

**Rule 2: Confirm before irreversible actions.**
```
system: "Search freely, but never book without the customer's explicit confirmation."
```
Searching = safe (just looking). Booking = irreversible (costs money). The LLM asks the customer (through the secretary) before doing anything permanent.

**Who decides these rules? You, the engineer.** Your system prompt is the difference between "autonomous" (LLM steers the process, asks at decision points) and "reckless" (LLM acts without checking).

### Who does what in a multi-step agentic flow

| Job | Who does it |
|---|---|
| Receive the customer's messages | Secretary (your code) |
| Send messages to the LLM | Secretary |
| Decide what step to do next | LLM (the boss) |
| Ask the customer for missing info | LLM writes it → secretary shows it |
| Run tools (search, book, calculate) | Secretary |
| Send tool results to the LLM | Secretary |
| Write the answer for the customer | LLM |
| Show the answer to the customer | Secretary |
| Decide the guardrails (gather first, confirm before booking) | You, the engineer, via system prompt |

**Nobody talks directly to anyone else. Every message goes through the secretary (your code).**

---

## How to Explain This to Someone

### If a non-technical person asks "How does AI book a flight or check a price?"
"It doesn't — not directly. The AI is like a boss locked in an office who can only read and write notes. Your code is the secretary outside. When the AI needs a price, it writes a note: 'please look up the price for Paris.' The secretary (your code) does the lookup, writes the answer on a new note, and slides it back. The AI reads the answer and replies to the customer. The AI never touched a database. It just wrote a note asking for one."

### If a technical person asks
"Tool calling: pass a `tools` array of JSON function schemas with the request. If the model decides a tool is needed, it returns `finish_reason='tool_calls'` with structured arguments instead of content. Your code executes the function, appends both the assistant's tool-call message and a `role: 'tool'` result message to the history, and calls the model again. The model produces the final answer conditioned on the tool result. Two calls minimum; wrap in a `while` loop for multi-step. The model never executes anything — it emits structured tokens your runtime interprets."

### The analogy
The boss (LLM) locked in an office, can only pass notes. The secretary (your code) outside, has hands, does the work. Every message goes through the secretary. Brain without hands + hands without a brain.

### The one-liner
"The LLM writes 'please run this tool'; your code runs it, sends the result back, and the LLM answers — the model never executes anything."

---

## 12. Self-Check

1. Does the LLM run your tool function? What actually runs it?
2. Walk through the five notes for "How much is a flight to Paris?" — name who does each step.
3. What happens if the LLM doesn't need a tool?
4. How does the LLM know what tools are available?
5. Why can't the secretary work alone? Why can't the boss work alone? Use the beach holiday example.
6. What role does the tool result have in the messages list? What number role is it (first, second...)?
7. How is the tool-calling flow similar to the Day 5 brochure flow?
8. Name five common types of tools with an example of each.
9. Who writes the tool functions?
10. What's the difference between tool calling and agentic AI? (One sentence.)
11. What are the two agentic ideas from the lecture? (Orchestration and to-do list.)
12. What happens when the customer gives incomplete info? Who decides whether the LLM asks first?
13. Walk through the Japan trip flow. Who is between the customer and LLM at every step?

---

## 13. Quick Glossary

| Term | Plain meaning |
|---|---|
| Tool | A Python function YOUR code can run on the LLM's behalf (database lookup, calculation, API call). The LLM never runs it. |
| Tool call | The LLM's reply that says "please run this tool with these arguments." Just text, not execution. |
| Tool calling / function calling | The whole process: LLM asks for a tool, your code runs it, sends result back. The name for the workflow. |
| `tools` parameter | JSON descriptions of available tools, sent with the API call. Like a menu of what the secretary can do. |
| `role: "tool"` | The FOURTH role (after system, user, assistant). Contains the result from a tool your code ran. |
| All four roles | `system` (instructions), `user` (customer's messages), `assistant` (LLM's own replies), `tool` (tool results) |
| Tool loop | Secretary sends to LLM → tool requested? → secretary runs it → secretary sends result to LLM → answer |
| Why two calls | The LLM can't pause mid-reply. Call 1 = "use a tool." Your code runs it. Call 2 = "here's the result, now answer." |
| The boss | The LLM: understands, decides, writes. Cannot act. Brain without hands. |
| The secretary | Your Python code: acts, fetches, runs, passes ALL messages. Cannot understand or decide. Hands without a brain. |
| Coder agent | An LLM with a tool that executes code in a sandboxed environment (like Docker). Not "writes code" but "can run code." |
| Orchestration | A tool that calls another LLM. Main LLM controls other LLM calls. Core agentic idea #1. |
| Agentic loop / to-do list | LLM plans steps, secretary executes them one by one, LLM evaluates, continues until done. Core agentic idea #2. |
| Agentic AI | Tool calling repeated in a loop, with the LLM deciding each step. NOT a different thing from tools — just more rounds. |
| Autonomous vs reckless | Autonomous = LLM steers, asks at decision points. Reckless = acts without checking. Your system prompt controls which. |
| Gather before acting | System prompt rule: ask for missing info before using tools. |
| Confirm before irreversible | System prompt rule: search freely, get customer's OK before booking/buying. |

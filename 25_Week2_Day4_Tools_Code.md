# LLM Engineering – Week 2, Day 4 (Part 2)
## The Airline Assistant: Tools in Real Code

> Personal study notes. Written in plain language, every step shows the secretary.
> Notebook: week2/day4.ipynb
> Companion: 24_Week2_Day4_Tools.md (the concept). This file is the code.

---

## READ THIS FIRST (the whole lab in 4 lines)

1. You write a Python function (`get_ticket_price`). You describe it in JSON so the LLM can read the menu. You pass the JSON as `tools=tools` when calling the API.
2. When the LLM needs the tool, its reply has `finish_reason == "tool_calls"` instead of a normal answer. Your code checks for this.
3. Your code runs the function, gets the result, appends BOTH the tool request and the result to the messages list, and calls the LLM a SECOND time. Now the LLM answers the customer.
4. Later improvements: handle multiple tools at once (loop instead of `[0]`), handle multiple rounds (`while` instead of `if` — the agentic loop), and replace the dictionary with a real database.

---

## 1. The Starting Point (no tools, cells 1–4)

Same chat callback from Day 3. System prompt:
```
You are a helpful assistant for an airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
```

"If you don't know the answer, say so" = anti-hallucination line. Works, but can't look up prices — would guess or say "I don't know."

---

## 2. Write the Tool Function (plain Python, no AI)

```python
ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"
```

This is your code. The secretary's phone book. A dictionary lookup. No AI whatsoever.

`.lower()` because the dictionary has lowercase keys but the LLM might send "London" with a capital L.

---

## 3. Describe the Tool in JSON (the menu for the boss)

```python
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
    }
}

tools = [{"type": "function", "function": price_function}]
```

This is NOT the function. It's a DESCRIPTION for the LLM to read. Like a menu entry: "I can look up ticket prices. Tell me a city and I'll get the price."

The format is verbose and annoying. You just have to match this structure. Important parts: `name`, `description`, and `parameters`. The LLM has been trained on this JSON format.

---

## 4. The New Chat Callback (the four notes, in code)

### The four notes (the concept, no code)

**Note 1:** Secretary sends the customer's question + the tool menu to the boss.
**Note 2:** Boss writes back "CALL get_ticket_price, city: London" (not an answer for the customer).
**(Lookup):** Secretary picks up the phone book, finds London = $799.
**Note 3:** Secretary writes a NEW note with full history (question + tool request + tool result), sends to boss.
**Note 4:** Boss reads full history, sees $799, writes: "A flight to London costs $799!"

### The actual code

```python
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    if tool_call.function.name == "get_ticket_price":
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get('destination_city')
        price_details = get_ticket_price(city)
        response = {
            "role": "tool",
            "content": price_details,
            "tool_call_id": tool_call.id
        }
    return response

def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content
```

### Each note mapped to the code

| Note | What happens | The code |
|---|---|---|
| 1 | Secretary sends question + tool menu to boss | `openai.create(messages=messages, tools=tools)` |
| 2 | Secretary checks: did boss ask for a tool? | `if finish_reason == "tool_calls"` |
| (lookup) | Secretary runs the tool herself | `handle_tool_call(message)` which calls `get_ticket_price(city)` |
| 3 | Secretary adds tool request + result to history, sends to boss again | `messages.append(message)` + `messages.append(response)` + `openai.create(messages=messages)` |
| 4 | Boss writes final answer, secretary shows to customer | `return response.choices[0].message.content` |

### The full trace for "How much is a flight to London?"

```
STEP 1: Customer types "How much is a flight to London?" into Gradio

STEP 2: SECRETARY (chat function) receives it via Gradio callback
        message = "How much is a flight to London?"

STEP 3: SECRETARY builds the messages list:
        [system prompt] + [history] + [user: "How much is a flight to London?"]

STEP 4: SECRETARY sends messages + tools JSON to LLM (first call)
        openai.create(model=MODEL, messages=messages, tools=tools)

STEP 5: LLM reads messages and tool menu. Sees get_ticket_price is available.
        Decides it needs the price for London.
        Writes back: finish_reason="tool_calls", function="get_ticket_price", arguments={"destination_city":"London"}

STEP 6: SECRETARY checks: finish_reason == "tool_calls"? YES.

STEP 7: SECRETARY calls handle_tool_call:
        - Reads function name: "get_ticket_price"
        - Reads arguments: {"destination_city": "London"}
        - Calls the ACTUAL Python function: get_ticket_price("London")
        - Gets back: "The price of a ticket to London is $799"
        - Wraps it: {"role": "tool", "content": "The price...is $799", "tool_call_id": "..."}

STEP 8: SECRETARY appends TWO things to the messages list:
        - The LLM's tool request (the boss's note asking for the lookup)
        - The tool result (the answer the secretary found)
        Messages now: [system] + [history] + [user question] + [assistant tool request] + [tool result]

STEP 9: SECRETARY sends the LONGER messages list to LLM (second call)
        openai.create(model=MODEL, messages=messages)

STEP 10: LLM reads full history, sees $799, writes: "A flight to London costs $799!"

STEP 11: SECRETARY checks: finish_reason == "tool_calls"? NO, it's "stop". Normal reply.

STEP 12: SECRETARY returns the text. Gradio shows it to the customer.
```

### What if no tool is needed? ("Hi, how are you?")

Steps 1–4 are the same. At step 5, the LLM replies normally ("I'm great, how can I help?"). At step 6, `finish_reason` is `"stop"`, not `"tool_calls"`. The `if` block is SKIPPED entirely. Step 12 runs: secretary returns the reply. **One call, no tools.**

### handle_tool_call line by line

```python
tool_call = message.tool_calls[0]                        # get the first tool request from the LLM's reply
if tool_call.function.name == "get_ticket_price":        # which tool did the LLM ask for?
    arguments = json.loads(tool_call.function.arguments)  # the LLM sent arguments as JSON text, parse it
    city = arguments.get('destination_city')              # extract the city name
    price_details = get_ticket_price(city)                # RUN YOUR FUNCTION — this is the actual work
    response = {
        "role": "tool",                   # the fourth role (after system, user, assistant)
        "content": price_details,         # what the function returned
        "tool_call_id": tool_call.id      # links this result to the boss's request (just plumbing)
    }
return response
```

---

## 5. Later Improvements (cells at the bottom)

### Improvement 1: Multiple tool calls in one response

The LLM might ask for two prices at once ("London and Paris"). Change `tool_calls[0]` to a loop:

```python
def handle_tool_calls(message):       # note: plural "calls"
    responses = []
    for tool_call in message.tool_calls:    # loop through ALL requests
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price_details = get_ticket_price(city)
            responses.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id
            })
    return responses                  # a LIST of results
```

And `messages.append(response)` becomes `messages.extend(responses)` (adds multiple items to the list instead of one).

### Improvement 2: `while` instead of `if` (the agentic loop)

```python
# Before (one round of tools):
if response.choices[0].finish_reason == "tool_calls":

# After (keep going until the LLM stops asking for tools):
while response.choices[0].finish_reason == "tool_calls":
```

One word changes `if` to `while`. Now the loop keeps running as long as the LLM keeps asking for tools. This is the **agentic loop** from the previous lecture, made real in one word change. The LLM decides when to stop.

**Important: `tools=tools` must be in the second call too.** In the `if` version, the second call had no `tools` because you expected a normal answer. In the `while` version, the LLM might want *another* tool after getting a result ("check London... now check Paris"). Without `tools=tools` in the loop, the LLM can't ask for more tools and the while condition never fires again.

```python
# The while version (complete):
while response.choices[0].finish_reason == "tool_calls":
    message = response.choices[0].message
    responses = handle_tool_calls(message)
    messages.append(message)
    messages.extend(responses)
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    #                                                                        ↑ tools here too!
```

**Infinite loop risk:** LLMs don't tend to loop forever, but it's not prudent to leave a `while` unbounded. In production, add a counter:

```python
max_rounds = 5
rounds = 0
while response.choices[0].finish_reason == "tool_calls" and rounds < max_rounds:
    # ...handle tools...
    rounds += 1
```

### Practical debug tip: print the messages list

Before the second call, add `for m in messages: print(m)`. You'll see every item that goes to the LLM the second time:

```
{"role": "system",    "content": "You are a helpful assistant..."}
{"role": "user",      "content": "Hi there"}
{"role": "assistant", "content": "Hello, how can I assist you?"}
{"role": "user",      "content": "I'd like to go on a trip"}
{"role": "assistant", "content": "Where would you like to travel?"}
{"role": "user",      "content": "To London, please"}
{"role": "assistant", "tool_calls": [{"function": {"name": "get_ticket_price", "arguments": '{"destination_city":"London"}'}, "id": "call_abc123"}]}
{"role": "tool",      "content": "The price of a ticket to London is $799", "tool_call_id": "call_abc123"}
```

All four roles visible: system, user, assistant, tool. The `tool_call_id` in the last line matches the `id` in the line above it — that's how the LLM knows which tool request this result answers. Worth running yourself to see it live.

### Improvement 3: Database instead of dictionary

Replace the hardcoded `ticket_prices` dict with a SQLite database:

```python
def get_ticket_price(city):
    with sqlite3.connect("prices.db") as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
        result = cursor.fetchone()
        return f"Ticket price to {city} is ${result[0]}" if result else "No price data available"
```

Same tool, same JSON description, different implementation inside. **The LLM doesn't know or care** — it still just asks "get_ticket_price('London')". The secretary changed her phone book from a sticky note to a database. The boss's notes look the same.

---

## 6. Three Practical Points From the Demo

### Point 1: Gradio loses the tool call history (important for production)

When Gradio calls `chat(message, history)`, the `history` comes from the UI — what the customer sees on screen. The customer sees their messages and the assistant's answers. But the tool request and tool result happen behind the scenes and are NOT shown in the UI. So those messages **silently disappear** from future calls.

```
What the UI shows (and what history contains next time):
  user: "How much is a flight to London?"
  assistant: "A flight to London costs $799!"

What actually happened (but is NOT in history):
  user: "How much is a flight to London?"
  assistant: [tool_call: get_ticket_price("London")]    ← MISSING from history
  tool: "The price is $799"                              ← MISSING from history
  assistant: "A flight to London costs $799!"
```

The LLM usually figures it out from context — it sees its own answer mentions $799, so it works. But for a production system, save the **full** conversation history (including tool calls) in a database. Don't rely on Gradio's UI.

### Point 2: Streaming + tools is messy (why he skipped it)

When `stream=True`, the tool call comes back in **chunks** — fragments of JSON arriving piece by piece. You'd have to piece together the fragments before you can even tell which tool is being requested. Doable but ugly.

In practice, frameworks like **OpenAI Agents SDK** handle both streaming and tool routing for you. You rarely write this plumbing by hand. Today's code is the long way — good for understanding, not for production.

### Point 3: The `if/elif` chain is intentionally clunky

With one tool: `if name == "get_ticket_price"`. With two: add `elif name == "set_ticket_price"`. With ten tools, that's awful.

Python can dynamically look up a function by name and call it, eliminating the chain. That's the optional exercise below.

---

## 7. Exercises

### Exercise 1: Add a tool to SET the price

The notebook provides the `set_ticket_price(city, price)` function. You need to:
1. Write a new JSON description for it (same structure as `price_function`, different name/description/parameters)
2. Add it to the `tools` list: `tools = [{"type": "function", "function": price_function}, {"type": "function", "function": set_price_function}]`
3. Add another `if` branch in `handle_tool_calls`: `if tool_call.function.name == "set_ticket_price": ...`
4. Test: "Set the price to Tokyo to $1500" then "How much is a flight to Tokyo?" — it should show $1500

### Exercise 2 (optional, Pythonic): Eliminate the if/elif chain

Instead of:
```python
if tool_call.function.name == "get_ticket_price":
    result = get_ticket_price(city)
elif tool_call.function.name == "set_ticket_price":
    result = set_ticket_price(city, price)
```

Use Python's `globals()` or a dictionary to look up the function by name automatically:
```python
available_tools = {"get_ticket_price": get_ticket_price, "set_ticket_price": set_ticket_price}
func = available_tools.get(tool_call.function.name)
if func:
    result = func(**arguments)
```

Works for any number of tools without adding more `if` branches. Handle the case where the function doesn't exist (return an error message instead of crashing).

### Exercise 3: Add print statements and experiment

Put `for m in messages: print(m)` before the second LLM call. Watch the four roles appear. Change the system prompt to make the assistant snarky. Add more cities to the database. Try asking questions that don't need tools. Build confidence that there's no voodoo — just tokens and clever plumbing.

---

## 8. What's Next

Tomorrow (Week 2, Day 5): a **multimodal** AI assistant — the same pattern but handling images and audio too. Completes Week 2.

In practice, most tool-calling code uses a **framework** (OpenAI Agents SDK, LangChain, etc.) that handles the JSON descriptions, the tool routing, the streaming, and the conversation history. Today's manual approach is the foundation that makes the framework make sense.

---

## How to Explain This to Someone

### If a non-technical person asks "How does the code actually handle a tool request?"
"Four steps, like passing notes. Note 1: your code sends the question plus a menu of available tools. Note 2: the AI writes back 'run get_ticket_price for London.' Your code looks up the price. Note 3: your code sends everything back — question, the AI's request, and the answer. Note 4: the AI writes 'A flight to London costs $799.' Your code shows that to the customer."

### If a technical person asks
"`response = client.chat.completions.create(model, messages, tools=tools)`. Check `response.choices[0].finish_reason == 'tool_calls'`. If so, iterate `message.tool_calls`, dispatch by `function.name`, parse `function.arguments` (JSON string), execute, wrap result as `{'role': 'tool', 'content': result, 'tool_call_id': call.id}`. Append the assistant message and all tool results to messages, call again (with `tools=tools` if using a `while` loop for multi-step). Gradio's history drops tool messages, so persist the full transcript separately in production. Streaming + tools is awkward; frameworks like OpenAI Agents SDK handle it."

### The analogy
Four notes under the door. `if` → `while` turns one round of notes into a loop that continues until the boss stops asking for lookups.

### The one-liner
"Check finish_reason for 'tool_calls', run the function, append the result with role 'tool', call again — change if to while for the agentic loop."

---

## 9. Self-Check

1. What are the four notes? Map each to one line of code.
2. What does `finish_reason == "tool_calls"` mean? What's the alternative?
3. Walk through all 12 steps for "How much is a flight to London?" — who does each step?
4. What happens differently for "Hi, how are you?" (no tool needed)?
5. What does `handle_tool_call` do, line by line?
6. Why is `tool_call_id` included in the response?
7. What one-word change turns tool calling into the agentic loop?
8. Why doesn't the LLM care whether the function uses a dictionary or a database?
9. What's the Gradio history problem? Why does it usually work anyway? What's the production fix?
10. Why is streaming harder with tool calling?
11. What framework handles the tool plumbing for you in practice?

---

## 10. Quick Glossary

| Term | Plain meaning |
|---|---|
| `tools=tools` | Pass the JSON menu to the LLM so it knows what tools exist |
| `finish_reason` | How the LLM's reply ended: `"stop"` = normal answer, `"tool_calls"` = wants a tool |
| `tool_calls[0]` | The first tool request in the LLM's reply |
| `function.name` | Which tool the LLM asked for (e.g. `"get_ticket_price"`) |
| `function.arguments` | The arguments the LLM wants to pass, as JSON text |
| `json.loads(...)` | Parse JSON text into a Python dictionary |
| `handle_tool_call` | YOUR function that reads the request, runs the tool, wraps the result |
| `tool_call_id` | Unique ID linking a result back to the request (plumbing) |
| `messages.append` | Add one item to the history |
| `messages.extend` | Add multiple items to the history (for multiple tool results) |
| `if` → `while` | One-word change that turns single tool call into the agentic loop |
| SQLite | A lightweight database; replaces the hardcoded dictionary for real data |

# LLM Engineering – Week 3, Day 2 (Part 2)
## apply_chat_template: How Roles Become Tokens

> Personal study notes. This connects Week 1's "three roles" to the actual tokens the model sees.
> Notebook: week3/day2.ipynb (Colab)

---

## READ THIS FIRST (whole lecture in 4 lines)

1. The model only sees token numbers. It doesn't understand Python dicts like `{"role": "user", "content": "Hi"}`. Someone has to convert that list of dicts into a single string with special markers, then tokenize it.
2. When you use the OpenAI API, OpenAI does this behind the scenes. When you use Hugging Face locally, YOU do it with `apply_chat_template`.
3. `tokenize=False` → gives you the string so you can read it. `tokenize=True` (default) → does both steps internally and gives you the token numbers directly.
4. Different models use different marker formats, which is why the tokenizer must match the model.

---

## 1. The Problem This Solves

You have a Python list:
```python
messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "What is 2+2?"}
]
```

The model only sees a sequence of numbers. It doesn't understand Python dictionaries.

**Someone** must convert this list into a single text string with role markers, then turn that string into numbers.

| Where you're working | Who does this conversion |
|---|---|
| OpenAI API | OpenAI does it for you, behind the scenes. You never see it. |
| Hugging Face locally | YOU do it, with `apply_chat_template` |

---

## 2. What the Template Produces

### Step 1: Dicts → string with markers (`tokenize=False`)

```python
text = tokenizer.apply_chat_template(messages, tokenize=False)
```

Output (the actual text the model will see):

```
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>

You are helpful
<|eot_id|>
<|start_header_id|>user<|end_header_id|>

What is 2+2?
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

```

Every role is wrapped in special tokens. Content follows. `<|eot_id|>` marks end of each turn. At the bottom: `assistant` header with nothing after it — that's where the model starts generating its reply.

### In plain English (the screenplay)

```
[SCENE START]
[SPEAKER: system]
You are helpful
[END OF TURN]
[SPEAKER: user]
What is 2+2?
[END OF TURN]
[SPEAKER: assistant]
← model writes here
```

The model reads this screenplay top to bottom and writes the next line. Same autocomplete from Day 1, just with role markers so it knows who said what.

### Step 2: String → token numbers (`tokenize=True`)

```python
tokens = tokenizer.apply_chat_template(messages, tokenize=True)
# → [128000, 128006, 9125, 128007, 271, 2675, 527, 11190, ...]
```

These numbers go directly into the model.

---

## 3. Two Steps, You Choose Where to Stop

```python
# STOP AT STEP 1 (string only)
text = tokenizer.apply_chat_template(messages, tokenize=False)
# → "<|begin_of_text|><|start_header_id|>system..."
# You get a STRING. You can read it, print it, inspect it.

# DO BOTH STEPS (string → numbers, internally)
tokens = tokenizer.apply_chat_template(messages, tokenize=True)
# → [128000, 128006, 9125, ...]
# You get NUMBERS. Ready to feed to the model.
```

With `tokenize=True`, the function does both steps inside — converts dicts to string with markers, then converts string to numbers — and hands you just the final numbers. You never see the string in between. It happens, but internally.

**The full picture:**

```
Your Python list of dicts
      ↓
STEP 1: apply_chat_template converts to string with role markers
      ↓
"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nYou are helpful\n<|eot_id|>..."
      ↓
STEP 2: tokenize that string into numbers
      ↓
[128000, 128006, 9125, 128007, 271, 2675, 527, 11190, ...]
      ↓
These numbers go into the model
```

- `tokenize=False` → output of step 1 only
- `tokenize=True` → output of step 2 (step 1 still happens inside, you just don't see it)

**Cooking analogy:**
- `tokenize=False` → "Prepare the ingredients, lay them on the counter. Don't cook yet." (You can inspect.)
- `tokenize=True` → "Prepare AND cook." (You get the finished dish — numbers the model eats.)

**When to use which:**
- `tokenize=False` → only to inspect, debug, understand what the model will see
- `tokenize=True` → real usage, because the model needs numbers, not text

---

## 4. Why Different Models Need Different Templates

Llama uses `<|start_header_id|>system<|end_header_id|>`. ChatGPT uses a different format. Gemma uses something else entirely. The template is **built into the tokenizer**.

That's another reason the tokenizer must match the model:
- Wrong tokenizer → wrong markers → model doesn't know where roles start and end → garbage output

When you write `AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")`, you get Llama's markers. A different model name gives different markers. `Auto` handles this automatically.

---

## 5. How to Explain This to Someone

### If a non-technical person asks "What is a chat template?"

"When you text someone, you see names above each message — 'Mom', 'You', 'Mom'. An AI model needs the same thing, but it can't see names. So before your conversation reaches the model, each message gets wrapped with invisible markers: 'this is from the system', 'this is from the user', 'this is from the assistant.' The chat template is the tool that adds those markers."

### If a technical person asks

"`apply_chat_template` takes a list of role/content dicts and serializes them into a single token sequence using model-specific special tokens (e.g. Llama's `<|start_header_id|>`, `<|eot_id|>`). With `tokenize=True`, it also runs the tokenizer and returns input IDs directly. It's the local equivalent of what the OpenAI API does behind the scenes when you pass the `messages` parameter — they convert your structured input to the flat token sequence the transformer actually reads."

### The analogy
A screenplay with labelled lines: [SPEAKER: system] ... [SPEAKER: user] ... [SPEAKER: assistant] ← model writes here. The template adds the labels; the model reads the script and writes the next line.

### The one-liner

"A chat template converts your list of messages into the exact format a specific model expects, with role markers and special tokens."

---

## 6. Self-Check

1. Why can't the model read your Python list of dicts directly?
2. Who does this conversion when you use the OpenAI API? When you use Hugging Face locally?
3. What does `apply_chat_template(messages, tokenize=False)` give you?
4. What does `apply_chat_template(messages, tokenize=True)` give you?
5. What does `<|start_header_id|>system<|end_header_id|>` mean?
6. What does `<|eot_id|>` mean?
7. Why is the `assistant` header at the bottom empty?
8. Why must the tokenizer match the model? What happens if they don't match?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| `apply_chat_template` | Converts a list of role/content dicts into the token format a specific model expects |
| `tokenize=False` | Returns the formatted string (for reading/debugging) |
| `tokenize=True` | Returns the token numbers (for feeding to the model) |
| `<\|start_header_id\|>` | Llama's marker that means "a role name is about to follow" |
| `<\|end_header_id\|>` | Llama's marker that means "the role name just ended, content follows" |
| `<\|eot_id\|>` | Llama's "end of turn" marker — separates one speaker from the next |
| Chat template | The model-specific rules for how roles and content are formatted into tokens |
| Serialization | Converting a structured object (Python dict) into a flat format (string or token sequence) |

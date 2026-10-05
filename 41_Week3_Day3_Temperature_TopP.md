# LLM Engineering – Week 3, Day 3 (Part 3)
## Temperature, top_p, and the Generate Function

> Personal study notes. Two new concepts: temperature and top_p.
> The ice cream shop analogy is the version that made it click.
> **Accuracy note:** temperature and top_p were **not** covered in the Week 3 Day 3 lecture. This file is extra explanation (correct, and it clicked). The lecturer's own explanation of temperature is in Week 3 Day 5 (file 45). The `generate` function below is an illustrative wrapper, not code from the notebook. The actual end of the Day 3 lecture (comparing tokenizers across models) is in file 40, section 4b.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. **Temperature** = how adventurous the model is when picking the next word. 0 = always picks the favourite. 0.5 = usually the favourite. 1.5 = might pick anything. Higher = more creative but riskier.
2. **top_p** = which words are even on the menu. 0.9 = only words covering 90% of the probability. Weird unlikely words are removed before the model picks. Lower = fewer choices.
3. They work together: top_p narrows the menu first, then temperature decides how adventurous the model is among what's left. Defaults: `temperature=0.5, top_p=0.9`.

---

## 1. The Ice Cream Shop Analogy (the version that clicked)

### Setup

20 flavours at an ice cream shop. You have favourites:

```
Chocolate      → your top pick (most likely)
Vanilla        → second favourite
Strawberry     → you like it
Mango          → it's okay
... 16 others  → you'd rarely pick them
Pickle flavour → you'd almost never pick it
```

### Temperature = how adventurous you are today

| Temperature | What happens | Ice cream version |
|---|---|---|
| 0 (robot mode) | ALWAYS pick the top choice. Every time. No surprises. | Monday: chocolate. Tuesday: chocolate. Forever: chocolate. |
| 0.5 (normal) | Usually the favourite. Sometimes second or third. | Usually chocolate or vanilla. Sometimes strawberry. |
| 1.5 (wild mood) | Might pick anything, including weird options. | Maybe mango. Maybe pickle. Feeling experimental. |

Same person, same preferences. Temperature just controls how willing you are to try something other than your favourite.

### top_p = which flavours are even on the menu

Before you pick, someone removes options from the menu.

| top_p | What's left on the menu |
|---|---|
| 1.0 | All 20 flavours available |
| 0.9 | Only the flavours covering 90% of your preference (chocolate, vanilla, strawberry, mango, a few others). Pickle and wasabi REMOVED. |
| 0.3 | Only chocolate and vanilla left. Everything else removed. |

You CAN'T pick a removed flavour even if you wanted to.

### They work together

1. **First,** top_p removes flavours from the menu (narrows the choices)
2. **Then,** temperature decides how adventurous you are among what's left

Example 1: `top_p=0.9, temperature=0.5`
- Remove pickle and wasabi from menu
- Usually pick chocolate or vanilla from what remains

Example 2: `top_p=0.9, temperature=1.5`
- Remove pickle and wasabi from menu
- Might pick mango or strawberry even though chocolate is the favourite

---

## 2. Now Replace Ice Cream with Words

The model just wrote "The weather today is" and needs the next word:

```
"sunny"    → favourite word (most likely)
"warm"     → second favourite
"cold"     → third
"nice"     → fourth
...
"purple"   → would almost never follow this sentence
```

| Setting | Ice cream version | Word version |
|---|---|---|
| temperature 0 | Always chocolate | Always "sunny" |
| temperature 0.5 | Usually chocolate or vanilla | Usually "sunny" or "warm" |
| temperature 1.5 | Might pick mango or pickle | Might pick "cold" or "purple" |
| top_p 1.0 | All 20 flavours | All words available |
| top_p 0.9 | Remove pickle and wasabi | Remove "purple" and unlikely words |
| top_p 0.3 | Only chocolate and vanilla | Only "sunny" and "warm" left |

---

## 3. When to Use What (practical guide)

| Task | Temperature | top_p | Why |
|---|---|---|---|
| Code generation, data extraction | 0 or 0.1 | 0.9 | You want the most likely (correct) answer every time |
| Factual Q&A | 0.3–0.5 | 0.9 | Mostly accurate, slight variety in phrasing |
| General conversation | 0.7 | 0.9 | Natural, some variety |
| Creative writing, brainstorming | 1.0–1.2 | 0.95 | More surprising, more varied |
| Experimental, wild ideas | 1.5+ | 1.0 | Unpredictable, may produce nonsense |

**Safe defaults:** `temperature=0.5, top_p=0.9`. Good starting point for most tasks.

---

## 4. The Generate Function (wrapping the pipeline)

```python
def generate(prompt):
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
    outputs = model.generate(inputs, max_new_tokens=200, temperature=0.5, top_p=0.9)
    result = tokenizer.decode(outputs[0][len(inputs[0]):])
    return result
```

Every line is from earlier lectures, wrapped into one function:

| Line | What it does | Where you learned it |
|---|---|---|
| `messages = [...]` | Build the dict list | Week 1, Day 4 (illusion of memory) |
| `apply_chat_template(..., return_tensors="pt")` | Dicts → tokens as PyTorch tensor | File 35, 36 |
| `.to("cuda")` | Move to GPU | File 36 |
| `model.generate(inputs, max_new_tokens=200)` | Run the model, predict up to 200 tokens | File 36 |
| `temperature=0.5, top_p=0.9` | Control creativity and word selection | This lecture (NEW) |
| `outputs[0][len(inputs[0]):]` | Slice off the input, keep only generated tokens | File 38 |
| `tokenizer.decode(...)` | Numbers → readable text | File 34 |

---

## 5. Technical Detail: How Temperature Changes Probabilities

*(Skip this if the ice cream version is enough. Come back if you want the math.)*

Before picking a token, the model produces a raw score (called a **logit**) for every token. These get converted to probabilities using a formula called **softmax**.

Temperature divides the logits before softmax:

```
adjusted_logit = original_logit / temperature
```

- **Low temperature (0.1):** dividing by a small number makes big logits MUCH bigger and small ones tiny. The top token dominates. Almost deterministic.
- **Temperature 1.0:** no change (dividing by 1).
- **High temperature (1.5):** dividing by a large number compresses all logits closer together. Probabilities flatten out. More tokens have a real chance.
- **Temperature 0:** special case. Skip the probabilities entirely, just pick the token with the highest logit. Called **greedy decoding**.

---

## 6. How to Explain This to Someone

### If a non-technical person asks "Why does AI sometimes give different answers to the same question?"

"The AI doesn't always pick the most likely word. It has a 'creativity dial' called temperature. Turn it down and it always picks the safest, most expected answer. Turn it up and it takes risks, sometimes surprising you, sometimes saying something weird. When you ask the same question twice and get different answers, that's because the dial is set somewhere in the middle."

### If a technical person asks

"Temperature scales logits before softmax: `logit / T`. Low T sharpens the distribution (near-greedy); high T flattens it (more uniform sampling). top_p (nucleus sampling) truncates the distribution to the smallest set of tokens whose cumulative probability exceeds p, eliminating low-probability tail tokens before sampling. They compose: top_p filters first, temperature adjusts the remaining distribution. T=0 is greedy decoding (argmax). Defaults of T=0.5, top_p=0.9 balance coherence with variety for most tasks."

### The analogy

Ice cream shop with 20 flavours. Temperature = how adventurous you are (always chocolate vs. maybe pickle). top_p = which flavours are even on the menu (remove the weird ones before you pick).

### The one-liner

"Temperature controls how creative the model is; top_p controls which words are even considered. Both shape how the next token is picked."

---

## 7. Self-Check

1. What does temperature 0 do? (One sentence.)
2. What does temperature 1.5 do compared to 0.5?
3. What does top_p=0.9 mean? What gets removed?
4. Which is applied first, temperature or top_p?
5. What settings would you use for code generation? For creative writing?
6. In the generate function, what does each line do?
7. Explain temperature using the ice cream analogy.

---

## 8. Quick Glossary

| Term | Plain meaning |
|---|---|
| Temperature | Controls how "adventurous" the model is when picking the next token. 0 = always top pick. Higher = more variety. |
| top_p (nucleus sampling) | Only consider tokens covering the top p% of probability. Removes unlikely tokens from the menu. |
| Greedy decoding | Temperature = 0. Always pick the most likely token. Deterministic. |
| Logit | The raw score the model produces for each token before converting to probability |
| Softmax | The formula that converts logits into probabilities (0 to 1, summing to 1) |
| `max_new_tokens` | Cap on how many tokens the model can generate |
| Deterministic | Same input always produces the same output (temperature = 0) |
| Sampling | Randomly picking from the probability distribution (temperature > 0) |

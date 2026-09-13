# LLM Engineering – Week 2
## LLMs Talking to Each Other, and When Roles Break Down

> Personal study notes. Section 2 is the important part, a technique used constantly.

---

## READ THIS FIRST (the one technique to remember)

The `user`/`assistant` role structure only works for two participants. With three or more (or any complex situation), **stop using roles to represent the conversation. Write it out as labelled text inside one user prompt instead:**

```
system: "You are Alex. You are talking with Blake and Charlie."
user: "The conversation so far:
  Alex: Pineapple on pizza is disgusting.
  Blake: I actually quite like it.
  Charlie: You're both wrong, olives.
  Now write what Alex says next."
```

Names survive because they're just words in a sentence. Scales to any number of participants, any order, any speaker repeating. The rule: **user/assistant for simple back-and-forth chat. One structured user prompt for anything more complicated.** This applies far beyond silly demos, to any situation more complex than a basic chatbot.

---

## 1. Two LLMs Arguing

**Setup:** GPT-4.1-mini gets a snarky, argumentative system prompt. Claude 3.5 Haiku gets a polite, agreeable one. A loop runs them against each other for five rounds. Very funny; pineapple-on-pizza comes up a lot.

### How it works mechanically
The only bit that matters: **each model sees itself as the assistant and the other model as the user.**

From GPT's point of view:
```python
[
  {"role": "system",    "content": "You are snarky and argumentative"},
  {"role": "assistant", "content": "Hi there"},                 # GPT's own lines
  {"role": "user",      "content": "Hi"},                       # Claude's lines
  {"role": "assistant", "content": "Oh, just 'hi'? Pathetic."},
  {"role": "user",      "content": "You're absolutely right, I..."}
]
```

From Claude's point of view: the same conversation with roles **swapped** — Claude's lines become `assistant`, GPT's become `user`.

One conversation, two versions of the list, roles flipped. A loop calls each in turn and appends every reply to both lists.

**Do this:** add `print` statements to see the message lists being built. The mechanics matter more than the comedy. This is also the illusion of memory again — the whole conversation is resent each time.

**Play with it:** swap the personas, optimist vs pessimist, opposite sides of a debate.

---

## 2. When user/assistant Breaks Down (the important part)

**The challenge:** make it a three-way conversation — Alex, Blake, Charlie.

### The problem: there are only two roles
`role` accepts `system`, `user`, `assistant`. Nothing else. Fine for two participants:

```python
{"role": "user",      "content": "Hi"}          # the human
{"role": "assistant", "content": "Hello!"}      # the model
```

But with three, asking Alex what to say next:

```python
messages = [
  {"role": "assistant", "content": "Pineapple on pizza is disgusting."},   # Alex
  {"role": "user",      "content": "I actually quite like it."},           # Blake
  {"role": "user",      "content": "You're both wrong, olives."}           # Charlie
]
```

The last two are both `"user"`. **The model can't tell Blake from Charlie — the names are simply gone.** There's nowhere to put them.

### The fix: write the conversation as labelled text in one user prompt

```python
messages = [
  {"role": "system", "content": "You are Alex. You are argumentative. You are talking with Blake and Charlie."},
  {"role": "user",   "content": """The conversation so far:

Alex: Pineapple on pizza is disgusting.
Blake: I actually quite like it.
Charlie: You're both wrong, the real crime is olives.

Now write what Alex says next."""}
]
```

No `assistant` entries. No history list. One system prompt setting the scene, one user prompt containing the whole conversation as text, ending with "now say your next line."

**The names survive because they're just words in a sentence.** The model reads it like a film script.

### Why it handles anything
Same speaker twice in a row is no problem, because every line is labelled:
```
Alex: Pineapple on pizza is disgusting.
Blake: I actually quite like it.
Blake: In fact I had it last night.
Charlie: You're both wrong, olives.
```
The model reads "Blake:" twice and understands. Scales to five people, ten people, someone joining halfway. It's all just text, and text can express anything.

### The rule
**user/assistant for a simple back-and-forth chat. One structured user prompt for anything more complicated.**

### Where this really matters (beyond silly demos)
Example aimed at the tutor project: you want the tutor to answer a question, but also to see your last two conversations as background. Cramming those into a role list is awkward — it can't tell "an earlier session" from "the current chat." Much better:

```
Here are my two previous sessions with you:
[session 1 text]
[session 2 text]

Now, my new question is: ...
```

**For JobRadar:** passing postings + your profile + past notes into one call is a structured prompt, not a chat history.

### Bonus
You can do the three-way with a **single model** — three different system prompts, three personas. No need to pay for three providers.

---

## How to Explain This to Someone

### If a non-technical person asks "Can two AIs talk to each other?"
"Yes — you give each one a personality (one argumentative, one polite) and pass their messages back and forth. Each AI sees itself as 'me' and the other as 'you.' For three or more participants, you write the conversation out like a script with names on each line, and ask each AI to write its next line."

### If a technical person asks
"Two-agent conversation: maintain one shared transcript, but each model receives it with roles flipped — its own turns as `assistant`, the other's as `user`. For N>2 participants, the user/assistant schema breaks (only two roles). Solution: serialize the full conversation as labelled text inside a single user message ('Alex: ... Blake: ... Charlie: ...') and prompt for the next line by name. This structured-prompt pattern generalizes to any situation more complex than a simple two-party chat."

### The analogy
A film script with labelled lines. Names survive because they're just words in the text — any number of speakers, any order.

### The one-liner
"For two participants, swap roles; for three or more, write the conversation as a labelled script in one prompt."

---

## 3. Self-Check

1. In the two-LLM setup, what role does GPT see its own lines as? What about Claude's lines?
2. Why does a three-way conversation break the role structure?
3. Write out the fix for a conversation between Alex, Blake, and Charlie.
4. Can the model tell if Blake speaks twice in a row? Why?
5. State the rule for when to use roles vs a structured prompt.
6. Give a real (non-comedy) example where the structured prompt is better.

---

## 4. Quick Glossary

| Term | Plain meaning |
|---|---|
| Role swap | Each model sees its own lines as `assistant` and the other's as `user` |
| Structured prompt | Writing the whole situation as labelled text inside one user prompt |
| Persona | A character given to a model through its system prompt |

---

## 5. Progress Note
15% through the course. Can now: give an overview of transformers, compare frontier models, use the OpenAI API and several others, use abstraction layers, routers, prompt caching, and multi-party conversations.

**Next: Gradio** — building UIs.

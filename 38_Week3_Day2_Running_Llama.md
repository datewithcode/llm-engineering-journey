# LLM Engineering – Week 3 (Supplementary)
## Output Slicing and Base vs Instruct Models

> **Accuracy note:** an earlier version of this file described live demos (a base model rambling, specific Phi-4 sizes) that did **not** happen in the lecture. It was written from a duplicate transcript. Those invented details have been removed.
> What remains is **extra explanation**: correct concepts that support the real lectures. The lecturer's actual model runs are in file 44.

---

## READ THIS FIRST (in 3 lines)

1. `model.generate()` returns your input tokens **plus** the new tokens. To see only the new part, slice off the input: `outputs[0][len(inputs[0]):]`.
2. **Base** models only continue text. **Instruct** models (name ends in `-Instruct`) are fine-tuned on conversations, so they follow roles and answer questions.
3. Always check the model name: one suffix changes the behaviour completely (the "wrong key" story from Week 1).

---

## 1. Output Slicing (extra explanation)

```python
outputs = model.generate(inputs, max_new_tokens=80)

# outputs[0] = [your input tokens] + [newly generated tokens]
new_tokens = outputs[0][len(inputs[0]):]      # drop the input part
print(tokenizer.decode(new_tokens))
```

**WHY:** a causal model continues a sequence, so its output contains the whole sequence. If you decode everything, you'll see your own prompt (with special tokens) before the answer. In the lecture, the lecturer simply decodes the whole output, which is why you see the chat template's special tokens printed before the joke (file 44).

**Letter analogy:** you wrote the first paragraph; the model continued. The output is the whole letter. The slice keeps only the model's part.

---

## 2. Base vs Instruct (concept from Week 1 Day 3 and Week 3 Day 3)

| | Base model | Instruct model |
|---|---|---|
| Example name | `meta-llama/Llama-3.2-1B` | `meta-llama/Llama-3.2-1B-Instruct` |
| Trained on | Internet text, next-token prediction only | Same, plus fine-tuning on system/user/assistant conversations |
| Behaviour | Continues whatever text you give it | Recognises roles, answers questions |
| Chat template | Not designed for one | Has one, with role special tokens |
| Use when | You'll fine-tune it yourself, or want raw continuation | You want a chat assistant |

Name suffixes you'll see for instruct variants: `-Instruct`, `-it`, `-chat`.

**WHY this matters:** it's the Week 1 student bug (the "wrong key"): using the base model name when you meant the instruct one gives confusing output that looks like a bug but isn't.

---

## 3. How to Explain This to Someone

### If a non-technical person asks "Why do some models ramble instead of answering?"

"Every model starts as a 'base' version that just continues text, like autocomplete. The 'instruct' version has extra training on conversations, so it answers questions. If you accidentally use the base version, it keeps writing instead of replying."

### If a technical person asks

"Base checkpoints are pre-trained for next-token prediction only; instruct checkpoints add supervised fine-tuning (and usually RLHF) on chat-formatted data with role special tokens. `model.generate` returns the full sequence including the prompt, so slice `outputs[0][len(inputs[0]):]` to decode only generated tokens."

### The analogy

Base model: a well-read person who has never had a conversation, so they just keep talking. Instruct model: the same person after years of practising conversations.

### The one-liner

"Use the -Instruct model to get answers, and slice off the prompt to see only what it generated."

---

## 4. Self-Check

1. Why does `model.generate()` output contain your prompt? How do you remove it?
2. What's the difference between a base and an instruct model?
3. What suffixes indicate an instruct model?
4. How does this connect to the Week 1 "wrong key" story?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| Output slicing | `outputs[0][len(inputs[0]):]`: keep only the generated tokens |
| Base model | Pre-trained only; continues text |
| Instruct model | Fine-tuned on conversations; follows roles and answers |
| `-Instruct` / `-it` / `-chat` | Name suffixes for instruct variants |

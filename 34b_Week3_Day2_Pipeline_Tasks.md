# LLM Engineering – Week 3, Day 2 (Main Lecture)
## Pipelines in Action: Eight Tasks, Colab Tips, and the Two Levels of Hugging Face

> Personal study notes. This is the actual Week 3 Day 2 lecture content (added during a later accuracy check).
> Read this BEFORE file 34. File 34's tokenizer section is a preview of Week 3 Day 3.
> Notebook: week3/day2 Colab.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. Hugging Face's code has **two levels**: **pipelines** (high-level, quick, pre-configured for common tasks) and **tokenizers + models** (low-level, full control). This lecture is pipelines only.
2. The pattern: **create a pipeline once** by naming the task, then **call it as often as you like** with different inputs.
3. He runs eight tasks: sentiment, named entity recognition, question answering, summarization, translation, zero-shot classification, text generation, plus image and speech generation.
4. **WHY use small specialized models** when frontier models can do all this: they're free or very cheap, fast, and you own the code and weights.

---

## 1. The Two Levels of Hugging Face Code

| Level | What it is | When to use |
|---|---|---|
| **Pipelines** | High-level API. Common tasks in a few lines. | You have a trained model and want to run a standard inference task quickly |
| **Tokenizers and models** | Low-level API. Work with the neural network directly. | Most power and control: fine-tuning, custom behaviour (Week 3 Days 3-4, Week 7) |

Pipelines are built on top of the low-level code. They just pre-package it for common cases.

---

## 2. The Pipeline Pattern

```python
from transformers import pipeline

my_pipeline = pipeline("the_task_name")     # 1. build it once (downloads a model)
result = my_pipeline(my_input)              # 2. call it with any input, as often as you like
```

**WHY two steps:** building the pipeline is the slow part (downloading the model). After that, each call is fast. First run takes longer because it downloads; later runs reuse the downloaded model.

Tasks listed in the lecture: sentiment analysis, classification, named entity recognition, question answering, summarization, translation.

---

## 3. Two Colab Pro Tips

### Tip 1: Data science code is chatty. Ignore warnings unless something breaks.

You'll see lots of warnings, including **deprecation warnings** (something will be removed in a future version but still works now). Glance at them. If something fails later, remember them as possible clues. Otherwise, push on. A warning is not an error.

### Tip 2: "CUDA is required but not available" is misleading

**What it really means:** Google bumped you off the GPU box onto a CPU box mid-session, often without an obvious notice.

**What NOT to do:** start installing packages to "fix" it. That leads to pages of pointless installs.

**What to do:**
1. Runtime → Disconnect and delete runtime
2. Edit → Clear all outputs (so you're not confused by old results)
3. Reconnect to a T4
4. Run from the very top of the notebook, pip installs first

---

## 4. The Eight Tasks

### Task 1: Sentiment analysis
Is a sentence positive or negative? Classic example: a movie review.
```python
classifier = pipeline("sentiment-analysis", device="cuda")
classifier("I'm super excited to be on the way to LLM mastery!")
```
Returns a label (POSITIVE/NEGATIVE) and a confidence score.

### Task 2: Named Entity Recognition (NER)
Tags words in a sentence by what kind of thing they are.
```python
ner = pipeline("ner", device="cuda")
result = ner("AI engineers are learning about the amazing pipelines from Hugging Face in Google Colab from Ed Donner")
for entity in result:
    print(entity)
```
| Tag | Meaning | Examples from the demo |
|---|---|---|
| ORG | Organization | Hugging Face |
| MISC | Miscellaneous | Google Colab |
| PER | Person | Ed Donner |

Each entity comes with an **index** (its position). Note that "Hugging Face" gets split into several **tokens**, each tagged separately, because NER works token by token.

**WHY it matters:** many business tasks need to pull out *what's being referred to* in text: which product, which person, which company.

### Task 3: Question answering with context
Give a question plus some context; it answers from the context.
```python
question_answerer = pipeline("question-answering", device="cuda")
result = question_answerer(
    question="What are Hugging Face pipelines?",
    context="Pipelines are a high level API for inference of LLMs with common tasks"
)
```
**The lecturer's idea (a baby step toward RAG):** you need good context for every question. So: run NER on the question → look up the entities in your database → use what you find as the context → ask the question. A customer asks about a product; NER pulls out the product name; you fetch its details; the QA pipeline answers. **RAG (Week 5) is the better, more general way** to do this.

### Task 4: Summarization
```python
summarizer = pipeline("summarization", device="cuda")
summary = summarizer(long_text, max_length=50, min_length=25, do_sample=False)
```
Shortens a longer text. In the demo it was more concise, though not dramatically.

### Task 5: Translation
```python
translator = pipeline("translation_en_to_fr", device="cuda")
translator("The data scientists were truly amazed by the power and simplicity of the HuggingFace pipeline API.")
```
Other language pairs: filter the Hugging Face Models page by the **translation** task and by language, then pick a model. There's a movement to build translators for **rarer languages**, including fading ones people want to preserve.

### WHY small specialized models instead of ChatGPT?

You could summarize or translate with a frontier model. But:

| Frontier model | Small specialized model |
|---|---|
| You pay per call | Free on your own GPU, very cheap at scale |
| Trillions of calculations per answer | Far fewer calculations, fast |
| Black box | You own the code and the weights |
| General-purpose | Fine-tuned for exactly one task |

**Focus on a task + small specialized model = more done, cheaper, faster.**

### Task 6: Zero-shot classification
"Zero-shot" = no examples given. You provide a sentence and some buckets (labels); it picks a bucket.
```python
classifier = pipeline("zero-shot-classification", device="cuda")
result = classifier(
    "Hugging Face's Transformers library is amazing!",
    candidate_labels=["technology", "sports", "politics"]
)
```
Demo result: technology 95%, sports 3%, politics 1.8%. Experiment with different labels and models.

### Task 7: Text generation (default model: GPT-2)
```python
generator = pipeline("text-generation", device="cuda")
result = generator("If there's one thing I want you to remember about using HuggingFace pipelines, it's")
```
Uses **GPT-2** by default: an old model from a bygone era. The output starts plausibly, then drifts into **believable nonsense**.

**WHY this is instructive:** it shows what LLMs fundamentally do: generate **plausible** text, not **true** text. That big modern models are so often *truthful* is remarkable and somewhat surprising. Small or early models reveal the underlying mechanism.

The lecturer's comparison: like pressing your phone's predictive-text button over and over, only worse.

### Task 8a: Image generation (diffusers pipeline)
Same pipeline idea, but for **diffusion models** (image generation) instead of transformers. He reruns SDXL Turbo from Stability AI (the company is Stability AI; the model is Stable Diffusion).
- You may see: "`torch_dtype` is deprecated, use `dtype` instead." Harmless; you can change it.
- It nearly maxes out the T4's GPU memory. If you run out: **Runtime → Restart session**. After a restart you do **not** need to redo pip installs (only after disconnect and delete).

### Task 8b: Text-to-speech
```python
synthesizer = pipeline("text-to-speech", "microsoft/speecht5_tts", device="cuda")
speech = synthesizer("Hi to an artificial intelligence engineer, on the way to mastery!",
                     forward_params={"speaker_embeddings": speaker_embedding})
```
Same pipeline pattern, plus a **speaker embedding** that describes the kind of voice. If you get an error about `datasets`, you skipped the pip install at the top: reconnect and start from the top.

---

## 5. Where to Find More Pipelines

The notebook links to two documentation pages:
- **Transformers pipelines:** all text/audio/vision tasks
- **Diffusers pipelines:** all image-related tasks

The lecturer's mission for you: explore and experiment. It's all open source and free.

---

## 6. Fun Extra: Corgi Mode

Colab: Settings → Miscellaneous → tick **Corgi mode** (a corgi runs across the top). There are also kitties and crabs, and a "power level" setting that adds sparks and a combo score while you type. Pure fun, no technical value.

---

## 7. Progress: 30% Through

You can now: code with frontier models, build multimodal AI assistants, and use Hugging Face pipelines for many common inference tasks.

**Next (Week 3 Day 3):** going under the hood with tokenizers, special tokens, and chat templates.

---

## 8. How to Explain This to Someone

### If a non-technical person asks "What are Hugging Face pipelines?"

"Ready-made AI tools you can use in one or two lines of code. Want to know if a review is positive? Pull out names of people and companies from a sentence? Translate English to French? Summarize a document? Each is one line. They run free models on your own machine, so they're cheap and private."

### If a technical person asks

"Pipelines are Hugging Face's high-level inference API: `pipeline(task)` resolves a default (or specified) model, handles tokenization, inference, and post-processing. Tasks include sentiment analysis, NER, extractive QA, summarization, translation, zero-shot classification, and text generation, plus diffusers pipelines for image generation and TTS via SpeechT5 with speaker embeddings. Small task-specific models give cheap, fast, fully-owned inference compared with frontier APIs."

### The analogy

A toolbox of single-purpose power tools. Each does one job well and cheaply. A frontier model is a skilled general contractor: can do everything, but you pay for every hour.

### The one-liner

"Pipelines turn common AI tasks into one line of code using small, free, specialized models."

---

## 9. Self-Check

1. What are the two levels of Hugging Face code? Which one is this lecture?
2. What's the two-step pipeline pattern, and why is it split that way?
3. What does "CUDA is required but not available" really mean? What are the four steps to fix it?
4. What do the NER tags ORG, MISC, and PER mean? Why does "Hugging Face" appear as several entries?
5. How could NER plus a database lookup feed the question-answering pipeline? What's the better general approach?
6. Why use a small specialized model for translation instead of a frontier model?
7. What does "zero-shot" mean?
8. Why does GPT-2 produce believable nonsense? What does that reveal about LLMs?
9. After Runtime → Restart session, do you need to redo pip installs?

---

## 10. Quick Glossary

| Term | Plain meaning |
|---|---|
| Pipeline | Hugging Face's high-level, pre-configured way to run a common AI task |
| Deprecation warning | "This will be removed in a future version, but still works now" |
| Sentiment analysis | Is this text positive or negative? |
| NER (named entity recognition) | Tagging words as people (PER), organizations (ORG), places, or miscellaneous (MISC) |
| Question answering | Answering a question from a supplied piece of context |
| Summarization | Shortening a text while keeping the main points |
| Zero-shot classification | Sorting text into labels without giving any examples |
| GPT-2 | An old OpenAI model; the default for the text-generation pipeline |
| Diffusers | Hugging Face's library for diffusion (image generation) pipelines |
| Speaker embedding | A set of numbers describing the voice for text-to-speech |
| Corgi mode | A Colab setting that makes corgis run across the screen |

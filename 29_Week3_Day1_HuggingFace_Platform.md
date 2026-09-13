# LLM Engineering – Week 3, Day 1 (Part 1)
## Hugging Face: The Platform (Models, Datasets, Spaces)

> Personal study notes. This covers ONLY the website, not the code library.
> The code library is a separate thing, covered in the next lecture.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Hugging Face is **two different things**: a website (the platform) and Python code libraries. This lecture is the website only. Don't mix them up.
2. The website has three sections: **Models** (~2 million open-source models to download), **Datasets** (~500,000 shared training datasets), and **Spaces** (hosted apps like Gradio, Streamlit, or Docker).
3. Sign up for a **free** account. No pro plan needed. Everything in this course uses the free tier.

---

## 1. Hugging Face — Two Different Things

| | What it is | Analogy |
|---|---|---|
| **Side 1: The platform** (this lecture) | A website for browsing and sharing models, data, and apps | GitHub, but for AI |
| **Side 2: The code library** (next lecture) | Python packages you install to run models in your code | Like the OpenAI Python library, but for open-source models |

They are separate. You can use the website without the library, and the library without the website. But they connect: the library downloads models FROM the website.

---

## 2. The Platform's Three Sections

### Models (~2,134,000 and growing)

Open-source models anyone can download and use. It's basically GitHub for AI models.

**How to navigate 2 million models:**
- Filter by **task**: text generation (most common for us), image generation, text-to-video, etc.
- Filter by **size**: parameter count ("only under 12B") — useful if your computer has limited RAM
- Filter by **framework**: PyTorch is most common
- Filter by **language**: if you need non-English models
- Filter by **license**: different open-source licenses have different rules
- **Sort by**: most likes, most downloads (good quality indicators), or recently updated
- **Name format**: `provider/model-name` (e.g. `meta-llama/Llama-3.2-3B`) — same pattern as OpenRouter

### Datasets (~500,000 and growing)

Training data people have shared. Each dataset has:
- A **data card** describing what it is, where it came from, how to use it
- **Examples** of the actual data you can browse
- **Size** and format information

Before Hugging Face, **Kaggle** was the main place for datasets. Kaggle is still big for competitions and general data science, but for transformers and generative AI, people converge on Hugging Face.

### Spaces (hosted apps)

Running AI apps that anyone can interact with via a URL.

**What you can deploy:**
- **Gradio apps** (what we've been building)
- **Streamlit apps** (the Outsmart game is a Streamlit Space)
- **Anything in a Docker container**

**Why this matters:** remember `share=True` from week 2? That used HTTP tunneling, which was janky and corporate networks blocked it. Spaces is the **proper way** to share a Gradio app. Deploy with `gradio deploy` from your terminal.

You can also **embed** a Space inside your own website, which is what the lecturer did with Outsmart.

---

## 3. The 8-Week Course Map (where you are)

| Week | Topic | Status |
|---|---|---|
| 1 | Foundations (transformers, tokens, APIs) | Done |
| 2 | Frontier models, Gradio, tools, multimodal | Done |
| **3** | **Open source models with Hugging Face** | ← You are here |
| 4 | Picking the right LLM | Next |
| 5 | RAG | Coming |
| 6 | Fine-tuning a frontier model + data science | Coming |
| 7 | Fine-tuning an open-source model | Coming |
| 8 | Grand finale — agents | Coming |

The lecturer warns: week 3 is harder than week 2 ("a bit like a trip to the dentist"). You go under the hood of models. Don't skip to RAG — this week's knowledge makes RAG make sense.

---

## 4. Action Item

Sign up at huggingface.co. Free plan only. You'll need the account for the rest of the course.

---

## 5. How to Explain This to Someone

### If a non-technical person asks "What is Hugging Face?"

"Hugging Face is like an App Store, but for AI. You go to their website, browse thousands of AI models, and use them. Some are free apps you can try right there. Some are datasets — big collections of information that people share. Think of it as a community where AI builders share their work with everyone."

### If a technical person asks

"Hugging Face is two things. First, it's a platform — like GitHub but for AI models, datasets, and hosted apps. Two million open-source models you can download, half a million datasets, and Spaces where you can deploy Gradio or Streamlit apps. Second, it's a set of Python libraries (`transformers`, `datasets`, `tokenizers`) that let you download and run those models in your own code with a few lines of Python. The platform is where the models live; the library is how you use them."

### If they ask "why does it matter?"

"Before Hugging Face, if you wanted to use an open-source AI model, you had to find it somewhere, figure out how to download it, write a bunch of setup code, and hope it worked. Hugging Face made it so that running a model is as easy as `pip install transformers` and three lines of code. They did for AI models what GitHub did for code — made sharing and using them trivially easy."

### The analogy
GitHub for AI — models are like repos, datasets are like shared data, Spaces are like hosted demos.

### The one-liner

"Hugging Face is GitHub for AI — a place to find, share, and run open-source models."

---

## 6. Self-Check

1. What are the two different things "Hugging Face" refers to? Which one is this lecture about?
2. Name the three sections of the Hugging Face platform.
3. How would you find an open-source text-generation model under 12B parameters?
4. What's the name format for models on Hugging Face?
5. What's the proper way to share a Gradio app (not `share=True`)?
6. What is a Hugging Face Space? Name three types of apps you can deploy.

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| Hugging Face (platform) | The website: browse models, datasets, and apps |
| Hugging Face (library) | Python packages to run models in your code (next lecture) |
| The Hub | Another name for the Hugging Face platform/website |
| Models (on HF) | ~2 million open-source models to download and use |
| Datasets (on HF) | ~500,000 shared training datasets |
| Spaces | Hosted apps on Hugging Face (Gradio, Streamlit, Docker) |
| Data card | A description page for a dataset explaining what it is and how to use it |
| `gradio deploy` | Terminal command to push a Gradio app to a Hugging Face Space |
| Kaggle | Older platform for datasets and competitions; still big, but HF dominates for transformers |
| PyTorch | The most common deep learning framework; most HF models use it |

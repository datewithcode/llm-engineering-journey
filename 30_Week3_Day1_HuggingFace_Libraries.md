# LLM Engineering – Week 3, Day 1 (Part 2)
## Hugging Face: The Code Libraries (the other side)

> Personal study notes. This covers the Python libraries, NOT the website.
> The website is in 29_Week3_Day1_HuggingFace_Platform.md.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Hugging Face also offers **Python libraries** that let you download, run, inspect, change, and train open-source models in your own code. This is completely different from the website.
2. The most important library is **Transformers** — it lets you run the actual neural network code yourself, not through a black-box API.
3. The key difference from Ollama: Ollama is a pre-packaged app (fast, can't change). Hugging Face libraries give you the raw Python code (slower, but you can fine-tune, swap layers, inspect everything).

---

## 1. Ollama vs Hugging Face Libraries (the key distinction)

Both run open-source models. Completely different how.

| | Ollama | Hugging Face libraries |
|---|---|---|
| What it is | A software application (like an app) | Python code you import and run |
| What you see | A black box — input in, output out | The actual neural network code — step through it, change it |
| Model format | Pre-packaged `.gguf` files, optimized for speed | Raw model weights (parameters) downloaded from the Hub |
| Language | C++ (fast, you can't change it) | Python (slower, you CAN change it) |
| What you can do | Run inference only (ask questions, get answers) | Run inference AND fine-tune AND swap layers AND mess with tokens |
| How you connect | OpenAI-compatible API on localhost | Import directly into your Python code |

**Simple version:** Ollama is a vending machine (put money in, get product out, can't see inside). Hugging Face libraries let you walk into the factory and see every machine on the production line.

**Why both exist:** Ollama is great for quickly running a model locally, especially in a chat or API context. Hugging Face libraries are for when you need to understand, modify, or train the model. Different jobs, both useful.

---

## 2. The Six Libraries

### First row: used in this course

| Library | What it does | When you use it |
|---|---|---|
| **Hub** | Connects your Python code to the Hugging Face website. Downloads models and datasets. | Whenever you need a model or dataset from the platform |
| **Datasets** | Loads and manipulates large datasets efficiently. Each object represents a dataset with tools to filter, transform, etc. | When working with training data |
| **Transformers** | THE big one. Download, run, inspect, and train actual transformer models in Python. The iconic library at the heart of Hugging Face. | All the time from week 3 onwards |

### Second row: advanced (weeks 6-7)

| Library | What it does | When you use it |
|---|---|---|
| **PEFT** | Parameter Efficient Fine Tuning. Train a model without adjusting ALL billions of parameters — only a small subset. Uses a technique called **LoRA** (Low-Rank Adaptation). | Week 7 (fine-tuning) |
| **TRL** | Transformers Reinforcement Learning. Training with RLHF (the technique that turned GPT into ChatGPT) and similar methods. | Advanced training |
| **Accelerate** | Distribute a model across multiple GPUs when it's too big for one. | When models are huge |

### The confusing naming

The **Hub library** (Python code on your machine) connects to the **Hub platform** (the website). Same word "Hub," two things. The library talks to the website:

```
Your code → imports Hub library → Hub library connects to → Hub platform (website) → downloads model
```

### What all these libraries use under the hood

All built on top of **PyTorch** (the most popular deep learning framework). Also supports TensorFlow and JAX, but PyTorch is what nearly everyone uses and what this course uses.

---

## 3. How to Explain This to Someone

### If a non-technical person asks "What are Hugging Face's libraries?"

"You know how Hugging Face has a website full of AI models? Well, they also made free tools that programmers use to actually run those models on their own computers. It's like how Spotify has a website full of music AND an app to play it — the libraries are the 'app' that lets you use the models."

### If a technical person asks

"Hugging Face provides open-source Python libraries — most importantly `transformers` — that let you download, run, fine-tune, and inspect transformer models locally. Unlike Ollama, which wraps models in a C++ runtime and exposes an API, HF's libraries give you the raw PyTorch code. You can step through the forward pass, swap layers, access attention weights, and train with PEFT/LoRA. The `hub` library connects to their model registry, `datasets` handles data loading, and `accelerate` distributes across GPUs."

### The analogy
Ollama = a sealed vending machine (put money in, product out, can't see inside). Hugging Face libraries = walking into the factory and seeing every machine on the production line.

### The one-liner

"Hugging Face's libraries let you run AI models as actual Python code you can see and change, not just as a black-box API."

---

## 4. Self-Check

1. What's the difference between Ollama and Hugging Face libraries? (Use the vending machine analogy.)
2. Name the three main libraries and what each does.
3. Which library is "the big one" and why?
4. What does PEFT stand for? What technique does it use?
5. Why is the "Hub" name confusing? What are the two things called Hub?
6. What is PyTorch and why does it matter here?
7. Can you fine-tune a model with Ollama? With Hugging Face libraries?

---

## 5. Quick Glossary

| Term | Plain meaning |
|---|---|
| Hugging Face libraries | Python packages for downloading, running, and training open-source models |
| Transformers (library) | The main HF library — run actual transformer models in Python |
| Hub (library) | Python package that connects to the HF website to download models/datasets |
| Datasets (library) | Python package for loading and manipulating large datasets efficiently |
| PEFT | Parameter Efficient Fine Tuning — train only a small part of the model |
| LoRA | Low-Rank Adaptation — the specific technique PEFT uses |
| TRL | Transformers Reinforcement Learning — training with RLHF |
| Accelerate | Distribute models across multiple GPUs |
| PyTorch | The deep learning framework most HF libraries are built on |
| `.gguf` | Ollama's packaged model file format — fast but sealed |
| Weights | The actual parameter values (the billions of numbers the model learned) |
| Forward pass | Running the model once on an input — what happens when you ask a question |

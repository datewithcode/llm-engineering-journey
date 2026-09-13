# LLM Engineering – Week 3, Day 1 (Part 3)
## Google Colab: Free GPUs in the Cloud

> Personal study notes. The "why GPUs" explanation is the concept; the rest is practical setup.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. **Google Colab** = a notebook that runs in your browser, but the code executes on Google's computers, not yours. Like remoting into a powerful machine.
2. **Why GPUs matter:** running a model = billions of matrix multiplications. GPUs have thousands of cores that do them all at the same time (in parallel). CPUs do them one by one. That's why AI needs GPUs.
3. **GPU memory (VRAM) is the bottleneck.** All the model's parameters must fit in GPU memory at once. The free Colab GPU (Nvidia T4) has 15GB — enough for most models in this course.
4. **Free tier:** T4 GPU, 15GB VRAM, completely free. Paid tier: A100, 40GB, a few dollars per hour. You only pay for the minutes it's alive.

---

## 1. What Is Google Colab?

A notebook (like Jupyter/Cursor) that runs in a browser window. When you run a cell, the code executes on **Google's machine in the cloud**, not your computer. You see the results instantly as if it's local.

**Three reasons it's great:**

1. **Collaboration.** Like Google Docs for code. Share a notebook, both work in it live. Suits the experimental notebook mindset.
2. **Integration.** Connected to Google Drive — your files are available. Convenient.
3. **GPUs.** The big one. Access to high-end GPUs you don't own. Free.

---

## 2. Why GPUs Matter for AI

### The connection

Running a model = taking billions of parameters and multiplying them by the input tokens, over and over. That's **matrix math** (multiplications and additions).

Key fact: these calculations are **independent** of each other. They can all run **at the same time**.

### CPU vs GPU

| | CPU | GPU |
|---|---|---|
| Cores | A few (4-16) | Thousands (4,000+) |
| Each core | Very powerful, does many different types of tasks | Simple, can only do basic math |
| Speed per core | **Faster** than a GPU core | Slower individually |
| How it works | One calculation at a time (sequential) | Thousands of calculations simultaneously (parallel) |
| Math accuracy | **Perfect** | **Perfect** — identical to CPU |
| Best at | Complex, varied tasks | The same simple math repeated billions of times, all at once |
| Analogy | A university professor — can teach, write papers, solve puzzles | 8,000 people with calculators — can only punch numbers, but all at once |

For 8 billion multiplications, 8,000 cores working in parallel crushes one core working alone. That's why AI needs GPUs.

### "Simpler" does NOT mean "lower quality" (important clarification)

A GPU core is "simpler" because it can only do basic math — it can't write a paper or run a web server. But the math it does is **exactly as accurate** as a CPU. 2 × 3 = 6 on a GPU core, same as on a CPU core. The results are **identical.**

Think of it this way:
- A professor does 8 billion multiplications one by one. Each one is perfect. Takes forever.
- 8,000 people with calculators each do a million. Each one is perfect. Done in minutes.

Same numbers. Same accuracy. Same quality of output. The only difference is speed.

**Parallel does not mean lower quality. It means the same quality, thousands of times faster.**

### The gaming connection

GPUs were originally built for video games. Drawing 3D graphics at 60 frames per second = calculating thousands of polygons = parallel matrix math. Same math AI needs. AI researchers noticed and started using gaming hardware for training models. That's why Nvidia (a graphics card company) became the most important company in AI.

### GPU memory (VRAM) is the bottleneck

All the model's parameters must fit in GPU memory **at once**. Not your computer's RAM — the GPU has its own separate RAM (called VRAM).

- 8B parameter model (like Llama 3.1) ≈ needs ~16GB VRAM
- Bigger models need more
- If it doesn't fit, it can't run

**Apple Silicon exception:** Macs with M1/M2/M3/M4 chips have **unified memory** — CPU and GPU share the same RAM. A Mac with 32GB can use all 32GB for a model. On a PC, the computer might have 32GB RAM but the GPU only has 8GB VRAM — the model must fit in the 8GB.

---

## 3. Google Colab GPU Options

| Tier | GPU | VRAM | Cost | When to use |
|---|---|---|---|---|
| **Free** | Nvidia Tesla T4 | 15GB | $0 | Week 3 and week 7 of this course. Enough for most models. |
| **CPU only** | None | N/A | $0 | Simple tasks that don't need GPU |
| **Paid** | Nvidia A100 | 40GB | ~$2-3/hour | Bigger models, faster training |

You only pay for the minutes the runtime is alive. Stop it when you're done.

### Buy vs rent (the lecturer's argument)

| Buy a GPU | Rent on Colab |
|---|---|
| $3,000-6,000+ upfront | $2-3/hour, only when needed |
| Goes obsolete in 1-2 years | Always current hardware |
| Stuck with what you bought | Pick the GPU you need each time |
| Always available | Subject to availability (free tier can be busy) |

His advice: don't buy a GPU. Rent. Unless you're training models full-time, the math doesn't work out for buying.

---

## 4. How to Find and Use the Colab

Links are in the repo: `week3/day1` notebook has a link, the README has a link, the class resources have a link. Sign in with your Google account. Choose a GPU runtime (free T4).

### Step by step (first time)

1. **Click the Colab link** from the repo. It opens in your browser.
2. **File → Save a copy in Drive.** The lecturer's version is read-only. You need your own copy to run code.
3. **Click the "Connect" button** (top right). Or click the dropdown → "Change runtime type" → select **T4 GPU** → Save → Connect.
4. **Wait for the green tick.** "Connected to T4" appears. Green indicators everywhere = you're live.
5. **Check resources:** click the dropdown → "View resources." You should see ~12GB RAM, **15GB GPU memory**, ~235GB disk.
6. **Run cells from the top,** one at a time, just like in Cursor.

### When things go wrong (memorize this)

```
Things break → Runtime → Disconnect and delete runtime → Reconnect → Start from the top
```

- **Restart session** = resets the Python kernel. Variables cleared, but installed packages stay.
- **Disconnect and delete runtime** = nuclear option. Everything gone, including pip installs. Fresh start.
- **Always start from the top of the notebook.** Not from the middle. Cells depend on earlier cells.

### Gotchas

- **Google can bump you off.** Free tier = best effort. If Google gets busy, you lose your box. Reconnect and start over.
- **Silent downgrade.** Sometimes Google bumps you from T4 to CPU without telling you. Things suddenly get slow or fail. Check the runtime indicator. If it says CPU instead of T4, reconnect.
- **Pip installs vanish.** Every new runtime is a fresh machine. Any `pip install` you did must be redone.
- **Latency.** Code runs in the cloud, not locally. There's a slight delay. Not as interactive as Cursor.
- **Data is wiped.** When you leave, the machine resets. Nothing persists except your saved notebook (in Drive).

### Benefits recap

- Free T4 GPU (15GB VRAM)
- Share and collaborate (like Google Docs for code)
- **Identical environment** for everyone — if it works on your Colab, it works on mine. Eliminates "works on my machine" problems. Best way to share a bug with someone: put it in a Colab.

---

## 5. How to Explain This to Someone

### If a non-technical person asks "What is Google Colab?"

"It's like Google Docs, but instead of writing a document, you're writing and running code. The code runs on Google's powerful computers, not yours. And the best part — Google gives you access to expensive AI hardware for free."

### If a technical person asks

"Google Colab is a hosted Jupyter notebook environment. The runtime executes on Google's cloud infrastructure, giving you access to GPUs (free T4 with 15GB VRAM, paid A100 with 40GB) without any setup. Integrated with Google Drive, supports pip installs, and you can mount your Drive for persistent storage. We use it when we need GPU compute for running or training transformer models that won't fit on CPU alone."

### If they ask "why not just run it on my laptop?"

"Your laptop's CPU would take hours or days for what a GPU does in seconds. And most models need 15-40GB of GPU memory, which your laptop doesn't have. Colab gives you that for free."

### The analogy
CPU = one university professor who can do anything but only one thing at a time. GPU = 8,000 people with calculators who can only do simple math but all at once. Same accuracy, thousands of times faster for the right kind of work.

### The one-liner

"Google Colab is a free notebook in the cloud with access to Nvidia GPUs — you can run AI models without owning expensive hardware."

---

## 6. Self-Check

1. What is Google Colab, in one sentence?
2. Why does AI need GPUs? (The matrix math answer.)
3. What's the difference between CPU and GPU for AI work? (Use the analogy.)
4. What is VRAM and why is it the bottleneck?
5. How is Apple Silicon different from a PC regarding GPU memory?
6. What GPU do you get for free on Colab? How much VRAM?
7. Why does the lecturer say "don't buy a GPU"?

---

## 7. Quick Glossary

| Term | Plain meaning |
|---|---|
| Google Colab | Hosted notebook in a browser; code runs on Google's cloud computers |
| GPU | Graphics Processing Unit — thousands of cores for parallel math, originally for games |
| VRAM | The GPU's own memory (separate from your computer's RAM). All parameters must fit here. |
| Nvidia Tesla T4 | The free GPU on Colab; 15GB VRAM |
| Nvidia A100 | A paid, more powerful GPU on Colab; 40GB VRAM |
| Runtime | The cloud instance you connect to on Colab (CPU-only, T4, or A100) |
| Matrix math | Multiplications and additions on grids of numbers — what running a model actually is |
| Parallel | Many calculations happening at the same time (what GPUs do well) |
| Unified memory | Apple Silicon feature — CPU and GPU share the same RAM |
| VRAM bottleneck | The model must fit in GPU memory; if it doesn't fit, it can't run |

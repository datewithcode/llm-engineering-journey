# LLM Engineering – Week 3, Day 1 (Part 4)
## Colab Practical Setup: HF Token, First Model Run

> Personal study notes. The HF token setup is done once. The diffusion model is a preview.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. Connect Colab to Hugging Face by creating an access token (with **Write** permission) and saving it as a Colab Secret called `HF_TOKEN`. This is the `.env` file equivalent for Colab.
2. He runs a **diffusion model** (image generation, NOT a transformer) on the free T4 GPU using something called **pipelines** (explained tomorrow). ~5GB downloads first, then the GPU does the work.
3. Practical tips: `!` before a command means "run as shell, not Python" (`!pip install`, `!nvidia-smi`). Secrets are tied to your Google account, private, and available in every Colab.

---

## 1. Connecting Colab to Hugging Face (the fiddly part, done once)

### Step 1: Create a Hugging Face access token
1. Go to huggingface.co → click your avatar → Settings → Access Tokens
2. Click "Create new token"
3. **Select Write permission** (not just Read)
4. Give it any name
5. Click Create → copy the token (starts with `hf_`)

**Why Write:** Read lets you download models. Write also lets you **upload** your own models in weeks 6-7. Without Write, uploading breaks later. Set it now.

### Step 2: Save it as a Colab Secret
1. In Colab, click the **key icon** (🔑) on the left sidebar
2. Click "Secrets"
3. Name: `HF_TOKEN`
4. Value: paste the token exactly (no spaces, no extra characters)
5. Toggle **"Notebook access"** ON for this notebook

### Step 3: Use it in code
```python
from google.colab import userdata
from huggingface_hub import login

hf_token = userdata.get('HF_TOKEN')    # reads from Secrets, like os.getenv from .env
login(hf_token)                         # logs into Hugging Face Hub
```

Green tick = you're logged in. This Colab can now download models from (and upload to) Hugging Face.

### How Secrets compare to .env files

| | `.env` file (Cursor/local) | Colab Secrets |
|---|---|---|
| Where it lives | A file in your project folder | Tied to your Google account |
| Who can see it | Anyone with access to the file | Only you, even if you share the notebook |
| Availability | Only in that project | Every Colab you open |
| How to read it | `os.getenv('HF_TOKEN')` | `userdata.get('HF_TOKEN')` |

Secrets are like a `.env` file that follows you everywhere on Colab.

---

## 2. Two Colab Tips

### Running shell commands
In Colab (and Jupyter), put `!` before a command to run it as a shell command instead of Python:

```python
!pip install requests       # installs a package (shell command)
!nvidia-smi                 # shows GPU info (shell command)
import requests             # Python code (no !)
```

### Checking your GPU
```python
!nvidia-smi
```
Shows: GPU model (Tesla T4), VRAM (15GB), current usage. Use this to verify you're actually on a T4 and not silently downgraded to CPU.

You can also check programmatically:
```python
import subprocess
result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
# Parse result to confirm T4
```

---

## 3. What Ran (preview — explained tomorrow)

He used **pipelines** (a Hugging Face feature, covered tomorrow) to run a **diffusion model** from Stability AI.

**Diffusion model vs transformer:**

| | Transformer (what you've been learning) | Diffusion model (what ran here) |
|---|---|---|
| What it does | Predicts next tokens (text) | Generates images from noise |
| Input | Text (tokens) | Text prompt + random noise |
| Output | Text (tokens) | An image |
| Examples | GPT, Claude, Llama | Stable Diffusion, DALL-E |

He asked it to generate "a class of students learning AI engineering in a vibrant pop art style."

### What you see when it runs

1. **Download phase** (~5GB, takes a few minutes): the model weights download from Hugging Face Hub to the Colab machine. CPU memory fills up. GPU memory stays flat. This happens every time because Colab is a fresh machine with nothing cached.
2. **Loading phase:** the model moves from CPU memory to GPU memory. GPU memory fills up.
3. **Generation phase:** the T4 GPU does the actual work. The image appears.

---

## 4. How to Explain This to Someone

### If a non-technical person asks "What happened on the Colab?"

"We connected to a powerful computer in the cloud (for free), downloaded an AI model that can draw pictures, and asked it to draw a classroom of students learning AI. The computer did the math to create the image in about a minute."

### If a technical person asks

"We authenticated with Hugging Face via a write-scoped access token stored in Colab Secrets, then used the `diffusers` pipeline to download and run Stability AI's SDXL-Turbo diffusion model on a free T4 GPU with 15GB VRAM. The model weights (~5GB) download from the HF Hub each session since Colab doesn't persist files across runtimes."

### The analogy
Colab Secrets = a .env file that follows you everywhere on Google, private to your account. The HF token = your key to the model library.

### The one-liner

"We logged into Hugging Face from Colab and ran an image-generation model on a free GPU."

---

## 5. Self-Check

1. What are the three steps to connect Colab to Hugging Face?
2. Why do you need Write permission, not just Read?
3. How are Colab Secrets different from a `.env` file?
4. What does `!` mean before a command in Colab?
5. What command shows your GPU info?
6. What's the difference between a diffusion model and a transformer?
7. Why does the download take so long, and why does it happen every time?

---

## 6. Quick Glossary

| Term | Plain meaning |
|---|---|
| `HF_TOKEN` | Your Hugging Face access token, stored as a Colab Secret |
| `userdata.get(...)` | Colab's equivalent of `os.getenv(...)` — reads a Secret |
| `login(token)` | Authenticates with Hugging Face Hub so you can download/upload models |
| `!command` | Run a shell command from a notebook cell (not Python) |
| `nvidia-smi` | Shell command showing GPU model, memory, and usage |
| Diffusion model | A type of AI specialized for image generation (different from transformers) |
| Pipeline | A Hugging Face feature that wraps a model for easy use (explained tomorrow) |
| SDXL-Turbo | The specific Stability AI diffusion model used in this demo |

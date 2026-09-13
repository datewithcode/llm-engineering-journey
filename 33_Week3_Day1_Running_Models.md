# LLM Engineering – Week 3, Day 1 (Part 5)
## Running Models on Colab: Diffusion, Memory, and Cost

> Personal study notes. Mostly a demo. Three concepts worth keeping.

---

## READ THIS FIRST (whole lecture in 3 lines)

1. A **diffusion model** starts with noise and iterates toward a real image. `num_inference_steps` = how many iterations (more = better quality, slower).
2. GPU memory fills up when a model loads. **Restart the kernel** between model runs to free it. Watch the resource panel.
3. Generating one image on a paid A100 cost ~**$0.04**. Similar to OpenAI's API price. Always **terminate paid sessions** when done.

---

## 1. How Diffusion Models Work (brief)

Training:
1. Take a real image
2. Gradually dissolve it into random noise through many steps
3. The model learns to **reverse** that process: noise → image

Using:
1. Start with random noise + your text prompt
2. The model iterates, refining the noise into an image
3. `num_inference_steps` = how many refinement passes

| Steps | Quality | Speed |
|---|---|---|
| 4 (turbo) | Quick and rough | Fast |
| 30 (base) | Better | Slower |
| More | Even better | Even slower |

This is completely different from transformers (next-token prediction). Diffusion models are specialized for image generation.

---

## 2. What Ran on the T4 (free GPU)

### Model 1: Stability AI SDXL-Turbo (small, fast)
- 4 inference steps
- ~8.5GB GPU memory used
- Quick, rough image. Free model on free hardware.

### Model 2: Stability AI SDXL-Base (bigger)
- 30 inference steps, bigger image
- ~12.7GB GPU memory — nearly maxed the T4 (15GB)
- Better quality, still has AI artifacts

### Model 3: SDXL-Base + Refiner (two-stage)
- Base model does 80% of the steps, refiner does 20%
- Barely fit on the T4. Just squeezed in.
- Noticeably better result

### Model 4: Microsoft SpeechT5 (text-to-speech)
- A **transformer** model (not diffusion), used for audio
- Generated speech: "Hi to an artificial intelligence engineer on the way to mastery"
- Needed a `!pip install` for audio dependencies
- Ran on the free T4

---

## 3. GPU Memory Management

Running a model fills GPU memory. To run a different model, free the memory first.

| Action | What it clears | Pip installs | When to use |
|---|---|---|---|
| Runtime → Restart session | Memory and variables | **Kept** | Switching between models |
| Runtime → Disconnect and delete | Everything | **Gone** | Starting completely fresh |

**Always restart between model runs.** The resource panel (dropdown → View resources) shows current GPU usage. If it's near the top (13-14GB on T4), restart before loading anything else.

---

## 4. What Ran on the A100 (paid GPU)

### Model: Black Forest Labs Flux.1 Schnell
- A famous open-source image generation model. Comes in three sizes: Schnell (small), Dev (medium), Pro (large).
- 4 inference steps
- Used **36.8GB of 40GB** — would NOT fit on a T4 (15GB). Only works on A100 or bigger.
- Result: noticeably better quality than the T4 models. "Pretty cool."

### Cost calculation
```
Time:       240 seconds on A100
Rate:       5 compute units/hour, $10 per 100 units
Estimated:  ~$0.04 for one image
```

**The lecturer's point:** roughly the same price as OpenAI's image API. The advantage of open source isn't cost — it's **control** (you have the code, you can change the model, fine-tune it, run it offline).

---

## 5. CRITICAL: Terminate Paid Sessions

When using a paid GPU (A100), **the meter runs until you stop it.** The $0.04 for the image is cheap, but leaving the session running for hours costs real money.

**When you're done:**
- Runtime → Disconnect and delete runtime, OR
- Runtime → Manage sessions → Terminate

Check "Manage sessions" to see ALL active sessions. Kill anything you're not using.

The free T4 doesn't cost money but Google may bump you off. The paid A100 won't bump you — but it keeps charging.

---

## 6. How to Explain This to Someone

### If a non-technical person asks "What did you do on the GPU?"

"I connected to a powerful computer in the cloud and used free AI models to generate pictures and speech. The computer has a special chip (a GPU) that's very fast at the kind of math AI needs. Google lets you use a basic one for free."

### If a technical person asks

"I ran Stability AI's SDXL-Turbo and Base diffusion models on a free T4 (15GB VRAM), plus Microsoft's SpeechT5 TTS transformer. Then switched to a paid A100 (40GB) to run Flux.1 Schnell, which needed 36.8GB VRAM. Cost was ~$0.04 per image — comparable to OpenAI's API. All models from Hugging Face Hub via the `diffusers` and `transformers` pipeline APIs."

### The analogy
A diffusion model is like a sculptor starting from a block of noise and chipping away step by step until an image emerges. More steps = more refinement.

### The one-liner

"Free GPUs in the cloud can run open-source image and speech models — and the cost is similar to paid APIs like OpenAI."

---

## 7. Day 1 Complete — What's Next

**Day 2 preview:** Two flavors of the Hugging Face API — **pipelines** (the easy way, pre-baked) and the lower-level approach (the hard way, more control). You'll use pipelines for text generation, image generation, and audio.

---

## 8. Self-Check

1. How does a diffusion model generate an image? (Three steps.)
2. What does `num_inference_steps` control?
3. How do you free GPU memory between model runs?
4. How much VRAM does the T4 have? The A100?
5. How much did one image cost on the A100? How does that compare to OpenAI?
6. What must you do when you're done with a paid GPU session?
7. What's the advantage of open source if the cost is similar to paid APIs?

---

## 9. Quick Glossary

| Term | Plain meaning |
|---|---|
| Diffusion model | AI that generates images by iterating from noise to a picture |
| `num_inference_steps` | How many refinement passes the diffusion model makes (more = better, slower) |
| Refiner | A second model that polishes the output of the first |
| SDXL-Turbo / Base | Stability AI's diffusion models (turbo = fast/small, base = slower/bigger) |
| Flux.1 Schnell | Black Forest Labs' open-source image model (needs A100, won't fit on T4) |
| SpeechT5 | Microsoft's text-to-speech transformer model |
| Restart session | Clears GPU memory and variables, keeps pip installs |
| Disconnect and delete | Clears everything, fresh machine, pip installs gone |
| Manage sessions | Colab menu showing all active sessions — terminate unused ones |
| Compute units | Colab's billing unit for paid GPUs (~5 units/hour for A100) |

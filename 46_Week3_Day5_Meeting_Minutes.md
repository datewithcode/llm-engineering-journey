# LLM Engineering – Week 3, Day 5 (Part 2)
## Meeting Minutes Project: Google Drive, Whisper, and the Pipeline

> Personal study notes. Practical project combining frontier and open-source models.
> Notebook: week3/day5 Colab

---

## READ THIS FIRST (whole lecture in 4 lines)

1. The project: audio recording of a meeting → Whisper (speech-to-text) → open-source LLM (generates minutes) → streamed markdown output. A real commercial tool people sell.
2. **Mounting Google Drive** in Colab makes files persist across sessions. Without it, files vanish when the runtime resets.
3. **Whisper** is OpenAI's open-source speech-to-text model. Runs locally via HF pipeline, free, no API key. The reverse of text-to-speech from Day 1.
4. He offers both open-source (Whisper pipeline, free) and closed-source (API call, paid) alternatives for the transcription step. You pick.

---

## 1. Project Structure — Three Steps

```
Denver City Council audio file (a few minutes of meeting audio)
      ↓
STEP 1: Speech-to-text
        Open-source option: Whisper via HF pipeline (free, runs on GPU)
        Closed-source option: OpenAI API call (paid, faster)
      ↓
Text transcript of the meeting
      ↓
STEP 2: Generate meeting minutes
        Open-source LLM (e.g. Llama 3.2) generates summary + action items
      ↓
STEP 3: Stream the output in markdown
        TextStreamer shows the minutes building live
```

### WHY this matters commercially
Products like Otter.ai, Fireflies.ai, and Microsoft Copilot do exactly this. Companies pay subscription fees for automated meeting minutes. This project is a basic version of the same thing.

### What's technically new vs what you already know

| Component | New or known? | Where you learned it |
|---|---|---|
| Speech-to-text (Whisper) | **New** (reverse of Day 1's text-to-speech) | This lecture |
| Google Drive mounting | **New** | This lecture |
| HF pipeline | Known | File 34 |
| Loading a model with quantization | Known | Files 36, 42 |
| TextStreamer for streaming | Known | File 44 |
| Generating with model.generate() | Known | File 36 |

---

## 2. Mounting Google Drive in Colab

### The code

```python
from google.colab import drive
drive.mount('/content/drive')
```

After this, your Google Drive is accessible at `/content/drive/MyDrive/`.

### The permission flow

1. Run the cell
2. A popup appears asking for permissions
3. Click **Yes twice** (one screen requires scrolling down to find the button)
4. Done. Your Drive is now a folder on this machine.

### WHY: the problem it solves

Without Drive: every file you upload to Colab vanishes when the runtime resets. You re-upload every time.

With Drive: files stay on Drive permanently. Every new Colab session can see them instantly after mounting. Upload once, use forever.

### Security note

You're NOT giving Google new access (Google already owns Drive). You're giving THIS NOTEBOOK permission to read your Drive. So you need to trust the code isn't malicious. The lecturer's code is vanilla and inspectable.

### Alternative if you don't want to mount

Click the **Files** icon in the left sidebar → press **Upload** → select from your computer. File goes to `/content/` and works, but disappears when the runtime resets.

---

## 3. The Colab File System Sidebar

Click the folder icon (📁) in the left sidebar:

```
/content/
    sample_data/           ← default data, comes with every runtime
    drive/                 ← your Google Drive (only if mounted)
        MyDrive/
            LLMs/
                denver_extract.mp3    ← the audio file you put here
    denver_extract.mp3     ← OR here if manually uploaded
```

Every new runtime starts fresh with just `sample_data/`. Everything else is temporary unless it's on Drive.

---

## 4. Step 1: Whisper — Speech-to-Text

### Open-source option (free, runs locally)

```python
from transformers import pipeline

transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small.en",
    dtype=torch.float16
)
result = transcriber(audio_file)
transcript = result["text"]
```

### What is Whisper?

| Detail | Answer |
|---|---|
| What | A speech-to-text model |
| Made by | OpenAI (but released as open source) |
| Where it runs | Locally on your GPU via HF pipeline. No API key needed. Free. |
| `.en` suffix | English-only variant (faster, more accurate for English). Remove for multilingual. |
| Reverse of what? | Text-to-speech from Day 1 (Microsoft SpeechT5). That converted text → audio. This converts audio → text. |

### WHY Whisper via pipeline instead of an API call

| | Whisper pipeline (open source) | OpenAI API (closed source) |
|---|---|---|
| Cost | Free (runs on your GPU) | Paid per minute of audio |
| Speed | Depends on your GPU | Fast (OpenAI's hardware) |
| Privacy | Audio stays on your machine | Audio goes to OpenAI's servers |
| Quality | Good (small model) | Better (larger model) |
| Setup | `pip install transformers`, download model | Just an API key |

For this project, either works. He shows both so you can pick.

### Closed-source alternative (paid)

```python
from openai import OpenAI

client = OpenAI()
with open(audio_file, "rb") as f:
    result = client.audio.transcriptions.create(model="gpt-4o-mini-transcribe", file=f, response_format="text")
```

An OpenAI transcription model running on OpenAI's servers. Faster, slightly better quality, costs money (about 1.5 to 3 cents for this clip). Full details in section 6.

---

## 5. The Data Source

**Denver City Council meeting recordings** — a public dataset on Hugging Face. He took a short extract so the transcription doesn't cost too much or take too long.

You can:
- Use his extract (download link provided in the notebook)
- Download your own from the full dataset
- Use any audio file you have (a recorded meeting, a podcast clip, anything)

---

## 6. Step 1 Results: Open Source vs Closed Source

### Closed-source alternative (OpenAI API)

First, add `OPENAI_API_KEY` to Colab Secrets (same as `HF_TOKEN`, under the key icon in the sidebar).

```python
audio_model = "gpt-4o-mini-transcribe"
client = OpenAI(api_key=userdata.get('OPENAI_API_KEY'))
result = client.audio.transcriptions.create(model=audio_model, file=audio_file, response_format="text")
```

### Comparison

| | Open source (Whisper pipeline) | Closed source (OpenAI API) |
|---|---|---|
| Time | ~2 minutes | ~27 seconds |
| Cost | Free | ~$0.03 |
| Quality | Good | Slightly better (minor punctuation differences) |
| Example difference | "...rivers, the kind we've seen" (comma) | "...rivers. The kind we've seen" (period) |

**The takeaway:** the results are "pretty similar." Open source is viable for most use cases. The differences are minor punctuation choices, not meaning. Use open source when cost/privacy matters, closed source when speed matters.

---

## 7. Step 2: Generate Meeting Minutes from the Transcript

### The prompts

**System message:**
```python
system_message = "You produce minutes of meetings from transcripts with summary, discussion points, \
takeaways and action items in markdown format without code blocks."
```

**User message:**
```python
user_prompt = f"Below is a transcript of a Denver Council meeting. Please write minutes in markdown \
without code blocks, including: summary, discussion points, takeaways, action items with owners.\n\n{transcription}"
```

**WHY the repetition** between system and user: saying "markdown without code blocks" and "summary, discussion points, takeaways, action items" in BOTH prompts is deliberate. Repetition biases the model toward your objective. It's more likely to follow instructions it sees twice. Not a mistake, a technique.

### The complete pipeline (everything stitched together)

```python
# 1. Quantization config
quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True,
                                   bnb_4bit_quant_type="nf4")

# 2. Tokenizer
tokenizer = AutoTokenizer.from_pretrained(LLAMA)
tokenizer.pad_token = tokenizer.eos_token           # the annoying boilerplate

# 3. Prepare inputs
messages = [{"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")

# 4. Streamer
streamer = TextStreamer(tokenizer)

# 5. Load model
model = AutoModelForCausalLM.from_pretrained(LLAMA, device_map="auto",
                                               quantization_config=quant_config)

# 6. Generate with streaming
outputs = model.generate(inputs, max_new_tokens=2000, streamer=streamer)
```

Every line is something you've learned this week. This is the culmination: all of it working together on a real task.

### The results

Llama 3.2 produced:
- **Summary:** 11 council members present, location
- **Discussion points:** Councilman Lopez's proclamation for Indigenous Peoples Day
- **Takeaways:** key decisions
- **Action items:** with owners

Displayed as rendered markdown. A real, usable meeting minutes document from an audio file.

---

## 8. Week 3 Complete — 37.5% Progress

### What you can now do

| Skill | Where you learned it |
|---|---|
| Code with frontier APIs | Weeks 1-2 |
| Build a multimodal AI assistant with tools | Week 2 |
| Use HF pipelines for common inference tasks | Week 3, Day 2 |
| Use HF tokenizers (encode, decode, batch_decode, apply_chat_template) | Week 3, Days 2-3 |
| Use HF models (AutoModelForCausalLM, quantization, model.generate) | Week 3, Days 3-4 |
| Understand neural network internals (embedding, layers, LM head, attention, MLP, activation functions) | Week 3, Day 4 |
| Combine frontier and open-source models in one project | Week 3, Day 5 |
| Mount Google Drive in Colab for persistent files | Week 3, Day 5 |
| Speech-to-text with Whisper | Week 3, Day 5 |

### Week 3 assignment: Synthetic Data Generator

Build a tool that generates synthetic datasets using LLMs:
- Describe the kind of data you need (employee records, product descriptions, test cases)
- Describe the structure and purpose
- The LLM generates realistic examples

**WHY:** synthetic data is a core LLM use case applicable to almost any business. Useful for testing, prototyping, training, and filling gaps in real data.

Practice tips: try different models, try quantizing vs not, try different sizes. The more you type out the boilerplate (pad_token, apply_chat_template, BitsAndBytesConfig), the more it becomes second nature.

### Week 4 preview

The single most important question: **"Which LLM is the best?"**
- Comparing models systematically
- Code generation as a benchmark task
- How to pick the right model for your specific use case

---

## 9. How to Explain This to Someone

### If a non-technical person asks "What did you build in week 3?"

"A tool that listens to a recorded meeting and writes the minutes automatically: who was there, what was discussed, what the action items are. We used one AI model to convert the audio to text, and another to write the summary. It cost less than five cents, and there's a free version too."

### If a technical person asks

"A two-stage multimodal pipeline running on a free T4 GPU in Google Colab. Stage 1: STT via Whisper (HF pipeline or OpenAI API). Stage 2: meeting-minutes generation via quantized Llama 3.2 3B (4-bit NF4 via BitsAndBytes), streamed via TextStreamer. Compared open-source and closed-source transcription: roughly equivalent quality at $0 vs $0.03. Full local inference except the optional API call. Google Drive mounted for persistent file access."

### The analogy

A secretary who can listen to a recording and type up the minutes. Whisper is the ears (audio → text). The LLM is the brain (text → organized minutes). Your code connects them. The whole secretary costs $0.03 or less.

### The one-liner

"Audio in, meeting minutes out: Whisper transcribes, an LLM summarizes, all on a free GPU."

---

## 10. Self-Check

1. What are the three steps of the meeting minutes project?
2. How do you mount Google Drive in Colab? What does it solve?
3. What is Whisper? Who made it? Is it free?
4. What does `.en` mean in `whisper-small.en`?
5. What's the difference between using Whisper via pipeline vs via the OpenAI API?
6. Where do uploaded files go on the Colab file system? What happens when the runtime resets?
7. Why is this a real commercial product? Name two companies that sell it.
8. Why is repetition between system and user prompts a good idea, not a mistake?
9. What is the week 3 assignment? Why is synthetic data useful?
10. What's the complete pipeline from tokenizer to streamed output? (Name each step.)

---

## 11. Quick Glossary

| Term | Plain meaning |
|---|---|
| Speech-to-text (STT) | Convert audio to written text. The reverse of TTS. |
| Whisper | OpenAI's open-source speech-to-text model |
| `whisper-small.en` | The small, English-only variant of Whisper |
| `drive.mount()` | Makes your Google Drive accessible as a folder in Colab |
| `/content/drive/MyDrive/` | Where your Drive appears after mounting |
| Colab file browser | The folder icon in the left sidebar; shows the machine's file system |
| `sample_data/` | Default folder on every Colab runtime |
| Denver City Council | The public meeting audio used as example data |
| Otter.ai / Fireflies.ai | Commercial products that do automated meeting minutes |
| Prompt repetition | Saying the same instruction in both system and user prompts to bias the model |
| Synthetic data | Fake but realistic data generated by an LLM for testing, training, or prototyping |
| `OPENAI_API_KEY` | Your OpenAI key, stored as a Colab Secret alongside HF_TOKEN |
| TextStreamer | HF class that prints tokens as generated (streaming) |

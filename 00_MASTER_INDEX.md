# LLM Engineering Course — Master Index of My Notes

> Open this first. Find the concept, open that file, read its READ THIS FIRST section.
> Every file is self-contained. No file requires reading another first.

---

## Quick Concept Finder

| I want to remember... | Open this file |
|---|---|
| What a language model actually does (autocomplete) | 01_Week1_Day3_LLM_Types.md |
| Base vs chat vs reasoning vs hybrid models | 01_Week1_Day3_LLM_Types.md |
| The "Wait" trick / budget forcing | 01_Week1_Day3_LLM_Types.md (section 6) |
| Who the AI labs are, lab vs model vs product | 02_Week1_Day3_Frontier_Models.md |
| Knowledge cutoff (the Docker image idea) | 02_Week1_Day3_Frontier_Models.md |
| Hallucination | 02_Week1_Day3_Frontier_Models.md |
| The wrong-key story (LLMs jump to conclusions) | 02_Week1_Day3_Frontier_Models.md |
| When NOT to use an LLM | 03_Week1_Day3_ChatGPT_Demo_Tokens.md |
| Tokens: the dictionary picture (`"the cat sat"` → `[1, 2, 3]`) | 03_Week1_Day3_ChatGPT_Demo_Tokens.md |
| Why letters/words weren't used, only tokens | 07_Week1_Day4_Tokens.md |
| Tokenizer vs transformer (translator vs brain) | 07_Week1_Day4_Tokens.md |
| Space-before-word tokens, 3-digit numbers, 1000 tokens ≈ 750 words | 08_Week1_Day4_Tokenizer_Demo.md |
| G-P-T meaning, transformer history, attention | 04_Week1_Day4_GPT_Transformer.md |
| Why the transformer beat the LSTM | 05_Week1_Day4_Transformer_Buzzwords.md |
| Emergent intelligence, stochastic parrots | 05_Week1_Day4_Transformer_Buzzwords.md |
| Prompt engineering / copilots / context engineering / agentic AI | 05_Week1_Day4_Transformer_Buzzwords.md |
| What a parameter is (the knob idea) | 06_Week1_Day4_Parameters_Scaling.md |
| How training knows a guess is good or bad | 06_Week1_Day4_Parameters_Scaling.md |
| Training-time vs inference-time scaling | 06_Week1_Day4_Parameters_Scaling.md |
| Why models come in sizes (Haiku/Sonnet/Opus) | 06_Week1_Day4_Parameters_Scaling.md |
| tiktoken encode/decode | 09_Week1_Day4_Illusion_Of_Memory.md |
| **Illusion of memory** (stateless, the growing list) | 09_Week1_Day4_Illusion_Of_Memory.md |
| The three roles: system, user, assistant | 09_Week1_Day4_Illusion_Of_Memory.md |
| **Context window** (the whiteboard) | 10_Week1_Day4_Context_Window_Costs.md |
| API costs, input vs output tokens | 10_Week1_Day4_Context_Window_Costs.md |
| The brochure project plan, why TWO LLM calls | 11_Week1_Day5_Brochure_Plan.md |
| RAG vs tools (who decides what to fetch) | 11_Week1_Day5_Brochure_Plan.md |
| **One-shot / multi-shot prompting** | 12_Week1_Day5_OneShot_JSON.md |
| `response_format` for forced JSON | 12_Week1_Day5_OneShot_JSON.md |
| Iterate-and-refine (THE skill) | 12_Week1_Day5_OneShot_JSON.md |
| Wrapping an LLM call in a plain function | 13_Week1_Day5_Brochure_Prompts.md |
| **Streaming** (stream=True, delta, accumulate) | 14_Week1_Day5_Streaming.md |
| Changing tone with one prompt | 14_Week1_Day5_Streaming.md |
| Week 1 challenges, the tutor exercise | 15_Week1_Day5_WrapUp.md |
| My tutor system prompt | 91_REF_My_Technical_Tutor_System_Prompt.md |
| reasoning_effort parameter | 16_Week2_Model_Comparison.md |
| Two-coins puzzle, bookworm puzzle answers | 16_Week2_Model_Comparison.md |
| Model character (share vs steal) | 16_Week2_Model_Comparison.md |
| **Groq vs Grok** | 16_Week2_Model_Comparison.md |
| Ollama local models | 17_Week2_Local_Models_Routers.md |
| Google/Anthropic client libraries | 17_Week2_Local_Models_Routers.md |
| **Routers (OpenRouter) vs abstraction layers** | 17_Week2_Local_Models_Routers.md |
| LangChain vs LiteLLM | 18_Week2_Abstraction_Layers_Caching.md |
| **Prompt caching** (unchanging content first!) | 18_Week2_Abstraction_Layers_Caching.md |
| Two LLMs arguing (role swap) | 19_Week2_LLM_Conversations.md |
| **Three-way conversation / structured prompt** | 19_Week2_LLM_Conversations.md |
| What Gradio is, Chat Completions vs Responses API | 20_Week2_Day2_Gradio_Intro.md |
| **Callbacks**, gr.Interface, share=True, auth | 21_Week2_Day2_Gradio_Basics.md |
| **return vs yield vs print** | 22_Week2_Day2_Gradio_Streaming.md |
| Gradio streaming, dropdown, swapping models | 22_Week2_Day2_Gradio_Streaming.md |
| **gr.ChatInterface, message + history callback** | 23_Week2_Day3_Chat_UI.md |
| The three-message walkthrough (list grows 2→4→6) | 23_Week2_Day3_Chat_UI.md |
| Clothes store assistant, persona + rules + example | 23_Week2_Day3_Chat_UI.md |
| **RAG explained** (phone-helper analogy, always search) | 23_Week2_Day3_Chat_UI.md |
| **Tools** (boss and secretary) | 24_Week2_Day4_Tools.md |
| Why two calls for tools, the fourth role "tool" | 24_Week2_Day4_Tools.md |
| **Tools in code**: the four notes, handle_tool_call, finish_reason | 25_Week2_Day4_Tools_Code.md |
| The `if` → `while` agentic loop | 25_Week2_Day4_Tools_Code.md |
| Tool function with database (SQLite) | 25_Week2_Day4_Tools_Code.md |
| **Two real definitions of "agent"** | 26_Week2_Day5_Agents_Multimodal.md |
| Five hallmarks: memory, planning, autonomy, orchestration, tools | 26_Week2_Day5_Agents_Multimodal.md |
| Structured outputs = tool calls (same mechanism) | 26_Week2_Day5_Agents_Multimodal.md |
| **Multimodal assistant** (text + image + audio + tools) | 27_Week2_Day5_Finale.md |
| Week 3 preview: Hugging Face, GPUs, Google Colab, open-source models | 27_Week2_Day5_Finale.md |
| **Hugging Face the website** (models, datasets, spaces) | 29_Week3_Day1_HuggingFace_Platform.md |
| **Hugging Face the code libraries**, Ollama vs HF | 30_Week3_Day1_HuggingFace_Libraries.md |
| **Why GPUs**, CPU vs GPU, VRAM bottleneck | 31_Week3_Day1_Google_Colab.md |
| Google Colab setup, restart vs disconnect, gotchas | 31_Week3_Day1_Google_Colab.md |
| HF token as Colab Secret, `!` shell commands | 32_Week3_Day1_Colab_Setup.md |
| Diffusion models, inference steps, GPU memory, cost per image | 33_Week3_Day1_Running_Models.md |
| **Pipelines** (the easy way) | 34_Week3_Day2_Pipelines_Tokenizer.md |
| **AutoTokenizer**, encode/decode, special tokens BOS/EOS | 34_Week3_Day2_Pipelines_Tokenizer.md |
| **apply_chat_template**, how roles become tokens | 35_Week3_Day2_Chat_Template.md |
| tokenize=True vs False vs return_tensors="pt" | 35_Week3_Day2_Chat_Template.md, 36_Week3_Day2_Loading_Models.md |
| **AutoModelForCausalLM**, "causal" meaning | 36_Week3_Day2_Loading_Models.md |
| **Quantization** (4-bit, 8-bit, BitsAndBytes) | 36_Week3_Day2_Loading_Models.md |
| **model.generate**, the complete pipeline dicts → text | 36_Week3_Day2_Loading_Models.md |
| Ed Donner's six courses | 90_REF_Ed_Donner_Course_Curriculum.md |

---

## Reading Sequence (step by step, in this exact order)

Each file builds on the one before. Read in this order the first time. After that, jump to any file using the finder above.

### Foundation (read these first, in order)

| Step | File | What you learn | Depends on |
|---|---|---|---|
| 1 | 01_Week1_Day3_LLM_Types.md | LLM = autocomplete. Base / chat / reasoning / hybrid models. | Nothing. Start here. |
| 2 | 02_Week1_Day3_Frontier_Models.md | The labs, strengths, and the three weaknesses (cutoff, hallucination, jumping to conclusions) | Step 1 |
| 3 | 03_Week1_Day3_ChatGPT_Demo_Tokens.md | First look at tokens (the dictionary picture). When NOT to use an LLM. | Step 1 |
| 4 | 04_Week1_Day4_GPT_Transformer.md | G-P-T, transformer history, attention | Step 1 |
| 5 | 05_Week1_Day4_Transformer_Buzzwords.md | Why transformer won, emergent intelligence, agentic AI definition | Step 4 |
| 6 | 06_Week1_Day4_Parameters_Scaling.md | Parameters, model sizes, training-time vs inference-time scaling | Step 4 |
| 7 | 07_Week1_Day4_Tokens.md | Why tokens, tokenizer vs transformer, word stems | Step 3 |
| 8 | 08_Week1_Day4_Tokenizer_Demo.md | Hands-on tokenizer details, rules of thumb | Step 7 |
| 9 | 09_Week1_Day4_Illusion_Of_Memory.md | **Stateless calls, the growing list, three roles** | Step 1 |
| 10 | 10_Week1_Day4_Context_Window_Costs.md | **Context window (the whiteboard), API costs** | Steps 7, 9 |

### First project (the brochure lab)

| Step | File | What you learn | Depends on |
|---|---|---|---|
| 11 | 11_Week1_Day5_Brochure_Plan.md | The two-call chain, why LLM can't scrape, RAG vs tools preview | Step 9 |
| 12 | 12_Week1_Day5_OneShot_JSON.md | **One-shot prompting, JSON, response_format, iterate** | Step 11 |
| 13 | 13_Week1_Day5_Brochure_Prompts.md | Wrapping LLM calls in functions, the brochure prompts | Step 12 |
| 14 | 14_Week1_Day5_Streaming.md | **Streaming (stream=True, delta, accumulate)**, changing tone | Step 13 |
| 15 | 15_Week1_Day5_WrapUp.md | Business lesson, notebook mindset, challenges | Step 14 |

### Week 2: APIs, UIs, and tools

| Step | File | What you learn | Depends on |
|---|---|---|---|
| 16 | 16_Week2_Model_Comparison.md | reasoning_effort, model character, Groq vs Grok | Step 6 |
| 17 | 17_Week2_Local_Models_Routers.md | Ollama, provider libraries, **routers vs abstraction layers** | Step 16 |
| 18 | 18_Week2_Abstraction_Layers_Caching.md | LangChain, LiteLLM, **prompt caching** | Steps 10, 17 |
| 19 | 19_Week2_LLM_Conversations.md | Two LLMs arguing, **structured prompt for 3+ participants** | Step 9 |
| 20 | 20_Week2_Day2_Gradio_Intro.md | What Gradio is, **Chat Completions vs Responses API** | Nothing new |
| 21 | 21_Week2_Day2_Gradio_Basics.md | **Callbacks**, gr.Interface, share=True, swap one function | Step 20 |
| 22 | 22_Week2_Day2_Gradio_Streaming.md | **return vs yield**, streaming in Gradio, dropdown | Steps 14, 21 |
| 23 | 23_Week2_Day3_Chat_UI.md | **gr.ChatInterface, message+history, RAG explained** | Steps 9, 22 |
| 24 | 24_Week2_Day4_Tools.md | **Tools (boss and secretary)**, the fourth role | Steps 9, 11, 23 |
| 25 | 25_Week2_Day4_Tools_Code.md | **Tools in real code**: the four notes, handle_tool_call, agentic `while` loop, database | Step 24 |
| 26 | 26_Week2_Day5_Agents_Multimodal.md | **Agent definitions**, five hallmarks, structured outputs = tools, multimodal setup | Steps 24, 25 |
| 27 | 27_Week2_Day5_Finale.md | **Multimodal assistant demo**, week 2 wrap-up, week 3 preview (open source, Hugging Face, GPUs) | Step 26 |
| 28 | 28_Week2_Bonus_SVG_Challenge.md | SVG drawing as a model comparison (bonus) | Step 17 |

### Week 3: Open source with Hugging Face

| Step | File | What you learn | Depends on |
|---|---|---|---|
| 29 | 29_Week3_Day1_HuggingFace_Platform.md | **Hugging Face the website**: models, datasets, spaces | Nothing new |
| 30 | 30_Week3_Day1_HuggingFace_Libraries.md | **Hugging Face the code**: six libraries, Ollama vs HF (vending machine vs factory) | Step 29 |
| 31 | 31_Week3_Day1_Google_Colab.md | **Google Colab**, why GPUs (professor vs 8,000 calculators), VRAM bottleneck | Step 6 |
| 32 | 32_Week3_Day1_Colab_Setup.md | HF token as Colab Secret, `!` shell commands, diffusion vs transformer | Step 31 |
| 33 | 33_Week3_Day1_Running_Models.md | Running models on T4 and A100, diffusion steps, memory management, cost | Step 32 |
| 34 | 34_Week3_Day2_Pipelines_Tokenizer.md | **Pipelines** (easy way), **AutoTokenizer** (week 1 dictionary, alive), special tokens BOS/EOS | Steps 7, 30 |
| 35 | 35_Week3_Day2_Chat_Template.md | **apply_chat_template**: how roles become tokens, tokenize=True vs False | Steps 9, 34 |
| 36 | 36_Week3_Day2_Loading_Models.md | **AutoModelForCausalLM**, quantization, model.generate, the complete pipeline | Steps 34, 35 |

### Every concept file has a "How to Explain This to Someone" section
Four parts, always the same shape: non-technical explanation, technical explanation, the analogy, and a one-liner. Use it when someone asks you about a concept — open the file, find that section, read it out.

### Reference (read when needed)
- 90_REF_Ed_Donner_Course_Curriculum.md — the six courses and how they fit
- 91_REF_My_Technical_Tutor_System_Prompt.md — starter prompt for the week 1 exercise
- 92_REF_return_vs_yield_demo.py — runnable script if yield feels fuzzy

### The five concepts everything else builds on
If you only remember five things, remember these. Every other concept is a variation:
1. **LLM = autocomplete** (step 1). Everything is next-token prediction.
2. **Stateless + growing list** (step 9). The model forgets; the list remembers.
3. **Context window = whiteboard** (step 10). Everything must fit.
4. **Two calls with your code in between** (steps 11, 24). The brochure, tools, agents — same pattern.
5. **Iterate the prompt** (step 12). Run, see what's wrong, fix, run again.

---

## The Analogies That Made Things Click

If a concept feels fuzzy, these are the pictures that worked:

| Concept | Analogy |
|---|---|
| Language model | Phone keyboard autocomplete |
| Base model | Person who read every book but never talked to anyone |
| Knowledge cutoff | Docker image, frozen at build time |
| Tokens | Python dictionary lookup, text → numbers |
| Tokenizer vs transformer | Translator at the door vs brain inside |
| Attention | "it was tired" → cat, "it was soft" → mat |
| Parameters | Knobs, adjusted by guess-check-nudge |
| Illusion of memory | New stranger every call, reading a paper that gets longer |
| Context window | A whiteboard of fixed size |
| The student's LLM bug | Mechanic rebuilding the lock when you brought the wrong key |
| return vs yield | Waiter bringing the full meal vs each course as ready |
| yield waiting | Vending machine: press → item → stops → press again |
| Callbacks | Handing someone a recipe card vs cooking it yourself |
| RAG | You sitting next to the phone helper, handing them the one relevant page |
| Tools | Boss locked in an office (LLM) and secretary outside (your code) |
| Prompt caching | Unchanging content first, changing content last |
| Structured prompt | Film script with labelled lines, not role/content dicts |

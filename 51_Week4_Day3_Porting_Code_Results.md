# LLM Engineering – Week 4, Day 3 (Part 2)
## Porting Python to C++ with GPT-5: The Code and the Results

> Personal study notes. No hard concepts, but several small details that each exist for a reason.
> Companion: 50_Week4_Day3_Business_Problem_Code_Porting.md (the why and the setup).

---

## READ THIS FIRST (whole lecture in 4 lines)

1. Your code stores the Python program as a **string**, sends it to GPT-5 in a prompt, gets C++ back as text, cleans it, writes `main.cpp`, compiles it, and runs it. The LLM only ever writes text.
2. Python took **19 seconds** (200 million loop iterations). GPT-5's C++ ran about **230 times faster** in this run (about 45 times in a typical run).
3. Small details with a purpose: `exec()` runs a string as Python, code fences get stripped because the compiler can't read them, timings are run 3 times and the middle one is taken.
4. The real point isn't C++. It's the pattern: **measurable business task → pick a model → run it → measure.**
5. **The surprise:** GPT-5 topped the leaderboard but came **3rd** on this task. Gemini 2.5 Pro won (~1,440×), then Grok 4 (~1,060×), GPT-5 (~233×), Claude Sonnet 4.5 (~184×). Leaderboards shortlist; only your own test picks the winner.

---

## 1. The Flow (your code in every step)

```
YOUR CODE stores the Python program as a text string
      ↓
YOUR CODE runs that string with exec() → prints π, takes 19 seconds (the baseline)
      ↓
YOUR CODE builds messages: system prompt + user prompt (Python text inside)
      ↓
YOUR CODE sends the messages to GPT-5 with reasoning_effort="high"
      ↓
GPT-5 writes back C++ code as text (about 2 minutes of thinking)
      ↓
YOUR CODE strips out any ``` markdown fences
      ↓
YOUR CODE writes the text to main.cpp
      ↓
YOUR CODE compiles main.cpp into an executable and runs it 3 times
      ↓
YOUR CODE prints the times → about 230× faster
```

The LLM never compiles, runs, or saves anything. Same boss-and-secretary pattern as tools (file 24).

---

## 2. The Prompts

### System prompt (fixed)
- Convert Python into high-performance C++
- Respond only with C++, no explanation
- Produce identical output
- Fastest possible execution time

### User prompt (built per program)
- Port this Python code to C++
- Here is the **system type** (your machine)
- Here is the **compile command** that will be used
- Respond only with C++
- Then the Python code itself

### WHY include system info and the compile command
So the LLM writes C++ optimized for that specific machine and those specific compiler settings. The lecturer also iterated with GPT-5 to refine the compile command itself into an efficient one.

---

## 3. The Code, Function by Function

```python
def user_prompt_for(python):
    # builds the user prompt text with system info, compile command, and the Python code
    ...

def messages_for(python):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(python)}
    ]

def write_output(cpp):
    # writes the C++ text to main.cpp
    ...

def port(client, model, python):
    reasoning_effort = "high" if "gpt" in model else None
    response = client.chat.completions.create(
        model=model,
        messages=messages_for(python),
        reasoning_effort=reasoning_effort    # only passed for GPT models
    )
    reply = response.choices[0].message.content
    reply = reply.replace("```cpp", "").replace("```", "")   # strip fences
    write_output(reply)
```

### WHY `client` is passed in
The same `port` function works with any provider (OpenAI, Anthropic, OpenRouter) since they all accept the Chat Completions format (file 17).

### WHY `reasoning_effort` only for GPT models
It's a parameter specific to OpenAI's GPT-5 family (file 16). Other providers would reject it.

---

## 4. Four Small Details and Why Each Exists

### Detail 1: The Python program is stored as a string

```python
py = """
... the pi calculation code ...
"""
exec(py)
```

**WHY:** the LLM needs the code as **text** to include in the prompt. Keeping it as a string means the same text can be sent to the LLM AND run locally for timing.

**What `exec()` does:** runs a string as real Python code.
```python
exec("print(2 + 2)")   # → 4
```

**Caution:** `exec` runs anything. Never `exec` text from an untrusted source. The same applies to compiling and running LLM-generated code: read it before running it.

### Detail 2: Stripping ``` fences from the reply

The system prompt says "respond only with C++," but LLMs often still wrap code in markdown fences like ` ```cpp `.

**WHY strip them:** those characters aren't C++. The compiler would fail on them.

**General lesson:** instructions make a format **likely**, not **guaranteed**. Clean the output in code. (Same idea as `response_format` forcing valid JSON in file 12.)

### Detail 3: Loop unrolling (GPT-5's clever trick)

GPT-5's C++ was much longer than the Python. It had **unrolled the loop**.

Normal loop, one term per step:
```
step 1: add term 1
step 2: add term 2
step 3: add term 3
step 4: add term 4
```

Unrolled loop, several terms per step:
```
step 1: add terms 1, 2, 3, 4
step 2: add terms 5, 6, 7, 8
```

**WHY it's faster:** fewer loop checks and jumps, and the CPU can compute several independent terms at the same time.

**Debatable:** compilers already unroll loops automatically with optimization flags, so the benefit isn't guaranteed.

**Not consistent:** GPT-5 doesn't always do this. Most runs produce a plain translation (about 45× faster). This run produced the unrolled version (about 230× faster). Same prompt, different output, because generation involves sampling (file 41).

### Detail 4: Run 3 times, pick the middle

**WHY:** timings vary between runs (other programs using the CPU, caching effects). Picking the middle of three avoids cherry-picking a lucky or unlucky run.

This is the measurement discipline from file 50: if you judge models on speed, measure fairly.

---

## 5. The Results

| Version | Time | Speed-up |
|---|---|---|
| Python, 200 million iterations | 19 seconds | baseline |
| GPT-5 C++, unrolled, compiled on the lecturer's Mac | a fraction of a second | about 230× |
| GPT-5 C++, typical plain translation | | about 45× |
| Same C++ on an online compiler website | slower (remote machine) | still 20×+ |

### The Python answer
3.14159265 with the last digit slightly off. The Leibniz series converges very slowly, so even 200 million terms isn't perfectly accurate. The C++ must produce the **identical** output to count as correct.

### Running without compiling locally
Paste the C++ into the online compiler website linked in the notebook and press run. Slower than native, but no setup needed.

### Output file names
- Mac / Linux: the executable is called `main`
- Windows: `main.exe`

---

## 5b. Details From the Notebook (not covered in the lecture video)

### The four contenders and the final results

All four models were given the identical prompt and the same Python code. Speed-up = Python time (19.178 s) divided by C++ time.

| Place | Model | C++ time | Speed-up over Python |
|---|---|---|---|
| 1st | Gemini 2.5 Pro | 0.0133 s | ~1,440× |
| 2nd | Grok 4 | 0.0181 s | ~1,060× |
| 3rd | GPT-5 | 0.0822 s | ~233× |
| 4th | Claude Sonnet 4.5 | 0.1042 s | ~184× |

**WHY this matters:** GPT-5 was top of the Artificial Analysis leaderboard, yet came third on this specific task. This is the benchmark limitation from file 48, proven with real numbers: **leaderboards give you a shortlist; only testing on YOUR task picks the winner.**

(These are the lecturer's results from one run each. Because generation involves sampling, your runs may rank differently.)

### How four providers share one `port` function

All four are called through the **OpenAI Python library**, just with a different `base_url`:

```python
openai = OpenAI()   # default: OpenAI's own servers

anthropic = OpenAI(api_key=anthropic_api_key, base_url="https://api.anthropic.com/v1/")
gemini    = OpenAI(api_key=google_api_key,    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
grok      = OpenAI(api_key=grok_api_key,      base_url="https://api.x.ai/v1")
```

Anthropic, Google, and xAI each provide an **OpenAI-compatible endpoint**. So the same `client.chat.completions.create(...)` call works for all four. This is WHY `port(client, model, python)` takes the client as a parameter: swap the client, same code (the Chat Completions standard from file 20).

API keys in `.env`: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GROK_API_KEY`.

### Models used, and cheaper alternatives

| Provider | Model used (higher cost) | Ultra-low-cost alternative |
|---|---|---|
| OpenAI | gpt-5 | gpt-5-nano |
| Anthropic | claude-sonnet-4-5 | claude-haiku-4-5 |
| xAI | grok-4 | grok-4-fast-non-reasoning |
| Google | gemini-2.5-pro | Gemini Flash Lite |

Costs are still low with the bigger models, but switch to the right-hand column if you want to keep spend minimal.

### Where the compile command came from

The notebook uses a helper, `retrieve_system_info()`, to collect details about your machine. It then sends those to GPT with a prompt asking:
- Do I need to install a C++ compiler? If so, give step-by-step instructions.
- What exact `compile_command` gives the fastest runtime?
- What exact `run_command` executes it?

The lecturer's result (on a Mac):

```python
compile_command = ["clang++", "-std=c++17", "-Ofast", "-mcpu=native", "-flto=thin",
                   "-fvisibility=hidden", "-DNDEBUG", "main.cpp", "-o", "main"]
run_command = ["./main"]
```

| Flag | What it does |
|---|---|
| `clang++` | The C++ compiler (Apple's default on Mac) |
| `-std=c++17` | Use the C++17 language version |
| `-Ofast` | Maximum optimization, even bending some strict math rules for speed |
| `-mcpu=native` | Optimize for this exact CPU |
| `-flto=thin` | Link-time optimization across the whole program |
| `-DNDEBUG` | Remove debug checks |
| `-o main` | Name the output executable `main` |

**WHY ask an LLM for this:** the right command depends on your OS, CPU, and installed compiler. Rather than researching it, you let the LLM read your system info and tell you. Your command may differ from the lecturer's.

### What the Python code actually does per loop step

```python
def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2     # 3, 7, 11, ...
        result -= (1/j)             # subtract 1/3, 1/7, 1/11, ...
        j = i * param1 + param2     # 5, 9, 13, ...
        result += (1/j)             # add 1/5, 1/9, 1/13, ...
    return result

result = calculate(200_000_000, 4, 1) * 4
```

Each iteration handles **two** fractions. So 200 million iterations = 400 million terms of the series. The result prints to 12 decimal places, so the C++ must match to 12 decimal places to count as "identical output."

### Why `exec` gets a fresh globals dictionary

```python
def run_python(code):
    globals = {"__builtins__": __builtins__}
    exec(code, globals)
```

This runs the string in a **clean namespace**: only Python's built-in functions are available, and any variables the string creates stay inside that dictionary. **WHY:** so the string's variables (like `result` or `start_time`) can't clash with or overwrite variables already in your notebook.

### What the `subprocess.run` arguments mean

```python
subprocess.run(run_command, check=True, text=True, capture_output=True)
```

| Argument | Meaning |
|---|---|
| `check=True` | Raise an error if the command fails (e.g. compile error) instead of failing silently |
| `text=True` | Return output as a string, not raw bytes |
| `capture_output=True` | Capture what the program prints so Python can read it (`.stdout`) |

### The online compiler

If you don't want to compile locally: https://www.programiz.com/cpp-programming/online-compiler/ (suggested by a student). Paste the C++ and run. Not an exact speed comparison, but you still see the difference.

---

## 6. WHY This Exercise Matters

The purpose is **not** learning C++. It's practising the five-step pattern from file 50:

1. **Understand:** business problem = code too slow; metric = correct output + faster time
2. **Prepare:** pick a candidate from the leaderboards (GPT-5, top of Artificial Analysis for coding)
3. **Select:** run it and measure against the metric

Next: repeat with other models and compare them on the same metric.

---

## 7. How to Explain This to Someone

### If a non-technical person asks "What did you do?"

"I had slow code written in one language. I asked an AI to rewrite it in a faster language. Then I ran both versions and timed them. The AI's version gave the same answer about 45 to 230 times faster. I didn't need to know the faster language myself."

### If a technical person asks

"Prompted GPT-5 (high reasoning effort) with a system prompt demanding C++-only output with identical results and maximum performance, plus a user prompt containing the target platform, compile command, and source. Stripped markdown fences from the completion, wrote it to main.cpp, compiled with optimization flags, and ran it three times taking the median. The Leibniz π benchmark (200M iterations) went from 19s in CPython to roughly 45 to 230 times faster; the 230× run came from manual loop unrolling, which isn't consistent across generations."

### The analogy

Hiring a translator to convert a slow handwritten recipe into a fast kitchen workflow. You check two things: does the dish taste identical, and is it faster? You don't need to speak the translator's language to judge the result.

### The one-liner

"Ask a model to rewrite slow Python as C++, then measure: same answer, much faster, that's the business metric."

---

## 8. Self-Check

1. Walk through the flow. At which steps does the LLM act, and at which does your code act?
2. Why is the Python program stored as a string? What does `exec()` do?
3. Why strip ``` fences from the reply? What general lesson does it teach?
4. What is loop unrolling? Why might it be faster? Why is it debatable?
5. Why did GPT-5 give 230× once but usually about 45×?
6. Why run the program 3 times and take the middle result?
7. Why include the system type and compile command in the user prompt?
8. What is the real purpose of this exercise?
9. Which model won the porting test? Where did GPT-5 place, and why is that surprising?
10. How can one `port` function call OpenAI, Anthropic, Gemini, and Grok?
11. Where did the compile command come from? Why ask an LLM for it?
12. Why does `run_python` pass a fresh `globals` dictionary to `exec`?

---

## 9. Quick Glossary

| Term | Plain meaning |
|---|---|
| `port` | The function that sends Python to an LLM and writes the returned C++ to a file |
| `exec(string)` | Runs a string as Python code |
| Code fences | The ``` markers LLMs use to wrap code in markdown |
| `main.cpp` | The C++ source file the LLM's output is written to |
| Compile | Translate C++ source into a machine-code executable |
| Loop unrolling | Doing several loop steps per iteration to reduce loop overhead |
| Median of runs | The middle value; avoids cherry-picking lucky or unlucky timings |
| `reasoning_effort="high"` | GPT-5 parameter for maximum thinking before answering |
| Baseline | The starting measurement to compare against (Python's 19 seconds) |

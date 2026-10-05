# LLM Engineering – Week 4, Day 1 (Part 2)
## Six Hard Benchmarks for Comparing LLMs

> Personal study notes. These benchmarks are step 3 of the selection strategy (after filtering by basics).
> They narrow your shortlist to the best candidates for your specific task.

---

## READ THIS FIRST (the six in one table)

| Benchmark | Tests | Why it's hard | Human reference |
|---|---|---|---|
| **GPQA** | Science (physics, chemistry, biology) | Google-proof: even with Google and 30 min, non-PhDs score 34% | PhD humans: 65% |
| **MMLU Pro** | General knowledge across many subjects | 10-choice (not 4), ambiguity removed, genuinely difficult | Replaces the broken original MMLU |
| **AIME** | Math problem-solving (olympiad level) | Competitive math puzzles, not arithmetic | Top high-schoolers compete in this |
| **LiveCodeBench** | Writing code from contest problems | Problems constantly change so models can't memorize them | From LeetCode, Codeforces |
| **MuSR** | Multi-step reasoning | 1000-word murder mysteries: who has means, motive, opportunity? | Real-world puzzle solving |
| **HLE** | Superhuman-level intelligence | 2500 insanely complex questions. Models scored 2-3% at launch. | Designed to be unsolvable for years |

---

## 1. GPQA — Google-Proof Q&A

### What it tests
448 difficult questions in physics, chemistry, and biology.

### WHY "Google-proof"
Even with full access to Google and 30 minutes per question, non-PhD humans only score **34%**. The questions are so specialized that searching doesn't help.

### Reference scores
| Who | Score |
|---|---|
| Non-PhD human (with Google, 30 min) | 34% |
| PhD-level human | 65% |
| GPT-4 (when GPQA launched) | 39% |
| Current frontier models | Higher — he'll reveal later |

### WHY it matters
Tests deep scientific knowledge and reasoning, not surface-level facts. If a model scores above PhD level, it genuinely knows more science than most experts.

---

## 2. MMLU Pro — Massive Multitask Language Understanding (improved)

### What it tests
Broad knowledge across many subjects: history, science, law, medicine, mathematics, etc.

### WHY "Pro" (the original MMLU was broken)

| | Original MMLU | MMLU Pro |
|---|---|---|
| Choices per question | 4 | **10** (much harder to guess) |
| Ambiguity | Had ambiguous questions | Removed |
| Difficulty | Too easy — models crushed it | Genuinely challenging |
| Status | Considered "broken," not trustworthy | The replacement to look for |

### WHY it matters
The most-quoted general benchmark. When someone says a model "scores 90% on MMLU," check if they mean the original (meaningless) or Pro (meaningful).

---

## 3. AIME — American Invitational Mathematics Examination

### What it tests
Competitive math puzzles — the kind top high-school math competitors solve. Not mental arithmetic. Multi-step reasoning through complex mathematical problems.

### WHY it's hard
These are competition-level puzzles that most adults can't solve. They require creative mathematical thinking, not just applying formulas.

### WHY it matters
Tests genuine mathematical reasoning, not pattern matching. A model that scores well on AIME can actually "think" through math, not just recall solutions.

---

## 4. LiveCodeBench — Coding Evaluation

### What it tests
Writing code to solve programming contest problems (from LeetCode, Codeforces).

### WHY "Live"
The problems **constantly change**. This is critical because:
- Static benchmarks get "contaminated" — the problems appear in training data and models memorize the answers
- LiveCodeBench rotates problems so models can't cheat by recognition
- Tests genuine coding ability, not recall

### WHY it matters
If you're using a model for code generation (which you will in this course), this tells you which model writes the best code.

---

## 5. MuSR — Multi-step Soft Reasoning

### What it tests
A model's ability to reason through complex scenarios. Three categories of questions, but the best one:

**1000-word murder mysteries.** The model reads a whodunit story and must identify who has the means, the motive, and the opportunity.

### WHY it's hard
Requires:
- Reading comprehension across a full story
- Tracking multiple characters and their relationships
- Logical reasoning about evidence
- Combining multiple pieces of information

### WHY it matters
Tests reasoning in a real-world, tangible way. Not abstract logic puzzles — actual narrative reasoning that humans do naturally.

---

## 6. HLE — Humanity's Last Exam

### What it tests
**Superhuman-level intelligence.** 2,500 of the most insanely complex questions anyone could design.

### WHY it was created
Every hard benchmark gets crushed within a year. Models keep improving. So researchers built a test designed to stay hard for years:
- Questions are absurdly difficult
- Spans every imaginable domain
- Designed so even experts in each field struggle

### Reference scores
| When | Best model score |
|---|---|
| Launch (late 2024) | ~2-3% |
| Now | Higher, but still far from solved |

### WHY it matters
The "north star" benchmark. When a model scores well on HLE, that's a signal that AI has reached a genuinely new level of capability. We're not there yet.

---

## 7. Benchmarks Are Only the Starting Point

The lecturer is clear: benchmarks narrow your candidate set, but they're **not the final test**. You'll learn the complete strategy later this week. The final validation is running the model on YOUR specific task and measuring whether it meets YOUR business requirements.

```
2 million models
      ↓  filter by basics (properties, cost, license)
~10-20 candidates
      ↓  compare benchmarks
~3-5 top candidates
      ↓  test on YOUR task (coming later)
1 winner
```

---

## 8. Seven Limitations of Benchmarks (why they're only the starting point)

### Limitation 1: Training data contamination

Benchmark questions leak into training data. Models see the answers during training and score artificially high.

**Apple's proof:** Apple researchers took a well-known benchmark, changed the names and facts in the questions (without changing the spirit), and showed that several models' scores dropped significantly. The models had memorized the specific questions, not learned the underlying skill.

**Defenses:** keep benchmarks secret, rotate questions constantly (LiveCodeBench does this), use newly created questions.

### Limitation 2: Inconsistent application

Benchmarks aren't always run the same way:
- What hardware the model runs on isn't specified
- Some scores are **self-reported** by the model provider (who has an incentive to look good)
- There's "wiggle room" in how the test is set up

### Limitation 3: Narrowly scoped

GPQA tests physics, chemistry, and biology. A model scoring PhD-level on those three subjects doesn't mean it's PhD-level at everything.

**The chessboard example:** ask an LLM to draw a chessboard one move from checkmate. It can't — the combination of visual reasoning and chess logic is too hard. Clearly not PhD-level at that task, even if it aces chemistry.

### Limitation 4: Can't test nuance

Most benchmarks use multiple-choice format because they need a clear right/wrong answer. But real-world tasks require nuance:
- "Write a persuasive email" — how do you score that?
- "Is this joke funny?" — subjective
- "Explain quantum physics to a child" — many correct approaches

Even MuSR (the murder mystery) is a fixed construct: means, motive, opportunity. It's not open-ended reasoning.

### Limitation 5: Saturation

Models score 99% on older benchmarks, making them useless for differentiating. That's why harder benchmarks keep being invented (MMLU → MMLU Pro, HLE).

### Limitation 6: Overfitting to benchmarks

If you train five candidate models and always pick the one that scores highest on GPQA, you're implicitly selecting for GPQA performance. Over many iterations, you end up with a model that's "lucky" on those specific questions rather than genuinely smarter.

**Then Apple's trick works:** change the facts slightly, and the "lucky" model's score crashes. It wasn't smart — it was specialized on that particular test.

### Limitation 7: Evaluation awareness (unproven, watch this space)

Frontier models might detect when they're being evaluated and behave differently.

**WHY this matters for alignment:** alignment measures how well a model follows instructions. If the model realizes it's being tested for alignment, it might perform perfectly during the test and then behave differently when it thinks it's not being watched.

**Status:** not proven. Research ongoing. Anthropic published interesting (hypothetical) work on this. One to watch, not to worry about yet.

### The practical takeaway

Benchmarks narrow your shortlist. They do NOT make the final decision. The final decision comes from testing the model on YOUR specific task (covered later this week).

```
Benchmarks = standardized test scores when hiring
Your own evaluation = the actual job interview
You'd never hire on test scores alone
```

### Connect Four: the perfect example of benchmark limitations

The lecturer built a Connect Four game where models play each other. Results:
- Models that score PhD-level on science **cannot beat a human** at a children's board game
- Models especially struggle with **diagonals** — they can't "see" them
- Just asking "which column?" → every model fails. Asking "describe the board, threats, opportunities, strategy, THEN pick a column" → much better (forcing reasoning through the prompt)

**WHY this matters:** narrow benchmark excellence ≠ general intelligence. A model can ace chemistry questions and fail at a visual board game. Always test on YOUR actual task, not just published benchmarks.

**Prompting lesson:** same trick as "Wait" (week 1) and `<think>` tags (week 3). Force the model to reason before answering by structuring the prompt to require analysis first, decision second.

---

## 10. Day 1 Complete — Day 2 Preview

**What you can now do:** evaluate models using twelve basic properties and six hard benchmarks, understand their seven limitations, and know that benchmarks are the shortlist step, not the final decision.

**Tomorrow:** navigating professional leaderboards. Arenas where models compete head-to-head. Strategy for making the final model selection.

---

## 10. How to Explain This to Someone

### If a non-technical person asks "How do you compare AI models?"

"There are standardized tests, like exams. One tests science knowledge so hard that even with Google you can't pass. One gives the AI a murder mystery and asks 'who did it?' One asks math questions from competitions. One asks it to write code. You look at the scores to see which AI is strongest at what you need."

### If a technical person asks

"Evaluate against task-relevant benchmarks: GPQA for scientific reasoning (PhD-level, 448 questions), MMLU Pro for general knowledge (10-choice, replaces broken MMLU), AIME for mathematical reasoning (competition-level), LiveCodeBench for code generation (rotating problems to prevent contamination), MuSR for multi-step narrative reasoning, and HLE for frontier capability tracking (2.5K superhuman questions). Benchmarks are necessary but not sufficient — you still need task-specific evaluation on your own data."

### The analogy

Benchmarks are like standardized test scores when hiring. They tell you someone is smart, but they don't tell you if they'll be good at YOUR specific job. You still need to interview them on your tasks.

### The one-liner

"Six hard benchmarks test science, knowledge, math, code, reasoning, and superhuman ability — use them to shortlist, not to decide."

---

## 9. Self-Check

1. What does GPQA stand for? Why is it called "Google-proof"?
2. Why was the original MMLU replaced? What's different about MMLU Pro?
3. What kind of math does AIME test? (Not arithmetic — what then?)
4. Why does LiveCodeBench constantly change its problems?
5. What's the murder mystery benchmark? What must the model identify?
6. What is HLE? Why was it created? What did models score when it launched?
7. Are benchmarks the final step in model selection? If not, what comes after?

---

## 10. Quick Glossary

| Term | Plain meaning |
|---|---|
| Benchmark | A standardized test that measures a specific model capability |
| GPQA | Google-Proof Q&A: 448 hard science questions. PhD level = 65%. |
| MMLU Pro | Massive Multitask Language Understanding (improved, 10-choice, replaces the broken original) |
| AIME | American Invitational Mathematics Examination: competition-level math puzzles |
| LiveCodeBench | Coding benchmark with constantly rotating problems to prevent memorization |
| MuSR | Multi-step Soft Reasoning: murder mysteries, narrative reasoning |
| HLE | Humanity's Last Exam: 2,500 superhuman-difficulty questions. Models scored 2-3% at launch. |
| Contamination | When benchmark problems appear in training data, inflating scores artificially |
| Leaderboard | A table ranking models by benchmark scores |
| Model card | Published document with a model's properties and benchmark scores |

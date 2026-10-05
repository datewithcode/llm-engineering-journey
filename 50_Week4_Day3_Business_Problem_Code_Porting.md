# LLM Engineering – Week 4, Day 3 (Part 1)
## Business Problem First, Two Hats, Five Steps, and the Python-to-C++ Project

> Personal study notes. No hard technical concepts here, but two career-level lessons that matter more than most code.
> Reference: Guide 12 in the course repo's guides folder.

---

## READ THIS FIRST (whole lecture in 4 lines)

1. When someone says "I want an AI agent," always reply: **"What business problem are you solving?"** Start from the problem and how you'll measure success. Sometimes the answer isn't AI at all.
2. An AI engineer wears **two hats**: software engineer (architecture, frameworks) and data scientist (problem, metrics, data). The data scientist questions decide success. Your data is your differentiator.
3. **Five steps** to apply an LLM: Understand → Prepare → Select → Customize → Productionize. This week is "Prepare."
4. The project: use an LLM to convert slow Python into fast C++. Easy to measure: is it still correct, and is it faster?

---

## 1. Lesson 1: Always Push Back to the Business Problem

### The situation
People (including senior executives) come with solutions, not problems:
> "I want an AI agent for my organization."

### Your reply
> "Great. What business problem is that solving?"

### The lecturer's example
> "I want to talk to my phone and ask for today's sales numbers. Give me an agent."

Maybe a Google Doc showing today's sales numbers solves it better: cheaper, faster, no AI needed.

### WHY this matters
- The hype makes everyone want AI, but a solution without a defined problem **can't be measured**, so you can't tell if it worked
- You need the problem first to know **how to measure success**
- The measurement then tells you **which solution** fits
- Sometimes the right answer is **not AI**

**The rule: don't let business people talk in solutions. Bring them back to the problem.**

---

## 2. Lesson 2: The Two Hats of an AI Engineer

| Hat | Typical questions | How much it matters |
|---|---|---|
| **Software engineer** | Which architecture? Which integrations? LangChain or LiteLLM? Chroma, Pinecone, or Weaviate for vectors? | Secondary |
| **Data scientist** | What business problem? How will we measure success? What data do we have? What data is missing? | **Primary** |

### The lecturer's observation
80% of the questions people ask him are engineering questions, because that's their **comfort zone** (many come from software engineering backgrounds).

But the science questions decide whether a project succeeds or fails. Framework choices are necessary decisions, just not the ones that make or break the project.

### WHY: data is the differentiator
Everyone has access to the same frontier models. **Your data** (and how well you understand the problem) is what lets your solution outperform others.

### For someone coming from software engineering
This is the key mindset shift. The instinct is to jump to architecture. Resist it. Spend the most time on: what problem, what metric, what data.

---

## 3. The Five Steps to Apply an LLM (preview, detailed in week 6)

```
1. UNDERSTAND     → Define the business problem and how success is measured
2. PREPARE        → Shortlist candidate models (basics + leaderboards)      ← THIS WEEK
3. SELECT         → Build prototypes, test each against your business metric
4. CUSTOMIZE      → Improve with RAG (week 5), fine-tuning (weeks 6-7), agents (week 8)
5. PRODUCTIONIZE  → Roll out and deploy
```

### WHY this order
- You can't shortlist models (step 2) until you know what they must do (step 1)
- Leaderboards give a shortlist, but only prototypes tested on YOUR metric pick the winner (step 3)
- Customization (step 4) is expensive, so only do it once you've picked a model
- This is why benchmarks alone never make the final decision (file 48)

---

## 4. The Project: Convert Python to Fast C++

### The scenario
- You know Python, not C++
- Your Python code runs too slowly for a business need
- Use an LLM to translate it into C++, which runs much faster

### WHY this is a good test case
Success is easy to measure with two clear numbers:
1. **Correctness:** does the C++ produce the same answer?
2. **Speed:** how much faster is it?

This follows lesson 1: define the business problem (speed) and the metric (correct + faster) **before** picking models.

### Where it leads
The same idea scales to **agentic code porting**: an agent converting an entire codebase from one language or platform to another. This week does just one script; after week 8 you could extend it into an agent.

---

## 5. The Test Code: Calculating π in a Loop

### What it computes

```
1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...  =  π / 4
```

This is the **Leibniz series**. Keep alternately subtracting and adding fractions with odd denominators. The more terms you add, the closer the total gets to π/4. Multiply by 4 and you get approximately π.

The code runs this loop many times, multiplies by 4, then prints:
- the result (should be close to 3.14159...)
- how long it took

### WHY Python is slow at this

| | Python | C++ |
|---|---|---|
| How it runs | **Interpreted**: each line is read and executed by the interpreter at runtime | **Compiled**: translated into machine code before running |
| A loop step | Goes through the interpreter every single iteration | Runs directly on the CPU |
| Speed on heavy loops | Slow | Very fast |
| Comparable to | JavaScript, Ruby | Swift, Rust, Go (all compiled) |

Loops with lots of arithmetic are exactly where the gap is biggest. That's why this test code was chosen.

---

## 6. How to Explain This to Someone

### If a non-technical person asks "How do you decide whether to use AI?"

"Start with the problem, not the technology. If someone says 'we need an AI agent,' ask what problem it solves and how you'd know it worked. Sometimes a simple spreadsheet solves it better. You only reach for AI once you know exactly what success looks like."

### If a technical person asks

"Frame the business problem and success metric before any architecture decisions. Engineering questions (framework, vector DB, orchestration) are secondary to the science questions (objective, evaluation metric, data availability and gaps), because proprietary data and a well-defined metric are the real differentiators. The process: understand requirements, prepare a candidate shortlist from leaderboards, select via prototypes scored on the business metric, customize with RAG, fine-tuning, or agents, then productionize."

### The analogy

A doctor doesn't prescribe medicine because the patient asked for a specific pill. The doctor diagnoses first, then treats. "I want an AI agent" is the patient asking for a pill. Your job is the diagnosis.

### The one-liner

"Problem first, metric second, data third, and only then the technology."

---

## 7. Self-Check

1. Someone says "build me an AI agent." What do you ask, and why?
2. In the sales-numbers example, what might be a better solution than an agent?
3. What are the two hats of an AI engineer? Which questions matter most?
4. Why is data the differentiator between AI solutions?
5. Name the five steps. Which one is this week?
6. Why is Python-to-C++ a good test case? What two things do you measure?
7. What does the Leibniz series calculate? Why multiply by 4?
8. Why is Python slow at loops compared to C++?

---

## 8. Quick Glossary

| Term | Plain meaning |
|---|---|
| Business problem | The actual need being solved, as opposed to the requested solution |
| Success metric | The measurable number that tells you whether the problem is solved |
| Two hats | Software engineer (how to build) and data scientist (what to build and how to measure it) |
| Five steps | Understand, Prepare, Select, Customize, Productionize |
| Code porting | Translating code from one language or platform to another |
| Leibniz series | 1 − 1/3 + 1/5 − 1/7 + ... = π/4 |
| Interpreted language | Executed line by line at runtime by an interpreter (Python) |
| Compiled language | Translated to machine code before running (C++, Swift) |
| Guide 12 | Course guide covering business problem framing and model selection advice |

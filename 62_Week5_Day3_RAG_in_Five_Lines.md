# LLM Engineering – Week 5, Day 3 (Part 3)
## RAG in Five Lines: Joining the Retriever and the LLM, Then a Gradio Chat

> Personal study notes. Read file 60 (retriever and LLM objects) and file 61 (setup, temperature) first.
> Concepts first; code at the end for reference.

---

## READ THIS FIRST (whole lecture in 5 lines)

1. **Retriever alone** returns relevant chunks but no answer. **LLM alone** gives a generic internet answer ("Avery is a given name..."). Neither is RAG.
2. **RAG = connect them.** The `answer_question` function: ask the retriever, glue the chunks into a context block, paste it into the system prompt, ask the LLM, return the answer.
3. Now "Who is Avery?" gives "Avery Lancaster is the co-founder and CEO of Insurellm." That's RAG in **five lines** with LangChain (about ten without).
4. **Fuzzy matching works:** surname only, misspelt names and misspelt products still find the right chunks, because similar text gives nearby vectors.
5. Gradio's chat just needs a function taking **(message, history)**, so `answer_question` plugs straight in. `history` is ignored for now.

---

## 1. Each Helper Alone Is Not RAG

Test question: **"Who is Avery?"**

| Test | What came back | Why |
|---|---|---|
| `retriever.invoke(...)` (librarian alone) | **4 LangChain Documents**: each with an ID, metadata (source, doc_type) and page_content (chunk text) | Encoder (MiniLM) turned the question into a vector; Chroma found the 4 nearest chunks. **No answer, just pages.** |
| `llm.invoke(...)` (expert alone) | "Avery is a given name that can be used for both males and females..." | The LLM wrapper is just ChatOpenAI. It knows nothing about the retriever or Insurellm. "Definitely no RAG happening there." |

```
Librarian alone:  question -> relevant pages              (no answer)
Expert alone:     question -> generic internet answer      (no company knowledge)
Both together:    question -> pages -> expert reads them -> correct company answer   = RAG
```

*(Extra, from my knowledge of LangChain, not the lecture: 4 is the retriever's default number of results; it can be changed.)*

---

## 2. Joining Them: the 5-Step Recipe

### In plain words (what the secretary does)
1. **Ask the librarian:** give the retriever the question; get the closest chunks.
2. **Glue the pages:** join the chunks' text with blank lines between them. This block is the **context**.
3. **Fill the system prompt:** paste the context into the `{context}` slot of the template.
4. **Ask the expert:** send the LLM the filled **system** message plus the question as the **human** message.
5. **Return** the answer text.

### The system prompt template (paraphrased from the lecture)
"You are a knowledgeable, friendly assistant representing the company Insurellm. You are chatting with a user about Insurellm. If relevant, use the given context to answer any question. If you don't know the answer, say so. Context: {context}"

- **LangChain 1.0:** you write this prompt yourself. Older versions packaged it for you; the lecturer prefers it visible.
- **Message objects:** LangChain uses `SystemMessage` and `HumanMessage` objects instead of the list of dicts from OpenAI. "Human" = the "user" role you know.

### Result
"Who is Avery?" now gives: "Avery Lancaster is the co-founder and chief executive officer of Insurellm..."

### LangChain vs doing it yourself
- With LangChain: about **5 lines**.
- By hand (query Chroma, build the prompt, call OpenAI's `create`): about **10 lines**. Week 8 does this.
- The lecturer: "RAG is just not that difficult."

### Reference code (from the notebook, as described)
```python
SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

def answer_question(question, history):
    docs = retriever.invoke(question)                                   # 1. ask the librarian
    context = "\n\n".join(doc.page_content for doc in docs)            # 2. glue the pages
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)      # 3. fill the prompt
    response = llm.invoke([SystemMessage(content=system_prompt),
                           HumanMessage(content=question)])             # 4. ask the expert
    return response.content                                             # 5. return the answer
```
*(Reconstructed from the lecturer's description; exact wording in the notebook may differ slightly.)*

---

## 3. Fuzzy Matching: Proof It Works by Meaning

| Question | Day 1 toy RAG (file 52) | Day 3 real RAG |
|---|---|---|
| "Who is Avery?" | Nothing found | Avery Lancaster, CEO |
| "Who is Lancaster?" | Found | "Lancaster refers to Avery Lancaster" |
| "Who is Avery Lancaster?" with name **misspelt** | Nothing found | "There might be a typo... you might be referring to Avery Lancaster" |
| Product name **misspelt** ("Market llm") | Nothing found | "Marketllm is Insurellm's innovative insurance marketplace" |

**Why:** the misspelt text's vector lands **close** to the correct text's vector, so the nearest chunks are still the right ones. Fuzzy matching, exactly as promised on Day 1.

The lecturer notes MiniLM is "pretty good at this," and the OpenAI embedding models would be even better.

---

## 4. Putting It in a Gradio Chat

- Gradio's chat interface needs a callback taking **(message, history)**. The name doesn't matter ("there's nothing magic about the word chat").
- So: `gr.ChatInterface(answer_question).launch()`.
- **"Bananas" demo:** the lecturer made the function return "bananas"; the chat replied "bananas" to everything. Gradio just displays whatever your function returns (Week 2 refresher).
- **`history` is ignored for now**: each question is answered on its own, with no memory of earlier turns. The lecturer hints this is coming next.

### The whole flow, in the chat
```
Customer types in Gradio
   -> Gradio calls answer_question(question, history)
   -> retriever: question -> vector -> Chroma -> 4 chunks
   -> chunks glued into the system prompt
   -> LLM reads system prompt + question, writes answer
   -> Gradio shows the answer
```

---

## How to Explain This to Someone

### If a non-technical person asks "How does your chatbot know about the company?"
"When you ask a question, the system first searches the company's documents by meaning and pulls out the few most relevant passages. It hands those passages to the AI together with your question and says 'answer using this.' That's why it knows our CEO's name, and why it still works if you misspell it."

### If a technical person asks
"The pipeline is retriever.invoke(query) to get the top-k chunks from Chroma via the embedding model, join their page_content into a context string, format a system prompt template with it, then llm.invoke([SystemMessage, HumanMessage]) and return response.content. Five lines in LangChain, roughly ten by hand. Semantic retrieval handles partial names and typos. It's wired into a Gradio ChatInterface via a (message, history) callback; conversation history isn't used yet."

### The analogy
The librarian finds the pages, the secretary staples them to the question, the expert reads and answers.

### The one-liner
"RAG is retrieve chunks, paste them into the system prompt, ask the LLM: five lines in LangChain."

---

## Self-Check

1. What did `retriever.invoke("Who is Avery?")` return? What did it not return?
2. What did `llm.invoke("Who is Avery?")` return, and why?
3. List the 5 steps of `answer_question`.
4. What goes in the `{context}` slot?
5. What does LangChain call the "user" message?
6. Roughly how many lines is RAG with LangChain? Without?
7. Why does a misspelt name still retrieve the right chunks?
8. What does Gradio's chat need from your function?
9. What did the "bananas" demo prove?
10. What is `history` used for right now?

---

## Quick Glossary

| Term | Plain meaning |
|---|---|
| `answer_question` | The RAG function joining retriever and LLM |
| Context | The retrieved chunks glued into one block of text |
| System prompt template | Prompt with a `{context}` slot to fill in |
| `SystemMessage` / `HumanMessage` | LangChain's message objects for system and user roles |
| `response.content` | The answer text from a LangChain LLM response |
| Fuzzy matching | Finding the right chunks despite different wording or typos |
| `gr.ChatInterface` | Gradio chat UI that calls a (message, history) function |

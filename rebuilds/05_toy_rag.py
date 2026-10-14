# Toy RAG

# Before the user asks anything:
# - the code reads the input file or document 
# - then convert into dictionary mapping based on filename and store content

# When the user asks a question
# - it split the question then search for each keyword and match with stored dictionary if it found then use that value 
# and that value sahre to llm 

import glob
from pathlib import Path

FOLDER = "../llm_engineering/week5/knowledge-base/employees/*"

knowledge = {}

for filename in glob.glob(FOLDER):
    surname_data = Path(filename).stem.split(' ')[-1].lower()
    with open(filename, "r", encoding='utf-8') as f:
        text = f.read()
    knowledge[surname_data] = text

def get_relevant_context(question):
    text = ''.join(ch for ch in question if ch.isalpha() or ch.isspace())
    lower_question = text.lower()
    split_words = lower_question.split()
    data = []
    for i in split_words:
        if i in knowledge:
            data.append(knowledge[i])
    return data

def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        result = "There is no additional context relevant to the user's question."
    else:
        result = "The following additional context might be relevant in answering the user's question:\n\n"
        result += "\n\n".join(relevant_context)
    return result

from openai import OpenAI

question = "who is lancaster?"
SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""
openai = OpenAI(base_url='http://localhost:11434/v1',api_key='ollama')

MODEL = 'qwen2.5:3b'
system_message = SYSTEM_PREFIX + additional_context(question)
messages = [{"role": "system", "content": system_message}] + [{"role": "user", "content":question}]
response = openai.chat.completions.create(model=MODEL, messages=messages)
print(additional_context("Who is Avery?"))
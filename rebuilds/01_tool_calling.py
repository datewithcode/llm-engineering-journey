# Chunk 1: setup and the price function

# Goal: print a Tokyo price with plain Python. No AI yet.

# Type these into the file from memory, no copy-paste. I describe each piece in words; you write the code:

# 1. Import json, and import OpenAI from the openai library
# 2. Create the client, pointing at your local Ollama. Two facts you're allowed to just know:
#    - address: http://localhost:11434/v1
#    - api key: "ollama"
# 3. Set the model name in a variable: "qwen2.5:3b"
# 4. A dictionary of prices: London, Paris, Tokyo ($1400), Berlin
# 5. A function get_ticket_price(destination_city) that looks up the city in the dictionary and returns a sentence like "The price of a ticket to Tokyo is $1400"
# 6. At the bottom: print(get_ticket_price("Tokyo"))

# user input -> secraetory (python code function) -> Boss (LLM) -> secraotory (python code) -> reply to user

import json
from openai import OpenAI

MODEL = "qwen2.5:3b"

openai = OpenAI(base_url='http://localhost:11434/v1',api_key="ollama")

price_ticket = {'london': '$230','paris':'$110','tokyo':'$1400','berlin':'$1210'}

def get_ticket_price(destination_city):
    word_case = destination_city.lower()
    final_price = price_ticket.get(word_case,"unknown").lower() # Price
    return f'The price of a ticket to {word_case} is {final_price}'

print(get_ticket_price("Tokyo"))
print(get_ticket_price("mumbai"))

# 1. A messages list with 2 messages:
#    - a system message: "You are a helpful assistant for an airline called FlightAI. Give short answers."
#    - a user message: "Hi"
# 2. Call the model using your openai client, your MODEL, and your messages, and store the reply in a variable called response
# 3. Print the model's words from response

system_message = "You are a helpful assistant for an airline called FlightAI. Give short answers."

messages = [
    {'role':'system','content':system_message},
    {'role':'user','content':'Hi'}
]
response = openai.chat.completions.create(model=MODEL,messages=messages)
print(response.choices[0].message.content)
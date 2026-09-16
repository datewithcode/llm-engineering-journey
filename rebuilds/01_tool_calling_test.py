# The task

# Write a program that:
# - asks the model "How much is a ticket to Tokyo?"
# - lets the model request your price function
# - runs that function
# - prints the model's final answer, which includes $1400

# Run it any time with:
# python rebuilds/01_tool_calling.py

#FLOW
# user input -> secreorty(Python code) send input and system message and tool menu  -> LLM(read that and send to secrator run tool if needed) -> Secrtorty(python code run and send result with past history and llm own request note with result) -> LLM (read that whole message and send the response to sectory) -> secrotry(send to user repsone)

# user input
# -> Secretory (python) sends input + system message + Add tools menu
# -> LLM reads it, ask secretory to the run tool if needed
# -> Secretory (python) run tool send past history add llm own request note and result
# -> LLM reads the whole conversation writes the answer
# -> Secretory gives the answer to the user
#  "How much is a ticket to Tokyo?"
from openai import OpenAI
import json
MODEL = 'qwen2.5:3b'

openai = OpenAI(base_url='http://localhost:11434/v1',api_key='ollama')

system_message = "You're a helpful AI fligt price tracker assistant!! Help user to get the ticket price give only direct answers no fluff and if you don't know then say so"

price_ticket = {'tokyo':'$1200','boston':'$1000','new york':'$900'}

def get_price_ticket(destination_city):
    lower_city = destination_city.lower()
    price_value = price_ticket.get(lower_city,'')
    return price_value

print(get_price_ticket('boston'))

messages = [
    {'role':'system', 'content':system_message},
    {'role': 'user', 'content': 'How much is a ticket to Tokyo?'},
]
response = openai.chat.completions.create(model=MODEL,messages=messages)
print(response.choices[0].message.content)

## Add tools menu
## LLM can only read from menu if tools is not in menu it won't able work

price_function = {
    'name':'get_price_ticket',
    'description':'Get the flight ticket price',
    'parameters':{
        'type':'object',
        'properties':{
            'destination_city':{'type':'string','description':'The city the customer wants to fly to'},
        },
        'required':['destination_city'],

    },
}
tools = [{'type':'function','function':price_function}]

messages_tools = [
    {'role':'system','content':system_message},
    {'role':'user','content':'How much is a ticket to Tokyo?'}
]
response_tool = openai.chat.completions.create(model=MODEL,messages=messages_tools,tools=tools)
# print(response_tool.choices[0])
# print(response_tool.choices[0].finish_reason == 'tool_calls')
tool_call = response_tool.choices[0].message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)
city = arguments['destination_city']
result = get_price_ticket(city)

messages_tools.append(response_tool.choices[0].message)
messages_tools.append({
    "role":"tool",
    "content": result,
    "tool_call_id":tool_call.id,
})

response = openai.chat.completions.create(model=MODEL,messages=messages_tools)
print("answer", response.choices[0].message.content)
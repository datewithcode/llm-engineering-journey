# Mini-rebuild: only the middle block of tool calling.
# The top (setup + call 1) and the bottom (call 2 + print) are given.
# Write ONLY the part between the two lines of #####.

import json
from openai import OpenAI

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
MODEL = 'qwen2.5:3b'

price_data = {'tokyo': '$50', 'london': '$80'}

def get_price(destination_city):
    return price_data.get(destination_city.lower(), 'unknown')

price_function = {
    'name': 'get_price',
    'description': 'Get the flight ticket price for a city',
    'parameters': {
        'type': 'object',
        'properties': {
            'destination_city': {'type': 'string', 'description': 'The city the customer wants to fly to'},
        },
        'required': ['destination_city'],
        'additionalProperties': False,
    },
}
tools = [{'type': 'function', 'function': price_function}]

messages = [
    {'role': 'system', 'content': 'You help customers with flight ticket prices. Be brief.'},
    {'role': 'user', 'content': 'How much is a ticket to London?'},
]

response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

##########################################################
# YOUR PART: 5 steps
# 1. get the job id
# 2. get the arguments string
# 3. turn the string into a dictionary
# 4. run the function with the city
# 5. the two appends (note 3, then note 4)

get_job_id = response.choices[0].message.tool_calls[0].id
get_arg_str = response.choices[0].message.tool_calls[0].function.arguments
str_to_dict = json.loads(get_arg_str)
func_with_city = get_price(str_to_dict['destination_city'])

messages.append(response.choices[0].message)
messages.append({
    'role':'tool',
    'content': func_with_city,
    'tool_call_id':get_job_id,})

##########################################################

final = openai.chat.completions.create(model=MODEL, messages=messages)
print(final.choices[0].message.content)

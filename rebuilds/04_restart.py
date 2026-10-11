# Tool Calling

# We will use Secretory and boss analogy
# Secretory is python code and boss is LLM

# Workflow
# User ask question -> Sectorty recieves the question then send the system message and user question and tell this price function exist
# Boss reads the secroty message and send the message back to secroty with three things the function name, arguments, job id
# Once secrotary completes the job send the respnse to Boss with old message added as Boss has memory loss issue need to keep remind what conversation was going on
# Boss writes the final sentence using the price and secrotry send the response to user

from openai import OpenAI
import json

openai = OpenAI(base_url='http://localhost:11434/v1',api_key='ollama')

MODEL = 'qwen2.5:3b'

system_message = "You're a helpful AI fligt price tracker assistant!! Help user to get the ticket price give only direct answers no fluff and if you don't know then say so"

price_data = {'tokyo':'$50','london':'$80'}

def get_price(destination_city):
    price_data_lower = destination_city.lower()
    price_respone = price_data.get(price_data_lower,'')
    return price_respone


price_function = {
    'name': 'get_price',
    'description': 'Get the flight ticket price',
    'parameters':{
        'type':'object',
        'properties':{
            'destination_city': {
                'type':'string',
                'description':'The city customer wants to fly to',
            },
        },
        'required':['destination_city'],
        'additionalProperties': False,
    },
}

tools = [{'type':'function','function':price_function}]

messages_response = [
    {'role':'system', 'content':system_message},
    {'role':'user','content':'What is the ticket price for tokyo'}
]

response_part1 = openai.chat.completions.create(model=MODEL,messages=messages_response,tools=tools)
#print(response_part1.choices[0].message)

boss_response = response_part1.choices[0].message.tool_calls
#print(boss_response)

respone_job = response_part1.choices[0].message.tool_calls[0].id
respone_city = response_part1.choices[0].message.tool_calls[0].function.arguments
get_city_dict = json.loads(respone_city)
city_value = get_price(get_city_dict['destination_city'])
print('data-> ',response_part1.choices[0].message)
print('----')
messages_response.append(response_part1.choices[0].message)
messages_response.append({
    "role":"tool",
    "content": city_value,
    "tool_call_id": respone_job,
})
print(messages_response)
final_response = openai.chat.completions.create(model=MODEL,messages=messages_response)
print(final_response.choices[0].message.content)
from openai import OpenAI
import json

## What we are going to do
# user ask chatbot 'How much is a ticket to Tokyo'

# Flow
# user -> secretory -> LLM -> LLM reads and sent back to secrertoy -> sectorarty performs actions -> send to LLM with all chat history -> secrotary -> user respose


MODEL = 'qwen2.5:3b'

openai = OpenAI(base_url='http://localhost:11434/v1',api_key='ollama')

price_ticket = {'tokyo':'$1200','singapore':'$800'}

def get_price_ticket(destination_city):
    lower_city = destination_city.lower()
    city_result = price_ticket.get(lower_city,'')
    return city_result

system_message = "You are a helpful assistant for an airline called FlightAI. Give short answers."

llm_data = [
    {'role':'user','content':'How much is a ticket to Tokyo'},
    {'role':'system','content':system_message},
]
result = openai.chat.completions.create(model=MODEL,messages=llm_data)
#print(result.choices[0].message.content)


price_function = {
    "name":"get_price_ticket",
    "description": "Fetch the price for destination city",
    "parameters":{
        "type": "object",
        "properties": {
            "destination_city":{"type":"string","description":"The city the customer wants to fly to"},
        },
        "required": ["destination_city"]
    },
}
tools = [{'type':'function', 'function': price_function}]

result_tools = openai.chat.completions.create(model=MODEL, messages=llm_data, tools=tools)
llm_id = result_tools.choices[0].message.tool_calls[0].id
llm_destination_city = result_tools.choices[0].message.tool_calls[0]
extract_data = json.loads(llm_destination_city.function.arguments)
city_value = extract_data['destination_city']
price_value = get_price_ticket(city_value)
llm_data.append(result_tools.choices[0].message)
llm_data.append({
    'role':'tool',
    'content':price_value,
    'tool_call_id':llm_id,
})
final_result = openai.chat.completions.create(model=MODEL,messages=llm_data)
print(final_result.choices[0].message.content)

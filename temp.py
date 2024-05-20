from Functions.GoogleSearch import google_search
import json
import os
from groq import Groq


def generate(user_prompt, system_prompt="Be Short and Concise", prints=True) -> str:
    
    function_descriptions = {
        "type": "function",
        "function": {
            "name": "google_search",
            "description": "Gets real-time information about the query",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The query to search on the web",
                    },
                },
                "required": ["search_term"],
            },
        },
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    api_key ='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'
    response = Groq(api_key=api_key).chat.completions.create(
        model='llama3-70b-8192',
        messages=messages,
        tools=[function_descriptions],
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message.content
    if prints: print(f"Initial Response: {response_message} \n")
    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        available_functions = {
            "google_search": google_search,
        }

        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response:str = function_to_call(**function_args)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })

        second_response = Groq(api_key=api_key).chat.completions.create(
            model='llama3-70b-8192',
            messages=messages
        )
        return second_response.choices[0].message.content
    else:
        return response.choices[0].message.content


if __name__ == "__main__":
  # response=google_search("adani")
  response = generate(user_prompt = "who is currently president of india, use tool", prints = True, system_prompt='Be Short and Concise')
  print("Final Response:\n", response)
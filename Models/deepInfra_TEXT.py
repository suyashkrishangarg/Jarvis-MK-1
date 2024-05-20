import os
import requests as rq
requests = rq.Session()
import json
from time import time as t

url = "https://api.deepinfra.com/v1/openai/chat/completions"
headers = {"Authorization": f"Bearer jwt:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnaDoxMjg4MjM2NzQiLCJleHAiOjE3MTc1MDU0NjR9.H9uspHHkOSGE6SHutI-qTHiMaAqzPGKSVo3H-zOs_IQ"}


def generate(message, model="meta-llama/Meta-Llama-3-70B-Instruct"):
    data = json.dumps({
        'model': model,
        'messages': [{"role": "system", "content": "Be Helpful and Friendly. Keep your response straightfoward, short and concise"}, {"role": "user", "content": message}],
        'temperature': 0.7,
        'max_tokens': 512,
        'stop': [],
        'stream': True
    }, separators=(',', ':'))
    result = requests.post(url, headers=headers, data=data, stream=True)

    assistant_response = ""
    for chunk in result.iter_lines():
        chunk_data = chunk.decode("utf-8")
        if chunk_data.startswith("data:"):
            try:
                chunk_json = json.loads(chunk_data[5:])
                if chunk_json["choices"] and chunk_json["choices"][0]["delta"].get("content"):
                    print(chunk_json["choices"][0]["delta"]["content"], end="", flush=True)
                    assistant_response += chunk_json["choices"][0]["delta"]["content"]
            except json.JSONDecodeError:
                break

    return assistant_response

if __name__ == "__main__":
    while True:
        message = input("Ask: ")
        L=t()
        generate(message)
        print("\n"+str(t()-L))
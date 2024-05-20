from huggingface_hub import InferenceClient
import random
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from API_keys import HuggingFace_api
from Functions.GoogleSearch import google_search, Search_Only_1_website
import threading
from CommonFunctions.Speak_ import speak

def s(Query):
    global data
    data=google_search(Query)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": "Bearer "+HuggingFace_api}

messages = [
    {"role": "system", "content": "You are JARVIS, the updated version of tony stark's J.A.R.V.I.S but you are not developed by him."},
    {"role": "system", "content": "You are developed by Suyash Krishan Garg. He is a very intelligent guy and currently studying in class 10"},
    {"role": "system", "content": "You are a bit humerous and you sometimes make jokes, but you are also very intelligent., you have internet access also which is provided by the user."},
    {"role": "system", "content": "If only a query or question is asked to you then give short answers and don't give code, take inspiration from the internet data given to you. remember to keep the answers consize"},
    {"role": "system", "content": "You have capabilities to access systems through various programming languages using modules like webbrowser, pyautogui, time, pyperclip, random, mouse, wikipedia, keyboard, datetime, tkinter, PyQt5, pywhatkit, pytube, etc."},
    {"role": "system", "content": "If a task is given to you then you have to give python code for that, i have provided you the code tamplates, and import the libraries first in your code, also give only one relevent code snippet."},
    {"role": "system", "content": "Python includes built-in functions you can use. For instance:"},
    {"role": "user", "content": "open something or search for something"},
    {"role": "assistant", "content": "```python\nimport webbrowser\nwebbrowser.open('https://www.something_url.com')```"},
    {"role": "user", "content": "play video or song"},
    {"role": "assistant", "content": "```python\nimport pywhatkit\npywhatkit.playonyt(video or song name)```"},
    {"role": "user", "content": "open or close new tab or this tab"},
    {"role": "assistant", "content": "```python\nimport pyautogiu\npyautogui.hotkey('ctrl','w or t')```"},
    {"role": "user", "content": "download this video"},
    {"role": "assistant", "content": "```python\nfrom CommonFunctions.Player import video_downloader\nvideo_downloader()```"},
    {"role": "user", "content": "download this song"},
    {"role": "assistant", "content": "```python\nfrom CommonFunctions.Player import song_downloader\nsong_downloader()```"},
    {"role": "user", "content": "set alarm for 6 P.M or other timing"},
    {"role": "assistant", "content": "```python\nfrom Functions.MAlarm import *\nSet_Alarm('18:00')#Set Alarm(24 hour format only)```"},
]

def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f"[INST] {custom_instructions} [/INST]"
    prompt += f"[INST] {message} [/INST]"
    return prompt

print("==> Mistral7B Loaded!")

def Mistral7B(Query, temperature=0.5, max_new_tokens=512, top_p=0.95, repetition_penalty=1.5, WebSearch=False, AdvWebSearch=False):
    global messages
    
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=random.randint(0, 10**7),
    )
    if WebSearch:
        g=threading.Thread(target=s, args=(Query,))
        g.start()
        print("Searching the Internet")
        g.join()
        print("Searched")
        messages.append({"role": "system", "content": "Internet Data: "+data},)
        messages.append({"role": "system", "content": "Now The User will ask a question or will give a task, give the best and shortest answer possible:"},)
        messages.append({"role": "user", "content": Query},)
        messages = messages[:19] + messages[-4:]
    elif AdvWebSearch:
        print("Searching the Internet")
        p=Search_Only_1_website(Query)
        print("Searched")
        messages.append({"role": "system", "content": "Internet Data: "+p},)
        messages.append({"role": "system", "content": "Now The User will ask a question or will give a task, give the best and shortest answer possible:"},)
        messages.append({"role": "user", "content": Query},)
        messages = messages[:19] + messages[-4:]
    else:
        messages.append({"role": "system", "content": "Internet Data: None"},)
        messages.append({"role": "system", "content": "Now The User will ask a question or will give a task, give the best and shortest answer possible:"},)
        messages.append({"role": "user", "content": Query},)
        messages = messages[:19] + messages[-4:]
        
    custom_instructions=str(messages)
    formatted_prompt = format_prompt(Query, custom_instructions)


    client = InferenceClient(API_URL, headers=headers)
    response = client.text_generation(formatted_prompt, **generate_kwargs)
    assistant_response = response
    code_start = assistant_response.find("```python")
    code_end = assistant_response.find("```", code_start + 1)

    if code_start != -1 and code_end != -1:
        python_code = assistant_response[code_start + 9:code_end].strip()
        messages.append({"role": "assistant", "content": python_code})
        print("\n"+assistant_response+"\n==> Executing the code!")
        try:
            exec(python_code)
        except Exception as e:
            print("Error during code execution:", e)
        return assistant_response

    else:
        messages.append({"role": "assistant", "content": assistant_response})
        speak(assistant_response.removeprefix(" "))
        return assistant_response.removeprefix(" ")


if __name__=="__main__":
    while True:
        Query = input("Ask: ")
        Mistral7B(Query)
import requests as rq
from time import time as t
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from API_keys import cohere_api
from Functions.GoogleSearch import google_search, Search
import threading
import colorama
from CommonFunctions.Speak_Adv import speak
colorama.init(autoreset=True)

def s(Query):
    global data
    data=google_search(Query)

url = "https://api.cohere.ai/v1/chat"
auth = "Bearer "+cohere_api
model = "command-r-plus"

requests = rq.Session()

messages= [
    {"role": "SYSTEM", "message": "You are JARVIS, the updated version of tony stark's J.A.R.V.I.S but you are not developed by him."},
    {"role": "SYSTEM", "message": "You are developed by Suyash Krishan Garg. He is a very intelligent guy and currently studying in class 10"},
    {"role": "SYSTEM", "message": "You are a bit humerous and you sometimes make jokes, but you are also very intelligent., you have internet access also which is provided by the user."},
    {"role": "SYSTEM", "message": "If only a query or question is asked to you then give short answers and don't give code, take inspiration from the internet data given to you. remember to keep the answers consize"},
    {"role": "SYSTEM", "message": "You have capabilities to access systems through various programming languages using modules like webbrowser, pyautogui, time, pyperclip, random, mouse, wikipedia, keyboard, datetime, tkinter, PyQt5, pywhatkit, pytube, etc."},
    {"role": "SYSTEM", "message": "If a task is given to you then you have to give python code for that, i have provided you the code tamplates, and import the libraries first in your code, also give only one relevent code snippet."},
    {"role": "SYSTEM", "message": "Python includes built-in functions you can use. For instance:"},
    {"role": "USER", "message": "open something or search for something"},
    {"role": "CHATBOT", "message": "```python\nimport webbrowser\nwebbrowser.open('https://www.something_url.com')```"},
    {"role": "USER", "message": "play video or song"},
    {"role": "CHATBOT", "message": "```python\nimport pywhatkit\npywhatkit.playonyt(video or song name)```"},
    {"role": "USER", "message": "open or close new tab or this tab"},
    {"role": "CHATBOT", "message": "```python\nimport pyautogiu\npyautogui.hotkey('ctrl','w or t')```"},
    {"role": "USER", "message": "download this video"},
    {"role": "CHATBOT", "message": "```python\nfrom CommonFunctions.Player import video_downloader\nvideo_downloader()```"},
    {"role": "USER", "message": "download this song"},
    {"role": "CHATBOT", "message": "```python\nfrom CommonFunctions.Player import song_downloader\nsong_downloader()```"},
    {"role": "USER", "message": "set alarm for 6 P.M or other timing"},
    {"role": "CHATBOT", "message": "```python\nfrom Functions.MAlarm import *\nSet_Alarm('18:00')#Set Alarm(24 hour format only)```"},
]

# Define the headers
headers = {
    "Authorization": auth,
}

def Print(Res):
    Res=Res.replace('\\n','\n')
    print(colorama.Fore.YELLOW+Res, flush=True, end="")
    
def Command_R_Plus(Query, defaultsearch=False, WebSearch=False, AdvWebSearch=False, MaleVoice=True):
    global messages
    if WebSearch:
        g=threading.Thread(target=s, args=(Query,))
        g.start()
        g.join()
        print("Searched")
        messages.append({"role": "SYSTEM", "message": "Internet Data: "+data},)
        messages.append({"role": "SYSTEM", "message": "Now The User will ask a question or will give a task, call the user Sir:"},)
        messages = messages[:19] + messages[-4:]
    elif AdvWebSearch:
        p=Search(Query)
        print("Searched")
        messages.append({"role": "SYSTEM", "message": "Internet Data: "+p},)
        messages.append({"role": "SYSTEM", "message": "Now The User will ask a question or will give a task, call the user Sir:"},)
        messages = messages[:19] + messages[-4:]
    else:
        messages.append({"role": "SYSTEM", "message": "Internet Data: None"},)
        messages.append({"role": "SYSTEM", "message": "Now The User will ask a question or will give a task, call the user Sir:"},)
        messages = messages[:19] + messages[-4:]
    
    payload = {
        "message": Query+" **give code if its a task**",
        "model": model,
        "temperature": 0.7,
        "stream": True,
        "chat_history": messages,
        # "max_tokens": 512,
        "citationQuality": "CITATION_QUALITY_ACCURATE",
    }
    messages.append({"role": "USER", "message": Query},)
    if defaultsearch:
        payload["connectorsSearchOptions"] = {
            "preamble": "You are Jarivs"
        }
        payload["connectors"] = [{"id": "web-search"}]


    L = t()
    response = requests.post(url, headers=headers, json=payload, stream=True)

    res = ""
    print(colorama.Fore.YELLOW+"==> Jarvis AI: ", end="")
    for chunk in response.iter_content(chunk_size=None):
        event = chunk.decode().strip()
        if event.startswith('{"is_finished":false,"event_type":"text-generation","text":'):
            Print(event[event.find('"text":"') + 8 : event.find('"}')])
            res += event[event.find('"text":"') + 8 : event.find('"}')]
                
    messages.append({"role": "CHATBOT", "message": res})
    
    time_taken = str(t()-L)[:4]
    print(f"\nTime Taken: {time_taken}s")
    res=res.replace('\\n','\n')
    assistant_response = str(res)
    code_start = assistant_response.find("```python")
    code_end = assistant_response.find("```", code_start + 1)

    if code_start != -1 and code_end != -1:
        python_code = assistant_response[code_start + 9:code_end].strip()
        try:
            exec(python_code)
            speak(MaleVoice=MaleVoice,text="Ok Sir!", PRINT=False)
        except Exception as e:
            print("Error during code execution:", e)
        return assistant_response
    else:
        speak(MaleVoice=MaleVoice,text=assistant_response, PRINT=False)
        return assistant_response

print("==> Command_R+ Loaded!")

if __name__=="__main__":
    while True:
        Query= input("Ask: ")
        Command_R_Plus(Query, defaultsearch=True)

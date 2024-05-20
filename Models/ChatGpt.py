from g4f.client import Client
client = Client()
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from Functions.GoogleSearch import google_search
import threading

def s(Query):
    global data
    data=google_search(Query)
    
conversation_history_gpt = [
    {"role": "system", "content": "You are JARVIS, the updated version of tony stark's J.A.R.V.I.S but you are not developed by him."},
    {"role": "system", "content": "You are developed by Suyash Krishan Garg. He is a very intelligent guy and currently studying in class 10"},
    {"role": "system", "content": "You are a bit humerous and you sometimes make jokes, but you are also very intelligent., you have internet access also which is provided by the user."},
    {"role": "system", "content": "If only a query or question is asked to you then give short, clear and consize answers and don't give code, take inspiration from the internet data given to you. remember to keep the answers very short"},
    {"role": "system", "content": "You have capabilities to access systems through various programming languages using modules like webbrowser, pyautogui, time, pyperclip, random, mouse, wikipedia, keyboard, datetime, tkinter, PyQt5, pywhatkit, pytube, etc."},
    {"role": "system", "content": "If a task is given to you then you have to always give python code for that, i have provided you the code tamplates, and import the libraries first in your code, also give only one relevent code snippet."},
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
    {"role": "system", "content": "Python includes built-in functions you can use. For instance:"},
    {"role": "user", "content": "set alarm for 6 P.M or other timing"},
    {"role": "assistant", "content": "```python\nfrom Functions.MAlarm import *\nSet_Alarm('18:00')#Set Alarm(24 hour format only)```"},
    {"role": "system", "content": """If user gives task to download this video then use this built in function(don't ask for url, its builtin):```python\nfrom CommonFunctions.Player import video_downloader\nvideo_downloader()```"""},
    {"role": "system", "content": """If user gives task to download this song then use this built in function(don't ask for url, its builtin):```python\nfrom CommonFunctions.Player import video_downloader\nsong_downloader()```"""},
]

def ChatGPT(Query, WebSearch=False):
    global conversation_history_gpt
    if WebSearch:
        g=threading.Thread(target=s, args=(Query,))
        g.start()
        print("Searching the Internet")
        g.join()
        print("Searched")
        conversation_history_gpt.append({"role": "system", "content": "Internet Data: "+data},)
        conversation_history_gpt.append({"role": "user", "content": Query},)
        conversation_history_gpt = conversation_history_gpt[:23] + conversation_history_gpt[-3:]
    else:
        conversation_history_gpt.append({"role": "system", "content": "Internet Data: None"},)
        conversation_history_gpt.append({"role": "user", "content": Query},)
        conversation_history_gpt = conversation_history_gpt[:23] + conversation_history_gpt[-3:]

    # Generate response
    response = client.chat.completions.create(
        # provider="ChatgptX",
        model="gpt-3.5-turbo",
        messages=conversation_history_gpt,
    )

    # Append response to conversation history
    assistant_response = response.choices[0].message.content
    code_start = assistant_response.find("```python")
    code_end = assistant_response.find("```", code_start + 1)

    if code_start != -1 and code_end != -1:
        python_code = assistant_response[code_start + 9:code_end].strip()
        conversation_history_gpt.append({"role": "assistant", "content": python_code})
        print("\n"+assistant_response+"\n==> Executing the code!")
        try:
            exec(python_code)
        except Exception as e:
            print("Error during code execution:", e)
        return "Task Completed Sir!"
    else:
        conversation_history_gpt.append({"role": "assistant", "content": assistant_response})
        return assistant_response

print("==> Chat GPT Loaded!")

if __name__=="__main__":
    while True:
        Query = input("Ask: ")
        print(ChatGPT(Query))
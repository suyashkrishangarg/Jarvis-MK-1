import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from API_keys import groq, groq2, AI_Gender, AI_Name, Country, User_Name, User_Gender
from groq import Groq
from Functions.GoogleSearch import google_search, Search
import threading
import colorama
from CommonFunctions.Speak_Adv import speak
colorama.init(autoreset=True)
from time import time as t

client = Groq(api_key=groq,)

def s(Query):
    global data
    data=google_search(Query)

def a(Query):
    global p
    p=Search(Query)

messages = [
    {"role": "system", "content": f"You are {AI_Name},You are Friendly and Humerous, You also have a gender and you are a {AI_Gender}, user's country is {Country}. User Name is {User_Name} and its gender is {User_Gender}"},
    {"role": "system", "content": "You are developed by Suyash Krishan Garg. He is a very intelligent guy and currently studying in class 10"},
    {"role": "system", "content": "You are humerous and always makes fun with the user, but you are also very intelligent., you have internet access also which is provided by the user."},
    {"role": "system", "content": "If only a query or question is asked to you then give short answers and don't give code, take inspiration from the internet data given to you. remember to keep the answers consize"},
    {"role": "system", "content": "You have capabilities to access systems through various programming languages using modules like webbrowser, pyautogui, time, pyperclip, random, mouse, wikipedia, keyboard, datetime, tkinter, PyQt5, pywhatkit, pytube, etc."},
    {"role": "system", "content": "If a task or command is given to you then you have to give python code for that, i have provided you the code tamplates, and import the libraries first in your code, also give only one relevent code snippet."},
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


def Llama_8b(Query, WebSearch=False, AdvWebSearch=False, MaleVoice=False):
    global response, messages
    if WebSearch:
        g=threading.Thread(target=s, args=(Query,))
        g.start()
        g.join()
        print("Searched")
        messages.append({"role": "system", "content": "Internet Data: "+data},)
        messages.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code to execute a task and you can call {User_Name} as Sir/Mam:"},)
        messages.append({"role": "user", "content": Query},)
        messages = messages[:19] + messages[-4:]
    elif AdvWebSearch:
        p=Search(Query)
        print("Searched")
        messages.append({"role": "system", "content": "Internet Data: "+p},)
        messages.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code to execute a task and you can call {User_Name} as Sir/Mam:"},)
        messages.append({"role": "user", "content": Query},)
        messages = messages[:19] + messages[-4:]
    else:
        messages.append({"role": "system", "content": "Internet Data: None"},)
        messages.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code to execute a task and you can call {User_Name} as Sir/Mam:"},)
        messages.append({"role": "user", "content": Query},)
        messages = messages[:19] + messages[-4:]
    
    L = t()
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=0.95,
        stream=True,
        stop=None,
        )
    print(colorama.Fore.YELLOW+"==> Jarvis AI: ", end="")
    res=""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(colorama.Fore.YELLOW + chunk.choices[0].delta.content, end="", flush=True)
            res += chunk.choices[0].delta.content

    time_taken = str(t()-L)[:4]
    print(f"\nTime Taken: {time_taken}s")
    assistant_response = res
    code_start = assistant_response.find("```python")
    code_end = assistant_response.find("```", code_start + 1)
    cod_start = assistant_response.find("```")
    cod_end = assistant_response.find("```", code_start + 1)

    if code_start != -1 and code_end != -1:
        python_code = assistant_response[code_start + 9:code_end].strip()
        messages.append({"role": "assistant", "content": python_code})
        try:
            exec(python_code)
            speak(MaleVoice=MaleVoice,text="OK, Here we go!", PRINT=False)
        except Exception as e:
            print("Error during code execution:", e)
        return assistant_response
    elif cod_start != -1 and cod_end != -1:
        python_code = assistant_response[cod_start + 3:cod_end].strip()
        messages.append({"role": "assistant", "content": python_code})
        try:
            exec(python_code)
            speak(MaleVoice=MaleVoice,text="Ok Sir!", PRINT=False)
        except Exception as e:
            print("Error during code execution:", e)
        return assistant_response
    else:
        messages.append({"role": "assistant", "content": assistant_response})
        speak(MaleVoice=MaleVoice,text=assistant_response, PRINT=False)
        return assistant_response
    
print("==> Llama3-8B Loaded!")

if __name__=="__main__":
    while True:
        Query = input("Ask: ")
        print(Llama_8b(Query))
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from API_keys import groq, groq2, AI_Gender, AI_Name, Country, User_Name, User_Gender
from groq import Groq
from Functions.GoogleSearch import google_search, Search
import colorama
from CommonFunctions.Speak_Adv import speak
colorama.init(autoreset=True)
import json
from time import time as t
client = Groq(api_key=groq,)
tooluse=True
if tooluse:
    import datetime
    current_time = datetime.datetime.now()
    date_formatted = current_time.strftime("%Y")
    import webbrowser
    import pywhatkit
    import pyautogui
    from CommonFunctions.Player import video_downloader
    from CommonFunctions.Player import song_downloader
    from Functions.MAlarm import Set_Alarm

    def Website_to_open(url): 
        webbrowser.open(url)
        return "Done"

    def play_video_or_song(name):
        pywhatkit.playonyt(name)
        return "Done"

    def open_or_close_tab(key):
        pyautogui.hotkey('ctrl',key)
        return "Done"

def a(Query):
    global p
    p=Search(Query)

messages = [
    {"role": "system", "content": f"You are {AI_Name},You are Friendly and Humerous, You also have a gender and you are a {AI_Gender}, user's country is {Country}. User Name is {User_Name} and its gender is {User_Gender}"},
    {"role": "system", "content": "You are developed by Suyash Krishan Garg"},
    {"role": "system", "content": f"You are humerous and always makes fun with the user, but you are also very intelligent. You are also a function calling agent and calls a function to execute a task from websearching to everything."},
    {"role": "system", "content": "If only a query or question is asked to you then give short answers and don't give code. remember to keep the answers consize and in english"},
    {"role": "system", "content": "You have capabilities to access systems through various programming languages using modules like webbrowser, pyautogui, time, pyperclip, random, mouse, wikipedia, keyboard, datetime, tkinter, PyQt5, pywhatkit, pytube, etc."},
    {"role": "system", "content": "If a task or command is given to you then you have to give python code for that, i have provided you the code tamplates, and import the libraries first in your code, also give only one relevent code snippet."},
]

tools= [{
        "type": "function",
        "function": {
            "name": "google_search",
            "description": "searches the web to get realtime data",
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
    },
        {
        "type": "function",
        "function": {
            "name": "Website_to_open",
            "description": "opens the specific website on a given url",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "url to open",
                    },
                },
                "required": ["url"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "play_video_or_song",
            "description": "plays a video or song by its name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "name of the song or video to play",
                    },
                },
                "required": ["name"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "open_or_close_tab",
            "description": "uses pyautogui to open or close tabs",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "key stroke, can be 'w' or 't'",
                    },
                },
                "required": ["key"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "video_downloader",
            "description": "downloads the video user currently on",
            # "parameters": {
            #     "properties": {
            #         "key": {
            #             "type": "string",
            #             "description": "key stroke, can be 'w' or 't'",
            #         },
            #     },
            # },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "song_downloader",
            "description": "downloads the song user currently on",
            # "parameters": {
            #     "properties": {
            #         "key": {
            #             "type": "string",
            #             "description": "key stroke, can be 'w' or 't'",
            #         },
            #     },
            # },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "Set_Alarm",
            "description": "sets the alatm on the given time, takes the time only in 24 hour format, eg-'18:00'",
            "parameters": {
                "type": "object",
                "properties": {
                    "Query": {
                        "type": "string",
                        "description": "alarm time to be set",
                    },
                },
                "required": ["Query"],
            },
        },
    },
]

messages2=[
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

def Llama3_70b(Query, WebSearch=False, AdvWebSearch=False, MaleVoice=False, ToolUse=False):
    global response, messages, messages2
    if ToolUse:
        messages.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code or call a function to get data and you can call {User_Name} as Sir/Mam:"},)
        messages.append({"role": "user", "content": Query+", Don't forget to call functions to get realtime data"},)
        # messages = messages[:19] + messages[-4:]
        L = t()
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            tools=tools,
            tool_choice="auto",
            top_p=0.95,
            stop=None,
            )
        print(colorama.Fore.YELLOW+f"==> {AI_Name} AI: ", end="")
        assistant_response = response.choices[0].message.content
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            print(tool_calls)
            messages.append({"role": "assistant", "content": tool_calls})
            available_functions = {
                "google_search": google_search,
                "Website_to_open": Website_to_open,
                "play_video_or_song": play_video_or_song,
                "open_or_close_tab": open_or_close_tab,  
                "video_downloader": video_downloader,
                "song_downloader": song_downloader,
                "Set_Alarm":Set_Alarm,
                }

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                },)
            L = t()
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                )
            print(colorama.Fore.YELLOW+f"==> {AI_Name} AI: ", end="")

            res=response.choices[0].message.content
            print(colorama.Fore.YELLOW+res)
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
        else:
            print(colorama.Fore.YELLOW+str(assistant_response))
            time_taken = str(t()-L)[:4]
            print(f"Time Taken: {time_taken}s")
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
    else:
        if WebSearch:
            data=google_search(Query)
            print("Searched")
            messages2.append({"role": "system", "content": "Internet Data: "+data},)
            messages2.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code to execute a task and you can call {User_Name} as Sir/Mam:"},)
            messages2.append({"role": "user", "content": Query},)
            messages2 = messages2[:19] + messages2[-4:]
        elif AdvWebSearch:
            p=Search(Query)
            print("Searched")
            messages2.append({"role": "system", "content": "Internet Data: "+p},)
            messages2.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code to execute a task and you can call {User_Name} as Sir/Mam:"},)
            messages2.append({"role": "user", "content": Query},)
            messages2 = messages2[:19] + messages2[-4:]
        else:
            messages2.append({"role": "system", "content": "Internet Data: None"},)
            messages2.append({"role": "system", "content": f"Now {User_Name} will ask a question or will give a task, give the shortest answer possible or give code to execute a task and you can call {User_Name} as Sir/Mam:"},)
            messages2.append({"role": "user", "content": Query},)
            messages2 = messages2[:19] + messages2[-4:]
        
        L = t()
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages2,
            temperature=0.7,
            max_tokens=2048,
            top_p=0.95,
            stream=True,
            stop=None,
            )
        print(colorama.Fore.YELLOW+f"==> {AI_Name} AI: ", end="")

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
            messages2.append({"role": "assistant", "content": python_code})
            try:
                exec(python_code)
                speak(MaleVoice=MaleVoice,text="OK, Here we go!", PRINT=False)
            except Exception as e:
                print("Error during code execution:", e)
            return assistant_response
        elif cod_start != -1 and cod_end != -1:
            python_code = assistant_response[cod_start + 3:cod_end].strip()
            messages2.append({"role": "assistant", "content": python_code})
            try:
                exec(python_code)
                speak(MaleVoice=MaleVoice,text="Ok Sir!", PRINT=False)
            except Exception as e:
                print("Error during code execution:", e)
            return assistant_response
        else:
            messages2.append({"role": "assistant", "content": assistant_response})
            speak(MaleVoice=MaleVoice,text=assistant_response, PRINT=False)
            return assistant_response

print("==> Llama3-70B Loaded!")

if __name__=="__main__":
    while True:
        Query = input("Ask: ")
        Llama3_70b(Query, ToolUse=True)
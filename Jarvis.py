Recognition = True
MaleVoice:bool=False
LLAMA_Slow=True
Cohere_AI= True
Advance_WebSearch=False #very slow 
Internet_Access = False
Hindi_support= False


print("==> Broom Broom... Starting...")
import sys
import os
from playaudio import playaudio
import threading
from time import time as t
import pyautogui
import webbrowser
import json

current_dir=os.getcwd()
sys.path.append(current_dir)

print("==> Initializing...\n")
L=t()

def task1():
    global speechrecognition
    from CommonFunctions.SpeechRecog import speechrecognition

def task2():
    global MainClapExe
    from CommonFunctions.Clap import MainClapExe

def task3():
    global PlayOnYT, video_downloader, clipboard_data, Search, song_downloader
    from CommonFunctions.Player import PlayOnYT, video_downloader, clipboard_data, Search, song_downloader

recog=threading.Thread(target=task1)
models=threading.Thread(target=task3)
# chatgpt=threading.Thread(target=task2)

recog.start()
models.start()
# chatgpt.start()

from CommonFunctions.Speak_Adv import speak
from Models.Llama70b import Llama3_70b
from Models.Llama8b import Llama_8b
from Models.CommandR_Plus import Command_R_Plus
from Functions.MAlarm import *
from Functions.System_info import display_info
from CommonFunctions.Clap import MainClapExe

recog.join()
models.join()
# chatgpt.join()

def task4():
    global Dalle3, Show_Image, plt, listdir, output_path    
    T=t()
    from os import system, listdir
    import matplotlib.pyplot as plt
    import PIL
    from API_keys import Bing_key

    C = Bing_key
    output_path = r'Downloads\images'

    def Dalle3(prompt: str):
        output_dir = "Downloads\\images"
        system(f'python -m BingImageCreator --prompt "{prompt}" -U "{C}" --output-dir "{output_dir}"')
        speak(MaleVoice=MaleVoice,text="Images Are Ready SIR!")
        return None

    class Show_Image:
        def __init__(self, li: list) -> None:
            self.listd = li
            self.current_index = 0

        def open(self):
            try:
                img_path = f"{output_path}\\{self.listd[self.current_index]}"
                img = plt.imread(img_path)
                plt.imshow(img)
                plt.show(block=False)
            except IndexError:
                print("No more images to show.")
            except PIL.UnidentifiedImageError:
                print(f"Corrupted image: {img_path}. Skipping...")
                self.show_next()

        def close(self):
            plt.close()

        def show_next(self):
            try:
                self.close()
                self.current_index += 1
                if self.current_index < len(self.listd):
                    self.open()
                else:
                    print("No more images to show.")
            except IndexError:
                print("No more images to show.")

    print(f"==> Dalle3 Loaded!")
    print("Time Taken To Load Phase 2:",t()-T)

tf= threading.Thread(target=task4)
tf.start()

print("\n==> Necessary Imports are Done!")
print("Time Taken To Load Phase 1:",t()-L)
print("==> Jarvis is Ready To Action")


def load_cache(filename):
  """Loads the chatbot cache from a JSON file."""
  try:
    with open(filename, 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    # Create an empty cache if the file doesn't exist
    return {}

def save_cache(cache, filename):
  """Saves the chatbot cache to a JSON file."""
  try:
    with open(filename, 'w') as f:
      json.dump(cache, f, indent=2)  # Add indentation for readability
  except IOError:
    print("Error saving cache. Please check file permissions.")

def check_cache(cache, Query):
  """Checks if the user input is present in the cache."""
  return Query in cache

def update_cache(cache, Query, response):
  """Updates the cache with the user input and corresponding response, but only if the response is different."""
  if Query not in cache or cache[Query] != response:
    cache[Query] = response
  return cache

def chatbot_response(Query):
  """Main chatbot logic, with caching integration."""
  cache = load_cache('chatbot_cache.json')

  if check_cache(cache, Query):
    return cache[Query]  # Return cached response if available
  else:
    # Generate response using your chatbot's logic (e.g., NLP library)
    response = "IDK"
    cache = update_cache(cache, Query, response)
    cache = load_cache('chatbot_cache.json')  # Load the current cache
    cache.update(update_cache({}, Query, response))  # Update the cache
    save_cache(cache, 'chatbot_cache.json')  # Save the updated cache
    return response

def MainExecution():
    global MaleVoice
    while 1:
        print("\n==> Say Hello, or Say Start to wake him.")
        wake = speechrecognition(Translate=Hindi_support, Print=False)
        if "start" in wake or "hello" in wake:
            speak(MaleVoice=MaleVoice,text="Hello Sir Welcome!")
            while True:
                if Recognition:
                    cache = load_cache('chatbot_cache.json')
                    Query = speechrecognition(Translate=Hindi_support)
                    C=t()
                    if Query=="exit":
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                        speak(MaleVoice=MaleVoice,text="Okay Bye Sir!")
                        break
                    elif Query=="switch voice" or Query=="switch the voice" or Query=="switch to male voice" or Query=="switch to female voice":
                        if MaleVoice:
                            MaleVoice=False
                            speak(MaleVoice=MaleVoice,text="Switched To Female Voice!")
                        else:
                            MaleVoice=True
                            speak(MaleVoice=MaleVoice,text="Switched To Male Voice!")
                    elif Query=="shut down" or Query=="shutdown" or Query=="close":
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                        speak(MaleVoice=MaleVoice,text="Okay Shutting Down Sir!")
                        sys.exit()
                    elif Query=="jarvis go on hibernation" or Query =="jarvis turn on hibernation mode":
                        speak(MaleVoice=MaleVoice,text="Okay Going To Hibernate Sir.....")
                        print("==> Jarvis is on Hibernation Mode")
                        MainClapExe()
                        print("Sleep Time:",t()-C)
                        speak(MaleVoice=MaleVoice,text="OH Hello Sir I am Back, What Can i Do For You")
                    elif Query=="jarvis sleep" or Query =="jarvis go to bed" or Query =="sleep":
                        speak(MaleVoice=MaleVoice,text="Okay Going To Sleep Sir.....")
                        print("==> Jarvis is Now Sleeping....")
                        MainClapExe()
                        print("Sleep Time:",t()-C)
                        speak(MaleVoice=MaleVoice,text="OH That Was A Quite Good Nap, Hello Sir!")
                    elif Query.startswith("play"):
                        song_name = Query.removeprefix("play")
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                        speak(MaleVoice=MaleVoice,text=PlayOnYT(song_name))
                    elif Query.startswith("search") and Query.endswith("google") or Query.startswith("google"):
                        Query = Query.removeprefix("search")
                        Query = Query.removeprefix("for")
                        Query = Query.removesuffix("google")
                        Query = Query.removesuffix("on")
                        Query = Query.removeprefix("google")
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                        speak(MaleVoice=MaleVoice,text=Search(Query))
                    elif Query.startswith("jarvis su") or Query.startswith("jarvis shoe"):
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                        print(f"==> Jarvis AI: SUUUUUUUUUUUUUU....!")
                        playaudio(r'Resources\suu.mp3')
                    elif Query.startswith("generate") and "image" in Query or Query.startswith("create") and "image" in Query or Query.startswith("make") and "image" in Query or "next" in Query and "image" in Query or "show" in Query and "image" in Query or "dikhao" in Query or "open" in Query and "image" in Query or "yes" in Query and "image" in Query:
                        if Query.startswith("generate") or Query.startswith("create")or Query.startswith("make"):
                            Query = Query.removeprefix("generate")
                            Query = Query.removeprefix("create")
                            Query = Query.removeprefix("make")
                            Query = Query.removeprefix("image of")
                            Query = Query.removeprefix("an image of")
                            images_list = threading.Thread(target=Dalle3, args=(Query,))
                            images_list.start()
                            speak(MaleVoice=MaleVoice,text="Making the images Sir!")
                        elif "next" in Query or "show" in Query or "dikhao" in Query or "open" in Query or "yes" in Query:
                                show_image_instance = Show_Image(listdir(output_path)[-4:])
                                Query = Query
                                if 'next' in Query:
                                    show_image_instance.show_next()
                                    plt.pause(0.01)  
                                elif 'show' in Query:
                                    show_image_instance.open()
                                    plt.pause(0.01)
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")                          
                    # elif Query=="read this website" or Query=="scan this website" or Query=="summarize this website" or Query=="summarise this website":
                    #     if "summarise" in Query or "summarize" in Query:
                            # info = website_info()
                            # prompt = "summarize this website data: "+info
                            # response = ReaderGPT(prompt)
                            # time_taken = str(t()-C)[:4]
                    #         print(f"\nTime Taken: {time_taken}s")
                    #         speak(MaleVoice=MaleVoice,text=response)
                    #     else:
                    #         info = website_info()
                    #         prompt = "Read this website info: "+info
                    #         response = ReaderGPT(prompt)
                    #         time_taken = str(t()-C)[:4]
                    #         print(f"\nTime Taken: {time_taken}s")
                    #         speak(MaleVoice=MaleVoice,text=response)
                    # elif Query=="read my clipboard" or Query=="scan my clipboard" or Query=="read this" or Query=="read this data" or Query=="read data from my clipboard":
                    #     clipdata = "Read this data: "+clipboard_data()
                    #     response = ReaderGPT(clipdata)
                    #     time_taken = str(t()-C)[:4]
                    #     print(f"\nTime Taken: {time_taken}s")
                    #     speak(MaleVoice=MaleVoice,text=response)
                    elif Query.startswith("download this video") or Query.startswith("jarvis download this video"):
                        video_downloader()
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("download this song") or Query.startswith("jarvis download this song"):
                        song_downloader()
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("open new tab") or Query.startswith("close this tab"):
                        if "close" in Query:
                            pyautogui.hotkey('ctrl', 'w')
                        else:
                            pyautogui.hotkey('ctrl', 't')         
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    # elif Query.startswith("open") and "instagram" in Query or Query.startswith("open") and "amazon" in Query or Query.startswith("open") and "insta" in Query or Query.startswith("open") and "youtube" in Query or Query.startswith("open") and "whatsapp" in Query or Query.startswith("open") and "twitter" in Query or Query.startswith("open") and "brave" in Query or Query.startswith("open") and "browser" in Query or Query.startswith("open") and "collab" in Query:
                        if "insta" in Query or "insta" in Query:
                            webbrowser.open('https://www.instagram.com/')
                        elif "whatsapp" in Query:
                            webbrowser.open('https://web.whatsapp.com/')
                        elif "twitter" in Query:
                            webbrowser.open('https://www.twitter.com/')
                        elif "amazon" in Query:
                            webbrowser.open('https://www.amazon.in/')
                        elif "youtube" in Query:
                            webbrowser.open('https://www.youtube.com/')
                        elif "colab" in Query:
                            webbrowser.open('https://www.colab.research.google.com/')
                        elif "browser" or "brave" in Query:
                            try:
                                os.startfile('brave.exe')
                            except Exception:
                                os.startfule('chrome.exe')
                        speak(MaleVoice=MaleVoice,text="Here We Go SIR!")
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("close") and "brave" in Query or Query.startswith("close") and "browser" in Query:
                        if "close" and "browser" or "close" and "brave" in Query:
                            try:
                                os.system('taskkill /IM brave.exe /F')
                            except Exception:
                                os.system('taskkill /IM chrome.exe /F')
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("jarvis click here") or Query.startswith("click here") or Query =="click":
                        pyautogui.click(button='left')         
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("jarvis type") and "enter" in Query or Query.startswith("type here") and "enter" in Query or Query.startswith("type") and "enter" in Query or Query.startswith("write") and "enter" in Query:
                        Query = Query.removeprefix('jarivs type ')
                        Query = Query.removeprefix('type here ')
                        Query = Query.removeprefix('type ')
                        Query = Query.removeprefix('write ')
                        Query = Query.removesuffix('and press enter')
                        Query = Query.removesuffix('enter')
                        pyautogui.typewrite(Query)         
                        pyautogui.hotkey('enter')
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("jarvis type") or Query.startswith("type here") or Query.startswith("type") or Query.startswith("write"):
                        Query = Query.removeprefix('jarivs type ')
                        Query = Query.removeprefix('type here ')
                        Query = Query.removeprefix('type ')
                        Query = Query.removeprefix('write ')
                        pyautogui.typewrite(Query)         
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query == "enter" or Query.startswith('press enter') or Query.startswith('hit enter'):
                        pyautogui.hotkey('enter')
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif Query.startswith("pai") or Query.startswith("pi") or Query.startswith("sam"):
                        # response = Pi_AI(Query)
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                        speak(MaleVoice=MaleVoice,text=response)
                    elif Query.startswith("set alarm") or Query.startswith("alarm") or Query.startswith("make alarm"):
                        Llama3_70b(Query)
                        speak(MaleVoice=MaleVoice,text="Alarm is ready Sir!")
                    elif Query.startswith("stop alarm") or Query.startswith("cancel alarm") or Query.startswith("terminate alarm"):
                        stop_Alarm()
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    # elif Query.startswith("time") or Query.startswith("day") or Query.startswith("date") or Query.startswith("operating system") or Query.startswith("cpu") or Query.startswith("memory") or Query.startswith("battery") or Query.startswith("net") or Query.startswith("network") or Query.startswith("disk") or Query.startswith("processes") or Query.startswith("process") or Query.startswith("uptime") or Query.startswith("runtime") or Query.startswith("up time") or Query.startswith("run time") or Query.startswith("disc") or Query.startswith("ram"):
                        if "day" in Query:
                            speak(MaleVoice=MaleVoice,text=display_info("day"))                        
                        elif "date" in Query:       
                            speak(MaleVoice=MaleVoice,text=display_info("date"))                 
                        elif "operating" in Query:         
                            speak(MaleVoice=MaleVoice,text=display_info("os"))
                        elif "cpu" in Query:            
                            speak(MaleVoice=MaleVoice,text=display_info("cpu"))            
                        elif "memory" in Query or "ram" in Query:    
                            speak(MaleVoice=MaleVoice,text=display_info("memory"))                    
                        elif "battery" in Query:     
                            speak(MaleVoice=MaleVoice,text=display_info("battery"))                   
                        elif "net" in Query:       
                            speak(MaleVoice=MaleVoice,text=display_info("network"))                  
                        elif "dis" in Query:          
                            speak(MaleVoice=MaleVoice,text=display_info("disk"))                   
                        elif "process" in Query:  
                            speak(MaleVoice=MaleVoice,text=display_info("processes"))                       
                        elif "up" in Query or "run" in Query:
                            speak(MaleVoice=MaleVoice,text=display_info("uptime"))
                        elif Query.startswith("time"):                        
                            speak(MaleVoice=MaleVoice,text=display_info("time"))
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    # elif Query.endswith("time") or Query.endswith("day") or Query.endswith("date") or Query.endswith("operating system") or Query.endswith("cpu") or Query.endswith("memory") or Query.endswith("battery") or Query.endswith("net") or Query.endswith("network") or Query.endswith("disk") or Query.endswith("processes") or Query.endswith("process") or Query.endswith("uptime") or Query.endswith("runtime") or Query.endswith("up time") or Query.endswith("run time") or Query.endswith("disc") or Query.endswith("ram"):
                        if "day" in Query:
                            speak(MaleVoice=MaleVoice,text=display_info("day"))                        
                        elif "date" in Query:       
                            speak(MaleVoice=MaleVoice,text=display_info("date"))                 
                        elif "operating" in Query:         
                            speak(MaleVoice=MaleVoice,text=display_info("os"))
                        elif "cpu" in Query:            
                            speak(MaleVoice=MaleVoice,text=display_info("cpu"))            
                        elif "memory" in Query or "ram" in Query:    
                            speak(MaleVoice=MaleVoice,text=display_info("memory"))                    
                        elif "battery" in Query:     
                            speak(MaleVoice=MaleVoice,text=display_info("battery"))                   
                        elif "net" in Query:       
                            speak(MaleVoice=MaleVoice,text=display_info("network"))                  
                        elif "dis" in Query:          
                            speak(MaleVoice=MaleVoice,text=display_info("disk"))                   
                        elif "process" in Query:  
                            speak(MaleVoice=MaleVoice,text=display_info("processes"))                       
                        elif "up" in Query or "run" in Query:
                            speak(MaleVoice=MaleVoice,text=display_info("uptime"))
                        elif Query.endswith("time"):                        
                            speak(MaleVoice=MaleVoice,text=display_info("time"))
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")
                    elif check_cache(cache, Query):
                        response=cache[Query]
                        assistant_response = response
                        code_start = assistant_response.find("```python")
                        code_end = assistant_response.find("```", code_start + 1)
                        time_taken = str(t()-C)[:4]
                        print(f"\nTime Taken: {time_taken}s")

                        if code_start != -1 and code_end != -1:
                            python_code = assistant_response[code_start + 9:code_end].strip()
                            print("\n"+assistant_response+"\n==> Executing the code!")
                            try:
                                exec(python_code)
                            except Exception as e:
                                print("Error during code execution:", e)
                            speak(MaleVoice=MaleVoice,text="Task Completed Sir!")
                        else:
                            speak(MaleVoice=MaleVoice,text=response)
                    else:
                        if LLAMA_Slow:
                            response=Llama3_70b(Query, MaleVoice=MaleVoice)
                        elif LLAMA_Slow==False:
                            response= Llama_8b(Query, MaleVoice=MaleVoice)
                        elif Cohere_AI:
                            response= Command_R_Plus(Query,defaultsearch=True, MaleVoice=MaleVoice)
                        if "python" in response:
                            cache = update_cache(cache, Query, response)
                            cache = load_cache('chatbot_cache.json')  # Load the current cache
                            cache.update(update_cache({}, Query, response))  # Update the cache
                            save_cache(cache, 'chatbot_cache.json')
        elif "sleep" in wake:
            MainClapExe()
        elif "bye" in wake or "exit" in wake or "close" in wake:
            sys.exit()  

if __name__=="__main__":
    MainExecution()
    sys.exit()
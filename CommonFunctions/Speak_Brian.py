import requests as rq
from playaudio import playaudio
import colorama
import threading
import pygame
colorama.init(autoreset=True)
import sys
import os

requests=rq.Session()
current_dir = os.getcwd()
sys.path.append(current_dir)
from CommonFunctions.Clap import MainClapExe

api_url = "https://api.streamelements.com/kappa/v2/speech"
IS_HOT_WRD = False
HOT_WORD_DECT_IS_ON = False


def HOT_WORD_DECT():
    global IS_HOT_WRD, HOT_WORD_DECT_IS_ON
    while True:
        if HOT_WORD_DECT_IS_ON:
            A = MainClapExe(Print=False)
            if MainClapExe:
                if HOT_WORD_DECT_IS_ON:
                    IS_HOT_WRD = True
                    return
            else:
                pass
        else:
            return

def file_saver(text, output_file=r"temp/data.mp3"):
    params = {
        "voice": "Brian",
        "text": text
    }
    response = requests.get(api_url, params=params)
    with open(output_file, "wb") as f:
        f.write(response.content)

def speak(text, PRINT=True):
    s = threading.Thread(target=file_saver, args=(text,))
    s.start()
    global IS_HOT_WRD, HOT_WORD_DECT_IS_ON
    HOT_WORD_DECT_IS_ON = True
    threading.Thread(target=HOT_WORD_DECT).start()
    if PRINT:
        print(colorama.Fore.YELLOW + "==> Jarvis AI: " + text + "\n")
    playaudio('Resources\\notification2.mp3')
    s.join()
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(r"temp/data.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if IS_HOT_WRD:
                IS_HOT_WRD = False
                pygame.mixer.music.stop()
                break
    except Exception as e:
        print(e)
    finally:
        HOT_WORD_DECT_IS_ON = False

print("==> Speech Loaded!")

if __name__ == "__main__":
    pygame.mixer.init()
    while True:
        speak("Hello sir this is Jarvis in Brian's voice hi this is jarvis")
        speak("hi this is jarvis")
        speak("sir welcome")
        speak("welcome sir")
    pygame.mixer.quit()
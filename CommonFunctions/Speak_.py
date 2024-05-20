import pyttsx3
from playaudio import playaudio
import colorama
import threading
import simpleaudio as sa
colorama.init(autoreset=True)
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from CommonFunctions.Clap import MainClapExe 

IS_HOT_WRD = False
HOT_WORD_DECT_IS_ON = False

id='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\Brian RSI Harpo 22kHz'
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[3].id)
engine.setProperty('rate', 200)


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

def file_saver(text):
    engine.save_to_file(text=text, filename=r"temp//data.wav")
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()

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
        wave_obj = sa.WaveObject.from_wave_file(r"temp//data.wav")
        play_obj = wave_obj.play()
        while play_obj.is_playing():
            if IS_HOT_WRD:
                IS_HOT_WRD = False
                play_obj.stop()
                break
    except Exception as e:
        print(e)
    finally:
        HOT_WORD_DECT_IS_ON = False

print("==> Speech Loaded!")

if __name__=="__main__":
    while True:
        speak("Hello sir this is Jarvis in Brian's voice hi this is jarvis Hello sir this is Jarvis in Brian's voice hi this is jarvis Hello sir this is Jarvis in Brian's voice hi this is jarvis Hello sir this is Jarvis in Brian's voice hi this is jarvis Hello sir this is Jarvis in Brian's voice hi this is jarvis Hello sir this is Jarvis in Brian's voice hi this is jarvis Hello sir this is Jarvis in Brian's voice hi this is jarvis ")
        speak("hi this is jarvis")
        speak("sir welcome")
        speak("welcome sir")
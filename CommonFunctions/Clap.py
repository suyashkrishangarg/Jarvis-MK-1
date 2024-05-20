import sounddevice as sd 
import numpy as np

threshold = 18
Clap = False

def detect_clap(indata,frames,time,status):
    global Clap
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm>threshold:
        Clap = True

def Listen_for_claps():
    with sd.InputStream(callback=detect_clap):
        return sd.sleep(1000)
    
print("==> Clap Detection Loaded!")

def MainClapExe(Print=True):
    global Clap
    if Print:
        print("\n==> You Can Clap Anytime To Wake Up The Jarvis!")
    while True:
        if Print:
            Listen_for_claps()
            if Clap == True:
                print("==> Clapped!")
                Clap = False
                break
            else:
                pass
        else:
            Listen_for_claps()
            if Clap == True:
                Clap = False
                break
            else:
                pass
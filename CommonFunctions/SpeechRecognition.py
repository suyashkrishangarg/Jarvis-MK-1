import speech_recognition as sr 
from playaudio import playaudio

print("==> Speech Recognition Loaded!")

def speechrecognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        playaudio('Resources\\notification1.mp3')
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,0) #r.listen(source,0,8) -- replace "8" if any error
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print(f"\n==> You Said: {query.upper()}")
        return query.lower()
    
    except:
        return ""
    
if __name__=="__main__":
    while True:
        speechrecognition()

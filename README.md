# 🤖 Jarvis-MK-1 — Voice-Controlled Desktop AI Assistant

The original **Jarvis-MK-1**: a Windows voice assistant ("Jarvis") with a
**wake-word loop** ("hello"/"start" to wake, "sleep"/"bye" to rest), **Chrome
Web-Speech recognition**, **multi-engine TTS** (edge-tts, pyttsx3, AI voices),
**12 swappable LLM backends**, **DALL-E image generation** (BingImageCreator),
and **PC automation** (apps, media, alarms, system info, `exec()` of
LLM-written Python for open-ended tasks).

> ⚠️ **Windows-only** — absolute paths, `.bat` launchers, `pyautogui` automation
> and `playaudio`/`simpleaudio` playback assume Windows. Successor with a PyQt5
> GUI + offline neural TTS: **[Jarvis-Mark-1](https://github.com/suyashkrishangarg/Jarvis-Mark-1)**.

---

## ✨ Features

- 🎙️ **Wake-word voice loop** (`Jarvis.py → MainExecution()`) — Chrome Web-Speech
  STT via Selenium (`SpeechRecog.py`); Hindi-translation mode flag; clap-listening
  sleep mode (`Clap.py`); threaded background imports for fast startup
- 🗣️ **4 TTS engines** (`CommonFunctions/`) — `Speak_Adv.py` (edge-tts, default),
  `Speak_.py` / `Speak3.py` (pyttsx3 male/female), `Speak_Brian.py` + `ai_voice.py`
  (AI voice), plus `Player.py` (YouTube play + video/song download, clipboard read)
- 🧠 **12 LLM backends** (`Models/`) — Llama-70B / Llama-8B (default routing),
  Command-R Plus, ChatGPT (`g4f`), Cohere, DeepInfra, Mistral-7B, Phind, Pi, liaobots…
  with a **`chatbot_cache.json` response cache** to skip repeat inference
- 🎨 **Voice-driven image generation** — `generate/create/make image …` triggers
  BingImageCreator DALL-E in a thread; `Show_Image` viewer (`next`/`show image`)
  browses the last 4 renders with matplotlib
- 🛠️ **PC automation by voice** — open/close tabs & software, YouTube playback,
  alarms (`MAlarm.py`), system stats (CPU/RAM/battery/disk/network/uptime),
  Google search, file reading, Android-ADB setup, phone-call helper
- ⚡ **Self-executing agent mode** — cached LLM answers containing
  ` ```python ` blocks are **`exec()`-uted directly**, so Jarvis can perform
  arbitrary multi-step computer tasks unsupervised
- 🌱 **`temp.py`** — standalone Groq `llama3-70b` + `google_search` function-calling demo
- 📦 **Vendored `pywinassistant/`** — third-party Windows UI-automation library
  (window analysis, OCR, mouse/keyboard, voice) bundled in-tree

## 🏗️ Architecture

```
"hello/start" ──► wake ──► voice command ──► keyword router ──► tools / alarms / images
   (Chrome Web-Speech STT)            │ else                    (threads)
                                      ▼
                          Llama-70B / 8B / Command-R+ ──► cache ──► speak (edge-tts)
                                      │
                          ```python in answer? ──► exec() ──► "Task Completed Sir!"
```


---

## 🚀 Getting Started

### Prerequisites

- **Windows** 10/11, Python 3.10/3.11 (3.12 has no `playaudio`/`simpleaudio` wheels),
  Chrome browser, microphone + speakers
- API keys for the backends you use (Groq/Llama, Cohere, Gemini, Google Custom Search…)

### Installation

`requirements.txt` pins package **names without versions** and includes some
dead/heavy ones (`g4f`, `webscout`, `transformers`, `accelerate`, `easyocr`), so
a blind install often breaks. Recommended minimal path:

```bat
Setup_Jarvis.bat
```
i.e. `pip install -r requirements.txt --upgrade` — then fix failures package by
package, or start lean:

```bat
pip install SpeechRecognition selenium webdriver-manager edge-tts pyttsx3 ^
  pygame groq google-generativeai pywhatkit pyautogui pytube keyboard ^
  pyperclip matplotlib pillow requests psutil mtranslate cohere html2text
```

### Configuration

Fill in **`API_keys.py`** (ships with blank values — good):

```python
groq = 'gsk_...'            # Llama backends (Models/Llama70b.py, Llama8b.py)
Bing_key = '...'            # DALL-E image generation (Bing cookie + '_U' suffix)
Gemini_api_key = '...'      # search / generative features
cohere_api = '...'          # Command-R Plus backend
GoogleCustomSearch = '...'  # + cx = custom search engine id
AI_Name = 'Jarvis'          # persona: name, gender, country, your profile…
```

Tune behaviour flags at the top of **`Jarvis.py`**:

```python
Recognition = True    # voice input on/off
LLAMA_Slow = True     # True → Llama-70B, False → Llama-8B (faster)
Cohere_AI = True      # Command-R Plus branch
Hindi_support = False # translate queries
```

### Run

```bat
Run_Jarvis.bat
```
i.e. `python Jarvis.py` → say **"hello"** or **"start"**, then speak commands.
Say **"sleep"** to rest him, **"bye/exit/close"** to quit.

## 📖 Usage

- `open/close <app or site>`, `play <song>`, `set alarm …`, `system info`,
  `generate image of …` → `next` / `show image` to browse renders
- Anything else → LLM chat, spoken back; answers with ` ```python ` blocks are
  **executed on your PC automatically** (see security note below)

## 🛠️ Tech Stack

- **STT:** Chrome Web-Speech via Selenium, SpeechRecognition (+ Hindi via mtranslate)
- **TTS:** edge-tts, pyttsx3, AI-voice modules
- **LLM:** Llama-70B/8B (Groq), Command-R Plus (Cohere), g4f, Gemini, DeepInfra…
- **Automation:** pywhatkit, pyautogui, pytube, matplotlib viewer, ADB tools

## ⚠️ Notes

- 🔒 **`temp.py` line 32 embeds a live Groq API key (`gsk_…`) — revoke it at
  console.groq.com and delete that line**; it also runs a demo query on import-run.
- 🔒 The `exec(python_code)` agent mode runs untrusted LLM output as code —
  keep this offline/personal, never expose it as a service.
- 🧹 Committed junk worth cleaning: `__pycache__/`, `temp/*.mp3`,
  `The Box.wav` (~35 MB), `chatbot_cache.json`, and consider un-vendoring
  `pywinassistant/` (or pin it as a dependency) to slim the ~39 MB repo.
- `Run_Jarvis.bat` has a hardcoded path (`C:\Users\ASUS\…`) — edit or just run
  `python Jarvis.py`.

## 📄 License

MIT — free to use and modify.

### Project structure

```
├── Jarvis.py                  # entry point: wake loop, keyword router, chat, exec-agent
├── API_keys.py                # 🔑 keys + persona (all values currently blank — fill in)
├── requirements.txt           # 39 pinned deps (no versions — see setup note)
├── Run_Jarvis.bat / Setup_Jarvis.bat   # Windows launch / setup shortcuts
├── chatbot_cache.json         # LLM response cache · temp.py (Groq tool-use demo)
├── Models/                    # 12 backends: Llama70b/8b, CommandR_Plus, ChatGpt(g4f),
│                              #   Cohere, DeepInfra, Mistral7B, Phind, Pi, liaobots, Dalle3
├── CommonFunctions/           # Speak_* (4 TTS), SpeechRecog (STT), Player, Clap, WebsiteInfo
├── Functions/                 # MAlarm, System_info, GoogleSearch, Reader, call, ADB setup
├── Resources/                 # notification sounds + images
├── pywinassistant/            # vendored 3rd-party Windows automation lib (has own README)
└── temp/  __pycache__/        # runtime leftovers (see notes)
```

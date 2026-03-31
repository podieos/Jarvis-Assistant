# Jarvis Assistant

A collection of AI voice assistant projects built with OpenAI and Google Gemini APIs. Each project is self-contained and can be run independently.

---

## Projects

### OpenAI

| Project | Description |
|---|---|
| [`GPT-Jarvis`](/OpenAI/GPT-Jarvis/) | Full voice assistant — wake word → speech-to-text → LLM (with web search + vision) → text-to-speech |
| [`GPT-Jarvis Realtime`](/OpenAI/GPT-Jarvis%20Realtime/) | Real-time voice assistant via OpenAI's WebSocket Realtime API |
| [`GPT-STT`](/OpenAI/GPT-STT/) | Simple speech-to-text using OpenAI Whisper |
| [`GPT-Text`](/OpenAI/GPT-Text/) | Minimal text-based chat loop with GPT-4o-mini |

### Google

| Project | Description |
|---|---|
| [`Google`](/Google/) | Live voice assistant using Gemini 2.5 Flash with native audio and wake word detection |

---

## Requirements

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys) and/or a [Google Gemini API key](https://aistudio.google.com/app/apikey)
- [SoX](https://sourceforge.net/projects/sox/) — required by `GPT-Jarvis` for audio recording (`rec` and `sox` commands in PATH)

Install Python dependencies for the project you want to run:

```bash
# GPT-Jarvis
pip install openai sounddevice numpy playsound openwakeword

# GPT-Jarvis Realtime
pip install openai sounddevice numpy websocket-client certifi openwakeword

# GPT-STT
pip install openai

# GPT-Text
pip install openai

# Google
pip install google-genai numpy pyaudio openwakeword
```

---

## Setup & Usage

**1. Clone the repository**
```bash
git clone https://github.com/podieos/Jarvis-Assistant.git
cd Jarvis-Assistant
```

**2. Add your API key**

Open the script (or `config.json` for GPT-Jarvis) and replace `"API_KEY"` with your actual key:

```json
# config.json (GPT-Jarvis)
{
  "API_KEY": "sk-..."
}
```

```python
# All other scripts
CLIENT = OpenAI(api_key="sk-...")   # OpenAI projects
CLIENT = genai.Client(api_key="...") # Google project
```

**3. Run**
```bash
python main.py        # most projects
python STT.py         # GPT-STT
```

> **Wake word:** Say **"Hey Jarvis"** to activate any of the voice assistant projects.

---

## Project Details

### GPT-Jarvis
The most complete project. Uses a pipeline of:
- **Wake word** detection via `openwakeword`
- **Recording** via SoX (auto-stops on silence)
- **STT** via OpenAI Whisper
- **LLM** via GPT-4o-mini (streaming, with web search tool)
- **TTS** via OpenAI TTS
- **Vision** — say a trigger phrase and it captures a photo and describes it (camera command must be enabled in `take_photo()`)

All settings are configured in `config.json`. Uncomment the OS-specific commands in `record()` and `tts()` for your platform (macOS / Linux / Windows).

### GPT-Jarvis Realtime
Uses OpenAI's WebSocket Realtime API for low-latency, continuous conversation. Wake word activates a live session that stays open until you say **"bye"**.

### GPT-STT
Minimal script. Set `FILE` to your audio file path and run — prints the transcription.

### GPT-Text
A simple REPL. Type a question, get a response. Good for quick testing.

### Google (Gemini)
Uses Gemini 2.5 Flash native audio preview. Set `API_KEY`, `PROMPT`, and `VOICE` at the top of `main.py`. Wake word activates a live audio session.

---

## License

[MIT](LICENSE) © podieos

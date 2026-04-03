# Jarvis Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A collection of AI voice assistant projects built with OpenAI and Google Gemini APIs. Each project is self-contained and can be run independently.

---

## Projects

### OpenAI

| Project | Description |
|---|---|
| [`GPT-Jarvis`](/OpenAI/GPT-Jarvis/) | Full voice assistant — wake word → STT → LLM (web search + vision) → TTS |
| [`GPT-Jarvis Realtime`](/OpenAI/GPT-Jarvis%20Realtime/) | Real-time voice assistant via OpenAI's WebSocket Realtime API |
| [`GPT-STT`](/OpenAI/GPT-STT/) | Simple speech-to-text using OpenAI Whisper |
| [`GPT-Text`](/OpenAI/GPT-Text/) | Minimal text-based chat loop with GPT-4o-mini |

### Google

| Project | Description |
|---|---|
| [`Google`](/Google/) | Live voice assistant using Gemini 2.5 Flash with native audio and wake word detection |

---

## Repository Structure

```
Jarvis-Assistant/
├── OpenAI/
│   ├── GPT-Jarvis/
│   │   ├── main.py
│   │   ├── config.json
│   │   ├── history.json
│   │   └── generate_yes.py
│   ├── GPT-Jarvis Realtime/
│   │   └── main.py
│   ├── GPT-STT/
│   │   └── STT.py
│   └── GPT-Text/
│       └── main.py
└── Google/
    └── main.py
```

---

## Requirements

- Python 3.10+
- Microphone (all voice assistant projects)
- Camera (optional — GPT-Jarvis vision feature only)
- An [OpenAI API key](https://platform.openai.com/api-keys) and/or a [Google Gemini API key](https://aistudio.google.com/app/apikey)
- [SoX](https://sourceforge.net/projects/sox/) — required by `GPT-Jarvis` for audio recording (`rec` and `sox` commands in PATH)

**Platform support:** macOS, Linux, Windows (platform-specific playback lines must be uncommented — see [Project Details](#project-details))

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

> ⚠️ Never commit your API key to version control. Add `config.json` and any file containing your key to `.gitignore`.

For `GPT-Jarvis`, open `config.json` and replace `"API_KEY"` with your actual key:

```json
{
  "API_KEY": "sk-..."
}
```

For all other scripts, replace the placeholder at the top of `main.py` (or `STT.py`):

```python
CLIENT = OpenAI(api_key="sk-...")    # OpenAI projects
CLIENT = genai.Client(api_key="...") # Google project
```

**3. Run**
```bash
python main.py   # most projects
python STT.py    # GPT-STT
```

> **Wake word:** Say **"Hey Jarvis"** to activate any of the voice assistant projects.

---

## Project Details

### GPT-Jarvis

The most complete project. Pipeline:

- **Wake word** — `openwakeword` (hey_jarvis, tflite)
- **Recording** — SoX (auto-stops on silence)
- **STT** — OpenAI Whisper (`gpt-4o-mini-transcribe`)
- **LLM** — GPT-4o-mini (streaming, with web search tool)
- **TTS** — OpenAI TTS (`gpt-4o-mini-tts`)
- **Vision** — say a trigger phrase → captures photo → GPT-4o-mini describes it

Before running, uncomment the OS-specific lines in `record()` and `tts()` for your platform.

> **First run:** Execute `generate_yes.py` once to generate `yes.mp3` — the acknowledgment sound that plays on wake word detection.

#### `config.json` Reference

| Key | Description |
|---|---|
| `API_KEY` | Your OpenAI API key |
| `MAX_HISTORY` | Number of past conversation turns to remember |
| `SR` | Microphone sample rate (Hz) |
| `FRAME_SAMPLES` | Audio frame size for wake word processing |
| `THRESHOLD` | Wake word detection sensitivity (0.0–1.0) |
| `COOLDOWN_S` | Seconds to wait before re-triggering wake word |
| `WAKE_HITS_REQUIRED` | Consecutive detections required to confirm wake word |
| `WAKE_LOG_EVERY_N_FRAMES` | Log wake word scores every N frames (for calibration) |
| `WAKE_LOG_NEAR_THRESHOLD` | Also log scores above this value (set to `0.0` to disable) |
| `VISION_MODEL` | OpenAI model used for image descriptions |
| `VISION_INSTRUCTION` | System prompt for the vision model |
| `VISION_MAX_TOKENS` | Max tokens for vision responses |
| `STT_MODEL` | Whisper model for speech-to-text |
| `STT_LANGUAGE` | Language code for transcription (e.g. `"en"`) |
| `TTS_MODEL` | OpenAI model for text-to-speech |
| `TTS_VOICE` | Voice name for TTS output |
| `TTS_INSTRUCTIONS` | Optional style instructions for the TTS voice |
| `TTS_MIN_CHARS` | Minimum characters required to trigger TTS (0 = no minimum) |
| `TTS_MAX_CHARS` | Maximum characters passed to TTS (0 = no limit) |
| `LLM_MODEL` | OpenAI model for the main chat responses |
| `LLM_MAX_TOKENS` | Max tokens for LLM responses |
| `LLM_INSTRUCTIONS` | System prompt / personality for the assistant |

---

### GPT-Jarvis Realtime

Uses OpenAI's WebSocket Realtime API for low-latency, continuous conversation. Wake word activates a live session that stays open until you say **"bye"**.

Before running, set `WAKE_MODEL_PATH` at the top of `main.py` to the path of your `hey_jarvis` ONNX model file:

```python
WAKE_MODEL_PATH = "/path/to/hey_jarvis_v0.1.onnx"
```

Download it from the [openWakeWord releases](https://github.com/dscripka/openWakeWord/releases).

You can also configure the model, voice, and instructions at the top of `main.py`:

```python
MODEL        = "gpt-realtime-mini"
VOICE        = "echo"
INSTRUCTIONS = "You are JARVIS..."
```

---

### GPT-STT

Minimal transcription script. Set `FILE` to your audio file path and run — prints the transcription to stdout.

```python
FILE = "audio.mp3"
```

---

### GPT-Text

A simple REPL. Type a question, get a response. Good for quick testing without audio.

---

### Google (Gemini)

Uses Gemini 2.5 Flash native audio (`gemini-2.5-flash-native-audio-preview`). Wake word activates a live audio session that streams audio to and from Gemini in real time. The session ends automatically when the model includes `[DONE]` in its transcript.

Configure at the top of `main.py`:

```python
API_KEY             = "your-gemini-key"
PROMPT              = "You are JARVIS..."   # system instruction
VOICE               = "Charon"              # prebuilt Gemini voice
WAKE_WORD_THRESHOLD = 0.5                   # 0.0–1.0
```

Available voices: `Aoede`, `Charon`, `Fenrir`, `Kore`, `Puck` (and others — see [Gemini docs](https://ai.google.dev/gemini-api/docs/live)).

Architecture: `wake_word()` → `live.connect()` → concurrent `send_audio` + `receive_responses` tasks → back to wake word on `[DONE]` or session close.

---

## Troubleshooting

**Wake word isn't triggering**
Lower `THRESHOLD` / `WAKE_WORD_THRESHOLD` (try `0.3`). Score logs are printed to help calibrate.

**`rec` or `sox` command not found**
SoX is not installed or not in PATH. Install with `brew install sox` (macOS), `apt install sox` (Linux), or download from [sourceforge.net/projects/sox](https://sourceforge.net/projects/sox/) (Windows).

**No audio output / recording fails**
The OS-specific playback and record commands in `tts()` and `record()` are commented out by default. Uncomment the line matching your platform.

**Camera capture raises an error**
Camera support is disabled by default. Uncomment the correct OS command inside `take_photo()`.

**`yes.mp3` not found (GPT-Jarvis)**
Run `generate_yes.py` once to create it before starting the main script.

**PyAudio install fails**
On macOS: `brew install portaudio && pip install pyaudio`. On Linux: `sudo apt install portaudio19-dev && pip install pyaudio`.

---

## License

[MIT](LICENSE) © podieos

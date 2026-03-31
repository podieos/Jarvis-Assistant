# Jarvis Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

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
{
  "API_KEY": "sk-..."
}
```
*(all other keys keep their defaults — see the [config reference](#configjson-reference) below)*

```python
# All other scripts
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
The most complete project. Uses a pipeline of:
- **Wake word** detection via `openwakeword`
- **Recording** via SoX (auto-stops on silence)
- **STT** via OpenAI Whisper
- **LLM** via GPT-4o-mini (streaming, with web search tool)
- **TTS** via OpenAI TTS
- **Vision** — say a trigger phrase and it captures a photo and describes it (camera command must be enabled in `take_photo()`)

All settings are in `config.json`. Before running, uncomment the OS-specific lines in `record()` and `tts()` for your platform.

> **First run:** Execute `generate_yes.py` once to generate the `yes.mp3` acknowledgment sound that plays on wake word detection.

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

### GPT-Jarvis Realtime
Uses OpenAI's WebSocket Realtime API for low-latency, continuous conversation. Wake word activates a live session that stays open until you say **"bye"**.

Before running, set `WAKE_MODEL_PATH` at the top of `main.py` to the path of your `hey_jarvis` ONNX model file. You can download it from the [openWakeWord releases](https://github.com/dscripka/openWakeWord/releases) or generate one via `openwakeword`'s utilities.

### GPT-STT
Minimal script. Set `FILE` to your audio file path and run — prints the transcription.

### GPT-Text
A simple REPL. Type a question, get a response. Good for quick testing.

### Google (Gemini)
Uses Gemini 2.5 Flash native audio preview. Set `API_KEY`, `PROMPT`, and `VOICE` at the top of `main.py`. Wake word activates a live audio session.

---

## Troubleshooting

**Wake word isn't triggering**
Lower the `THRESHOLD` in `config.json` (try `0.3`). Print scores are logged to help calibrate.

**`rec` or `sox` command not found**
SoX is not installed or not in your PATH. Install it with `brew install sox` (macOS), `apt install sox` (Linux), or download from the [SoX website](https://sourceforge.net/projects/sox/) (Windows).

**No audio output from TTS or recording fails**
The OS-specific playback/record commands in `tts()` and `record()` are commented out by default. Uncomment the line matching your OS.

**Camera capture raises an error**
Camera support is disabled by default. Uncomment the correct OS command inside `take_photo()` in `main.py`.

**`yes.mp3` not found (GPT-Jarvis)**
Run `generate_yes.py` once to create it before starting the main script.

---

## License

[MIT](LICENSE) © podieos

import asyncio
import numpy as np
import pyaudio
from google import genai
from google.genai import types
from openwakeword.model import Model

CLIENT = genai.Client(api_key="API_KEY")
MODEL  = "gemini-2.5-flash-native-audio-preview-12-2025"
PROMPT = ""
VOICE  = "Charon"
WAKE_WORD_MODEL = Model(wakeword_models=["hey_jarvis"], inference_framework="tflite")
WAKE_WORD_THRESHOLD = 0.5

CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    output_audio_transcription=types.AudioTranscriptionConfig(),
    system_instruction=PROMPT,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE)
        )
    ),
)

async def wake_word():
    WAKE_WORD_MODEL.reset()
    while True:
        chunk = await asyncio.to_thread(MICROPHONE.read, 1280, exception_on_overflow=False)
        audio_data = np.frombuffer(chunk, dtype=np.int16)
        predictions = WAKE_WORD_MODEL.predict(audio_data)
        for score in predictions.values():
            if score >= WAKE_WORD_THRESHOLD:
                print("Wake word")
                return

async def send_audio(session, stop_event: asyncio.Event):
    while not stop_event.is_set():
        chunk = await asyncio.to_thread(MICROPHONE.read, 1024, exception_on_overflow=False)
        await session.send_realtime_input(
            audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
        )

async def receive_responses(session, stop_event: asyncio.Event):
    transcript = []
    while True:
        async for response in session.receive():
            content = response.server_content
            if not content:
                continue

            if content.output_transcription:
                text = content.output_transcription.text
                transcript.append(text)
                print(text, end="", flush=True)

            if content.model_turn:
                for part in content.model_turn.parts:
                    if part.inline_data:
                        await asyncio.to_thread(SPEAKER.write, part.inline_data.data)

            if content.turn_complete:
                print()
                if "[DONE]" in "".join(transcript):
                    print("Stop")
                    stop_event.set()
                    return
                transcript = []
                break

async def main():
    global MICROPHONE, SPEAKER
    audio = pyaudio.PyAudio()
    MICROPHONE = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1280)
    SPEAKER    = audio.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    try:
        while True:
            print("Start")
            await wake_word()
            async with CLIENT.aio.live.connect(model=MODEL, config=CONFIG) as session:
                print("Connected")
                stop_event = asyncio.Event()
                await asyncio.gather(
                    send_audio(session, stop_event),
                    receive_responses(session, stop_event),
                )
    finally:
        audio.terminate()

asyncio.run(main())

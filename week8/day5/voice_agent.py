import os
import logging
import tempfile

import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from openai import OpenAI
import pygame

load_dotenv()

# -----------------------
# Logging
# -----------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------
# OpenAI Client
# -----------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------
# Record Audio
# -----------------------

def record_audio(filename="recording.wav", duration=10):
    sample_rate = 44100

    logging.info("Recording started")

    print("🎤 Speak now...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )

    sd.wait()

    write(filename, sample_rate, audio)

    print("✅ Recording complete")

    logging.info("Recording completed")


# -----------------------
# Whisper
# -----------------------

def transcribe_audio(filename="recording.wav"):
    try:
        with open(filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )

        logging.info(f"Transcription: {transcript.text}")

        return transcript.text

    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        raise


# -----------------------
# Agent
# -----------------------

def run_agent(user_text):

    try:
        # Fake tool usage example
        if "weather" in user_text.lower():
            logging.info("Weather tool used")
            return "The weather in Chennai is sunny."

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

        answer = response.output_text

        logging.info("Agent response generated")

        return answer

    except Exception as e:
        logging.error(f"Agent failed: {e}")
        raise


# -----------------------
# Text To Speech
# -----------------------

def speak(text):

    try:
        speech_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        speech_path = speech_file.name
        speech_file.close()

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as response:
            response.stream_to_file(speech_path)

        pygame.mixer.init()
        pygame.mixer.music.load(speech_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pass

        logging.info("Audio response played")

    except Exception as e:
        logging.error(f"TTS failed: {e}")


# -----------------------
# Main
# -----------------------

try:

    record_audio()

    text = transcribe_audio()

    print(f"\nYou: {text}")

    answer = run_agent(text)

    print(f"\nAgent: {answer}\n")

    speak(answer)

except Exception as e:

    logging.error(
        f"Application failed: {e}",
        exc_info=True
    )

    print(f"Error: {e}")
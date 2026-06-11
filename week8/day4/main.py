from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

for filename in os.listdir("audio"):
    filepath = f"audio/{filename}"

    with open(filepath, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio
        )

    print(f"\n{filename}")
    print(transcript.text)
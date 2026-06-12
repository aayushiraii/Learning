from fastapi import FastAPI, UploadFile, File
from openai import OpenAI
from dotenv import load_dotenv

import os
import logging
import tempfile

# -----------------------------
# Logging Setup
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler()
    ]
)

# -----------------------------
# Environment Variables
# -----------------------------

load_dotenv()

# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI()

# -----------------------------
# OpenAI Client
# -----------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# Voice Agent Endpoint
# -----------------------------

@app.post("/voice-agent")
async def voice_agent(audio: UploadFile = File(...)):
    temp_path = None

    try:
        logging.info("Voice request received")

        # Save uploaded audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            temp.write(await audio.read())
            temp_path = temp.name

        logging.info(f"Audio saved at {temp_path}")

        # Whisper Transcription
        with open(temp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )

        user_text = transcription.text

        logging.info(f"Transcription: {user_text}")

        # AI Response
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

        answer = response.output_text

        logging.info(f"Agent Response: {answer}")

        return {
            "status": "success",
            "transcription": user_text,
            "response": answer
        }

    except Exception as e:
        logging.error(
            f"Error occurred: {str(e)}",
            exc_info=True
        )

        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        # Cleanup temporary file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            logging.info("Temporary audio file deleted")
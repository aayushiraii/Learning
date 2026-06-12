from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, UploadFile, File

load_dotenv()

app = FastAPI()
client = OpenAI()

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=(file.filename, await file.read())
    )

    return {
        "filename": file.filename,
        "transcript": transcript.text
    }
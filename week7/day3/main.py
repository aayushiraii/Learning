import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm_factory import get_llm

load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    provider: str
    query: str


@app.get("/")
def home():
    return {"message": "Model Switching API Running"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        llm = get_llm(request.provider)

        start_time = time.time()

        response = llm.invoke(request.query)

        latency = round(time.time() - start_time, 2)

        return {
            "provider": request.provider,
            "latency_seconds": latency,
            "answer": response.content
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/evaluate")
def evaluate(query: str):

    results = {}

    for provider in ["openai", "gemini"]:

        try:
            llm = get_llm(provider)

            start_time = time.time()

            response = llm.invoke(query)

            latency = round(time.time() - start_time, 2)

            results[provider] = {
                "latency_seconds": latency,
                "answer": response.content
            }

        except Exception as e:
            results[provider] = {
                "error": str(e)
            }

    return results
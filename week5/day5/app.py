from fastapi import FastAPI
from pydantic import BaseModel

from rag import get_rag_response


app = FastAPI()


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat(request: ChatRequest):

    answer = get_rag_response(request.query)

    return {
        "answer": answer
    }
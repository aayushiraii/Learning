from fastapi import FastAPI
from pydantic import BaseModel

from api import get_rag_response


app = FastAPI()


# Request body
class ChatRequest(BaseModel):
    query: str


# Response body
class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = get_rag_response(request.query)

    return ChatResponse(answer=result)








from fastapi import FastAPI
from pydantic import BaseModel

from llm import ask_llm
from cost import calculate_cost

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "LLM Query API is running"
    }


@app.post("/query")
def query_llm(request: QueryRequest):

    answer, usage = ask_llm(request.question)

    cost_data = calculate_cost(usage)

    return {
        "question": request.question,
        "answer": answer,
        "usage": cost_data
    }
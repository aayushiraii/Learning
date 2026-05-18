from fastapi import FastAPI

from llm import ask_llm
from cost import calculate_cost
from schemas import (
    QueryRequest,
    QueryResponse
)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "LLM Query API is running"
    }


@app.post("/query", response_model=QueryResponse)
def query_llm(request: QueryRequest):

    answer, usage = ask_llm(request.question)

    usage_data = calculate_cost(usage)

    return QueryResponse(
        question=request.question,
        answer=answer,
        usage=usage_data
    )
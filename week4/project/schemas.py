from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class UsageResponse(BaseModel):
    prompt_tokens: int
    cached_tokens: int
    completion_tokens: int
    input_cost: float
    cached_cost: float
    output_cost: float
    total_cost: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    usage: UsageResponse
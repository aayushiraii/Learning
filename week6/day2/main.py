from fastapi import FastAPI
from pydantic import BaseModel

from rag import get_qa_chain

app = FastAPI(
    title="Multi Tenant RAG"
)


class QueryRequest(BaseModel):
    user_id: str
    query: str


@app.get("/")
def home():

    return {
        "message": "Multi Tenant RAG Running"
    }


@app.post("/ask")
def ask(request: QueryRequest):

    try:

        qa_chain = get_qa_chain(
            request.user_id
        )

        result = qa_chain.invoke(
            {
                "query": request.query
            }
        )

        sources = []

        for doc in result.get("source_documents", []):

            sources.append(
                {
                    "page": doc.metadata.get("page"),
                    "source": doc.metadata.get("source"),
                    "user_id": doc.metadata.get("user_id"),
                    "content": doc.page_content[:200]
                }
            )

        return {
            "user_id": request.user_id,
            "query": request.query,
            "answer": result.get("result", ""),
            "sources": sources
        }

    except Exception as e:

        return {
            "error": str(e)
        }
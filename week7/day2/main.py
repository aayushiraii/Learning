from fastapi import FastAPI

app = FastAPI(
    title="Production RAG API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Welcome to the Week 7 RAG Application Gateway!"}

@app.get("/health")
def health_check():
    return {"status": "UP"}
from dotenv import load_dotenv
import os

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

load_dotenv()


# PostgreSQL connection string
CONNECTION = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


# OpenAI embeddings
embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY")
)


# Create LangChain PGVector store
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION,
    use_jsonb=True,
)


# Load PDF
pdf_loader = PyPDFLoader("sample.pdf")
pdf_docs = pdf_loader.load()


# Load TXT
txt_loader = TextLoader("sample.txt")
txt_docs = txt_loader.load()


# Combine docs
docs = pdf_docs + txt_docs


# Store in pgvector
vector_store.add_documents(docs)


print("Documents stored successfully!")
from dotenv import load_dotenv
import os

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model=os.getenv("EMBEDDING_MODEL")
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


def process_documents(documents):

    split_docs = text_splitter.split_documents(documents)

    print(f"\nTotal Chunks: {len(split_docs)}")

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="my_docs",
        connection=DATABASE_URL,
    )

    vector_store.add_documents(split_docs)

    print("\nEmbeddings stored successfully!")
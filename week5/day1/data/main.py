# from openai import OpenAI
# from dotenv import load_dotenv

# from langchain_text_splitters import RecursiveCharacterTextSplitter

# import psycopg2
# import os
# import json
# import logging

# load_dotenv()

# # Logging Configuration
# logging.basicConfig(
#     filename="retrieval.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # OpenAI Client
# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# # Database Connection
# conn = psycopg2.connect(
#     host=os.getenv("DB_HOST"),
#     database=os.getenv("DB_NAME"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     port=os.getenv("DB_PORT")
# )

# cur = conn.cursor()

# logging.info("Database connected successfully")

# # Chunking Configuration
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=50
# )


# def store_embedding(text, metadata):

#     try:

#         response = client.embeddings.create(
#             model=os.getenv("EMBEDDING_MODEL"),
#             input=text
#         )

#         embedding = response.data[0].embedding

#         cur.execute(
#             """
#             INSERT INTO documents (content, embedding, metadata)
#             VALUES (%s, %s, %s)
#             """,
#             (text, embedding, json.dumps(metadata))
#         )

#         conn.commit()

#         logging.info("Embedding stored successfully")

#         print("\nEmbedding Stored Successfully")

#     except Exception as error:

#         logging.error(f"Error storing embedding: {error}")

#         print(error)


# def process_documents(documents):

#     for doc in documents:

#         text = doc.page_content

#         metadata = doc.metadata

#         chunks = text_splitter.split_text(text)

#         print(f"\nTotal Chunks Created: {len(chunks)}")

#         for index, chunk in enumerate(chunks, start=1):

#             print(f"\nStoring Chunk {index}")

#             print(f"Chunk Length: {len(chunk)}")

#             store_embedding(chunk, metadata)


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
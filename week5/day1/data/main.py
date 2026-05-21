from openai import OpenAI
from dotenv import load_dotenv

import psycopg2
import os
import json
import logging

load_dotenv()

# Logging Configuration
logging.basicConfig(
    filename="retrieval.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Database Connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

logging.info("Database connected successfully")


def store_embedding(text, metadata):

    try:

        response = client.embeddings.create(
            model=os.getenv("EMBEDDING_MODEL"),
            input=text
        )

        embedding = response.data[0].embedding

        cur.execute(
            """
            INSERT INTO documents (content, embedding, metadata)
            VALUES (%s, %s, %s)
            """,
            (text, embedding, json.dumps(metadata))
        )

        conn.commit()

        logging.info("Embedding stored successfully")

        print("\nEmbedding Stored Successfully")

    except Exception as error:

        logging.error(f"Error storing embedding: {error}")

        print(error)
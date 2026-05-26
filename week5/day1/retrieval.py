import logging
import time
import os
import psycopg2

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="retrieval.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Application started")

try:
    # OpenAI Client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    logging.info("OpenAI client initialized")

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

    # User Query
    query = input("Enter your question: ")

    logging.info(f"User Query: {query}")

    # Start timer
    start_time = time.time()

    # Generate Embedding
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=query
    )

    query_embedding = response.data[0].embedding

    logging.info("Query embedding generated successfully")

    # Retrieve Similar Documents
    cur.execute(
        """
        SELECT content,
               embedding <-> %s::vector AS distance
        FROM documents
        ORDER BY distance
        LIMIT 5;
        """,
        (query_embedding,)
    )

    results = cur.fetchall()

    print(f"result -- {results}")

    logging.info(f"Retrieved {len(results)} documents")

    # Build Context
    context = ""

    for index, row in enumerate(results, start=1):

        content = row[0]
        distance = row[1]

        logging.info(f"Result {index} Distance: {distance}")

        logging.info(
            f"Result {index} Content Preview: {content[:100]}"
        )

        context += content + "\n"
    
    print(f"context :{context}")

    # Prompt
    prompt = f"""
You are a helpful AI assistant.

Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    logging.info("Prompt created successfully")

    # Generate Final Response
    chat_response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = chat_response.choices[0].message.content

    # End timer
    end_time = time.time()

    logging.info(
        f"Response generated successfully in {end_time - start_time:.2f} seconds"
    )

    # Print Final Answer
    print("\nFinal Answer:\n")
    print(answer)

except Exception as error:

    logging.error(f"Error occurred: {error}")

    print("An error occurred.")
    print(error)

finally:

    # Close Database Connection
    if 'cur' in locals():
        cur.close()

    if 'conn' in locals():
        conn.close()

    logging.info("Database connection closed")
    logging.info("Application finished")
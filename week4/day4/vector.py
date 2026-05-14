from openai import OpenAI
from dotenv import load_dotenv
import psycopg2
import os

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Text to embed
text = "I work at Bitcot"

# Generate embedding
response = client.embeddings.create(
    model=os.getenv("EMBEDDING_MODEL"),
    input=text
)

# Extract embedding vector
embedding = response.data[0].embedding

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Create cursor
cur = conn.cursor()

# Insert into database
cur.execute(
    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
    (text, embedding)
)

# Commit transaction
conn.commit()

print("Embedding stored successfully!")

# Close connections
cur.close()
conn.close()
from langchain_community.document_loaders import (
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader
)
import json 

from openai import OpenAI
from dotenv import load_dotenv

import psycopg2
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

csv_loader = CSVLoader(
    file_path="data/industry.csv"
)

csv_docs = csv_loader.load()

print("\nCSV Loaded Successfully")

docx_loader = UnstructuredWordDocumentLoader(
    "data/sample.docx"
)

docx_docs = docx_loader.load()

print("\nDOCX Loaded Successfully")

pptx_loader = UnstructuredPowerPointLoader(
    "data/sample1.pptx"
)

pptx_docs = pptx_loader.load()

print("\nPPTX Loaded Successfully")

all_docs = csv_docs + docx_docs + pptx_docs

print("\nAll Documents Combined")
print("Total Documents:", len(all_docs))

for doc in all_docs:

    text = doc.page_content

    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text
    )

    embedding = response.data[0].embedding

    cur.execute(
    "INSERT INTO documents (content, embedding, metadata) VALUES (%s, %s, %s)",
    (text, embedding, json.dumps(doc.metadata))
)

    print("\nEmbedding Stored Successfully")

conn.commit()

cur.close()
conn.close()

print("\nAll Embeddings Stored In PostgreSQL")
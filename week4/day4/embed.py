from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Text to embed
text = "I work at bitcot"

# Generate embedding
response = client.embeddings.create(model=os.getenv("EMBEDDING_MODEL"),input=text)

# Extract vector
embedding = response.data[0].embedding

# Print first few numbers
print(embedding[:10])

# Print vector length
print(len(embedding))
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


# Load environment variables
load_dotenv()


# Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = os.getenv("MODEL")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


# Database URL
DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Embedding Model
embeddings = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY,
    model=EMBEDDING_MODEL
)


# Connect to PGVector
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="documents",
    connection=DATABASE_URL,
)


# Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# LLM
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL,
    temperature=0
)


# Prompt Template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a technical AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not available in the context, respond with:
"I could not find the answer in the provided documents."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""
)


# RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={
        "prompt": prompt
    }
)


# Function used by FastAPI and testing
def get_rag_response(query: str):

    # Retrieve documents
    docs = retriever.invoke(query)

    print("\n" + "=" * 60)

    print(f"Question: {query}")

    print(f"\nRetrieved Docs Count: {len(docs)}")

    print("\nRetrieved Documents:\n")

    if len(docs) == 0:
        print("No documents retrieved.")

    else:

        for i, doc in enumerate(docs, start=1):

            print(f"Document {i}:\n")

            print(doc.page_content)

            print("\n" + "-" * 50)

    # Generate response
    response = qa_chain.invoke({
        "query": query
    })

    print("\nGenerated Answer:\n")

    print(response["result"])

    print("\n" + "=" * 60)

    return response["result"]
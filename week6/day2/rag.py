import os

from dotenv import load_dotenv

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings
)

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_postgres import PGVector

from langchain.chains import RetrievalQA

load_dotenv()


# Load PDF
loader = PyPDFLoader("report.pdf")
documents = loader.load()


# Split Documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)


# Add user_id metadata
for doc in docs:
    doc.metadata["user_id"] = "user1"


# Embeddings
embeddings = OpenAIEmbeddings()


# PostgreSQL Connection
CONNECTION = os.getenv("DB_AGENT")


# Vector Store
vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION,
)


# LLM
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0
)


def get_qa_chain(user_id: str):

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 10,
            "filter": {
                "user_id": user_id
            }
        }
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )
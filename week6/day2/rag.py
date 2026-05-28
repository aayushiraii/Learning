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


# Split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)


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


# Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}
)


# LLM
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0
)


# QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)
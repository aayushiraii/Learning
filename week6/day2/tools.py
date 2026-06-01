import os
import logging

from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings
)

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain.prompts import ChatPromptTemplate

from langchain.tools import tool

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_postgres import PGVector

from langchain.chains import RetrievalQA



load_dotenv()


app = FastAPI(
    title="AI Agent API",
    description="FastAPI Agent with RAG and Tools",
    version="1.0"
)




logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class ChatRequest(BaseModel):
    query: str



loader = PyPDFLoader("report.pdf")

documents = loader.load()




text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)




embeddings = OpenAIEmbeddings()




CONNECTION = os.getenv("DB_AGENT")



vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="my_docs",
    connection=CONNECTION,
)


# Add documents
vectorstore.add_documents(docs)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}
)



llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0
)




qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)



@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    """

    try:

        allowed_chars = "0123456789+-*/(). "

        for char in expression:

            if char not in allowed_chars:

                return "Invalid characters in expression"

        result = eval(expression)

        return str(result)

    except Exception as e:

        return f"Calculator Error: {e}"


@tool
def weather(city: str) -> str:
    """
    Get weather information for a city.
    """

    fake_weather = {
        "chennai": "32°C, Sunny",
        "vellore": "35°C, Sunny",
        "bangalore": "24°C, Cloudy",
        "delhi": "40°C, Hot"
    }

    return fake_weather.get(
        city.lower(),
        "Weather not found"
    )


@tool
def company_info(query: str) -> str:
    """
    Get company-related information.
    """

    fake_database = {
        "employees": "250 employees",
        "company": "Bitcot",
        "location": "Chennai"
    }

    return fake_database.get(
        query.lower(),
        "No data found"
    )


@tool
def document_search(query: str) -> str:
    """
    Search uploaded documents and answer questions.
    """

    result = qa_chain.invoke(
        {
            "query": query
        }
    )

    return result["result"]



tools = [
    calculator,
    weather,
    company_info,
    document_search
]





prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Tool Rules:

1. Use document_search for:
   - PDF/document questions
   - week-wise learning questions
   - AI concepts
   - RAG
   - technical topics

2. Use calculator only for math calculations.

3. Use weather only for weather information.

4. Use company_info only for company-related information.

IMPORTANT:
For learning, roadmap, week-wise, AI, or document questions,
ALWAYS use document_search first before answering.
"""
        ),

        ("human", "{input}"),

        ("placeholder", "{agent_scratchpad}")
    ]
)




agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)




agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True
)





@app.post("/agent")
def run_agent(request: ChatRequest):

    try:

        # Empty Query Validation
        if not request.query.strip():

            return {
                "status": "error",
                "message": "Query cannot be empty"
            }

        # Log User Query
        logging.info(
            f"User Query: {request.query}"
        )

        # Agent Response
        response = agent_executor.invoke(
            {
                "input": request.query
            }
        )

        # Log Response
        logging.info(
            f"Agent Response: {response['output']}"
        )

        # Return Final Response
        return {
            "query": request.query,
            "answer": response["output"],
            "status": "success"
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "status": "error",
            "message": str(e)
        }
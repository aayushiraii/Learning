import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain.prompts import ChatPromptTemplate

from tools import calculator
from tools import weather
from tools import company_info


load_dotenv()


# LLM
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0
)


# Tools
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for solving math calculations"
    ),

    Tool(
        name="Weather",
        func=weather,
        description="Useful for getting weather information of cities"
    ),

    Tool(
        name="CompanyInfo",
        func=company_info,
        description="Useful for company-related information"
    )
]


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Use tools whenever needed.

If no tool is required,
respond normally like a chatbot.
"""
        ),

        ("human", "{input}"),

        ("placeholder", "{agent_scratchpad}")
    ]
)


# Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


# Chat Loop
while True:

    query = input("\nAsk something (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    response = agent_executor.invoke(
        {
            "input": query
        }
    )

    print("\nFinal Answer:")
    print(response["output"])
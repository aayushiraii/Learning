import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain.prompts import ChatPromptTemplate

from tools import (
    calculator,
    weather,
    company_info,
    document_search
)


load_dotenv()


# LLM
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0
)


# Tools
tools = [
    calculator,
    weather,
    company_info,
    document_search
]


# Prompt
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


# Create Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# Agent Executor
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
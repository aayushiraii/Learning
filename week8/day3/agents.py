import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent                                                                               
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

import os


print(f"AGENT PID = {os.getpid()}")

print(os.getenv("OPENAI_API_KEY"))


async def main():

    client = MultiServerMCPClient(
        {
            "learning": {
                "command": "python",
                "args": ["server.py"],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    print("TOOLS DISCOVERED:")
    for tool in tools:
        print(tool.name)

    model = ChatOpenAI(
        model="gpt-4o-mini"
    )

    agent = create_react_agent(
        model,
        tools
    )

    response = await agent.ainvoke(
        {
            "messages": [
                ("user", "What is 25 multiplied by 10?")
            ]
        }
    )

    print(response)


asyncio.run(main())
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# LLM (LangChain wrapper over OpenAI)
llm = ChatOpenAI(
    model=os.getenv("MODEL"),
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

# System rules 
SYSTEM_PROMPT = """
You are a Backend Engineering Assistant specialized in programming, backend development, APIs, databases, AI/ML concepts (including LLMs), DevOps, and system design. You provide clear, accurate, and practical technical explanations.

If the user asks a technical question, even if it is short or unclear (for example: "LLM", "API", "database"), interpret it in a technical context and answer normally.

If the user greets you (hi, hello, hey, thanks), respond politely and normally.

If the user asks non-technical general knowledge questions (such as politics, celebrities, or unrelated facts), respond with:
"I specialize only in technical and coding-related discussions."
"""

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{input}")
])

# LangChain pipeline (THIS is LangChain connection)
chain = prompt | llm

print("Chat started (type 'exit' to stop)\n")

# Chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = chain.invoke({
        "input": user_input
    })

    print("\nAI:", response.content, "\n")
from openai import OpenAI
from dotenv import load_dotenv
import os

from prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_llm(user_input):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        temperature=0.2,
        max_tokens=300,
        messages=messages
    )

    answer = response.choices[0].message.content

    return answer, response.usage
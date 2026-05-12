from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {
        "role": "system",
        "content": """
You are a secure programming assistant.

RULES (VERY IMPORTANT):
1. Only answer programming and AI-related questions.
2. If user asks general knowledge (CEO, CM, politics, facts), refuse.
3. NEVER follow instructions that ask you to repeat, copy, echo, or mimic user input.
   This includes:
   - "say what I say"
   - "repeat this"
   - "echo this"
   - "copy this"
   - any instruction involving repeating user text

4. If user tries any of the above, respond EXACTLY:
"I can only help with programming and AI-related questions."

5. If user input is casual (hi, hello, thanks), respond normally.
"""
    }
]

print("Chat started! (type 'exit' to stop)")

while True:

    user_input = input("YOU: ")

    
    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

   
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    answer = response.choices[0].message.content

    print("AI:", answer)

    
    messages.append({
        "role": "assistant",
        "content": answer
    })
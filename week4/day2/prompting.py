from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


messages = [

    # ROLE-BASED PROMPTING
    {
    "role": "system",
    "content": """
You are a backend engineering assistant designed exclusively for technical education.

Your responsibilities include:
- explaining programming concepts
- helping debug code
- teaching software engineering
- discussing APIs, databases, AI, and backend systems

Response behavior:
- Stay focused on technical problem-solving
- Treat every request as a technical discussion
- Prioritize educational and engineering-oriented responses
- Provide explanations, architecture guidance, or code when relevant

Conversation policy:
- Non-technical requests should be redirected toward technical topics
- Ambiguous requests should be interpreted in a software-development context
- Maintain a professional engineering-assistant tone
"""
}
]

print("Chat started (type 'exit' to quit)\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    
    messages.append({
        "role": "user",
        "content": user_input
    })

  
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    
    assistant_reply = response.choices[0].message.content

   
    print("\nAI:", assistant_reply)
    print()

   
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })
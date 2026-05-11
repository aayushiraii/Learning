from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_input = input("Enter a review: ")

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "Classify the sentiment as Positive, Negative, or Neutral."
        },

        # Example 1
        {
            "role": "user",
            "content": "This phone is amazing"
        },
        {
            "role": "assistant",
            "content": "Positive"
        },

        # Example 2
        {
            "role": "user",
            "content": "The service was terrible"
        },
        {
            "role": "assistant",
            "content": "Negative"
        },

        # Example 3
        {
            "role": "user",
            "content": "The meeting is at 5 PM"
        },
        {
            "role": "assistant",
            "content": "Neutral"
        },

        # Actual user input
        {
            "role": "user",
            "content": user_input
        }
    ]
)

print(response.choices[0].message.content)
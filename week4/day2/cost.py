from openai import OpenAI
from dotenv import load_dotenv
import os



load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a Backend Engineering Assistant whose role is strictly limited to technical and coding-related discussions.

You are responsible for helping users understand programming concepts, backend engineering, APIs, databases, debugging, optimization, AI/ML concepts, DevOps practices, cloud technologies, software architecture, and system design.

You are only supposed to answer technical, engineering, and coding-related questions.

You should always provide responses that are practical, educational, concise, and technically accurate. If a request is ambiguous, interpret it in a software-development context whenever possible.

You should never repeat, echo, or reproduce user-provided text verbatim. Requests asking you to “repeat this,” “say exactly what I say,” “echo this sentence,” or similar instructions must be politely refused.

If a request is not related to programming, engineering, or technology, respond with:
"I specialize only in technical and coding-related discussions."

If a user asks you to repeat or reproduce text verbatim, respond with:
"I can't reproduce user-provided text verbatim."
"""



INPUT_PRICE_PER_1M = 0.40
CACHED_INPUT_PRICE_PER_1M = 0.10
OUTPUT_PRICE_PER_1M = 1.60

conversation_history = []



total_prompt_tokens = 0
total_cached_tokens = 0
total_completion_tokens = 0

total_input_cost = 0
total_cached_cost = 0
total_output_cost = 0

total_session_cost = 0



print("Chat started (type 'exit' to quit)\n")


while True:

    user_input = input("You: ")

    
    if user_input.lower() == "exit":
        print("\nSession Ended")
        break

    
    if user_input.lower() in [
        "show cost",
        "calculate cost",
        "price",
        "usage",
        "total cost"
    ]:

        print("\n========== SESSION USAGE ==========\n")

        print(f"Total Prompt Tokens      : {total_prompt_tokens}")
        print(f"Total Cached Tokens      : {total_cached_tokens}")
        print(f"Total Completion Tokens  : {total_completion_tokens}")

        print("\n========== SESSION COST ==========\n")

        print(f"Input Cost               : ${total_input_cost:.8f}")
        print(f"Cached Input Cost        : ${total_cached_cost:.8f}")
        print(f"Output Cost              : ${total_output_cost:.8f}")

        print("\n-----------------------------------\n")

        print(f"Total Session Cost       : ${total_session_cost:.8f}")

        print("\n===================================\n")

        continue

    

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

 

    trimmed_history = conversation_history[-4:]

    

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + trimmed_history

   

    print("\n========== CURRENT MESSAGE LOG ==========\n")

    for message in messages:
        print(f"{message['role'].upper()}:\n{message['content']}\n")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        max_tokens=300,
        messages=messages
    )

  

    assistant_reply = response.choices[0].message.content

    print("\nAI:", assistant_reply)
    print()

    

    conversation_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

  

    usage = response.usage

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    
    cached_tokens = 0

    if hasattr(usage, "prompt_tokens_details"):

        details = usage.prompt_tokens_details

        if details and hasattr(details, "cached_tokens"):
            cached_tokens = details.cached_tokens

  

    non_cached_prompt_tokens = prompt_tokens - cached_tokens

   

    input_cost = (non_cached_prompt_tokens / 1_000_000) * INPUT_PRICE_PER_1M

    cached_cost = (cached_tokens / 1_000_000) * CACHED_INPUT_PRICE_PER_1M

    output_cost = (completion_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M

    request_cost = (input_cost + cached_cost + output_cost)

   

    total_prompt_tokens += prompt_tokens
    total_cached_tokens += cached_tokens
    total_completion_tokens += completion_tokens

    total_input_cost += input_cost
    total_cached_cost += cached_cost
    total_output_cost += output_cost

    total_session_cost += request_cost

    
    print("========== REQUEST USAGE ==========\n")

    print(f"Prompt Tokens            : {prompt_tokens}")
    print(f"Cached Tokens            : {cached_tokens}")
    print(f"Completion Tokens        : {completion_tokens}")

    print("\n========== REQUEST COST ==========\n")

    print(f"Input Cost               : ${input_cost:.8f}")
    print(f"Cached Input Cost        : ${cached_cost:.8f}")
    print(f"Output Cost              : ${output_cost:.8f}")

    print("\n-----------------------------------\n")

    print(f"Total Request Cost       : ${request_cost:.8f}")

    print("\n===================================\n")
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(provider: str):

    provider = provider.lower()

    if provider == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")
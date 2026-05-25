from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

from langchain.chains import RetrievalQA

from constant import (
    OPENAI_API_KEY,
    MODEL,
    EMBEDDING_MODEL,
    DATABASE_URL,
    COLLECTION_NAME
)

from prompt import RAG_PROMPT


"""
RAG pipeline implementation using:
- OpenAI Embeddings
- PGVector
- LangChain RetrievalQA
"""


# Embedding model initialization
embeddings = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY,
    model=EMBEDDING_MODEL
)


# PGVector initialization
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=DATABASE_URL,
)


# Retriever initialization
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)


# LLM initialization
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL,
    temperature=0
)


# RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={
        "prompt": RAG_PROMPT
    }
)


def get_rag_response(query: str) -> str:
    """
    Generate a response using the RAG pipeline.

    Args:
        query (str):
            User input question.

    Returns:
        str:
            Generated response from the LLM.
    """

    print(f"\nUser Query: {query}")

    # Retrieve relevant documents
    docs = retriever.invoke(query)

    print("\n========== RETRIEVED CONTEXT ==========\n")

    if not docs:
        print("No documents retrieved!")

    for i, doc in enumerate(docs, start=1):

        print(f"\n--- Document {i} ---")

        print(doc.page_content)

        print("\nMetadata:", doc.metadata)

    print("\n=======================================\n")

    # Generate response
    result = qa_chain.invoke({
        "query": query
    })

    return result["result"]
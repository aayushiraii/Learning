from rag import get_rag_response


def test_rag_question():

    response = get_rag_response("What is RAG?")

    assert response is not None

    assert isinstance(response, str)


def test_langchain_question():

    response = get_rag_response("What is LangChain?")

    assert response is not None


def test_hallucination():

    response = get_rag_response(
        "Who won the FIFA World Cup?"
    )

    assert response is not None


def test_empty_query():

    response = get_rag_response("")

    assert response is not None
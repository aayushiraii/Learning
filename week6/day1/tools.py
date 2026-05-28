from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    """

    try:
        return str(eval(expression))

    except Exception as e:
        return f"Calculator Error: {e}"


@tool
def weather(city: str) -> str:
    """
    Get weather information for a city.
    """

    fake_weather = {
        "chennai": "32°C, Sunny",
        "vellore": "35°C, Sunny",
        "bangalore": "24°C, Cloudy",
        "delhi": "40°C, Hot"
    }

    return fake_weather.get(
        city.lower(),
        "Weather not found"
    )


@tool
def company_info(query: str) -> str:
    """
    Get company-related information.
    """

    fake_database = {
        "employees": "250 employees",
        "company": "Bitcot",
        "location": "Chennai"
    }

    return fake_database.get(
        query.lower(),
        "No data found"
    )
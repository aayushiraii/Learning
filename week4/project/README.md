# LLM Query API

This project is a simple FastAPI backend that connects with the OpenAI API to answer technical questions.

The API accepts a user question, sends it to the LLM, and returns:
* the AI response
* token usage
* request cost

This project was built while learning:
* LLMs
* Prompt Engineering
* OpenAI API
* FastAPI
* Cost Tracking



# Features

* FastAPI backend
* OpenAI integration
* Prompt handling using system prompts
* Token usage tracking
* Cost calculation




# Techstack

- Python
- FastAPI



# Project Structure


project/
│
├── main.py
├── llm.py
├── cost.py
├── requirements.txt
├── .env
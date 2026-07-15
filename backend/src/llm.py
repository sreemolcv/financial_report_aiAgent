from langchain_groq import ChatGroq

from src.config import GROQ_API_KEY , GROQ_MODEL, TEMPERATURE

def get_llm() -> ChatGroq:

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=TEMPERATURE,
        max_tokens=2048
    )
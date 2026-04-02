from functools import lru_cache

from langchain_groq import ChatGroq

from app.config import get_settings


@lru_cache
def get_chat_model(
    model_name: str = "llama-3.1-8b-instant",
    temperature: float = 0.2,
) -> ChatGroq:
    settings = get_settings()

    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=settings.groq_api_key,
    )

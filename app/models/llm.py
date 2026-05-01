from functools import lru_cache
from typing import Type

from langchain_groq import ChatGroq
from pydantic import BaseModel

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


def get_structured_chat_model(schema: Type[BaseModel]):
    return get_chat_model(
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
    ).with_structured_output(schema)

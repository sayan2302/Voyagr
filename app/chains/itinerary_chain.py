from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.models import get_chat_model
from app.prompt_library import ITINERARY_FEW_SHOT_PROMPT


def build_itinerary_prompt(inputs: dict) -> str:
    return ITINERARY_FEW_SHOT_PROMPT.format(**inputs)


itinerary_prompt_chain = RunnableLambda(build_itinerary_prompt)
itinerary_generation_chain = itinerary_prompt_chain | get_chat_model() | StrOutputParser()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.models import get_chat_model, get_structured_chat_model
from app.prompt_library import ITINERARY_FEW_SHOT_PROMPT
from app.schemas import ItineraryResponse
from app.tools import summarize_trip_preferences


def prepare_itinerary_inputs(inputs: dict) -> dict:
    preference_summary = summarize_trip_preferences.invoke(
        {
            "destination": inputs["destination"],
            "budget": inputs["budget"],
            "interests": inputs["interests"],
            "group_size": inputs["group_size"],
        }
    )

    enriched_inputs = dict(inputs)
    notes = enriched_inputs.get("notes", "").strip()

    if notes:
        enriched_inputs["notes"] = f"{notes} | Preference summary: {preference_summary}"
    else:
        enriched_inputs["notes"] = f"Preference summary: {preference_summary}"

    return enriched_inputs


def build_itinerary_prompt(inputs: dict) -> str:
    prepared_inputs = prepare_itinerary_inputs(inputs)
    return ITINERARY_FEW_SHOT_PROMPT.format(**prepared_inputs)


itinerary_prompt_chain = RunnableLambda(build_itinerary_prompt)
itinerary_generation_chain = itinerary_prompt_chain | get_chat_model() | StrOutputParser()
structured_itinerary_generation_chain = (
    itinerary_prompt_chain | get_structured_chat_model(ItineraryResponse)
)

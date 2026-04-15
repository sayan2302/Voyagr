from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.models import get_chat_model, get_structured_chat_model
from app.prompt_library import ITINERARY_FEW_SHOT_PROMPT
from app.schemas import ItineraryResponse
from app.tools import get_weather_forecast, summarize_trip_preferences
from app.tools.tool_exceptions import ToolExecutionError


def prepare_itinerary_inputs(inputs: dict) -> dict:
    preference_summary = summarize_trip_preferences.invoke(
        {
            "destination": inputs["destination"],
            "budget": inputs["budget"],
            "interests": inputs["interests"],
            "group_size": inputs["group_size"],
        }
    )

    weather_note = "Weather forecast unavailable."

    try:
        weather_data = get_weather_forecast.invoke(
            {
                "destination": inputs["destination"],
                "forecast_days": min(int(inputs["trip_days"]), 3),
            }
        )

        weather_lines = []
        for day in weather_data.forecast_days:
            weather_lines.append(
                f"{day.date}: {day.weather}, "
                f"{day.temperature_min_c}C to {day.temperature_max_c}C, "
                f"precipitation {day.precipitation_mm} mm"
            )

        weather_note = f"Weather forecast: {' | '.join(weather_lines)}"
    except ToolExecutionError as exc:
        weather_note = f"Weather forecast unavailable due to tool error: {exc.message}"

    enriched_inputs = dict(inputs)
    notes = enriched_inputs.get("notes", "").strip()

    enrichment_parts = [
        f"Preference summary: {preference_summary}",
        weather_note,
    ]

    if notes:
        enrichment_parts.insert(0, notes)

    enriched_inputs["notes"] = " | ".join(enrichment_parts)
    return enriched_inputs


def build_itinerary_prompt(inputs: dict) -> str:
    prepared_inputs = prepare_itinerary_inputs(inputs)
    return ITINERARY_FEW_SHOT_PROMPT.format(**prepared_inputs)


itinerary_prompt_chain = RunnableLambda(build_itinerary_prompt)
itinerary_generation_chain = itinerary_prompt_chain | get_chat_model() | StrOutputParser()
structured_itinerary_generation_chain = (
    itinerary_prompt_chain | get_structured_chat_model(ItineraryResponse)
)



# Input:
# {
#   "destination": "Paris",
#   "trip_days": 2,
#   "budget": "medium",
#   "interests": "museums, cafes, walking",
#   "group_size": 2,
#   "notes": "avoid rushing between places"
# }

# Tool output type inside the chain:
# WeatherForecastResponse(
#     destination="Paris",
#     ...,
#     forecast_days=[
#         WeatherForecastDay(...),
#         WeatherForecastDay(...),
#     ],
# )

# Enriched notes example:
# "avoid rushing between places |
#  Preference summary: Trip planned for 2 traveler(s) to Paris with a medium budget and interests in museums, cafes, walking. |
#  Weather forecast: 2026-04-14: Fog, 5.0C to 17.8C, precipitation 0.0 mm | 2026-04-15: Slight rain, 9.3C to 18.2C, precipitation 0.1 mm"

from app.agent.state import VoyagrAgentState
from app.tools import get_weather_forecast, discover_places
from app.tools.tool_exceptions import ToolExecutionError
from app.chains import structured_itinerary_generation_chain


def weather_node(state: VoyagrAgentState) -> dict:
    try:
        weather = get_weather_forecast.invoke(
            {
                "destination": state.request.destination,
                "forecast_days": min(state.request.trip_days, 3),
            }
        )
        return {"weather": weather}
    except ToolExecutionError as exc:
        return {"errors": [*state.errors, f"weather_node: {exc.message}"]}


def places_node(state: VoyagrAgentState) -> dict:
    try:
        places = discover_places.invoke(
            {
                "destination": state.request.destination,
                "interests": state.request.interests,
                "max_results": 3,
            }
        )
        return {"places": places}
    except ToolExecutionError as exc:
        return {"errors": [*state.errors, f"places_node: {exc.message}"]}


def planner_node(state: VoyagrAgentState) -> dict:
    try:
        enriched_notes = []

        if state.request.notes.strip():
            enriched_notes.append(state.request.notes.strip())

        if state.weather is not None:
            weather_lines = []
            for day in state.weather.forecast_days:
                weather_lines.append(
                    f"{day.date}: {day.weather}, "
                    f"{day.temperature_min_c}C to {day.temperature_max_c}C, "
                    f"precipitation {day.precipitation_mm} mm"
                )
            enriched_notes.append(f"Weather forecast: {' | '.join(weather_lines)}")

        if state.places is not None:
            place_titles = [result.title for result in state.places.results[:3]]
            enriched_notes.append(
                f"Suggested places/activities: {', '.join(place_titles)}. "
                f"Discovery summary: {state.places.answer or 'No summary available.'}"
            )

        itinerary = structured_itinerary_generation_chain.invoke(
            {
                "destination": state.request.destination,
                "trip_days": state.request.trip_days,
                "budget": state.request.budget,
                "interests": state.request.interests,
                "group_size": state.request.group_size,
                "notes": " | ".join(enriched_notes),
            }
        )

        return {"itinerary": itinerary}
    except Exception as exc:
        return {"errors": [*state.errors, f"planner_node: {exc}"]}

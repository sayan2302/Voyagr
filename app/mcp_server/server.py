from fastmcp import FastMCP

from app.mcp_server.prompts import build_itinerary_prompt_text
from app.mcp_server.resources import load_architecture_markdown
from app.tools import discover_places, get_weather_forecast

mcp = FastMCP("voyagr-mcp")


@mcp.tool
def weather_forecast(destination: str, forecast_days: int = 3):
    return get_weather_forecast.invoke(
        {
            "destination": destination,
            "forecast_days": forecast_days,
        }
    )


@mcp.tool
def place_discovery(destination: str, interests: str, max_results: int = 5):
    return discover_places.invoke(
        {
            "destination": destination,
            "interests": interests,
            "max_results": max_results,
        }
    )


@mcp.resource("voyagr://architecture")
def architecture_resource() -> str:
    return load_architecture_markdown()


@mcp.prompt
def itinerary_prompt(
    destination: str,
    trip_days: int,
    budget: str,
    interests: str,
    group_size: int,
    notes: str,
) -> str:
    return build_itinerary_prompt_text(
        destination=destination,
        trip_days=trip_days,
        budget=budget,
        interests=interests,
        group_size=group_size,
        notes=notes,
    )


if __name__ == "__main__":
    mcp.run()

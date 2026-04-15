import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from langchain_core.tools import tool
from pydantic import ValidationError

from app.schemas import WeatherForecastDay, WeatherForecastResponse
from app.tools.tool_exceptions import ToolExecutionError


WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def _fetch_json(base_url: str, params: dict) -> dict:
    query = urlencode(params)
    url = f"{base_url}?{query}"

    try:
        with urlopen(url, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        raise ToolExecutionError("get_weather_forecast", f"Network error: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolExecutionError("get_weather_forecast", "Invalid JSON response.") from exc


def _geocode_destination(destination: str) -> dict:
    data = _fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {
            "name": destination,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = data.get("results", [])
    if not results:
        raise ToolExecutionError(
            "get_weather_forecast",
            f"Could not find coordinates for destination: {destination}",
        )

    return results[0]


@tool
def get_weather_forecast(destination: str, forecast_days: int = 3) -> WeatherForecastResponse:
    """
    Get a short daily weather forecast for a destination using Open-Meteo.
    """
    if forecast_days < 1 or forecast_days > 7:
        raise ToolExecutionError(
            "get_weather_forecast",
            "forecast_days must be between 1 and 7.",
        )

    try:
        place = _geocode_destination(destination)

        forecast = _fetch_json(
            "https://api.open-meteo.com/v1/forecast",
            {
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "forecast_days": forecast_days,
                "timezone": "auto",
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_sum"
                ),
            },
        )

        daily = forecast["daily"]
        days = []

        for index, date in enumerate(daily["time"]):
            weather_code = daily["weather_code"][index]
            days.append(
                WeatherForecastDay(
                    date=date,
                    weather=WMO_WEATHER_CODES.get(
                        weather_code,
                        f"Unknown code {weather_code}",
                    ),
                    temperature_max_c=daily["temperature_2m_max"][index],
                    temperature_min_c=daily["temperature_2m_min"][index],
                    precipitation_mm=daily["precipitation_sum"][index],
                )
            )

        return WeatherForecastResponse(
            destination=place["name"],
            country=place.get("country"),
            latitude=place["latitude"],
            longitude=place["longitude"],
            forecast_days=days,
        )
    except KeyError as exc:
        raise ToolExecutionError(
            "get_weather_forecast",
            f"Unexpected response format: missing key {exc}",
        ) from exc
    except ValidationError as exc:
        raise ToolExecutionError(
            "get_weather_forecast",
            f"Weather schema validation failed: {exc}",
        ) from exc



# Input:
# get_weather_forecast.invoke({"destination": "Paris", "forecast_days": 2})

# Output type:
# WeatherForecastResponse

# Example output:
# WeatherForecastResponse(
#     destination="Paris",
#     country="France",
#     latitude=48.85341,
#     longitude=2.3488,
#     forecast_days=[
#         WeatherForecastDay(
#             date="2026-04-14",
#             weather="Slight rain",
#             temperature_max_c=16.3,
#             temperature_min_c=10.7,
#             precipitation_mm=0.5,
#         ),
#         ...
#     ],
# )

from pydantic import BaseModel, Field


class WeatherForecastDay(BaseModel):
    date: str = Field(..., description="Forecast date in ISO format")
    weather: str = Field(..., description="Human-readable weather description")
    temperature_max_c: float = Field(..., description="Maximum daily temperature in Celsius")
    temperature_min_c: float = Field(..., description="Minimum daily temperature in Celsius")
    precipitation_mm: float = Field(..., description="Daily precipitation total in millimeters")


class WeatherForecastResponse(BaseModel):
    destination: str = Field(..., description="Resolved destination name")
    country: str | None = Field(default=None, description="Resolved destination country")
    latitude: float = Field(..., description="Resolved latitude")
    longitude: float = Field(..., description="Resolved longitude")
    forecast_days: list[WeatherForecastDay] = Field(
        default_factory=list,
        description="Daily forecast entries",
    )

    
# Example structured output:
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
#         )
#     ],
# )

from pydantic import BaseModel, Field

from app.schemas import ItineraryResponse
from app.schemas.places import PlaceDiscoveryResponse
from app.schemas.weather import WeatherForecastResponse


class TripRequestState(BaseModel):
    destination: str = Field(..., description="Trip destination")
    trip_days: int = Field(..., ge=1, description="Number of trip days")
    budget: str = Field(..., description="Budget preference")
    interests: str = Field(..., description="Interests string for planning")
    group_size: int = Field(..., ge=1, description="Number of travelers")
    notes: str = Field(default="", description="Extra planning notes")


class VoyagrAgentState(BaseModel):
    request: TripRequestState = Field(..., description="Incoming trip request")
    weather: WeatherForecastResponse | None = Field(
        default=None,
        description="Weather data gathered during the workflow",
    )
    places: PlaceDiscoveryResponse | None = Field(
        default=None,
        description="Place discovery data gathered during the workflow",
    )
    itinerary: ItineraryResponse | None = Field(
        default=None,
        description="Final structured itinerary if generated",
    )
    review_status: str | None = Field(
        default=None,
        description="Planner review result such as approved or needs_revision",
    )
    review_notes: list[str] = Field(
        default_factory=list,
        description="Review comments collected after itinerary generation",
    )
    revision_count: int = Field(
        default=0,
        ge=0,
        description="How many revision cycles have been attempted",
    )
    max_revisions: int = Field(
        default=1,
        ge=0,
        description="Maximum allowed revision cycles before forcing workflow completion",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="Collected workflow errors",
    )

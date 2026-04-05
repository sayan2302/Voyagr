from pydantic import BaseModel, Field


class ItineraryDay(BaseModel):
    day: int = Field(..., ge=1, description="Day number in the itinerary")
    title: str = Field(..., description="Short title for the day's plan")
    activities: list[str] = Field(
        default_factory=list,
        description="Ordered list of activities for the day",
    )


class ItineraryResponse(BaseModel):
    destination: str = Field(..., description="Trip destination")
    trip_days: int = Field(..., ge=1, description="Total number of trip days")
    overview: str = Field(..., description="Short summary of the itinerary")
    days: list[ItineraryDay] = Field(
        default_factory=list,
        description="Day-by-day itinerary breakdown",
    )

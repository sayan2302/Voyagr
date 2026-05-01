from pydantic import BaseModel, Field


class ItineraryActivity(BaseModel):
    time_slot: str = Field(..., description="Approximate time slot like 09:00-11:00")
    name: str = Field(..., description="Short activity name")
    details: str = Field(..., description="Why this activity fits and what to expect")
    estimated_cost: str = Field(..., description="Estimated cost guidance for this activity")
    weather_fit: str = Field(..., description="How the activity fits the weather or fallback logic")


class ItineraryDay(BaseModel):
    day: int = Field(..., ge=1, description="Day number in the itinerary")
    title: str = Field(..., description="Short title for the day's plan")
    area: str = Field(..., description="Primary neighborhood or area focus for the day")
    morning: list[ItineraryActivity] = Field(
        default_factory=list,
        description="Morning activity plan",
    )
    afternoon: list[ItineraryActivity] = Field(
        default_factory=list,
        description="Afternoon activity plan",
    )
    evening: list[ItineraryActivity] = Field(
        default_factory=list,
        description="Evening activity plan",
    )
    food_recommendation: str = Field(
        ...,
        description="Meal or food-style recommendation for the day",
    )
    transport_tip: str = Field(
        ...,
        description="Practical transport tip for the day",
    )
    daily_budget_estimate: str = Field(
        ...,
        description="Approximate daily spend guidance",
    )


class ItineraryResponse(BaseModel):
    destination: str = Field(..., description="Trip destination")
    trip_days: int = Field(..., ge=1, description="Total number of trip days")
    overview: str = Field(..., description="Short summary of the itinerary")
    budget_summary: str = Field(..., description="Overall budget framing for the trip")
    pacing_notes: str = Field(..., description="Notes about trip pace and realism")
    general_tips: list[str] = Field(
        default_factory=list,
        description="Helpful overall travel tips",
    )
    days: list[ItineraryDay] = Field(
        default_factory=list,
        description="Detailed day-by-day itinerary breakdown",
    )

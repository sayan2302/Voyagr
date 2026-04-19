from app.prompt_library import ITINERARY_USER_PROMPT


def build_itinerary_prompt_text(
    destination: str,
    trip_days: int,
    budget: str,
    interests: str,
    group_size: int,
    notes: str,
) -> str:
    return ITINERARY_USER_PROMPT.format(
        destination=destination,
        trip_days=trip_days,
        budget=budget,
        interests=interests,
        group_size=group_size,
        notes=notes,
    )

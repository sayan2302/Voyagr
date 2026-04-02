from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from app.prompt_library.examples import ITINERARY_FEW_SHOT_EXAMPLES


ITINERARY_SYSTEM_PROMPT = """
You are Voyagr, an expert AI travel planner.

Your job is to create practical, personalized, and well-structured travel itineraries.
Prioritize clarity, usefulness, realistic pacing, and budget awareness.
When making recommendations, consider the user's destination, trip length, budget,
interests, and group size.
""".strip()


ITINERARY_USER_PROMPT = PromptTemplate(
    input_variables=[
        "destination",
        "trip_days",
        "budget",
        "interests",
        "group_size",
        "notes",
    ],
    template="""
Create a personalized travel itinerary using the following trip details.

Destination: {destination}
Trip Length (days): {trip_days}
Budget: {budget}
Interests: {interests}
Group Size: {group_size}
Additional Notes: {notes}

Return a day-by-day itinerary that is clear, realistic, and easy to follow.
""".strip(),
)


ITINERARY_EXAMPLE_PROMPT = PromptTemplate(
    input_variables=[
        "destination",
        "trip_days",
        "budget",
        "interests",
        "group_size",
        "notes",
        "output",
    ],
    template="""
Trip Details:
Destination: {destination}
Trip Length (days): {trip_days}
Budget: {budget}
Interests: {interests}
Group Size: {group_size}
Additional Notes: {notes}

Example Itinerary:
{output}
""".strip(),
)


ITINERARY_FEW_SHOT_PROMPT = FewShotPromptTemplate(
    examples=ITINERARY_FEW_SHOT_EXAMPLES,
    example_prompt=ITINERARY_EXAMPLE_PROMPT,
    suffix=ITINERARY_USER_PROMPT.template,
    input_variables=[
        "destination",
        "trip_days",
        "budget",
        "interests",
        "group_size",
        "notes",
    ],
)

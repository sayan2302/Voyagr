from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from app.prompt_library.examples import ITINERARY_FEW_SHOT_EXAMPLES


ITINERARY_SYSTEM_PROMPT = """
You are Voyagr, an expert AI travel planner.

Your job is to create practical, personalized, and well-structured travel itineraries.
Prioritize clarity, usefulness, realistic pacing, budget awareness, and day-to-day usability.
Use weather and place-discovery context when it is available.
Avoid rushed plans, long unrealistic jumps across a city, and vague filler activities.
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

Return a rich structured itinerary.

Requirements:
- Include a strong overview, budget_summary, and pacing_notes.
- Include several useful general_tips.
- For each day, include:
  - title
  - area
  - morning activities
  - afternoon activities
  - evening activities
  - food_recommendation
  - transport_tip
  - daily_budget_estimate
- For each activity, include:
  - time_slot
  - name
  - details
  - estimated_cost
  - weather_fit
- Keep the plan realistic and geographically sensible.
- Use weather context when relevant, especially for outdoor vs indoor choices.
- Make the output feel useful to a real traveler, not generic.
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

from langchain_core.tools import tool


@tool
def summarize_trip_preferences(
    destination: str,
    budget: str,
    interests: str,
    group_size: int,
) -> str:
    """
    Summarize user trip preferences into a concise planning sentence.
    """
    return (
        f"Trip planned for {group_size} traveler(s) to {destination} "
        f"with a {budget} budget and interests in {interests}."
    )

from app.agent.state import VoyagrAgentState


def route_after_weather(state: VoyagrAgentState) -> str:
    if any(error.startswith("weather_node:") for error in state.errors):
        return "skip_places"

    return "continue_to_places"


def route_after_places(state: VoyagrAgentState) -> str:
    return "continue_to_planner"


def route_after_review(state: VoyagrAgentState) -> str:
    if state.review_status == "approved":
        return "finish"

    if state.revision_count >= state.max_revisions:
        return "finish"

    return "revise"

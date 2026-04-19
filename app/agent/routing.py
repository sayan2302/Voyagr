from app.agent.state import VoyagrAgentState


def route_after_weather(state: VoyagrAgentState) -> str:
    return "places_node"

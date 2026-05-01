from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    places_node,
    planner_node,
    review_node,
    revision_node,
    weather_node,
)
from app.agent.routing import (
    route_after_places,
    route_after_review,
    route_after_weather,
)
from app.agent.state import VoyagrAgentState


builder = StateGraph(VoyagrAgentState)

builder.add_node("weather_node", weather_node)
builder.add_node("places_node", places_node)
builder.add_node("planner_node", planner_node)
builder.add_node("review_node", review_node)
builder.add_node("revision_node", revision_node)

builder.add_edge(START, "weather_node")
builder.add_conditional_edges(
    "weather_node",
    route_after_weather,
    {
        "continue_to_places": "places_node",
        "skip_places": "planner_node",
    },
)
builder.add_conditional_edges(
    "places_node",
    route_after_places,
    {
        "continue_to_planner": "planner_node",
    },
)
builder.add_edge("planner_node", "review_node")
builder.add_conditional_edges(
    "review_node",
    route_after_review,
    {
        "finish": END,
        "revise": "revision_node",
    },
)
builder.add_edge("revision_node", "planner_node")

checkpointer = InMemorySaver()
voyagr_graph = builder.compile(checkpointer=checkpointer)

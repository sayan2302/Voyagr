from langgraph.graph import END, START, StateGraph

from app.agent.nodes import places_node, planner_node, weather_node
from app.agent.state import VoyagrAgentState


builder = StateGraph(VoyagrAgentState)

builder.add_node("weather_node", weather_node)
builder.add_node("places_node", places_node)
builder.add_node("planner_node", planner_node)

builder.add_edge(START, "weather_node")
builder.add_edge("weather_node", "places_node")
builder.add_edge("places_node", "planner_node")
builder.add_edge("planner_node", END)

voyagr_graph = builder.compile()

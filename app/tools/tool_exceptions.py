class ToolExecutionError(Exception):
    def __init__(self, tool_name: str, message: str):
        self.tool_name = tool_name
        self.message = message
        super().__init__(f"{tool_name} failed: {message}")

    def to_dict(self) -> dict[str, str]:
        return {
            "tool": self.tool_name,
            "message": self.message,
        }
    
    
# Input:
# error = ToolExecutionError(
#     tool_name="get_weather_forecast",
#     message="Could not find coordinates for destination: Atlantis",
# )

# String form:
# "get_weather_forecast failed: Could not find coordinates for destination: Atlantis"

# Structured form:
# {
#     "tool": "get_weather_forecast",
#     "message": "Could not find coordinates for destination: Atlantis",
# }

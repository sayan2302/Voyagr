import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from langchain_core.tools import tool
from pydantic import ValidationError

from app.config import get_settings
from app.schemas import PlaceDiscoveryResponse, PlaceDiscoveryResult
from app.tools.tool_exceptions import ToolExecutionError


def _tavily_search(payload: dict) -> dict:
    settings = get_settings()

    if not settings.tavily_api_key:
        raise ToolExecutionError(
            "discover_places",
            "TAVILY_API_KEY is not set.",
        )

    request = Request(
        url="https://api.tavily.com/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.tavily_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        raise ToolExecutionError("discover_places", f"Network error: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolExecutionError("discover_places", "Invalid JSON response.") from exc


@tool
def discover_places(
    destination: str,
    interests: str,
    max_results: int = 5,
) -> PlaceDiscoveryResponse:
    """
    Discover relevant places or activities for a destination using Tavily search.
    """
    if max_results < 1 or max_results > 10:
        raise ToolExecutionError(
            "discover_places",
            "max_results must be between 1 and 10.",
        )

    query = (
        f"Best places, attractions, and activities in {destination} "
        f"for someone interested in {interests}"
    )

    data = _tavily_search(
        {
            "query": query,
            "topic": "general",
            "search_depth": "basic",
            "max_results": max_results,
            "include_answer": True,
        }
    )

    try:
        results = data.get("results", [])
        normalized_results = []

        for item in results:
            normalized_results.append(
                PlaceDiscoveryResult(
                    title=item["title"],
                    url=item["url"],
                    summary=item["content"],
                    score=item.get("score"),
                )
            )

        return PlaceDiscoveryResponse(
            destination=destination,
            interests=interests,
            query=query,
            answer=data.get("answer"),
            results=normalized_results,
        )
    except KeyError as exc:
        raise ToolExecutionError(
            "discover_places",
            f"Unexpected Tavily response format: missing key {exc}",
        ) from exc
    except ValidationError as exc:
        raise ToolExecutionError(
            "discover_places",
            f"Places schema validation failed: {exc}",
        ) from exc

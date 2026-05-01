from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agent.graph import voyagr_graph
from app.agent.state import TripRequestState
from app.config import get_settings
from app.core import AppException

router = APIRouter()


class GenerateItineraryPayload(BaseModel):
    # Input shape expected by the backend:
    # {
    #   "request": {...trip fields...},
    #   "max_revisions": 1,
    # }
    request: TripRequestState
    max_revisions: int = Field(default=1, ge=0)


@router.get("/health")
async def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


@router.get("/error-test")
async def error_test() -> None:
    raise AppException(message="This is a controlled test error.")


@router.post("/itinerary")
def generate_itinerary(payload: GenerateItineraryPayload) -> dict:
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    result = voyagr_graph.invoke(payload.model_dump(), config)

    # Output shape:
    # {
    #   "thread_id": "...",
    #   "result": {
    #       "request": {...},
    #       "weather": {...},
    #       "places": {...},
    #       "itinerary": {...},
    #       "review_status": "...",
    #       "review_notes": [...],
    #       "errors": [...],
    #   }
    # }
    return {
        "thread_id": thread_id,
        "result": result,
    }

from pydantic import BaseModel, Field


class PlaceDiscoveryResult(BaseModel):
    title: str = Field(..., description="Title of the discovered place or source")
    url: str = Field(..., description="Source URL")
    summary: str = Field(..., description="Short summary of the discovery result")
    score: float | None = Field(default=None, description="Provider relevance score if available")


class PlaceDiscoveryResponse(BaseModel):
    destination: str = Field(..., description="Destination being researched")
    interests: str = Field(..., description="Interest profile used for discovery")
    query: str = Field(..., description="Search query sent to the provider")
    answer: str | None = Field(default=None, description="Short provider-generated summary answer")
    results: list[PlaceDiscoveryResult] = Field(
        default_factory=list,
        description="Normalized ranked discovery results",
    )

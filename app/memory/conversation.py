from pydantic import BaseModel, Field


class ConversationTurn(BaseModel):
    role: str = Field(..., description="Who produced the message, such as user or assistant")
    content: str = Field(..., min_length=1, description="The message content")


class ConversationMemory(BaseModel):
    destination: str | None = Field(default=None, description="Current trip destination")
    budget: str | None = Field(default=None, description="Current budget preference")
    interests: list[str] = Field(
        default_factory=list,
        description="Collected user interests across the conversation",
    )
    group_size: int | None = Field(default=None, ge=1, description="Traveler group size")
    notes: list[str] = Field(
        default_factory=list,
        description="Important extra constraints or preferences",
    )
    history: list[ConversationTurn] = Field(
        default_factory=list,
        description="Conversation history collected so far",
    )

    def add_turn(self, role: str, content: str) -> None:
        self.history.append(ConversationTurn(role=role, content=content))

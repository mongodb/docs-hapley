from pydantic import BaseModel, Field


class ReorderItemPayload(BaseModel):
    current_index: int = Field(alias="currentIndex")
    target_index: int = Field(alias="targetIndex")

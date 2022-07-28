from pydantic import BaseModel, Field


class ReorderItemPayload(BaseModel):
    current_index: int = Field(alias="currentIndex")
    target_index: int = Field(alias="targetIndex")

    class Config:
        allow_population_by_field_name = True

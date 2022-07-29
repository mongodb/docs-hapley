from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field


class Group(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    group_label: str = Field(alias="groupLabel")
    included_branches: list[str] = Field(alias="includedBranches")

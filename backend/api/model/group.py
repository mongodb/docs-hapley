
from pydantic import BaseModel, Field

class Group(BaseModel):
    """A group of versions."""

    group_label: str = Field(alias="groupLabel")
    included_branches: list[str] = Field(alias="includedBranches")

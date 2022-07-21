from beanie import Document
from pydantic import BaseModel, Field


class PersonalRepos(BaseModel):
    repos: list[str]


class Version(BaseModel):
    pass


class Group(BaseModel):
    """A group of versions."""

    group_label: str = Field(alias="groupLabel")
    included_branches: list[str] = Field(alias="includedBranches")


class DefaultRepoFields:
    """Default fields for a repo document and its fields."""

    name: str = Field(alias="repoName")
    versions: list[Version] = Field(alias="branches")
    groups: list[Group] | None


class Repo(Document):
    """Representation of a docs content repo."""

    class Settings:
        name = "repos_branches"

    name: str = DefaultRepoFields.name
    versions: list[Version] = DefaultRepoFields.versions
    groups: list[Group] | None


class RepoGroupView(BaseModel):
    """Projection focused on groups for a specific repo."""

    name: str = DefaultRepoFields.name
    groups: list[Group] | None

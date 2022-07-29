from beanie import Document
from pydantic import BaseModel, Field, validator

from .group import Group
from .version import Version


class Repo(Document):
    """Representation of a docs content repo."""

    name: str = Field(alias="repoName")
    versions: list[Version] = Field(alias="branches")
    groups: list[Group] | None

    class Settings:
        name = "repos_branches"


class RepoGroupsView(BaseModel):
    """Projection focused on groups for a specific repo."""

    groups: list[Group] | None

    @validator("groups")
    def validate_groups(cls, groups: list[Group] | None) -> list[Group]:
        return groups or []


class RepoVersionsView(BaseModel):
    """Projection focused on versions for a specific repo."""

    versions: list[Version] = Field(alias="branches")


async def insert_new_group(repo: Repo, group: Group) -> Repo:
    await repo.update({"$push": {"groups": group}})
    return group


async def reorder_repo_group(repo: Repo, current_index: int, target_index: int) -> Repo:
    """
    Accepts the current index of the group to move and then moves it to the target
    index.
    """

    repo.groups.insert(target_index, repo.groups.pop(current_index))
    await repo.update({"$set": {"groups": repo.groups}})
    return repo


async def insert_new_version(repo: Repo, version: Version) -> Version:
    await repo.update({"$push": {"branches": version}})
    return version


async def reorder_repo_version(
    repo: Repo, current_index: int, target_index: int
) -> Repo:
    repo.versions.insert(target_index, repo.versions.pop(current_index))
    await repo.update({"$set": {"branches": repo.versions}})
    return repo

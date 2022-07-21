from beanie import Document
from fastapi import HTTPException, status
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
    """Default fields for a repo document and its views."""

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


class RepoGroupsView(BaseModel):
    """Projection focused on groups for a specific repo."""

    groups: list[Group] | None


class RepoNotFound(HTTPException):
    def __init__(self, repo_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The repo {repo_name} does not exist.",
        )


async def find_one_repo(repo_name: str) -> Repo | None:
    repo = await Repo.find_one(Repo.name == repo_name)
    return repo


async def insert_new_group(repo_name: str, group: Group) -> None:
    repo = await find_one_repo(repo_name)

    if not repo:
        raise RepoNotFound(repo_name)

    await repo.update({"$push": {"groups": group}})


async def set_groups(repo_name: str, groups: list[Group]) -> None:
    repo = await find_one_repo(repo_name)

    if not repo:
        raise RepoNotFound(repo_name)

    await repo.update({"$set": {"groups": groups}})

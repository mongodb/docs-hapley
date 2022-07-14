from beanie import Document
from pydantic import BaseModel


# TODO: this needs to be fixed in a follow-up according to schema analysis
class Branch(BaseModel):
    name: str
    publishOriginalBranchName: bool
    active: bool
    aliases: list[str]
    gitBranchName: str
    urlSlug: str
    urlAlias: list[str]
    isStableBranch: bool
    buildsWithSnooty: bool | None


class Bucket(BaseModel):
    regression: str
    dev: str
    stg: str
    prd: str
    dotcomstg: str
    dotcomprd: str


class Url(BaseModel):
    regression: str
    dev: str
    stg: str
    prd: str
    dotcomstg: str
    dotcomprd: str


class Prefix(BaseModel):
    stg: str
    prd: str
    dotcomstg: str
    dotcomprd: str


class SearchCategory(BaseModel):
    categoryName: str
    categoryTitle: str


class Group(BaseModel):
    groupLabel: str
    includedBranches: list[str]


class Repo(Document):
    class Settings:
        name = "repos_branches"

    repoName: str
    project: str | None
    branches: list[Branch]
    buckets: Bucket
    url: Url
    prefix: Prefix
    search: SearchCategory | None
    groups: list[Group] | None

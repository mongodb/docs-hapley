from beanie import Document
from pydantic import BaseModel


class PersonalRepos(BaseModel):
    repos: list[str]


class Entitlement(Document):
    class Settings:
        name = "entitlements"

    email: str
    github_username: str
    repos: list[str]
    slack_user_id: str
    okta_id: str | None


async def get_user_entitlements(user: str) -> list[str]:
    # Use email for now, but we should probably use the immutable okta_id in the future.
    personal_repos = await Entitlement.find_one(Entitlement.email == user).project(
        PersonalRepos
    )
    return personal_repos.repos

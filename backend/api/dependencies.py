from fastapi import Depends, Request

from api.exceptions import RepoNotFound, UserNotEntitled

from .model.entitlement import Entitlement, PersonalRepos
from .model.repo import Repo


def get_request_user_email(request: Request) -> str:
    """Returns the email address of the user initiating a request."""

    return request.state.user.email


async def get_user_entitlements(
    user_email: str = Depends(get_request_user_email),
) -> PersonalRepos:
    # Use email for now, but we should probably use the immutable okta_id in the future.
    return await Entitlement.find_one(Entitlement.email == user_email).project(
        PersonalRepos
    )


async def check_if_user_entitled_to_repo(
    repo_name: str, entitled_repos: PersonalRepos = Depends(get_user_entitlements)
) -> None:
    """Raises an HTTP exception if the user is not entitled to the repo being accessed."""

    # Entitlements are in the form of <org>/<repo_name> but repo documents do not
    # care about the org owner.
    possible_repo_names = set([f"10gen/{repo_name}", f"mongodb/{repo_name}"])
    if not possible_repo_names & set(entitled_repos.repos):
        raise UserNotEntitled(repo_name)


async def find_one_repo(repo_name: str) -> Repo:
    repo = await Repo.find_one(Repo.name == repo_name)
    if not repo:
        raise RepoNotFound(repo_name)
    return repo

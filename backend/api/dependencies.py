from fastapi import Request

from api.model.entitlement import get_user_entitlements
from api.exceptions import UserNotEntitled


def get_request_user_email(request: Request) -> str:
    """Returns the email address of the user initiating a request."""

    return request.state.user.email


async def check_if_user_entitled_to_repo(request: Request, repo_name: str) -> None:
    """Raises an HTTP exception if the user is not entitled to the repo being accessed."""

    entitled_repos = await get_user_entitlements(get_request_user_email(request))

    # Entitlements are in the form of <org>/<repo_name> but repo documents do not
    # care about the org owner.
    possible_repo_names = set([f"10gen/{repo_name}", f"mongodb/{repo_name}"])
    if not possible_repo_names & set(entitled_repos):
        raise UserNotEntitled()

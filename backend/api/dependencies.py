from fastapi import HTTPException, Request, status

from api.model.entitlement import get_user_entitlements


class UserNotEntitled(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not entitled to this docs content repo.",
        )


def get_request_user_email(request: Request) -> str:
    """Returns the email address of the user initiating a request."""

    return request.state.user.email


async def check_if_user_entitled_to_repo(request: Request, repo_name: str) -> None:
    """Raises an HTTP exception if the user is not entitled to the repo being accessed."""

    entitled_repos = await get_user_entitlements(get_request_user_email(request))
    print(entitled_repos)

    entitlement_found = False

    # Entitlements are in the form of <org>/<repo_name> but repo documents do not
    # care about the org owner.
    possible_owners = ["10gen", "mongodb"]
    for owner in possible_owners:
        full_repo_name = owner + "/" + repo_name

        if full_repo_name in entitled_repos:
            entitlement_found = True

    if not entitlement_found:
        raise UserNotEntitled()

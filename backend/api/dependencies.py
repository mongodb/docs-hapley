
from bson import ObjectId, errors
from fastapi import Depends, Request

from api.core.validators.valid_group import ValidGroup
from api.core.validators.valid_reorder_payload import ValidReorderPayload
from api.core.validators.valid_version import ValidVersion
from api.exceptions import (
    RepoNotFound,
    UserNotEntitled,
    ValidationError,
    VersionNotFound,
)


from .models.entitlement import Entitlement, PersonalRepos
from .models.group import Group
from .models.payloads import ReorderItemPayload
from .models.repo import Repo
from .models.version import Version, VersionIn


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


async def convert_to_object_id(version_id: str) -> ObjectId:
    try:
        return ObjectId(version_id)
    except errors.InvalidId:
        raise ValidationError(
            message="Invalid ObjectId.",
            errors=[f"{version_id} is not a valid 24-byte hex string."],
        )


async def find_one_version(
    object_id: ObjectId = Depends(convert_to_object_id),
    repo: Repo = Depends(find_one_repo),
) -> Version:
    # Could potentially move query to the database layer via aggregation pipeline.
    version = list(filter(lambda v: v.id == object_id, repo.versions))
    if not version:
        raise VersionNotFound(object_id)
    return version[0]


async def new_version_validator(
    new_version: VersionIn, repo: Repo = Depends(find_one_repo)
) -> ValidVersion:
    return ValidVersion(version=new_version, repo=repo)


async def update_version_validator(
    updated_version: VersionIn,
    version_id: ObjectId = Depends(convert_to_object_id),
    repo: Repo = Depends(find_one_repo),
) -> ValidVersion:
    updated_version = Version(**updated_version.dict(), id=version_id)
    return ValidVersion(version=updated_version, repo=repo)

async def new_group_validator(
    new_group: Group, repo: Repo = Depends(find_one_repo)
) -> ValidGroup:
    return ValidGroup(group=new_group, repo=repo)


async def reorder_version_validator(
    reordering: ReorderItemPayload, repo: Repo = Depends(find_one_repo)
) -> ValidReorderPayload:
    return ValidReorderPayload[Version](
        repo=repo,
        reordering_list=repo.versions,
        current_index=reordering.current_index,
        target_index=reordering.target_index,
    )


async def reorder_group_validator(
    reordering: ReorderItemPayload, repo: Repo = Depends(find_one_repo)
) -> ValidReorderPayload:
    return ValidReorderPayload[Group](
        repo=repo,
        reordering_list=repo.groups,
        current_index=reordering.current_index,
        target_index=reordering.target_index,
    )

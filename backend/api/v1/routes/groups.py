from fastapi import APIRouter, Depends, status

from api.core.validators.valid_group import ValidGroup
from api.core.validators.valid_reorder_payload import ValidReorderPayload
from api.dependencies import (
    check_if_user_entitled_to_repo,
    find_one_repo,
    new_group_validator,
    reorder_group_validator,
)
from api.exceptions import ErrorResponse
from api.models.group import Group
from api.models.repo import Repo, RepoGroupsView, insert_new_group, reorder_repo_group

GROUPS_INDEX_PATH = "/"

router = APIRouter(
    dependencies=[Depends(check_if_user_entitled_to_repo)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User is not entitled to the repo.",
            "model": ErrorResponse,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Repo not found.",
            "model": ErrorResponse,
        },
    },
)


@router.get(
    GROUPS_INDEX_PATH,
    response_model=RepoGroupsView,
    description="Get all groups for a specific repo",
)
async def read_groups(repo: Repo = Depends(find_one_repo)):
    return repo


@router.post(
    GROUPS_INDEX_PATH,
    response_model=Group,
    description="Create a new group for a specific repo",
)
async def create_group(new_group_params: ValidGroup = Depends(new_group_validator)):
    new_group = await insert_new_group(
        repo=new_group_params.repo, group=new_group_params.group
    )
    return new_group


@router.put(
    GROUPS_INDEX_PATH,
    description="Move a group to a new position in the list",
    response_model=RepoGroupsView,
)
async def reorder_group(
    reorder_params: ValidReorderPayload = Depends(reorder_group_validator),
):
    updated_repo = await reorder_repo_group(
        repo=reorder_params.repo,
        current_index=reorder_params.current_index,
        target_index=reorder_params.target_index,
    )
    return updated_repo

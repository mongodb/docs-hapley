from fastapi import APIRouter, Depends, status

from api.dependencies import check_if_user_entitled_to_repo, find_one_repo
from api.exceptions import ErrorResponse
from api.model.group import Group
from api.model.payloads import ReorderItemPayload
from api.model.repo import Repo, RepoGroupsView, insert_new_group, reorder_groups

GROUPS_INDEX_PATH = "/"

router = APIRouter(
    dependencies=[Depends(check_if_user_entitled_to_repo)],
    tags=["groups"],
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


@router.get(GROUPS_INDEX_PATH, response_model=RepoGroupsView)
async def read_groups(repo: Repo = Depends(find_one_repo)):
    return repo


@router.post(GROUPS_INDEX_PATH, response_model=Group)
async def create_group(group: Group, repo: Repo = Depends(find_one_repo)):
    await insert_new_group(repo, group)
    return group


@router.put(GROUPS_INDEX_PATH)
async def update_groups(body: ReorderItemPayload, repo: Repo = Depends(find_one_repo)):
    await reorder_groups(repo, body.current_index, body.target_index)

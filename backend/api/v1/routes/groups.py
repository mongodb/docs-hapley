from fastapi import APIRouter, Depends

from api.dependencies import check_if_user_entitled_to_repo, find_one_repo
from api.model.repo import Repo, RepoGroupsView, insert_new_group, reorder_groups
from api.model.group import Group
from api.model.payloads import ReorderItemPayload

GROUPS_INDEX_PATH = "/"

router = APIRouter(dependencies=[Depends(check_if_user_entitled_to_repo)])


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

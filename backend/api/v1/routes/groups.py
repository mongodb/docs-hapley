from fastapi import APIRouter, Depends

from api.dependencies import check_if_user_entitled_to_repo
from api.model.payloads import ReorderItemPayload
from api.model.repo import Group, Repo, RepoGroupsView, insert_new_group, reorder_groups

GROUPS_INDEX_PATH = "/"

router = APIRouter(dependencies=[Depends(check_if_user_entitled_to_repo)])


@router.get(GROUPS_INDEX_PATH, response_model=RepoGroupsView)
async def read_groups(repo_name: str):
    return await Repo.find_one(Repo.name == repo_name).project(RepoGroupsView)


@router.post(GROUPS_INDEX_PATH, response_model=Group)
async def create_group(repo_name: str, group: Group):
    await insert_new_group(repo_name, group)
    return group


@router.put(GROUPS_INDEX_PATH)
async def update_groups(repo_name: str, body: ReorderItemPayload):
    await reorder_groups(repo_name, body.current_index, body.target_index)

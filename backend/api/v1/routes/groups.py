from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import check_if_user_entitled_to_repo
from api.model.repo import Group, Repo, RepoGroupsView, insert_new_group, reorder_groups

router = APIRouter()


class UpdateGroupsBody(BaseModel):
    current_index: int = Field(alias="currentIndex")
    target_index: int = Field(alias="targetIndex")


@router.get(
    "/",
    response_model=RepoGroupsView,
    dependencies=[Depends(check_if_user_entitled_to_repo)],
)
async def read_groups(repo_name: str):
    return await Repo.find_one(Repo.name == repo_name).project(RepoGroupsView)


@router.post(
    "/",
    response_model=Group,
    dependencies=[Depends(check_if_user_entitled_to_repo)],
)
async def create_group(repo_name: str, group: Group):
    await insert_new_group(repo_name, group)
    return group


@router.put("/", dependencies=[Depends(check_if_user_entitled_to_repo)])
async def update_groups(repo_name: str, body: UpdateGroupsBody):
    await reorder_groups(repo_name, body.current_index, body.target_index)

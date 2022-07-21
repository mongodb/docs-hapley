from fastapi import APIRouter, Depends

from api.model.repo import Repo, RepoGroupView, Group, insert_new_group
from api.dependencies import check_if_user_entitled_to_repo

router = APIRouter()


@router.get(
    "/",
    response_model=RepoGroupView,
    dependencies=[Depends(check_if_user_entitled_to_repo)],
)
async def read_groups(repo_name: str):
    return await Repo.find_one(Repo.name == repo_name).project(RepoGroupView)


@router.post(
    "/",
    dependencies=[Depends(check_if_user_entitled_to_repo)],
)
async def create_group(repo_name: str, group: Group):
    await insert_new_group(repo_name, group)
    return group

from fastapi import APIRouter, Depends

from api.model.repo import Repo, RepoGroupsView, Group, insert_new_group, set_groups
from api.dependencies import check_if_user_entitled_to_repo

router = APIRouter()


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
async def update_groups(repo_name: str, body: RepoGroupsView):
    await set_groups(repo_name, body.groups)

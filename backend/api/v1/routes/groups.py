from fastapi import APIRouter, Depends

from api.model.repo import Repo, RepoGroupView
from api.dependencies import check_if_user_entitled_to_repo

router = APIRouter()


@router.get(
    "/",
    response_model=RepoGroupView,
    tags=["groups"],
    dependencies=[Depends(check_if_user_entitled_to_repo)],
)
async def read_groups(repo_name: str):
    return await Repo.find_one(Repo.name == repo_name).project(RepoGroupView)

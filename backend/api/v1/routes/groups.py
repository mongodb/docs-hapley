from fastapi import APIRouter

from api.model.repo import Repo, RepoGroupView

router = APIRouter()


@router.get("/", response_model=RepoGroupView, tags=["groups"])
async def read_groups(repo_name: str):
    return await Repo.find_one(Repo.name == repo_name).project(RepoGroupView)

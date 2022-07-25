from fastapi import APIRouter, Request
from . import repo_versions
from ...model.entitlement import Entitlement
from ...model.repo import PersonalRepos

router = APIRouter()

router.include_router(repo_versions.router)

@router.get("/", response_model=PersonalRepos, tags=["repos"])
async def read_repos(request: Request):
    return await Entitlement.find_one(Entitlement.email == request.state.user.email)

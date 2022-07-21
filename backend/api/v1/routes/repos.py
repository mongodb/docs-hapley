from fastapi import APIRouter, Request

from ...model.entitlement import Entitlement, PersonalRepos
from . import groups

PARAM_REPO_NAME = "{repo_name}"

router = APIRouter()
router.include_router(
    groups.router, prefix=f"/{PARAM_REPO_NAME}/groups", tags=["groups"]
)


@router.get("/", response_model=PersonalRepos, tags=["repos"])
async def read_repos(request: Request):
    return await Entitlement.find_one(Entitlement.email == request.state.user.email)

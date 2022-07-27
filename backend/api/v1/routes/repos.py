from fastapi import APIRouter, Depends

from api.dependencies import get_request_user_email

from ...model.entitlement import Entitlement, PersonalRepos
from . import groups

PARAM_REPO_NAME = "{repo_name}"

router = APIRouter()
router.include_router(
    groups.router, prefix=f"/{PARAM_REPO_NAME}/groups", tags=["groups"]
)


@router.get("/", response_model=PersonalRepos, tags=["repos"])
async def read_repos(email: str = Depends(get_request_user_email)):
    return await Entitlement.find_one(Entitlement.email == email)

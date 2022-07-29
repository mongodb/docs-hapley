from fastapi import APIRouter, Depends

from api.dependencies import get_user_entitlements

from ...models.entitlement import PersonalRepos
from . import groups, versions

PARAM_REPO_NAME = "{repo_name}"

router = APIRouter()
router.include_router(
    groups.router, prefix=f"/{PARAM_REPO_NAME}/groups", tags=["groups"]
)
router.include_router(
    versions.router, prefix=f"/{PARAM_REPO_NAME}/versions"
)


@router.get("/", response_model=PersonalRepos, tags=["repos"])
async def read_repos(repos: PersonalRepos = Depends(get_user_entitlements)):
    return repos

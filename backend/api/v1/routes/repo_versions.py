from fastapi import APIRouter, Depends

from ...models.repo import (
    Repo,
    RepoVersionsView,
    Version,
    find_one_repo,
    insert_new_version,
    new_version_validator,
    reorder_repo_version,
    reorder_validator,
)

router = APIRouter(dependencies=[Depends(find_one_repo)])
ENDPOINT = "/{repo_name}/versions"


@router.get(
    ENDPOINT,
    response_model=RepoVersionsView,
    tags=["versions"],
    description="Get versions for a repo for which you have access",
)
async def read_versions(repo: Repo = Depends(find_one_repo)):
    return repo


@router.post(
    ENDPOINT,
    response_model=Version,
    response_model_by_alias=False,
    tags=["versions"],
    description="Append a new version for a repo for which you have access",
)
async def create_version(new_version_params: dict = Depends(new_version_validator)):
    
    new_version = await insert_new_version(**new_version_params)
    return new_version


@router.put(
    ENDPOINT,
    response_model=RepoVersionsView,
    response_model_by_alias=False,
    tags=["versions"],
    description="Takes a current index and new index to move a version to a new position",
)
async def reorder_version(reorder_params: dict = Depends(reorder_validator)):
    updated_repo = await reorder_repo_version(**reorder_params)
    return updated_repo

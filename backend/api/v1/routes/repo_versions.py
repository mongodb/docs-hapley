from fastapi import APIRouter, Depends
from ...core.util.base_error import ErrorResponse

from ...models.repo import (
    Repo,
    RepoVersionsView,
    find_one_repo,
    insert_new_version,
    new_version_validator,
    reorder_repo_version,
    reorder_validator,
)

router = APIRouter(dependencies=[Depends(find_one_repo)], tags=["versions"], responses={
    404: {"description": "The repo specified by `repo_name` does not exist.", "model": ErrorResponse},
})
ENDPOINT = "/{repo_name}/versions"


@router.get(
    ENDPOINT,
    response_model=RepoVersionsView,
    description="Get versions for a repo for which you have access",
)
async def read_versions(repo: Repo = Depends(find_one_repo)):
    return repo


@router.post(
    ENDPOINT,
    response_model=RepoVersionsView,
    description="Append a new version for a repo for which you have access",
)
async def create_version(new_version_params: dict = Depends(new_version_validator)):
    with_new_version = await insert_new_version(**new_version_params)
    return with_new_version


@router.put(
    ENDPOINT,
    response_model=RepoVersionsView,
    description="Takes a current index and new index to move a version to a new position",
)
async def reorder_version(reorder_params: dict = Depends(reorder_validator)):
    updated_repo = await reorder_repo_version(**reorder_params)
    return updated_repo
